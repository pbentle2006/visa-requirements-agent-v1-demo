import streamlit as st
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.enhanced_document_parser import EnhancedDocumentParser, get_available_formats


def show_enhanced_file_upload(demo_mode: bool = False) -> Optional[Dict[str, Any]]:
    """
    Enhanced file upload component with multi-format support.
    
    Args:
        demo_mode: Whether in demo mode or not
        
    Returns:
        Dictionary with document data or None
    """
    
    st.header("📄 Policy Document")
    
    if demo_mode:
        return _show_demo_mode_selection()
    else:
        return _show_live_mode_upload()


def _show_demo_mode_selection() -> Dict[str, Any]:
    """Show demo mode policy selection."""
    policy_options = {
        "Parent Boost Visitor Visa (Original)": "parent_boost_policy.txt",
        "Tourist Visa (Synthetic)": "tourist_visa.txt", 
        "Skilled Worker Visa (Synthetic)": "skilled_worker_visa.txt",
        "Student Visa (Synthetic)": "student_visa.txt",
        "Family Reunion Visa (Synthetic)": "family_reunion_visa.txt"
    }
    
    selected_policy = st.selectbox("Select Policy Document", list(policy_options.keys()))
    policy_filename = policy_options[selected_policy]
    
    # Use absolute path to ensure it works
    base_path = Path("/Users/peterbentley/CascadeProjects/visa-requirements-agent-demo")
    
    if "Synthetic" in selected_policy:
        policy_path = base_path / 'data' / 'synthetic' / policy_filename
    else:
        policy_path = base_path / 'data' / 'input' / policy_filename
    
    st.info(f"Using: {selected_policy}")
    st.info(f"Looking for file at: {policy_path}")
    st.info(f"File exists: {policy_path.exists()}")
    
    # Check if file exists
    if not policy_path.exists():
        st.error(f"Policy file not found: {policy_path}")
        # Try to list what's actually in the directory
        parent_dir = policy_path.parent
        if parent_dir.exists():
            files = list(parent_dir.glob("*"))
            st.write(f"Files in {parent_dir}: {[f.name for f in files]}")
        else:
            st.error(f"Directory doesn't exist: {parent_dir}")
        return {
            'path': str(policy_path),
            'content': f"Sample policy content for {selected_policy} (file not found)",
            'original_name': selected_policy,
            'filename': policy_filename
        }
    
    # Simple direct file reading - like the working iteration
    try:
        with open(policy_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        st.success(f"✅ Loaded {len(content)} characters from {policy_filename}")
        
        # Return simple structure that main app expects
        return {
            'content': content,  # Direct content - no nesting
            'original_name': selected_policy,
            'filename': policy_filename,
            'path': str(policy_path)
        }
    except Exception as e:
        st.error(f"Failed to load document: {e}")
        return None


def _show_live_mode_upload() -> Optional[Dict[str, Any]]:
    """Show live mode file upload with enhanced format support."""
    
    # Get available formats
    available_formats = get_available_formats()
    
    # Display format support status
    with st.expander("📋 Supported Document Formats", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Always Supported:**")
            st.write("✅ Text files (.txt)")
            st.write("✅ Markdown (.md)")
            
        with col2:
            st.write("**Additional Formats:**")
            st.write(f"{'✅' if available_formats['pdf'] else '❌'} PDF documents (.pdf)")
            st.write(f"{'✅' if available_formats['docx'] else '❌'} Word documents (.docx)")
            st.write(f"{'✅' if available_formats['excel'] else '❌'} Excel files (.xlsx)")
        
        if not all([available_formats['pdf'], available_formats['docx']]):
            st.info("💡 Install additional packages for full format support: `pip install PyPDF2 pdfplumber python-docx pandas`")
    
    # File upload options
    upload_option = st.radio(
        "Choose input method:",
        ["Use sample document", "Upload your own document"],
        horizontal=True
    )
    
    if upload_option == "Use sample document":
        return _handle_sample_document()
    else:
        return _handle_file_upload(available_formats)


def _handle_sample_document() -> Dict[str, Any]:
    """Handle sample document selection."""
    project_root = Path(__file__).parent.parent.parent
    policy_path = project_root / 'data' / 'input' / 'parent_boost_policy.txt'
    
    st.info(f"Using sample: {policy_path.name}")
    
    try:
        parser = EnhancedDocumentParser()
        document_data = parser.load_document(str(policy_path))
        return {
            'path': str(policy_path),
            'data': document_data,
            'structured': parser.extract_structured_content(document_data)
        }
    except Exception as e:
        st.error(f"Error loading sample document: {e}")
        return None


def _handle_file_upload(available_formats: Dict[str, bool]) -> Optional[Dict[str, Any]]:
    """Handle file upload with format detection."""
    
    # Determine supported file types for uploader
    supported_types = ['txt', 'md']
    if available_formats['pdf']:
        supported_types.append('pdf')
    if available_formats['docx']:
        supported_types.extend(['docx', 'doc'])
    if available_formats['excel']:
        supported_types.extend(['xlsx', 'xls'])
    
    uploaded_file = st.file_uploader(
        "Upload Policy Document",
        type=supported_types,
        help=f"Supported formats: {', '.join(supported_types)}"
    )
    
    if uploaded_file is not None:
        return _process_uploaded_file(uploaded_file)
    
    return None


def _process_uploaded_file(uploaded_file) -> Optional[Dict[str, Any]]:
    """Process the uploaded file with enhanced parsing."""
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
        
        # Parse document
        parser = EnhancedDocumentParser()
        document_data = parser.load_document(tmp_file_path)
        structured_data = parser.extract_structured_content(document_data)
        
        # Display upload success and document info
        st.success(f"✅ Successfully uploaded: {uploaded_file.name}")
        
        # Show document metadata
        with st.expander("📊 Document Information", expanded=False):
            metadata = document_data['metadata']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Format", metadata.get('format', 'Unknown'))
            with col2:
                st.metric("Size", f"{metadata.get('size', 0):,} chars")
            with col3:
                if 'pages' in metadata:
                    st.metric("Pages", metadata['pages'])
                elif 'sheets' in metadata:
                    st.metric("Sheets", len(metadata['sheets']))
                else:
                    st.metric("Type", document_data['format'].title())
            
            # Show extraction results
            if structured_data:
                st.write("**Extracted Content:**")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Sections", len(structured_data.get('sections', {})))
                with col_b:
                    st.metric("Requirements", len(structured_data.get('requirements', [])))
                with col_c:
                    st.metric("Conditions", len(structured_data.get('conditions', [])))
        
        # Save to project directory for workflow processing
        project_root = Path(__file__).parent.parent.parent
        saved_path = project_root / 'data' / 'input' / uploaded_file.name
        saved_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy to permanent location
        import shutil
        shutil.copy2(tmp_file_path, saved_path)
        
        # Clean up temp file
        Path(tmp_file_path).unlink()
        
        return {
            'path': str(saved_path),
            'data': document_data,
            'structured': structured_data,
            'original_name': uploaded_file.name
        }
        
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
        return None


def show_document_preview(document_info: Dict[str, Any]) -> None:
    """Show a preview of the loaded document."""
    
    if not document_info:
        return
    
    structured = document_info.get('structured', {})
    
    with st.expander("👀 Document Preview", expanded=False):
        
        # Show sections if available
        sections = structured.get('sections', {})
        if sections:
            st.write("**📋 Document Sections:**")
            for section_code, section_data in list(sections.items())[:5]:  # Show first 5 sections
                st.write(f"- **{section_code}**: {section_data.get('title', 'No title')}")
            
            if len(sections) > 5:
                st.write(f"... and {len(sections) - 5} more sections")
        
        # Show sample requirements
        requirements = structured.get('requirements', [])
        if requirements:
            st.write("**📝 Sample Requirements:**")
            for req in requirements[:3]:  # Show first 3 requirements
                st.write(f"- {req.get('requirement', 'No content')[:100]}...")
        
        # Show thresholds
        thresholds = structured.get('thresholds', {})
        if thresholds:
            st.write("**🎯 Extracted Thresholds:**")
            if thresholds.get('currency_amounts'):
                amounts = thresholds['currency_amounts'][:3]  # Show first 3
                st.write(f"- Currency amounts: {', '.join([f'${a:,}' for a in amounts])}")
            if thresholds.get('age_limits'):
                ages = thresholds['age_limits'][:3]
                st.write(f"- Age limits: {', '.join(map(str, ages))}")


# Utility function for easy integration
def get_document_content(document_info: Dict[str, Any]) -> str:
    """Extract plain text content from document info for workflow processing."""
    if not document_info:
        return ""
    
    return document_info.get('data', {}).get('content', '')


def get_document_path(document_info: Dict[str, Any]) -> str:
    """Get the file path from document info."""
    if not document_info:
        return ""
    
    return document_info.get('path', '')
