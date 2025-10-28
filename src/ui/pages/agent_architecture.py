"""
Agent Architecture Overview Page
Explains the role, inputs, outputs, and interactions of each agent in the system.
"""

import streamlit as st
import json
from pathlib import Path

def show_agent_architecture():
    """Display comprehensive agent architecture information."""
    
    # Page header
    st.markdown("""
    <style>
        .agent-card {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 0.5rem;
        }
        .agent-title {
            color: #007bff;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .io-section {
            background-color: #ffffff;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0.25rem;
            border: 1px solid #e9ecef;
        }
        .input-box {
            background-color: #e8f5e8;
            border-left: 3px solid #28a745;
        }
        .output-box {
            background-color: #fff3cd;
            border-left: 3px solid #ffc107;
        }
        .interaction-box {
            background-color: #e7f3ff;
            border-left: 3px solid #17a2b8;
        }
        .workflow-diagram {
            text-align: center;
            padding: 2rem;
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            margin: 2rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏗️ Agent Architecture Overview")
    st.markdown("**Understanding the Visa Requirements Agent System**")
    
    # System Overview
    st.markdown("## 🎯 System Overview")
    st.markdown("""
    The Visa Requirements Agent is a multi-agent system that processes immigration policy documents 
    and generates comprehensive application requirements and questions. The system operates through 
    5 specialized agents working in sequence to deliver complete policy analysis.
    """)
    
    # Workflow Diagram
    st.markdown("## 🔄 Agent Workflow")
    st.markdown("""
    <div class="workflow-diagram">
        <h3>📄 Policy Document</h3>
        ⬇️
        <h4>🔍 PolicyEvaluator Agent</h4>
        ⬇️
        <h4>📋 RequirementsCapture Agent</h4>
        ⬇️
        <h4>❓ QuestionGenerator Agent</h4>
        ⬇️
        <h4>✅ ValidationAgent</h4>
        ⬇️
        <h4>🔗 ConsolidationAgent</h4>
        ⬇️
        <h3>📊 Final Results</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent Details
    st.markdown("## 🤖 Agent Details")
    
    # PolicyEvaluator Agent
    st.markdown("""
    <div class="agent-card">
        <div class="agent-title">🔍 PolicyEvaluator Agent</div>
        <p><strong>Purpose:</strong> Analyzes immigration policy documents to extract structure, eligibility rules, and conditions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="io-section input-box">
            <h4>📥 Inputs</h4>
            <ul>
                <li><strong>policy_path:</strong> Path to policy document</li>
                <li><strong>policy_content:</strong> Raw document text</li>
                <li><strong>detected_visa_type:</strong> Pre-detected visa type (optional)</li>
                <li><strong>detected_visa_code:</strong> Pre-detected visa code (optional)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="io-section output-box">
            <h4>📤 Outputs</h4>
            <ul>
                <li><strong>policy_structure:</strong> Visa type, code, objectives</li>
                <li><strong>eligibility_rules:</strong> Who can apply, sponsor requirements</li>
                <li><strong>conditions:</strong> Visa conditions and restrictions</li>
                <li><strong>sections:</strong> Document structure analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="io-section interaction-box">
        <h4>🔗 Agent-to-Agent Interactions</h4>
        <ul>
            <li><strong>Receives:</strong> Raw policy document from workflow orchestrator</li>
            <li><strong>Sends to:</strong> RequirementsCapture Agent (policy structure and rules)</li>
            <li><strong>LLM Methods (V2):</strong> _analyze_policy_structure_llm(), _extract_eligibility_rules_llm(), _extract_conditions_llm()</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # RequirementsCapture Agent
    st.markdown("""
    <div class="agent-card">
        <div class="agent-title">📋 RequirementsCapture Agent</div>
        <p><strong>Purpose:</strong> Transforms policy analysis into specific, actionable requirements for visa applications.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="io-section input-box">
            <h4>📥 Inputs</h4>
            <ul>
                <li><strong>policy_structure:</strong> From PolicyEvaluator</li>
                <li><strong>eligibility_rules:</strong> From PolicyEvaluator</li>
                <li><strong>conditions:</strong> From PolicyEvaluator</li>
                <li><strong>sections:</strong> Document sections</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="io-section output-box">
            <h4>📤 Outputs</h4>
            <ul>
                <li><strong>functional_requirements:</strong> Core application requirements</li>
                <li><strong>data_requirements:</strong> Information that must be provided</li>
                <li><strong>business_rules:</strong> Processing and validation rules</li>
                <li><strong>validation_rules:</strong> Data validation criteria</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="io-section interaction-box">
        <h4>🔗 Agent-to-Agent Interactions</h4>
        <ul>
            <li><strong>Receives:</strong> Policy analysis from PolicyEvaluator Agent</li>
            <li><strong>Sends to:</strong> QuestionGenerator Agent (structured requirements)</li>
            <li><strong>Processing:</strong> Converts policy text into structured requirement objects</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # QuestionGenerator Agent
    st.markdown("""
    <div class="agent-card">
        <div class="agent-title">❓ QuestionGenerator Agent</div>
        <p><strong>Purpose:</strong> Generates user-friendly application form questions based on requirements.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="io-section input-box">
            <h4>📥 Inputs</h4>
            <ul>
                <li><strong>functional_requirements:</strong> From RequirementsCapture</li>
                <li><strong>data_requirements:</strong> From RequirementsCapture</li>
                <li><strong>business_rules:</strong> From RequirementsCapture</li>
                <li><strong>policy_structure:</strong> Visa context information</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="io-section output-box">
            <h4>📤 Outputs</h4>
            <ul>
                <li><strong>questions:</strong> Complete application form questions</li>
                <li><strong>sections:</strong> Organized question categories</li>
                <li><strong>validation_rules:</strong> Question validation criteria</li>
                <li><strong>help_text:</strong> User guidance for each question</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="io-section interaction-box">
        <h4>🔗 Agent-to-Agent Interactions</h4>
        <ul>
            <li><strong>Receives:</strong> Structured requirements from RequirementsCapture Agent</li>
            <li><strong>Sends to:</strong> ValidationAgent (questions for validation)</li>
            <li><strong>LLM Methods (V2):</strong> _generate_applicant_questions_llm(), _generate_sponsor_questions_llm(), _generate_dependent_questions_llm(), _generate_financial_questions_llm(), _generate_health_character_questions_llm()</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # ValidationAgent
    st.markdown("""
    <div class="agent-card">
        <div class="agent-title">✅ ValidationAgent</div>
        <p><strong>Purpose:</strong> Validates requirements and questions for completeness, consistency, and quality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="io-section input-box">
            <h4>📥 Inputs</h4>
            <ul>
                <li><strong>requirements:</strong> All requirement types</li>
                <li><strong>questions:</strong> Generated questions</li>
                <li><strong>policy_structure:</strong> Policy context</li>
                <li><strong>sections:</strong> Document organization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="io-section output-box">
            <h4>📤 Outputs</h4>
            <ul>
                <li><strong>validation_report:</strong> Quality assessment scores</li>
                <li><strong>gap_analysis:</strong> Missing elements identification</li>
                <li><strong>recommendations:</strong> Improvement suggestions</li>
                <li><strong>overall_score:</strong> System quality percentage</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="io-section interaction-box">
        <h4>🔗 Agent-to-Agent Interactions</h4>
        <ul>
            <li><strong>Receives:</strong> Requirements and questions from previous agents</li>
            <li><strong>Sends to:</strong> ConsolidationAgent (validation results)</li>
            <li><strong>LLM Methods (V2):</strong> _validate_requirements_llm(), _validate_questions_llm(), _analyze_coverage_llm(), _check_consistency_llm(), _identify_gaps_llm()</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # ConsolidationAgent
    st.markdown("""
    <div class="agent-card">
        <div class="agent-title">🔗 ConsolidationAgent</div>
        <p><strong>Purpose:</strong> Combines all agent outputs into a final, comprehensive result package.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="io-section input-box">
            <h4>📥 Inputs</h4>
            <ul>
                <li><strong>All agent outputs:</strong> Complete workflow results</li>
                <li><strong>Metadata:</strong> Processing information</li>
                <li><strong>Validation results:</strong> Quality assessments</li>
                <li><strong>Timing data:</strong> Performance metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="io-section output-box">
            <h4>📤 Outputs</h4>
            <ul>
                <li><strong>consolidated_results:</strong> Final system output</li>
                <li><strong>summary:</strong> Executive summary</li>
                <li><strong>metadata:</strong> Processing statistics</li>
                <li><strong>recommendations:</strong> System-wide suggestions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="io-section interaction-box">
        <h4>🔗 Agent-to-Agent Interactions</h4>
        <ul>
            <li><strong>Receives:</strong> All outputs from previous 4 agents</li>
            <li><strong>Sends to:</strong> Workflow orchestrator (final results)</li>
            <li><strong>Processing:</strong> Creates unified result structure for UI display</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Version Differences
    st.markdown("## 🔄 Version Differences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 V1_Demo Mode (Port 8501)
        - **Execution**: Fallback methods only
        - **Speed**: 0.0 seconds (instant)
        - **Content**: Template-based, consistent
        - **Validation**: Fixed 75% scores
        - **Use Case**: Presentations and demos
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 V2_LiveAPI Mode (Port 8502)
        - **Execution**: Real LLM calls to OpenAI GPT-4
        - **Speed**: 30-60 seconds (authentic processing)
        - **Content**: AI-generated, varies each run
        - **Validation**: Real analysis scores
        - **Use Case**: Production policy analysis
        """)
    
    # Technical Implementation
    st.markdown("## ⚙️ Technical Implementation")
    
    st.markdown("""
    ### Environment Variables
    - **VISA_AGENT_VERSION**: Controls UI mode (`v1_demo` or `v2_live_api`)
    - **VISA_AGENT_FORCE_LLM**: Forces LLM calls when `true`
    - **OPENAI_API_KEY**: Required for V2 mode operation
    
    ### Agent Method Patterns
    - **Base Methods**: `_method_name()` - Fallback implementations
    - **LLM Methods**: `_method_name_llm()` - Real AI implementations
    - **Version Detection**: Automatic selection based on environment
    
    ### Error Handling
    - **Graceful Degradation**: LLM failures fall back to base methods
    - **Rich Fallbacks**: High-quality template content when needed
    - **Comprehensive Logging**: Detailed debug output for troubleshooting
    """)
    
    # Data Flow Summary
    st.markdown("## 📊 Data Flow Summary")
    
    st.markdown("""
    ```
    Policy Document
    ├── PolicyEvaluator → policy_structure, eligibility_rules, conditions
    │   └── RequirementsCapture → functional_requirements, data_requirements, business_rules
    │       └── QuestionGenerator → questions, sections, validation_rules
    │           └── ValidationAgent → validation_report, gap_analysis, recommendations
    │               └── ConsolidationAgent → consolidated_results, summary, metadata
    │                   └── Final Results (UI Display)
    ```
    """)
    
    # Performance Metrics
    st.markdown("## 📈 Performance Metrics")
    
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    with metrics_col1:
        st.metric("V1 Demo Speed", "0.0s", "Instant")
        st.metric("V1 Consistency", "100%", "Always same")
    
    with metrics_col2:
        st.metric("V2 Live Speed", "30-60s", "Real processing")
        st.metric("V2 Authenticity", "100%", "AI generated")
    
    with metrics_col3:
        st.metric("Total Agents", "5", "Specialized roles")
        st.metric("LLM Methods", "13", "Real AI calls")

if __name__ == "__main__":
    show_agent_architecture()
