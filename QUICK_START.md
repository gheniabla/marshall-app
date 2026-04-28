# Quick Start Guide - Marshall Defense Database

## ⚡ 30-Second Start

### macOS/Linux
```bash
chmod +x run.sh
./run.sh
```

### Windows
```bash
run.bat
```

### Manual (Any OS)
```bash
python setup_and_run.py
```

Then open: **http://localhost:8000**

---

## 📊 What You Get

✅ **100+ Defense Companies** - Southern California focused  
✅ **Smart Search** - Find companies by name, location, certifications  
✅ **Readiness Scores** - Assess manufacturing capabilities  
✅ **API Access** - Full REST API for programmatic access  
✅ **Responsive UI** - Works on desktop, tablet, mobile  

---

## 🗂️ Project Structure

```
Marshall/
├── README.md                              ← Full documentation
├── QUICK_START.md                         ← This file
├── API_REFERENCE.md                       ← API endpoints
├── requirements.txt                       ← Python dependencies
├── setup_and_run.py                       ← One-click setup (Python)
├── run.sh                                 ← One-click setup (Mac/Linux)
├── run.bat                                ← One-click setup (Windows)
│
├── backend/
│   ├── app.py                            ← FastAPI application
│   └── __init__.py
│
├── frontend/
│   ├── index.html                        ← Web interface
│   └── __init__.py
│
├── database/
│   ├── models.py                         ← SQLAlchemy models
│   ├── marshall_defense.db               ← SQLite database (created on run)
│   └── __init__.py
│
├── scripts/
│   ├── scrape_defense_companies.py       ← Web scraper
│   ├── populate_db.py                    ← Database population
│   └── __init__.py
│
└── raw-material/
    └── marshall-website.html             ← Original design reference
```

---

## 🎯 Main Features

### 1. **Company Database**
- 100+ curated defense manufacturers
- Southern California focused
- Detailed company profiles
- Contact information
- Capabilities and certifications

### 2. **Readiness Assessment**
- 5-point scoring system
- Manufacturing Maturity
- Quality/Compliance Readiness
- Production Scalability
- Defense Applicability
- Responsiveness/Operational Readiness

### 3. **Search & Filter**
- Real-time text search
- Filter by location
- Filter by readiness score
- Sort by company name

### 4. **REST API**
- List companies
- Search companies
- Get company details
- Create/update companies
- Manage readiness scores
- Get statistics

---

## 📡 API Quick Reference

### Get all companies
```bash
curl http://localhost:8000/api/companies
```

### Search
```bash
curl "http://localhost:8000/api/companies/search?q=aerospace"
```

### Get stats
```bash
curl http://localhost:8000/api/stats
```

### Full API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔧 Common Tasks

### Add a Company
1. Click "+ Add Company" button
2. Fill in company details
3. Click "Add Company"

### View Company Details
1. Click company row in table
2. View full profile
3. Add/update readiness score

### Search Companies
1. Use search box at top
2. Search by: name, location, certifications
3. Results appear in real-time

### Export Companies
```bash
curl http://localhost:8000/api/companies > companies.json
```

---

## 📊 Database Stats

After running setup:
- **Total Companies**: 100+
- **Southern California**: ~95
- **With Scores**: 30+
- **Average Readiness**: ~78

---

## 🚀 Next Steps

1. **Explore the data**
   - Visit http://localhost:8000
   - Browse companies
   - Check out readiness scores

2. **Add your own companies**
   - Click "+ Add Company"
   - Fill in details
   - Submit

3. **Score companies**
   - Open company details
   - Click "Add Score"
   - Enter 5 metrics (0-100)

4. **Use the API**
   - Read [API_REFERENCE.md](API_REFERENCE.md)
   - Build your own tools
   - Integrate with other systems

---

## 🐛 Troubleshooting

### "Port 8000 is already in use"
```bash
cd backend
python -m uvicorn app:app --port 8080
# Then visit http://localhost:8080
```

### Database appears empty
```bash
python scripts/populate_db.py --action populate
python scripts/populate_db.py --action add-scores
```

### Can't access from other machines
```bash
# Server is already set to 0.0.0.0
# Use your machine's IP: http://192.168.x.x:8000
```

### Virtual environment issues
```bash
# Delete and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 💡 Tips

- **Search is powerful**: Try searching for technologies, locations, or certifications
- **Readiness scores matter**: Higher scores indicate production-ready suppliers
- **API is open**: Build custom tools, dashboards, or integrations
- **Data is local**: Everything is in SQLite, portable and private

---

## 📚 Documentation

- **[README.md](README.md)** - Full project documentation
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API endpoints
- **[QUICK_START.md](QUICK_START.md)** - This file

---

## 🆘 Need Help?

1. Check [README.md](README.md) - Comprehensive documentation
2. Check [API_REFERENCE.md](API_REFERENCE.md) - API examples
3. Open http://localhost:8000/docs - Interactive API docs
4. Check terminal output for error messages

---

## 🎉 You're Ready!

Your Marshall Defense Database is ready to use. Start exploring today!

```bash
./run.sh          # macOS/Linux
# or
run.bat           # Windows
# or
python setup_and_run.py  # Any OS
```

**Then visit:** http://localhost:8000

---

**Happy exploring! 🛡️**
