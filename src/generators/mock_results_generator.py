"""
Mock Results Generator

Generates realistic sample outputs for demo purposes when LLM APIs are not available.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class MockResultsGenerator:
    """Generates mock results for all workflow stages."""
    
    def __init__(self):
        """Initialize the mock results generator."""
        self.visa_codes = ["V1", "V2", "V3", "V4", "V5", "W1", "W2", "S1", "S2", "F1", "F2"]
        self.requirement_types = ["functional", "data", "business_rule", "validation"]
        self.priorities = ["must_have", "should_have", "could_have"]
        
    def generate_complete_workflow_results(self, policy_name: str = "Sample Policy") -> Dict[str, Any]:
        """Generate complete workflow results for demo."""
        
        # Generate all stage outputs
        policy_structure = self.generate_policy_structure(policy_name)
        eligibility_rules = self.generate_eligibility_rules()
        conditions = self.generate_conditions()
        
        functional_requirements = self.generate_functional_requirements()
        data_requirements = self.generate_data_requirements()
        business_rules = self.generate_business_rules()
        validation_rules = self.generate_validation_rules()
        
        application_questions = self.generate_application_questions()
        conditional_logic = self.generate_conditional_logic()
        
        validation_report = self.generate_validation_report()
        gap_analysis = self.generate_gap_analysis()
        recommendations = self.generate_recommendations()
        
        consolidated_spec = self.generate_consolidated_spec()
        implementation_guide = self.generate_implementation_guide()
        traceability_matrix = self.generate_traceability_matrix()
        summary_statistics = self.generate_summary_statistics()
        
        return {
            "status": "completed",
            "duration_seconds": round(random.uniform(180, 300), 2),
            "stages": [
                {
                    "name": "policy_analysis",
                    "status": "completed",
                    "duration": round(random.uniform(30, 60), 2),
                    "agent": "PolicyEvaluator"
                },
                {
                    "name": "requirements_capture", 
                    "status": "completed",
                    "duration": round(random.uniform(45, 90), 2),
                    "agent": "RequirementsCapture"
                },
                {
                    "name": "question_generation",
                    "status": "completed", 
                    "duration": round(random.uniform(60, 120), 2),
                    "agent": "QuestionGenerator"
                },
                {
                    "name": "validation",
                    "status": "completed",
                    "duration": round(random.uniform(30, 60), 2),
                    "agent": "ValidationAgent"
                },
                {
                    "name": "consolidation",
                    "status": "completed",
                    "duration": round(random.uniform(30, 45), 2),
                    "agent": "ConsolidationAgent"
                }
            ],
            "outputs": {
                "policy_structure": policy_structure,
                "eligibility_rules": eligibility_rules,
                "conditions": conditions,
                "functional_requirements": functional_requirements,
                "data_requirements": data_requirements,
                "business_rules": business_rules,
                "validation_rules": validation_rules,
                "application_questions": application_questions,
                "conditional_logic": conditional_logic,
                "validation_report": validation_report,
                "gap_analysis": gap_analysis,
                "recommendations": recommendations,
                "consolidated_spec": consolidated_spec,
                "implementation_guide": implementation_guide,
                "traceability_matrix": traceability_matrix,
                "summary_statistics": summary_statistics
            }
        }
    
    def generate_policy_structure(self, policy_name: str) -> Dict[str, Any]:
        """Generate mock policy structure."""
        visa_code = random.choice(self.visa_codes)
        
        return {
            "visa_type": policy_name,
            "visa_code": visa_code,
            "objective": {
                "primary_purpose": "Enable temporary entry for specific purposes",
                "secondary_purposes": ["family reunification", "economic contribution", "cultural exchange"]
            },
            "key_requirements": {
                "location": "Must be outside country when applying",
                "sponsorship": "Sponsorship required from eligible person",
                "health": "Must meet health requirements",
                "character": "Must meet character requirements",
                "financial": "Must demonstrate financial capacity"
            },
            "stakeholders": ["applicants", "sponsors", "dependents", "employers"],
            "scope": "Applications lodged on or after effective date",
            "effective_date": "1 January 2024",
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}"
        }
    
    def generate_eligibility_rules(self) -> Dict[str, Any]:
        """Generate mock eligibility rules."""
        return {
            "applicant_requirements": [
                {
                    "requirement": "Must be outside country",
                    "reference": f"{random.choice(self.visa_codes)}.5(a)(i)",
                    "mandatory": True
                },
                {
                    "requirement": "Must hold valid passport",
                    "reference": f"{random.choice(self.visa_codes)}.5(a)(ii)", 
                    "mandatory": True
                },
                {
                    "requirement": "Must meet health requirements",
                    "reference": f"{random.choice(self.visa_codes)}.5(b)",
                    "mandatory": True
                }
            ],
            "sponsor_requirements": [
                {
                    "requirement": "Must be citizen or resident",
                    "reference": f"{random.choice(self.visa_codes)}.10(a)",
                    "mandatory": True
                },
                {
                    "requirement": "Must meet income threshold",
                    "reference": f"{random.choice(self.visa_codes)}.10(b)",
                    "mandatory": True
                }
            ],
            "dependent_requirements": [
                {
                    "requirement": "Must be under 18 years old",
                    "reference": f"{random.choice(self.visa_codes)}.15(a)",
                    "mandatory": True
                }
            ]
        }
    
    def generate_conditions(self) -> Dict[str, Any]:
        """Generate mock visa conditions."""
        return {
            "visa_conditions": [
                "No work permitted",
                "Must maintain health insurance", 
                "Must not engage in criminal activity"
            ],
            "financial_conditions": [
                f"Maintain access to ${random.randint(10, 50) * 1000} funds",
                "Provide evidence of financial support"
            ],
            "health_conditions": [
                "Undergo medical examination",
                "Maintain health insurance coverage"
            ]
        }
    
    def generate_functional_requirements(self) -> List[Dict[str, Any]]:
        """Generate mock functional requirements."""
        requirements = []
        
        base_requirements = [
            "System must verify applicant location",
            "System must validate passport details", 
            "System must check sponsor eligibility",
            "System must calculate income thresholds",
            "System must process health certificates",
            "System must validate relationship evidence",
            "System must generate decision recommendations",
            "System must track application status",
            "System must send notifications",
            "System must maintain audit trail"
        ]
        
        for i, req in enumerate(base_requirements[:random.randint(8, 12)]):
            requirements.append({
                "requirement_id": f"FR-{i+1:03d}",
                "description": req,
                "category": random.choice(["eligibility", "processing", "validation", "notification"]),
                "priority": random.choice(self.priorities),
                "policy_reference": f"{random.choice(self.visa_codes)}.{random.randint(5, 50)}",
                "acceptance_criteria": [
                    f"System validates {req.split()[-1]} correctly",
                    f"Error handling for invalid {req.split()[-1]}",
                    f"Audit logging for {req.split()[-1]} checks"
                ]
            })
        
        return requirements
    
    def generate_data_requirements(self) -> List[Dict[str, Any]]:
        """Generate mock data requirements."""
        requirements = []
        
        fields = [
            ("applicant_name", "text", "Full legal name of applicant"),
            ("date_of_birth", "date", "Date of birth"),
            ("passport_number", "text", "Passport number"),
            ("nationality", "text", "Country of citizenship"),
            ("current_location", "text", "Current country of residence"),
            ("sponsor_name", "text", "Name of sponsor"),
            ("sponsor_income", "currency", "Annual income of sponsor"),
            ("relationship_type", "select", "Type of relationship to sponsor"),
            ("intended_duration", "number", "Intended length of stay in days"),
            ("accommodation_address", "text", "Address where applicant will stay")
        ]
        
        for i, (field, data_type, description) in enumerate(fields[:random.randint(8, 10)]):
            requirements.append({
                "requirement_id": f"DR-{i+1:03d}",
                "field_name": field,
                "data_type": data_type,
                "description": description,
                "required": random.choice([True, True, False]),  # 2/3 chance of required
                "validation": f"Must be valid {data_type}",
                "policy_reference": f"{random.choice(self.visa_codes)}.{random.randint(5, 50)}"
            })
        
        return requirements
    
    def generate_business_rules(self) -> List[Dict[str, Any]]:
        """Generate mock business rules."""
        rules = []
        
        base_rules = [
            ("Maximum 2 sponsors allowed", "constraint", "COUNT(sponsors) <= 2"),
            ("Sponsor can support max 6 parents", "constraint", "COUNT(sponsored_parents) <= 6"),
            ("Medical certificates valid 36 months", "validation", "certificate_date >= (current_date - 36 months)"),
            ("Income threshold varies by family size", "calculation", "threshold = base_amount + (dependents * additional_amount)"),
            ("Age validation for dependents", "validation", "dependent_age < 18"),
            ("Passport validity requirement", "validation", "passport_expiry > (application_date + 6 months)")
        ]
        
        for i, (description, rule_type, logic) in enumerate(base_rules[:random.randint(5, 8)]):
            rules.append({
                "rule_id": f"BR-{i+1:03d}",
                "description": description,
                "rule_type": rule_type,
                "logic": logic,
                "policy_reference": f"{random.choice(self.visa_codes)}.{random.randint(10, 50)}",
                "parameters": {
                    "max_value": random.randint(2, 10) if "max" in description.lower() else None,
                    "threshold": random.randint(1000, 100000) if "threshold" in description.lower() else None
                }
            })
        
        return rules
    
    def generate_validation_rules(self) -> List[Dict[str, Any]]:
        """Generate mock validation rules."""
        rules = []
        
        validations = [
            ("applicant_age", "range", "Age must be between 18 and 65", "Age must be between 18 and 65 years"),
            ("passport_expiry", "date", "Passport must be valid for 6+ months", "Passport expires too soon"),
            ("income_amount", "currency", "Income must meet threshold", "Income below required threshold"),
            ("relationship_duration", "number", "Relationship must be 12+ months", "Relationship duration too short"),
            ("health_certificate_date", "date", "Certificate must be within 36 months", "Health certificate expired")
        ]
        
        for i, (field, validation_type, rule, error_msg) in enumerate(validations[:random.randint(4, 6)]):
            rules.append({
                "validation_id": f"VR-{i+1:03d}",
                "field": field,
                "validation_type": validation_type,
                "rule": rule,
                "error_message": error_msg,
                "policy_reference": f"{random.choice(self.visa_codes)}.{random.randint(20, 40)}"
            })
        
        return rules
    
    def generate_application_questions(self) -> List[Dict[str, Any]]:
        """Generate mock application questions."""
        questions = []
        
        sections = {
            "Applicant Details": [
                ("What is your full legal name?", "text", True, "Enter name as shown on passport"),
                ("What is your date of birth?", "date", True, "DD/MM/YYYY format"),
                ("What is your passport number?", "text", True, "Enter passport number"),
                ("Are you currently in the country?", "boolean", True, "You must be outside the country to apply")
            ],
            "Sponsorship": [
                ("Who is your sponsor?", "text", True, "Full name of sponsor"),
                ("How many sponsors do you have?", "number", True, "Maximum 2 sponsors allowed"),
                ("What is your relationship to the sponsor?", "select", True, "Select relationship type")
            ],
            "Financial": [
                ("What is the sponsor's annual income?", "currency", True, "Income for last tax year"),
                ("How much maintenance funds do you have?", "currency", True, "Minimum $10,000 required")
            ],
            "Health & Character": [
                ("When was your medical certificate issued?", "date", True, "Must be within 36 months"),
                ("Do you have health insurance?", "boolean", True, "Minimum $200,000 coverage required")
            ]
        }
        
        question_id = 1
        for section, section_questions in sections.items():
            for question_text, input_type, required, help_text in section_questions:
                questions.append({
                    "question_id": f"Q_{section.upper().replace(' ', '_')[:4]}_{question_id:03d}",
                    "section": section,
                    "question_text": question_text,
                    "input_type": input_type,
                    "required": required,
                    "validation": {
                        "rules": [f"required"] if required else [],
                        "error_messages": {
                            "required": "This field is required"
                        }
                    },
                    "help_text": help_text,
                    "policy_reference": f"{random.choice(self.visa_codes)}.{random.randint(5, 50)}",
                    "options": ["Parent", "Partner", "Child"] if input_type == "select" else None
                })
                question_id += 1
        
        return questions[:random.randint(15, 25)]
    
    def generate_conditional_logic(self) -> Dict[str, Any]:
        """Generate mock conditional logic."""
        return {
            "Q_APPL_004": {
                "triggers": ["decline_application"],
                "condition": "if answer is 'Yes', decline application"
            },
            "Q_SPON_002": {
                "triggers": ["calculate_income_threshold"],
                "affects": ["Q_FINA_001"]
            }
        }
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate mock validation report."""
        total_reqs = random.randint(40, 60)
        valid_reqs = int(total_reqs * random.uniform(0.85, 0.98))
        
        total_questions = random.randint(20, 35)
        valid_questions = int(total_questions * random.uniform(0.90, 0.98))
        
        overall_score = (valid_reqs/total_reqs + valid_questions/total_questions) / 2 * 100
        
        return {
            "overall_score": round(overall_score, 1),
            "requirement_validation": {
                "total_requirements": total_reqs,
                "valid_requirements": valid_reqs,
                "invalid_requirements": total_reqs - valid_reqs,
                "validation_rate": round(valid_reqs/total_reqs * 100, 1),
                "errors": [
                    {"requirement_id": "FR-023", "errors": ["Missing policy_reference"]},
                    {"requirement_id": "DR-015", "errors": ["Invalid data_type"]}
                ][:total_reqs - valid_reqs]
            },
            "question_validation": {
                "total_questions": total_questions,
                "valid_questions": valid_questions,
                "invalid_questions": total_questions - valid_questions,
                "validation_rate": round(valid_questions/total_questions * 100, 1),
                "errors": [
                    {"question_id": "Q_HEAL_002", "errors": ["Missing validation rules"]}
                ][:total_questions - valid_questions]
            },
            "consistency_check": {
                "consistent": random.choice([True, True, False]),
                "inconsistencies": []
            }
        }
    
    def generate_gap_analysis(self) -> Dict[str, Any]:
        """Generate mock gap analysis."""
        return {
            "missing_requirements": [
                "No requirement for partnership duration validation",
                "Missing validation for dependent age limits"
            ][:random.randint(0, 3)],
            "missing_questions": [
                "No question about insurance provider approval",
                "Missing question about previous visa history"
            ][:random.randint(0, 2)],
            "uncovered_policy_sections": [
                f"{random.choice(self.visa_codes)}.40(a)(ii)",
                f"{random.choice(self.visa_codes)}.45(b)"
            ][:random.randint(0, 2)]
        }
    
    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate mock recommendations."""
        return [
            {
                "priority": "high",
                "category": "requirements",
                "description": "Fix invalid requirements",
                "action": "Add missing policy references and correct data types"
            },
            {
                "priority": "medium", 
                "category": "coverage",
                "description": "Improve policy coverage",
                "action": "Add requirements for uncovered policy sections"
            },
            {
                "priority": "low",
                "category": "enhancement",
                "description": "Enhance user experience",
                "action": "Add more detailed help text for complex questions"
            }
        ][:random.randint(2, 4)]
    
    def generate_consolidated_spec(self) -> Dict[str, Any]:
        """Generate mock consolidated specification."""
        return {
            "executive_summary": "Complete specification for automated visa application processing system",
            "system_overview": {
                "purpose": "Automate visa application processing and validation",
                "scope": "End-to-end application workflow",
                "stakeholders": ["applicants", "sponsors", "case officers", "system administrators"]
            },
            "architecture": {
                "pattern": "Multi-tier web application",
                "components": ["Web UI", "API Layer", "Business Logic", "Database", "Integration Layer"],
                "technologies": ["React", "Node.js", "PostgreSQL", "REST APIs"]
            }
        }
    
    def generate_implementation_guide(self) -> Dict[str, Any]:
        """Generate mock implementation guide."""
        return {
            "phases": [
                {
                    "phase": "Foundation",
                    "duration": "4 weeks",
                    "deliverables": ["Database schema", "API framework", "Authentication"]
                },
                {
                    "phase": "Core Features", 
                    "duration": "8 weeks",
                    "deliverables": ["Application forms", "Validation engine", "Workflow engine"]
                },
                {
                    "phase": "Integration",
                    "duration": "4 weeks", 
                    "deliverables": ["External integrations", "Reporting", "Testing"]
                }
            ],
            "database_schema": {
                "tables": ["applications", "applicants", "sponsors", "documents", "validations"],
                "relationships": "Normalized relational design"
            },
            "api_endpoints": [
                "POST /api/applications",
                "GET /api/applications/{id}",
                "PUT /api/applications/{id}/validate",
                "GET /api/requirements"
            ]
        }
    
    def generate_traceability_matrix(self) -> List[Dict[str, Any]]:
        """Generate mock traceability matrix."""
        matrix = []
        
        for i in range(random.randint(15, 25)):
            matrix.append({
                "policy_reference": f"{random.choice(self.visa_codes)}.{random.randint(5, 50)}",
                "requirement_id": f"FR-{i+1:03d}",
                "requirement_type": random.choice(self.requirement_types),
                "requirement_description": f"Sample requirement {i+1}",
                "related_questions": [f"Q_SECT_{j:03d}" for j in range(1, random.randint(2, 4))],
                "coverage": random.choice(["full", "partial", "none"])
            })
        
        return matrix
    
    def generate_summary_statistics(self) -> Dict[str, Any]:
        """Generate mock summary statistics."""
        total_reqs = random.randint(40, 60)
        total_questions = random.randint(20, 35)
        
        return {
            "total_requirements": total_reqs,
            "requirements_by_type": {
                "functional": random.randint(15, 25),
                "data": random.randint(10, 20),
                "business_rules": random.randint(8, 15),
                "validation": random.randint(5, 10)
            },
            "total_questions": total_questions,
            "questions_by_section": {
                "Applicant Details": random.randint(5, 8),
                "Sponsorship": random.randint(3, 6),
                "Financial": random.randint(2, 4),
                "Health & Character": random.randint(3, 5)
            },
            "validation_score": round(random.uniform(85, 95), 1),
            "policy_coverage": round(random.uniform(90, 98), 1),
            "processing_time": round(random.uniform(180, 300), 1)
        }


def main():
    """Example usage of MockResultsGenerator."""
    generator = MockResultsGenerator()
    
    # Generate complete workflow results
    results = generator.generate_complete_workflow_results("Sample Tourist Visa")
    
    print("Generated Mock Results:")
    print("=" * 80)
    print(f"Status: {results['status']}")
    print(f"Duration: {results['duration_seconds']}s")
    print(f"Stages: {len(results['stages'])}")
    
    # Show summary statistics
    stats = results['outputs']['summary_statistics']
    print(f"\nSummary Statistics:")
    print(f"- Total Requirements: {stats['total_requirements']}")
    print(f"- Total Questions: {stats['total_questions']}")
    print(f"- Validation Score: {stats['validation_score']}%")
    print(f"- Policy Coverage: {stats['policy_coverage']}%")
    
    # Save to file for demo
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "mock_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nMock results saved to: {output_dir / 'mock_results.json'}")


if __name__ == "__main__":
    main()
