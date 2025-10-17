"""
Synthetic Policy Document Generator

This module generates realistic immigration policy documents from templates and parameters.
Useful for testing, demos, and training scenarios.
"""

import json
import random
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml


class PolicyGenerator:
    """Generates synthetic immigration policy documents."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """Initialize the policy generator.
        
        Args:
            templates_dir: Directory containing policy templates
        """
        self.templates_dir = Path(templates_dir) if templates_dir else Path(__file__).parent / "templates"
        self.visa_types = self._load_visa_types()
        self.policy_templates = self._load_policy_templates()
        
    def _load_visa_types(self) -> Dict[str, Any]:
        """Load visa type definitions."""
        return {
            "visitor": {
                "codes": ["V1", "V2", "V3", "V4", "V5"],
                "purposes": ["tourism", "business", "family_visit", "medical", "transit"],
                "duration_ranges": [(30, 90), (90, 180), (180, 365)],
                "typical_requirements": [
                    "passport_validity", "financial_support", "return_ticket",
                    "accommodation_proof", "travel_insurance"
                ]
            },
            "work": {
                "codes": ["W1", "W2", "W3", "W4", "W5"],
                "purposes": ["skilled_work", "seasonal_work", "intra_company", "entrepreneur"],
                "duration_ranges": [(365, 1095), (1095, 1825)],
                "typical_requirements": [
                    "job_offer", "skills_assessment", "english_proficiency",
                    "health_check", "character_check", "qualifications"
                ]
            },
            "student": {
                "codes": ["S1", "S2", "S3", "S4"],
                "purposes": ["university", "vocational", "language", "research"],
                "duration_ranges": [(180, 365), (365, 1460)],
                "typical_requirements": [
                    "enrollment_confirmation", "financial_capacity", "english_proficiency",
                    "health_insurance", "genuine_student_test"
                ]
            },
            "family": {
                "codes": ["F1", "F2", "F3", "F4"],
                "purposes": ["spouse", "parent", "child", "partner"],
                "duration_ranges": [(365, 1825), (1825, 3650)],
                "typical_requirements": [
                    "relationship_evidence", "sponsor_eligibility", "financial_support",
                    "health_check", "character_check", "accommodation"
                ]
            }
        }
    
    def _load_policy_templates(self) -> Dict[str, str]:
        """Load policy document templates."""
        return {
            "header": """
{visa_name} ({visa_code})
Immigration Instructions

Effective Date: {effective_date}
Version: {version}

OBJECTIVE
{objective}

SCOPE
This instruction applies to applications for {visa_name} visas lodged {scope_details}.
""",
            "eligibility": """
ELIGIBILITY REQUIREMENTS

{visa_code}.5 Basic Requirements
An applicant for a {visa_name} visa must:
{basic_requirements}

{visa_code}.10 Specific Requirements
{specific_requirements}
""",
            "financial": """
FINANCIAL REQUIREMENTS

{visa_code}.15 Financial Support
{financial_requirements}

{visa_code}.20 Income Thresholds
{income_thresholds}
""",
            "health_character": """
HEALTH AND CHARACTER

{visa_code}.25 Health Requirements
{health_requirements}

{visa_code}.30 Character Requirements
{character_requirements}
""",
            "conditions": """
VISA CONDITIONS

{visa_code}.35 Standard Conditions
{standard_conditions}

{visa_code}.40 Special Conditions
{special_conditions}
""",
            "processing": """
PROCESSING REQUIREMENTS

{visa_code}.45 Application Process
{application_process}

