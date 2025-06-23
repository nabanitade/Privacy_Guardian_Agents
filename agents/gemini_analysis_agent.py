"""
GeminiAnalysisAgent - AI-Powered Privacy Violation Enhancement
==============================================================

This agent is responsible for enhancing privacy violation findings with Google Gemini AI
analysis. It listens for FindingsReady events from PrivacyScanAgent and emits
AIEnhancedFindings events for downstream agents to consume.

Key Responsibilities:
--------------------
- Listen for FindingsReady events from PrivacyScanAgent
- Enhance violation descriptions with business context using Gemini AI
- Re-assess severity based on broader implications and context
- Discover additional privacy violations not caught by rule-based detection
- Provide AI-powered insights and recommendations
- Emit AIEnhancedFindings events with enhanced results

Event-Based Architecture:
------------------------
This agent is the second in the event flow chain:
- Listens for FindingsReady events from PrivacyScanAgent
- Performs AI enhancement using Google Gemini
- Emits AIEnhancedFindings events with enhanced results
- Discovers new violations through AI analysis

AI Enhancement Capabilities:
---------------------------
Context-Aware Analysis:
- Enhances violation descriptions with business context
- Re-assesses severity based on broader implications
- Identifies related privacy issues not caught by rules
- Provides additional context and recommendations

Violation Discovery:
- Discovers new violations through AI analysis
- Identifies patterns and correlations between violations
- Finds context-specific privacy risks
- Suggests additional areas for investigation

Business Impact Analysis:
- Assesses financial and reputational risks
- Evaluates compliance implications
- Provides strategic recommendations
- Identifies priority areas for remediation

Processing Flow:
---------------
1. Listen for FindingsReady event from PrivacyScanAgent
2. Convert scan results to ScanResult objects if needed
3. Check Gemini AI availability
4. Group violations by file for efficient processing
5. Enhance each violation with AI analysis
6. Generate comprehensive AI insights
7. Emit AIEnhancedFindings event with enhanced results

AI Integration:
--------------
When Gemini AI is available:
- Enhances violation descriptions with business context
- Re-assesses severity based on broader implications
- Identifies related privacy issues not caught by rules
- Provides additional context and recommendations
- Discovers new violations through AI analysis

Fallback Mechanisms:
-------------------
- Returns original results if Gemini AI is unavailable
- Emits AIAnalysisSkipped event with fallback reason
- Maintains system reliability through graceful degradation

Integration Points:
------------------
- PrivacyScanAgent: Receives FindingsReady events
- Google Gemini AI: Primary AI enhancement engine
- ComplianceAgent: Emits AIEnhancedFindings for compliance analysis
- Event System: Listens for and emits events

Usage:
------
The agent is typically invoked by the Agent Orchestrator after PrivacyScanAgent:
- enhanced_results: Scan results from PrivacyScanAgent
- correlation_id: Request tracking ID
- ai_options: Optional AI configuration

Returns:
- Enhanced ScanResult objects with AI insights
- Additional violations discovered through AI
- Comprehensive AI analysis and recommendations

Event Communication:
-------------------
Listens for:
- FindingsReady: Raw scan results from PrivacyScanAgent

Emits:
- AIEnhancedFindings: Enhanced results with AI insights
- AIAnalysisSkipped: When AI is unavailable (fallback)
- AIAnalysisFailed: When AI processing fails

Dependencies:
-------------
- Google Gemini AI: Primary AI enhancement engine
- PrivacyScanAgent: Source of FindingsReady events
- asyncio: Asynchronous processing
- json: Data serialization and parsing
- datetime: Timestamp management
- typing: Type hints and data structures

Author: Privacy Guardian Team
Built with Google Cloud Agent Development Kit (ADK)

Integrations:
- Inserts enhanced results analytics into BigQuery after AI analysis
- Exports AI analysis metrics to Cloud Monitoring
- Fetches secrets (e.g., Gemini config) from Secret Manager
- Cloud Function trigger template provided for serverless execution
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
import json

from .base_agent import BaseAgent, ScanResult, AgentEvent

class GeminiAnalysisAgent(BaseAgent):
    """
    Agent responsible for AI-powered privacy analysis using Google Gemini.
    
    This agent serves as the primary AI analysis engine for the Privacy Guardian
    system, providing comprehensive privacy posture assessment, architectural
    analysis, and strategic recommendations. It combines the power of Google
    Gemini AI with deep privacy compliance expertise.
    
    Key Features:
    - Comprehensive AI analysis of privacy violations with context
    - Architectural privacy analysis and data flow pattern recognition
    - Business impact assessment and risk quantification
    - Strategic recommendations for privacy improvements
    - Additional violation discovery through AI analysis
    - Robust fallback to original results when AI is unavailable
    
    Processing Flow:
    1. Receive scan results from PrivacyScanAgent
    2. Group violations by file for efficient AI processing
    3. Analyze each file with context-aware AI prompts
    4. Enhance violations with AI insights and additional discoveries
    5. Generate comprehensive privacy analysis and recommendations
    
    AI Analysis:
    - Context-aware violation analysis with file content understanding
    - Architectural privacy assessment and data flow analysis
    - Business impact quantification and risk assessment
    - Strategic recommendations for privacy improvements
    - Additional violation discovery through AI pattern recognition
    """
    
    def __init__(self):
        """Initialize the GeminiAnalysisAgent with AI capabilities."""
        super().__init__("gemini_analysis_agent", "🤖 GeminiAnalysisAgent")
        # Use base agent's Gemini initialization
        
    async def process(self, input_data: Dict[str, Any]) -> List[ScanResult]:
        """Process AI analysis request by listening for FindingsReady event"""
        self.log_activity("Starting AI analysis - listening for FindingsReady event")
        
        # Example: Fetch a secret (Gemini config) from Secret Manager
        # gemini_config = self.fetch_secret(f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/GEMINI_CONFIG")

        # Check if we have scan results in input_data (from FindingsReady event)
        scan_results = input_data.get('scan_results', [])
        correlation_id = input_data.get('correlation_id', 'default')
        
        if not scan_results:
            self.log_activity("No scan results found in input - waiting for FindingsReady event", "warning")
            return []
        
        # Convert scan results from dict to ScanResult objects if needed
        if isinstance(scan_results[0], dict):
            scan_results = [self._dict_to_scan_result(result) for result in scan_results]
        
        # Check if Gemini is available
        if not self.is_gemini_available():
            self.log_activity("Gemini AI not available, returning original results", "warning")
            self.publish_event(
                "AIAnalysisSkipped",
                {"reason": "Gemini not available", "fallback": "original_results"},
                correlation_id
            )
            return scan_results
        
        # Publish AI analysis started event
        self.publish_event(
            "AIAnalysisStarted",
            {"total_violations": len(scan_results), "agent": self.agent_name},
            correlation_id
        )
        
        enhanced_results = []
        
        try:
            # Group violations by file for efficient processing
            file_violations = self._group_violations_by_file(scan_results)
            
            for file_path, violations in file_violations.items():
                file_results = await self._analyze_file_violations(file_path, violations)
                enhanced_results.extend(file_results)
            
            # Generate comprehensive AI insights
            ai_insights = await self._generate_comprehensive_insights(scan_results, enhanced_results)
            
            # Publish AIEnhancedFindings event for other agents to consume
            self.publish_event(
                "AIEnhancedFindings",
                {
                    "original_violations": len(scan_results),
                    "enhanced_violations": len(enhanced_results),
                    "ai_enhancements": len(enhanced_results) - len(scan_results),
                    "ai_insights": ai_insights,
                    "enhanced_results": [self._scan_result_to_dict(result) for result in enhanced_results],
                    "gemini_enhanced": True
                },
                correlation_id
            )
            
            self.log_activity(f"AI analysis completed: {len(enhanced_results)} enhanced violations - emitting AIEnhancedFindings")
            
        except Exception as e:
            self.log_activity(f"AI analysis failed: {str(e)} - returning original results", "error")
            self.publish_event(
                "AIAnalysisFailed",
                {"error": str(e), "fallback": "original_results"},
                correlation_id
            )
            # Return original results if AI fails
            return scan_results
        
        # --- Google Cloud Integrations ---
        # Insert enhanced results analytics into BigQuery
        table_id = f"{os.getenv('GOOGLE_CLOUD_PROJECT')}.privacy.enhanced_results"
        rows = [r.__dict__ for r in enhanced_results]
        self.insert_bigquery_analytics(table_id, rows)

        # Export AI analysis metric to Cloud Monitoring
        self.export_custom_metric(
            metric_type="custom.googleapis.com/agent/ai_enhanced_violations",
            value=len(enhanced_results),
            labels={"agent": self.agent_id}
        )

        return enhanced_results

    def _group_violations_by_file(self, scan_results: List[ScanResult]) -> Dict[str, List[ScanResult]]:
        """Group violations by file path for efficient AI processing"""
        grouped = {}
        for result in scan_results:
            if result.file_path not in grouped:
                grouped[result.file_path] = []
            grouped[result.file_path].append(result)
        return grouped
    
    async def _analyze_file_violations(self, file_path: str, violations: List[ScanResult]) -> List[ScanResult]:
        """Analyze violations in a single file using enhanced Gemini AI"""
        enhanced_results = []
        
        try:
            # Read file content for context
            file_content = self._read_file_content(file_path)
            if not file_content:
                return violations
            
            # Prepare enhanced AI prompt
            prompt = self._create_enhanced_ai_prompt(file_path, file_content, violations)
            
            # Get AI analysis using base agent's Gemini capabilities
            ai_response = await self.get_gemini_analysis(prompt, {
                "file_path": file_path,
                "violation_count": len(violations),
                "file_size": len(file_content)
            })
            
            if ai_response:
                # Process AI response and enhance violations
                enhanced_results = self._process_enhanced_ai_response(violations, ai_response, file_path)
            else:
                # Fallback to original violations if AI fails
                enhanced_results = violations
            
        except Exception as e:
            self.log_activity(f"Error analyzing {file_path}: {str(e)} - using original violations", "warning")
            return violations
        
        return enhanced_results
    
    def _read_file_content(self, file_path: str) -> Optional[str]:
        """Read file content for AI context"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Limit content to avoid token limits while preserving context
                return content[:4000] if len(content) > 4000 else content
        except Exception as e:
            self.log_activity(f"Could not read {file_path}: {str(e)}", "warning")
            return None
    
    def _create_enhanced_ai_prompt(self, file_path: str, file_content: str, violations: List[ScanResult]) -> str:
        """Create enhanced AI prompt for comprehensive privacy analysis"""
        violations_text = "\n".join([
            f"- Line {v.line_number}: {v.violation_type} - {v.description} [Severity: {v.severity}]"
            for v in violations
        ])
        
        prompt = f"""
You are an expert privacy compliance analyst with deep knowledge of GDPR, CCPA, HIPAA, and other privacy regulations.

File: {file_path}
Content (first 4000 characters):
{file_content}

Detected violations:
{violations_text}

Please provide a comprehensive privacy analysis including:

1. **Enhanced Violation Analysis**: For each detected violation:
   - Detailed explanation of the privacy risk
   - Specific regulatory violations (GDPR articles, CCPA sections, etc.)
   - Business impact assessment
   - Enhanced fix suggestions with code examples
   - Related privacy concerns

2. **Additional Violations**: Identify any related privacy issues not yet detected:
   - Missing consent mechanisms
   - Data retention violations
   - Security vulnerabilities
   - Privacy by design violations

3. **Context Analysis**: How these violations relate to:
   - Overall application architecture
   - Data flow patterns
   - User privacy rights
   - Compliance requirements

Format your response as JSON:
{{
    "enhanced_violations": [
        {{
            "line_number": <line>,
            "enhanced_description": "<detailed explanation with context>",
            "risk_assessment": "<HIGH/MEDIUM/LOW>",
            "business_impact": "<specific business consequences>",
            "enhanced_fix": "<detailed code fix with explanation>",
            "regulatory_articles": ["<specific GDPR Article X>", "<CCPA Section Y>"],
            "related_concerns": ["<related privacy issue 1>", "<related privacy issue 2>"],
            "compliance_priority": "<IMMEDIATE/HIGH/MEDIUM/LOW>"
        }}
    ],
    "additional_violations": [
        {{
            "line_number": <line>,
            "violation_type": "<specific violation type>",
            "description": "<detailed description>",
            "severity": "<HIGH/MEDIUM/LOW>",
            "fix_suggestion": "<specific fix with code>",
            "regulation_reference": "<specific regulation>",
            "compliance_impact": "<HIGH/MEDIUM/LOW>"
        }}
    ],
    "context_analysis": {{
        "overall_risk_level": "<HIGH/MEDIUM/LOW>",
        "compliance_gaps": ["<gap 1>", "<gap 2>"],
        "architectural_concerns": ["<concern 1>", "<concern 2>"],
        "recommendations": ["<recommendation 1>", "<recommendation 2>"]
    }}
}}

Focus on actionable insights that help developers understand the full scope of privacy implications and implement effective fixes.
"""
        return prompt
    
    def _process_enhanced_ai_response(self, original_violations: List[ScanResult], ai_response: str, file_path: str) -> List[ScanResult]:
        """Process enhanced AI response and improve violations"""
        enhanced_results = []
        
        try:
            # Try to extract JSON from AI response
            ai_data = self._extract_json_from_response(ai_response)
            if not ai_data:
                self.log_activity("Failed to extract valid JSON from AI response - using original violations", "warning")
                return original_violations
            
            # Enhance existing violations with AI insights
            for violation in original_violations:
                enhanced_violation = self._find_enhancement(violation, ai_data.get('enhanced_violations', []))
                if enhanced_violation:
                    # Update violation with comprehensive AI insights
                    violation.description = enhanced_violation.get('enhanced_description', violation.description)
                    violation.fix_suggestion = enhanced_violation.get('enhanced_fix', violation.fix_suggestion)
                    
                    # Update regulation reference with specific articles
                    regulatory_articles = enhanced_violation.get('regulatory_articles', [])
                    if regulatory_articles:
                        violation.regulation_reference = ', '.join(regulatory_articles)
                    
                    # Update severity based on AI risk assessment
                    if enhanced_violation.get('risk_assessment'):
                        violation.severity = enhanced_violation['risk_assessment']
                    
                    # Add business impact and related concerns to description
                    business_impact = enhanced_violation.get('business_impact', '')
                    related_concerns = enhanced_violation.get('related_concerns', [])
                    if business_impact or related_concerns:
                        additional_info = []
                        if business_impact:
                            additional_info.append(f"Business Impact: {business_impact}")
                        if related_concerns:
                            additional_info.append(f"Related Concerns: {', '.join(related_concerns)}")
                        violation.description += f" | {' | '.join(additional_info)}"
                
                enhanced_results.append(violation)
            
            # Add new violations found by AI
            for new_violation in ai_data.get('additional_violations', []):
                enhanced_results.append(ScanResult(
                    file_path=file_path,
                    line_number=new_violation.get('line_number', 0),
                    violation_type=new_violation.get('violation_type', 'AIEnhancedViolation'),
                    description=new_violation.get('description', 'AI-detected privacy violation'),
                    severity=new_violation.get('severity', 'MEDIUM'),
                    fix_suggestion=new_violation.get('fix_suggestion', 'Review and fix privacy violation'),
                    regulation_reference=new_violation.get('regulation_reference', 'GDPR/CCPA'),
                    agent_id=self.agent_id,
                    timestamp=datetime.now(UTC)
                ))
            
        except Exception as e:
            self.log_activity(f"Error processing AI response: {str(e)} - using original violations", "warning")
            return original_violations
        
        return enhanced_results
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from AI response, handling various response formats"""
        try:
            # First, try to parse the response directly as JSON
            return json.loads(response)
        except json.JSONDecodeError:
            try:
                # Try to find JSON blocks in the response
                import re
                json_pattern = r'\{.*\}'
                matches = re.findall(json_pattern, response, re.DOTALL)
                
                for match in matches:
                    try:
                        return json.loads(match)
                    except json.JSONDecodeError:
                        continue
                
                # If no JSON found, return None
                return None
            except Exception:
                return None

    async def _generate_comprehensive_insights(self, original_results: List[ScanResult], enhanced_results: List[ScanResult]) -> Dict[str, Any]:
        """Generate comprehensive AI insights about the privacy analysis"""
        try:
            prompt = f"""
