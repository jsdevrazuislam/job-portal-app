# 🧑‍💼 JobPortal - Django Job Portal

JobPortal is a modern and professional job listing platform built with **Django** and styled using **Tailwind CSS** and **ShadCN UI**. It allows users to **search** and **apply for jobs**, while employers can **post jobs** by subscribing to a **paid plan**.

---

## ✨ Features

### 👨‍💻 For Job Seekers
- 🔍 Browse and filter jobs by category, location, type, etc.
- 🔗 View job details with full descriptions
- 📄 Create and update profile
- 🔐 Secure registration, login, logout, email verification
- 🔑 Forgot/reset password functionality

### 🏢 For Employers
- ✅ Register/Login and manage their company profile
- 💼 Create job listings *(only after purchasing a plan)*
- 📊 View all posted jobs
- 🖼️ Job detail view
- 💳 Plan-based access control for job posting

---

## 🔐 Authentication & User Management
- User Registration with Email Verification
- Login / Logout
- Forgot Password & Reset
- Profile Update
- Separate functionality for Job Seekers and Employers

---

## 💸 Payment System
Employers must purchase a **paid plan** before being able to post jobs. This ensures quality control and helps support the platform.

---

## 🧩 Tech Stack

- **Backend:** Django 4+
- **Frontend:** Tailwind CSS + ShadCN UI
- **Database:** PostgreSQL / SQLite (based on your setup)
- **Auth:** Django's built-in auth system
- **Styling:** Tailwind CSS + ShadCN for modern, accessible UI

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/jobify.git
cd jobify
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
## 🔧 Environment Setup
Create a .env file in your project root:

```bash
DEBUG=False
SECRET_KEY=SECRET_KEY
PASSWORD=PASSWORD
GMAIL=GMAIL
DEFAULT_FROM_EMAIL= DEFAULT_FROM_EMAIL
HOST = HOST
STRIPE_SECRET_KEY=STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY=STRIPE_PUBLISHABLE_KEY
STRIPE_WEBHOOK_SECRET=STRIPE_WEBHOOK_SECRET
# For production, set up real email backend and payment keys
```

## 🚀 Run the Project
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

./tailwindcss -i ./static/input.css -o ./static/output.css --watch