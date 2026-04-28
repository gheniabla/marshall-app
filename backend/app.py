"""
FastAPI Backend for Marshall Defense Company Database
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Add database module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.models import Company, ReadinessScore, ManufacturingNeed, init_db, get_db, get_db_engine

# ============================================
# Pydantic Models (Request/Response Schemas)
# ============================================
class ReadinessScoreSchema(BaseModel):
    manufacturing_maturity: float = 0
    quality_compliance_readiness: float = 0
    production_scalability: float = 0
    defense_applicability: float = 0
    responsiveness_operational_readiness: float = 0
    mrl_level: Optional[int] = None
    assessment_notes: Optional[str] = None
    assessed_by: Optional[str] = None
    
    class Config:
        from_attributes = True


class CompanySchema(BaseModel):
    id: int
    company_name: str
    location: str
    state: Optional[str]
    website: Optional[str]
    phone: Optional[str]
    contact_person: Optional[str]
    contact_email: Optional[str]
    industry_focus: Optional[str]
    manufacturing_processes: Optional[str]
    equipment_capabilities: Optional[str]
    materials: Optional[str]
    certifications: Optional[str]
    production_stage: Optional[str]
    defense_relevance: Optional[str]
    notes: Optional[str]
    relationship_status: str
    readiness_scores: Optional[ReadinessScoreSchema]
    is_southern_california: bool
    active_capacity_status: Optional[str] = "unknown"
    lead_time_days: Optional[int] = None
    itar_registered: Optional[bool] = False
    cmmc_level: Optional[int] = None

    class Config:
        from_attributes = True


class CompanyCreateSchema(BaseModel):
    company_name: str
    location: str
    state: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    industry_focus: Optional[str] = None
    manufacturing_processes: Optional[str] = None
    equipment_capabilities: Optional[str] = None
    materials: Optional[str] = None
    certifications: Optional[str] = None
    production_stage: Optional[str] = None
    defense_relevance: Optional[str] = None
    notes: Optional[str] = None
    relationship_status: str = "cold"
    is_southern_california: bool = False
    active_capacity_status: Optional[str] = "unknown"
    lead_time_days: Optional[int] = None
    itar_registered: Optional[bool] = False
    cmmc_level: Optional[int] = None


class CompanyUpdateSchema(BaseModel):
    location: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    industry_focus: Optional[str] = None
    manufacturing_processes: Optional[str] = None
    equipment_capabilities: Optional[str] = None
    materials: Optional[str] = None
    certifications: Optional[str] = None
    production_stage: Optional[str] = None
    defense_relevance: Optional[str] = None
    notes: Optional[str] = None
    relationship_status: Optional[str] = None
    is_southern_california: Optional[bool] = None
    active_capacity_status: Optional[str] = None
    lead_time_days: Optional[int] = None
    itar_registered: Optional[bool] = None
    cmmc_level: Optional[int] = None


class StatsSchema(BaseModel):
    total_companies: int
    southern_california_count: int
    companies_with_scores: int
    average_readiness: float
    top_5_companies: List[CompanySchema]


# ============================================
# FastAPI App Setup
# ============================================
app = FastAPI(title="Marshall Defense Database API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup():
    init_db()
    print("Starting Marshall Defense Database API...")

    # Auto-seed on first boot when the companies table is empty.
    # Disable with AUTO_SEED=0 (e.g. for tests).
    if os.environ.get("AUTO_SEED", "1") != "0":
        from database.models import get_session_maker
        SessionLocal = get_session_maker()
        db = SessionLocal()
        try:
            if db.query(Company).count() == 0:
                print("Empty database detected — seeding curated SoCal defense companies...")
                from scripts.populate_db import populate_database_from_scraper, add_sample_scores
                populate_database_from_scraper()
                add_sample_scores()
                print("Seed complete.")
        except Exception as e:
            print(f"Auto-seed skipped: {e}")
        finally:
            db.close()


# ============================================
# API Endpoints
# ============================================

# --- Stats Endpoint ---
@app.get("/api/stats", response_model=StatsSchema)
async def get_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    total = db.query(Company).count()
    socal_count = db.query(Company).filter(Company.is_southern_california == True).count()
    with_scores = db.query(Company).filter(Company.readiness_scores != None).count()
    
    # Average readiness score
    avg_readiness = db.query(func.avg(ReadinessScore.overall_readiness_score)).scalar() or 0
    
    # Top 5 companies by readiness score
    top_5 = db.query(Company).join(
        ReadinessScore, Company.id == ReadinessScore.company_id
    ).order_by(ReadinessScore.overall_readiness_score.desc()).limit(5).all()
    
    return {
        "total_companies": total,
        "southern_california_count": socal_count,
        "companies_with_scores": with_scores,
        "average_readiness": float(avg_readiness),
        "top_5_companies": top_5
    }


# --- List Companies ---
@app.get("/api/companies", response_model=List[CompanySchema])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    southern_california_only: bool = False,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all companies with pagination"""
    query = db.query(Company)
    
    if southern_california_only:
        query = query.filter(Company.is_southern_california == True)
    
    if state:
        query = query.filter(Company.state.ilike(state))
    
    companies = query.order_by(Company.company_name).offset(skip).limit(limit).all()
    return companies


# --- Search Companies ---
@app.get("/api/companies/search", response_model=List[CompanySchema])
async def search_companies(
    q: str = Query("", min_length=1),
    db: Session = Depends(get_db)
):
    """Search companies by name, location, certifications, or capabilities"""
    search_term = f"%{q}%"
    companies = db.query(Company).filter(
        or_(
            Company.company_name.ilike(search_term),
            Company.location.ilike(search_term),
            Company.certifications.ilike(search_term),
            Company.equipment_capabilities.ilike(search_term),
            Company.industry_focus.ilike(search_term)
        )
    ).limit(50).all()
    return companies