You are analyzing the results of a comprehensive privacy compliance scan.

Original violations found: {len(original_results)}
Enhanced violations after AI analysis: {len(enhanced_results)}

Violation types detected:
{self._get_violation_type_summary(enhanced_results)}

Please provide comprehensive insights including:

1. **Overall Assessment**: Summary of privacy posture
2. **Critical Issues**: Most urgent privacy concerns
3. **Compliance Gaps**: Missing privacy controls
4. **Risk Prioritization**: Which issues to address first
5. **Strategic Recommendations**: Long-term privacy improvements

Format as JSON:
{{
    "overall_assessment": {{
        "privacy_posture": "<EXCELLENT/GOOD/FAIR/POOR>",
        "compliance_status": "<COMPLIANT/PARTIALLY_COMPLIANT/NON_COMPLIANT>",
        "risk_level": "<HIGH/MEDIUM/LOW>"
    }},
    "critical_issues": [
        {{
            "issue": "<description>",
            "impact": "<business/legal/user impact>",
            "urgency": "<IMMEDIATE/HIGH/MEDIUM>"
        }}
    ],
    "compliance_gaps": [
        "<specific gap description>"
    ],
    "risk_prioritization": [
        {{
            "priority": "<1/2/3>",
            "violation_types": ["<types>"],
            "rationale": "<why this priority>"
        }}
    ],
    "strategic_recommendations": [
        {{
            "recommendation": "<description>",
            "timeline": "<short/medium/long term>",
            "impact": "<expected outcome>"
        }}
    ]
}}
"""
            
            ai_response = await self.get_gemini_analysis(prompt, {
                "original_count": len(original_results),
                "enhanced_count": len(enhanced_results),
                "violation_types": list(set([r.violation_type for r in enhanced_results]))
            })
            
            if ai_response:
                insights = self._extract_json_from_response(ai_response)
                if insights:
                    return insights
                else:
                    return {"error": "Failed to parse AI insights"}
            else:
                return {"error": "Failed to generate AI insights"}
                
        except Exception as e:
            self.log_activity(f"Error generating comprehensive insights: {str(e)}", "warning")
            return {"error": f"Insights generation failed: {str(e)}"}

    def _get_violation_type_summary(self, results: List[ScanResult]) -> str:
        """Get summary of violation types for AI analysis"""
        type_counts = {}
        for result in results:
            type_counts[result.violation_type] = type_counts.get(result.violation_type, 0) + 1
        
        return "\n".join([f"- {vtype}: {count}" for vtype, count in type_counts.items()])
    
    def _find_enhancement(self, violation: ScanResult, enhanced_violations: List[Dict]) -> Optional[Dict]:
        """Find AI enhancement for a specific violation"""
        for enhanced in enhanced_violations:
            if enhanced.get('line_number') == violation.line_number:
                return enhanced
        return None

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

    def _scan_result_to_dict(self, result: ScanResult) -> Dict[str, Any]:
        """Convert ScanResult to dictionary for event publishing"""
        return {
            "file_path": result.file_path,
            "line_number": result.line_number,
            "violation_type": result.violation_type,
            "description": result.description,
            "severity": result.severity,
            "fix_suggestion": result.fix_suggestion,
            "regulation_reference": result.regulation_reference,
            "agent_id": result.agent_id,
            "timestamp": result.timestamp.isoformat()
        }

    # Cloud Function trigger template (for reference)
    # def cloud_function_entrypoint(request):
    #     """
    #     Cloud Function HTTP trigger for GeminiAnalysisAgent.
    #     """
    #     # Parse request, call self.process(), return response
    #     pass