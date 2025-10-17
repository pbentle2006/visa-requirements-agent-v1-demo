# Agent Architecture & Build Documentation

## System Overview

The Visa Requirements Agent System is a multi-agent architecture where specialized AI agents collaborate to transform policy documents into validated, actionable requirements and application questions.

### Architecture Principles

1. **Single Responsibility:** Each agent has one clear purpose
2. **Loose Coupling:** Agents communicate through well-defined interfaces
3. **High Cohesion:** Related functionality grouped within agents
4. **Extensibility:** Easy to add new agents or modify existing ones
5. **Observability:** All agent actions are logged and traceable

## Agent Communication Flow

```
Policy Document
      ↓
PolicyEvaluator → RequirementsCapture → QuestionGenerator
      ↓                    ↓                    ↓
      └─────────────→ ValidationAgent ←────────┘
                           ↓
                  ConsolidationAgent
                           ↓
              Final Specification
```

## Agent Catalog

### 1. PolicyEvaluator Agent

**Purpose:** Parse and understand immigration policy documents

**Key Responsibilities:**
- Load and parse policy documents (TXT, PDF, DOCX)
- Extract document structure (sections, subsections)
- Identify key policy elements (objectives, requirements, conditions)
- Extract eligibility rules and criteria
- Parse numerical thresholds and limits
- Identify stakeholders and their roles

**Input Schema:**
```json
{
  "policy_document_path": "string (required)",
  "policy_document": "string (optional raw text)"
}
```

**Output Schema:**
```json
{
  "policy_structure": {
    "visa_type": "string",
    "visa_code": "string", 
    "objective": "object",
    "key_requirements": "object",
    "stakeholders": "array"
  },
  "eligibility_rules": {
    "applicant_requirements": "array",
    "sponsor_requirements": "array",
    "dependent_requirements": "array"
  },
  "conditions": {
    "visa_conditions": "array",
    "financial_conditions": "array",
    "health_conditions": "array"
  },
  "thresholds": {
    "currency_amounts": "array",
    "time_periods": "array",
    "age_limits": "array"
  },
  "sections": "object"
}
```

**Performance Metrics:**
- Execution time: 30-60 seconds
- LLM tokens: ~3,000-5,000
- Accuracy: 90-95% (validated against manual analysis)
- Policy sections parsed: 10-20 typically

### 2. RequirementsCapture Agent

**Purpose:** Extract and categorize business and technical requirements

**Key Responsibilities:**
- Identify functional requirements (what system must do)
- Extract data requirements (what information to collect)
- Define business rules (logic and constraints)
- Specify validation rules (how to validate data)
- Assign priorities (must/should/could have)
- Link requirements to policy references

**Input Schema:**
```json
{
  "policy_structure": "object",
  "eligibility_rules": "object", 
  "conditions": "object",
  "thresholds": "object",
  "sections": "object"
}
```

**Output Schema:**
```json
{
  "functional_requirements": [
    {
      "requirement_id": "string",
      "description": "string",
      "category": "string",
      "priority": "must_have|should_have|could_have",
      "policy_reference": "string",
      "acceptance_criteria": "array"
    }
  ],
  "data_requirements": [
    {
      "requirement_id": "string",
      "field_name": "string",
      "data_type": "text|number|date|boolean|file|currency",
      "description": "string",
      "required": "boolean",
      "validation": "string",
      "policy_reference": "string"
    }
  ],
  "business_rules": [
    {
      "rule_id": "string",
      "description": "string", 
      "rule_type": "constraint|calculation|conditional|threshold",
      "logic": "string",
      "policy_reference": "string",
      "parameters": "object"
    }
  ],
  "validation_rules": [
    {
      "validation_id": "string",
      "field": "string",
      "validation_type": "range|date|calculation|format|conditional",
      "rule": "string",
      "error_message": "string",
      "policy_reference": "string"
    }
  ]
}
```

**Performance Metrics:**
- Execution time: 45-90 seconds
- LLM tokens: ~4,000-6,000
- Output: 40-60 requirements typically
- Categories: 4 requirement types

### 3. QuestionGenerator Agent

**Purpose:** Generate application form questions with validation rules

**Key Responsibilities:**
- Create user-facing questions from requirements
- Assign appropriate input types (text, number, date, etc.)
- Define validation rules for each question
- Generate help text and examples
- Establish conditional logic (show/hide based on answers)
- Group questions into logical sections
- Link questions to policy references

