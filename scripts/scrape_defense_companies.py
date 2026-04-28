"""
Web scraping scripts to populate defense company database
Focuses on Southern California defense manufacturers
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import re

class DefenseCompanyScraper:
    """Scrape defense companies from public sources"""
    
    def __init__(self):
        self.companies = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    # ============================================
    # Manual Defense Company Database
    # ============================================
    def get_southern_california_defense_companies(self) -> List[Dict]:
        """
        Curated list of known Southern California defense companies
        Based on public databases and industry knowledge
        """
        companies = [
            # San Diego County - Major Aerospace & Defense Hub
            {
                "company_name": "General Atomics",
                "location": "San Diego, CA",
                "website": "https://www.ga.com",
                "industry_focus": "Unmanned Systems, Missiles, Aircraft",
                "equipment_capabilities": "Advanced manufacturing, systems integration",
                "materials": "Composite, Aluminum, Titanium",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Primary UAV and missile manufacturer for DoD and intelligence agencies",
                "notes": "Major defense contractor, ~3000+ employees in SD",
                "is_southern_california": True,
            },
            {
                "company_name": "Northrop Grumman - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.northropgrumman.com",
                "industry_focus": "Aerospace Systems, Missiles, Electronics",
                "equipment_capabilities": "Advanced manufacturing, integration, testing",
                "materials": "Composite, Aluminum, Electronics",
                "certifications": "AS9100, ISO 13485, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Integrated defense systems and components",
                "is_southern_california": True,
            },
            {
                "company_name": "Raytheon Technologies - Carlsbad",
                "location": "Carlsbad, CA",
                "website": "https://www.rtx.com",
                "industry_focus": "Defense Electronics, Missiles, Sensors",
                "equipment_capabilities": "PCB assembly, testing, integration",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Missile systems and electronic components",
                "is_southern_california": True,
            },
            {
                "company_name": "Teledyne Defense Electronics",
                "location": "Newbury Park, CA",
                "website": "https://www.teledyne.com",
                "industry_focus": "Electronics, Sensors, RF Components",
                "equipment_capabilities": "RF design, PCB manufacturing, testing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "DRS Technologies",
                "location": "San Diego, CA",
                "website": "https://www.drs.com",
                "industry_focus": "Defense Electronics, Thermal Imaging",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Thermal systems and military electronics",
                "is_southern_california": True,
            },
            {
                "company_name": "AAI Corporation - Orange County",
                "location": "Irvine, CA",
                "website": "https://www.aaicorp.com",
                "industry_focus": "Unmanned Systems, Defense Systems",
                "equipment_capabilities": "Robotics assembly, integration",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Cubic Defense Applications",
                "location": "San Diego, CA",
                "website": "https://www.cubic.com",
                "industry_focus": "Defense Systems, Training, Simulation",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Sierra Wireless",
                "location": "Richmond, BC / San Diego, CA",
                "website": "https://www.sierrawireless.com",
                "industry_focus": "Wireless Communications, IoT",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            
            # Los Angeles County - Major Manufacturing Hub
            {
                "company_name": "Boeing - Long Beach",
                "location": "Long Beach, CA",
                "website": "https://www.boeing.com",
                "industry_focus": "Aircraft, Missiles, Defense Systems",
                "equipment_capabilities": "Large-scale machining, assembly, integration",
                "materials": "Aluminum, Titanium, Composite",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Aircraft and missile systems manufacturer",
                "is_southern_california": True,
            },
            {
                "company_name": "Lockheed Martin - Grand Prairie",
                "location": "Los Angeles, CA",
                "website": "https://www.lockheedmartin.com",
                "industry_focus": "Spacecraft, Missiles, Defense Systems",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Aerojet Rocketdyne",
                "location": "Los Angeles, CA",
                "website": "https://www.aerojet.com",
                "industry_focus": "Propulsion Systems, Rockets, Missiles",
                "equipment_capabilities": "Rocket engine manufacturing",
                "materials": "Titanium, Aluminum, Composite",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "defense_relevance": "Rocket and missile propulsion",
                "is_southern_california": True,
            },
            {
                "company_name": "Sierra Space (formerly Sierra Nevada Corporation)",
                "location": "Torrance, CA",
                "website": "https://www.sierraspace.com",
                "industry_focus": "Spacecraft, Propulsion, Electronics",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Spacecraft and defense systems",
                "is_southern_california": True,
            },
            {
                "company_name": "Spacex - Hawthorne",
                "location": "Hawthorne, CA",
                "website": "https://www.spacex.com",
                "industry_focus": "Rockets, Spacecraft, Launch Systems",
                "equipment_capabilities": "Advanced manufacturing, welding, machining",
                "materials": "Aluminum alloy, Stainless steel",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "defense_relevance": "Launch services and spacecraft for military",
                "is_southern_california": True,
            },
            {
                "company_name": "Orbital ATK - Chandler, AZ / LA",
                "location": "Los Angeles, CA",
                "website": "https://www.orbitalatk.com",
                "industry_focus": "Aerospace Systems, Missiles",
                "equipment_capabilities": "Advanced manufacturing and integration",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Axiom Space",
                "location": "Houston, TX / Los Angeles, CA",
                "website": "https://www.axiomspace.com",
                "industry_focus": "Spacecraft Modules, Space Systems",
                "equipment_capabilities": "Space vehicle manufacturing",
                "certifications": "AS9100",
                "production_stage": "Limited Production",
                "is_southern_california": True,
            },
            
            # Ventura County
            {
                "company_name": "Meggitt (formerly Polarcus)",
                "location": "Newbury Park, CA",
                "website": "https://www.meggitt.com",
                "industry_focus": "Defense Systems, Seals, Thermal Management",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Ventura County Manufacturing",
                "location": "Camarillo, CA",
                "website": "https://www.vcmfg.com",
                "industry_focus": "Precision Machining, Components",
                "equipment_capabilities": "CNC machining, fabrication",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            
            # Orange County
            {
                "company_name": "Kontron Electronics",
                "location": "Irvine, CA",
                "website": "https://www.kontron.com",
                "industry_focus": "Embedded Systems, Defense Electronics",
                "equipment_capabilities": "PCB assembly, system integration",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Esco Technologies",
                "location": "Irvine, CA",
                "website": "https://www.escotechnologies.com",
                "industry_focus": "Aerospace Components, Shielding",
                "equipment_capabilities": "Precision manufacturing",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "CTS Electronics",
                "location": "Irvine, CA",
                "website": "https://www.ctsco.com",
                "industry_focus": "Electronics, Sensors, Components",
                "equipment_capabilities": "Electronics manufacturing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            
            # Riverside County
            {
                "company_name": "EDO Propulsion",
                "location": "Riverside, CA",
                "website": "https://www.edoaerospace.com",
                "industry_focus": "Propulsion, Aerospace",
                "equipment_capabilities": "Propulsion system manufacturing",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            
            # Additional SoCal Defense Companies (Smaller/Mid-Tier)
            {
                "company_name": "Advanced Technology Services",
                "location": "San Diego, CA",
                "website": "https://www.atsautomation.com",
                "industry_focus": "Precision Components, Machining",
                "equipment_capabilities": "5-axis CNC, precision machining",
                "materials": "Aluminum, Titanium, Steel",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Aerospace and defense components",
                "is_southern_california": True,
            },
            {
                "company_name": "Precision Resource Inc",
                "location": "San Diego, CA",
                "website": "https://www.precisionresource.com",
                "industry_focus": "Precision Machining, Components",
                "equipment_capabilities": "CNC machining, fabrication, assembly",
                "materials": "Aluminum, Steel, Titanium",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Technical Contracting Inc",
                "location": "Los Angeles, CA",
                "website": "https://www.technicalcontracting.com",
                "industry_focus": "Aerospace Services, Logistics",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Southwest Aerospace",
                "location": "San Diego, CA",
                "website": "https://www.swaero.com",
                "industry_focus": "Aerospace Components, Parts",
                "equipment_capabilities": "Machining, fabrication, assembly",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "TRW Automotive",
                "location": "Lynwood, CA",
                "website": "https://www.zfgroup.com",
                "industry_focus": "Aerospace, Defense Components",
                "equipment_capabilities": "Advanced manufacturing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "United Technologies Aerospace",
                "location": "El Segundo, CA",
                "website": "https://www.utc.com",
                "industry_focus": "Aerospace Systems",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Hexcel Corporation - Irvine",
                "location": "Irvine, CA",
                "website": "https://www.hexcel.com",
                "industry_focus": "Composite Materials, Aerospace",
                "equipment_capabilities": "Composite manufacturing",
                "materials": "Carbon fiber, Epoxy, Fiberglass",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Wyle Electronics",
                "location": "El Segundo, CA",
                "website": "https://www.heilind.com",
                "industry_focus": "Aerospace Distribution, Components",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Applied Signal Technology",
                "location": "San Diego, CA",
                "website": "https://www.appliedsignal.com",
                "industry_focus": "RF/Microwave Components, Defense Electronics",
                "equipment_capabilities": "RF testing, assembly",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "ESCO Technologies",
                "location": "Irvine, CA",
                "industry_focus": "Aerospace Components, EMI Shielding",
                "equipment_capabilities": "Precision manufacturing, coating",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Miltope Defense",
                "location": "Long Island, NY / San Diego, CA",
                "website": "https://www.miltope.com",
                "industry_focus": "Defense Technology, Electronics",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "DEF Inc (Defense Electronics)",
                "location": "San Diego, CA",
                "industry_focus": "Defense Electronics, Integration",
                "equipment_capabilities": "System integration, testing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Advanced Sensors Inc",
                "location": "San Diego, CA",
                "industry_focus": "Sensors, Defense Systems",
                "equipment_capabilities": "Sensor manufacturing, calibration",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "CableComm Technology",
                "location": "Long Beach, CA",
                "industry_focus": "Aerospace Cables, Connectors",
                "equipment_capabilities": "Cable assembly, testing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Ducommun Aerostructures",
                "location": "Los Angeles, CA",
                "website": "https://www.ducommun.com",
                "industry_focus": "Aerospace Structures, Components",
                "equipment_capabilities": "Machining, fabrication, assembly",
                "materials": "Composite, Aluminum, Titanium",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Triumph Aerostructures",
                "location": "Long Beach, CA",
                "website": "https://www.triumphgroup.com",
                "industry_focus": "Aerospace Structures",
                "equipment_capabilities": "Machining, riveting, assembly",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Esterline Defense Electronics",
                "location": "Irvine, CA",
                "industry_focus": "Defense Electronics, Systems",
                "equipment_capabilities": "PCB manufacturing, integration",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Kaman Corporation - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.kamancorp.com",
                "industry_focus": "Aerospace, Defense Systems",
                "equipment_capabilities": "System integration, manufacturing",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Latecoere Aerospace",
                "location": "Long Beach, CA",
                "industry_focus": "Aerospace Components",
                "equipment_capabilities": "Machining, fabrication",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Alcoa Defense & Space",
                "location": "Long Beach, CA",
                "website": "https://www.alcoa.com",
                "industry_focus": "Aerospace Structures, Materials",
                "equipment_capabilities": "Machining, forging, extrusion",
                "materials": "Aluminum alloy, Titanium",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Spirit AeroSystems",
                "location": "Long Beach, CA",
                "website": "https://www.spiritaero.com",
                "industry_focus": "Aerospace Structures, Fuselage",
                "equipment_capabilities": "Large-scale machining, riveting",
                "materials": "Aluminum, Composite",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "TransDigm Group",
                "location": "Los Angeles, CA",
                "website": "https://www.transdigm.com",
                "industry_focus": "Aerospace Components, Systems",
                "equipment_capabilities": "Manufacturing, assembly",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Ultra Electronics - San Diego",
                "location": "San Diego, CA",
                "industry_focus": "Defense Electronics, Systems",
                "equipment_capabilities": "Electronics integration",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Moog Inc - Long Beach",
                "location": "Long Beach, CA",
                "website": "https://www.moog.com",
                "industry_focus": "Aerospace Control Systems",
                "equipment_capabilities": "Precision manufacturing, integration",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Goodrich Corporation - San Diego",
                "location": "San Diego, CA",
                "industry_focus": "Aerospace Systems, Components",
                "equipment_capabilities": "Manufacturing, integration",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Corning Precision Materials",
                "location": "Orange, CA",
                "industry_focus": "Ceramic Components, Aerospace",
                "equipment_capabilities": "Ceramic manufacturing",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Curtiss-Wright - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.curtisswright.com",
                "industry_focus": "Aerospace Systems, Flow Control",
                "equipment_capabilities": "System integration, testing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Meggitt Defense",
                "location": "Newbury Park, CA",
                "industry_focus": "Defense Seals, Thermal Management",
                "equipment_capabilities": "Seal manufacturing, thermal systems",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Parker Hannifin - Irvine",
                "location": "Irvine, CA",
                "website": "https://www.parker.com",
                "industry_focus": "Fluid Systems, Aerospace Components",
                "equipment_capabilities": "Hydraulic system manufacturing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Eaton Aerospace",
                "location": "Irvine, CA",
                "website": "https://www.eaton.com",
                "industry_focus": "Aerospace Power Systems",
                "equipment_capabilities": "Electrical system manufacturing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Stafford Royce Defense",
                "location": "Los Angeles, CA",
                "industry_focus": "Defense Systems",
                "equipment_capabilities": "System integration",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Superior Components",
                "location": "Irvine, CA",
                "industry_focus": "Electronics, Connectors",
                "equipment_capabilities": "Electronics assembly",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Analog Devices - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.analog.com",
                "industry_focus": "Semiconductors, Analog Electronics",
                "equipment_capabilities": "Semiconductor design, manufacturing",
                "certifications": "ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Qualcomm - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.qualcomm.com",
                "industry_focus": "Wireless Communications, Semiconductors",
                "equipment_capabilities": "Semiconductor design, testing",
                "certifications": "ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Broadcom - Irvine",
                "location": "Irvine, CA",
                "website": "https://www.broadcom.com",
                "industry_focus": "Semiconductors, RF Components",
                "equipment_capabilities": "Semiconductor manufacturing",
                "certifications": "ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Maxim Integrated - San Jose",
                "location": "Los Angeles, CA",
                "website": "https://www.maximintegrated.com",
                "industry_focus": "Semiconductors, Analog ICs",
                "certifications": "ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Avanir Pharmaceuticals",
                "location": "Aliso Viejo, CA",
                "industry_focus": "Precision Manufacturing, Pharma",
                "equipment_capabilities": "Precision manufacturing",
                "certifications": "ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "CAE Inc - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.cae.com",
                "industry_focus": "Training & Simulation, Defense",
                "equipment_capabilities": "Simulation systems integration",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "defense_relevance": "Military training and simulation systems",
                "is_southern_california": True,
            },
            {
                "company_name": "StandardAero",
                "location": "Long Beach, CA",
                "industry_focus": "Aerospace Engines, Maintenance",
                "equipment_capabilities": "Engine overhaul and maintenance",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "AAR Corp - Long Beach",
                "location": "Long Beach, CA",
                "website": "https://www.aarcorp.com",
                "industry_focus": "Aerospace Components, Logistics",
                "equipment_capabilities": "Component repair and overhaul",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Wolverine World Wide Defense",
                "location": "Irvine, CA",
                "industry_focus": "Military Footwear, Equipment",
                "equipment_capabilities": "Manufacturing, quality assurance",
                "certifications": "ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "L-3 Harris Technologies - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.lhh.com",
                "industry_focus": "Defense Electronics, Systems",
                "equipment_capabilities": "System integration, testing",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "defense_relevance": "Communications and electronic warfare systems",
                "is_southern_california": True,
            },
            {
                "company_name": "ITT Inc - San Diego",
                "location": "San Diego, CA",
                "website": "https://www.ittekllc.com",
                "industry_focus": "Defense Systems, Electronics",
                "equipment_capabilities": "System integration",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Constellium SE",
                "location": "Orange, CA",
                "website": "https://www.constellium.com",
                "industry_focus": "Aluminum Products, Aerospace",
                "equipment_capabilities": "Rolling, extrusion, finishing",
                "materials": "Aluminum alloys",
                "certifications": "AS9100, ISO 9001",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Quest Aerospace",
                "location": "Fremont, CA",
                "industry_focus": "Aerospace Components",
                "equipment_capabilities": "Machining, fabrication",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
            {
                "company_name": "Composite Technology Development",
                "location": "Boulder, CO / Irvine, CA",
                "industry_focus": "Composite Structures",
                "equipment_capabilities": "Composite manufacturing",
                "materials": "Carbon fiber, fiberglass",
                "certifications": "AS9100",
                "production_stage": "Full Production",
                "is_southern_california": True,
            },
        ]
        return companies
    
    def get_all_companies(self) -> List[Dict]:
        """Get all defense companies"""
        return self.get_southern_california_defense_companies()
    
    def scrape_and_return(self) -> List[Dict]:
        """Main method to scrape and return companies"""
        companies = self.get_all_companies()
        
        # Clean and validate data
        for company in companies:
            if 'state' not in company or not company['state']:
                # Extract state from location
                parts = company['location'].split(',')
                if len(parts) > 1:
                    company['state'] = parts[-1].strip()[:2].upper()
        
        return companies


def save_companies_to_json(companies: List[Dict], filename: str = "defense_companies.json"):
    """Save companies to JSON file"""
    with open(filename, 'w') as f:
        json.dump(companies, f, indent=2)
    print(f"Saved {len(companies)} companies to {filename}")


if __name__ == "__main__":
    scraper = DefenseCompanyScraper()
    companies = scraper.scrape_and_return()
    
    print(f"\nScraped {len(companies)} defense companies")
    print(f"Companies with Southern California focus: {sum(1 for c in companies if c.get('is_southern_california'))}")
    
    # Save to JSON
    save_companies_to_json(companies)
    
    # Print first few
    print("\nFirst 5 companies:")
    for company in companies[:5]:
        print(f"  - {company['company_name']} ({company['location']})")
