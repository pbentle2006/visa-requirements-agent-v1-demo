from typing import Dict, Any, List
import time
from .base_agent import BaseAgent
from ..utils.validator import Validator


class ValidationAgent(BaseAgent):
    """Agent for validating requirements against policy and technical constraints."""
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate requirements and questions against policy.
        
        Args:
            inputs: Dictionary containing all previous agent outputs
            
        Returns:
            Dictionary with validation_report and gap_analysis
        """
        start_time = time.time()
        
        try:
            # Extract inputs
            policy_structure = inputs.get('policy_structure', {})
            sections = inputs.get('sections', {})
            requirements = inputs.get('functional_requirements', []) + \
                          inputs.get('data_requirements', []) + \
                          inputs.get('business_rules', [])
            questions = inputs.get('application_questions', [])
            
            # Perform validations
            requirement_validation = self._validate_requirements(requirements)
            question_validation = self._validate_questions(questions)
            coverage_analysis = self._analyze_coverage(requirements, questions, sections)
            consistency_check = self._check_consistency(requirements, questions, policy_structure)
            gap_analysis = self._identify_gaps(requirements, questions, sections)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                requirement_validation,
                question_validation,
                coverage_analysis,
                gap_analysis
            )
            
            outputs = {
                'validation_report': {
                    'requirement_validation': requirement_validation,
                    'question_validation': question_validation,
                    'consistency_check': consistency_check,
                    'overall_score': self._calculate_overall_score(
                        requirement_validation,
                        question_validation,
                        coverage_analysis
                    )
                },
                'gap_analysis': gap_analysis,
                'coverage_analysis': coverage_analysis,
                'recommendations': recommendations
            }
            
            outputs = self._add_metadata(outputs)
            
            duration = time.time() - start_time
            self._log_execution(inputs, outputs, duration, True)
            
            return outputs
            
        except Exception as e:
            duration = time.time() - start_time
            self._log_execution(inputs, {}, duration, False, str(e))
            raise
    
    def _validate_requirements(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate individual requirements."""
        valid_count = 0
        invalid_count = 0
        errors = []
        
        for req in requirements:
            is_valid, req_errors = Validator.validate_requirement(req)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                errors.append({
                    'requirement_id': req.get('requirement_id', 'unknown'),
                    'errors': req_errors
                })
        
        return {
            'total_requirements': len(requirements),
            'valid_requirements': valid_count,
            'invalid_requirements': invalid_count,
            'validation_rate': (valid_count / len(requirements) * 100) if requirements else 0,
            'errors': errors
        }
    
    def _validate_questions(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate individual questions."""
        valid_count = 0
        invalid_count = 0
        errors = []
        
        for q in questions:
            is_valid, q_errors = Validator.validate_question(q)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                errors.append({
                    'question_id': q.get('question_id', 'unknown'),
                    'errors': q_errors
                })
        
        return {
            'total_questions': len(questions),
            'valid_questions': valid_count,
            'invalid_questions': invalid_count,
            'validation_rate': (valid_count / len(questions) * 100) if questions else 0,
            'errors': errors
        }
    
    def _analyze_coverage(
        self,
        requirements: List[Dict[str, Any]],
        questions: List[Dict[str, Any]],
        sections: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze coverage of policy sections."""
        policy_sections = list(sections.keys())
        
        req_coverage = Validator.check_requirement_coverage(requirements, policy_sections)
        q_req_mapping = Validator.check_question_requirement_mapping(questions, requirements)
        
        return {
            'requirement_coverage': req_coverage,
            'question_requirement_mapping': q_req_mapping
        }
    
    def _check_consistency(
        self,
        requirements: List[Dict[str, Any]],
        questions: List[Dict[str, Any]],
        policy_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check consistency between requirements, questions, and policy using LLM."""
        
        context = f"""
Policy Structure: {policy_structure}
Sample Requirements: {requirements[:5]}
Sample Questions: {questions[:5]}
"""
        
        prompt = f"""Analyze consistency between policy, requirements, and questions.

Context:
{context[:2500]}

Check for:
1. Requirements that contradict policy
2. Questions that don't align with requirements
3. Missing validation rules
4. Conflicting business rules
5. Inconsistent terminology

Return a JSON object with:
- consistent: boolean (overall consistency)
- inconsistencies: Array of inconsistency objects with:
  - type: contradiction|misalignment|missing|conflict
  - description: What is inconsistent
  - severity: high|medium|low
  - affected_items: List of requirement/question IDs
  - recommendation: How to fix

Return ONLY valid JSON, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result
    
    def _identify_gaps(
        self,
        requirements: List[Dict[str, Any]],
        questions: List[Dict[str, Any]],
        sections: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identify gaps in requirements and questions using LLM."""
        
        context = f"""
Policy Sections: {list(sections.keys())}
Requirements Count: {len(requirements)}
Questions Count: {len(questions)}
Sample Requirements: {requirements[:5]}
Sample Questions: {questions[:5]}
"""
        
        prompt = f"""Identify gaps in requirements capture and question generation.

Context:
{context[:2500]}

Identify:
1. Policy sections not covered by requirements
2. Requirements without corresponding questions
3. Missing validation rules
4. Missing conditional logic
5. Incomplete data collection

Return a JSON object with:
- missing_requirements: Array of missing requirement descriptions
- missing_questions: Array of missing question descriptions
- missing_validations: Array of missing validation descriptions
- uncovered_policy_sections: Array of section codes
- severity: high|medium|low for each gap

Return ONLY valid JSON, no other text."""

        response = self.llm.invoke(prompt)
        result = self._extract_json_from_response(response.content)
        
        return result
    
    def _generate_recommendations(
        self,
        requirement_validation: Dict[str, Any],
        question_validation: Dict[str, Any],
        coverage_analysis: Dict[str, Any],
        gap_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for improvements."""
        
        recommendations = []
        
        # Recommendations based on validation errors
        if requirement_validation['invalid_requirements'] > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'requirements',
                'description': f"Fix {requirement_validation['invalid_requirements']} invalid requirements",
                'action': 'Review and correct requirement definitions'
            })
        
        if question_validation['invalid_questions'] > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'questions',
                'description': f"Fix {question_validation['invalid_questions']} invalid questions",
                'action': 'Review and correct question definitions'
            })
        
        # Recommendations based on coverage
        coverage = coverage_analysis['requirement_coverage']['coverage_percentage']
        if coverage < 95:
            recommendations.append({
                'priority': 'high',
                'category': 'coverage',
                'description': f"Policy coverage is only {coverage:.1f}%",
                'action': 'Add requirements for uncovered policy sections'
            })
        
        # Recommendations based on gaps
        if gap_analysis.get('missing_requirements'):
            recommendations.append({
                'priority': 'medium',
                'category': 'gaps',
                'description': f"Found {len(gap_analysis['missing_requirements'])} missing requirements",
                'action': 'Add missing requirements identified in gap analysis'
            })
        
        return recommendations
    
    def _calculate_overall_score(
        self,
        requirement_validation: Dict[str, Any],
        question_validation: Dict[str, Any],
        coverage_analysis: Dict[str, Any]
    ) -> float:
        """Calculate overall validation score (0-100)."""
        req_score = requirement_validation['validation_rate']
        q_score = question_validation['validation_rate']
        cov_score = coverage_analysis['requirement_coverage']['coverage_percentage']
        
        # Weighted average
        overall = (req_score * 0.3 + q_score * 0.3 + cov_score * 0.4)
        
        return round(overall, 2)
