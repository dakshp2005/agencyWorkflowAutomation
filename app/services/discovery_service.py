import google.generativeai as genai
from app.models.lead import Lead
from app.extensions import db
from app.services.ai_utils import extract_json

class DiscoveryService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def discover_leads(self, domain_topic: str) -> list:
        """
        Uses Gemini to identify 5 high-potential companies in a given domain.
        In a production environment, this would integrate with a Search/Prospecting API.
        """
        prompt = f"""
        Identify 5 real, high-potential companies/startups in the '{domain_topic}' industry 
        that would likely need marketing, automation, or consulting services.
        
        For each company, provide:
        - Name
        - Company Name
        - Website (representative URL)
        - Contact Email (if easily guessable or found, e.g. info@company.com, else null)
        - Brief Description
        - Industry
        
        Return ONLY a JSON list of objects with these keys: 
        ["name", "company", "website", "email", "description", "industry"]
        """
        
        try:
            response = self.model.generate_content(prompt)
            lead_data_list = extract_json(response.text)
            
            if not lead_data_list or not isinstance(lead_data_list, list):
                print(f"[DiscoveryService] AI returned invalid JSON list: {response.text}")
                return []
            
            created_leads = []
            for item in lead_data_list:
                # Basic ICP Scoring logic (ML-simulated for now)
                score_result = self.score_icp(item)
                
                lead = Lead(
                    name=item.get("name"),
                    company=item.get("company"),
                    website=item.get("website"),
                    email=item.get("email"),
                    description=item.get("description"),
                    industry=item.get("industry"),
                    domain_topic=domain_topic,
                    icp_score=score_result["score"],
                    icp_reasoning=score_result["reasoning"]
                )
                db.session.add(lead)
                created_leads.append(lead)
            
            db.session.commit()
            return created_leads
        except Exception as e:
            print(f"[DiscoveryService] Error during discovery: {e}")
            return []

    def score_icp(self, lead_data: dict) -> dict:
        """
        Calculates an ICP score (0-100) based on company fit criteria.
        Uses Gemini as a zero-shot classifier for scoring reasoning.
        """
        description = lead_data.get("description", "")
        
        prompt = f"""
        Evaluate this company for an 'Ideal Customer Profile' (ICP) match for a B2B Agency.
        The agency provides AI, Automation, and Outreach services.
        
        Company: {lead_data.get('company')}
        Industry: {lead_data.get('industry')}
        Description: {description}
        
        Rate the match from 0-100 (score) and provide a one-sentence reasoning.
        Return ONLY JSON: {{"score": 85, "reasoning": "..."}}
        """
        
        try:
            response = self.model.generate_content(prompt)
            data = extract_json(response.text)
            if data and "score" in data:
                return data
            raise ValueError("Invalid ICP score format")
        except Exception as e:
            print(f"[DiscoveryService] ICP Scoring Error: {e}")
            return {"score": 50, "reasoning": "Standard match based on industry focus."}

discovery_service = DiscoveryService()
