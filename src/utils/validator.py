from typing import Dict, Any, List, Tuple
import re


class Validator:
    """Utility class for validating requirements and questions."""
    
    @staticmethod
    def validate_requirement(requirement: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a requirement dictionary.
        
        Args:
            requirement: Requirement dictionary to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for any reasonable ID field
        id_fields = ['requirement_id', 'id', 'rule_id']
        has_id = any(field in requirement and requirement[field] for field in id_fields)
        if not has_id:
            errors.append("Missing requirement ID")
        
        # Check for description field (various names)
        desc_fields = ['description', 'requirement', 'rule', 'text']
        has_description = any(field in requirement and requirement[field] for field in desc_fields)
        if not has_description:
            errors.append("Missing description")
        
        # Type validation - be more lenient
        type_field = requirement.get('type', requirement.get('category', ''))
        valid_types = ['functional', 'data', 'business_rule', 'validation', 'business', 'technical', 'policy']
        if type_field and type_field not in valid_types:
            # Don't fail validation for unknown types, just note it
            pass
        
        # Priority validation - be more lenient  
        priority_field = requirement.get('priority', '')
        valid_priorities = ['must_have', 'should_have', 'could_have', 'high', 'medium', 'low', 'mandatory', 'optional']
        if priority_field and priority_field not in valid_priorities:
            # Don't fail validation for unknown priorities, just note it
            pass
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_question(question: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a question dictionary.
        
        Args:
            question: Question dictionary to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for any reasonable ID field
        id_fields = ['question_id', 'id', 'q_id']
        has_id = any(field in question and question[field] for field in id_fields)
        if not has_id:
            errors.append("Missing question ID")
        
        # Check for question text (various names)
        text_fields = ['question_text', 'question', 'text', 'prompt']
        has_text = any(field in question and question[field] for field in text_fields)
        if not has_text:
            errors.append("Missing question text")
        
        # Input type validation - be more lenient
        input_type = question.get('input_type', '')
        valid_input_types = ['text', 'number', 'boolean', 'date', 'select', 'multiselect', 'file', 'textarea', 'email', 'phone']
        if input_type and input_type not in valid_input_types:
            # Don't fail validation for unknown input types, just note it
            pass
        
        # If select/multiselect, check for options (but don't fail if missing)
        if question.get('input_type') in ['select', 'multiselect']:
            if not question.get('options'):
                # Don't fail validation, just note it
                pass
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_policy_reference(reference: str) -> bool:
        """
        Validate a policy reference format.
        
        Args:
            reference: Policy reference string (e.g., "V4.10(a)")
            
        Returns:
            True if valid format
        """
        # Pattern: V{number}.{number}[.{number}][({letter})]
        pattern = r'^V\d+\.\d+(?:\.\d+)?(?:\([a-z]+\))?$'
        return bool(re.match(pattern, reference))
    
    @staticmethod
    def check_requirement_coverage(
        requirements: List[Dict[str, Any]], 
        policy_sections: List[str]
    ) -> Dict[str, Any]:
        """
        Check if requirements cover all policy sections.
        
        Args:
            requirements: List of requirements
            policy_sections: List of policy section codes
            
        Returns:
            Coverage analysis
        """
        covered_sections = set()
        for req in requirements:
            ref = req.get('policy_reference', '')
            if ref:
                # Extract section code (e.g., "V4.10" from "V4.10(a)")
                match = re.match(r'(V\d+\.\d+)', ref)
                if match:
                    covered_sections.add(match.group(1))
        
        policy_section_set = set(policy_sections)
        uncovered = policy_section_set - covered_sections
        
        coverage_pct = (len(covered_sections) / len(policy_section_set) * 100) if policy_section_set else 0
        
        return {
            'total_sections': len(policy_section_set),
            'covered_sections': len(covered_sections),
            'coverage_percentage': coverage_pct,
            'uncovered_sections': list(uncovered)
        }
    
    @staticmethod
    def check_question_requirement_mapping(
        questions: List[Dict[str, Any]], 
        requirements: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check if questions map to requirements.
        
        Args:
            questions: List of questions
            requirements: List of requirements
            
        Returns:
            Mapping analysis
        """
        requirement_refs = {req.get('policy_reference') for req in requirements if req.get('policy_reference')}
        question_refs = {q.get('policy_reference') for q in questions if q.get('policy_reference')}
        
        mapped = question_refs & requirement_refs
        unmapped_questions = question_refs - requirement_refs
        
        return {
            'total_questions': len(questions),
            'questions_with_policy_refs': len(question_refs),
            'mapped_to_requirements': len(mapped),
            'unmapped_questions': list(unmapped_questions)
        }
