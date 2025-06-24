# QA-Prod-Project

This repository contains the code for a production-ready PDF Question-Answering (QA) bot using Django, LangChain, Qdrant Cloud, and modern LLMs. This project is featured on the YouTube channel **SaikumarreddyN**.

---

## 📺 YouTube Tutorial
Watch the full step-by-step guide: [Saikumarreddy](https://www.youtube.com/@Saikumarreddyn)

---

## 🛠️ Tech Stack
- Python 3.12
- Django 5.2
- LangChain
- Qdrant Cloud
- Gunicorn
- Docker
- Conda (for local development)

---

## 📝 Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd QA-Prod-Project/rag-prod
```

### 2. Create and Activate Conda Environment (for local development)
```sh
conda create -n rag-prod python=3.12 -y
conda activate rag-prod
```

### 3. Install Requirements
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `rag-prod` directory:
```
GROQ_API_KEY=your_groq_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=https://your-qdrant-url.gcp.cloud.qdrant.io
```
> **Note:** No spaces or quotes around the values.

### 5. Run Django Server (for development)
```sh
python manage.py migrate
python manage.py runserver
```

App will be available at [http://localhost:8000](http://localhost:8000)

---

## 🐳 Docker Instructions (Production)

### 1. Build Docker Image
```sh
docker build -t rag-prod .
```

### 2. Run Docker Container
```sh
docker run -d --env-file .env -p 8000:8000 rag-prod
```

App will be available at [http://localhost:8000](http://localhost:8000)

---

## 📂 Project Structure
```
QA-Prod-Project/
├── rag-prod/
│   ├── retrival/           # Django app for PDF upload & QA
│   ├── rag/                # Django project settings
│   ├── Dockerfile          # Production Docker setup
│   ├── requirements.txt    # Python dependencies
│   ├── .env                # Environment variables (not committed)
│   └── ...
├── README.md               # (This file)
└── ...
```

---

## ⚡ Usage
1. **Upload a PDF** via the web interface.
2. **Ask questions** about the content.
3. **Get instant, context-rich answers** powered by LLMs and Qdrant.

---

## 🧑‍💻 For Contributors
- PRs and issues are welcome!
- For questions, comment on the YouTube video or open an issue here.

---

## 📢 About the Author
This project is created and maintained by **Saikumarreddy**. Subscribe for more AI, ML, and production-ready coding tutorials!

- [YouTube: Saikumarreddy](https://www.youtube.com/@Saikumarreddyn)

---

## 📝 License
This project is licensed under the MIT License.