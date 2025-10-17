#!/usr/bin/env python3
"""
Synthetic Data Generation Demo

This script demonstrates how to generate synthetic policy documents and mock results
for testing and demonstration purposes.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.generators.policy_generator import PolicyGenerator
from src.generators.mock_results_generator import MockResultsGenerator


def main():
    """Run synthetic data generation demo."""
    print("=" * 80)
    print("SYNTHETIC DATA GENERATION DEMO")
    print("=" * 80)
    print()
    
    # Initialize generators
    print("🔧 Initializing generators...")
    policy_gen = PolicyGenerator()
    results_gen = MockResultsGenerator()
    print("✅ Generators initialized")
    print()
    
    # Generate synthetic policies
    print("📄 Generating synthetic policy documents...")
    
    policy_specifications = [
        {
            "name": "tourist_visa",
            "visa_category": "visitor",
            "visa_name": "Tourist Visa",
            "complexity": "simple"
        },
        {
            "name": "skilled_worker_visa",
            "visa_category": "work", 
            "visa_name": "Skilled Worker Visa",
            "complexity": "complex"
        },
        {
            "name": "student_visa",
            "visa_category": "student",
            "visa_name": "International Student Visa", 
            "complexity": "medium"
        },
        {
            "name": "family_reunion_visa",
            "visa_category": "family",
            "visa_name": "Family Reunion Visa",
            "complexity": "medium"
        }
    ]
    
    # Generate policies
    policies = policy_gen.generate_multiple_policies(policy_specifications)
    
    print(f"✅ Generated {len(policies)} synthetic policies:")
    for name, content in policies.items():
        print(f"   - {name}: {len(content)} characters")
        
        # Save policy to file
        filename = f"{name}.txt"
        file_path = policy_gen.save_policy(content, filename, "data/synthetic")
        print(f"     Saved to: {file_path}")
    
    print()
    
    # Generate mock workflow results for each policy
    print("🔄 Generating mock workflow results...")
    
    all_results = {}
    for spec in policy_specifications:
        policy_name = spec["visa_name"]
        print(f"   Processing: {policy_name}")
        
        # Generate complete mock results
        results = results_gen.generate_complete_workflow_results(policy_name)
        all_results[spec["name"]] = results
        
        # Show summary
        stats = results['outputs']['summary_statistics']
        print(f"     - Requirements: {stats['total_requirements']}")
        print(f"     - Questions: {stats['total_questions']}")
        print(f"     - Validation Score: {stats['validation_score']}%")
    
    print()
    
    # Save all results
    print("💾 Saving results...")
    
    output_dir = Path("data/synthetic/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save individual results
    for name, results in all_results.items():
        result_file = output_dir / f"{name}_results.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"   - {result_file}")
    
    # Save combined results
    combined_file = output_dir / "all_synthetic_results.json"
    with open(combined_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"   - {combined_file}")
    
    print()
    
    # Generate comparison analysis
    print("📊 Generating comparison analysis...")
    
    comparison = generate_comparison_analysis(all_results)
    
    comparison_file = output_dir / "comparison_analysis.json"
    with open(comparison_file, 'w') as f:
        json.dump(comparison, f, indent=2, default=str)
    
    print("✅ Comparison analysis saved")
    print()
    
    # Show summary
    print("=" * 80)
    print("SYNTHETIC DATA GENERATION COMPLETE")
    print("=" * 80)
    print(f"📁 Policies generated: {len(policies)}")
    print(f"📊 Result sets created: {len(all_results)}")
    print(f"💾 Files saved to: data/synthetic/")
    print()
    
    print("📈 Summary Statistics:")
    for name, results in all_results.items():
        stats = results['outputs']['summary_statistics']
        print(f"   {name}:")
        print(f"     Requirements: {stats['total_requirements']}")
        print(f"     Questions: {stats['total_questions']}")
        print(f"     Validation: {stats['validation_score']}%")
    
    print()
    print("🎯 Use Cases Demonstrated:")
    print("   ✅ Generate realistic policy documents from templates")
    print("   ✅ Create comprehensive mock workflow results")
    print("   ✅ Compare different visa types and complexities")
    print("   ✅ Provide complete datasets for testing and demos")
    print("   ✅ Showcase system capabilities without API dependencies")
    
    print()
    print("🚀 Next Steps:")
    print("   1. Use synthetic policies to test the system")
    print("   2. Load mock results into Streamlit for demo")
    print("   3. Compare different visa processing approaches")
    print("   4. Validate system performance with various inputs")
    
    return 0


def generate_comparison_analysis(all_results):
    """Generate comparison analysis across different visa types."""
    
    comparison = {
        "generated_at": datetime.now().isoformat(),
        "visa_types_compared": len(all_results),
        "metrics_comparison": {},
        "complexity_analysis": {},
        "coverage_analysis": {}
    }
    
    # Extract metrics for comparison
    metrics = {}
    for name, results in all_results.items():
        stats = results['outputs']['summary_statistics']
        validation = results['outputs']['validation_report']
        
        metrics[name] = {
            "total_requirements": stats['total_requirements'],
            "total_questions": stats['total_questions'],
            "validation_score": stats['validation_score'],
            "policy_coverage": stats['policy_coverage'],
            "processing_time": stats['processing_time'],
            "requirements_by_type": stats['requirements_by_type'],
            "questions_by_section": stats['questions_by_section']
        }
    
    comparison["metrics_comparison"] = metrics
    
    # Complexity analysis
    complexity_scores = {}
    for name, data in metrics.items():
        # Calculate complexity score based on various factors
        complexity_score = (
            data['total_requirements'] * 0.3 +
            data['total_questions'] * 0.2 +
            (100 - data['validation_score']) * 0.3 +  # Higher complexity if lower validation
            data['processing_time'] / 10 * 0.2  # Processing time factor
        )
        complexity_scores[name] = round(complexity_score, 2)
    
    comparison["complexity_analysis"] = {
        "complexity_scores": complexity_scores,
        "most_complex": max(complexity_scores.items(), key=lambda x: x[1]),
        "least_complex": min(complexity_scores.items(), key=lambda x: x[1]),
        "average_complexity": round(sum(complexity_scores.values()) / len(complexity_scores), 2)
    }
    
    # Coverage analysis
    coverage_stats = {name: data['policy_coverage'] for name, data in metrics.items()}
    comparison["coverage_analysis"] = {
        "coverage_by_type": coverage_stats,
        "highest_coverage": max(coverage_stats.items(), key=lambda x: x[1]),
        "lowest_coverage": min(coverage_stats.items(), key=lambda x: x[1]),
        "average_coverage": round(sum(coverage_stats.values()) / len(coverage_stats), 2)
    }
    
    return comparison


if __name__ == '__main__':
    sys.exit(main())
