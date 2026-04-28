"""
Populate database with scraped defense companies
"""
import sys
import os
import json
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.models import Company, ReadinessScore, get_session_maker, init_db
from scripts.scrape_defense_companies import DefenseCompanyScraper


def populate_database_from_scraper(batch_size: int = 50):
    """
    Scrape defense companies and populate database
    """
    # Initialize database
    init_db()
    
    # Get database session
    SessionLocal = get_session_maker()
    db = SessionLocal()
    
    try:
        # Scrape companies
        print("Scraping defense companies...")
        scraper = DefenseCompanyScraper()
        companies_data = scraper.scrape_and_return()
        
        print(f"Found {len(companies_data)} companies")
        
        # Add to database
        added_count = 0
        duplicate_count = 0
        
        for company_data in companies_data:
            # Check if company already exists
            existing = db.query(Company).filter(
                Company.company_name.ilike(company_data['company_name'])
            ).first()
            
            if existing:
                duplicate_count += 1
                continue
            
            # Create company record
            company = Company(
                company_name=company_data['company_name'],
                location=company_data['location'],
                state=company_data.get('state'),
                website=company_data.get('website'),
                phone=company_data.get('phone'),
                contact_person=company_data.get('contact_person'),
                contact_email=company_data.get('contact_email'),
                industry_focus=company_data.get('industry_focus'),
                manufacturing_processes=company_data.get('manufacturing_processes'),
                equipment_capabilities=company_data.get('equipment_capabilities'),
                materials=company_data.get('materials'),
                certifications=company_data.get('certifications'),
                production_stage=company_data.get('production_stage'),
                defense_relevance=company_data.get('defense_relevance'),
                notes=company_data.get('notes'),
                relationship_status=company_data.get('relationship_status', 'cold'),
                is_southern_california=company_data.get('is_southern_california', False)
            )
            
            db.add(company)
            added_count += 1
            
            # Commit in batches
            if added_count % batch_size == 0:
                db.commit()
                print(f"  Added {added_count} companies...")
        
        # Final commit
        db.commit()
        
        print(f"\n✓ Successfully added {added_count} companies to database")
        print(f"  Skipped {duplicate_count} duplicates")
        
        # Print statistics
        total = db.query(Company).count()
        socal_count = db.query(Company).filter(Company.is_southern_california == True).count()
        
        print(f"\nDatabase Statistics:")
        print(f"  Total companies: {total}")
        print(f"  Southern California: {socal_count}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def populate_database_from_json(json_file: str = "defense_companies.json"):
    """
    Populate database from JSON file
    """
    # Initialize database
    init_db()
    
    # Get database session
    SessionLocal = get_session_maker()
    db = SessionLocal()
    
    try:
        if not os.path.exists(json_file):
            print(f"File not found: {json_file}")
            return
        
        print(f"Loading companies from {json_file}...")
        with open(json_file, 'r') as f:
            companies_data = json.load(f)
        
        print(f"Found {len(companies_data)} companies")
        
        added_count = 0
        duplicate_count = 0
        
        for company_data in companies_data:
            # Check if company already exists
            existing = db.query(Company).filter(
                Company.company_name.ilike(company_data['company_name'])
            ).first()
            
            if existing:
                duplicate_count += 1
                continue
            
            # Create company record
            company = Company(
                company_name=company_data['company_name'],
                location=company_data['location'],
                state=company_data.get('state'),
                website=company_data.get('website'),
                phone=company_data.get('phone'),
                contact_person=company_data.get('contact_person'),
                contact_email=company_data.get('contact_email'),
                industry_focus=company_data.get('industry_focus'),
                manufacturing_processes=company_data.get('manufacturing_processes'),
                equipment_capabilities=company_data.get('equipment_capabilities'),
                materials=company_data.get('materials'),
                certifications=company_data.get('certifications'),
                production_stage=company_data.get('production_stage'),
                defense_relevance=company_data.get('defense_relevance'),
                notes=company_data.get('notes'),
                relationship_status=company_data.get('relationship_status', 'cold'),
                is_southern_california=company_data.get('is_southern_california', False)
            )
            
            db.add(company)
            added_count += 1
            
            # Commit in batches
            if added_count % 50 == 0:
                db.commit()
                print(f"  Added {added_count} companies...")
        
        db.commit()
        
        print(f"\n✓ Successfully added {added_count} companies to database")
        if duplicate_count > 0:
            print(f"  Skipped {duplicate_count} duplicates")
        
        # Print statistics
        total = db.query(Company).count()
        socal_count = db.query(Company).filter(Company.is_southern_california == True).count()
        
        print(f"\nDatabase Statistics:")
        print(f"  Total companies: {total}")
        print(f"  Southern California: {socal_count}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def reset_database():
    """
    Reset database (delete all records)
    """
    from database.models import get_db_engine
    
    engine = get_db_engine()
    
    # Drop all tables
    from database.models import Base
    Base.metadata.drop_all(bind=engine)
    print("Database reset")
    
    # Recreate tables
    init_db()
    print("Database re-initialized")


def add_sample_scores():
    """
    Add sample readiness scores for companies
    """
    SessionLocal = get_session_maker()
    db = SessionLocal()
    
    try:
        companies = db.query(Company).all()
        added_count = 0
        
        for i, company in enumerate(companies[:30]):  # Add scores to first 30
            # Check if score already exists
            existing_score = db.query(ReadinessScore).filter(
                ReadinessScore.company_id == company.id
            ).first()
            
            if existing_score:
                continue
            
            # Generate realistic scores based on company
            import random
            
            # Larger companies get higher scores
            base_score = 60 + (random.randint(0, 30))
            
            score = ReadinessScore(
                company_id=company.id,
                manufacturing_maturity=base_score + random.randint(-10, 10),
                quality_compliance_readiness=base_score + random.randint(-10, 10),
                production_scalability=base_score + random.randint(-10, 10),
                defense_applicability=base_score + random.randint(-10, 10),
                responsiveness_operational_readiness=base_score + random.randint(-10, 10),
                assessment_notes="Initial assessment",
                assessed_by="System"
            )
            
            score.calculate_overall_score()
            db.add(score)
            added_count += 1
            
            if (i + 1) % 10 == 0:
                db.commit()
                print(f"Added {added_count} scores...")
        
        db.commit()
        print(f"✓ Added {added_count} readiness scores")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Populate Marshall database")
    parser.add_argument(
        "--action",
        choices=["populate", "populate-json", "reset", "add-scores"],
        default="populate",
        help="Action to perform"
    )
    parser.add_argument(
        "--json-file",
        default="defense_companies.json",
        help="JSON file to load companies from"
    )
    
    args = parser.parse_args()
    
    if args.action == "populate":
        populate_database_from_scraper()
    elif args.action == "populate-json":
        populate_database_from_json(args.json_file)
    elif args.action == "reset":
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        if confirm.lower() == "yes":
            reset_database()
            populate_database_from_scraper()
    elif args.action == "add-scores":
        add_sample_scores()