# --- Get Company by ID ---
@app.get("/api/companies/{company_id}", response_model=CompanySchema)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get company details by ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


# --- Create Company ---
@app.post("/api/companies", response_model=CompanySchema)
async def create_company(
    company: CompanyCreateSchema,
    db: Session = Depends(get_db)
):
    """Create a new company"""
    # Check if company already exists
    existing = db.query(Company).filter(
        Company.company_name.ilike(company.company_name)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")
    
    # Extract state from location if not provided
    state = company.state
    if not state and company.location:
        parts = company.location.split(',')
        if len(parts) > 1:
            state = parts[-1].strip()[:2].upper()
    
    db_company = Company(
        **company.dict(),
        state=state
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


# --- Update Company ---
@app.put("/api/companies/{company_id}", response_model=CompanySchema)
async def update_company(
    company_id: int,
    company: CompanyUpdateSchema,
    db: Session = Depends(get_db)
):
    """Update company information"""
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = company.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


# --- Update Readiness Score ---
@app.post("/api/companies/{company_id}/readiness", response_model=ReadinessScoreSchema)
async def update_readiness_score(
    company_id: int,
    score: ReadinessScoreSchema,
    db: Session = Depends(get_db)
):
    """Update or create readiness score for company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get or create readiness score
    readiness = db.query(ReadinessScore).filter(
        ReadinessScore.company_id == company_id
    ).first()
    
    if not readiness:
        readiness = ReadinessScore(company_id=company_id)
    
    # Update scores
    readiness.manufacturing_maturity = score.manufacturing_maturity
    readiness.quality_compliance_readiness = score.quality_compliance_readiness
    readiness.production_scalability = score.production_scalability
    readiness.defense_applicability = score.defense_applicability
    readiness.responsiveness_operational_readiness = score.responsiveness_operational_readiness
    readiness.mrl_level = score.mrl_level
    readiness.assessment_notes = score.assessment_notes
    readiness.assessed_by = score.assessed_by
    
    # Calculate overall score
    readiness.calculate_overall_score()
    
    db.add(readiness)
    db.commit()
    db.refresh(readiness)
    return readiness


# --- Delete Company ---
@app.delete("/api/companies/{company_id}")
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete a company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(company)
    db.commit()
    return {"status": "deleted"}


# --- Filter by Readiness Score ---
@app.get("/api/companies/filter/by-readiness", response_model=List[CompanySchema])
async def filter_by_readiness(
    min_score: float = Query(0, ge=0, le=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Filter companies by minimum readiness score"""
    companies = db.query(Company).join(
        ReadinessScore, Company.id == ReadinessScore.company_id
    ).filter(
        ReadinessScore.overall_readiness_score >= min_score
    ).order_by(
        ReadinessScore.overall_readiness_score.desc()
    ).offset(skip).limit(limit).all()
    return companies


# ============================================
# Manufacturing Need intake (Need → Match → Verify → Route)
# ============================================
class ManufacturingNeedCreateSchema(BaseModel):
    requester_name: Optional[str] = None
    requester_email: Optional[str] = None
    requester_org: Optional[str] = None
    part_description: str
    process: Optional[str] = None
    material: Optional[str] = None
    quantity: Optional[int] = None
    urgency: str = "standard"
    required_certifications: Optional[str] = None
    geography_constraints: Optional[str] = None
    other_constraints: Optional[str] = None


class ManufacturingNeedSchema(ManufacturingNeedCreateSchema):
    id: int
    status: str

    class Config:
        from_attributes = True


@app.post("/api/needs", response_model=ManufacturingNeedSchema)
async def submit_need(need: ManufacturingNeedCreateSchema, db: Session = Depends(get_db)):
    """Submit a manufacturing need (buyer intake)."""
    db_need = ManufacturingNeed(**need.dict())
    db.add(db_need)
    db.commit()
    db.refresh(db_need)
    return db_need


@app.get("/api/needs", response_model=List[ManufacturingNeedSchema])
async def list_needs(
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """List submitted manufacturing needs, optionally filtered by status."""
    q = db.query(ManufacturingNeed)
    if status:
        q = q.filter(ManufacturingNeed.status == status)
    return q.order_by(ManufacturingNeed.created_at.desc()).offset(skip).limit(limit).all()


@app.post("/api/needs/{need_id}/match", response_model=List[CompanySchema])
async def match_need(need_id: int, top_n: int = Query(5, ge=1, le=25), db: Session = Depends(get_db)):
    """Return a readiness-ranked shortlist for a manufacturing need.

    Mirrors the marshall.us "Match" step: rank manufacturers by overall readiness,
    biased toward active capacity and required certifications.
    """
    need = db.query(ManufacturingNeed).filter(ManufacturingNeed.id == need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Need not found")

    q = db.query(Company).join(ReadinessScore, Company.id == ReadinessScore.company_id)
    if need.required_certifications:
        for cert in [c.strip() for c in need.required_certifications.split(",") if c.strip()]:
            q = q.filter(Company.certifications.ilike(f"%{cert}%"))
    if need.process:
        q = q.filter(or_(
            Company.manufacturing_processes.ilike(f"%{need.process}%"),
            Company.equipment_capabilities.ilike(f"%{need.process}%"),
        ))

    shortlist = q.order_by(ReadinessScore.overall_readiness_score.desc()).limit(top_n).all()
    need.status = "matched"
    db.commit()
    return shortlist


# --- Health Check ---
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# --- Root endpoint (serves frontend) ---
@app.get("/")
async def root():
    """Serve the frontend"""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
        return FileResponse(frontend_path)
    except:
        return {"message": "Welcome to Marshall Defense Database API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
