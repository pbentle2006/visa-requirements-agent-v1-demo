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
            st.write("**Conditionally Supported:**")
            for format_name, available in available_formats.items():
                icon = "✅" if available else "❌"
                st.write(f"{icon} {format_name}")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a policy document",
        type=['txt', 'md', 'pdf', 'docx', 'doc', 'xlsx', 'xls'],
        help="Upload a policy document in any supported format"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Parse the document
            parser = EnhancedDocumentParser()
            document_data = parser.load_document(tmp_file_path)
            
            # Show success message
            st.success(f"✅ Successfully loaded: {uploaded_file.name}")
            
            # Show document info
            metadata = document_data.get('metadata', {})
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Format", metadata.get('format', 'Unknown'))
            with col2:
                st.metric("Size", f"{metadata.get('size', 0):,} chars")
            with col3:
                if 'pages' in metadata:
                    st.metric("Pages", metadata['pages'])
            
            return {
                'content': document_data['content'],
                'original_name': uploaded_file.name,
                'filename': uploaded_file.name,
                'path': tmp_file_path,
                'metadata': metadata
            }
            
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            return None
        finally:
            # Clean up temporary file
            try:
                Path(tmp_file_path).unlink()
            except:
                pass
    
    return None


def show_document_preview(document_info: Dict[str, Any]):
    """Show document preview and metadata."""
    if not document_info:
        return
    
    st.subheader("📄 Document Preview")
    
    # Show metadata
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {document_info.get('original_name', 'Unknown')}")
        st.write(f"**Path:** {document_info.get('path', 'Unknown')}")
    
    with col2:
        content = document_info.get('content', '')
        st.write(f"**Size:** {len(content):,} characters")
        st.write(f"**Lines:** {len(content.splitlines()):,}")
    
    # Show content preview
    if content:
        preview_lines = content.split('\n')[:10]
        preview_text = '\n'.join(preview_lines)
        if len(content.split('\n')) > 10:
            preview_text += '\n... (truncated)'
        
        st.text_area("Content Preview", preview_text, height=200, disabled=True)


def get_document_content(document_info: Dict[str, Any]) -> str:
    """Extract document content from document info."""
    if not document_info:
        return ""
    return document_info.get('content', '')


def get_document_path(document_info: Dict[str, Any]) -> str:
    """Extract document path from document info."""
    if not document_info:
        return ""
    return document_info.get('path', '')
