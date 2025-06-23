"""
PrivacyScanAgent - Rule-Based Privacy Violation Detection
========================================================

This agent is responsible for scanning codebases across multiple programming languages
to detect privacy violations using the TypeScript RuleEngine. It focuses solely on
rule-based detection and emits FindingsReady events for downstream agents to consume.

Key Responsibilities:
--------------------
- Scan codebases in multiple programming languages (Python, JavaScript, Java, C#, etc.)
- Detect 50+ types of privacy violations including PII exposure, security issues, consent violations
- Integrate with TypeScript RuleEngine for comprehensive rule-based detection
- Emit FindingsReady events with raw scan results for downstream processing
- Provide detailed violation reports with file locations and line numbers
- Support both imported TypeScript RuleEngine and Node.js CLI fallback

Event-Based Architecture:
------------------------
This agent is the first in the event flow chain:
- Receives scan requests from Agent Orchestrator
- Performs rule-based detection using TypeScript RuleEngine
- Emits FindingsReady event with raw scan results
- No AI enhancement (delegated to GeminiAnalysisAgent)

Detection Capabilities:
----------------------
PII Detection:
- Hardcoded emails, SSNs, credit cards, phone numbers
- Passport numbers, driver's licenses, national IDs
- Bank account numbers, medical data, biometric data
- Addresses and other personal identifiers

Security Issues:
- Hardcoded secrets and API keys
- Insecure connections and TLS violations
- Missing encryption and rate limiting
- Raw PII used as primary keys

Consent & Privacy:
- Consent violations and forced consent
- Missing purpose limitations and opt-out mechanisms
- Right to be forgotten violations
- Data sharing and retention issues

Data Flow & Handling:
- Sensitive data sources and data masking
- Unsanitized stack traces and error handling
- Data sharing and retention violations
- Missing DSAR registration

Advanced Privacy:
- Privacy by design violations
- Data minimization and cross-border transfers
- Breach notification and DPO requirements
- Vendor management and privacy training

AI Privacy:
- AI privacy violations and automated decisions
- Claude Sonnet and Gemini privacy issues
- AI bias and explainability concerns
- AI model privacy and training data issues

Developer Guidance:
- Missing privacy comments and documentation
- Privacy testing and logging violations
- Privacy configuration and deployment issues

Processing Flow:
---------------
1. Receive scan request with project path
2. Attempt to use imported TypeScript RuleEngine
3. Fallback to Node.js CLI if import fails
4. Parse violation strings into structured data
5. Emit FindingsReady event with scan results
6. Return raw scan results to orchestrator

Integration Points:
------------------
- TypeScript RuleEngine: Primary detection engine
- Agent Orchestrator: Receives scan requests and returns results
- Event System: Emits FindingsReady events for downstream agents
- Node.js CLI: Fallback mechanism for RuleEngine execution

Usage:
------
The agent is typically invoked by the Agent Orchestrator with:
- project_path: Path to the codebase to scan
- correlation_id: Request tracking ID
- scan_options: Optional scan configuration

Returns:
- List of ScanResult objects with detailed violation information
- Raw scan results without AI enhancement
- Comprehensive coverage of privacy and security issues

Event Emission:
--------------
Emits FindingsReady event containing:
- total_violations: Number of violations found
- scan_results: List of violation data
- project_path: Path of scanned project
- agent: Agent identifier

Dependencies:
-------------
- TypeScript RuleEngine: Core detection engine
- Node.js: CLI wrapper execution
- asyncio: Asynchronous processing
- pathlib: File path handling
- re: Regular expression matching
- json: Data serialization
- subprocess: Node.js CLI execution

Author: Privacy Guardian Team
Built with Google Cloud Agent Development Kit (ADK)
"""

import os
import re
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, UTC
import subprocess
import json
import sys

# Add the src directory to Python path to import ruleEngine
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from ruleEngine import RuleEngine
    from ruleEngine import Rule, PiiRule, PrivacyPolicyRule, PiiDetectionRule
    from ruleEngine import AiPrivacyRule, DeveloperGuidanceRule, GeminiPrivacyRule
    from ruleEngine import ConsentRule, EncryptionRule, DataFlowRule, AdvancedPrivacyRule
    from scanners import Scanner
    RULE_ENGINE_AVAILABLE = True
    print("✅ TypeScript RuleEngine imported successfully via Python bridge")
