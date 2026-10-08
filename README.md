# 🏥 CareTrack — Smart Clinic Operations Dashboard

CareTrack is a premium, lightweight clinic operations dashboard built with Flask, SQLite, HTML, CSS and JavaScript.

## ✨ Features

- Real-time appointment queue
- Patient appointment management
- Doctor availability dashboard
- Appointment status tracking
- Waiting-time estimation
- Interactive patient-flow chart
- Search and status filters
- Responsive premium UI
- SQLite persistence
- Automated tests with Pytest
- Docker support
- GitHub Actions-ready project structure

## 🛠️ Tech Stack

Python · Flask · SQLite · HTML5 · CSS3 · JavaScript · Chart.js · Pytest · Docker · GitHub Actions

## ▶️ Run locally

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
python app.py
```

Open:
http://127.0.0.1:5000

## 🧪 Run tests

```bash
pytest
```

## 🐳 Docker

```bash
docker build -t caretrack .
docker run -p 5000:5000 caretrack
```

## 📌 Note

This is an academic/demo operations dashboard. It does not provide medical diagnosis or clinical decision-making.
