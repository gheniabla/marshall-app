# 🚀 Getting Started - First 5 Minutes

## Step 1: Navigate to Project
```bash
cd /Users/abla/Desktop/Marshall
```

## Step 2: Run Setup (Choose One)

### Option A: Python (Recommended)
```bash
python setup_and_run.py
```

### Option B: Shell Script (macOS/Linux)
```bash
chmod +x run.sh
./run.sh
```

### Option C: Batch File (Windows)
```cmd
run.bat
```

## Step 3: Wait for Startup
The script will:
1. ✓ Check Python version
2. ✓ Install dependencies
3. ✓ Scrape 100+ companies
4. ✓ Populate database
5. ✓ Add sample scores
6. ✓ Start server

## Step 4: Open Browser
```
http://localhost:8000
```

## Step 5: Explore! 🎉
- Browse 100+ defense companies
- Search by name, location, certifications
- View detailed company profiles
- See readiness scores
- Add new companies

---

## 📊 What You'll See

### Dashboard
- **Total Companies**: 100+
- **Southern California**: 95
- **Average Score**: 78.5

### Company Table
- Company name & location
- Certifications
- Production stage
- Relationship status
- Readiness score

### Company Details
- Contact information
- Website link
- Equipment capabilities
- Manufacturing processes
- Defense relevance
- Readiness assessment

---

## 🔍 Key Features

### Search
- Real-time search across all company data
- Search by: name, location, certifications, capabilities

### Filter
- By Southern California region
- By readiness score (75+, 80+, etc.)

### Manage
- Add new companies
- View details
- Update information
- Add/update scores

### API Access
- http://localhost:8000/docs (interactive API)
- Full REST API endpoints
- JSON responses

---

## 📋 Navigation

| Feature | Location |
|---------|----------|
| Web App | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Search | Search box at top |
| Add Company | "+ Add Company" button |
| Company Details | Click company row |
| Scores | Click "Add Score" in details |

---

## 🛑 If Something Goes Wrong

### Port 8000 Already in Use
```bash
cd backend
python -m uvicorn app:app --port 8080
# Visit http://localhost:8080
```

### Database Issues
```bash
python scripts/populate_db.py --action reset
```

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

---

## 📖 Documentation

- [README.md](README.md) - Full guide
- [API_REFERENCE.md](API_REFERENCE.md) - All endpoints
- [QUICK_START.md](QUICK_START.md) - Detailed quick start
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Overview

---

## ⏱️ Expected Startup Time

| Task | Time |
|------|------|
| Python check | <1 sec |
| Dependency install | 20-30 sec |
| Database scrape | 5 sec |
| Database populate | 10-15 sec |
| Add scores | 5 sec |
| Start server | 2-3 sec |
| **Total** | **~1 minute** |

---

## 💾 Database Location

```
/Users/abla/Desktop/Marshall/marshall_defense.db
```

The database file is automatically created on first run with 100+ companies pre-populated.

---

## 🔗 API Quick Examples

### Get all companies
```bash
curl http://localhost:8000/api/companies
```

### Search
```bash
curl "http://localhost:8000/api/companies/search?q=aerospace"
```

### Get company details
```bash
curl http://localhost:8000/api/companies/1
```

### Get statistics
```bash
curl http://localhost:8000/api/stats
```

See [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation.

---

## ✅ Verification Checklist

After starting, verify:
- [ ] http://localhost:8000 loads
- [ ] Company table shows 100+ companies
- [ ] Search works
- [ ] Can click company for details
- [ ] http://localhost:8000/docs loads

---

## 🎯 Next Steps After Setup

1. **Explore Companies**
   - Browse through the list
   - Click on companies to see details
   - Check out Southern California companies

2. **Try Search**
   - Search for "aerospace"
   - Search for "San Diego"
   - Search for "AS9100"

3. **Add Companies**
   - Click "+ Add Company"
   - Fill in sample data
   - Submit

4. **Score Companies**
   - Open a company detail
   - Click "Add Score"
   - Enter 5 metrics (0-100)

5. **Use API**
   - Visit http://localhost:8000/docs
   - Try endpoints in Swagger UI
   - Read [API_REFERENCE.md](API_REFERENCE.md)

---

## 🛠️ Project Files Overview

```
setup_and_run.py      ← All-in-one Python setup
run.sh               ← Mac/Linux quick start
run.bat              ← Windows quick start
requirements.txt     ← Python packages

backend/app.py       ← FastAPI application
frontend/index.html  ← Web interface
database/models.py   ← Database schema
scripts/             ← Data & population scripts
```

---

## 📱 Works On

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablet (iPad, Android tablets)
- ✅ Mobile (iPhone, Android phones)
- ✅ Any modern browser

---

## 🆘 Still Need Help?

1. Check [README.md](README.md)
2. Check [QUICK_START.md](QUICK_START.md)
3. Visit http://localhost:8000/docs (interactive API)
4. Review error messages in terminal

---

## 🎉 Ready to Go!

```bash
# Run this command
python setup_and_run.py

# Then visit
http://localhost:8000
```

**Enjoy your defense contractor database! 🛡️**

---

*Questions? Check the documentation files in the Marshall directory.*