**Input Schema:**
```json
{
  "functional_requirements": "array",
  "data_requirements": "array",
  "business_rules": "array", 
  "validation_rules": "array"
}
```

**Output Schema:**
```json
{
  "application_questions": [
    {
      "question_id": "string",
      "section": "string",
      "question_text": "string",
      "input_type": "text|number|boolean|date|select|multiselect|file|currency",
      "required": "boolean",
      "validation": {
        "rules": "array",
        "error_messages": "object"
      },
      "conditional_logic": {
        "show_if": "array",
        "triggers": "array"
      },
      "help_text": "string",
      "policy_reference": "string",
      "options": "array (for select types)"
    }
  ],
  "conditional_logic": "object",
  "question_count": "number"
}
```

**Question Sections:**
- Applicant Details
- Sponsorship
- Dependent Children
- Financial Requirements
- Health & Character

**Performance Metrics:**
- Execution time: 60-120 seconds
- LLM tokens: ~5,000-8,000
- Output: 30-50 questions typically
- Sections: 5-7 logical groupings

### 4. ValidationAgent

**Purpose:** Validate requirements and questions against policy

**Key Responsibilities:**
- Validate requirement structure and completeness
- Validate question structure and logic
- Check policy coverage (are all sections covered?)
- Verify traceability (policy → requirements → questions)
- Identify gaps and inconsistencies
- Generate quality scores
- Provide actionable recommendations

**Input Schema:**
```json
{
  "policy_structure": "object",
  "sections": "object",
  "functional_requirements": "array",
  "data_requirements": "array", 
  "business_rules": "array",
  "validation_rules": "array",
  "application_questions": "array"
}
```

**Output Schema:**
```json
{
  "validation_report": {
    "overall_score": "number (0-100)",
    "requirement_validation": {
      "total_requirements": "number",
      "valid_requirements": "number", 
      "invalid_requirements": "number",
      "validation_rate": "number",
      "errors": "array"
    },
    "question_validation": {
      "total_questions": "number",
      "valid_questions": "number",
      "invalid_questions": "number", 
      "validation_rate": "number",
      "errors": "array"
    },
    "consistency_check": "object"
  },
  "gap_analysis": {
    "missing_requirements": "array",
    "missing_questions": "array",
    "uncovered_policy_sections": "array"
  },
  "coverage_analysis": {
    "requirement_coverage": "object",
    "question_requirement_mapping": "object"
  },
  "recommendations": "array"
}
```

**Validation Checks:**
- ✅ Requirement structure validation
- ✅ Question structure validation  
- ✅ Policy coverage analysis
- ✅ Traceability verification
- ✅ Gap identification
- ✅ Consistency checking

**Performance Metrics:**
- Execution time: 30-60 seconds
- LLM tokens: ~2,000-4,000
- Validation score: 85-95% typical
- Coverage: 95%+ policy sections

### 5. ConsolidationAgent

**Purpose:** Synthesize all outputs into cohesive specification

**Key Responsibilities:**
- Create consolidated specification document
- Generate implementation guide
- Build traceability matrix
- Calculate summary statistics
- Format outputs for different audiences
- Generate diagrams and visualizations

**Input Schema:**
```json
{
  "policy_structure": "object",
  "functional_requirements": "array",
  "data_requirements": "array",
  "business_rules": "array", 
  "validation_rules": "array",
  "application_questions": "array",
  "validation_report": "object",
  "gap_analysis": "object",
  "recommendations": "array"
}
```

**Output Schema:**
```json
{
  "consolidated_spec": {
    "executive_summary": "string",
    "system_overview": "object",
    "functional_requirements": "object",
    "data_requirements": "object",
    "business_rules": "object",
    "application_flow": "object",
    "validation_rules": "object",
    "ui_requirements": "object",
    "integration_requirements": "object",
    "quality_attributes": "object"
  },
  "implementation_guide": {
    "architecture_overview": "object",
    "implementation_phases": "object", 
    "database_schema": "object",
    "api_endpoints": "object",
    "security_considerations": "object",
    "testing_strategy": "object",
    "deployment_considerations": "object"
  },
  "traceability_matrix": "array",
  "summary_statistics": "object"
}
```

