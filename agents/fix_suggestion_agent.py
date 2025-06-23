"""
FixSuggestionAgent - AI-Powered Code Fix Generation
==================================================

This agent is responsible for generating actionable code fixes for privacy violations.
It listens for ComplianceAnalysisCompleted events from ComplianceAgent and emits
FixSuggestionsCompleted events for downstream agents to consume.

Key Responsibilities:
--------------------
- Listen for ComplianceAnalysisCompleted events from ComplianceAgent
- Generate AI-powered fix suggestions for privacy violations
- Provide code patches and implementation guidance
- Prioritize fixes based on severity and compliance impact
- Generate comprehensive fix recommendations
- Emit FixSuggestionsCompleted events with fix suggestions

Event-Based Architecture:
------------------------
This agent is the fourth in the event flow chain:
- Listens for ComplianceAnalysisCompleted events from ComplianceAgent
- Generates AI-powered fix suggestions
- Emits FixSuggestionsCompleted events with fix recommendations
- Provides implementation guidance for remediation

Fix Generation Capabilities:
---------------------------
AI-Powered Fix Suggestions:
- Generates context-aware code fixes using Gemini AI
- Provides specific, actionable implementation guidance
- Adapts fixes to the specific codebase and technology stack
- Considers compliance requirements and best practices

Code Patch Generation:
- Creates specific code patches for each violation
- Provides before/after code examples
- Includes implementation steps and considerations
- Addresses security and compliance requirements

Fix Prioritization:
- Prioritizes fixes based on severity and compliance impact
- Identifies critical fixes requiring immediate attention
- Provides implementation timeline and effort estimates
- Suggests optimal fix order for maximum impact

Implementation Guidance:
- Provides step-by-step implementation instructions
- Includes testing and validation recommendations
- Addresses potential side effects and dependencies
- Suggests monitoring and verification approaches

Processing Flow:
---------------
1. Listen for ComplianceAnalysisCompleted event from ComplianceAgent
2. Convert enhanced results to ScanResult objects if needed
3. Generate AI-powered fix suggestions for each violation
4. Create code patches and implementation guidance
5. Prioritize fixes based on severity and compliance impact
6. Emit FixSuggestionsCompleted event with fix recommendations

AI Integration:
--------------
When Gemini AI is available:
- Generates context-aware code fixes
- Provides specific implementation guidance
- Adapts fixes to codebase architecture
- Considers compliance and security requirements

Fallback Mechanisms:
-------------------
- Uses hardcoded fix templates when AI is unavailable
- Provides comprehensive fix coverage for all violation types
- Maintains reliable fix generation capabilities

Integration Points:
------------------
- ComplianceAgent: Receives ComplianceAnalysisCompleted events
- Google Gemini AI: AI-powered fix generation
- ReportAgent: Emits FixSuggestionsCompleted for report generation
- Event System: Listens for and emits events

Usage:
------
The agent is typically invoked by the Agent Orchestrator after ComplianceAgent:
- enhanced_results: AI-enhanced results from previous agents
- compliance_report: Compliance analysis from ComplianceAgent
- correlation_id: Request tracking ID
- fix_options: Optional fix configuration

Returns:
- Comprehensive fix suggestions report
- Code patches and implementation guidance
- Fix prioritization and timeline recommendations

Event Communication:
-------------------
Listens for:
- ComplianceAnalysisCompleted: Compliance analysis from ComplianceAgent

Emits:
- FixSuggestionsCompleted: Fix suggestions and recommendations
- FixSuggestionsStarted: When fix generation begins

Dependencies:
-------------
- Google Gemini AI: AI-powered fix generation
- ComplianceAgent: Source of ComplianceAnalysisCompleted events
- asyncio: Asynchronous processing
- json: Data serialization and parsing
- datetime: Timestamp management
- typing: Type hints and data structures

Author: Privacy Guardian Team
Built with Google Cloud Agent Development Kit (ADK)

Integrations:
- Inserts fix analytics into BigQuery after fix generation
- Exports fix metrics to Cloud Monitoring
- Fetches secrets (e.g., fix config) from Secret Manager
- Cloud Function trigger template provided for serverless execution
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

class FixSuggestionAgent(BaseAgent):
    """
    Agent responsible for providing specific code fixes and AI-powered refactoring.
    
    This agent generates actionable code fixes for privacy violations, combining
    comprehensive hardcoded templates with AI-enhanced suggestions. It provides
    language-specific solutions, security best practices, and implementation
    guidance for developers.
    
    Key Features:
    - Comprehensive fix templates for 50+ violation types
    - AI-enhanced context-aware fix suggestions
    - Language-specific code examples and best practices
    - Security-focused recommendations and alternatives
    - Implementation guidance and effort estimation
    - Robust fallback to hardcoded templates when AI is unavailable
    
    Processing Flow:
    1. Receive scan results from PrivacyScanAgent
    2. Generate base fix suggestions using hardcoded templates
    3. Enhance fixes with AI analysis if available
    4. Provide context-specific recommendations
    5. Include implementation guidance and effort estimation
    
    AI Enhancement:
    - Context-aware fix suggestions based on file content
    - Language-specific code examples and best practices
    - Alternative approaches and implementation strategies
    - Security-focused recommendations
    - Effort estimation and prioritization guidance
    """
    
    def __init__(self):
        """Initialize the FixSuggestionAgent with comprehensive fix templates."""
        super().__init__("fix_suggestion_agent", "🛠️ FixSuggestionAgent")
        self.fix_templates = self._initialize_fix_templates()
        
    def _initialize_fix_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize fix suggestion templates for all 50+ violation types"""
        return {
            # PII Detection Types
            "HardcodedEmail": {
                "template": "Replace hardcoded email with environment variable:\n```\n# Before:\nemail = \"{email}\"\n\n# After:\nemail = os.getenv('USER_EMAIL')\n```",
                "priority": "HIGH",
                "estimated_effort": "5 minutes"
            },
            "SSNExposure": {
                "template": "Remove SSN from code and use secure storage:\n```\n# Before:\nssn = \"{ssn}\"\n\n# After:\n# Remove SSN from code\n# Use secure database or vault service\nssn_hash = hashlib.sha256(ssn.encode()).hexdigest()\n```",
                "priority": "CRITICAL",
                "estimated_effort": "15 minutes"
            },
            "CreditCardExposure": {
                "template": "Remove credit card data and use PCI-compliant processing:\n```\n# Before:\ncard_number = \"{card}\"\n\n# After:\n# Remove credit card from code\n# Use Stripe, PayPal, or other PCI-compliant service\npayment_token = payment_service.create_token(card_number)\n```",
                "priority": "CRITICAL",
                "estimated_effort": "30 minutes"
            },
            "PassportExposure": {
                "template": "Remove passport data and use secure storage:\n```\n# Before:\npassport = \"{passport}\"\n\n# After:\n# Remove passport from code\n# Use secure database with encryption\npassport_hash = hashlib.sha256(passport.encode()).hexdigest()\n```",
                "priority": "CRITICAL",
                "estimated_effort": "15 minutes"
            },
            "PhoneNumberExposure": {
                "template": "Remove phone number from code:\n```\n# Before:\nphone = \"{phone}\"\n\n# After:\nphone = os.getenv('CONTACT_PHONE')\n# Or use secure storage\n```",
                "priority": "MEDIUM",
                "estimated_effort": "5 minutes"
            },
            "BankAccountExposure": {
                "template": "Remove bank account data and use secure storage:\n```\n# Before:\naccount = \"{account}\"\n\n# After:\n# Remove bank account from code\n# Use secure financial service integration\naccount_token = financial_service.create_token(account)\n```",
                "priority": "CRITICAL",
                "estimated_effort": "20 minutes"
            },
            "DriversLicenseExposure": {
                "template": "Remove driver's license data:\n```\n# Before:\nlicense = \"{license}\"\n\n# After:\n# Remove driver's license from code\n# Use secure storage with encryption\nlicense_hash = hashlib.sha256(license.encode()).hexdigest()\n```",
                "priority": "CRITICAL",
                "estimated_effort": "15 minutes"
            },
            "NationalIdExposure": {
                "template": "Remove national ID data:\n```\n# Before:\nnational_id = \"{national_id}\"\n\n# After:\n# Remove national ID from code\n# Use secure storage with encryption\nid_hash = hashlib.sha256(national_id.encode()).hexdigest()\n```",
                "priority": "CRITICAL",
                "estimated_effort": "15 minutes"
            },
            "AddressExposure": {
                "template": "Remove address data from code:\n```\n# Before:\naddress = \"{address}\"\n\n# After:\naddress = os.getenv('USER_ADDRESS')\n# Or use secure storage\n```",
                "priority": "MEDIUM",
                "estimated_effort": "5 minutes"
            },
            "MedicalDataExposure": {
                "template": "Remove medical data and use HIPAA-compliant storage:\n```\n# Before:\nmedical_record = \"{medical}\"\n\n# After:\n# Remove medical data from code\n# Use HIPAA-compliant storage service\nrecord_id = medical_service.store_encrypted(medical_record)\n```",
                "priority": "CRITICAL",
                "estimated_effort": "25 minutes"
            },
            "BiometricDataExposure": {
                "template": "Remove biometric data and use secure storage:\n```\n# Before:\nbiometric = \"{biometric}\"\n\n# After:\n# Remove biometric data from code\n# Use secure biometric storage service\nbiometric_hash = biometric_service.store_encrypted(biometric)\n```",
                "priority": "CRITICAL",
                "estimated_effort": "20 minutes"
            },
            "HardcodedSecret": {
                "template": "Replace hardcoded secret with environment variable:\n```\n# Before:\napi_key = \"{secret}\"\n\n# After:\napi_key = os.getenv('API_KEY')\n# Or use a secrets manager\napi_key = secrets_manager.get_secret('api_key')\n```",
                "priority": "HIGH",
                "estimated_effort": "10 minutes"
            },
            
            # Security & Encryption Types
            "InsecureConnection": {
                "template": "Replace HTTP with HTTPS:\n```\n# Before:\nurl = \"http://api.example.com\"\n\n# After:\nurl = \"https://api.example.com\"\n# Ensure SSL/TLS is properly configured\n```",
                "priority": "MEDIUM",
                "estimated_effort": "5 minutes"
            },
            "TLSDisabled": {
                "template": "Enable TLS/SSL encryption:\n```\n# Before:\ntls_enabled = false\n\n# After:\ntls_enabled = true\n# Configure proper SSL/TLS settings\n```",
                "priority": "HIGH",
                "estimated_effort": "10 minutes"
            },
            "EncryptionViolation": {
                "template": "Add encryption for sensitive data:\n```\n# Before:\nstore_sensitive_data(data)\n\n# After:\nencrypted_data = encryption_service.encrypt(data)\nstore_sensitive_data(encrypted_data)\n```",
                "priority": "HIGH",
                "estimated_effort": "15 minutes"
            },
            "RawPiiAsPrimaryKey": {
                "template": "Hash or tokenize PII before using as primary key:\n```\n# Before:\nuser_id = email\n\n# After:\nuser_id = hashlib.sha256(email.encode()).hexdigest()\n# Or use a tokenization service\n```",
                "priority": "HIGH",
                "estimated_effort": "15 minutes"
            },
            "MissingRateLimiting": {
                "template": "Add rate limiting for API endpoints:\n```\n# Before:\n@app.route('/api/user-data')\ndef get_user_data():\n    return user_data\n\n# After:\n@app.route('/api/user-data')\n@rate_limit(requests=100, window=3600)\ndef get_user_data():\n    return user_data\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "MissingEncryptionAtRest": {
                "template": "Add encryption at rest for database:\n```\n# Before:\nCREATE TABLE users (id INT, email VARCHAR(255));\n\n# After:\nCREATE TABLE users (\n    id INT,\n    email VARCHAR(255) ENCRYPTED\n);\n```",
                "priority": "HIGH",
                "estimated_effort": "20 minutes"
            },
            "UnencryptedDataWrite": {
                "template": "Encrypt data before writing to storage:\n```\n# Before:\nstore_data(sensitive_data)\n\n# After:\nencrypted_data = encryption_service.encrypt(sensitive_data)\nstore_data(encrypted_data)\n```",
                "priority": "HIGH",
                "estimated_effort": "15 minutes"
            },
            "PiiHashingFound": {
                "template": "Good practice - PII hashing detected:\n```\n# This is correct implementation\n# No changes needed\n```",
                "priority": "LOW",
                "estimated_effort": "0 minutes"
            },
            
            # Consent & Privacy Policy Types
            "ConsentViolation": {
                "template": "Add proper consent mechanism:\n```\n# Before:\nuser_data = collect_user_data()\n\n# After:\nif user_consent.is_granted('data_collection'):\n    user_data = collect_user_data()\nelse:\n    raise ConsentRequiredError('User consent required')\n```",
                "priority": "HIGH",
                "estimated_effort": "20 minutes"
            },
            "MissingPurposeLimitation": {
                "template": "Add purpose limitation annotation:\n```\n# Before:\nuser_data = collect_user_data()\n\n# After:\nuser_data = collect_user_data()\n# Purpose: Account creation and authentication\n# Retention: 30 days\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "MissingProfilingOptOut": {
                "template": "Add profiling opt-out check:\n```\n# Before:\napply_profiling_algorithm(user_data)\n\n# After:\nif not user_consent.profiling_disabled:\n    apply_profiling_algorithm(user_data)\nelse:\n    skip_profiling()\n```",
                "priority": "HIGH",
                "estimated_effort": "15 minutes"
            },
            "DisabledOptOut": {
                "template": "Enable opt-out mechanism:\n```\n# Before:\nopt_out_enabled = false\n\n# After:\nopt_out_enabled = true\n# Provide clear opt-out instructions\n```",
                "priority": "HIGH",
                "estimated_effort": "10 minutes"
            },
            "ForcedConsent": {
                "template": "Remove forced consent:\n```\n# Before:\nforced_consent = true\n\n# After:\nforced_consent = false\n# Implement genuine consent mechanism\n```",
                "priority": "HIGH",
                "estimated_effort": "15 minutes"
            },
            "DefaultEnabledConsent": {
                "template": "Change default to opt-in:\n```\n# Before:\ndefault_enabled = true\n\n# After:\ndefault_enabled = false\n# Default should be opt-in for data collection\n```",
                "priority": "MEDIUM",
                "estimated_effort": "5 minutes"
            },
            "RightToBeForgottenViolation": {
                "template": "Implement proper deletion mechanism:\n```\n# Before:\narchive_user_data(user_id)\n\n# After:\nif user_consent.is_granted('deletion'):\n    permanently_delete_user_data(user_id)\n    log_deletion_event(user_id)\n```",
                "priority": "HIGH",
                "estimated_effort": "25 minutes"
            },
            "DoNotSellViolation": {
                "template": "Implement opt-out for data sales:\n```\n# Before:\nsell_user_data(user_data)\n\n# After:\nif not user_consent.do_not_sell:\n    sell_user_data(user_data)\nelse:\n    respect_do_not_sell_preference()\n```",
                "priority": "HIGH",
                "estimated_effort": "20 minutes"
            },
            
            # Data Flow & Handling Types
            "SensitiveDataSource": {
                "template": "Implement taint tracking for PII:\n```\n# Before:\nuser_data = get_user_data()\nprocess_data(user_data)\n\n# After:\nuser_data = get_user_data()\nif is_pii(user_data):\n    user_data = mask_pii(user_data)\nprocess_data(user_data)\n```",
                "priority": "MEDIUM",
                "estimated_effort": "15 minutes"
            },
            "DataMaskingFound": {
                "template": "Good practice - data masking detected:\n```\n# This is correct implementation\n# No changes needed\n```",
                "priority": "LOW",
                "estimated_effort": "0 minutes"
            },
            "UnsanitizedStackTrace": {
                "template": "Implement stack trace sanitization:\n```\n# Before:\nprint_stack_trace()\n\n# After:\nsanitized_trace = sanitize_stack_trace(get_stack_trace())\nprint_stack_trace(sanitized_trace)\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "DataSharingViolation": {
                "template": "Add data sharing controls:\n```\n# Before:\nshare_data_with_third_party(user_data)\n\n# After:\nif user_consent.is_granted('data_sharing'):\n    share_data_with_third_party(user_data)\nelse:\n    log_warning('Data sharing consent not granted')\n```",
                "priority": "HIGH",
                "estimated_effort": "20 minutes"
            },
            "DataRetentionViolation": {
                "template": "Implement data retention policy:\n```\n# Before:\nstore_data(user_data)\n\n# After:\nstore_data(user_data, retention_days=30)\n# Implement automatic deletion\nschedule_deletion(user_data_id, days=30)\n```",
                "priority": "MEDIUM",
                "estimated_effort": "25 minutes"
            },
            "MissingDSARRegistration": {
                "template": "Add DSAR compliance registration:\n```\n# Before:\nstore_user_data(user_data)\n\n# After:\nstore_user_data(user_data)\nregister_dsar(user_id, 'data_storage', purpose='account_creation')\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "LoggingViolation": {
                "template": "Remove PII from logs:\n```\n# Before:\nlogger.info(f\"User {user_email} logged in\")\n\n# After:\nlogger.info(f\"User {user_id} logged in\")\n# Or use structured logging with PII masking\nlogger.info(\"User logged in\", extra={\"user_id\": user_id})\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "ThirdPartyDataSharing": {
                "template": "Add third-party data protection:\n```\n# Before:\nthird_party_api.send_data(user_data)\n\n# After:\nif third_party_api.has_adequate_protection():\n    third_party_api.send_data(user_data)\nelse:\n    raise InadequateProtectionError()\n```",
                "priority": "HIGH",
                "estimated_effort": "20 minutes"
            },
            "ApprovedEndpointsFound": {
                "template": "Good practice - approved endpoints detected:\n```\n# This is correct implementation\n# No changes needed\n```",
                "priority": "LOW",
                "estimated_effort": "0 minutes"
            },
            "RetentionTimerFound": {
                "template": "Good practice - retention timer detected:\n```\n# This is correct implementation\n# No changes needed\n```",
                "priority": "LOW",
                "estimated_effort": "0 minutes"
            },
            
            # Advanced Privacy Types
            "MissingFieldLevelAccessScoping": {
                "template": "Add field-level access scoping:\n```\n# Before:\ntype User {\n  email: String\n  ssn: String\n}\n\n# After:\ntype User {\n  email: String @scope(role: \"admin\")\n  ssn: String @scope(role: \"hr\")\n}\n```",
                "priority": "MEDIUM",
                "estimated_effort": "15 minutes"
            },
            "AdTrackingCode": {
                "template": "Add consent check for ad/tracking:\n```\n# Before:\nload_ad_tracking_code()\n\n# After:\nif user_consent.is_granted('ad_tracking'):\n    load_ad_tracking_code()\nelse:\n    load_privacy_friendly_analytics()\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "RegionLockViolation": {
                "template": "Ensure EU data stays within EEA:\n```\n# Before:\naws_region = 'us-east-1'\n\n# After:\naws_region = 'eu-west-1'  # EEA region\n# Or implement proper data transfer mechanisms\n```",
                "priority": "HIGH",
                "estimated_effort": "30 minutes"
            },
            "LargePiiTableJoin": {
                "template": "Pseudonymize join keys:\n```\n# Before:\nJOIN users ON users.email = orders.customer_email\n\n# After:\nJOIN users ON users.email_hash = orders.customer_email_hash\n# Ensure email_hash is pseudonymized\n```",
                "priority": "MEDIUM",
                "estimated_effort": "20 minutes"
            },
            "MLPipelineDataMinimization": {
                "template": "Minimize data in ML pipeline:\n```\n# Before:\nload_all_user_data_for_training()\n\n# After:\nload_only_necessary_columns(['age', 'gender'])\n# Exclude sensitive fields like SSN, email\n```",
                "priority": "MEDIUM",
                "estimated_effort": "15 minutes"
            },
            "ApiVersionFound": {
                "template": "Bump API version for PII changes:\n```\n# Before:\napi_version = 'v1'\n\n# After:\napi_version = 'v2'  # Bump when PII fields change\n# Update privacy contract version\n```",
                "priority": "LOW",
                "estimated_effort": "5 minutes"
            },
            "NewDatabaseColumn": {
                "template": "Verify column necessity:\n```\n# Before:\nALTER TABLE users ADD COLUMN new_field VARCHAR(255);\n\n# After:\n-- Verify this column is necessary\n-- Add @required annotation if needed\nALTER TABLE users ADD COLUMN new_field VARCHAR(255);\n```",
                "priority": "LOW",
                "estimated_effort": "5 minutes"
            },
            "FieldScopingFound": {
                "template": "Good practice - field scoping detected:\n```\n# This is correct implementation\n# No changes needed\n```",
                "priority": "LOW",
                "estimated_effort": "0 minutes"
            },
            
            # Developer Guidance Types
            "ObjectCreationWithPii": {
                "template": "Minimize PII in object creation:\n```\n# Before:\nuser = User(email, ssn, phone, address)\n\n# After:\nuser = User(email)  # Only collect necessary fields\n# Collect additional fields only when needed\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "DataStorageOperation": {
                "template": "Add consent and retention for data storage:\n```\n# Before:\nsave_user_data(user_data)\n\n# After:\nif user_consent.is_granted('data_storage'):\n    save_user_data(user_data, retention_days=30)\nelse:\n    raise ConsentRequiredError()\n```",
                "priority": "HIGH",
                "estimated_effort": "15 minutes"
            },
            "CommunicationWithPii": {
                "template": "Add opt-out for communications:\n```\n# Before:\nsend_email(user_email, message)\n\n# After:\nif user_consent.is_granted('communications'):\n    send_email(user_email, message)\n    include_opt_out_link()\nelse:\n    skip_communication()\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "DataExportWithPii": {
                "template": "Add access controls for data export:\n```\n# Before:\nexport_user_data(user_id)\n\n# After:\nif user_has_permission('data_export'):\n    audit_export_request(user_id)\n    export_user_data(user_id)\nelse:\n    raise PermissionDeniedError()\n```",
                "priority": "HIGH",
                "estimated_effort": "20 minutes"
            },
            "ApiEndpointWithPii": {
                "template": "Add security for PII API endpoints:\n```\n# Before:\n@app.route('/api/user-data')\ndef get_user_data():\n    return user_data\n\n# After:\n@app.route('/api/user-data')\n@require_auth\n@rate_limit(requests=100, window=3600)\ndef get_user_data():\n    return user_data\n```",
                "priority": "HIGH",
                "estimated_effort": "15 minutes"
            },
            "DatabaseSchemaWithPii": {
                "template": "Add encryption for PII database schema:\n```\n# Before:\nCREATE TABLE users (email VARCHAR(255), ssn VARCHAR(11));\n\n# After:\nCREATE TABLE users (\n    email VARCHAR(255) ENCRYPTED,\n    ssn VARCHAR(11) ENCRYPTED\n);\n```",
                "priority": "HIGH",
                "estimated_effort": "25 minutes"
            },
            "CachingWithPii": {
                "template": "Add expiration for PII caching:\n```\n# Before:\ncache.set('user_data', user_data)\n\n# After:\ncache.set('user_data', user_data, expire=3600)\n# Or avoid caching PII entirely\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "SearchQueryWithPii": {
                "template": "Add access controls for search queries:\n```\n# Before:\nsearch_users(query)\n\n# After:\nif user_has_permission('search'):\n    audit_search_query(query)\n    search_users(query)\nelse:\n    raise PermissionDeniedError()\n```",
                "priority": "MEDIUM",
                "estimated_effort": "15 minutes"
            },
            
            # AI Privacy Types
            "ExcessiveDataCollection": {
                "template": "Minimize data collection:\n```\n# Before:\ncollect_all_user_data()\n\n# After:\ncollect_only_necessary_data(['name', 'email'])\n# Remove unnecessary fields\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            "IncompleteDataDeletion": {
                "template": "Implement complete data deletion:\n```\n# Before:\nsoft_delete_user(user_id)\n\n# After:\npermanently_delete_user(user_id)\nverify_deletion(user_id)\nlog_deletion_event(user_id)\n```",
                "priority": "HIGH",
                "estimated_effort": "25 minutes"
            },
            "ExcessiveDataBackup": {
                "template": "Minimize backup data:\n```\n# Before:\nbackup_all_user_data()\n\n# After:\nbackup_only_essential_data()\n# Exclude sensitive PII from backups\n```",
                "priority": "MEDIUM",
                "estimated_effort": "15 minutes"
            },
            "DataMinimizationViolation": {
                "template": "Implement data minimization:\n```\n# Before:\nstore_all_user_fields()\n\n# After:\nstore_only_necessary_fields()\n# Review and remove unnecessary fields\n```",
                "priority": "MEDIUM",
                "estimated_effort": "10 minutes"
            },
            
            # Privacy Policy Types
            "PrivacyViolation": {
                "template": "Review and fix privacy violation:\n```\n# General privacy violation detected\n# Review the specific violation and implement appropriate fix\n# Consider consulting privacy compliance guidelines\n```",
                "priority": "MEDIUM",
                "estimated_effort": "15 minutes"
            }
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process fix suggestion generation by listening for ComplianceAnalysisCompleted event"""
        self.log_activity("Starting fix suggestion generation - listening for ComplianceAnalysisCompleted event")
        
        # Example: Fetch a secret (fix config) from Secret Manager
        # fix_config = self.fetch_secret(f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/FIX_CONFIG")

        # Check if we have compliance analysis and enhanced results in input_data
        compliance_report = input_data.get('compliance_report', {})
        enhanced_results = input_data.get('enhanced_results', [])
        correlation_id = input_data.get('correlation_id', 'default')
        
        if not enhanced_results:
            self.log_activity("No enhanced results found in input - waiting for ComplianceAnalysisCompleted event", "warning")
            return {"error": "No enhanced results available for fix suggestions"}

        # Convert enhanced results from dict to ScanResult objects if needed
        if isinstance(enhanced_results[0], dict):
            scan_results = [self._dict_to_scan_result(result) for result in enhanced_results]
        else:
            scan_results = enhanced_results

        # Publish fix suggestions started event
        self.publish_event(
            "FixSuggestionsStarted",
            {"violation_count": len(scan_results), "agent": self.agent_name},
            correlation_id
        )

        fix_suggestions = {
            "summary": {
                "total_violations": len(scan_results),
                "fixes_generated": 0,
                "ai_enhanced_fixes": 0,
                "priority_fixes": []
            },
            "fixes_by_violation": {},
            "fixes_by_file": {},
            "fixes_by_priority": {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            },
            "code_patches": [],
            "gemini_enhanced": self.is_gemini_available()
        }

        if not scan_results:
            fix_suggestions["summary"]["message"] = "No violations to fix"
            return fix_suggestions

        # Use Gemini AI for enhanced fix suggestions if available
        if self.is_gemini_available():
            try:
                enhanced_fixes = await self._get_gemini_fix_suggestions(scan_results, compliance_report)
                if enhanced_fixes and enhanced_fixes.get("summary"):
                    fix_suggestions.update(enhanced_fixes)
                    self.log_activity("Gemini AI enhanced fix suggestions completed")
                else:
                    # Fallback to hardcoded rules
                    hardcoded_fixes = await self._generate_hardcoded_fixes(scan_results)
                    fix_suggestions.update(hardcoded_fixes)
            except Exception as e:
                self.log_activity(f"Gemini fix suggestions failed: {str(e)} - using hardcoded rules", "warning")
                hardcoded_fixes = await self._generate_hardcoded_fixes(scan_results)
                fix_suggestions.update(hardcoded_fixes)
        else:
            # Use hardcoded rules
            hardcoded_fixes = await self._generate_hardcoded_fixes(scan_results)
            fix_suggestions.update(hardcoded_fixes)

        # Publish FixSuggestionsCompleted event for other agents to consume
        self.publish_event(
            "FixSuggestionsCompleted",
            {
                "total_fixes": fix_suggestions["summary"]["fixes_generated"],
                "ai_enhanced_fixes": fix_suggestions["summary"]["ai_enhanced_fixes"],
                "priority_fixes": fix_suggestions["summary"]["priority_fixes"],
                "fix_suggestions": fix_suggestions,
                "agent": self.agent_name
            },
            correlation_id
        )

        self.log_activity(f"Fix suggestions completed: {fix_suggestions['summary']['fixes_generated']} fixes generated - emitting FixSuggestionsCompleted")

        # --- Google Cloud Integrations ---
        # Insert fix analytics into BigQuery
        table_id = f"{os.getenv('GOOGLE_CLOUD_PROJECT')}.privacy.fix_suggestions"
        rows = [fix_suggestions]
        self.insert_bigquery_analytics(table_id, rows)

        # Export fix metric to Cloud Monitoring
        self.export_custom_metric(
            metric_type="custom.googleapis.com/agent/fix_suggestions_generated",
            value=len(fix_suggestions.get('fixes', [])),
            labels={"agent": self.agent_id}
        )

        return fix_suggestions

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

    async def _get_gemini_fix_suggestions(self, scan_results: List[ScanResult], compliance_report: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered fix suggestions from Gemini"""
        try:
            # Read file content for context
            file_contents = {result.file_path: await self._get_file_content_for_context(result.file_path) for result in scan_results}
            
            # Generate AI-enhanced fix suggestions
            enhanced_fixes = {}
            for result in scan_results:
                prompt = self._create_fix_prompt(result, file_contents.get(result.file_path))
                ai_response = await self.get_gemini_analysis(prompt, {
                    "violation_type": result.violation_type,
                    "severity": result.severity,
                    "file_path": result.file_path,
                    "line_number": result.line_number
                })
                
                if ai_response:
                    enhanced_fixes[result.file_path] = {
                        "fix_suggestion": self._parse_fix_response(ai_response, result),
                        "file_path": result.file_path,
                        "line_number": result.line_number,
                        "violation_type": result.violation_type,
                        "severity": result.severity
                    }
            
            # Update scan results with AI-enhanced fixes
            for result in scan_results:
                if result.file_path in enhanced_fixes:
                    result.fix_suggestion = enhanced_fixes[result.file_path]["fix_suggestion"]
            
            # Generate summary with AI enhancement
            summary = await self._generate_enhanced_fix_summary(scan_results)
            
            return {
                "summary": {
                    **summary,
                    "fixes_generated": len(scan_results),
                    "ai_enhanced_fixes": len(enhanced_fixes),
                    "priority_fixes": []
                },
                "fixes_by_violation": {result.violation_type: result for result in scan_results},
                "fixes_by_file": {result.file_path: result for result in scan_results},
                "fixes_by_priority": {
                    "critical": [result for result in scan_results if "CRITICAL" in result.description],
                    "high": [result for result in scan_results if "HIGH" in result.description],
                    "medium": [result for result in scan_results if "MEDIUM" in result.description],
                    "low": [result for result in scan_results if "LOW" in result.description]
                },
                "code_patches": [result.fix_suggestion for result in scan_results],
                "gemini_enhanced": self.is_gemini_available()
            }
        except Exception as e:
            self.log_activity(f"Gemini fix suggestions error: {str(e)}", "warning")
            # Return empty structure with proper summary
            return {
                "summary": {
                    "total_violations": len(scan_results),
                    "fixes_generated": len(scan_results),
                    "ai_enhanced_fixes": 0,
                    "priority_fixes": []
                },
                "fixes_by_violation": {},
                "fixes_by_file": {},
                "fixes_by_priority": {
                    "critical": [],
                    "high": [],
                    "medium": [],
                    "low": []
                },
                "code_patches": [],
                "gemini_enhanced": False
            }

    async def _get_file_content_for_context(self, file_path: str) -> Optional[str]:
        """Get file content for AI context"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Limit content to avoid token limits
                return content[:3000] if len(content) > 3000 else content
        except Exception as e:
            self.log_activity(f"Could not read {file_path} for context: {str(e)}", "warning")
            return None

    def _create_fix_prompt(self, violation: ScanResult, file_content: Optional[str]) -> str:
        """Create AI prompt for fix suggestion"""
        context_info = f"\nFile content (first 3000 chars):\n{file_content}" if file_content else "\nFile content not available."
        
        prompt = f"""
You are a privacy compliance expert providing specific code fixes for privacy violations.

Violation Details:
- Type: {violation.violation_type}
- Description: {violation.description}
- Severity: {violation.severity}
- File: {violation.file_path}
- Line: {violation.line_number}
- Regulation: {violation.regulation_reference}
{context_info}

Please provide a specific, actionable code fix that:

1. **Addresses the exact violation** with concrete code changes
2. **Follows security best practices** for the specific violation type
3. **Includes before/after code examples** showing the fix
4. **Explains the security/privacy improvement** made
5. **Considers the programming language** and context
6. **Provides alternative approaches** if applicable

Format your response as:
```code
# Before (problematic code):
[show the problematic code]

# After (fixed code):
[show the corrected code]

# Explanation:
[explain what was fixed and why it's more secure]
```

Focus on practical, implementable solutions that developers can apply immediately.
"""
        return prompt

    def _parse_fix_response(self, ai_response: str, violation: ScanResult) -> str:
        """Parse AI fix response and extract the fix suggestion"""
        try:
            # Clean up the response and extract the fix
            lines = ai_response.strip().split('\n')
            fix_sections = []
            in_code_block = False
            current_section = []
            
            for line in lines:
                if line.startswith('```'):
                    if in_code_block:
                        if current_section:
                            fix_sections.append('\n'.join(current_section))
                        current_section = []
                    in_code_block = not in_code_block
                elif in_code_block:
                    current_section.append(line)
                elif line.startswith('#') and not in_code_block:
                    if current_section:
                        fix_sections.append('\n'.join(current_section))
                    current_section = [line]
                elif not in_code_block:
                    current_section.append(line)
            
            if current_section:
                fix_sections.append('\n'.join(current_section))
            
            # Combine all sections
            if fix_sections:
                return '\n\n'.join(fix_sections)
            else:
                return ai_response.strip()
                
        except Exception as e:
            self.log_activity(f"Error parsing AI fix response: {str(e)}", "warning")
            return ai_response.strip()

    async def _generate_enhanced_fix_summary(self, violations: List[ScanResult]) -> Dict[str, Any]:
        """Generate enhanced fix summary with AI insights"""
        summary = self._generate_fix_summary(violations)
        
        # Enhance with AI if available
        if self.is_gemini_available() and violations:
            try:
                ai_summary = await self._get_gemini_summary_enhancement(violations, summary)
                if ai_summary:
                    summary.update(ai_summary)
            except Exception as e:
                self.log_activity(f"Gemini summary enhancement failed: {str(e)}", "warning")
        
        return summary

    async def _get_gemini_summary_enhancement(self, violations: List[ScanResult], current_summary: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get AI-enhanced summary insights"""
        try:
            violations_data = []
            for v in violations:
                violations_data.append({
                    "type": v.violation_type,
                    "severity": v.severity,
                    "file": v.file_path,
                    "line": v.line_number
                })
            
            prompt = f"""
You are analyzing a privacy compliance fix summary for a codebase.

Current Summary:
{json.dumps(current_summary, indent=2)}

Violations to Fix:
{json.dumps(violations_data, indent=2)}

Please provide enhanced insights including:

1. **Risk Assessment**: Overall risk level and business impact
2. **Implementation Strategy**: Recommended approach for implementing fixes
3. **Testing Recommendations**: How to verify fixes are working
4. **Prevention Measures**: How to prevent similar violations in the future
5. **Compliance Timeline**: Recommended timeline for achieving compliance

Format as JSON:
{{
    "risk_assessment": {{
        "overall_risk": "<HIGH/MEDIUM/LOW>",
        "business_impact": "<description>",
        "compliance_urgency": "<description>"
    }},
    "implementation_strategy": {{
        "approach": "<description>",
        "priority_order": ["<violation_types>"],
        "estimated_timeline": "<timeline>"
    }},
    "testing_recommendations": [
        "<specific test recommendation>"
    ],
    "prevention_measures": [
        "<specific prevention measure>"
    ],
    "compliance_timeline": {{
        "immediate": ["<actions>"],
        "short_term": ["<actions>"],
        "long_term": ["<actions>"]
    }}
}}
"""
            
            ai_response = await self.get_gemini_analysis(prompt, {
                "violation_count": len(violations),
                "current_summary": current_summary
            })
            
            if ai_response:
                return json.loads(ai_response)
                
        except Exception as e:
            self.log_activity(f"Gemini summary enhancement error: {str(e)}", "warning")
        
        return None
    
    async def _get_original_line_content(self, file_path: str, line_number: int) -> Optional[str]:
        """Get the original line content for context"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if 0 < line_number <= len(lines):
                    return lines[line_number - 1].strip()
        except Exception as e:
            self.log_activity(f"Could not read line {line_number} from {file_path}: {str(e)}", "warning")
        
        return None
    
    def _create_specific_fix(self, template: Dict[str, Any], original_line: Optional[str], violation: ScanResult) -> str:
        """Create specific fix suggestion based on template and original line"""
        base_template = template.get('template', 'Review and fix privacy violation')
        
        if original_line:
            # Extract specific values from the original line for more targeted fixes
            specific_fix = self._customize_fix_for_line(base_template, original_line, violation)
            return specific_fix
        
        return base_template
    
    def _customize_fix_for_line(self, template: str, original_line: str, violation: ScanResult) -> str:
        """Customize fix template based on the original line content"""
        violation_type = violation.violation_type
        
        if violation_type == "HardcodedEmail":
            # Extract email from line
            import re
            email_match = re.search(r'["\']([^"\']*@[^"\']*\.[^"\']*)["\']', original_line)
            if email_match:
                email = email_match.group(1)
                return template.replace('{email}', email)
        
        elif violation_type == "SSNExposure":
            # Extract SSN from line
            import re
            ssn_match = re.search(r'["\'](\d{3}-\d{2}-\d{4})["\']', original_line)
            if ssn_match:
                ssn = ssn_match.group(1)
                return template.replace('{ssn}', ssn)
        
        elif violation_type == "CreditCardExposure":
            # Extract credit card from line
            import re
            cc_match = re.search(r'["\'](\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4})["\']', original_line)
            if cc_match:
                card = cc_match.group(1)
                return template.replace('{card}', card)
        
        elif violation_type == "HardcodedSecret":
            # Extract secret from line
            import re
            secret_match = re.search(r'["\']([^"\']{10,})["\']', original_line)
            if secret_match:
                secret = secret_match.group(1)
                return template.replace('{secret}', secret)
        
        return template
    
    def _generate_fix_summary(self, violations: List[ScanResult]) -> Dict[str, Any]:
        """Generate summary of fix suggestions"""
        summary = {
            "total_violations": len(violations),
            "fix_priorities": {
                "CRITICAL": len([v for v in violations if "CRITICAL" in v.description]),
                "HIGH": len([v for v in violations if "HIGH" in v.description]),
                "MEDIUM": len([v for v in violations if "MEDIUM" in v.description]),
                "LOW": len([v for v in violations if "LOW" in v.description])
            },
            "estimated_efforts": {},
            "fix_categories": {
                "environment_variables": len([v for v in violations if "os.getenv" in v.fix_suggestion]),
                "encryption": len([v for v in violations if "encrypt" in v.fix_suggestion.lower()]),
                "consent_mechanisms": len([v for v in violations if "consent" in v.fix_suggestion.lower()]),
                "secure_storage": len([v for v in violations if "secure" in v.fix_suggestion.lower()]),
                "https_upgrade": len([v for v in violations if "https" in v.fix_suggestion.lower()])
            }
        }
        
        # Calculate effort breakdown
        for violation in violations:
            effort_match = re.search(r'Estimated Effort: ([^|]+)', violation.description)
            if effort_match:
                effort = effort_match.group(1).strip()
                if effort not in summary["estimated_efforts"]:
                    summary["estimated_efforts"][effort] = 0
                summary["estimated_efforts"][effort] += 1
        
        return summary
    
    def _calculate_total_effort(self, violations: List[ScanResult]) -> str:
        """Calculate total estimated effort for all fixes"""
        total_minutes = 0
        
        for violation in violations:
            effort_match = re.search(r'Estimated Effort: (\d+) minutes', violation.description)
            if effort_match:
                total_minutes += int(effort_match.group(1))
        
        if total_minutes < 60:
            return f"{total_minutes} minutes"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours} hours {minutes} minutes"

    async def _generate_hardcoded_fixes(self, violations: List[ScanResult]) -> Dict[str, Any]:
        """Generate hardcoded fix suggestions"""
        hardcoded_fixes = {}
        for violation in violations:
            template = self.fix_templates.get(violation.violation_type, {})
            if template:
                original_line = await self._get_original_line_content(violation.file_path, violation.line_number)
                specific_fix = self._create_specific_fix(template, original_line, violation)
                hardcoded_fixes[violation.file_path] = {
                    "fix_suggestion": specific_fix,
                    "file_path": violation.file_path,
                    "line_number": violation.line_number,
                    "violation_type": violation.violation_type,
                    "severity": violation.severity
                }
            else:
                hardcoded_fixes[violation.file_path] = {
                    "fix_suggestion": f"Review and fix {violation.violation_type} violation manually.",
                    "file_path": violation.file_path,
                    "line_number": violation.line_number,
                    "violation_type": violation.violation_type,
                    "severity": violation.severity
                }
        
        return {
            "summary": {
                **self._generate_fix_summary(violations),
                "fixes_generated": len(violations),
                "ai_enhanced_fixes": 0,
                "priority_fixes": []
            },
            "fixes_by_violation": {violation.violation_type: violation for violation in violations},
            "fixes_by_file": {violation.file_path: violation for violation in violations},
            "fixes_by_priority": {
                "critical": [violation for violation in violations if "CRITICAL" in violation.description],
                "high": [violation for violation in violations if "HIGH" in violation.description],
                "medium": [violation for violation in violations if "MEDIUM" in violation.description],
                "low": [violation for violation in violations if "LOW" in violation.description]
            },
            "code_patches": [hardcoded_fixes[file_path]["fix_suggestion"] for file_path in hardcoded_fixes],
            "gemini_enhanced": False
        } 