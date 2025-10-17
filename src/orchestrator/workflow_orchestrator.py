import os
import yaml
import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from ..agents import (
    PolicyEvaluatorAgent,
    RequirementsCaptureAgent,
    QuestionGeneratorAgent,
    ValidationAgent,
    ConsolidationAgent
)
from ..utils.output_formatter import OutputFormatter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrates the multi-agent workflow for visa requirements capture."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the workflow orchestrator.
        
        Args:
            config_dir: Path to configuration directory (default: project config/)
        """
        # Load environment variables
        load_dotenv()
        
        # Set config directory
        if config_dir is None:
            project_root = Path(__file__).parent.parent.parent
            config_dir = project_root / 'config'
        else:
            config_dir = Path(config_dir)
        
        # Load configurations
        self.agent_config = self._load_config(config_dir / 'agent_config.yaml')
        self.workflow_config = self._load_config(config_dir / 'workflow_config.yaml')
        
        # Initialize agents
        self.agents = self._initialize_agents()
        
        # Workflow state
        self.workflow_state: Dict[str, Any] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all agents with their configurations."""
        llm_config = self.agent_config.get('llm', {})
        agent_configs = self.agent_config.get('agents', {})
        
        agents = {
            'policy_evaluator': PolicyEvaluatorAgent(
                name='PolicyEvaluator',
                config={**llm_config, **agent_configs.get('policy_evaluator', {})}
            ),
            'requirements_capture': RequirementsCaptureAgent(
                name='RequirementsCapture',
                config={**llm_config, **agent_configs.get('requirements_capture', {})}
            ),
            'question_generator': QuestionGeneratorAgent(
                name='QuestionGenerator',
                config={**llm_config, **agent_configs.get('question_generator', {})}
            ),
            'validation_agent': ValidationAgent(
                name='ValidationAgent',
                config={**llm_config, **agent_configs.get('validation_agent', {})}
            ),
            'consolidation_agent': ConsolidationAgent(
                name='ConsolidationAgent',
                config={**llm_config, **agent_configs.get('consolidation_agent', {})}
            )
        }
        return agents
    
    def run_workflow(self, policy_document_path: str, policy_document_content: str = None, detected_visa_type: str = None, detected_visa_code: str = None, force_visa_type: bool = False) -> Dict[str, Any]:
        """
        Run the complete workflow for processing a policy document.
        
        Args:
            policy_document_path: Path to the policy document
            policy_document_content: Direct content of the policy document (optional)
            
        Returns:
            Dictionary containing workflow results
        """
        # CRITICAL DEBUG - This should ALWAYS appear
        print(f"DEBUG: ===== WORKFLOW ORCHESTRATOR CALLED =====")
        print(f"DEBUG: WorkflowOrchestrator.run_workflow() called")
        print(f"DEBUG: policy_document_path: {policy_document_path}")
        print(f"DEBUG: Policy content provided: {len(policy_document_content) if policy_document_content else 0} characters")
        if policy_document_content:
            print(f"DEBUG: First 300 chars of content: {policy_document_content[:300]}")
            print(f"DEBUG: Contains 'Working Holiday': {'Working Holiday' in policy_document_content}")
            print(f"DEBUG: Contains 'Skilled Migrant': {'Skilled Migrant' in policy_document_content}")
            print(f"DEBUG: Contains 'Parent': {'Parent' in policy_document_content}")
        print(f"DEBUG: ==========================================")
        workflow_start = time.time()
        
        # Set output directory FIRST
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / 'data' / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # NUCLEAR CACHE CLEARING - Delete ALL cached output files before execution
        import shutil
        print(" NUCLEAR ORCHESTRATOR CACHE CLEARING ", flush=True)
        if output_dir.exists():
            for item in output_dir.iterdir():
                if item.is_dir() and item.name != '.git':
                    shutil.rmtree(item)
                    print(f" DELETED CACHED DIR: {item} ", flush=True)
                elif item.is_file() and item.name != '.gitkeep':
                    item.unlink()
                    print(f" DELETED CACHED FILE: {item} ", flush=True)
        print(" ALL ORCHESTRATOR CACHE CLEARED - FORCING FRESH AGENT EXECUTION ", flush=True)
        
        logger.info("Starting Visa Requirements Workflow")
        logger.info("=" * 80)
        
        # Initialize workflow state
        self.workflow_state = {
            'policy_document_path': policy_document_path,
            'policy_document': policy_document_content,  # Add direct content
            'output_dir': str(output_dir),
            'start_time': datetime.now().isoformat(),
            # Add detected visa type hints for hybrid approach
            'detected_visa_type': detected_visa_type,
            'detected_visa_code': detected_visa_code,
            'force_visa_type': force_visa_type
        }
        
        # Log hybrid approach information
        if detected_visa_type and force_visa_type:
            print(f" ORCHESTRATOR: HYBRID MODE - Using detected visa type: {detected_visa_type} ({detected_visa_code}) ", flush=True)
        else:
            print(f" ORCHESTRATOR: STANDARD MODE - No visa type hints provided ", flush=True)
        
        # Execute stages
        stages = self.workflow_config['workflow']['stages']
        stage_results = []
        
        for stage in stages:
            stage_name = stage['name']
            logger.info(f"\n{'=' * 80}")
            logger.info(f"Stage: {stage_name.upper()}")
            logger.info(f"{'=' * 80}")
            
            stage_result = self._execute_stage(stage, output_dir)
            stage_results.append(stage_result)
            
            # Update workflow state with stage outputs
            if stage_result['status'] == 'success':
                self.workflow_state.update(stage_result['outputs'])
            else:
                logger.error(f"Stage {stage_name} failed: {stage_result.get('error')}")
                if not self.workflow_config['execution'].get('continue_on_error', False):
                    break
        
        workflow_duration = time.time() - workflow_start
        
        # Compile final results
        results = {
            'status': 'success' if all(s['status'] == 'success' for s in stage_results) else 'failed',
            'duration_seconds': workflow_duration,
            'stages': stage_results,
            'outputs': self.workflow_state,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save summary report
        summary_path = output_dir / 'workflow_summary.txt'
        summary = OutputFormatter.create_summary_report(results)
        with open(summary_path, 'w') as f:
            f.write(summary)
        
        logger.info(f"\n{'=' * 80}")
        logger.info(f"Workflow completed in {workflow_duration:.2f}s")
        logger.info(f"Summary saved to: {summary_path}")
        logger.info(f"{'=' * 80}\n")
        
        return results
    
    def _execute_stage(self, stage_config: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
        """Execute a single workflow stage."""
        stage_name = stage_config['name']
        agent_names = stage_config['agents']
        
        stage_start = time.time()
        
        try:
            # Prepare inputs for this stage
            stage_inputs = self._prepare_stage_inputs(stage_config)
            
            # Execute agents (currently only single agent per stage)
            agent_name = agent_names[0]
            agent = self.agents[agent_name]
            
            print(f" ORCHESTRATOR: Executing stage '{stage_name}' with agent '{agent_name}' ", flush=True)
            print(f" ORCHESTRATOR: Stage inputs keys: {list(stage_inputs.keys()) if stage_inputs else 'None'} ", flush=True)
            
            logger.info(f"Executing agent: {agent.name}")
            outputs = agent.execute(stage_inputs)
            
            print(f" ORCHESTRATOR: Agent '{agent_name}' completed. Output keys: {list(outputs.keys()) if outputs else 'None'} ", flush=True)
            
            # Save outputs
            stage_output_dir = output_dir / stage_name
            stage_output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = stage_output_dir / f'{stage_name}_output.json'
            OutputFormatter.save_json(outputs, str(output_file))
            
            logger.info(f"Outputs saved to: {output_file}")
            
            stage_duration = time.time() - stage_start
            
            return {
                'name': stage_name,
                'status': 'success',
                'duration_seconds': stage_duration,
                'outputs': outputs,
                'output_file': str(output_file)
            }
            
        except Exception as e:
            stage_duration = time.time() - stage_start
            error_msg = str(e)
            logger.error(f"Stage {stage_name} failed: {error_msg}")
            
            print(f" ORCHESTRATOR: Stage '{stage_name}' FAILED with error: {error_msg} ", flush=True)
            print(f" ORCHESTRATOR: Agent '{agent_name}' caused the failure ", flush=True)
            
            return {
                'name': stage_name,
                'status': 'failed',
                'duration_seconds': stage_duration,
                'error': error_msg,
                'outputs': {},
                'agent': agent_name
            }
    
    def _prepare_stage_inputs(self, stage_config: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare inputs for a stage based on dependencies."""
        inputs = {}
        
        # Add policy document path and content for first stage
        if 'policy_document_path' in self.workflow_state:
            inputs['policy_document_path'] = self.workflow_state['policy_document_path']
        if 'policy_document' in self.workflow_state:
            inputs['policy_document'] = self.workflow_state['policy_document']
        
        # Add detected visa type hints for hybrid approach
        if 'detected_visa_type' in self.workflow_state:
            inputs['detected_visa_type'] = self.workflow_state['detected_visa_type']
            print(f" ORCHESTRATOR: Adding detected_visa_type = {self.workflow_state['detected_visa_type']} ", flush=True)
        if 'detected_visa_code' in self.workflow_state:
            inputs['detected_visa_code'] = self.workflow_state['detected_visa_code']
            print(f" ORCHESTRATOR: Adding detected_visa_code = {self.workflow_state['detected_visa_code']} ", flush=True)
        if 'force_visa_type' in self.workflow_state:
            inputs['force_visa_type'] = self.workflow_state['force_visa_type']
            print(f" ORCHESTRATOR: Adding force_visa_type = {self.workflow_state['force_visa_type']} ", flush=True)
        
        # Add outputs from dependent stages
        depends_on = stage_config.get('depends_on', [])
        
        if depends_on:
            # Add all previous outputs
            for key, value in self.workflow_state.items():
                if key not in ['policy_document_path', 'output_dir', 'start_time']:
                    inputs[key] = value
        
        return inputs
    
    def run_single_stage(
        self,
        stage_name: str,
        inputs: Dict[str, Any],
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a single stage independently.
        
        Args:
            stage_name: Name of the stage to run
            inputs: Input data for the stage
            output_dir: Directory to save outputs
            
        Returns:
            Stage execution results
        """
        # Find stage config
        stages = self.workflow_config['workflow']['stages']
        stage_config = next((s for s in stages if s['name'] == stage_name), None)
        
        if not stage_config:
            raise ValueError(f"Stage not found: {stage_name}")
        
        # Set output directory
        if output_dir is None:
            project_root = Path(__file__).parent.parent.parent
            output_dir = project_root / 'data' / 'output'
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Execute stage
        return self._execute_stage(stage_config, output_dir)
    
    def get_workflow_state(self) -> Dict[str, Any]:
        """Get current workflow state."""
        return self.workflow_state
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history for all agents."""
        history = {}
        for agent_name, agent in self.agents.items():
            history[agent_name] = agent.get_execution_history()
        return history
