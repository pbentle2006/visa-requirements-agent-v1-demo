import json
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime


class OutputFormatter:
    """Utility class for formatting and saving agent outputs."""
    
    @staticmethod
    def save_json(data: Dict[str, Any], output_path: str, pretty: bool = True):
        """
        Save data as JSON file.
        
        Args:
            data: Data to save
            output_path: Path to output file
            pretty: Whether to pretty-print JSON
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
    
    @staticmethod
    def load_json(input_path: str) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Args:
            input_path: Path to input file
            
        Returns:
            Loaded data
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def format_requirements(requirements: List[Dict[str, Any]]) -> str:
        """
        Format requirements as human-readable text.
        
        Args:
            requirements: List of requirement dictionaries
            
        Returns:
            Formatted string
        """
        output = []
        output.append("=" * 80)
        output.append("REQUIREMENTS SUMMARY")
        output.append("=" * 80)
        output.append("")
        
        # Group by type
        by_type = {}
        for req in requirements:
            req_type = req.get('type', 'unknown')
            if req_type not in by_type:
                by_type[req_type] = []
            by_type[req_type].append(req)
        
        for req_type, reqs in by_type.items():
            output.append(f"\n{req_type.upper().replace('_', ' ')}")
            output.append("-" * 80)
            
            for req in reqs:
                output.append(f"\nID: {req.get('requirement_id', 'N/A')}")
                output.append(f"Description: {req.get('description', 'N/A')}")
                output.append(f"Priority: {req.get('priority', 'N/A')}")
                output.append(f"Policy Ref: {req.get('policy_reference', 'N/A')}")
                output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def format_questions(questions: List[Dict[str, Any]]) -> str:
        """
        Format questions as human-readable text.
        
        Args:
            questions: List of question dictionaries
            
        Returns:
            Formatted string
        """
        output = []
        output.append("=" * 80)
        output.append("APPLICATION QUESTIONS")
        output.append("=" * 80)
        output.append("")
        
        # Group by section
        by_section = {}
        for q in questions:
            section = q.get('section', 'General')
            if section not in by_section:
                by_section[section] = []
            by_section[section].append(q)
        
        for section, qs in by_section.items():
            output.append(f"\n{section.upper()}")
            output.append("-" * 80)
            
            for q in qs:
                output.append(f"\nQ{q.get('question_id', 'N/A')}: {q.get('question_text', 'N/A')}")
                output.append(f"Type: {q.get('input_type', 'N/A')}")
                output.append(f"Required: {q.get('required', False)}")
                
                if q.get('help_text'):
                    output.append(f"Help: {q['help_text']}")
                
                if q.get('policy_reference'):
                    output.append(f"Policy Ref: {q['policy_reference']}")
                
                output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def create_summary_report(workflow_results: Dict[str, Any]) -> str:
        """
        Create a summary report of workflow execution.
        
        Args:
            workflow_results: Results from workflow orchestrator
            
        Returns:
            Formatted summary report
        """
        output = []
        output.append("=" * 80)
        output.append("VISA REQUIREMENTS WORKFLOW SUMMARY")
        output.append("=" * 80)
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        
        # Execution summary
        output.append("EXECUTION SUMMARY")
        output.append("-" * 80)
        output.append(f"Total Stages: {len(workflow_results.get('stages', []))}")
        output.append(f"Status: {workflow_results.get('status', 'unknown')}")
        output.append(f"Duration: {workflow_results.get('duration_seconds', 0):.2f}s")
        output.append("")
        
        # Stage details
        output.append("STAGE DETAILS")
        output.append("-" * 80)
        for stage in workflow_results.get('stages', []):
            output.append(f"\n{stage['name'].upper()}")
            output.append(f"  Status: {stage.get('status', 'unknown')}")
            output.append(f"  Duration: {stage.get('duration_seconds', 0):.2f}s")
            
            if stage.get('outputs'):
                output.append(f"  Outputs: {', '.join(stage['outputs'].keys())}")
        
        output.append("")
        
        return "\n".join(output)
