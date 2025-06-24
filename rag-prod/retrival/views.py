# qa_bot/views.py
from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from django.shortcuts import render

def home(request):
    return render(request, 'qa_bot/home.html')
from django.shortcuts import redirect

def redirect_to_upload(request):
    return redirect('upload')
from django.http import HttpResponse

# Load environment variables
load_dotenv()

# Initialize LLM
groq_api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(temperature=0.1, groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")
vector_search = None
def upload_pdf(request):
    global vector_search
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['pdf_file']
            documents = []

            try:
                # Load and process the PDF
                pdf_reader = PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        doc = Document(page_content=text)
                        documents.append(doc)
                    else:
                        return HttpResponse({"error": "Some pages couldn't be extracted from the PDF."})

                # Split the text into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    separators=["\n\n", "-", "\n", " ", ".", ",", "\u200b", "\uff0c", "\u3001", "\uff0e", "\u3002", ""],
                    chunk_size=1000,
                    chunk_overlap=0,
                )
                texts = text_splitter.split_documents(documents)
                print("completed_text_splitting")

                # Generate embeddings
                embeddings = FastEmbedEmbeddings()
                print("embieddings_stored")

                # Store embeddings in Qdrant
                qdrant_api_key = os.getenv('QDRANT_API_KEY')
                qdrant_url = os.getenv('QDRANT_URL')
                vector_search = Qdrant.from_documents(
                    texts, embeddings, url=qdrant_url, prefer_grpc=True, api_key=qdrant_api_key, collection_name="sample_transtest"
                )
                print("completed_vector_search")

                # Store only necessary data in session
                request.session['qdrant_collection'] = "sample_transtest"  # collection name
                request.session['qdrant_url'] = qdrant_url  # URL
                request.session.modified = True

                return redirect('ask_question')

            except Exception as e:
                return render(request, 'upload.html', {"form": form, "error": str(e)})

    else:
        form = PDFUploadForm()

    return render(request, 'upload.html', {"form": form})
def ask_question(request):
    
    if request.method == "POST":
        query = request.POST.get('question', '').strip()
        if query:
            try:
                # Check if we have session data for the vector store
                collection_name = request.session.get('qdrant_collection')
                qdrant_url = request.session.get('qdrant_url')
                
                print(f"Session data - Collection: {collection_name}, URL: {qdrant_url}")
                
                if not collection_name or not qdrant_url:
                    return render(request, 'ask_question.html', {"error": "No PDF has been uploaded yet. Please upload a PDF first."})
                
                # Recreate the vector store from session data
                embeddings = FastEmbedEmbeddings()
                qdrant_api_key = os.getenv('QDRANT_API_KEY')
                
                # Create Qdrant client
                qdrant_client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key,
                    prefer_grpc=True,
                    check_compatibility=False
                )
                
                vector_store = Qdrant(
                    client=qdrant_client,
                    collection_name=collection_name,
                    embeddings=embeddings
                )

                # Set up prompt template
                prompt = PromptTemplate(
                    template="""Based on the following context, provide a comprehensive and well-structured answer to the question. 
                    Format your response using markdown for better readability:
                    - Use bullet points for lists
                    - Use numbered lists for sequential information
                    - Use **bold** for important points
                    - Use proper headings (##, ###) when appropriate
                    - Organize information logically
                    
                    Context: {context}
                    
                    Question: {question}
                    
                    Answer:""",
                    input_variables=["context", "question"]
                )
                
                # Initialize QA chain
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
                    chain_type="stuff",
                    chain_type_kwargs={"prompt": prompt}
                )
                
                # Get the answer
                result = qa_chain.invoke({"query": query})
                answer = result.get("result", "No answer found")
                return render(request, 'ask_question.html', {"query": query, "answer": answer})
            except Exception as e:
                return render(request, 'ask_question.html', {"query": query, "error": f"Error: {e}"})
    return render(request, 'ask_question.html')