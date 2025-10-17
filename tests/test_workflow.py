import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator


class TestWorkflowOrchestrator:
    """Tests for WorkflowOrchestrator."""
    
    def test_orchestrator_initialization(self):
        """Test orchestrator can be initialized."""
        orchestrator = WorkflowOrchestrator()
        assert orchestrator.agents is not None
        assert len(orchestrator.agents) == 5
    
    def test_orchestrator_has_all_agents(self):
        """Test orchestrator has all required agents."""
        orchestrator = WorkflowOrchestrator()
        
        expected_agents = [
            'policy_evaluator',
            'requirements_capture',
            'question_generator',
            'validation_agent',
            'consolidation_agent'
        ]
        
        for agent_name in expected_agents:
            assert agent_name in orchestrator.agents


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
