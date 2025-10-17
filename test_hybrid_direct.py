#!/usr/bin/env python3
"""
Direct test of the hybrid approach without Streamlit
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator
from src.utils.enhanced_document_parser import EnhancedDocumentParser

def test_hybrid_approach(document_path: str):
    """Test the hybrid approach directly"""
    
    print("=" * 80)
    print("🚀 DIRECT HYBRID APPROACH TEST 🚀")
    print("=" * 80)
    
    # Read document content
    parser = EnhancedDocumentParser()
    try:
        doc_result = parser.load_document(document_path)
        policy_content = doc_result.get('content', '')
        print(f"✅ Document parsed successfully: {len(policy_content)} characters")
        print(f"📄 First 300 chars: {policy_content[:300]}...")
    except Exception as e:
        print(f"❌ Failed to parse document: {e}")
        return
    
    # HYBRID APPROACH - Detect visa type
    detected_visa_type = None
    detected_visa_code = None
    
    print("\n🔍 VISA TYPE DETECTION:")
    content_upper = policy_content.upper()
    
    print(f"🔍 Checking for PARENT BOOST: {'PARENT BOOST' in content_upper}")
    print(f"🔍 Checking for V4: {'V4' in content_upper}")
    print(f"🔍 Checking for PARENT: {'PARENT' in content_upper}")
    print(f"🔍 Checking for BOOST: {'BOOST' in content_upper}")
    print(f"🔍 Checking for VISITOR: {'VISITOR' in content_upper}")
    print(f"🔍 Checking for SKILLED MIGRANT: {'SKILLED MIGRANT' in content_upper}")
    print(f"🔍 Checking for WORKING HOLIDAY: {'WORKING HOLIDAY' in content_upper}")
    
    if any(keyword in content_upper for keyword in ['PARENT BOOST VISITOR VISA', 'PARENT BOOST', 'V4']):
        detected_visa_type = "Parent Boost Visitor Visa"
        detected_visa_code = "V4"
        print(f"🎯 DETECTED: PARENT BOOST VISITOR VISA (V4)")
    elif any(keyword in content_upper for keyword in ['SKILLED MIGRANT', 'SR1', 'SR3', 'SR4', 'SR5', 'SKILLED RESIDENCE']):
        detected_visa_type = "Skilled Migrant Residence Visa"
        detected_visa_code = "SR1"
        print(f"🎯 DETECTED: SKILLED MIGRANT RESIDENCE VISA (SR1)")
    elif any(keyword in content_upper for keyword in ['WORKING HOLIDAY', 'YOUTH', 'TEMPORARY WORK', 'WHV']):
        detected_visa_type = "Working Holiday Visa"
        detected_visa_code = "WHV"
        print(f"🎯 DETECTED: WORKING HOLIDAY VISA (WHV)")
    else:
        print(f"❌ NO SPECIFIC VISA TYPE DETECTED")
        print(f"📝 Content sample: {content_upper[:500]}...")
    
    # Run workflow with hybrid approach
    print(f"\n🚀 RUNNING WORKFLOW WITH HYBRID APPROACH:")
    print(f"📋 Detected Visa Type: {detected_visa_type}")
    print(f"📋 Detected Visa Code: {detected_visa_code}")
    print(f"📋 Force Visa Type: {bool(detected_visa_type)}")
    
    orchestrator = WorkflowOrchestrator()
    
    try:
        results = orchestrator.run_workflow(
            document_path,
            policy_content,
            detected_visa_type=detected_visa_type,
            detected_visa_code=detected_visa_code,
            force_visa_type=bool(detected_visa_type)
        )
        
        print(f"\n✅ WORKFLOW COMPLETED:")
        print(f"📊 Status: {results['status']}")
        print(f"⏱️ Duration: {results['duration_seconds']:.1f}s")
        print(f"📈 Stages: {len([s for s in results['stages'] if s['status'] == 'success'])}/{len(results['stages'])}")
        
        # Check policy structure
        policy_structure = results['outputs'].get('policy_structure', {})
        print(f"\n🏛️ POLICY STRUCTURE RESULTS:")
        print(f"📋 Visa Type: {policy_structure.get('visa_type', 'Not found')}")
        print(f"📋 Visa Code: {policy_structure.get('visa_code', 'Not found')}")
        
        if detected_visa_type:
            if policy_structure.get('visa_type') == detected_visa_type:
                print(f"✅ SUCCESS: Visa type matches detection!")
            else:
                print(f"❌ MISMATCH: Expected {detected_visa_type}, got {policy_structure.get('visa_type')}")
        
        return results
        
    except Exception as e:
        print(f"❌ WORKFLOW FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_hybrid_direct.py <path_to_document>")
        print("Example: python test_hybrid_direct.py data/sample_policies/parent_boost_policy.docx")
        sys.exit(1)
    
    document_path = sys.argv[1]
    if not Path(document_path).exists():
        print(f"❌ Document not found: {document_path}")
        sys.exit(1)
    
    results = test_hybrid_approach(document_path)
    
    if results:
        print(f"\n🎉 TEST COMPLETED SUCCESSFULLY!")
    else:
        print(f"\n💥 TEST FAILED!")
