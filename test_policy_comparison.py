#!/usr/bin/env python3
"""
Test script for the Enhanced Policy Comparison functionality
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.ui.enhanced_policy_comparison import show_enhanced_policy_comparison

# Page configuration
st.set_page_config(
    page_title="Policy Comparison Test",
    page_icon="📊",
    layout="wide"
)

# Main header
st.markdown("# 📊 Enhanced Policy Comparison Test")
st.markdown("Testing the side-by-side visa policy comparison functionality")

# Show the policy comparison interface
show_enhanced_policy_comparison()