**Performance Metrics:**
- Execution time: 30-45 seconds
- Output: Complete specification document
- Traceability: 100% policy-to-question mapping
- Statistics: Comprehensive metrics dashboard

## Technical Implementation

### Base Agent Class

All agents inherit from `BaseAgent` which provides:

```python
class BaseAgent(ABC):
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.llm = self._initialize_llm()
        self.execution_history = []
    
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def _initialize_llm(self) -> ChatOpenAI:
        # Initialize LLM with config
        pass
    
    def _log_execution(self, inputs, outputs, duration, success, error=None):
        # Log execution details
        pass
```

### LLM Integration

**Supported Providers:**
- OpenAI (GPT-4, GPT-3.5-turbo)
- Anthropic (Claude-3, Claude-2)
- Local models (via Ollama)

**Configuration:**
```yaml
llm:
  provider: openai
  model: gpt-4-turbo-preview
  temperature: 0.1
  max_tokens: 4000
```

### Error Handling

**Retry Logic:**
- Automatic retry on API failures (3 attempts)
- Exponential backoff
- Graceful degradation

**Validation:**
- JSON schema validation
- Output format verification
- Policy reference validation

### Monitoring & Observability

**Metrics Tracked:**
- Execution time per agent
- Token usage
- Success/failure rates
- Quality scores
- Coverage percentages

**Logging:**
- Structured logging (JSON)
- Execution traces
- Error details
- Performance metrics

## Workflow Orchestration

The `WorkflowOrchestrator` manages agent execution:

```python
class WorkflowOrchestrator:
    def __init__(self, config_dir=None):
        self.agents = self._initialize_agents()
        self.workflow_config = self._load_workflow_config()
    
    def run_workflow(self, policy_document_path):
        # Execute stages in sequence
        # Handle dependencies
        # Manage state
        # Save outputs
        pass
```

**Execution Stages:**
1. **policy_analysis** - PolicyEvaluator
2. **requirements_capture** - RequirementsCapture  
3. **question_generation** - QuestionGenerator
4. **validation** - ValidationAgent
5. **consolidation** - ConsolidationAgent

**State Management:**
- Shared state between agents
- Intermediate result caching
- Error recovery
- Progress tracking

## Configuration Management

**Agent Configuration:**
```yaml
agents:
  policy_evaluator:
    name: "Policy Evaluator"
    temperature: 0.1
    max_retries: 3
  
  requirements_capture:
    name: "Requirements Capture" 
    temperature: 0.2
    max_retries: 3
```

**Workflow Configuration:**
```yaml
workflow:
  stages:
    - name: "policy_analysis"
      agents: ["policy_evaluator"]
      parallel: false
      outputs: ["policy_structure", "eligibility_rules"]
```

## Testing Strategy

**Unit Tests:**
- Individual agent testing
- Mock LLM responses
- Input/output validation
- Error handling

**Integration Tests:**
- End-to-end workflow
- Agent communication
- State management
- Performance benchmarks

**Test Coverage:**
- Target: 80%+ code coverage
- Critical paths: 100% coverage
- Error scenarios: Comprehensive

## Performance Optimization

**Caching:**
- LLM response caching
- Intermediate result caching
- Policy parsing cache

**Parallel Processing:**
- Independent agent execution
- Batch processing
- Async operations

**Resource Management:**
- Memory optimization
- Token usage monitoring
- Rate limit handling

## Security Considerations

**Data Privacy:**
- No data persistence in LLM providers
- Local processing options
- Encryption at rest and in transit

**Access Control:**
- API key management
- Role-based access
- Audit logging

**Input Validation:**
- Sanitize policy documents
- Validate file types
- Size limits

## Deployment Architecture

**Components:**
- Agent runtime
- Workflow orchestrator
- Web UI (Streamlit)
- Configuration management
- Monitoring & logging

**Infrastructure:**
- Container-based deployment
- Horizontal scaling
- Load balancing
- Health checks

**Dependencies:**
- Python 3.9+
- LangChain framework
- LLM provider APIs
- Database (optional)
- Message queue (optional)

## Extensibility

**Adding New Agents:**
1. Inherit from `BaseAgent`
2. Implement `execute()` method
3. Add to agent configuration
4. Update workflow configuration
5. Add tests

**Custom Output Formats:**
- Implement custom formatters
- Add export options
- Configure templates

**Integration Points:**
- REST API endpoints
- Webhook notifications
- Database connectors
- File system integration
