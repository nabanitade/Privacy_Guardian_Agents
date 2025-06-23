"""
ComplianceAgent - Regulatory Compliance Analysis and Mapping
============================================================

This agent is responsible for analyzing privacy violations against regulatory frameworks
and providing compliance scoring. It listens for AIEnhancedFindings events from
GeminiAnalysisAgent and emits ComplianceAnalysisCompleted events for downstream agents.

Key Responsibilities:
--------------------
- Listen for AIEnhancedFindings events from GeminiAnalysisAgent
- Map privacy violations to regulatory frameworks (GDPR, CCPA, HIPAA, PCI-DSS)
- Calculate compliance scores and risk assessments
- Provide detailed regulatory analysis and gap identification
- Generate compliance recommendations and action items
- Emit ComplianceAnalysisCompleted events with analysis results

Event-Based Architecture:
------------------------
This agent is the third in the event flow chain:
- Listens for AIEnhancedFindings events from GeminiAnalysisAgent
- Performs regulatory compliance analysis
- Emits ComplianceAnalysisCompleted events with analysis results
- Provides compliance scoring for downstream processing

Regulatory Frameworks Supported:
-------------------------------
GDPR (General Data Protection Regulation):
- Data processing principles and legal basis
- Individual rights (access, rectification, erasure, portability)
- Consent requirements and data minimization
- Cross-border data transfers and breach notification
- Data Protection Officer (DPO) requirements

CCPA (California Consumer Privacy Act):
- Consumer rights and disclosure requirements
- Data sale opt-out mechanisms
- Service provider restrictions
- Financial incentive programs
- Right to know and deletion requests

HIPAA (Health Insurance Portability and Accountability Act):
- Protected Health Information (PHI) safeguards
- Administrative, physical, and technical safeguards
- Privacy rule compliance and patient rights
- Security rule implementation
- Breach notification requirements

PCI-DSS (Payment Card Industry Data Security Standard):
- Cardholder data protection requirements
- Network security and access control
- Vulnerability management and monitoring
- Information security policy
- Regular security testing and assessment

Compliance Analysis Capabilities:
-------------------------------
Violation Mapping:
- Maps each violation to applicable regulations
- Identifies specific regulatory requirements violated
- Provides detailed compliance gap analysis
- Assesses severity of regulatory violations

Compliance Scoring:
- Calculates overall compliance score (0-100)
- Provides regulation-specific compliance percentages
- Identifies critical compliance gaps
- Prioritizes compliance improvements

Risk Assessment:
- Evaluates regulatory risk levels
- Assesses potential fines and penalties
- Identifies reputational and legal risks
- Provides risk mitigation strategies

Processing Flow:
---------------
1. Listen for AIEnhancedFindings event from GeminiAnalysisAgent
2. Convert enhanced results to ScanResult objects if needed
3. Map violations to regulatory frameworks
4. Calculate compliance scores and risk assessments
5. Generate compliance recommendations
6. Emit ComplianceAnalysisCompleted event with analysis results

AI Integration:
--------------
When Gemini AI is available:
- Enhances compliance analysis with AI insights
- Provides context-aware regulatory interpretation
- Identifies emerging compliance trends
- Generates strategic compliance recommendations

Fallback Mechanisms:
-------------------
- Uses hardcoded regulatory mapping when AI is unavailable
- Maintains comprehensive compliance coverage
- Provides reliable compliance scoring and analysis

Integration Points:
------------------
- GeminiAnalysisAgent: Receives AIEnhancedFindings events
- Google Gemini AI: Enhanced compliance analysis
- FixSuggestionAgent: Emits ComplianceAnalysisCompleted for fix suggestions
- Event System: Listens for and emits events

Usage:
------
The agent is typically invoked by the Agent Orchestrator after GeminiAnalysisAgent:
- enhanced_results: AI-enhanced results from GeminiAnalysisAgent
- correlation_id: Request tracking ID
- compliance_options: Optional compliance configuration

Returns:
- Comprehensive compliance analysis report
- Regulatory mapping and compliance scores
- Risk assessment and recommendations

Event Communication:
-------------------
Listens for:
- AIEnhancedFindings: Enhanced results from GeminiAnalysisAgent

Emits:
- ComplianceAnalysisCompleted: Compliance analysis results
- ComplianceAnalysisStarted: When analysis begins

Dependencies:
-------------
- Google Gemini AI: Enhanced compliance analysis
- GeminiAnalysisAgent: Source of AIEnhancedFindings events
- asyncio: Asynchronous processing
- json: Data serialization and parsing
- datetime: Timestamp management
- typing: Type hints and data structures

Author: Privacy Guardian Team
Built with Google Cloud Agent Development Kit (ADK)
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
import json
import sys

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from .base_agent import BaseAgent, ScanResult, AgentEvent

class ComplianceAgent(BaseAgent):
    """
    Agent responsible for regulatory compliance mapping and severity classification.
    
    This agent analyzes privacy violations and maps them to specific regulatory
    requirements, providing comprehensive compliance analysis for GDPR, CCPA,
    HIPAA, PCI-DSS, and other privacy regulations. It combines hardcoded
    regulation mappings with AI-enhanced insights when Gemini is available.
    
    Key Features:
    - Comprehensive regulatory mapping for 50+ violation types
    - AI-enhanced compliance analysis with business impact assessment
    - Risk quantification and strategic recommendations
    - Implementation timeline and resource planning
    - Robust fallback to hardcoded rules when AI is unavailable
    
    Processing Flow:
    1. Receive scan results from PrivacyScanAgent
    2. Map each violation to applicable regulations
    3. Calculate compliance scores and risk assessments
    4. Generate strategic recommendations
    5. Provide implementation timeline and action plans
    
    AI Enhancement:
    - Dynamic compliance assessment based on business context
    - Enhanced risk analysis with financial and reputational impact
    - Strategic compliance planning with resource requirements
    - Implementation timeline optimization
    - Business impact quantification

    Integrations:
    - Inserts compliance analytics into BigQuery after analysis
    - Exports compliance metrics to Cloud Monitoring
    - Fetches secrets (e.g., compliance config) from Secret Manager
    - Cloud Function trigger template provided for serverless execution
    """
    
    def __init__(self):
        """Initialize the ComplianceAgent with comprehensive regulation mappings."""
        super().__init__("compliance_agent", "🧑‍⚖️ ComplianceAgent")
        self.regulation_mappings = self._initialize_regulation_mappings()
        
    def _initialize_regulation_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive regulation mappings for all 50+ violation types"""
        return {
            # PII Detection Types
            "HardcodedEmail": {
                "gdpr_articles": ["Article 4 (Definitions)", "Article 5 (Principles)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "hipaa": ["45 CFR 164.514 (De-identification)"],
                "severity_factors": ["data_exposure", "identifiability"],
                "compliance_impact": "MEDIUM"
            },
            "SSNExposure": {
                "gdpr_articles": ["Article 9 (Special Categories)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.514 (De-identification)", "45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["high_identifiability", "financial_risk", "identity_theft"],
                "compliance_impact": "HIGH"
            },
            "CreditCardExposure": {
                "gdpr_articles": ["Article 32 (Security)", "Article 34 (Data Breach Communication)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "pci_dss": ["Requirement 3 (Protect stored cardholder data)", "Requirement 4 (Encrypt transmission)"],
                "severity_factors": ["financial_risk", "fraud_potential", "pci_compliance"],
                "compliance_impact": "HIGH"
            },
            "PassportExposure": {
                "gdpr_articles": ["Article 9 (Special Categories)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.150 (Civil Action)"],
                "severity_factors": ["high_identifiability", "identity_theft", "national_security"],
                "compliance_impact": "HIGH"
            },
            "PhoneNumberExposure": {
                "gdpr_articles": ["Article 4 (Definitions)", "Article 5 (Principles)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_exposure", "identifiability"],
                "compliance_impact": "MEDIUM"
            },
            "BankAccountExposure": {
                "gdpr_articles": ["Article 9 (Special Categories)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.150 (Civil Action)"],
                "pci_dss": ["Requirement 3 (Protect stored cardholder data)"],
                "severity_factors": ["financial_risk", "fraud_potential"],
                "compliance_impact": "HIGH"
            },
            "DriversLicenseExposure": {
                "gdpr_articles": ["Article 9 (Special Categories)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.150 (Civil Action)"],
                "severity_factors": ["high_identifiability", "identity_theft"],
                "compliance_impact": "HIGH"
            },
            "NationalIdExposure": {
                "gdpr_articles": ["Article 9 (Special Categories)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.150 (Civil Action)"],
                "severity_factors": ["high_identifiability", "identity_theft", "national_security"],
                "compliance_impact": "HIGH"
            },
            "AddressExposure": {
                "gdpr_articles": ["Article 4 (Definitions)", "Article 5 (Principles)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_exposure", "identifiability"],
                "compliance_impact": "MEDIUM"
            },
            "MedicalDataExposure": {
                "gdpr_articles": ["Article 9 (Special Categories)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.514 (De-identification)", "45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["high_identifiability", "medical_privacy", "health_risk"],
                "compliance_impact": "HIGH"
            },
            "BiometricDataExposure": {
                "gdpr_articles": ["Article 9 (Special Categories)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.150 (Civil Action)"],
                "severity_factors": ["high_identifiability", "biometric_privacy", "irreversible"],
                "compliance_impact": "HIGH"
            },
            "HardcodedSecret": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["security_breach", "unauthorized_access"],
                "compliance_impact": "HIGH"
            },
            
            # Security & Encryption Types
            "InsecureConnection": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["data_interception", "man_in_middle"],
                "compliance_impact": "MEDIUM"
            },
            "TLSDisabled": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["data_interception", "man_in_middle", "encryption_required"],
                "compliance_impact": "HIGH"
            },
            "EncryptionViolation": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["data_protection", "breach_impact"],
                "compliance_impact": "HIGH"
            },
            "RawPiiAsPrimaryKey": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "severity_factors": ["data_protection", "identifiability"],
                "compliance_impact": "HIGH"
            },
            "MissingRateLimiting": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "severity_factors": ["security_breach", "abuse_potential"],
                "compliance_impact": "MEDIUM"
            },
            "MissingEncryptionAtRest": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["data_protection", "breach_impact"],
                "compliance_impact": "HIGH"
            },
            "UnencryptedDataWrite": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["data_protection", "breach_impact"],
                "compliance_impact": "HIGH"
            },
            "PiiHashingFound": {
                "gdpr_articles": ["Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["good_practice"],
                "compliance_impact": "LOW"
            },
            
            # Consent & Privacy Policy Types
            "ConsentViolation": {
                "gdpr_articles": ["Article 7 (Conditions for consent)", "Article 6 (Lawfulness)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)", "Section 1798.135 (Methods of submitting requests)"],
                "hipaa": ["45 CFR 164.508 (Uses and disclosures for which an authorization is required)"],
                "severity_factors": ["consent_requirement", "legal_basis"],
                "compliance_impact": "HIGH"
            },
            "MissingPurposeLimitation": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 6 (Lawfulness)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["purpose_limitation", "legal_basis"],
                "compliance_impact": "MEDIUM"
            },
            "MissingProfilingOptOut": {
                "gdpr_articles": ["Article 22 (Automated individual decision-making)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)"],
                "severity_factors": ["automated_decision", "user_rights"],
                "compliance_impact": "HIGH"
            },
            "DisabledOptOut": {
                "gdpr_articles": ["Article 7 (Conditions for consent)", "Article 21 (Right to object)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)"],
                "severity_factors": ["user_rights", "consent_requirement"],
                "compliance_impact": "HIGH"
            },
            "ForcedConsent": {
                "gdpr_articles": ["Article 7 (Conditions for consent)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)"],
                "severity_factors": ["consent_requirement", "user_autonomy"],
                "compliance_impact": "HIGH"
            },
            "DefaultEnabledConsent": {
                "gdpr_articles": ["Article 7 (Conditions for consent)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)"],
                "severity_factors": ["consent_requirement", "opt_in_requirement"],
                "compliance_impact": "MEDIUM"
            },
            "RightToBeForgottenViolation": {
                "gdpr_articles": ["Article 17 (Right to erasure)"],
                "ccpa_sections": ["Section 1798.105 (Right to deletion)"],
                "severity_factors": ["user_rights", "data_deletion"],
                "compliance_impact": "HIGH"
            },
            "DoNotSellViolation": {
                "gdpr_articles": ["Article 21 (Right to object)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)"],
                "severity_factors": ["user_rights", "data_sales"],
                "compliance_impact": "HIGH"
            },
            
            # Data Flow & Handling Types
            "SensitiveDataSource": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_flow", "privacy_by_design"],
                "compliance_impact": "MEDIUM"
            },
            "DataMaskingFound": {
                "gdpr_articles": ["Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["good_practice"],
                "compliance_impact": "LOW"
            },
            "UnsanitizedStackTrace": {
                "gdpr_articles": ["Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "severity_factors": ["data_exposure", "debugging_info"],
                "compliance_impact": "MEDIUM"
            },
            "DataSharingViolation": {
                "gdpr_articles": ["Article 28 (Processor)", "Article 44 (General principle for transfers)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.115 (Right to know)"],
                "hipaa": ["45 CFR 164.308 (Administrative safeguards)", "45 CFR 164.314 (Business associate contracts)"],
                "severity_factors": ["third_party_risk", "data_transfer"],
                "compliance_impact": "HIGH"
            },
            "DataRetentionViolation": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 17 (Right to erasure)"],
                "ccpa_sections": ["Section 1798.105 (Right to deletion)"],
                "hipaa": ["45 CFR 164.316 (Policies and procedures)"],
                "severity_factors": ["storage_duration", "purpose_limitation"],
                "compliance_impact": "MEDIUM"
            },
            "MissingDSARRegistration": {
                "gdpr_articles": ["Article 15-22 (Data Subject Rights)"],
                "ccpa_sections": ["Section 1798.100 (Consumer rights)"],
                "severity_factors": ["user_rights", "compliance_tracking"],
                "compliance_impact": "MEDIUM"
            },
            "LoggingViolation": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "hipaa": ["45 CFR 164.312 (Technical Safeguards)"],
                "severity_factors": ["data_exposure", "audit_trail"],
                "compliance_impact": "MEDIUM"
            },
            "ThirdPartyDataSharing": {
                "gdpr_articles": ["Article 28 (Processor)", "Article 44 (General principle for transfers)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)", "Section 1798.115 (Right to know)"],
                "severity_factors": ["third_party_risk", "data_transfer"],
                "compliance_impact": "HIGH"
            },
            "ApprovedEndpointsFound": {
                "gdpr_articles": ["Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["good_practice"],
                "compliance_impact": "LOW"
            },
            "RetentionTimerFound": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 17 (Right to erasure)"],
                "ccpa_sections": ["Section 1798.105 (Right to deletion)"],
                "severity_factors": ["good_practice"],
                "compliance_impact": "LOW"
            },
            
            # Advanced Privacy Types
            "MissingFieldLevelAccessScoping": {
                "gdpr_articles": ["Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["access_control", "privacy_by_design"],
                "compliance_impact": "MEDIUM"
            },
            "AdTrackingCode": {
                "gdpr_articles": ["Article 7 (Conditions for consent)", "Article 21 (Right to object)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)"],
                "severity_factors": ["tracking", "consent_requirement"],
                "compliance_impact": "MEDIUM"
            },
            "RegionLockViolation": {
                "gdpr_articles": ["Article 44 (General principle for transfers)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_transfer", "cross_border"],
                "compliance_impact": "HIGH"
            },
            "LargePiiTableJoin": {
                "gdpr_articles": ["Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_minimization", "privacy_by_design"],
                "compliance_impact": "MEDIUM"
            },
            "MLPipelineDataMinimization": {
                "gdpr_articles": ["Article 5 (Data minimization)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_minimization", "ai_privacy"],
                "compliance_impact": "MEDIUM"
            },
            "ApiVersionFound": {
                "gdpr_articles": ["Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["versioning", "privacy_by_design"],
                "compliance_impact": "LOW"
            },
            "NewDatabaseColumn": {
                "gdpr_articles": ["Article 5 (Data minimization)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_minimization", "necessity"],
                "compliance_impact": "LOW"
            },
            "FieldScopingFound": {
                "gdpr_articles": ["Article 25 (Privacy by design)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["good_practice"],
                "compliance_impact": "LOW"
            },
            
            # Developer Guidance Types
            "ObjectCreationWithPii": {
                "gdpr_articles": ["Article 5 (Data minimization)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_minimization", "necessity"],
                "compliance_impact": "MEDIUM"
            },
            "DataStorageOperation": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 6 (Lawfulness)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_storage", "legal_basis"],
                "compliance_impact": "HIGH"
            },
            "CommunicationWithPii": {
                "gdpr_articles": ["Article 7 (Conditions for consent)", "Article 6 (Lawfulness)"],
                "ccpa_sections": ["Section 1798.120 (Right to opt-out)"],
                "severity_factors": ["communication", "consent_requirement"],
                "compliance_impact": "MEDIUM"
            },
            "DataExportWithPii": {
                "gdpr_articles": ["Article 20 (Data portability)"],
                "ccpa_sections": ["Section 1798.100 (Consumer rights)"],
                "severity_factors": ["data_export", "user_rights"],
                "compliance_impact": "HIGH"
            },
            "ApiEndpointWithPii": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "severity_factors": ["api_security", "data_protection"],
                "compliance_impact": "HIGH"
            },
            "DatabaseSchemaWithPii": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "severity_factors": ["database_security", "data_protection"],
                "compliance_impact": "HIGH"
            },
            "CachingWithPii": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 32 (Security)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["caching", "data_protection"],
                "compliance_impact": "MEDIUM"
            },
            "SearchQueryWithPii": {
                "gdpr_articles": ["Article 32 (Security of processing)"],
                "ccpa_sections": ["Section 1798.150 (Civil Action)"],
                "severity_factors": ["search_security", "data_protection"],
                "compliance_impact": "MEDIUM"
            },
            
            # AI Privacy Types
            "ExcessiveDataCollection": {
                "gdpr_articles": ["Article 5(1)(c) (Data minimization)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_minimization", "necessity"],
                "compliance_impact": "MEDIUM"
            },
            "IncompleteDataDeletion": {
                "gdpr_articles": ["Article 17 (Right to erasure)"],
                "ccpa_sections": ["Section 1798.105 (Right to deletion)"],
                "severity_factors": ["data_deletion", "user_rights"],
                "compliance_impact": "HIGH"
            },
            "ExcessiveDataBackup": {
                "gdpr_articles": ["Article 5(1)(e) (Storage limitation)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["storage_limitation", "necessity"],
                "compliance_impact": "MEDIUM"
            },
            "DataMinimizationViolation": {
                "gdpr_articles": ["Article 5(1)(c) (Data minimization)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["data_minimization", "necessity"],
                "compliance_impact": "MEDIUM"
            },
            
            # Privacy Policy Types
            "PrivacyViolation": {
                "gdpr_articles": ["Article 5 (Principles)", "Article 6 (Lawfulness)"],
                "ccpa_sections": ["Section 1798.140 (Definitions)"],
                "severity_factors": ["general_privacy", "compliance"],
                "compliance_impact": "MEDIUM"
            }
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process compliance analysis by listening for AIEnhancedFindings event"""
        self.log_activity("Starting compliance analysis - listening for AIEnhancedFindings event")
        
        # Example: Fetch a secret (compliance config) from Secret Manager
        # compliance_config = self.fetch_secret(f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/COMPLIANCE_CONFIG")

        # Check if we have enhanced scan results in input_data (from AIEnhancedFindings event)
        enhanced_results = input_data.get('enhanced_results', [])
        correlation_id = input_data.get('correlation_id', 'default')
        
        if not enhanced_results:
            self.log_activity("No enhanced results found in input - waiting for AIEnhancedFindings event", "warning")
            return {"error": "No enhanced results available for compliance analysis"}

        # Convert enhanced results from dict to ScanResult objects if needed
        if isinstance(enhanced_results[0], dict):
            scan_results = [self._dict_to_scan_result(result) for result in enhanced_results]
        else:
            scan_results = enhanced_results

        # Publish compliance analysis started event
        self.publish_event(
            "ComplianceAnalysisStarted",
            {"violation_count": len(scan_results), "agent": self.agent_name},
            correlation_id
        )

        compliance_report = {
            "summary": {},
            "violations_by_regulation": {},
            "risk_assessment": {},
            "recommendations": [],
            "compliance_score": 0,
            "gemini_enhanced": self.is_gemini_available()
        }

        if not scan_results:
            compliance_report["summary"] = {
                "total_violations": 0,
                "compliance_status": "COMPLIANT",
                "message": "No privacy violations detected"
            }
            return compliance_report

        # Use Gemini AI for enhanced compliance analysis if available
        if self.is_gemini_available():
            try:
                enhanced_analysis = await self._get_gemini_compliance_analysis(scan_results)
                if enhanced_analysis:
                    compliance_report.update(enhanced_analysis)
                    self.log_activity("Gemini AI enhanced compliance analysis completed")
                else:
                    # Fallback to hardcoded rules
                    compliance_report.update(self._analyze_with_hardcoded_rules(scan_results))
            except Exception as e:
                self.log_activity(f"Gemini compliance analysis failed: {str(e)} - using hardcoded rules", "warning")
                compliance_report.update(self._analyze_with_hardcoded_rules(scan_results))
        else:
            # Use hardcoded rules
            compliance_report.update(self._analyze_with_hardcoded_rules(scan_results))

        # --- Google Cloud Integrations ---
        # Insert compliance analytics into BigQuery
        table_id = f"{os.getenv('GOOGLE_CLOUD_PROJECT')}.privacy.compliance_analysis"
        rows = [compliance_report]
        self.insert_bigquery_analytics(table_id, rows)

        # Export compliance metric to Cloud Monitoring
        self.export_custom_metric(
            metric_type="custom.googleapis.com/agent/compliance_score",
            value=compliance_report.get("compliance_score", 0),
            labels={"agent": self.agent_id}
        )

        # Publish ComplianceAnalysisCompleted event for other agents to consume
        self.publish_event(
            "ComplianceAnalysisCompleted",
            {
                "compliance_score": compliance_report["compliance_score"],
                "total_violations": compliance_report["summary"].get("total_violations", 0),
                "regulations_affected": list(compliance_report["violations_by_regulation"].keys()),
                "compliance_report": compliance_report,
                "agent": self.agent_name
            },
            correlation_id
        )

        self.log_activity(f"Compliance analysis completed: {compliance_report['compliance_score']}% compliance score - emitting ComplianceAnalysisCompleted")
        return compliance_report

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

    async def _get_gemini_compliance_analysis(self, scan_results: List[ScanResult]) -> Optional[Dict[str, Any]]:
        """Get enhanced compliance analysis from Gemini AI"""
        try:
            # Prepare violation data for AI analysis
            violations_data = []
            for result in scan_results:
                violations_data.append({
                    "file_path": result.file_path,
                    "line_number": result.line_number,
                    "violation_type": result.violation_type,
                    "description": result.description,
                    "severity": result.severity,
                    "fix_suggestion": result.fix_suggestion,
                    "regulation_reference": result.regulation_reference
                })

            prompt = self._create_compliance_prompt(violations_data)
            
            ai_response = await self.get_gemini_analysis(prompt, {
                "violation_count": len(scan_results),
                "severity_distribution": self._get_severity_distribution(scan_results)
            })
            
            if ai_response:
                return self._parse_compliance_response(ai_response, scan_results)
            
        except Exception as e:
            self.log_activity(f"Gemini compliance analysis error: {str(e)}", "warning")
        
        return None

    def _create_compliance_prompt(self, violations_data: List[Dict]) -> str:
        """Create AI prompt for compliance analysis"""
        violations_text = "\n".join([
            f"- {v['violation_type']} (Line {v['line_number']}): {v['description']} [Severity: {v['severity']}]"
            for v in violations_data
        ])
        
        prompt = f"""
You are a privacy compliance expert analyzing code violations for regulatory compliance.

Detected violations:
{violations_text}

Please provide a comprehensive compliance analysis including:

1. **Compliance Summary**: Overall compliance status and score
2. **Regulation Mapping**: Map each violation to specific regulations (GDPR, CCPA, HIPAA, etc.)
3. **Risk Assessment**: Evaluate business and legal risks
4. **Priority Recommendations**: Actionable compliance recommendations
5. **Compliance Score**: Calculate overall compliance percentage

Format your response as JSON:
{{
    "summary": {{
        "total_violations": <number>,
        "compliance_status": "<COMPLIANT/PARTIALLY_COMPLIANT/NON_COMPLIANT>",
        "compliance_score": <percentage>,
        "message": "<overall assessment>"
    }},
    "violations_by_regulation": {{
        "GDPR": [
            {{
                "violation_type": "<type>",
                "description": "<description>",
                "severity": "<HIGH/MEDIUM/LOW>",
                "article": "<GDPR article>",
                "penalty_risk": "<risk level>"
            }}
        ],
        "CCPA": [...],
        "HIPAA": [...]
    }},
    "risk_assessment": {{
        "business_risk": "<HIGH/MEDIUM/LOW>",
        "legal_risk": "<HIGH/MEDIUM/LOW>",
        "reputation_risk": "<HIGH/MEDIUM/LOW>",
        "financial_impact": "<estimated cost>"
    }},
    "recommendations": [
        {{
            "priority": "<HIGH/MEDIUM/LOW>",
            "action": "<specific action>",
            "timeline": "<recommended timeline>",
            "impact": "<expected impact>"
        }}
    ]
}}

Focus on practical compliance guidance and regulatory requirements.
"""
        return prompt

    def _parse_compliance_response(self, ai_response: str, scan_results: List[ScanResult]) -> Dict[str, Any]:
        """Parse AI compliance response"""
        try:
            ai_data = json.loads(ai_response)
            
            # Validate and enhance AI response
            compliance_report = {
                "summary": ai_data.get("summary", {}),
                "violations_by_regulation": ai_data.get("violations_by_regulation", {}),
                "risk_assessment": ai_data.get("risk_assessment", {}),
                "recommendations": ai_data.get("recommendations", []),
                "compliance_score": ai_data.get("summary", {}).get("compliance_score", 0)
            }
            
            # Ensure compliance score is calculated
            if compliance_report["compliance_score"] == 0:
                compliance_report["compliance_score"] = self._calculate_compliance_score(scan_results)
            
            return compliance_report
            
        except json.JSONDecodeError as e:
            self.log_activity(f"Failed to parse AI compliance response: {str(e)}", "warning")
            return None
        except Exception as e:
            self.log_activity(f"Error processing AI compliance response: {str(e)}", "warning")
            return None

    def _get_severity_distribution(self, scan_results: List[ScanResult]) -> Dict[str, int]:
        """Get distribution of violations by severity"""
        distribution = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for result in scan_results:
            distribution[result.severity] += 1
        return distribution

    def _analyze_with_hardcoded_rules(self, scan_results: List[ScanResult]) -> Dict[str, Any]:
        """Fallback to hardcoded compliance rules"""
        self.log_activity("Using hardcoded compliance rules")
        
        # Group violations by regulation
        violations_by_regulation = {}
        for result in scan_results:
            regulation = result.regulation_reference
            if regulation not in violations_by_regulation:
                violations_by_regulation[regulation] = []
            violations_by_regulation[regulation].append({
                "violation_type": result.violation_type,
                "description": result.description,
                "severity": result.severity,
                "file_path": result.file_path,
                "line_number": result.line_number
            })

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(scan_results)
        
        # Determine compliance status
        if compliance_score >= 90:
            compliance_status = "COMPLIANT"
        elif compliance_score >= 70:
            compliance_status = "PARTIALLY_COMPLIANT"
        else:
            compliance_status = "NON_COMPLIANT"

        # Generate recommendations
        recommendations = self._generate_hardcoded_recommendations(scan_results)

        return {
            "summary": {
                "total_violations": len(scan_results),
                "compliance_status": compliance_status,
                "compliance_score": compliance_score,
                "message": f"Found {len(scan_results)} privacy violations requiring attention"
            },
            "violations_by_regulation": violations_by_regulation,
            "risk_assessment": self._assess_risk_hardcoded(scan_results),
            "recommendations": recommendations,
            "compliance_score": compliance_score
        }

    def _calculate_compliance_score(self, scan_results: List[ScanResult]) -> int:
        """Calculate compliance score based on violations"""
        if not scan_results:
            return 100
        
        # Weight violations by severity
        total_weight = 0
        for result in scan_results:
            if result.severity == "HIGH":
                total_weight += 3
            elif result.severity == "MEDIUM":
                total_weight += 2
            else:
                total_weight += 1
        
        # Calculate score (higher weight = lower score)
        max_possible_weight = len(scan_results) * 3
        score = max(0, 100 - (total_weight / max_possible_weight) * 100)
        return int(score)

    def _assess_risk_hardcoded(self, scan_results: List[ScanResult]) -> Dict[str, str]:
        """Assess risk using hardcoded rules"""
        high_count = sum(1 for r in scan_results if r.severity == "HIGH")
        medium_count = sum(1 for r in scan_results if r.severity == "MEDIUM")
        
        if high_count > 5:
            business_risk = "HIGH"
        elif high_count > 2 or medium_count > 10:
            business_risk = "MEDIUM"
        else:
            business_risk = "LOW"
        
        return {
            "business_risk": business_risk,
            "legal_risk": business_risk,  # Simplified mapping
            "reputation_risk": business_risk,
            "financial_impact": f"${high_count * 5000 + medium_count * 1000} estimated"
        }

    def _generate_hardcoded_recommendations(self, scan_results: List[ScanResult]) -> List[Dict[str, str]]:
        """Generate recommendations using hardcoded rules"""
        recommendations = []
        
        high_violations = [r for r in scan_results if r.severity == "HIGH"]
        medium_violations = [r for r in scan_results if r.severity == "MEDIUM"]
        
        if high_violations:
            recommendations.append({
                "priority": "HIGH",
                "action": f"Fix {len(high_violations)} high-severity violations immediately",
                "timeline": "Within 24 hours",
                "impact": "Critical for compliance and risk mitigation"
            })
        
        if medium_violations:
            recommendations.append({
                "priority": "MEDIUM",
                "action": f"Address {len(medium_violations)} medium-severity violations",
                "timeline": "Within 1 week",
                "impact": "Important for maintaining compliance"
            })
        
        # Add general recommendations
        recommendations.append({
            "priority": "MEDIUM",
            "action": "Implement automated privacy scanning in CI/CD pipeline",
            "timeline": "Within 2 weeks",
            "impact": "Prevent future violations"
        })
        
        return recommendations

    # Cloud Function trigger template (for reference)
    # def cloud_function_entrypoint(request):
    #     """
    #     Cloud Function HTTP trigger for ComplianceAgent.
    #     """
    #     # Parse request, call self.process(), return response
    #     pass 