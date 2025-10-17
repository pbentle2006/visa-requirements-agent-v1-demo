#!/usr/bin/env python3
"""
Quick start script for running the visa requirements agent demo.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / '.env')

from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator


def main():
    """Run the demo workflow."""
    print("=" * 80)
    print("VISA REQUIREMENTS AGENT DEMO")
    print("=" * 80)
    print()
    
    # Check for API key
    import os
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print()
        print("Please create a .env file with your OpenAI API key:")
        print("  OPENAI_API_KEY=your_api_key_here")
        print()
        return 1
    
    # Policy document path
    policy_path = project_root / 'data' / 'input' / 'parent_boost_policy.txt'
    
    if not policy_path.exists():
        print(f"❌ Error: Policy document not found at {policy_path}")
        return 1
    
    print(f"📄 Policy document: {policy_path.name}")
    print()
    
    # Initialize orchestrator
    print("🔧 Initializing workflow orchestrator...")
    orchestrator = WorkflowOrchestrator()
    print("✅ Orchestrator initialized")
    print()
    
    # Run workflow
    print("🚀 Running complete workflow...")
    print("   This may take a few minutes...")
    print()
    
    try:
        results = orchestrator.run_workflow(str(policy_path))
        
        print()
        print("=" * 80)
        print("WORKFLOW COMPLETED")
        print("=" * 80)
        print(f"Status: {results['status']}")
        print(f"Duration: {results['duration_seconds']:.2f}s")
        print(f"Stages: {len(results['stages'])}")
        print()
        
        # Summary statistics
        summary_stats = results['outputs'].get('summary_statistics', {})
        if summary_stats:
            print("📊 Summary Statistics:")
            print(f"  Total Requirements: {summary_stats.get('total_requirements', 0)}")
            print(f"  Total Questions: {summary_stats.get('total_questions', 0)}")
            
            validation_score = results['outputs'].get('validation_report', {}).get('overall_score', 0)
            print(f"  Validation Score: {validation_score:.1f}%")
        
        print()
        print(f"📁 Results saved to: {project_root / 'data' / 'output'}")
        print()
        print("To view detailed results:")
        print(f"  streamlit run src/ui/streamlit_app.py")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 80)
        print("WORKFLOW FAILED")
        print("=" * 80)
        print(f"Error: {str(e)}")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
