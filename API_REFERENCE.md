# API Reference - Marshall Defense Database

## Base URL
```
http://localhost:8000/api
```

## Endpoints Reference

### Statistics

#### Get Database Statistics
```
GET /api/stats
```

**Response:**
```json
{
  "total_companies": 100,
  "southern_california_count": 95,
  "companies_with_scores": 30,
  "average_readiness": 78.5,
  "top_5_companies": [...]
}
```

---

### Companies

#### List All Companies
```
GET /api/companies
```

**Query Parameters:**
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100, max: 500) - Number of records to return
- `southern_california_only` (bool, default: false) - Filter to SoCal only
- `state` (string, optional) - Filter by state code (e.g., "CA")

**Example:**
```bash
GET /api/companies?skip=0&limit=50&southern_california_only=true
```

**Response:**
```json
[
  {
    "id": 1,
    "company_name": "General Atomics",
    "location": "San Diego, CA",
    "state": "CA",
    "website": "https://www.ga.com",
    "phone": null,
    "contact_person": null,
    "contact_email": null,
    "industry_focus": "Unmanned Systems, Missiles, Aircraft",
    "manufacturing_processes": null,
    "equipment_capabilities": "Advanced manufacturing, systems integration",
    "materials": "Composite, Aluminum, Titanium",
    "certifications": "AS9100, ISO 9001",
    "production_stage": "Full Production",
    "defense_relevance": "Primary UAV and missile manufacturer",
    "notes": "Major defense contractor",
    "relationship_status": "cold",
    "is_southern_california": true,
    "readiness_scores": {
      "manufacturing_maturity": 85.0,
      "quality_compliance_readiness": 90.0,
      "production_scalability": 80.0,
      "defense_applicability": 95.0,
      "responsiveness_operational_readiness": 88.0,
      "overall_readiness_score": 87.6
    }
  }
]
```

---

#### Search Companies
```
GET /api/companies/search?q=search_term
```

**Query Parameters:**
- `q` (string, required) - Search term (min 1 character)

**Searches across:**
- Company name
- Location
- Certifications
- Equipment capabilities
- Industry focus

**Example:**
```bash
GET /api/companies/search?q=aerospace
```

---

#### Get Company by ID
```
GET /api/companies/{id}
```

**Parameters:**
- `id` (int, path) - Company ID

**Example:**
```bash
GET /api/companies/1
```

**Response:**
```json
{
  "id": 1,
  "company_name": "General Atomics",
  "location": "San Diego, CA",
  ...
}
```

---

#### Create Company
```
POST /api/companies
```

**Request Body:**
```json
{
  "company_name": "New Defense Corp",
  "location": "Los Angeles, CA",
  "state": "CA",
  "website": "https://example.com",
  "phone": "+1-555-0123",
  "contact_person": "John Doe",
  "contact_email": "john@example.com",
  "industry_focus": "Aerospace, Electronics",
  "manufacturing_processes": "CNC, Welding, Assembly",
  "equipment_capabilities": "5-axis CNC, Cleanroom",
  "materials": "Aluminum, Titanium",
  "certifications": "AS9100, ISO 9001",
  "production_stage": "Full Production",
  "defense_relevance": "Aerospace components manufacturer",
  "notes": "Established 2010",
  "relationship_status": "cold",
  "is_southern_california": true
}
```

**Required Fields:**
- `company_name`
- `location`

**Response:** 201 Created
```json
{
  "id": 101,
  "company_name": "New Defense Corp",
  ...
}
```

---

#### Update Company
```
PUT /api/companies/{id}
```

**Parameters:**
- `id` (int, path) - Company ID

**Request Body:** (All fields optional)
```json
{
  "location": "Updated Location, CA",
  "relationship_status": "warm",
  "is_southern_california": true
}
```

**Response:** 200 OK
```json
{
  "id": 1,
  "company_name": "General Atomics",
  "location": "Updated Location, CA",
  ...
}
```

---

#### Delete Company
```
DELETE /api/companies/{id}
```

**Parameters:**
- `id` (int, path) - Company ID

**Response:** 200 OK
```json
{
  "status": "deleted"
}
```

---

### Readiness Scores

#### Update/Create Readiness Score
```
POST /api/companies/{id}/readiness
```

**Parameters:**
- `id` (int, path) - Company ID

**Request Body:**
```json
{
  "manufacturing_maturity": 85,
  "quality_compliance_readiness": 90,
  "production_scalability": 80,
  "defense_applicability": 95,
  "responsiveness_operational_readiness": 88,
  "assessment_notes": "Based on facility inspection",
  "assessed_by": "John Smith"
}
```

**All score fields:** (0-100 scale)
- `manufacturing_maturity` - Capability level of manufacturing operations
- `quality_compliance_readiness` - Quality systems and certifications
- `production_scalability` - Ability to scale production
- `defense_applicability` - Relevance to defense work
- `responsiveness_operational_readiness` - Speed and reliability of operations

