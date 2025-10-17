# Setup Guide - Visa Requirements Agent Demo

## Quick Start (5 minutes)

### Prerequisites
- Python 3.9 or higher
- Git
- OpenAI API key (or Anthropic Claude API key)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd visa-requirements-agent-demo
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file and add your API key:
   # OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the demo**
   ```bash
   # Option 1: Streamlit UI
   streamlit run src/ui/streamlit_app.py
   
   # Option 2: Command line
   python run_demo.py
   
   # Option 3: Jupyter notebook
   jupyter notebook notebooks/demo_walkthrough.ipynb
   ```

## Detailed Setup Instructions

### System Requirements

**Minimum Requirements:**
- Python 3.9+
- 4GB RAM
- 2GB free disk space
- Internet connection for LLM API calls

**Recommended:**
- Python 3.11+
- 8GB RAM
- 5GB free disk space
- Fast internet connection

### Step-by-Step Installation

#### 1. Environment Setup

**Check Python version:**
```bash
python --version
# Should show Python 3.9.0 or higher
```

**Install Python if needed:**
- **macOS:** `brew install python@3.11`
- **Ubuntu:** `sudo apt update && sudo apt install python3.11`
- **Windows:** Download from [python.org](https://python.org)

#### 2. Project Setup

**Clone repository:**
```bash
git clone https://github.com/your-org/visa-requirements-agent-demo.git
cd visa-requirements-agent-demo
```

**Verify project structure:**
```
visa-requirements-agent-demo/
├── README.md
├── requirements.txt
├── .env.example
├── config/
├── data/
├── src/
├── notebooks/
└── tests/
```

#### 3. Virtual Environment

**Create virtual environment:**
```bash
# Using venv (recommended)
python -m venv venv

# Or using conda
conda create -n visa-agent python=3.11
```

**Activate virtual environment:**
```bash
# venv on macOS/Linux
source venv/bin/activate

# venv on Windows
venv\Scripts\activate

# conda
conda activate visa-agent
```

**Verify activation:**
```bash
which python  # Should point to venv/bin/python
pip --version  # Should show pip from virtual environment
```

#### 4. Dependencies Installation

**Install core dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import langchain; print('LangChain installed successfully')"
python -c "import streamlit; print('Streamlit installed successfully')"
```

**Optional: Install development dependencies:**
```bash
pip install -r requirements-dev.txt  # If available
```

#### 5. Configuration

**Create environment file:**
```bash
cp .env.example .env
```

**Edit .env file:**
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL=gpt-4-turbo-preview
LOG_LEVEL=INFO
OUTPUT_DIR=data/output
```

**Get API keys:**
- **OpenAI:** Visit [platform.openai.com](https://platform.openai.com/api-keys)
- **Anthropic:** Visit [console.anthropic.com](https://console.anthropic.com/)

#### 6. Verification

**Test configuration:**
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API Key configured:', bool(os.getenv('OPENAI_API_KEY')))
"
```

**Run basic test:**
```bash
python -m pytest tests/test_agents.py::TestPolicyEvaluatorAgent::test_agent_initialization -v
```

## Running the Demo

### Option 1: Streamlit Web Interface (Recommended)

**Start the application:**
```bash
streamlit run src/ui/streamlit_app.py
```

**Access the interface:**
- Open browser to `http://localhost:8501`
- Upload policy document or use sample
- Click "Run Complete Workflow"
- View results in interactive tabs

### Option 2: Command Line Interface

**Run complete workflow:**
```bash
python run_demo.py
```

**Run individual agents:**
```bash
python -c "
from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator
orchestrator = WorkflowOrchestrator()
results = orchestrator.run_workflow('data/input/parent_boost_policy.txt')
print(f'Status: {results[\"status\"]}')
"
```

### Option 3: Jupyter Notebook

**Start Jupyter:**
```bash
jupyter notebook
```

**Open demo notebook:**
- Navigate to `notebooks/demo_walkthrough.ipynb`
- Run cells step by step
- Explore interactive results

### Option 4: Python API

**Basic usage:**
```python
from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator

# Initialize orchestrator
orchestrator = WorkflowOrchestrator()

# Run workflow
results = orchestrator.run_workflow('path/to/policy.txt')

# Access results
policy_structure = results['outputs']['policy_structure']
requirements = results['outputs']['functional_requirements']
questions = results['outputs']['application_questions']
```

## Troubleshooting

### Common Issues

#### 1. API Key Issues

**Problem:** `ValueError: OPENAI_API_KEY not found`
**Solution:**
```bash
# Check if .env file exists
ls -la .env

# Verify API key is set
cat .env | grep OPENAI_API_KEY

# Test API key
python -c "
import openai
import os
from dotenv import load_dotenv
load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print('API key is valid')
"
```

#### 2. Import Errors

**Problem:** `ModuleNotFoundError: No module named 'langchain'`
**Solution:**
```bash
# Verify virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt

# Check specific package
pip show langchain
```

#### 3. Permission Errors

**Problem:** `PermissionError: [Errno 13] Permission denied`
**Solution:**
```bash
# Check file permissions
ls -la data/

# Create output directory
mkdir -p data/output

# Fix permissions (macOS/Linux)
chmod 755 data/output
```

#### 4. Port Already in Use

**Problem:** `OSError: [Errno 48] Address already in use`
**Solution:**
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run src/ui/streamlit_app.py --server.port 8502
```

#### 5. Memory Issues

**Problem:** `MemoryError` or slow performance
**Solution:**
```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Reduce concurrent processing
# Edit config/agent_config.yaml:
# max_tokens: 2000  # Reduce from 4000
```

### Debugging Tips

#### Enable Debug Logging

**Edit .env file:**
```bash
LOG_LEVEL=DEBUG
```

**View logs:**
```bash
# In Python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or check log files
tail -f logs/application.log  # If logging to file
```

#### Test Individual Components

**Test document parser:**
```python
from src.utils.document_parser import DocumentParser
text = DocumentParser.load_document('data/input/parent_boost_policy.txt')
sections = DocumentParser.extract_sections(text)
print(f"Found {len(sections)} sections")
```

**Test single agent:**
```python
from src.agents import PolicyEvaluatorAgent
import yaml

# Load config
with open('config/agent_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize agent
agent = PolicyEvaluatorAgent('PolicyEvaluator', config['llm'])

# Test execution
result = agent.execute({
    'policy_document_path': 'data/input/parent_boost_policy.txt'
})
print(f"Agent completed: {list(result.keys())}")
```

#### Performance Profiling

**Time execution:**
```python
import time
start = time.time()
# Your code here
print(f"Execution time: {time.time() - start:.2f}s")
```

**Memory profiling:**
```bash
pip install memory-profiler
python -m memory_profiler run_demo.py
```

## Advanced Configuration

### Custom LLM Providers

**Use Anthropic Claude:**
```bash
# In .env file
ANTHROPIC_API_KEY=your_anthropic_key
```

```python
# In agent_config.yaml
llm:
  provider: anthropic
  model: claude-3-sonnet-20240229
  temperature: 0.1
```

**Use local models (Ollama):**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama2

# Configure
# In agent_config.yaml
llm:
  provider: ollama
  model: llama2
  base_url: http://localhost:11434
```

### Custom Configuration

**Agent settings:**
```yaml
# config/agent_config.yaml
agents:
  policy_evaluator:
    temperature: 0.05  # More deterministic
    max_retries: 5     # More resilient
    timeout: 120       # Longer timeout
```

**Workflow settings:**
```yaml
# config/workflow_config.yaml
execution:
  timeout_per_stage: 600  # 10 minutes
  continue_on_error: true  # Don't stop on errors
  parallel_execution: false  # Sequential only
```

### Docker Deployment

**Build image:**
```bash
docker build -t visa-requirements-agent .
```

**Run container:**
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  visa-requirements-agent
```

**Docker Compose:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
```

## Testing

### Run Test Suite

**All tests:**
```bash
pytest
```

**Specific test file:**
```bash
pytest tests/test_agents.py -v
```

**With coverage:**
```bash
pytest --cov=src tests/
```

### Manual Testing

**Test workflow:**
```bash
python run_demo.py
```

**Test UI:**
```bash
streamlit run src/ui/streamlit_app.py
# Navigate to localhost:8501
# Upload sample document
# Run workflow
```

**Test notebook:**
```bash
jupyter notebook notebooks/demo_walkthrough.ipynb
# Run all cells
```

## Getting Help

### Documentation
- **README.md** - Project overview
- **DEMO_GUIDE.md** - Presentation guide
- **PROJECT_PLAN.md** - Implementation plan
- **AGENT_ARCHITECTURE.md** - Technical details

### Support Channels
- **GitHub Issues** - Bug reports and feature requests
- **Documentation** - In-code documentation and docstrings
- **Community** - Stack Overflow with tag `visa-requirements-agent`

### Common Resources
- **LangChain Docs:** https://docs.langchain.com
- **Streamlit Docs:** https://docs.streamlit.io
- **OpenAI API:** https://platform.openai.com/docs
- **Python Virtual Environments:** https://docs.python.org/3/tutorial/venv.html

## Next Steps

After successful setup:

1. **Explore the demo** with sample policy document
2. **Try your own documents** by uploading them
3. **Review the code** to understand the architecture
4. **Customize agents** for your specific needs
5. **Integrate with your systems** using the API
6. **Deploy to production** following the deployment guide

## Maintenance

### Regular Updates

**Update dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

**Update configuration:**
```bash
# Review and update config files
# Check for new features in releases
```

**Clean up:**
```bash
# Remove old output files
rm -rf data/output/*

# Clean Python cache
find . -type d -name __pycache__ -delete
```

### Monitoring

**Check system health:**
```bash
python -c "
from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator
orchestrator = WorkflowOrchestrator()
print('System initialized successfully')
"
```

**Monitor API usage:**
- Check OpenAI usage dashboard
- Monitor costs and quotas
- Set up billing alerts
