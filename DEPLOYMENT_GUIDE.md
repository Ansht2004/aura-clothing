# 🚀 Aura Haute Atelier - Online Deployment Guide

Aura Haute Atelier is configured as a **Universal Full-Stack Application**. The production Flask backend automatically serves the compiled React 19 frontend (`frontend/dist`), the REST API, the SQLite database, and the Gemini AI Suite under a single domain with zero CORS issues.

---

## 🌟 Method 1: Render.com (Recommended — 100% Free Full-Stack)

Render gives you a free live URL (e.g., `https://aura-haute-atelier.onrender.com`) with automated SSL certificates (HTTPS).

### Steps:
1. **Create a GitHub Repository**:
   - Go to [GitHub.com](https://github.com) and click **New Repository** (name it `aura-clothing`).
   - Upload the project files (or upload `aura-clothing-compressed.zip` contents).

2. **Sign up on Render**:
   - Go to [render.com](https://render.com) and sign in with your GitHub account.

3. **Create New Web Service**:
   - Click **New +** -> **Web Service**.
   - Select your `aura-clothing` repository.
   - Configure the following fields:
     - **Name**: `aura-haute-atelier` (or your preferred name)
     - **Region**: Oregon (US West) or Frankfurt (EU)
     - **Branch**: `main`
     - **Runtime**: `Python 3`
     - **Build Command**:
       ```bash
       cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
       ```
     - **Start Command**:
       ```bash
       gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT
       ```
     - **Instance Type**: `Free`

4. **Environment Variables**:
   Under **Environment Variables**, click **Add Environment Variable**:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (click generate or type any secret key)
   - `JWT_SECRET_KEY` = (click generate or type any secret key)
   - `GEMINI_API_KEY` = `your_google_gemini_api_key` *(optional: local fallback activates automatically if empty)*

5. **Deploy**:
   - Click **Deploy Web Service**.
   - Render will build the React frontend, install dependencies, and launch your site live online in ~2 minutes!

---

## 🌟 Method 2: PythonAnywhere (100% Free — No GitHub Required)

If you don't have Git installed, you can deploy in under 5 minutes by uploading your zip file directly to PythonAnywhere.

### Steps:
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and create a free beginner account (username e.g., `ansh46`).
2. Go to the **Files** tab:
   - Upload `aura-clothing-compressed.zip`.
   - Open a **Bash Console** in PythonAnywhere and run:
     ```bash
     unzip aura-clothing-compressed.zip -d aura-clothing
     cd aura-clothing/backend
     pip install -r requirements.txt
     ```
3. Go to the **Web** tab:
   - Click **Add a new web app** -> **Manual configuration** -> **Python 3.10 / 3.11**.
   - In **Code** section, set Source code directory to: `/home/yourusername/aura-clothing/backend`.
   - Click the **WSGI configuration file** link, replace its content with:
     ```python
     import sys, os
     path = '/home/yourusername/aura-clothing/backend'
     if path not in sys.path:
         sys.path.append(path)
     from app import app as application
     ```
4. Click the green **Reload** button at the top.
5. Your website is live at `https://yourusername.pythonanywhere.com`!

---

## 🌟 Method 3: Split Deployment (Vercel Frontend + Render Backend)

If you prefer deploying the React frontend on Vercel's global Edge CDN:

1. **Deploy Backend on Render**:
   - Root directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Note the backend URL (e.g. `https://aura-api.onrender.com`).

2. **Deploy Frontend on Vercel**:
   - Go to [vercel.com](https://vercel.com) and import the repository.
   - Root Directory: `frontend`
   - Environment Variable:
     - `VITE_API_BASE_URL` = `https://aura-api.onrender.com/api`
   - Click **Deploy**. Vercel gives you an instant `https://aura-apparel.vercel.app` domain.

---

## 🔐 Credentials on Live Site
- **Admin Email**: `tanwaransh46@gmail.com`
- **Admin Password**: `Tanwar@12`
- **Role**: Sole Administrator with access to the Admin Dashboard (`/admin`).