**Response:** 200 OK
```json
{
  "manufacturing_maturity": 85.0,
  "quality_compliance_readiness": 90.0,
  "production_scalability": 80.0,
  "defense_applicability": 95.0,
  "responsiveness_operational_readiness": 88.0,
  "overall_readiness_score": 87.6,
  "assessment_notes": "Based on facility inspection",
  "assessed_by": "John Smith"
}
```

---

#### Filter by Readiness Score
```
GET /api/companies/filter/by-readiness
```

**Query Parameters:**
- `min_score` (float, default: 0, range: 0-100) - Minimum overall score
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100, max: 500) - Number of records to return

**Example:**
```bash
GET /api/companies/filter/by-readiness?min_score=75&limit=50
```

**Response:**
```json
[
  {
    "id": 1,
    "company_name": "General Atomics",
    "readiness_scores": {
      "overall_readiness_score": 87.6
    },
    ...
  }
]
```

---

### Health Check

#### Server Status
```
GET /health
```

**Response:** 200 OK
```json
{
  "status": "healthy"
}
```

---

## Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Error Responses

**Example Error Response:**
```json
{
  "detail": "Company not found"
}
```

---

## Request Examples

### Using curl

#### Get all companies
```bash
curl http://localhost:8000/api/companies
```

#### Search for aerospace companies
```bash
curl "http://localhost:8000/api/companies/search?q=aerospace"
```

#### Get company #1
```bash
curl http://localhost:8000/api/companies/1
```

#### Add new company
```bash
curl -X POST http://localhost:8000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "New Company",
    "location": "San Diego, CA"
  }'
```

#### Update readiness score
```bash
curl -X POST http://localhost:8000/api/companies/1/readiness \
  -H "Content-Type: application/json" \
  -d '{
    "manufacturing_maturity": 85,
    "quality_compliance_readiness": 90,
    "production_scalability": 80,
    "defense_applicability": 95,
    "responsiveness_operational_readiness": 88
  }'
```

### Using Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Get all companies
response = requests.get(f"{BASE_URL}/companies")
companies = response.json()

# Search companies
response = requests.get(f"{BASE_URL}/companies/search?q=aerospace")
results = response.json()

# Get specific company
response = requests.get(f"{BASE_URL}/companies/1")
company = response.json()

# Add new company
new_company = {
    "company_name": "New Defense Corp",
    "location": "Los Angeles, CA",
    "industry_focus": "Aerospace"
}
response = requests.post(f"{BASE_URL}/companies", json=new_company)
created = response.json()

# Update score
score = {
    "manufacturing_maturity": 85,
    "quality_compliance_readiness": 90,
    "production_scalability": 80,
    "defense_applicability": 95,
    "responsiveness_operational_readiness": 88
}
response = requests.post(f"{BASE_URL}/companies/1/readiness", json=score)
updated_score = response.json()
```

### Using JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000/api";

// Get all companies
fetch(`${BASE_URL}/companies`)
  .then(r => r.json())
  .then(data => console.log(data));

// Add new company
fetch(`${BASE_URL}/companies`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    company_name: "New Company",
    location: "San Diego, CA"
  })
})
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## Pagination

The API supports pagination for list endpoints:

```bash
# First page (0-49)
GET /api/companies?skip=0&limit=50

# Second page (50-99)
GET /api/companies?skip=50&limit=50

# Get specific range
GET /api/companies?skip=100&limit=25
```

---

## Filtering & Search

### By Location
```bash
GET /api/companies?state=CA
GET /api/companies?southern_california_only=true
```

### By Text (Search)
```bash
GET /api/companies/search?q=aerospace
GET /api/companies/search?q=san%20diego
```

### By Readiness Score
```bash
GET /api/companies/filter/by-readiness?min_score=75
GET /api/companies/filter/by-readiness?min_score=80&limit=20
```

---

## Data Types

### Company Object
```typescript
{
  id: number,
  company_name: string,
  location: string,
  state: string | null,
  website: string | null,
  phone: string | null,
  contact_person: string | null,
  contact_email: string | null,
  industry_focus: string | null,
  manufacturing_processes: string | null,
  equipment_capabilities: string | null,
  materials: string | null,
  certifications: string | null,
  production_stage: string | null,
  defense_relevance: string | null,
  notes: string | null,
  relationship_status: string,
  is_southern_california: boolean,
  readiness_scores: ReadinessScore | null
}
```

### Readiness Score Object
```typescript
{
  manufacturing_maturity: number (0-100),
  quality_compliance_readiness: number (0-100),
  production_scalability: number (0-100),
  defense_applicability: number (0-100),
  responsiveness_operational_readiness: number (0-100),
  overall_readiness_score: number (0-100),
  assessment_notes: string | null,
  assessed_by: string | null
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, implement rate limiting:
- Requests per minute per IP
- Requests per user (with authentication)
- Adaptive limiting based on load

---

## CORS

Currently CORS is open to all origins (`allow_origins=["*"]`).

For production, configure in `backend/app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

## Version

**API Version:** 1.0.0

---

For more information, visit http://localhost:8000/docs (Swagger UI) or http://localhost:8000/redoc (ReDoc)
