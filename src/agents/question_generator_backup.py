from typing import Dict, Any, List
import time
from .base_agent import BaseAgent


class QuestionGeneratorAgent(BaseAgent):
    """Agent for generating application form questions based on requirements."""
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate application form questions with validation rules.
        
        Args:
            inputs: Dictionary containing requirements and policy information
            
        Returns:
            Dictionary with application_questions and validation_rules
        """
        start_time = time.time()
        
        try:
            functional_requirements = inputs.get('functional_requirements', [])
            data_requirements = inputs.get('data_requirements', [])
            business_rules = inputs.get('business_rules', [])
            validation_rules = inputs.get('validation_rules', [])
            
            # Generate questions for different sections
            applicant_questions = self._generate_applicant_questions(
                data_requirements, validation_rules
            )
            
            sponsor_questions = self._generate_sponsor_questions(
                data_requirements, business_rules, validation_rules
            )
            
            dependent_questions = self._generate_dependent_questions(
                data_requirements, validation_rules
            )
            
            financial_questions = self._generate_financial_questions(
                data_requirements, business_rules, validation_rules
            )
            
            health_character_questions = self._generate_health_character_questions(
                data_requirements, validation_rules
            )
            
            # Combine all questions
            all_questions = (
                applicant_questions + 
                sponsor_questions + 
                dependent_questions + 
                financial_questions + 
                health_character_questions
            )
            
            # Generate conditional logic
            conditional_logic = self._generate_conditional_logic(all_questions, business_rules)
            
            outputs = {
                'application_questions': all_questions,
                'conditional_logic': conditional_logic,
                'question_count': len(all_questions)
            }
            
            outputs = self._add_metadata(outputs)
            
            duration = time.time() - start_time
            self._log_execution(inputs, outputs, duration, True)
            
            return outputs
            
        except Exception as e:
            duration = time.time() - start_time
            self._log_execution(inputs, {}, duration, False, str(e))
            raise
    
    def _generate_applicant_questions(
        self,
        data_requirements: List[Dict[str, Any]],
        validation_rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate questions for applicant section."""
        
        context = f"""
Data Requirements: {data_requirements[:10]}
Validation Rules: {validation_rules[:10]}
"""
        
        prompt = f"""Generate application form questions for the APPLICANT DETAILS section.

Context:
{context[:2000]}

Generate questions to collect:
- Personal information (name, DOB, passport)
- Current location (must be outside NZ)
- Contact details
- Relationship to sponsor

Return a JSON array of questions, each with:
- question_id: Unique ID (Q_APP_001, Q_APP_002, etc.)
- section: "Applicant Details"
- question_text: Clear, user-friendly question text
- input_type: text|number|boolean|date|select|multiselect|file
- required: boolean
- validation: Object with validation rules
- help_text: Helpful explanation for user
- policy_reference: Policy section reference (if applicable)

Return ONLY valid JSON array, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result if isinstance(result, list) else result.get('questions', [])
    
    def _generate_sponsor_questions(
        self,
        data_requirements: List[Dict[str, Any]],
        business_rules: List[Dict[str, Any]],
        validation_rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate questions for sponsor section."""
        
        context = f"""
Data Requirements: {data_requirements[:10]}
Business Rules: {business_rules[:10]}
"""
        
        prompt = f"""Generate application form questions for the SPONSORSHIP section.

Context:
{context[:2000]}

Generate questions to collect:
- Number of sponsors (max 2)
- Sponsor details (name, relationship, citizenship/residency)
- Number of parents being sponsored (max 6)
- Sponsorship form completion status

Return a JSON array of questions with proper validation rules and conditional logic.
Each question should have: question_id, section, question_text, input_type, required, validation, help_text, policy_reference

Return ONLY valid JSON array, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result if isinstance(result, list) else result.get('questions', [])
    
    def _generate_dependent_questions(
        self,
        data_requirements: List[Dict[str, Any]],
        validation_rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate questions for dependent children section."""
        
        prompt = f"""Generate application form questions for the DEPENDENT CHILDREN section.

Generate questions to collect:
- Whether applicant has dependent children
- Number of dependent children
- For each child: name, DOB, relationship
- Confirmation that children are under 18, unmarried, no own children

Return a JSON array of questions with proper validation rules and conditional logic.
Each question should have: question_id, section, question_text, input_type, required, validation, help_text, policy_reference

Return ONLY valid JSON array, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result if isinstance(result, list) else result.get('questions', [])
    
    def _generate_financial_questions(
        self,
        data_requirements: List[Dict[str, Any]],
        business_rules: List[Dict[str, Any]],
        validation_rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate questions for financial requirements section."""
        
        context = f"""
Business Rules: {business_rules[:10]}
"""
        
        prompt = f"""Generate application form questions for the FINANCIAL REQUIREMENTS section.

Context:
{context[:2000]}

Generate questions to collect:
- Sponsor income for last 3 tax years
- Income verification method (Inland Revenue)
- Maintenance funds available (NZD $10,000 + $5,000 per additional family member)
- Proof of funds

Include help text explaining income thresholds based on number of parents:
- 1-2 parents: NZD $65,000/year
- 3-4 parents: NZD $85,000/year
- 5-6 parents: NZD $105,000/year

Return a JSON array of questions with proper validation rules.
Each question should have: question_id, section, question_text, input_type, required, validation, help_text, policy_reference

Return ONLY valid JSON array, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result if isinstance(result, list) else result.get('questions', [])
    
    def _generate_health_character_questions(
        self,
        data_requirements: List[Dict[str, Any]],
        validation_rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate questions for health and character requirements section."""
        
        prompt = f"""Generate application form questions for the HEALTH & CHARACTER section.

Generate questions to collect:
- Medical certificate completion (INZ-approved physician)
- Medical certificate date (must be current, not older than 3 months)
- Police certificates from required countries
- Character declaration
- Travel/medical insurance details (NZD $200,000 minimum coverage)
- Insurance coverage dates

Return a JSON array of questions with proper validation rules.
Each question should have: question_id, section, question_text, input_type, required, validation, help_text, policy_reference

Return ONLY valid JSON array, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result if isinstance(result, list) else result.get('questions', [])
    
    def _generate_conditional_logic(
        self,
        questions: List[Dict[str, Any]],
        business_rules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate conditional logic for questions."""
        
        prompt = f"""Based on these questions and business rules, generate conditional logic.

Questions: {[q.get('question_id') for q in questions[:20]]}
Business Rules: {business_rules[:10]}

Identify:
1. Questions that should only show based on previous answers
2. Calculations triggered by certain answers
3. Validation dependencies between questions

Return a JSON object mapping question_ids to their conditional logic:
{{
  "question_id": {{
    "show_if": [{{"question": "other_question_id", "value": "expected_value"}}],
    "triggers": ["calculation_name", "validation_name"],
    "affects": ["other_question_id"]
  }}
}}

Return ONLY valid JSON, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result