{visa_code}.50 Decision Criteria
{decision_criteria}
"""
        }
    
    def generate_policy(self, 
                       visa_category: str,
                       visa_name: str,
                       complexity: str = "medium",
                       custom_params: Optional[Dict[str, Any]] = None) -> str:
        """Generate a complete policy document.
        
        Args:
            visa_category: Type of visa (visitor, work, student, family)
            visa_name: Specific name of the visa
            complexity: Level of complexity (simple, medium, complex)
            custom_params: Custom parameters to override defaults
            
        Returns:
            Complete policy document as string
        """
        if visa_category not in self.visa_types:
            raise ValueError(f"Unknown visa category: {visa_category}")
        
        # Get base parameters
        base_params = self.visa_types[visa_category]
        
        # Generate specific parameters
        params = self._generate_parameters(visa_category, visa_name, complexity, base_params)
        
        # Override with custom parameters
        if custom_params:
            params.update(custom_params)
        
        # Generate document sections
        sections = []
        
        # Header
        sections.append(self.policy_templates["header"].format(**params))
        
        # Eligibility
        sections.append(self.policy_templates["eligibility"].format(**params))
        
        # Financial (if applicable)
        if params.get("has_financial_requirements", True):
            sections.append(self.policy_templates["financial"].format(**params))
        
        # Health and Character
        sections.append(self.policy_templates["health_character"].format(**params))
        
        # Conditions
        sections.append(self.policy_templates["conditions"].format(**params))
        
        # Processing
        sections.append(self.policy_templates["processing"].format(**params))
        
        return "\n".join(sections)
    
    def _generate_parameters(self, 
                           visa_category: str, 
                           visa_name: str, 
                           complexity: str,
                           base_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate parameters for policy document."""
        
        # Basic parameters
        params = {
            "visa_name": visa_name,
            "visa_code": random.choice(base_params["codes"]),
            "effective_date": "1 January 2024",
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}",
            "objective": self._generate_objective(visa_category, visa_name),
            "scope_details": self._generate_scope(visa_category),
        }
        
        # Requirements based on complexity
        complexity_multiplier = {"simple": 0.7, "medium": 1.0, "complex": 1.5}[complexity]
        num_requirements = int(len(base_params["typical_requirements"]) * complexity_multiplier)
        
        selected_requirements = random.sample(
            base_params["typical_requirements"], 
            min(num_requirements, len(base_params["typical_requirements"]))
        )
        
        # Generate requirement text
        params.update({
            "basic_requirements": self._generate_basic_requirements(selected_requirements),
            "specific_requirements": self._generate_specific_requirements(visa_category, complexity),
            "financial_requirements": self._generate_financial_requirements(visa_category),
            "income_thresholds": self._generate_income_thresholds(visa_category),
            "health_requirements": self._generate_health_requirements(complexity),
            "character_requirements": self._generate_character_requirements(),
            "standard_conditions": self._generate_standard_conditions(visa_category),
            "special_conditions": self._generate_special_conditions(visa_category, complexity),
            "application_process": self._generate_application_process(),
            "decision_criteria": self._generate_decision_criteria(complexity)
        })
        
        return params
    
    def _generate_objective(self, visa_category: str, visa_name: str) -> str:
        """Generate visa objective text."""
        objectives = {
            "visitor": f"The {visa_name} visa allows temporary entry for tourism, business, or family visits.",
            "work": f"The {visa_name} visa enables skilled workers to contribute to the economy.",
            "student": f"The {visa_name} visa supports international education and cultural exchange.",
            "family": f"The {visa_name} visa facilitates family reunification and support."
        }
        return objectives.get(visa_category, f"The {visa_name} visa serves specific immigration purposes.")
    
    def _generate_scope(self, visa_category: str) -> str:
        """Generate scope details."""
        return f"on or after the effective date, whether inside or outside the country"
    
    def _generate_basic_requirements(self, requirements: List[str]) -> str:
        """Generate basic requirements list."""
        requirement_text = {
            "passport_validity": "(a) hold a passport valid for at least 6 months;",
            "financial_support": "(b) have sufficient funds for their stay;",
            "return_ticket": "(c) hold a return or onward ticket;",
            "accommodation_proof": "(d) have confirmed accommodation arrangements;",
            "travel_insurance": "(e) hold adequate travel insurance;",
            "job_offer": "(a) have a genuine job offer from an approved employer;",
            "skills_assessment": "(b) have their skills assessed by the relevant authority;",
            "english_proficiency": "(c) meet English language requirements;",
            "health_check": "(d) meet health requirements;",
            "character_check": "(e) meet character requirements;",
            "qualifications": "(f) have relevant qualifications;",
            "enrollment_confirmation": "(a) be enrolled in an approved course;",
            "financial_capacity": "(b) demonstrate financial capacity;",
            "health_insurance": "(c) hold adequate health insurance;",
            "genuine_student_test": "(d) satisfy the genuine student test;",
            "relationship_evidence": "(a) provide evidence of relationship;",
            "sponsor_eligibility": "(b) have an eligible sponsor;",
        }
        
        return "\n".join([requirement_text.get(req, f"({chr(97 + i)}) meet {req.replace('_', ' ')} requirements;") 
                         for i, req in enumerate(requirements)])
    
    def _generate_specific_requirements(self, visa_category: str, complexity: str) -> str:
        """Generate specific requirements based on category and complexity."""
        base_requirements = {
            "visitor": [
                "demonstrate genuine intention to visit temporarily",
                "show ties to home country",
                "not intend to work or study"
            ],
            "work": [
                "demonstrate relevant work experience",
                "meet salary threshold requirements",
                "employer must be approved sponsor"
            ],
            "student": [
                "demonstrate academic progression",
                "maintain full-time enrollment",
                "limit work to permitted hours"
            ],
            "family": [
                "demonstrate ongoing relationship",
                "meet sponsorship obligations",
                "satisfy integration requirements"
            ]
        }
        
        requirements = base_requirements.get(visa_category, ["meet general requirements"])
        
        if complexity == "complex":
            requirements.extend([
                "undergo additional assessment",
                "provide supplementary documentation",
                "attend interview if required"
            ])
        
        return "\n".join([f"({chr(97 + i)}) {req};" for i, req in enumerate(requirements)])
    
    def _generate_financial_requirements(self, visa_category: str) -> str:
        """Generate financial requirements."""
        amounts = {
            "visitor": random.choice([5000, 7500, 10000]),
            "work": random.choice([15000, 20000, 25000]),
            "student": random.choice([20000, 25000, 30000]),
            "family": random.choice([25000, 30000, 35000])
        }
        
        amount = amounts.get(visa_category, 10000)
        
        return f"""Applicants must demonstrate access to funds of at least ${amount:,} or equivalent.
Acceptable evidence includes:
(a) bank statements for the last 3 months;
(b) employment letter with salary details;
(c) sponsorship undertaking with financial evidence."""
    
    def _generate_income_thresholds(self, visa_category: str) -> str:
        """Generate income threshold requirements."""
        if visa_category in ["visitor", "student"]:
            return "No specific income thresholds apply."
        
        thresholds = {
            "work": [45000, 55000, 65000],
            "family": [65000, 85000, 105000]
        }
        
        amounts = thresholds.get(visa_category, [50000])
        threshold_text = []
        
        for i, amount in enumerate(amounts):
            if i == 0:
                threshold_text.append(f"Single applicant: ${amount:,} per annum")
            elif i == 1:
                threshold_text.append(f"Couple: ${amount:,} per annum")
            else:
                threshold_text.append(f"Family with dependents: ${amount:,} per annum")
        
        return "\n".join(threshold_text)
    
    def _generate_health_requirements(self, complexity: str) -> str:
        """Generate health requirements."""
        base_text = """All applicants must meet health requirements including:
(a) medical examination by approved panel physician;
(b) chest X-ray examination;
(c) HIV test if required."""
        
        if complexity == "complex":
            base_text += """
(d) additional specialist examinations if indicated;
(e) health insurance covering pre-existing conditions."""
        
        return base_text
    
    def _generate_character_requirements(self) -> str:
        """Generate character requirements."""
        return """All applicants must meet character requirements including:
(a) police clearance certificates from all countries of residence;
(b) declaration of criminal history;
(c) assessment of risk to community safety."""
    
    def _generate_standard_conditions(self, visa_category: str) -> str:
        """Generate standard visa conditions."""
        conditions = {
            "visitor": [
                "No work permitted",
                "No study for more than 3 months",
                "Must maintain adequate health insurance"
            ],
            "work": [
                "Work only for approved employer",
                "Notify of change in circumstances",
                "Maintain adequate health insurance"
            ],
            "student": [
                "Maintain full-time enrollment",
                "Work limited to 20 hours per week",
                "Maintain adequate health insurance"
            ],
            "family": [
                "Comply with sponsorship arrangements",
                "Notify of change in circumstances",
                "Maintain adequate health insurance"
            ]
        }
        
        visa_conditions = conditions.get(visa_category, ["Comply with visa conditions"])
        return "\n".join([f"({chr(97 + i)}) {condition}" for i, condition in enumerate(visa_conditions)])
    
    def _generate_special_conditions(self, visa_category: str, complexity: str) -> str:
        """Generate special conditions based on complexity."""
        if complexity == "simple":
            return "No special conditions apply."
        
        special_conditions = [
            "Regular reporting to authorities",
            "Restriction on travel to certain areas",
            "Participation in integration programs"
        ]
        
        if complexity == "complex":
            special_conditions.extend([
                "Electronic monitoring if required",
                "Surrender of passport during processing",
                "Attendance at scheduled interviews"
            ])
        
        selected = random.sample(special_conditions, min(2, len(special_conditions)))
        return "\n".join([f"({chr(97 + i)}) {condition}" for i, condition in enumerate(selected)])
    
    def _generate_application_process(self) -> str:
        """Generate application process description."""
        return """Applications must be lodged:
(a) online through the official portal;
(b) with all required documentation;
(c) accompanied by the prescribed fee;
(d) before the applicant's current visa expires (if applicable)."""
    
    def _generate_decision_criteria(self, complexity: str) -> str:
        """Generate decision criteria."""
        base_criteria = """Decisions will be made based on:
(a) satisfaction of all eligibility requirements;
(b) genuineness of application;
(c) risk assessment outcomes."""
        
        if complexity == "complex":
            base_criteria += """
(d) public interest considerations;
(e) ministerial direction compliance;
(f) precedent case analysis."""
        
        return base_criteria
    
    def generate_multiple_policies(self, 
                                 specifications: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate multiple policy documents.
        
        Args:
            specifications: List of policy specifications
            
        Returns:
            Dictionary mapping policy names to document content
        """
        policies = {}
        
        for spec in specifications:
            policy_name = spec.get("name", f"Policy_{len(policies) + 1}")
            policy_content = self.generate_policy(
                visa_category=spec["visa_category"],
                visa_name=spec["visa_name"],
                complexity=spec.get("complexity", "medium"),
                custom_params=spec.get("custom_params")
            )
            policies[policy_name] = policy_content
        
        return policies
    
    def save_policy(self, policy_content: str, filename: str, output_dir: str = "data/input"):
        """Save policy document to file.
        
        Args:
            policy_content: The policy document content
            filename: Name of the file to save
            output_dir: Directory to save the file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(policy_content)
        
        return str(file_path)


def main():
    """Example usage of the PolicyGenerator."""
    generator = PolicyGenerator()
    
    # Generate a single policy
    policy = generator.generate_policy(
        visa_category="visitor",
        visa_name="Tourist Visa",
        complexity="medium"
    )
    
    print("Generated Policy:")
    print("=" * 80)
    print(policy[:1000] + "..." if len(policy) > 1000 else policy)
    
    # Generate multiple policies
    specifications = [
        {
            "name": "skilled_worker_visa",
            "visa_category": "work",
            "visa_name": "Skilled Worker Visa",
            "complexity": "complex"
        },
        {
            "name": "student_visa",
            "visa_category": "student", 
            "visa_name": "Student Visa",
            "complexity": "medium"
        }
    ]
    
    policies = generator.generate_multiple_policies(specifications)
    print(f"\nGenerated {len(policies)} policies:")
    for name in policies.keys():
        print(f"- {name}")


if __name__ == "__main__":
    main()
