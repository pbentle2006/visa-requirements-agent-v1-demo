from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import os
import logging
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents in the visa requirements system."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            config: Configuration dictionary containing LLM settings
        """
        self.name = name
        self.config = config
        self.llm = self._initialize_llm()
        self.execution_history: List[Dict[str, Any]] = []
        
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the LLM based on configuration."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        model = self.config.get('model', 'gpt-4-turbo-preview')
        temperature = self.config.get('temperature', 0.1)
        max_tokens = self.config.get('max_tokens', 4000)
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key
        )
    
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary task.
        
        Args:
            inputs: Dictionary of input data
            
        Returns:
            Dictionary of output data
        """
        pass
    
    def _create_prompt(self, template: str, variables: Dict[str, Any]) -> ChatPromptTemplate:
        """Create a chat prompt template."""
        return ChatPromptTemplate.from_template(template)
    
    def _log_execution(self, inputs: Dict[str, Any], outputs: Dict[str, Any], 
                      duration: float, success: bool, error: Optional[str] = None):
        """Log execution details."""
        execution_record = {
            'timestamp': datetime.now().isoformat(),
            'agent': self.name,
            'inputs': inputs,
            'outputs': outputs if success else None,
            'duration_seconds': duration,
            'success': success,
            'error': error
        }
        self.execution_history.append(execution_record)
        
        if success:
            logger.info(f"{self.name} executed successfully in {duration:.2f}s")
        else:
            logger.error(f"{self.name} failed: {error}")
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history for this agent."""
        return self.execution_history
    
    def _extract_json_from_response(self, response: str, max_retries: int = 3) -> Dict[str, Any]:
        """Extract JSON from LLM response with retry logic and robust error handling."""
        import json
        import re
        
        # Clean the response
        response = response.strip()
        
        # Try multiple extraction strategies
        extraction_strategies = [
            self._extract_from_markdown_blocks,
            self._extract_from_json_objects,
            self._extract_from_arrays,
            self._extract_with_aggressive_cleaning
        ]
        
        for strategy in extraction_strategies:
            try:
                result = strategy(response)
                if result is not None:
                    return result
            except Exception as e:
                continue
        
        # If all strategies fail, try to extract key information from the raw response
        logger.warning(f"Failed to extract JSON from response, attempting text extraction. Response: {response[:200]}...")
        
        # Try to extract key information from the text response
        extracted_info = self._extract_info_from_text(response)
        if extracted_info:
            return extracted_info
            
        return self._get_fallback_response()
    
    def _extract_info_from_text(self, response: str) -> Dict[str, Any]:
        """Extract key information from text response when JSON parsing fails."""
        import re
        
        extracted = {}
        
        # Try to extract visa type with multiple patterns
        visa_type_patterns = [
            r'"?visa_type"?\s*:\s*"([^"]+)"',
            r'"?Policy"?\s*:\s*"([^"]+)"',
            r'visa type[:\s]+([^\n,]+)',
            r'skilled migrant[^"]*worker[^"]*visa',
            r'parent[^"]*resident[^"]*visa'
        ]
        
        for pattern in visa_type_patterns:
            visa_type_match = re.search(pattern, response, re.IGNORECASE)
            if visa_type_match:
                extracted['visa_type'] = visa_type_match.group(1) if visa_type_match.groups() else visa_type_match.group(0)
                break
        
        # Try to extract visa code
        visa_code_match = re.search(r'"?visa_code"?\s*:\s*"([^"]+)"', response, re.IGNORECASE)
        if visa_code_match:
            extracted['visa_code'] = visa_code_match.group(1)
        
        # Try to extract validation score
        score_match = re.search(r'"?Validation Score"?\s*:\s*([0-9.]+)', response, re.IGNORECASE)
        if score_match:
            extracted['validation_score'] = float(score_match.group(1))
        
        return extracted if extracted else None
    
    def _extract_from_markdown_blocks(self, response: str) -> Dict[str, Any]:
        """Extract JSON from markdown code blocks."""
        import json
        import re
        
        # Try multiple markdown patterns
        patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
            r'`(.*?)`'
        ]
        
        for pattern in patterns:
            json_match = re.search(pattern, response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
                json_str = self._fix_common_json_issues(json_str)
                try:
                    return json.loads(json_str)
                except:
                    continue
        
        return None
    
    def _extract_from_json_objects(self, response: str) -> Dict[str, Any]:
        """Extract JSON objects from response."""
        import json
        import re
        
        # Look for complete JSON objects
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0).strip()
            json_str = self._fix_common_json_issues(json_str)
            return json.loads(json_str)
        return None
    
    def _extract_from_arrays(self, response: str) -> Dict[str, Any]:
        """Extract JSON arrays from response."""
        import json
        import re
        
        # Look for JSON arrays
        json_match = re.search(r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0).strip()
            json_str = self._fix_common_json_issues(json_str)
            array_result = json.loads(json_str)
            # Wrap array in object if needed
            if isinstance(array_result, list):
                return {"items": array_result}
            return array_result
        return None
    
    def _extract_with_aggressive_cleaning(self, response: str) -> Dict[str, Any]:
        """Aggressively clean and extract JSON."""
        import json
        import re
        
        # Remove all non-JSON content
        cleaned = re.sub(r'^[^{\[]*', '', response)  # Remove prefix
        cleaned = re.sub(r'[^}\]]*$', '', cleaned)   # Remove suffix
        
        if cleaned:
            cleaned = self._fix_common_json_issues(cleaned)
            try:
                return json.loads(cleaned)
            except:
                pass
        
        return None
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Return a fallback response structure."""
        return {
            "error": "Failed to parse LLM response",
            "fallback": True,
            "items": []
        }
    
    def _fix_common_json_issues(self, json_str: str) -> str:
        """Fix common JSON formatting issues from LLM responses."""
        import re
        
        # Remove any trailing commas before closing brackets/braces
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        # Fix unescaped quotes in strings (basic attempt)
        # This is a simple fix - more complex cases might need better handling
        json_str = re.sub(r'(?<!\\)"(?=.*".*:)', r'\\"', json_str)
        
        # Remove any text before the first { or [
        first_brace = json_str.find('{')
        first_bracket = json_str.find('[')
        
        if first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket):
            json_str = json_str[first_brace:]
        elif first_bracket != -1:
            json_str = json_str[first_bracket:]
        
        # Remove any text after the last } or ]
        last_brace = json_str.rfind('}')
        last_bracket = json_str.rfind(']')
        
        if last_brace != -1 and last_brace > last_bracket:
            json_str = json_str[:last_brace + 1]
        elif last_bracket != -1:
            json_str = json_str[:last_bracket + 1]
        
        return json_str
    
    def _add_metadata(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata to output."""
        output['metadata'] = {
            'agent': self.name,
            'timestamp': datetime.now().isoformat(),
            'model': self.config.get('model', 'unknown')
        }
        return output
