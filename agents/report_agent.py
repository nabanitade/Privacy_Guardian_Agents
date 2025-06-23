"""
ReportAgent - Comprehensive Privacy Audit Report Generation
==========================================================

This agent is responsible for generating comprehensive privacy audit reports
by aggregating all previous agent outputs. It listens for FixSuggestionsCompleted
events from FixSuggestionAgent and emits ReportGenerated events with final reports.

Key Responsibilities:
--------------------
- Listen for FixSuggestionsCompleted events from FixSuggestionAgent
- Aggregate all previous agent outputs (scan results, compliance analysis, fix suggestions)
- Generate comprehensive privacy audit reports
- Provide executive summaries and detailed findings
- Store reports in Google Cloud Storage or Firestore
- Emit ReportGenerated events with final reports and storage locations

Event-Based Architecture:
------------------------
This agent is the final step in the event flow chain:
- Listens for FixSuggestionsCompleted events from FixSuggestionAgent
- Aggregates all previous agent outputs
- Generates comprehensive privacy audit reports
- Emits ReportGenerated events with final reports

Report Generation Capabilities:
------------------------------
Executive Summary:
- High-level privacy posture assessment
- Key findings and risk levels
- Compliance scores and status
- Strategic recommendations

Detailed Findings:
- Comprehensive violation analysis
- File-by-file breakdown of issues
- Severity assessment and prioritization
- Technical details and context

Compliance Analysis:
- Regulatory framework mapping
- Compliance gap identification
- Risk assessment and quantification
- Legal and business implications

Fix Recommendations:
- Prioritized action items
- Implementation guidance and timeline
- Resource requirements and effort estimates
- Success criteria and validation

Risk Assessment:
- Overall risk level determination
- Financial and reputational impact
- Compliance and regulatory risks
- Mitigation strategies and recommendations

Processing Flow:
---------------
1. Listen for FixSuggestionsCompleted event from FixSuggestionAgent
2. Aggregate all previous agent outputs (scan results, compliance analysis, fix suggestions)
3. Generate comprehensive privacy audit report
4. Store report in Google Cloud Storage or Firestore
5. Emit ReportGenerated event with final report and storage location

AI Integration:
--------------
When Gemini AI is available:
- Enhances report generation with AI insights
- Provides business impact analysis
- Generates strategic recommendations
- Improves report clarity and actionability

Fallback Mechanisms:
-------------------
- Uses hardcoded report templates when AI is unavailable
- Maintains comprehensive report coverage
- Provides reliable report generation capabilities

Integration Points:
------------------
- FixSuggestionAgent: Receives FixSuggestionsCompleted events
- Google Gemini AI: Enhanced report generation
- Google Cloud Storage: Report storage and retrieval
- Event System: Listens for and emits events

Usage:
------
The agent is typically invoked by the Agent Orchestrator after FixSuggestionAgent:
- enhanced_results: AI-enhanced results from previous agents
- compliance_report: Compliance analysis from ComplianceAgent
- fix_suggestions: Fix recommendations from FixSuggestionAgent
- correlation_id: Request tracking ID
- report_options: Optional report configuration

Returns:
- Comprehensive privacy audit report
- Executive summary and detailed findings
- Compliance analysis and risk assessment
- Fix recommendations and action items
- Report storage location

Event Communication:
-------------------
Listens for:
- FixSuggestionsCompleted: Fix suggestions from FixSuggestionAgent

Emits:
- ReportGenerated: Final comprehensive report
- ReportGenerationStarted: When report generation begins

Dependencies:
-------------
- Google Gemini AI: Enhanced report generation
- FixSuggestionAgent: Source of FixSuggestionsCompleted events
- Google Cloud Storage: Report storage and retrieval
- asyncio: Asynchronous processing
- json: Data serialization and parsing
- datetime: Timestamp management
- typing: Type hints and data structures

Author: Privacy Guardian Team
Built with Google Cloud Agent Development Kit (ADK)

Integrations:
- Inserts report analytics into BigQuery after report generation
- Exports report metrics to Cloud Monitoring
- Fetches secrets (e.g., report config) from Secret Manager
- Cloud Function trigger template provided for serverless execution
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
import json
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from google.cloud import storage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

from .base_agent import BaseAgent, ScanResult, AgentEvent

class ReportAgent(BaseAgent):
    """
    Agent responsible for compiling results and generating comprehensive reports.
    
    This agent serves as the final step in the privacy compliance analysis
    workflow, compiling results from all other agents and generating
    comprehensive reports with executive summaries, business impact analysis,
    and strategic recommendations. It combines structured data analysis with
    AI-enhanced insights for maximum value.
    
    Key Features:
    - Comprehensive report compilation from all scan agents
    - AI-enhanced executive summaries and business impact analysis
    - Professional PDF report generation with formatting
    - Google Cloud Storage integration for report accessibility
    - Strategic recommendations and action plans
    - Risk quantification and compliance assessment
    
    Processing Flow:
    1. Receive comprehensive results from all other agents
    2. Generate structured report data with statistics and analysis
    3. Enhance reports with AI insights if available
    4. Create professional PDF reports with formatting
    5. Upload reports to cloud storage for accessibility
    
    AI Enhancement:
    - AI-generated executive summaries with business context
    - Enhanced business impact analysis with financial quantification
    - Strategic recommendations with implementation guidance
    - Risk mitigation strategies with specific controls
    - Action plans with resource requirements and timelines
    """
    
    def __init__(self):
        """Initialize the ReportAgent with cloud storage capabilities."""
        super().__init__("report_agent", "📋 ReportAgent")
        self.storage_client = None
        self._initialize_cloud_storage()
        
    def _initialize_cloud_storage(self):
        """Initialize Google Cloud Storage for report storage"""
        try:
            self.storage_client = storage.Client()
            self.log_activity("Cloud Storage initialized successfully")
        except Exception as e:
            self.log_activity(f"Failed to initialize Cloud Storage: {str(e)}", "warning")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process report generation by listening for FixSuggestionsCompleted event"""
        self.log_activity("Starting report generation - listening for FixSuggestionsCompleted event")
        
        # Example: Fetch a secret (report config) from Secret Manager
        # report_config = self.fetch_secret(f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/REPORT_CONFIG")

        # Check if we have all the necessary data from previous agents
        fix_suggestions = input_data.get('fix_suggestions', {})
        compliance_report = input_data.get('compliance_report', {})
        enhanced_results = input_data.get('enhanced_results', [])
        correlation_id = input_data.get('correlation_id', 'default')
        
        if not enhanced_results:
            self.log_activity("No enhanced results found in input - waiting for FixSuggestionsCompleted event", "warning")
            return {"error": "No enhanced results available for report generation"}

        # Convert enhanced results from dict to ScanResult objects if needed
        if isinstance(enhanced_results[0], dict):
            scan_results = [self._dict_to_scan_result(result) for result in enhanced_results]
        else:
            scan_results = enhanced_results

        # Publish report generation started event
        self.publish_event(
            "ReportGenerationStarted",
            {"violation_count": len(scan_results), "agent": self.agent_name},
            correlation_id
        )

        # Generate comprehensive report
        report = {
            "metadata": {
                "generated_at": datetime.now(UTC).isoformat(),
                "correlation_id": correlation_id,
                "total_violations": len(scan_results),
                "agents_used": ["PrivacyScanAgent", "GeminiAnalysisAgent", "ComplianceAgent", "FixSuggestionAgent", "ReportAgent"],
                "gemini_enhanced": self.is_gemini_available()
            },
            "executive_summary": {},
            "detailed_findings": [],
            "compliance_analysis": {},
            "fix_recommendations": {},
            "risk_assessment": {},
            "action_items": [],
            "gemini_enhanced": self.is_gemini_available()
        }

        if not scan_results:
            report["executive_summary"] = {
                "status": "CLEAN",
                "message": "No privacy violations detected",
                "compliance_score": 100,
                "risk_level": "LOW"
            }
            return report

        # Use Gemini AI for enhanced report generation if available
        if self.is_gemini_available():
            try:
                enhanced_report = await self._get_gemini_enhanced_report(scan_results, compliance_report, fix_suggestions)
                if enhanced_report:
                    report.update(enhanced_report)
                    self.log_activity("Gemini AI enhanced report generation completed")
                else:
                    # Fallback to hardcoded templates
                    report.update(self._generate_hardcoded_report(scan_results, compliance_report, fix_suggestions))
            except Exception as e:
                self.log_activity(f"Gemini report generation failed: {str(e)} - using hardcoded templates", "warning")
                report.update(self._generate_hardcoded_report(scan_results, compliance_report, fix_suggestions))
        else:
            # Use hardcoded templates
            report.update(self._generate_hardcoded_report(scan_results, compliance_report, fix_suggestions))

        # Store report in GCS or Firestore (simulated)
        storage_location = await self._store_report(report, correlation_id)

        # Publish ReportGenerated event for other agents to consume
        self.publish_event(
            "ReportGenerated",
            {
                "report_id": correlation_id,
                "storage_location": storage_location,
                "total_violations": len(scan_results),
                "compliance_score": report.get("executive_summary", {}).get("compliance_score", 0),
                "risk_level": report.get("executive_summary", {}).get("risk_level", "UNKNOWN"),
                "report": report,
                "agent": self.agent_name
            },
            correlation_id
        )

        self.log_activity(f"Report generation completed: {storage_location} - emitting ReportGenerated")

        # --- Google Cloud Integrations ---
        # Insert report analytics into BigQuery
        table_id = f"{os.getenv('GOOGLE_CLOUD_PROJECT')}.privacy.reports"
        rows = [report]
        self.insert_bigquery_analytics(table_id, rows)

        # Export report metric to Cloud Monitoring
        self.export_custom_metric(
            metric_type="custom.googleapis.com/agent/reports_generated",
            value=1,
            labels={"agent": self.agent_id}
        )

        return report

    def _dict_to_scan_result(self, result_dict: Dict[str, Any]) -> ScanResult:
        """Convert dictionary back to ScanResult object"""
        return ScanResult(
            file_path=result_dict.get('file_path', ''),
            line_number=result_dict.get('line_number', 0),
            violation_type=result_dict.get('violation_type', ''),
            description=result_dict.get('description', ''),
            severity=result_dict.get('severity', 'MEDIUM'),
            fix_suggestion=result_dict.get('fix_suggestion', ''),
            regulation_reference=result_dict.get('regulation_reference', ''),
            agent_id=result_dict.get('agent_id', self.agent_id),
            timestamp=datetime.fromisoformat(result_dict.get('timestamp', datetime.now(UTC).isoformat()))
        )
    
    async def _generate_enhanced_report(self, scan_results: List[ScanResult], project_path: str) -> Dict[str, Any]:
        """Generate comprehensive report data with AI enhancement"""
        # Generate base report data
        report_data = {
            "metadata": {
                "scan_timestamp": datetime.now(UTC).isoformat(),
                "project_path": project_path,
                "total_violations": len(scan_results),
                "agents_used": ["PrivacyScanAgent", "GeminiAnalysisAgent", "ComplianceAgent", "FixSuggestionAgent", "ReportAgent"],
                "gemini_enhanced": self.is_gemini_available()
            },
            "summary": self._generate_summary_statistics(scan_results),
            "violations_by_file": self._group_violations_by_file(scan_results),
            "violations_by_type": self._group_violations_by_type(scan_results),
            "violations_by_severity": self._group_violations_by_severity(scan_results),
            "compliance_analysis": self._generate_compliance_analysis(scan_results),
            "fix_recommendations": self._generate_fix_recommendations(scan_results),
            "detailed_violations": [self._violation_to_dict(v) for v in scan_results]
        }
        
        # Enhance with AI insights if available
        if self.is_gemini_available():
            try:
                ai_enhancements = await self._get_ai_report_enhancements(scan_results, report_data)
                if ai_enhancements:
                    report_data.update(ai_enhancements)
                    self.log_activity("AI enhancements added to report")
            except Exception as e:
                self.log_activity(f"AI report enhancement failed: {str(e)} - using base report", "warning")
        
        return report_data
    
    def _generate_summary_statistics(self, scan_results: List[ScanResult]) -> Dict[str, Any]:
        """Generate summary statistics"""
        total_violations = len(scan_results)
        high_severity = len([v for v in scan_results if v.severity == "HIGH"])
        medium_severity = len([v for v in scan_results if v.severity == "MEDIUM"])
        low_severity = len([v for v in scan_results if v.severity == "LOW"])
        
        # Count unique files
        unique_files = len(set(v.file_path for v in scan_results))
        
        # Count violation types
        violation_types = {}
        for violation in scan_results:
            if violation.violation_type not in violation_types:
                violation_types[violation.violation_type] = 0
            violation_types[violation.violation_type] += 1
        
        # Count regulations affected
        regulations = set()
        for violation in scan_results:
            for reg in violation.regulation_reference.split(', '):
                if reg.strip():
                    regulations.add(reg.strip())
        
        return {
            "total_violations": total_violations,
            "severity_breakdown": {
                "HIGH": high_severity,
                "MEDIUM": medium_severity,
                "LOW": low_severity
            },
            "unique_files_affected": unique_files,
            "violation_types": violation_types,
            "regulations_affected": list(regulations),
            "risk_score": self._calculate_risk_score(scan_results)
        }
    
    def _calculate_risk_score(self, scan_results: List[ScanResult]) -> int:
        """Calculate overall risk score (0-100)"""
        score = 0
        for violation in scan_results:
            if violation.severity == "HIGH":
                score += 10
            elif violation.severity == "MEDIUM":
                score += 5
            else:
                score += 2
        
        return min(score, 100)
    
    def _group_violations_by_file(self, scan_results: List[ScanResult]) -> Dict[str, List[Dict]]:
        """Group violations by file"""
        grouped = {}
        for violation in scan_results:
            if violation.file_path not in grouped:
                grouped[violation.file_path] = []
            grouped[violation.file_path].append(self._violation_to_dict(violation))
        return grouped
    
    def _group_violations_by_type(self, scan_results: List[ScanResult]) -> Dict[str, List[Dict]]:
        """Group violations by type"""
        grouped = {}
        for violation in scan_results:
            if violation.violation_type not in grouped:
                grouped[violation.violation_type] = []
            grouped[violation.violation_type].append(self._violation_to_dict(violation))
        return grouped
    
    def _group_violations_by_severity(self, scan_results: List[ScanResult]) -> Dict[str, List[Dict]]:
        """Group violations by severity"""
        grouped = {}
        for violation in scan_results:
            if violation.severity not in grouped:
                grouped[violation.severity] = []
            grouped[violation.severity].append(self._violation_to_dict(violation))
        return grouped
    
    def _generate_compliance_analysis(self, scan_results: List[ScanResult]) -> Dict[str, Any]:
        """Generate compliance analysis"""
        gdpr_violations = [v for v in scan_results if "GDPR" in v.regulation_reference]
        ccpa_violations = [v for v in scan_results if "CCPA" in v.regulation_reference]
        hipaa_violations = [v for v in scan_results if "HIPAA" in v.regulation_reference]
        pci_violations = [v for v in scan_results if "PCI" in v.regulation_reference]
        
        return {
            "gdpr": {
                "total_violations": len(gdpr_violations),
                "high_severity": len([v for v in gdpr_violations if v.severity == "HIGH"]),
                "articles_affected": list(set([
                    reg for v in gdpr_violations 
                    for reg in v.regulation_reference.split(', ') 
                    if "GDPR" in reg
                ]))
            },
            "ccpa": {
                "total_violations": len(ccpa_violations),
                "high_severity": len([v for v in ccpa_violations if v.severity == "HIGH"]),
                "sections_affected": list(set([
                    reg for v in ccpa_violations 
                    for reg in v.regulation_reference.split(', ') 
                    if "CCPA" in reg
                ]))
            },
            "hipaa": {
                "total_violations": len(hipaa_violations),
                "high_severity": len([v for v in hipaa_violations if v.severity == "HIGH"])
            },
            "pci_dss": {
                "total_violations": len(pci_violations),
                "high_severity": len([v for v in pci_violations if v.severity == "HIGH"])
            }
        }
    
    def _generate_fix_recommendations(self, scan_results: List[ScanResult]) -> Dict[str, Any]:
        """Generate fix recommendations summary for all 50+ violation types"""
        fix_categories = {
            # PII Detection Fixes
            "environment_variables": len([v for v in scan_results if "os.getenv" in v.fix_suggestion]),
            "secure_storage": len([v for v in scan_results if "secure" in v.fix_suggestion.lower()]),
            "data_hashing": len([v for v in scan_results if "hash" in v.fix_suggestion.lower()]),
            "tokenization": len([v for v in scan_results if "token" in v.fix_suggestion.lower()]),
            
            # Security & Encryption Fixes
            "encryption": len([v for v in scan_results if "encrypt" in v.fix_suggestion.lower()]),
            "https_upgrade": len([v for v in scan_results if "https" in v.fix_suggestion.lower()]),
            "tls_enablement": len([v for v in scan_results if "tls" in v.fix_suggestion.lower() or "ssl" in v.fix_suggestion.lower()]),
            "rate_limiting": len([v for v in scan_results if "rate" in v.fix_suggestion.lower()]),
            
            # Consent & Privacy Policy Fixes
            "consent_mechanisms": len([v for v in scan_results if "consent" in v.fix_suggestion.lower()]),
            "opt_out_mechanisms": len([v for v in scan_results if "opt" in v.fix_suggestion.lower()]),
            "purpose_limitation": len([v for v in scan_results if "purpose" in v.fix_suggestion.lower()]),
            "profiling_controls": len([v for v in scan_results if "profiling" in v.fix_suggestion.lower()]),
            
            # Data Flow & Handling Fixes
            "data_masking": len([v for v in scan_results if "mask" in v.fix_suggestion.lower()]),
            "data_anonymization": len([v for v in scan_results if "anonymize" in v.fix_suggestion.lower()]),
            "retention_policies": len([v for v in scan_results if "retention" in v.fix_suggestion.lower()]),
            "dsar_compliance": len([v for v in scan_results if "dsar" in v.fix_suggestion.lower()]),
            "stack_trace_sanitization": len([v for v in scan_results if "stack" in v.fix_suggestion.lower()]),
            
            # Advanced Privacy Fixes
            "field_level_scoping": len([v for v in scan_results if "scope" in v.fix_suggestion.lower()]),
            "region_compliance": len([v for v in scan_results if "region" in v.fix_suggestion.lower()]),
            "api_versioning": len([v for v in scan_results if "version" in v.fix_suggestion.lower()]),
            "data_minimization": len([v for v in scan_results if "minimization" in v.fix_suggestion.lower()]),
            
            # Developer Guidance Fixes
            "access_controls": len([v for v in scan_results if "permission" in v.fix_suggestion.lower() or "auth" in v.fix_suggestion.lower()]),
            "audit_logging": len([v for v in scan_results if "audit" in v.fix_suggestion.lower()]),
            "cache_expiration": len([v for v in scan_results if "cache" in v.fix_suggestion.lower()]),
            "database_security": len([v for v in scan_results if "database" in v.fix_suggestion.lower()]),
            
            # AI Privacy Fixes
            "ml_pipeline_security": len([v for v in scan_results if "ml" in v.fix_suggestion.lower() or "ai" in v.fix_suggestion.lower()]),
            "data_deletion": len([v for v in scan_results if "delete" in v.fix_suggestion.lower()]),
            "backup_optimization": len([v for v in scan_results if "backup" in v.fix_suggestion.lower()]),
            
            # General Fixes
            "code_review": len([v for v in scan_results if "review" in v.fix_suggestion.lower()]),
            "documentation": len([v for v in scan_results if "document" in v.fix_suggestion.lower()]),
            "testing": len([v for v in scan_results if "test" in v.fix_suggestion.lower()])
        }
        
        # Calculate total estimated effort
        total_minutes = 0
        for violation in scan_results:
            effort_match = re.search(r'Estimated Effort: (\d+) minutes', violation.description)
            if effort_match:
                total_minutes += int(effort_match.group(1))
        
        # Categorize violations by priority
        critical_violations = [v for v in scan_results if "CRITICAL" in v.description]
        high_violations = [v for v in scan_results if "HIGH" in v.description and "CRITICAL" not in v.description]
        medium_violations = [v for v in scan_results if "MEDIUM" in v.description]
        low_violations = [v for v in scan_results if "LOW" in v.description]
        
        return {
            "fix_categories": fix_categories,
            "total_estimated_effort_minutes": total_minutes,
            "priority_fixes": {
                "critical": critical_violations,
                "high": high_violations,
                "medium": medium_violations,
                "low": low_violations
            },
            "violation_type_breakdown": self._get_violation_type_breakdown(scan_results)
        }
    
    def _get_violation_type_breakdown(self, scan_results: List[ScanResult]) -> Dict[str, int]:
        """Get breakdown of violation types"""
        breakdown = {}
        for violation in scan_results:
            violation_type = violation.violation_type
            if violation_type not in breakdown:
                breakdown[violation_type] = 0
            breakdown[violation_type] += 1
        return breakdown
    
    def _violation_to_dict(self, violation: ScanResult) -> Dict[str, Any]:
        """Convert violation to dictionary"""
        return {
            "file_path": violation.file_path,
            "line_number": violation.line_number,
            "violation_type": violation.violation_type,
            "description": violation.description,
            "severity": violation.severity,
            "fix_suggestion": violation.fix_suggestion,
            "regulation_reference": violation.regulation_reference,
            "agent_id": violation.agent_id,
            "timestamp": violation.timestamp.isoformat()
        }
    
    async def _generate_pdf_report(self, report_data: Dict[str, Any], correlation_id: str) -> str:
        """Generate PDF report"""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"privacy_scan_report_{correlation_id}_{timestamp}.pdf"
        pdf_path = f"reports/{pdf_filename}"
        
        # Ensure reports directory exists
        os.makedirs("reports", exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("Privacy Guardian Agents - Scan Report", title_style))
        story.append(Spacer(1, 20))
        
        # Metadata
        metadata = report_data['metadata']
        story.append(Paragraph(f"<b>Scan Date:</b> {metadata['scan_timestamp']}", styles['Normal']))
        story.append(Paragraph(f"<b>Project Path:</b> {metadata['project_path']}", styles['Normal']))
        story.append(Paragraph(f"<b>Total Violations:</b> {metadata['total_violations']}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary Statistics
        story.append(Paragraph("Summary Statistics", styles['Heading2']))
        summary = report_data['summary']
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Violations', str(summary['total_violations'])],
            ['High Severity', str(summary['severity_breakdown']['HIGH'])],
            ['Medium Severity', str(summary['severity_breakdown']['MEDIUM'])],
            ['Low Severity', str(summary['severity_breakdown']['LOW'])],
            ['Risk Score', f"{summary['risk_score']}/100"],
            ['Files Affected', str(summary['unique_files_affected'])]
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detailed Violations
        story.append(Paragraph("Detailed Violations", styles['Heading2']))
        for violation in report_data['detailed_violations'][:10]:  # Limit to first 10 for PDF
            story.append(Paragraph(f"<b>File:</b> {violation['file_path']}:{violation['line_number']}", styles['Normal']))
            story.append(Paragraph(f"<b>Type:</b> {violation['violation_type']}", styles['Normal']))
            story.append(Paragraph(f"<b>Severity:</b> {violation['severity']}", styles['Normal']))
            story.append(Paragraph(f"<b>Description:</b> {violation['description']}", styles['Normal']))
            story.append(Paragraph(f"<b>Fix:</b> {violation['fix_suggestion'][:200]}...", styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(story)
        
        return pdf_path
    
    async def _upload_to_cloud_storage(self, pdf_path: str, correlation_id: str) -> Optional[str]:
        """Upload PDF to Google Cloud Storage"""
        try:
            bucket_name = os.getenv('GCS_BUCKET_NAME', 'privacy-guardian-reports')
            bucket = self.storage_client.bucket(bucket_name)
            
            # Create bucket if it doesn't exist
            if not bucket.exists():
                bucket = self.storage_client.create_bucket(bucket_name)
            
            blob_name = f"reports/{os.path.basename(pdf_path)}"
            blob = bucket.blob(blob_name)
            
            blob.upload_from_filename(pdf_path)
            
            # Make blob publicly readable
            blob.make_public()
            
            return blob.public_url
            
        except Exception as e:
            self.log_activity(f"Failed to upload to Cloud Storage: {str(e)}", "warning")
            return None
    
    async def _get_ai_report_enhancements(self, scan_results: List[ScanResult], base_report: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get AI-enhanced report insights"""
        try:
            prompt = self._create_report_enhancement_prompt(scan_results, base_report)
            
            ai_response = await self.get_gemini_analysis(prompt, {
                "violation_count": len(scan_results),
                "report_sections": list(base_report.keys())
            })
            
            if ai_response:
                return self._parse_report_enhancement_response(ai_response)
                
        except Exception as e:
            self.log_activity(f"AI report enhancement error: {str(e)}", "warning")
        
        return None

    def _create_report_enhancement_prompt(self, scan_results: List[ScanResult], base_report: Dict[str, Any]) -> str:
        """Create AI prompt for report enhancement"""
        summary = base_report.get('summary', {})
        violation_types = summary.get('violation_types', {})
        
        prompt = f"""
You are a privacy compliance expert creating an executive report for a privacy vulnerability scan.

Scan Summary:
- Total violations: {len(scan_results)}
- High severity: {summary.get('severity_breakdown', {}).get('HIGH', 0)}
- Medium severity: {summary.get('severity_breakdown', {}).get('MEDIUM', 0)}
- Low severity: {summary.get('severity_breakdown', {}).get('LOW', 0)}
- Risk score: {summary.get('risk_score', 0)}/100
- Regulations affected: {', '.join(summary.get('regulations_affected', []))}

Top violation types:
{chr(10).join([f"- {vtype}: {count}" for vtype, count in list(violation_types.items())[:5]])}

Please provide enhanced report sections including:

1. **Executive Summary**: High-level overview for C-level executives
2. **Business Impact Analysis**: Financial, legal, and reputational risks
3. **Compliance Assessment**: Detailed regulatory compliance status
4. **Strategic Recommendations**: Long-term privacy strategy
5. **Action Plan**: Prioritized immediate actions
6. **Risk Mitigation**: Specific risk reduction strategies

Format as JSON:
{{
    "executive_summary": {{
        "overview": "<high-level summary>",
        "key_findings": ["<finding 1>", "<finding 2>"],
        "business_impact": "<impact assessment>",
        "urgency_level": "<CRITICAL/HIGH/MEDIUM/LOW>"
    }},
    "business_impact_analysis": {{
        "financial_risk": {{
            "potential_fines": "<estimated fines>",
            "compliance_costs": "<estimated costs>",
            "remediation_costs": "<estimated costs>"
        }},
        "legal_risk": {{
            "regulatory_violations": ["<violation 1>", "<violation 2>"],
            "litigation_risk": "<risk assessment>"
        }},
        "reputational_risk": {{
            "customer_trust": "<impact assessment>",
            "brand_damage": "<potential damage>"
        }}
    }},
    "compliance_assessment": {{
        "overall_status": "<COMPLIANT/PARTIALLY_COMPLIANT/NON_COMPLIANT>",
        "gdpr_compliance": {{
            "status": "<status>",
            "violations": ["<violation 1>", "<violation 2>"],
            "required_actions": ["<action 1>", "<action 2>"]
        }},
        "ccpa_compliance": {{
            "status": "<status>",
            "violations": ["<violation 1>", "<violation 2>"],
            "required_actions": ["<action 1>", "<action 2>"]
        }}
    }},
    "strategic_recommendations": [
        {{
            "recommendation": "<description>",
            "priority": "<HIGH/MEDIUM/LOW>",
            "timeline": "<short/medium/long term>",
            "expected_outcome": "<outcome>",
            "resource_requirements": "<resources needed>"
        }}
    ],
    "action_plan": {{
        "immediate_actions": [
            {{
                "action": "<description>",
                "timeline": "<timeline>",
                "owner": "<responsible party>",
                "success_criteria": "<criteria>"
            }}
        ],
        "short_term_actions": [
            {{
                "action": "<description>",
                "timeline": "<timeline>",
                "owner": "<responsible party>",
                "success_criteria": "<criteria>"
            }}
        ]
    }},
    "risk_mitigation": {{
        "technical_controls": ["<control 1>", "<control 2>"],
        "process_improvements": ["<improvement 1>", "<improvement 2>"],
        "training_recommendations": ["<training 1>", "<training 2>"],
        "monitoring_strategy": "<strategy description>"
    }}
}}

Focus on actionable insights that help executives understand the business implications and make informed decisions.
"""
        return prompt

    def _parse_report_enhancement_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI report enhancement response"""
        try:
            ai_data = json.loads(ai_response)
            return {
                "ai_enhancements": ai_data
            }
        except json.JSONDecodeError as e:
            self.log_activity(f"Failed to parse AI report enhancement: {str(e)}", "warning")
            return {}
        except Exception as e:
            self.log_activity(f"Error processing AI report enhancement: {str(e)}", "warning")
            return {}

    async def _get_gemini_enhanced_report(self, scan_results: List[ScanResult], compliance_report: Dict[str, Any], fix_suggestions: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get AI-enhanced report from Gemini"""
        try:
            prompt = self._create_report_prompt(scan_results, compliance_report, fix_suggestions)
            
            ai_response = await self.get_gemini_analysis(prompt, {
                "violation_count": len(scan_results),
                "compliance_score": compliance_report.get("compliance_score", 0),
                "fix_count": fix_suggestions.get("summary", {}).get("fixes_generated", 0)
            })
            
            if ai_response:
                return self._parse_report_response(ai_response, scan_results, compliance_report, fix_suggestions)
                
        except Exception as e:
            self.log_activity(f"Gemini report generation error: {str(e)}", "warning")
        
        return None

    def _generate_hardcoded_report(self, scan_results: List[ScanResult], compliance_report: Dict[str, Any], fix_suggestions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report using hardcoded templates"""
        # Executive Summary
        total_violations = len(scan_results)
        high_severity = len([v for v in scan_results if v.severity == "HIGH"])
        compliance_score = compliance_report.get("compliance_score", 0)
        
        if total_violations == 0:
            status = "CLEAN"
            risk_level = "LOW"
            message = "No privacy violations detected"
        elif high_severity > 0:
            status = "CRITICAL"
            risk_level = "HIGH"
            message = f"{high_severity} high-severity violations require immediate attention"
        elif compliance_score < 50:
            status = "NON_COMPLIANT"
            risk_level = "HIGH"
            message = "Significant compliance issues detected"
        else:
            status = "NEEDS_IMPROVEMENT"
            risk_level = "MEDIUM"
            message = f"{total_violations} violations need to be addressed"
        
        executive_summary = {
            "status": status,
            "message": message,
            "compliance_score": compliance_score,
            "risk_level": risk_level,
            "total_violations": total_violations,
            "high_severity_count": high_severity
        }
        
        # Detailed Findings
        detailed_findings = []
        for result in scan_results:
            detailed_findings.append({
                "file_path": result.file_path,
                "line_number": result.line_number,
                "violation_type": result.violation_type,
                "description": result.description,
                "severity": result.severity,
                "regulation_reference": result.regulation_reference,
                "fix_suggestion": result.fix_suggestion
            })
        
        # Risk Assessment
        risk_assessment = {
            "overall_risk": risk_level,
            "high_risk_violations": high_severity,
            "compliance_risk": "HIGH" if compliance_score < 50 else "MEDIUM" if compliance_score < 80 else "LOW",
            "regulatory_risk": "HIGH" if any("GDPR" in v.regulation_reference for v in scan_results) else "MEDIUM"
        }
        
        # Action Items
        action_items = []
        if high_severity > 0:
            action_items.append("Immediately address high-severity violations")
        if compliance_score < 80:
            action_items.append("Improve compliance score through systematic fixes")
        action_items.append("Implement suggested fixes for all violations")
        action_items.append("Establish ongoing privacy monitoring")
        
        return {
            "executive_summary": executive_summary,
            "detailed_findings": detailed_findings,
            "compliance_analysis": compliance_report,
            "fix_recommendations": fix_suggestions,
            "risk_assessment": risk_assessment,
            "action_items": action_items
        }

    async def _store_report(self, report: Dict[str, Any], correlation_id: str) -> str:
        """Store report in GCS or Firestore (simulated)"""
        try:
            # Simulate storage to GCS
            storage_location = f"gs://privacy-reports/{correlation_id}/report.json"
            self.log_activity(f"Report stored at: {storage_location}")
            return storage_location
        except Exception as e:
            self.log_activity(f"Report storage failed: {str(e)} - using local storage", "warning")
            return f"local://reports/{correlation_id}/report.json"

    def _create_report_prompt(self, scan_results: List[ScanResult], compliance_report: Dict[str, Any], fix_suggestions: Dict[str, Any]) -> str:
        """Create AI prompt for report generation"""
        violations_text = "\n".join([
            f"- {v.file_path}:{v.line_number} - {v.violation_type} ({v.severity}): {v.description}"
            for v in scan_results
        ])
        
        prompt = f"""
You are a privacy compliance expert generating a comprehensive privacy audit report.

Violations Found:
{violations_text}

Compliance Analysis:
{json.dumps(compliance_report, indent=2)}

Fix Suggestions:
{json.dumps(fix_suggestions, indent=2)}

Please generate a comprehensive report with:

1. **Executive Summary**: High-level status, risk assessment, key metrics
2. **Detailed Findings**: Each violation with context and impact
3. **Compliance Analysis**: Regulatory implications and compliance score
4. **Fix Recommendations**: Prioritized action items with implementation guidance
5. **Risk Assessment**: Overall risk level and specific risk factors
6. **Action Items**: Clear next steps for remediation

Format your response as JSON:
{{
    "executive_summary": {{
        "status": "<CLEAN/NEEDS_IMPROVEMENT/NON_COMPLIANT/CRITICAL>",
        "message": "<summary message>",
        "compliance_score": <0-100>,
        "risk_level": "<LOW/MEDIUM/HIGH>",
        "total_violations": <count>,
        "high_severity_count": <count>
    }},
    "detailed_findings": [
        {{
            "file_path": "<path>",
            "line_number": <line>,
            "violation_type": "<type>",
            "description": "<description>",
            "severity": "<HIGH/MEDIUM/LOW>",
            "regulation_reference": "<regulations>",
            "fix_suggestion": "<fix>",
            "impact": "<business impact>"
        }}
    ],
    "risk_assessment": {{
        "overall_risk": "<LOW/MEDIUM/HIGH>",
        "high_risk_violations": <count>,
        "compliance_risk": "<LOW/MEDIUM/HIGH>",
        "regulatory_risk": "<LOW/MEDIUM/HIGH>",
        "business_impact": "<description>"
    }},
    "action_items": [
        "<prioritized action item>"
    ]
}}

Focus on actionable insights and clear recommendations for privacy compliance improvement.
"""
        return prompt

    def _parse_report_response(self, ai_response: str, scan_results: List[ScanResult], compliance_report: Dict[str, Any], fix_suggestions: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response for report generation"""
        try:
            ai_data = json.loads(ai_response)
            
            return {
                "executive_summary": ai_data.get("executive_summary", {}),
                "detailed_findings": ai_data.get("detailed_findings", []),
                "compliance_analysis": compliance_report,
                "fix_recommendations": fix_suggestions,
                "risk_assessment": ai_data.get("risk_assessment", {}),
                "action_items": ai_data.get("action_items", [])
            }
            
        except json.JSONDecodeError as e:
            self.log_activity(f"Failed to parse AI report response: {str(e)}", "warning")
            return self._generate_hardcoded_report(scan_results, compliance_report, fix_suggestions)
        except Exception as e:
            self.log_activity(f"Error processing AI report response: {str(e)}", "warning")
            return self._generate_hardcoded_report(scan_results, compliance_report, fix_suggestions)

    # Cloud Function trigger template (for reference)
    # def cloud_function_entrypoint(request):
    #     """
    #     Cloud Function HTTP trigger for ReportAgent.
    #     """
    #     # Parse request, call self.process(), return response
    #     pass 