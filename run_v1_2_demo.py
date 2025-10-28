#!/usr/bin/env python3
"""
Launch script for Visa Requirements Agent V1.2 - Human-in-the-Loop Demo
Runs on port 8503 to avoid conflicts with V1 (8501) and V2 (8502)
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the V1.2 Human-in-the-Loop Demo."""
    
    print("🚀 Starting Visa Requirements Agent - Version 1.2 (Human-in-the-Loop Demo)")
    print("📡 Port: 8503")
    print("👥 Mode: Human Validation + Customer Form Generation")
    print("🔗 URL: http://localhost:8503")
    print("-" * 50)
    
    # Set environment variables for V1.2 mode
    os.environ["VISA_AGENT_VERSION"] = "v1.2_human_loop"
    os.environ["VISA_AGENT_FORCE_LLM"] = "false"  # Use fallback mode for demo
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Change to project directory
    os.chdir(project_root)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/ui/streamlit_app.py",
            "--server.port", "8503",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 V1.2 Demo stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting V1.2 Demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
