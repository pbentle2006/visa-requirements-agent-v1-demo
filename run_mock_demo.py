#!/usr/bin/env python3
"""
Mock Demo Runner

Runs the visa requirements workflow using pre-generated mock data instead of LLM APIs.
Perfect for demonstrations when API quotas are exceeded or internet is unavailable.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.generators.mock_results_generator import MockResultsGenerator
from src.utils.output_formatter import OutputFormatter


def main():
    """Run mock demo with pre-generated results."""
    print("=" * 80)
    print("VISA REQUIREMENTS AGENT - MOCK DEMO")
    print("=" * 80)
    print()
    
    print("🎭 Running demo with mock data (no API calls required)")
    print("📄 Policy document: Parent Boost Visitor Visa (simulated)")
    print()
    
    # Initialize mock generator
    print("🔧 Initializing mock workflow...")
    generator = MockResultsGenerator()
    print("✅ Mock system initialized")
    print()
    
    # Generate mock results
    print("🚀 Running simulated workflow...")
    print("   This demonstrates the complete process in seconds...")
    print()
    
    # Simulate processing time
    import time
    
    print("   Stage 1: Policy Analysis... ", end="", flush=True)
    time.sleep(0.5)
    print("✅ Complete (0.8s)")
    
    print("   Stage 2: Requirements Capture... ", end="", flush=True)
    time.sleep(0.7)
    print("✅ Complete (1.2s)")
    
    print("   Stage 3: Question Generation... ", end="", flush=True)
    time.sleep(0.9)
    print("✅ Complete (1.8s)")
    
    print("   Stage 4: Validation & QA... ", end="", flush=True)
    time.sleep(0.6)
    print("✅ Complete (0.9s)")
    
    print("   Stage 5: Consolidation... ", end="", flush=True)
    time.sleep(0.4)
    print("✅ Complete (0.6s)")
    
    print()
    
    # Generate complete results
    results = generator.generate_complete_workflow_results("Parent Boost Visitor Visa")
    
    print("=" * 80)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print(f"Status: {results['status']}")
    print(f"Total Duration: {results['duration_seconds']:.1f}s")
    print(f"Stages Completed: {len(results['stages'])}/5")
    print()
    
    # Display key results
    display_results_summary(results)
    
    # Save results
    save_mock_results(results)
    
    print()
    print("🎯 Demo Highlights:")
    print("   ✅ Complete end-to-end workflow simulation")
    print("   ✅ Realistic data generation without API calls")
    print("   ✅ All 5 agents working in harmony")
    print("   ✅ Comprehensive validation and quality checks")
    print("   ✅ Production-ready output formats")
    
    print()
    print("💡 This demonstrates:")
    print("   • System architecture and workflow")
    print("   • Data structures and output formats")
    print("   • Quality validation and gap analysis")
    print("   • Complete traceability matrix")
    print("   • Ready-to-implement specifications")
    
    print()
    print("🚀 To run with real LLM APIs:")
    print("   1. Add payment method to OpenAI account")
    print("   2. Run: python run_demo.py")
    print("   3. Or use Streamlit: streamlit run src/ui/streamlit_app.py")
    
    return 0


def display_results_summary(results):
    """Display a summary of the generated results."""
    outputs = results['outputs']
    
    print("📊 RESULTS SUMMARY")
    print("-" * 80)
    
    # Summary statistics
    stats = outputs['summary_statistics']
    print(f"📋 Requirements Generated: {stats['total_requirements']}")
    print(f"   • Functional: {stats['requirements_by_type']['functional']}")
    print(f"   • Data: {stats['requirements_by_type']['data']}")
    print(f"   • Business Rules: {stats['requirements_by_type']['business_rules']}")
    print(f"   • Validation: {stats['requirements_by_type']['validation']}")
    print()
    
    print(f"❓ Questions Generated: {stats['total_questions']}")
    for section, count in stats['questions_by_section'].items():
        print(f"   • {section}: {count}")
    print()
    
    # Validation results
    validation = outputs['validation_report']
    print(f"✅ Quality Metrics:")
    print(f"   • Overall Score: {validation['overall_score']:.1f}%")
    print(f"   • Requirements Valid: {validation['requirement_validation']['validation_rate']:.1f}%")
    print(f"   • Questions Valid: {validation['question_validation']['validation_rate']:.1f}%")
    print(f"   • Policy Coverage: {stats['policy_coverage']:.1f}%")
    print()
    
    # Sample requirements
    print("📝 Sample Requirements (first 3):")
    for i, req in enumerate(outputs['functional_requirements'][:3]):
        print(f"   {i+1}. {req['requirement_id']}: {req['description']}")
        print(f"      Priority: {req['priority']} | Ref: {req['policy_reference']}")
    print()
    
    # Sample questions
    print("❓ Sample Questions (first 3):")
    for i, q in enumerate(outputs['application_questions'][:3]):
        print(f"   {i+1}. {q['question_text']}")
        print(f"      Type: {q['input_type']} | Required: {q['required']} | Section: {q['section']}")
    print()
    
    # Recommendations
    recommendations = outputs['recommendations']
    if recommendations:
        print("💡 Recommendations:")
        for rec in recommendations:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "⚪")
            print(f"   {priority_icon} {rec['priority'].upper()}: {rec['description']}")
    print()


def save_mock_results(results):
    """Save mock results to output directory."""
    print("💾 Saving results...")
    
    # Ensure output directory exists
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save complete results
    results_file = output_dir / "mock_demo_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save individual components
    outputs = results['outputs']
    
    # Requirements
    req_file = output_dir / "mock_requirements.json"
    requirements_data = {
        'functional_requirements': outputs['functional_requirements'],
        'data_requirements': outputs['data_requirements'],
        'business_rules': outputs['business_rules'],
        'validation_rules': outputs['validation_rules']
    }
    with open(req_file, 'w') as f:
        json.dump(requirements_data, f, indent=2)
    
    # Questions
    questions_file = output_dir / "mock_questions.json"
    with open(questions_file, 'w') as f:
        json.dump(outputs['application_questions'], f, indent=2)
    
    # Summary report
    summary_file = output_dir / "mock_summary_report.txt"
    with open(summary_file, 'w') as f:
        f.write("VISA REQUIREMENTS AGENT - MOCK DEMO RESULTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Status: {results['status']}\n")
        f.write(f"Duration: {results['duration_seconds']:.1f}s\n\n")
        
        stats = outputs['summary_statistics']
        f.write("SUMMARY STATISTICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Requirements: {stats['total_requirements']}\n")
        f.write(f"Total Questions: {stats['total_questions']}\n")
        f.write(f"Validation Score: {stats['validation_score']:.1f}%\n")
        f.write(f"Policy Coverage: {stats['policy_coverage']:.1f}%\n\n")
        
        f.write("This mock demo demonstrates the complete workflow\n")
        f.write("and output formats of the Visa Requirements Agent system.\n")
    
    print(f"   ✅ Complete results: {results_file}")
    print(f"   ✅ Requirements: {req_file}")
    print(f"   ✅ Questions: {questions_file}")
    print(f"   ✅ Summary report: {summary_file}")


if __name__ == '__main__':
    sys.exit(main())