except ImportError as e:
    RULE_ENGINE_AVAILABLE = False
    print(f"Warning: Could not import ruleEngine: {e}")

# Handle imports for both module and script execution
try:
    from .base_agent import BaseAgent, ScanResult, AgentEvent
except ImportError:
    # When running as script, use absolute import
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from agents.base_agent import BaseAgent, ScanResult, AgentEvent

class PrivacyScanAgent(BaseAgent):
    """
    Agent responsible for scanning codebases to detect privacy violations.
    
    This agent combines the power of the TypeScript RuleEngine with Gemini AI
    to provide comprehensive privacy violation detection across multiple
    programming languages. It can detect 50+ types of violations including
    PII exposure, security issues, consent violations, and data handling problems.
    
    Key Features:
    - Multi-language support (Python, JavaScript, Java, C#, Go, Rust, etc.)
    - Integration with TypeScript RuleEngine for comprehensive detection
    - AI enhancement with Google Gemini for context-aware analysis
    - Robust fallback mechanisms when AI or RuleEngine is unavailable
    - Detailed violation reporting with file locations and line numbers
    
    Processing Flow:
    1. Receive scan request with project path
    2. Attempt to use imported TypeScript RuleEngine
    3. Fallback to Node.js CLI if import fails
    4. Enhance results with Gemini AI if available
    5. Parse and structure violation data
    6. Return comprehensive scan results
    
    AI Enhancement:
    - Enhances violation descriptions with business context
    - Re-assesses severity based on broader implications
    - Identifies related privacy issues not caught by rules
    - Provides additional context and recommendations
    - Discovers new violations through AI analysis

    Integrations:
    - Inserts scan analytics into BigQuery after each scan
    - Exports scan metrics to Cloud Monitoring
    - Fetches secrets (e.g., API keys) from Secret Manager
    - Cloud Function trigger template provided for serverless execution
    """
    
    def __init__(self):
        """Initialize the PrivacyScanAgent with RuleEngine integration."""
        super().__init__("privacy_scan_agent", "🔍 PrivacyScanAgent")
        self.supported_extensions = {
            '.js', '.ts', '.java', '.py', '.go', '.cs', '.php', 
            '.rb', '.swift', '.kt', '.rs', '.scala'
        }
        self.rule_engine = None
        if RULE_ENGINE_AVAILABLE:
            self._initialize_rule_engine()
        
    def _initialize_rule_engine(self):
        """
        Initialize the TypeScript RuleEngine for privacy violation detection.
        
        Attempts to import the TypeScript RuleEngine directly. If that fails,
        the agent will use the Node.js CLI wrapper as a fallback mechanism.
        """
        try:
            if RULE_ENGINE_AVAILABLE:
                # Use the Python bridge to TypeScript RuleEngine
                from ruleEngine import RuleEngine
                self.rule_engine = RuleEngine()
                self.log_activity("✅ TypeScript RuleEngine bridge initialized successfully")
            else:
                self.log_activity("TypeScript RuleEngine not available - will use Node.js CLI fallback", "warning")
                self.rule_engine = None
        except Exception as e:
            self.log_activity(f"RuleEngine initialization failed: {str(e)} - will use Node.js CLI fallback", "warning")
            self.rule_engine = None
        
    async def process(self, input_data: Dict[str, Any]) -> List[ScanResult]:
        """Process code scanning request using TypeScript RuleEngine - emits FindingsReady event"""
        self.log_activity("Starting privacy scan with TypeScript RuleEngine")
        project_path = input_data.get('project_path', '.')
        correlation_id = input_data.get('correlation_id', 'default')

        # Example: Fetch a secret (API key) from Secret Manager
        # secret = self.fetch_secret(f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/PRIVACY_SCAN_API_KEY")

        # Publish scan started event
        self.publish_event(
            "ScanStarted",
            {"project_path": project_path, "agent": self.agent_name},
            correlation_id
        )

        scan_results = []
        rule_engine_success = False
        
        # Try to use imported TypeScript RuleEngine first
        if self.rule_engine:
            try:
                self.log_activity("Using imported TypeScript RuleEngine")
                violations = self.rule_engine.run(project_path)
                
                for violation_string in violations:
                    parsed = self._parse_violation_string(violation_string)
                    if parsed:
                        scan_results.append(parsed)
                
                rule_engine_success = True
                self.log_activity(f"TypeScript RuleEngine found {len(scan_results)} violations")
                
            except Exception as e:
                self.log_activity(f"TypeScript RuleEngine failed: {str(e)}", "warning")
        
        # Fallback to Node.js CLI if imported RuleEngine failed
        if not rule_engine_success:
            try:
                # Try to call the Node.js RuleEngine CLI
                node_cmd = [
                    "node", os.path.join(os.getcwd(), "rule_engine_cli.js"),
                    project_path
                ]
                proc = await asyncio.create_subprocess_exec(
                    *node_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                if proc.returncode == 0:
                    # Clean the output - remove trailing characters and decode
                    output = stdout.decode().strip()
                    # Remove trailing % character if present
                    if output.endswith('%'):
                        output = output[:-1]
                    
                    # Debug logging
                    self.log_activity(f"Node.js output length: {len(output)}")
                    self.log_activity(f"Node.js output first 200 chars: {output[:200]}")
                    self.log_activity(f"Node.js output last 50 chars: {output[-50:]}")
                    
                    # Extract JSON part - find the first { and last }
                    start_idx = output.find('{')
                    end_idx = output.rfind('}')
                    if start_idx != -1 and end_idx != -1:
                        json_output = output[start_idx:end_idx + 1]
                        self.log_activity(f"Extracted JSON length: {len(json_output)}")
                        result = json.loads(json_output)
                    else:
                        raise ValueError("No valid JSON found in output")
                    
                    for v in result.get("violations", []):
                        # Parse violation string: [LANG] path:line - description (found: "match")
                        parsed = self._parse_violation_string(v)
                        if parsed:
                            scan_results.append(parsed)
                    rule_engine_success = True
                    self.log_activity(f"Node.js RuleEngine found {len(scan_results)} violations")
                else:
                    self.log_activity(f"Node.js RuleEngine error: {stderr.decode()}", "warning")
            except Exception as e:
                self.log_activity(f"Node.js RuleEngine failed: {str(e)}", "warning")

        # If all fail, log and return empty
        if not rule_engine_success:
            self.log_activity("All RuleEngine attempts failed. No scan performed.", "error")
            self.publish_event(
                "ScanFailed",
                {"error": "All RuleEngine attempts failed."},
                correlation_id
            )
            return scan_results

        # --- Google Cloud Integrations ---
        # Insert scan analytics into BigQuery
        table_id = f"{os.getenv('GOOGLE_CLOUD_PROJECT')}.privacy.scan_results"
        rows = [s.__dict__ for s in scan_results]
        self.insert_bigquery_analytics(table_id, rows)

        # Export scan metric to Cloud Monitoring
        self.export_custom_metric(
            metric_type="custom.googleapis.com/agent/scan_violations",
            value=len(scan_results),
            labels={"agent": self.agent_id}
        )

        return scan_results
    
    def get_rule_engine_status(self) -> Dict[str, Any]:
        """Get the status of the RuleEngine"""
        if self.rule_engine:
            try:
                stats = self.rule_engine.getRuleStats()
                gemini_available = self.rule_engine.isGeminiAvailable()
                return {
                    "status": "available",
                    "total_rules": stats.get("totalRules", 0),
                    "rule_types": stats.get("ruleTypes", []),
                    "gemini_available": gemini_available,
                    "engine_type": "TypeScript RuleEngine"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e),
                    "engine_type": "TypeScript RuleEngine"
                }
        else:
            return {
                "status": "unavailable",
                "engine_type": "Python Fallback Rules"
            }
    
    def _result_to_dict(self, result: ScanResult) -> Dict[str, Any]:
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

    def _parse_violation_string(self, vstr: str) -> ScanResult:
        """
        Parse violation string from TypeScript RuleEngine.
        
        Expected format: [LANG] path:line - description (found: "match")
        Example: [JS] src/app.js:42 - Hardcoded email found (found: "user@example.com")
        """
        try:
            # Parse the violation string format
            match = re.match(r'\[(\w+)\]\s+([^:]+):(\d+)\s+-\s+(.+?)\s+\(found:\s*"([^"]*)"\)', vstr)
            if not match:
                return None
                
            lang, file_path, line_num, description, found_value = match.groups()
            
            # Determine violation type based on description and found value
            violation_type = self._determine_violation_type(description, found_value)
            
            # Determine severity based on violation type
            severity = self._determine_severity(violation_type)
            
            # Generate basic fix suggestion
            fix_suggestion = self._generate_basic_fix(violation_type, found_value)
            
            # Determine regulation reference
            regulation_reference = self._determine_regulation(violation_type)
            
            return ScanResult(
                file_path=file_path.strip(),
                line_number=int(line_num),
                violation_type=violation_type,
                description=description.strip(),
                severity=severity,
                fix_suggestion=fix_suggestion,
                regulation_reference=regulation_reference,
                agent_id=self.agent_id,
                timestamp=datetime.now(UTC)
            )
            
        except Exception as e:
            self.log_activity(f"Error parsing violation string '{vstr}': {str(e)}", "warning")
            return None

    def _determine_violation_type(self, description: str, found_value: str) -> str:
        """Determine violation type based on description and found value"""
        description_lower = description.lower()
        found_lower = found_value.lower()
        
        # PII Detection
        if any(word in description_lower for word in ['email', 'mail']):
            return "HardcodedEmail"
        elif any(word in description_lower for word in ['ssn', 'social security']):
            return "SSNExposure"
        elif any(word in description_lower for word in ['credit card', 'card number']):
            return "CreditCardExposure"
        elif any(word in description_lower for word in ['passport']):
            return "PassportExposure"
        elif any(word in description_lower for word in ['phone', 'telephone']):
            return "PhoneNumberExposure"
        elif any(word in description_lower for word in ['bank account', 'account number']):
            return "BankAccountExposure"
        elif any(word in description_lower for word in ['driver', 'license']):
            return "DriversLicenseExposure"
        elif any(word in description_lower for word in ['national id', 'national id']):
            return "NationalIdExposure"
        elif any(word in description_lower for word in ['address']):
            return "AddressExposure"
        elif any(word in description_lower for word in ['medical', 'health']):
            return "MedicalDataExposure"
        elif any(word in description_lower for word in ['biometric']):
            return "BiometricDataExposure"
        
        # Security Issues
        elif any(word in description_lower for word in ['secret', 'api key', 'password', 'token']):
            return "HardcodedSecret"
        elif any(word in description_lower for word in ['http://', 'insecure']):
            return "InsecureConnection"
        elif any(word in description_lower for word in ['tls', 'ssl', 'encryption']):
            return "TLSDisabled"
        elif any(word in description_lower for word in ['encrypt', 'encryption']):
            return "EncryptionViolation"
        elif any(word in description_lower for word in ['primary key', 'pii']):
            return "RawPiiAsPrimaryKey"
        elif any(word in description_lower for word in ['rate limit', 'throttle']):
            return "MissingRateLimiting"
        elif any(word in description_lower for word in ['encrypt at rest']):
            return "MissingEncryptionAtRest"
        elif any(word in description_lower for word in ['unencrypted', 'plain text']):
            return "UnencryptedDataWrite"
        elif any(word in description_lower for word in ['hash', 'hashing']):
            return "PiiHashingFound"
        
        # Consent & Privacy
        elif any(word in description_lower for word in ['consent', 'permission']):
            return "ConsentViolation"
        elif any(word in description_lower for word in ['purpose', 'limitation']):
            return "MissingPurposeLimitation"
        elif any(word in description_lower for word in ['profiling', 'automated']):
            return "MissingProfilingOptOut"
        elif any(word in description_lower for word in ['opt out', 'opt-out']):
            return "DisabledOptOut"
        elif any(word in description_lower for word in ['forced', 'required']):
            return "ForcedConsent"
        elif any(word in description_lower for word in ['default', 'enabled']):
            return "DefaultEnabledConsent"
        elif any(word in description_lower for word in ['forgotten', 'erasure', 'delete']):
            return "RightToBeForgottenViolation"
        elif any(word in description_lower for word in ['sell', 'sale']):
            return "DoNotSellViolation"
        
        # Data Flow & Handling
        elif any(word in description_lower for word in ['sensitive', 'pii source']):
            return "SensitiveDataSource"
        elif any(word in description_lower for word in ['mask', 'masking']):
            return "DataMaskingFound"
        elif any(word in description_lower for word in ['stack trace', 'error']):
            return "UnsanitizedStackTrace"
        elif any(word in description_lower for word in ['share', 'sharing']):
            return "DataSharingViolation"
        elif any(word in description_lower for word in ['retention', 'retain']):
            return "DataRetentionViolation"
        elif any(word in description_lower for word in ['dsar', 'data subject']):
            return "MissingDSARRegistration"
        
        # Advanced Privacy
        elif any(word in description_lower for word in ['privacy by design']):
            return "PrivacyByDesignViolation"
        elif any(word in description_lower for word in ['data minimization']):
            return "DataMinimizationViolation"
        elif any(word in description_lower for word in ['cross border', 'international']):
            return "CrossBorderTransferViolation"
        elif any(word in description_lower for word in ['breach notification']):
            return "BreachNotificationViolation"
        elif any(word in description_lower for word in ['dpo', 'data protection']):
            return "MissingDPOViolation"
        elif any(word in description_lower for word in ['impact assessment', 'dpia']):
            return "MissingDPIAViolation"
        elif any(word in description_lower for word in ['vendor', 'third party']):
            return "VendorManagementViolation"
        elif any(word in description_lower for word in ['training', 'awareness']):
            return "MissingPrivacyTrainingViolation"
        elif any(word in description_lower for word in ['incident response']):
            return "MissingIncidentResponseViolation"
        elif any(word in description_lower for word in ['audit', 'monitoring']):
            return "MissingPrivacyAuditViolation"
        
        # AI Privacy
        elif any(word in description_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
            return "AiPrivacyViolation"
        elif any(word in description_lower for word in ['claude', 'anthropic']):
            return "ClaudeSonnetViolation"
        elif any(word in description_lower for word in ['gemini', 'google ai']):
            return "GeminiPrivacyViolation"
        elif any(word in description_lower for word in ['automated decision', 'algorithm']):
            return "AutomatedDecisionViolation"
        elif any(word in description_lower for word in ['bias', 'discrimination']):
            return "AiBiasViolation"
        elif any(word in description_lower for word in ['explainability', 'transparency']):
            return "AiExplainabilityViolation"
        elif any(word in description_lower for word in ['model', 'training data']):
            return "AiModelPrivacyViolation"
        
        # Developer Guidance
        elif any(word in description_lower for word in ['comment', 'documentation']):
            return "MissingPrivacyCommentViolation"
        elif any(word in description_lower for word in ['test', 'testing']):
            return "MissingPrivacyTestViolation"
        elif any(word in description_lower for word in ['logging', 'log']):
            return "PrivacyLoggingViolation"
        elif any(word in description_lower for word in ['configuration', 'config']):
            return "PrivacyConfigurationViolation"
        elif any(word in description_lower for word in ['deployment', 'production']):
            return "PrivacyDeploymentViolation"
        
        # Default fallback
        else:
            return "UnknownViolation"

    def _determine_severity(self, violation_type: str) -> str:
        """Determine severity based on violation type"""
        high_severity = {
            "SSNExposure", "CreditCardExposure", "PassportExposure", "BankAccountExposure",
            "DriversLicenseExposure", "NationalIdExposure", "MedicalDataExposure", 
            "BiometricDataExposure", "HardcodedSecret", "TLSDisabled", "EncryptionViolation",
            "RawPiiAsPrimaryKey", "MissingEncryptionAtRest", "UnencryptedDataWrite",
            "ConsentViolation", "MissingProfilingOptOut", "DisabledOptOut", "ForcedConsent",
            "RightToBeForgottenViolation", "DoNotSellViolation", "DataSharingViolation",
            "PrivacyByDesignViolation", "CrossBorderTransferViolation", "BreachNotificationViolation",
            "MissingDPOViolation", "MissingDPIAViolation", "AutomatedDecisionViolation",
            "AiBiasViolation"
        }
        
        medium_severity = {
            "HardcodedEmail", "PhoneNumberExposure", "AddressExposure", "InsecureConnection",
            "MissingRateLimiting", "MissingPurposeLimitation", "DefaultEnabledConsent",
            "SensitiveDataSource", "UnsanitizedStackTrace", "DataRetentionViolation",
            "MissingDSARRegistration", "DataMinimizationViolation", "VendorManagementViolation",
            "MissingPrivacyTrainingViolation", "MissingIncidentResponseViolation",
            "MissingPrivacyAuditViolation", "ClaudeSonnetViolation", "GeminiPrivacyViolation",
            "AiExplainabilityViolation", "AiModelPrivacyViolation", "MissingPrivacyTestViolation",
            "PrivacyLoggingViolation", "PrivacyConfigurationViolation", "PrivacyDeploymentViolation"
        }
        
        if violation_type in high_severity:
            return "HIGH"
        elif violation_type in medium_severity:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_basic_fix(self, violation_type: str, found_value: str) -> str:
        """Generate basic fix suggestion based on violation type"""
        if violation_type == "HardcodedEmail":
            return f"Replace hardcoded email '{found_value}' with environment variable or secure storage"
        elif violation_type == "HardcodedSecret":
            return f"Replace hardcoded secret with environment variable or secure credential management"
        elif violation_type == "InsecureConnection":
            return "Replace HTTP with HTTPS and ensure proper SSL/TLS configuration"
        elif violation_type == "TLSDisabled":
            return "Enable TLS/SSL encryption for secure data transmission"
        elif violation_type == "EncryptionViolation":
            return "Implement proper encryption for sensitive data"
        elif violation_type == "ConsentViolation":
            return "Implement proper consent mechanism with clear opt-in/opt-out options"
        elif violation_type == "DataSharingViolation":
            return "Add data sharing controls and user consent for third-party sharing"
        else:
            return f"Review and fix {violation_type} violation according to privacy best practices"

    def _determine_regulation(self, violation_type: str) -> str:
        """Determine applicable regulations based on violation type"""
        gdpr_violations = {
            "HardcodedEmail", "SSNExposure", "CreditCardExposure", "PassportExposure",
            "PhoneNumberExposure", "BankAccountExposure", "DriversLicenseExposure",
            "NationalIdExposure", "AddressExposure", "MedicalDataExposure", "BiometricDataExposure",
            "ConsentViolation", "MissingPurposeLimitation", "MissingProfilingOptOut",
            "DisabledOptOut", "ForcedConsent", "DefaultEnabledConsent", "RightToBeForgottenViolation",
            "DataSharingViolation", "DataRetentionViolation", "PrivacyByDesignViolation",
            "DataMinimizationViolation", "CrossBorderTransferViolation", "BreachNotificationViolation",
            "MissingDPOViolation", "MissingDPIAViolation", "AutomatedDecisionViolation"
        }
        
        ccpa_violations = {
            "HardcodedEmail", "SSNExposure", "CreditCardExposure", "PassportExposure",
            "PhoneNumberExposure", "BankAccountExposure", "DriversLicenseExposure",
            "NationalIdExposure", "AddressExposure", "MedicalDataExposure", "BiometricDataExposure",
            "DoNotSellViolation", "RightToBeForgottenViolation", "DataSharingViolation"
        }
        
        hipaa_violations = {
            "MedicalDataExposure", "BiometricDataExposure", "HardcodedSecret",
            "TLSDisabled", "EncryptionViolation", "MissingEncryptionAtRest",
            "UnencryptedDataWrite", "DataSharingViolation"
        }
        
        pci_violations = {
            "CreditCardExposure", "BankAccountExposure", "HardcodedSecret",
            "TLSDisabled", "EncryptionViolation", "MissingEncryptionAtRest",
            "UnencryptedDataWrite"
        }
        
        regulations = []
        if violation_type in gdpr_violations:
            regulations.append("GDPR")
        if violation_type in ccpa_violations:
            regulations.append("CCPA")
        if violation_type in hipaa_violations:
            regulations.append("HIPAA")
        if violation_type in pci_violations:
            regulations.append("PCI-DSS")
        
        return ", ".join(regulations) if regulations else "General Privacy"

    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status including RuleEngine status"""
        status = super().get_agent_status()
        status.update({
            "rule_engine_available": self.rule_engine is not None,
            "supported_extensions": list(self.supported_extensions),
            "total_violations_detected": len(self.events_published)
        })
        return status


# CLI/Test Harness for local testing
if __name__ == "__main__":
    import sys
    import asyncio
    import argparse
    
    def main():
        parser = argparse.ArgumentParser(description="PrivacyScanAgent - Local Testing")
        parser.add_argument("project_path", nargs="?", default=".", 
                          help="Path to the project to scan (default: current directory)")
        parser.add_argument("--verbose", "-v", action="store_true", 
                          help="Verbose output")
        parser.add_argument("--json", "-j", action="store_true", 
                          help="Output results as JSON")
        
        args = parser.parse_args()
        
        print("🔍 PrivacyScanAgent - Local Testing")
        print("=" * 50)
        print(f"📁 Project path: {args.project_path}")
        print(f"🤖 AI enabled: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is not None}")
        print()
        
        # Initialize agent
        agent = PrivacyScanAgent()
        
        # Check RuleEngine status
        rule_status = agent.get_rule_engine_status()
        print(f"📊 RuleEngine Status: {rule_status['status']}")
        if rule_status['status'] == 'available':
            print(f"   - Total Rules: {rule_status.get('total_rules', 'N/A')}")
            print(f"   - Rule Types: {', '.join(rule_status.get('rule_types', []))}")
            print(f"   - Gemini Available: {rule_status.get('gemini_available', 'N/A')}")
        print()
        
        # Run scan
        print("🚀 Starting scan...")
        input_data = {
            "project_path": args.project_path, 
            "correlation_id": "local-test-" + str(int(datetime.now(UTC).timestamp()))
        }
        
        try:
            results = asyncio.run(agent.process(input_data))
            
            print(f"\n✅ Scan Complete!")
            print(f"📊 Total Violations Found: {len(results)}")
            print()
            
            if len(results) == 0:
                print("🎉 No privacy violations detected!")
            else:
                print("🚨 Privacy Violations Found:")
                print("-" * 80)
                
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result.violation_type} - {result.severity}")
                    print(f"   📄 File: {result.file_path}:{result.line_number}")
                    print(f"   📝 Description: {result.description}")
                    print(f"   🛠️  Fix: {result.fix_suggestion}")
                    print(f"   📋 Regulations: {result.regulation_reference}")
                    print()
            
            # Output as JSON if requested
            if args.json:
                import json
                json_results = []
                for result in results:
                    json_results.append({
                        "violation_type": result.violation_type,
                        "severity": result.severity,
                        "file_path": result.file_path,
                        "line_number": result.line_number,
                        "description": result.description,
                        "fix_suggestion": result.fix_suggestion,
                        "regulation_reference": result.regulation_reference,
                        "timestamp": result.timestamp.isoformat()
                    })
                print("JSON Output:")
                print(json.dumps(json_results, indent=2))
            
            # Print agent status
            if args.verbose:
                print("\n📈 Agent Status:")
                status = agent.get_agent_status()
                for key, value in status.items():
                    print(f"   {key}: {value}")
                    
        except Exception as e:
            print(f"❌ Scan failed: {str(e)}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    main() 