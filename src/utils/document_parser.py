import re
from typing import Dict, List, Any
from pathlib import Path


class DocumentParser:
    """Utility class for parsing policy documents."""
    
    @staticmethod
    def load_document(file_path: str) -> str:
        """Load a document from file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def extract_sections(document: str) -> Dict[str, str]:
        """
        Extract sections from a policy document.
        
        Args:
            document: Full document text
            
        Returns:
            Dictionary mapping section codes to content
        """
        sections = {}
        
        # Pattern to match section headers like "V4.1 OBJECTIVE"
        pattern = r'(V\d+\.\d+(?:\.\d+)?)\s+([A-Z\s]+)\n\n(.*?)(?=\n\nV\d+\.\d+|$)'
        
        matches = re.finditer(pattern, document, re.DOTALL)
        
        for match in matches:
            section_code = match.group(1)
            section_title = match.group(2).strip()
            section_content = match.group(3).strip()
            
            sections[section_code] = {
                'title': section_title,
                'content': section_content
            }
        
        return sections
    
    @staticmethod
    def extract_requirements(section_content: str) -> List[str]:
        """
        Extract individual requirements from a section.
        
        Args:
            section_content: Content of a policy section
            
        Returns:
            List of requirement strings
        """
        requirements = []
        
        # Pattern to match numbered/lettered requirements
        pattern = r'\(([a-z]+|[ivx]+)\)\s+(.*?)(?=\n\([a-z]+|[ivx]+\)|$)'
        
        matches = re.finditer(pattern, section_content, re.DOTALL)
        
        for match in matches:
            requirement = match.group(2).strip()
            requirements.append(requirement)
        
        return requirements
    
    @staticmethod
    def extract_thresholds(document: str) -> Dict[str, Any]:
        """
        Extract numerical thresholds and limits from document.
        
        Args:
            document: Full document text
            
        Returns:
            Dictionary of extracted thresholds
        """
        thresholds = {}
        
        # Extract currency amounts
        currency_pattern = r'NZD\s*\$\s*([\d,]+)'
        amounts = re.findall(currency_pattern, document)
        
        # Extract time periods
        time_pattern = r'(\d+)\s+(months?|years?|days?)'
        periods = re.findall(time_pattern, document)
        
        # Extract age limits
        age_pattern = r'(?:under|over|age)\s+(\d+)'
        ages = re.findall(age_pattern, document, re.IGNORECASE)
        
        thresholds['currency_amounts'] = [int(a.replace(',', '')) for a in amounts]
        thresholds['time_periods'] = periods
        thresholds['age_limits'] = [int(a) for a in ages]
        
        return thresholds
    
    @staticmethod
    def extract_conditions(document: str) -> List[Dict[str, str]]:
        """
        Extract conditional statements from document.
        
        Args:
            document: Full document text
            
        Returns:
            List of conditions with their context
        """
        conditions = []
        
        # Pattern for "must" statements
        must_pattern = r'(.*?must\s+.*?)(?:\.|;|\n)'
        must_matches = re.finditer(must_pattern, document, re.IGNORECASE)
        
        for match in must_matches:
            conditions.append({
                'type': 'requirement',
                'statement': match.group(1).strip()
            })
        
        # Pattern for "may" statements
        may_pattern = r'(.*?may\s+.*?)(?:\.|;|\n)'
        may_matches = re.finditer(may_pattern, document, re.IGNORECASE)
        
        for match in may_matches:
            conditions.append({
                'type': 'optional',
                'statement': match.group(1).strip()
            })
        
        return conditions
