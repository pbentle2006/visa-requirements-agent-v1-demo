#!/usr/bin/env python3
"""
FastAPI alternative to Streamlit for testing the hybrid approach
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import os
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator
from src.utils.document_parser import DocumentParser

app = FastAPI(title="Visa Requirements Agent - FastAPI Demo")

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visa Requirements Agent - FastAPI Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
            .result { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
            .success { background: #d4edda; border: 1px solid #c3e6cb; }
            .error { background: #f8d7da; border: 1px solid #f5c6cb; }
        </style>
    </head>
    <body>
        <h1>🛂 Visa Requirements Agent - FastAPI Demo</h1>
        <p>Upload a visa policy document to test the hybrid approach</p>
        
        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="upload-area">
                <input type="file" name="file" accept=".docx,.pdf,.txt" required>
                <br><br>
                <button type="submit">🚀 Process Document</button>
            </div>
        </form>
        
        <div id="results"></div>
    </body>
    </html>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Process uploaded document with hybrid approach"""
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Parse document
        parser = DocumentParser()
        policy_content = parser.parse_document(tmp_path)
        
        # HYBRID APPROACH - Detect visa type
        detected_visa_type = None
        detected_visa_code = None
        
        content_upper = policy_content.upper()
        detection_results = {
            "PARENT BOOST": "PARENT BOOST" in content_upper,
            "V4": "V4" in content_upper,
            "PARENT": "PARENT" in content_upper,
            "BOOST": "BOOST" in content_upper,
            "VISITOR": "VISITOR" in content_upper,
            "SKILLED MIGRANT": "SKILLED MIGRANT" in content_upper,
            "WORKING HOLIDAY": "WORKING HOLIDAY" in content_upper
        }
        
        if any(keyword in content_upper for keyword in ['PARENT BOOST VISITOR VISA', 'PARENT BOOST', 'V4']):
            detected_visa_type = "Parent Boost Visitor Visa"
            detected_visa_code = "V4"
        elif any(keyword in content_upper for keyword in ['SKILLED MIGRANT', 'SR1', 'SR3', 'SR4', 'SR5']):
            detected_visa_type = "Skilled Migrant Residence Visa"
            detected_visa_code = "SR1"
        elif any(keyword in content_upper for keyword in ['WORKING HOLIDAY', 'YOUTH', 'TEMPORARY WORK', 'WHV']):
            detected_visa_type = "Working Holiday Visa"
            detected_visa_code = "WHV"
        
        # Run workflow
        orchestrator = WorkflowOrchestrator()
        results = orchestrator.run_workflow(
            tmp_path,
            policy_content,
            detected_visa_type=detected_visa_type,
            detected_visa_code=detected_visa_code,
            force_visa_type=bool(detected_visa_type)
        )
        
        # Extract policy structure
        policy_structure = results['outputs'].get('policy_structure', {})
        
        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "document_length": len(policy_content),
            "detection_results": detection_results,
            "detected_visa_type": detected_visa_type,
            "detected_visa_code": detected_visa_code,
            "workflow_status": results['status'],
            "workflow_duration": results['duration_seconds'],
            "stages_completed": f"{len([s for s in results['stages'] if s['status'] == 'success'])}/{len(results['stages'])}",
            "final_visa_type": policy_structure.get('visa_type'),
            "final_visa_code": policy_structure.get('visa_code'),
            "match_success": policy_structure.get('visa_type') == detected_visa_type if detected_visa_type else False
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e),
            "filename": file.filename
        }, status_code=500)
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    print("📱 Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
