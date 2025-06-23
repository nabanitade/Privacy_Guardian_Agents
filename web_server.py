"""
Privacy Guardian Agents - FastAPI Web Server
Built with Google Cloud Agent Development Kit (ADK)

Provides a modern web interface for the multi-agent privacy enforcement system
"""

import asyncio
import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
import json
import logging

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pathlib import Path
import shutil
import tempfile

from agent_orchestrator import PrivacyGuardianOrchestrator

# Initialize FastAPI app
app = FastAPI(
    title="Privacy Guardian Agents",
    description="Multi-Agent Privacy Enforcement System built with Google Cloud ADK",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = PrivacyGuardianOrchestrator()

# Pydantic models
class ScanRequest(BaseModel):
    project_path: str = "."
    enable_ai: bool = True

class ScanResponse(BaseModel):
    correlation_id: str
    status: str
    total_violations: int
    agents_used: List[str]
    timestamp: str

class AgentStatus(BaseModel):
    agent_id: str
    agent_name: str
    status: str
    events_published: int
    events_consumed: int
    last_activity: str

# Global scan sessions
scan_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the main web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Privacy Guardian Agents - Multi-Agent Privacy Enforcement</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            
            .header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }
            
            .main-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 40px;
            }
            
            .card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: transform 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
            }
            
            .card h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.5rem;
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .upload-area:hover {
                border-color: #764ba2;
                background-color: #f8f9ff;
            }
            
            .upload-area.dragover {
                border-color: #764ba2;
                background-color: #f0f2ff;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1rem;
                transition: all 0.3s ease;
                margin: 10px 5px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .agent-status {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .agent-card {
                background: #f8f9ff;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                border-left: 4px solid #667eea;
            }
            
            .agent-card.active {
                border-left-color: #28a745;
            }
            
            .agent-card h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 8px;
            }
            
            .status-active {
                background-color: #28a745;
            }
            
            .status-inactive {
                background-color: #dc3545;
            }
            
            .results-area {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-top: 30px;
            }
            
            .violation-item {
                background: #f8f9ff;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                border-left: 4px solid #667eea;
            }
            
            .violation-item.high {
                border-left-color: #dc3545;
                background: #fff5f5;
            }
            
            .violation-item.medium {
                border-left-color: #ffc107;
                background: #fffbf0;
            }
            
            .violation-item.low {
                border-left-color: #28a745;
                background: #f0fff4;
            }
            
            .severity-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            .severity-high {
                background: #dc3545;
                color: white;
            }
            
            .severity-medium {
                background: #ffc107;
                color: #333;
            }
            
            .severity-low {
                background: #28a745;
                color: white;
            }
            
            .loading {
                text-align: center;
                padding: 40px;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .progress-bar {
                width: 100%;
                height: 20px;
                background-color: #f3f3f3;
                border-radius: 10px;
                overflow: hidden;
                margin: 20px 0;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                transition: width 0.3s ease;
            }
            
            .hidden {
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Privacy Guardian Agents</h1>
                <p>Multi-Agent Privacy Enforcement System built with Google Cloud ADK</p>
            </div>
            
            <div class="main-content">
                <div class="card">
                    <h2>📁 Upload Project Files</h2>
                    <div class="upload-area" id="uploadArea">
                        <p>Drag and drop your project files here</p>
                        <p>or</p>
                        <input type="file" id="fileInput" multiple webkitdirectory directory style="display: none;">
                        <button class="btn" onclick="document.getElementById('fileInput').click()">Choose Files</button>
                    </div>
                    
                    <div style="margin-top: 20px;">
                        <label>
                            <input type="checkbox" id="enableAI" checked> Enable AI Analysis (Gemini)
                        </label>
                    </div>
                    
                    <button class="btn" id="scanBtn" onclick="startScan()" disabled>Start Privacy Scan</button>
                </div>
                
                <div class="card">
                    <h2>🤖 Agent Status</h2>
                    <div class="agent-status" id="agentStatus">
                        <div class="agent-card active">
                            <h3>🕵️ PrivacyScanAgent</h3>
                            <span class="status-indicator status-active"></span>
                            <span>Active</span>
                        </div>
                        <div class="agent-card active">
                            <h3>🤖 GeminiAnalysisAgent</h3>
                            <span class="status-indicator status-active"></span>
                            <span>Active</span>
                        </div>
                        <div class="agent-card active">
                            <h3>🧑‍⚖️ ComplianceAgent</h3>
                            <span class="status-indicator status-active"></span>
                            <span>Active</span>
                        </div>
                        <div class="agent-card active">
                            <h3>🛠️ FixSuggestionAgent</h3>
                            <span class="status-indicator status-active"></span>
                            <span>Active</span>
                        </div>
                        <div class="agent-card active">
                            <h3>📋 ReportAgent</h3>
                            <span class="status-indicator status-active"></span>
                            <span>Active</span>
                        </div>
                    </div>
                    
                    <button class="btn" onclick="refreshAgentStatus()">Refresh Status</button>
                </div>
            </div>
            
            <div class="results-area hidden" id="resultsArea">
                <h2>📊 Scan Results</h2>
                <div class="loading" id="loadingArea">
                    <div class="spinner"></div>
                    <p>Privacy Guardian Agents are analyzing your code...</p>
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill" style="width: 0%"></div>
                    </div>
                    <p id="currentStep">Initializing agents...</p>
                </div>
                <div id="resultsContent" class="hidden"></div>
            </div>
        </div>
        
        <script>
            let uploadedFiles = [];
            let scanInProgress = false;
            
            // File upload handling
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const scanBtn = document.getElementById('scanBtn');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                handleFiles(e.dataTransfer.files);
            });
            
            fileInput.addEventListener('change', (e) => {
                handleFiles(e.target.files);
            });
            
            function handleFiles(files) {
                uploadedFiles = Array.from(files);
                scanBtn.disabled = uploadedFiles.length === 0;
                
                if (uploadedFiles.length > 0) {
                    uploadArea.innerHTML = `
                        <p>✅ ${uploadedFiles.length} files selected</p>
                        <p>Ready to scan for privacy violations</p>
                    `;
                }
            }
            
            async function startScan() {
                if (scanInProgress) return;
                
                scanInProgress = true;
                scanBtn.disabled = true;
                
                // Show results area
                document.getElementById('resultsArea').classList.remove('hidden');
                document.getElementById('loadingArea').classList.remove('hidden');
                document.getElementById('resultsContent').classList.add('hidden');
                
                // Upload files and start scan
                const formData = new FormData();
                uploadedFiles.forEach(file => {
                    formData.append('files', file);
                });
                
                const enableAI = document.getElementById('enableAI').checked;
                
                try {
                    // Upload files
                    const uploadResponse = await fetch('/upload-files', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!uploadResponse.ok) {
                        throw new Error('Failed to upload files');
                    }
                    
                    const uploadResult = await uploadResponse.json();
                    
                    // Start scan
                    const scanResponse = await fetch('/scan', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            project_path: uploadResult.project_path,
                            enable_ai: enableAI
                        })
                    });
                    
                    if (!scanResponse.ok) {
                        throw new Error('Failed to start scan');
                    }
                    
                    const scanResult = await scanResponse.json();
                    
                    // Poll for results
                    pollScanResults(scanResult.correlation_id);
                    
                } catch (error) {
                    console.error('Scan failed:', error);
                    alert('Scan failed: ' + error.message);
                    scanInProgress = false;
                    scanBtn.disabled = false;
                }
            }
            
            async function pollScanResults(correlationId) {
                const steps = [
                    'Initializing agents...',
                    'Running PrivacyScanAgent...',
                    'Running GeminiAnalysisAgent...',
                    'Running ComplianceAgent...',
                    'Running FixSuggestionAgent...',
                    'Running ReportAgent...',
                    'Generating final report...'
                ];
                
                let currentStep = 0;
                const progressFill = document.getElementById('progressFill');
                const currentStepElement = document.getElementById('currentStep');
                
                const interval = setInterval(async () => {
                    try {
                        const response = await fetch(`/scan-status/${correlationId}`);
                        const status = await response.json();
                        
                        // Update progress
                        currentStep = Math.min(Math.floor((status.progress || 0) * steps.length), steps.length - 1);
                        progressFill.style.width = `${(currentStep / (steps.length - 1)) * 100}%`;
                        currentStepElement.textContent = steps[currentStep];
                        
                        if (status.status === 'completed') {
                            clearInterval(interval);
                            displayResults(status.results);
                        } else if (status.status === 'failed') {
                            clearInterval(interval);
                            alert('Scan failed: ' + status.error);
                        }
                        
                    } catch (error) {
                        console.error('Error polling status:', error);
                    }
                }, 1000);
            }
            
            function displayResults(results) {
                document.getElementById('loadingArea').classList.add('hidden');
                document.getElementById('resultsContent').classList.remove('hidden');
                
                const resultsContent = document.getElementById('resultsContent');
                
                let html = `
                    <div style="margin-bottom: 30px;">
                        <h3>📊 Summary</h3>
                        <p><strong>Total Violations:</strong> ${results.total_violations}</p>
                        <p><strong>Risk Score:</strong> ${results.risk_score || 0}/100</p>
                        <p><strong>Files Affected:</strong> ${results.unique_files_affected || 0}</p>
                    </div>
                `;
                
                if (results.violations && results.violations.length > 0) {
                    html += '<h3>🚨 Violations Found</h3>';
                    
                    results.violations.forEach(violation => {
                        const severityClass = violation.severity.toLowerCase();
                        html += `
                            <div class="violation-item ${severityClass}">
                                <span class="severity-badge severity-${severityClass}">${violation.severity}</span>
                                <h4>${violation.file_path}:${violation.line_number}</h4>
                                <p><strong>Type:</strong> ${violation.violation_type}</p>
                                <p><strong>Description:</strong> ${violation.description}</p>
                                <p><strong>Fix:</strong> ${violation.fix_suggestion}</p>
                                <p><strong>Regulation:</strong> ${violation.regulation_reference}</p>
                            </div>
                        `;
                    });
                } else {
                    html += '<p>✅ No privacy violations found!</p>';
                }
                
                resultsContent.innerHTML = html;
                scanInProgress = false;
                scanBtn.disabled = false;
            }
            
            async function refreshAgentStatus() {
                try {
                    const response = await fetch('/agent-status');
                    const status = await response.json();
                    
                    const agentStatusDiv = document.getElementById('agentStatus');
                    agentStatusDiv.innerHTML = '';
                    
                    Object.values(status).forEach(agent => {
                        const isActive = agent.status === 'active';
                        agentStatusDiv.innerHTML += `
                            <div class="agent-card ${isActive ? 'active' : ''}">
                                <h3>${agent.agent_name}</h3>
                                <span class="status-indicator ${isActive ? 'status-active' : 'status-inactive'}"></span>
                                <span>${agent.status}</span>
                                <p>Events: ${agent.events_published} published, ${agent.events_consumed} consumed</p>
                            </div>
                        `;
                    });
                } catch (error) {
                    console.error('Failed to refresh agent status:', error);
                }
            }
            
            // Initial agent status refresh
            refreshAgentStatus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/upload-files")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload project files for scanning"""
    try:
        # Create temporary directory for uploaded files
        temp_dir = tempfile.mkdtemp(prefix="privacy_guardian_")
        
        # Save uploaded files
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        return {"project_path": temp_dir, "files_uploaded": len(files)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/scan", response_model=ScanResponse)
async def start_scan(request: ScanRequest):
    """Start a new privacy scan"""
    try:
        correlation_id = str(uuid.uuid4())
        
        # Store scan session
        scan_sessions[correlation_id] = {
            "status": "running",
            "start_time": datetime.now(UTC),
            "request": request.dict(),
            "progress": 0.0
        }
        
        # Start scan in background
        asyncio.create_task(run_scan_background(correlation_id, request))
        
        return ScanResponse(
            correlation_id=correlation_id,
            status="started",
            total_violations=0,
            agents_used=[],
            timestamp=datetime.now(UTC).isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

async def run_scan_background(correlation_id: str, request: ScanRequest):
    """Run scan in background task"""
    try:
        # Update progress
        scan_sessions[correlation_id]["progress"] = 0.1
        
        # Run scan
        result = await orchestrator.run_privacy_scan(
            project_path=request.project_path,
            enable_ai=request.enable_ai
        )
        
        # Update session with results
        scan_sessions[correlation_id].update({
            "status": "completed",
            "progress": 1.0,
            "results": result
        })
        
    except Exception as e:
        scan_sessions[correlation_id].update({
            "status": "failed",
            "error": str(e)
        })

@app.get("/scan-status/{correlation_id}")
async def get_scan_status(correlation_id: str):
    """Get scan status and results"""
    if correlation_id not in scan_sessions:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    session = scan_sessions[correlation_id]
    
    if session["status"] == "completed":
        return {
            "status": "completed",
            "progress": 1.0,
            "results": session.get("results", {})
        }
    elif session["status"] == "failed":
        return {
            "status": "failed",
            "error": session.get("error", "Unknown error")
        }
    else:
        return {
            "status": "running",
            "progress": session.get("progress", 0.0)
        }

@app.get("/agent-status")
async def get_agent_status():
    """Get status of all agents"""
    return orchestrator.get_agent_status()

@app.get("/event-history/{correlation_id}")
async def get_event_history(correlation_id: str):
    """Get event history for a specific scan"""
    events = orchestrator.get_event_history(correlation_id)
    return {"events": events}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 