import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents import (
    PolicyEvaluatorAgent,
    RequirementsCaptureAgent,
    QuestionGeneratorAgent,
    ValidationAgent,
    ConsolidationAgent
)


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        'model': 'gpt-4-turbo-preview',
        'temperature': 0.1,
        'max_tokens': 4000
    }


@pytest.fixture
def sample_policy_path():
    """Path to sample policy document."""
    return str(project_root / 'data' / 'input' / 'parent_boost_policy.txt')


@pytest.fixture
def sample_policy_structure():
    """Sample policy structure for testing."""
    return {
        'visa_type': 'Parent Boost Visitor Visa',
        'visa_code': 'V4',
        'objective': {
            'family_reunification': True,
            'labour_force_support': True
        },
        'key_requirements': {
            'location': 'outside_nz',
            'sponsorship': 'required',
            'health': 'required',
            'character': 'required'
        }
    }


@pytest.fixture
def sample_requirements():
    """Sample requirements for testing."""
    return {
        'functional_requirements': [
            {
                'requirement_id': 'FR-001',
                'description': 'System must verify applicant is outside NZ',
                'type': 'functional',
                'priority': 'must_have',
                'policy_reference': 'V4.5(a)(i)'
            }
        ],
        'data_requirements': [
            {
                'requirement_id': 'DR-001',
                'field_name': 'applicant_name',
                'data_type': 'text',
                'description': 'Applicant full name',
                'required': True,
                'policy_reference': 'V4.5'
            }
        ],
        'business_rules': [
            {
                'rule_id': 'BR-001',
                'description': 'Maximum 2 sponsors allowed',
                'rule_type': 'constraint',
                'policy_reference': 'V4.10(f)'
            }
        ]
    }


class TestPolicyEvaluatorAgent:
    """Tests for PolicyEvaluatorAgent."""
    
    def test_agent_initialization(self, sample_config):
        """Test agent can be initialized."""
        agent = PolicyEvaluatorAgent('PolicyEvaluator', sample_config)
        assert agent.name == 'PolicyEvaluator'
        assert agent.llm is not None
    
    def test_agent_requires_policy_document(self, sample_config):
        """Test agent requires policy document input."""
        agent = PolicyEvaluatorAgent('PolicyEvaluator', sample_config)
        
        with pytest.raises(ValueError):
            agent.execute({})
    
    @pytest.mark.skipif(
        not Path(project_root / 'data' / 'input' / 'parent_boost_policy.txt').exists(),
        reason="Sample policy file not found"
    )
    def test_agent_execution_structure(self, sample_config, sample_policy_path):
        """Test agent returns expected output structure."""
        agent = PolicyEvaluatorAgent('PolicyEvaluator', sample_config)
        
        # Note: This test requires API key and will make actual API calls
        # Skip in CI/CD without API key
        import os
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip("OPENAI_API_KEY not set")
        
        outputs = agent.execute({'policy_document_path': sample_policy_path})
        
        assert 'policy_structure' in outputs
        assert 'eligibility_rules' in outputs
        assert 'conditions' in outputs
        assert 'metadata' in outputs


class TestRequirementsCaptureAgent:
    """Tests for RequirementsCaptureAgent."""
    
    def test_agent_initialization(self, sample_config):
        """Test agent can be initialized."""
        agent = RequirementsCaptureAgent('RequirementsCapture', sample_config)
        assert agent.name == 'RequirementsCapture'
        assert agent.llm is not None
    
    def test_agent_execution_structure(self, sample_config, sample_policy_structure):
        """Test agent returns expected output structure."""
        agent = RequirementsCaptureAgent('RequirementsCapture', sample_config)
        
        import os
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip("OPENAI_API_KEY not set")
        
        outputs = agent.execute({
            'policy_structure': sample_policy_structure,
            'eligibility_rules': {},
            'conditions': {}
        })
        
        assert 'functional_requirements' in outputs
        assert 'data_requirements' in outputs
        assert 'business_rules' in outputs
        assert 'validation_rules' in outputs


class TestQuestionGeneratorAgent:
    """Tests for QuestionGeneratorAgent."""
    
    def test_agent_initialization(self, sample_config):
        """Test agent can be initialized."""
        agent = QuestionGeneratorAgent('QuestionGenerator', sample_config)
        assert agent.name == 'QuestionGenerator'
        assert agent.llm is not None
    
    def test_agent_execution_structure(self, sample_config, sample_requirements):
        """Test agent returns expected output structure."""
        agent = QuestionGeneratorAgent('QuestionGenerator', sample_config)
        
        import os
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip("OPENAI_API_KEY not set")
        
        outputs = agent.execute(sample_requirements)
        
        assert 'application_questions' in outputs
        assert 'conditional_logic' in outputs
        assert 'question_count' in outputs


class TestValidationAgent:
    """Tests for ValidationAgent."""
    
    def test_agent_initialization(self, sample_config):
        """Test agent can be initialized."""
        agent = ValidationAgent('ValidationAgent', sample_config)
        assert agent.name == 'ValidationAgent'
        assert agent.llm is not None
    
    def test_requirement_validation(self, sample_config, sample_requirements):
        """Test requirement validation logic."""
        agent = ValidationAgent('ValidationAgent', sample_config)
        
        req_validation = agent._validate_requirements(
            sample_requirements['functional_requirements']
        )
        
        assert 'total_requirements' in req_validation
        assert 'valid_requirements' in req_validation
        assert 'validation_rate' in req_validation
    
    def test_question_validation(self, sample_config):
        """Test question validation logic."""
        agent = ValidationAgent('ValidationAgent', sample_config)
        
        sample_questions = [
            {
                'question_id': 'Q-001',
                'question_text': 'What is your name?',
                'input_type': 'text',
                'required': True
            }
        ]
        
        q_validation = agent._validate_questions(sample_questions)
        
        assert 'total_questions' in q_validation
        assert 'valid_questions' in q_validation
        assert 'validation_rate' in q_validation


class TestConsolidationAgent:
    """Tests for ConsolidationAgent."""
    
    def test_agent_initialization(self, sample_config):
        """Test agent can be initialized."""
        agent = ConsolidationAgent('ConsolidationAgent', sample_config)
        assert agent.name == 'ConsolidationAgent'
        assert agent.llm is not None
    
    def test_traceability_matrix_creation(self, sample_config, sample_requirements):
        """Test traceability matrix creation."""
        agent = ConsolidationAgent('ConsolidationAgent', sample_config)
        
        questions = [
            {
                'question_id': 'Q-001',
                'policy_reference': 'V4.5(a)(i)'
            }
        ]
        
        matrix = agent._create_traceability_matrix(sample_requirements, questions)
        
        assert isinstance(matrix, list)
        if matrix:
            assert 'policy_reference' in matrix[0]
            assert 'requirement_id' in matrix[0]
    
    def test_summary_stats_generation(self, sample_config, sample_requirements):
        """Test summary statistics generation."""
        agent = ConsolidationAgent('ConsolidationAgent', sample_config)
        
        questions = [
            {
                'question_id': 'Q-001',
                'section': 'Applicant Details'
            }
        ]
        
        validation_report = {
            'overall_score': 85.0,
            'requirement_validation': {'validation_rate': 90.0},
            'question_validation': {'validation_rate': 80.0}
        }
        
        stats = agent._generate_summary_stats(
            sample_requirements,
            questions,
            validation_report
        )
        
        assert 'total_requirements' in stats
        assert 'total_questions' in stats
        assert 'validation_score' in stats
        assert stats['validation_score'] == 85.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
