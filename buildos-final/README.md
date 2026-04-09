# BuildOS — Full Stack Construction Management Platform

## Project Structure
```
buildos/
├── app.py               ← Run this. Serves BOTH API and frontend
├── config.py            ← Supabase connection
├── schema.sql           ← Paste into Supabase SQL Editor once
├── requirements.txt     ← pip install -r requirements.txt
├── .env.example         ← Copy to .env and fill in keys
├── routes/
│   ├── projects.py
│   ├── materials.py
│   ├── transactions.py
│   ├── budget.py
│   └── invoices.py
├── templates/           ← All HTML pages (served by Flask)
│   ├── dashboard.html
│   ├── inventory.html
│   ├── finance.html
│   ├── invoices.html
│   ├── projects.html
│   └── mobile.html
└── static/
    └── js/
        └── api.js       ← All API calls to Flask backend
```

## Setup (One Time)

### 1. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Set up Supabase
1. Go to https://supabase.com → New Project
2. SQL Editor → paste schema.sql → Run
3. Settings → API → copy URL and anon key

### 3. Create .env file
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### 4. Run
```bash
python app.py
```

## Pages
| URL | Page |
|-----|------|
| http://localhost:5000 | Dashboard |
| http://localhost:5000/inventory | Inventory |
| http://localhost:5000/finance | Finance |
| http://localhost:5000/invoices | Invoices |
| http://localhost:5000/projects | Projects |
| http://localhost:5000/mobile | Site Engineer (mobile) |
| http://localhost:5000/api/projects/ | API test |
