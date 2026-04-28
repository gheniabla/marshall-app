"""
Database models for Marshall Defense Company Database
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

# Database setup — overridable via DATABASE_URL env var (e.g. Neon Postgres in prod)
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./marshall_defense.db")
# Force the psycopg (v3) driver — we don't ship psycopg2.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
Base = declarative_base()

# ============================================
# Company Profile Model
# ============================================
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), unique=True, index=True)
    location = Column(String(255))  # City, State
    state = Column(String(2), index=True)  # State code (e.g., "CA")
    website = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    contact_person = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    
    # Business Info
    industry_focus = Column(Text, nullable=True)  # e.g., "Aerospace, Defense, Electronics"
    manufacturing_processes = Column(Text, nullable=True)  # JSON or comma-separated
    equipment_capabilities = Column(Text, nullable=True)
    materials = Column(Text, nullable=True)  # e.g., "Aluminum, Titanium, Composites"
    certifications = Column(Text, nullable=True)  # e.g., "AS9100, ISO 9001, ISO 13485"
    production_stage = Column(String(100), nullable=True)  # e.g., "Full production", "Prototype"
    defense_relevance = Column(Text, nullable=True)  # How relevant to defense
    
    # Meta
    notes = Column(Text, nullable=True)
    relationship_status = Column(String(50), default="cold")  # cold, warm, engaged, partner
    is_southern_california = Column(Boolean, default=False)

    # Capacity / activation signals (mirrors marshall.us "Active Capacity" surface)
    active_capacity_status = Column(String(50), default="unknown")  # active, limited, full, unknown
    lead_time_days = Column(Integer, nullable=True)
    itar_registered = Column(Boolean, default=False)
    cmmc_level = Column(Integer, nullable=True)  # 0-3 per CMMC 2.0
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    readiness_scores = relationship("ReadinessScore", uselist=False, back_populates="company")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.company_name}', location='{self.location}')>"


# ============================================
# Readiness Scoring Model
# ============================================
class ReadinessScore(Base):
    __tablename__ = "readiness_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), unique=True, index=True)
    
    # Scoring metrics (0-100 scale)
    manufacturing_maturity = Column(Float, default=0)  # 0-100
    quality_compliance_readiness = Column(Float, default=0)  # 0-100
    production_scalability = Column(Float, default=0)  # 0-100
    defense_applicability = Column(Float, default=0)  # 0-100
    responsiveness_operational_readiness = Column(Float, default=0)  # 0-100

    # MRL — Manufacturing Readiness Level, 1–10. DoD scale Marshall scores against.
    mrl_level = Column(Integer, nullable=True)
    
    # Overall score
    overall_readiness_score = Column(Float, default=0)  # Average of all scores
    
    # Assessment notes
    assessment_notes = Column(Text, nullable=True)
    assessed_by = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="readiness_scores")
    
    def __repr__(self):
        return f"<ReadinessScore(company_id={self.company_id}, overall={self.overall_readiness_score})>"
    
    def calculate_overall_score(self):
        """Calculate overall readiness score as average of all metrics"""
        scores = [
            self.manufacturing_maturity,
            self.quality_compliance_readiness,
            self.production_scalability,
            self.defense_applicability,
            self.responsiveness_operational_readiness
        ]
        self.overall_readiness_score = sum(scores) / len(scores)
        return self.overall_readiness_score


# ============================================
# Manufacturing Need (buyer intake — Need → Match → Verify → Route)
# ============================================
class ManufacturingNeed(Base):
    __tablename__ = "manufacturing_needs"

    id = Column(Integer, primary_key=True, index=True)
    requester_name = Column(String(255), nullable=True)
    requester_email = Column(String(255), nullable=True)
    requester_org = Column(String(255), nullable=True)

    # Structured intake fields per marshall.us submission flow
    part_description = Column(Text)  # part / assembly being sourced
    process = Column(String(255), nullable=True)  # e.g. "5-Axis CNC", "Investment Casting"
    material = Column(String(255), nullable=True)  # e.g. "Aluminum 7075", "Inconel 718"
    quantity = Column(Integer, nullable=True)
    urgency = Column(String(50), default="standard")  # standard, high, critical
    required_certifications = Column(Text, nullable=True)  # AS9100D, Nadcap, CMMC L2, ITAR, ...
    geography_constraints = Column(Text, nullable=True)
    other_constraints = Column(Text, nullable=True)

    # Pipeline status: submitted → matched → verified → routed
    status = Column(String(50), default="submitted", index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ManufacturingNeed(id={self.id}, status='{self.status}')>"


# ============================================
# Database Engine Setup
# ============================================
def get_db_engine():
    """Create and return database engine"""
    if DATABASE_URL.startswith("sqlite"):
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def get_session_maker():
    """Create and return session maker"""
    engine = get_db_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database and create tables"""
    engine = get_db_engine()
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def get_db():
    """Dependency for FastAPI to get database session"""
    SessionLocal = get_session_maker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
