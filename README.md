# Privacy Guardian Agents (ADK Hackathon Edition)

## 🚀 Overview

**Privacy Guardian Agents** by Privacy License (https://www.privacylicense.ai) is a multi-agent privacy enforcement system built for the Google Cloud Agent Development Kit (ADK) Hackathon. It includes collaborative, event-driven system of AI agents that autonomously scan, analyze, and remediate privacy vulnerabilities in codebases.

- **Multi-agent orchestration** (Python, ADK-style)
- **Google Cloud integration**: Vertex AI (Gemini), Cloud Run, Cloud Storage, Bigquery, Gemini, ADK, Vertex AI, Secret Manager, Cloud Logging, Cloud monitoring, Cloud Build, Cloud Load balancing, Cloud DNS, Cloud Pub/sub, Cloud Security Command Center, Cloud Asset Inventory, Cloud IAM, Cloud Security etc
- **Modern web UI** for real-time scanning and results
- **Supported Programming language scanning** : 12+ Programming languages like Python, Typescript, Javascript, Java, Go, C#, PHP, Ruby, Swift, Kotlin, Rust, Scala etc. 
- **Event-driven, modular, hackathon-ready**

### 📚 **Documentation & Resources**
- **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)** - Complete system architecture with detailed diagrams
- **[BLOG_POST.md](BLOG_POST.md)** - Technical blog post: "How I Built a Multi-Agent Privacy Guardian with Google Cloud ADK + Vertex AI"
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive deployment guide
- **[QUICK_START.md](QUICK_START.md)** - Quick start instructions
- **[LICENSE](LICENSE)** - MIT License with Commons Clause (commercial use restrictions)

---

## 🔍 What Can It Scan? Comprehensive Privacy Detection

Privacy Guardian Agents integrates a powerful TypeScript RuleEngine with **12 specialized privacy rules** that detect violations across multiple categories. The PrivacyScanAgent supports **50+ violation types** that all downstream agents can process:

### 🎯 **Core Violation Types (50+ Types)**

#### **🆔 PII Detection (20+ Types)**
- **HardcodedEmail**: Email addresses hardcoded in source code
- **SSNExposure**: Social Security Number patterns and exposure
- **CreditCardExposure**: Credit card number patterns and PCI violations
- **PassportExposure**: Passport number detection
- **PhoneNumberExposure**: Phone number patterns in code
- **BankAccountExposure**: Bank account number detection
- **DriversLicenseExposure**: Driver's license number patterns
- **NationalIdExposure**: National ID number detection
- **AddressExposure**: Street addresses, ZIP codes, postal codes
- **MedicalDataExposure**: Medical record numbers, licenses, codes
- **BiometricDataExposure**: Biometric data and hash patterns
- **HardcodedSecret**: API keys, passwords, tokens, credentials

#### **🔐 Security & Encryption (8 Types)**
- **InsecureConnection**: HTTP URLs instead of HTTPS
- **TLSDisabled**: TLS/SSL encryption disabled
- **EncryptionViolation**: Missing encryption for sensitive data
- **RawPiiAsPrimaryKey**: Using raw PII as database primary keys
- **MissingRateLimiting**: API endpoints without rate limiting
- **MissingEncryptionAtRest**: Database tables without encryption
- **UnencryptedDataWrite**: Writing sensitive data without encryption
- **PiiHashingFound**: Proper PII hashing/tokenization (positive)

#### **📋 Consent & Privacy Policy (8 Types)**
- **ConsentViolation**: Data collection without proper consent markers
- **MissingPurposeLimitation**: Personal data without purpose specification
- **MissingProfilingOptOut**: Profiling without opt-out verification
- **DisabledOptOut**: Opt-out mechanisms disabled
- **ForcedConsent**: Forced consent violations
- **DefaultEnabledConsent**: Default enabled data collection
- **RightToBeForgottenViolation**: Improper deletion mechanisms
- **DoNotSellViolation**: CCPA "Do not sell" violations

#### **🔄 Data Flow & Handling (10 Types)**
- **SensitiveDataSource**: Sensitive data source detection
- **DataMaskingFound**: Proper data masking/anonymization (positive)
- **UnsanitizedStackTrace**: Stack traces without PII scrubbing
- **DataSharingViolation**: Third-party data sharing without protection
- **DataRetentionViolation**: Missing retention policies
- **MissingDSARRegistration**: Missing DSAR compliance registration
- **LoggingViolation**: PII in logs and console output
- **ThirdPartyDataSharing**: Third-party integration without protection
- **ApprovedEndpointsFound**: Proper endpoint allowlisting (positive)
- **RetentionTimerFound**: Proper retention timers (positive)

#### **🏗️ Advanced Privacy (8 Types)**
- **MissingFieldLevelAccessScoping**: GraphQL/REST fields without scoping
- **AdTrackingCode**: Ad/tracking code without consent checks
- **RegionLockViolation**: Cloud regions outside EEA for EU data
- **LargePiiTableJoin**: Large PII table joins without safety
- **MLPipelineDataMinimization**: ML training without data minimization
- **ApiVersionFound**: API versioning without privacy contract versioning
- **NewDatabaseColumn**: New columns without necessity verification
- **FieldScopingFound**: Proper field-level access scoping (positive)

#### **👨‍💻 Developer Guidance (8 Types)**
- **ObjectCreationWithPii**: Creating objects with PII
- **DataStorageOperation**: Storing personal data
- **CommunicationWithPii**: Sending communications with PII
- **DataExportWithPii**: Exporting data with PII
- **ApiEndpointWithPii**: API endpoints returning PII
- **DatabaseSchemaWithPii**: Database schemas with PII
- **CachingWithPii**: Caching operations with PII
- **SearchQueryWithPii**: Search queries with PII

#### **🤖 AI Privacy (4 Types)**
- **ExcessiveDataCollection**: Collecting more data than necessary
- **IncompleteDataDeletion**: Incomplete data deletion workflows
- **ExcessiveDataBackup**: Excessive data backup practices
- **DataMinimizationViolation**: Violations of data minimization principle

### 🔧 **Detection Capabilities**

#### **Pattern-Based Detection**
- **50+ PII patterns**: SSN, credit cards, passports, addresses, medical data
- **Security patterns**: HTTP, TLS, encryption, rate limiting
- **Consent patterns**: Opt-in/opt-out, purpose limitation, profiling
- **Data flow patterns**: Masking, sharing, retention, DSAR compliance

#### **Context-Aware Analysis**
- **Multi-language support**: JavaScript, TypeScript, Java, Python, Go, C#, PHP, Ruby, Swift, Kotlin, Rust, Scala
- **Framework detection**: GraphQL, REST, ORM, database operations
- **Cloud integration**: AWS, GCP, Azure region compliance
- **ML/AI pipeline**: Data minimization in training operations

#### **Positive Pattern Recognition**
- **Good practices**: Encryption annotations, consent markers, data masking
- **Compliance indicators**: DSAR registration, retention timers, field scoping
- **Security measures**: Rate limiting, approved endpoints, EU compliance

### 📊 **Compliance Coverage**

#### **GDPR Compliance**
- **Article 4**: Personal data definitions
- **Article 5**: Data processing principles
- **Article 6**: Lawfulness of processing
- **Article 7**: Conditions for consent
- **Article 9**: Special categories of data
- **Article 15-22**: Data subject rights
- **Article 25**: Privacy by design
- **Article 28**: Processor obligations
- **Article 32**: Security of processing
- **Article 44**: Data transfers

#### **CCPA Compliance**
- **Section 1798.100**: Consumer rights
- **Section 1798.105**: Right to deletion
- **Section 1798.120**: Right to opt-out
- **Section 1798.140**: Definitions

#### **Other Regulations**
- **PCI DSS**: Payment card security
- **HIPAA**: Medical data protection
- **Industry standards**: Best practices and guidelines

### 🔄 **Security & Encryption Violations**
- **Encryption-at-Rest**: Missing encryption for sensitive data storage
- **TLS/HTTPS**: Insecure HTTP connections, disabled TLS
- **Hash/Tokenization**: Raw PII used as primary keys without hashing
- **Rate Limiting**: Public endpoints returning personal data without rate limits
- **Key Management**: Insecure key storage practices

### 📋 **Consent & Privacy Policy Compliance**
- **Explicit Consent**: Missing `@consent_required` annotations for data capture
- **Purpose Limitation**: PII fields without `data_purpose=` specifications
- **Profiling Opt-Out**: Missing `profiling_disabled=true` checks
- **GDPR "Right to be Forgotten"**: Improper deletion mechanisms
- **CCPA "Do Not Sell"**: Violations of opt-out rights
- **Data Minimization**: Excessive data collection beyond stated purposes

### 🔄 **Data Flow & Handling**
- **Sensitive Payload Flow**: PII flowing without proper masking/anonymization
- **Raw PII Logging**: Personal data in logs without masking
- **Stack Trace Sanitization**: Unsanitized error traces exposing PII
- **Third-Party Sharing**: Data sharing without proper agreements
- **Retention Policies**: Missing automatic deletion mechanisms
- **DSAR Compliance**: Missing Data Subject Access Request registration

### 🤖 **AI & Advanced Privacy**
- **Field-Level Access Scoping**: Missing `@scope` directives for PII fields
- **Ad/Tracking Code**: Tracking on opt-out pages without consent checks
- **Region-Lock Enforcement**: EU data outside EEA without proper mechanisms
- **Join-Safety**: Unsafe joins between large PII tables
- **ML Pipeline Data Minimization**: Loading unused sensitive columns
- **Versioned Privacy Contracts**: API changes without PII field updates
- **Least-Privilege Validation**: Database columns not referenced elsewhere

### 🧠 **AI-Powered Analysis**
- **Context-Aware Explanations**: Plain-English violation descriptions
- **Specific Code Fixes**: Actionable remediation with code examples
- **Legal Compliance Mapping**: References to specific GDPR/CCPA articles
- **Risk Assessment**: Prioritization of violations by severity
- **Developer Guidance**: Step-by-step fix instructions

### 📊 **Regulations Covered**
- **GDPR**: Articles 4, 5, 6, 7, 9, 17, 20, 22, 25, 28, 32, 34
- **CCPA**: Sections 1798.100, 1798.110, 1798.115, 1798.120, 1798.140, 1798.150
- **HIPAA**: Protected Health Information requirements
- **PCI DSS**: Credit card data protection standards
- **Regional Laws**: Various international data protection regulations

### 🔧 **Supported Languages & Frameworks**
- **Languages**: JavaScript, TypeScript, Java, Python, Go, C#, PHP, Ruby, Swift, Kotlin, Rust, Scala
- **Frameworks**: GraphQL, REST APIs, Database schemas, ML pipelines
- **Cloud Platforms**: AWS, GCP, Azure integrations
- **Development Tools**: Logging systems, error handling, CI/CD pipelines

---

## 🧠 Multi-Agent System Architecture

| Agent Name             | Description                                                                     |
| ---------------------- | ------------------------------------------------------------------------------- |
| 🕵️ PrivacyScanAgent   | Scans the codebase using TypeScript RuleEngine and emits FindingsReady events  |
| 🤖 GeminiAnalysisAgent | Enhances findings with Gemini AI and emits AIEnhancedFindings events           |
| 🧑‍⚖️ ComplianceAgent  | Maps findings to GDPR/CCPA/HIPAA regulations and emits ComplianceAnalysisCompleted |
| 🛠️ FixSuggestionAgent | Generates AI-powered fix suggestions and emits FixSuggestionsCompleted events |
| 📋 ReportAgent         | Compiles comprehensive reports and emits ReportGenerated events                |

### Event-Based Architecture

The Privacy Guardian system uses ADK's event-based architecture for seamless agent collaboration:

#### Event Flow
```
PrivacyScanAgent → GeminiAnalysisAgent → ComplianceAgent → FixSuggestionAgent → ReportAgent
      │                    │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼                    ▼
FindingsReady    AIEnhancedFindings    ComplianceAnalysis    FixSuggestions    ReportGenerated
```

#### Agent Event Communication

**PrivacyScanAgent** emits `FindingsReady` event:
- Contains initial scan results from TypeScript RuleEngine
- No AI enhancement (delegated to GeminiAnalysisAgent)
- Focuses solely on rule-based detection

**GeminiAnalysisAgent** listens for `FindingsReady`, emits `AIEnhancedFindings`:
- Receives scan results from PrivacyScanAgent
- Enhances violations with Gemini AI analysis
- Discovers additional violations through AI
- Emits enhanced results for downstream agents

**ComplianceAgent** listens for `AIEnhancedFindings`, emits `ComplianceAnalysisCompleted`:
- Receives enhanced results from GeminiAnalysisAgent
- Maps violations to GDPR, CCPA, HIPAA, PCI-DSS regulations
- Provides compliance scoring and risk assessment
- Emits compliance analysis for fix suggestions

**FixSuggestionAgent** listens for `ComplianceAnalysisCompleted`, emits `FixSuggestionsCompleted`:
- Receives enhanced results and compliance analysis
- Generates AI-powered fix suggestions
- Provides code patches and implementation guidance
- Emits fix recommendations for report generation

**ReportAgent** listens for `FixSuggestionsCompleted`, emits `ReportGenerated`:
- Receives all previous agent outputs
- Generates comprehensive privacy audit report
- Stores results in GCS or Firestore
- Emits final report with storage location

#### Agent Responsibilities
- **PrivacyScanAgent**: Pure rule-based detection using TypeScript RuleEngine
- **GeminiAnalysisAgent**: AI enhancement and additional violation discovery
- **ComplianceAgent**: Regulatory mapping and compliance analysis
- **FixSuggestionAgent**: Code fix generation and implementation guidance
- **ReportAgent**: Comprehensive report generation and storage

#### Benefits of Event-Based Architecture
- **Clean Separation of Concerns**: Each agent has a single, well-defined responsibility
- **No Code Duplication**: Eliminated all duplicate logic across agents
- **Scalable Design**: Event-driven architecture allows easy agent addition/modification
- **Clear Data Flow**: Explicit event-based communication between agents
- **AI Integration Preserved**: Gemini AI capabilities maintained in each agent with fallbacks

---

## 🏗️ Architecture Diagram (Text Version)

> 📋 **For a complete visual architecture diagram with detailed component breakdowns, see [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)**

```
                         ┌────────────────────┐
                         │  Web UI (Cloud Run)│
                         └────────▲───────────┘
                                  │
                             Triggers Scan
                                  │
                          ┌───────┴─────────────┐
                          │ Agent Orchestrator  │  <-- ADK Runtime
                          └───────┬─────────────┘
                                  │
   ┌──────────────────────────────┼────────────────────────────────────────────┐
   ▼                              ▼                                            ▼
PrivacyScanAgent → GeminiAnalysisAgent → ComplianceAgent → FixSuggestionAgent → ReportAgent
        │            Uses Vertex AI            │             │                    │
        ▼                                      ▼             ▼                    ▼
FindingsReady    AIEnhancedFindings    ComplianceAnalysis    FixSuggestions    ReportGenerated
```

### Event Flow Architecture

The system follows a linear event-driven flow where each agent:
1. **Listens** for events from the previous agent
2. **Processes** data using its specialized capabilities
3. **Emits** events for the next agent to consume
4. **Maintains** AI integration with graceful fallbacks

### Key Architectural Benefits

- **Decoupled Agents**: Each agent operates independently through events
- **Scalable Design**: Easy to add new agents or modify existing ones
- **Clear Data Flow**: Explicit event communication between agents
- **AI Integration**: Gemini AI capabilities in each agent with fallbacks
- **Fault Tolerance**: Graceful degradation when AI is unavailable

## ☁️ **Comprehensive Google Cloud Integration**

Privacy Guardian Agents leverages the full power of Google Cloud for a production-ready, scalable solution:

### **Core Google Cloud Services**

#### **🤖 Vertex AI (Gemini 2.0 Flash)**
- **Primary AI Engine**: All agents use Gemini AI for intelligent analysis
- **Model Management**: Automatic model selection and fallback
- **Real-time Processing**: Low-latency AI responses for live scanning
- **Cost Optimization**: Efficient token usage and batch processing
- **AI Enhancement**: Context-aware violation analysis and discovery
- **Fix Generation**: AI-powered code fix suggestions with implementation guidance

#### **🚀 Cloud Run**
- **Web UI Deployment**: Modern, scalable web interface
- **Agent Orchestrator**: ADK runtime environment
- **Auto-scaling**: Handles variable scan workloads
- **Serverless**: Pay-per-use pricing model
- **Container Deployment**: Docker-based agent deployment
- **HTTPS Endpoints**: Secure API access

#### **📦 Cloud Storage**
- **Report Storage**: Secure, durable report storage
- **Version Control**: Historical report tracking
- **Access Control**: Fine-grained permissions
- **Global CDN**: Fast report access worldwide
- **JSON Report Storage**: Structured report data storage
- **PDF Report Storage**: Human-readable report formats

#### **🗄️ BigQuery**
- **Privacy Analytics**: Large-scale privacy violation analysis
- **Trend Analysis**: Historical compliance tracking
- **Custom Dashboards**: Privacy posture visualization
- **ML Pipeline**: Advanced privacy pattern detection
- **Scan Results Storage**: Structured violation data storage
- **Compliance Analytics**: Regulatory compliance tracking
- **Performance Metrics**: System optimization insights

#### **🔐 Secret Manager**
- **API Key Management**: Secure Gemini API key storage
- **Credential Rotation**: Automatic key updates
- **Access Control**: Role-based credential access
- **Audit Logging**: Complete access tracking
- **Environment Variables**: Secure configuration management
- **Service Account Keys**: Secure credential storage

#### **📝 Cloud Logging**
- **Structured Logging**: Agent activity and performance tracking
- **Error Monitoring**: Real-time issue detection
- **Compliance Auditing**: Complete audit trail
- **Performance Metrics**: System optimization insights
- **Agent Activity Logs**: Detailed agent interaction tracking
- **Event Correlation**: End-to-end request tracing

#### **📊 Cloud Monitoring**
- **Agent Performance**: Real-time agent health monitoring
- **AI Usage Tracking**: Gemini API usage optimization
- **Cost Monitoring**: Cloud resource cost tracking
- **Alert Management**: Proactive issue notification
- **Custom Metrics**: Privacy violation detection metrics
- **Performance Dashboards**: System health visualization
- **Resource Utilization**: Cloud service usage optimization

### **Advanced Google Cloud Features**

#### **🔄 Cloud Functions**
- **Event Triggers**: Automatic scan initiation
- **Webhook Integration**: CI/CD pipeline integration
- **Scheduled Scans**: Automated compliance monitoring
- **Real-time Notifications**: Instant violation alerts
- **Serverless Processing**: Event-driven scan processing
- **API Gateway**: RESTful API endpoints

#### **🌐 Cloud Load Balancing**
- **Global Distribution**: Multi-region deployment
- **Health Checks**: Automatic failover
- **SSL Termination**: Secure HTTPS connections
- **Traffic Management**: Intelligent request routing
- **Load Distribution**: Scalable traffic handling
- **Regional Routing**: Geographic compliance routing

#### **🔍 Cloud Build**
- **CI/CD Pipeline**: Automated deployment pipeline
- **Container Building**: Docker image creation
- **Security Scanning**: Container vulnerability scanning
- **Artifact Storage**: Build artifact management
- **Multi-stage Builds**: Optimized deployment process
- **Integration Testing**: Automated testing pipeline

#### **🛡️ Cloud Security Command Center**
- **Security Posture**: Overall security assessment
- **Vulnerability Scanning**: Security issue detection
- **Compliance Monitoring**: Regulatory compliance tracking
- **Risk Assessment**: Security risk quantification
- **Threat Detection**: Advanced threat monitoring
- **Security Analytics**: Security trend analysis

#### **📋 Cloud Asset Inventory**
- **Resource Discovery**: Automatic asset discovery
- **Compliance Mapping**: Resource compliance tracking
- **Change Tracking**: Asset modification monitoring
- **Policy Enforcement**: Automated policy compliance
- **Asset Classification**: Sensitive data identification
- **Inventory Management**: Resource organization

#### **🔐 Identity and Access Management (IAM)**
- **Role-Based Access**: Fine-grained permission control
- **Service Accounts**: Secure service authentication
- **Policy Management**: Access policy enforcement
- **Audit Logging**: Access attempt tracking
- **Multi-factor Authentication**: Enhanced security
- **Conditional Access**: Context-aware permissions

#### **🌍 Cloud DNS**
- **Domain Management**: Custom domain configuration
- **Load Balancing**: DNS-based load distribution
- **Health Checks**: Domain health monitoring
- **Geographic Routing**: Regional traffic routing
- **Security**: DNS security features
- **Performance**: Fast DNS resolution

#### **📡 Cloud Pub/Sub**
- **Event Streaming**: Real-time event processing
- **Agent Communication**: Inter-agent message passing
- **Scalable Messaging**: High-throughput message handling
- **Reliable Delivery**: Guaranteed message delivery
- **Topic Management**: Organized message routing
- **Subscription Management**: Flexible message consumption

### **Google Cloud Architecture Benefits**

- **Global Scale**: Deployable worldwide with regional compliance
- **Enterprise Security**: SOC 2, ISO 27001, GDPR compliance
- **Cost Optimization**: Pay-per-use with automatic scaling
- **Developer Experience**: Integrated tooling and APIs
- **Future-Proof**: Latest AI and cloud innovations
- **High Availability**: 99.9%+ uptime guarantees
- **Data Residency**: Regional data storage compliance
- **Backup & Recovery**: Automated disaster recovery
- **Monitoring & Alerting**: Proactive issue detection
- **Compliance Certifications**: Industry-standard compliance

---

## 🚀 **Current Project Status & How to Run**

### ✅ **What's Working Now**

The Privacy Guardian Agents system is **fully functional** with the following capabilities:

1. **✅ TypeScript RuleEngine Bridge**: Successfully bridges TypeScript RuleEngine to Python
2. **✅ PrivacyScanAgent CLI**: Standalone CLI for local testing and scanning
3. **✅ Multi-Agent Orchestration**: All 5 agents working together via events
4. **✅ Google Cloud Integration**: BigQuery, Secret Manager, Cloud Monitoring, Cloud Storage
5. **✅ Privacy Violation Detection**: Successfully detects hardcoded emails, PII, and security violations
6. **✅ Structured Logging**: Production-grade logging with Google Cloud integration
7. **✅ Custom Metrics**: Cloud Monitoring integration for scan analytics

### 🔧 **Recent Fixes & Improvements**

1. **✅ Fixed TypeScript RuleEngine Bridge**: Resolved JSON parsing issues and improved error handling
2. **✅ Added PrivacyScanAgent CLI**: Created standalone CLI for local testing
3. **✅ Fixed Cloud Monitoring**: Resolved protobuf timestamp issues for custom metrics
4. **✅ Enhanced Error Handling**: Improved fallback mechanisms and error reporting
5. **✅ Structured Logging**: Implemented production-grade logging with Google Cloud

### 🚀 **How to Run the System**

#### **Prerequisites**

1. **Python 3.8+** with virtual environment
2. **Node.js 16+** for TypeScript compilation
3. **Google Cloud Project** with APIs enabled
4. **Environment variables** configured

#### **Step 1: Install Dependencies**

```bash
# Clone the repository
git clone <repository-url>
cd agenthack

# Install Node.js dependencies
npm install

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

#### **Step 2: Configure Environment Variables**

Create a `.env` file in the project root:

```bash
# Google Cloud Configuration
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# Gemini AI Configuration
export GEMINI_API_KEY="your-gemini-api-key"

# Cloud Storage Configuration
export GCS_BUCKET_NAME="privacy-guardian-reports"

# Optional: Custom configuration
export GEMINI_MODEL="gemini-2.0-flash"
export GEMINI_MAX_TOKENS="2000"
export GEMINI_TEMPERATURE="0.1"
```

#### **Step 3: Enable Google Cloud APIs**

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable monitoring.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
```

#### **Step 4: Run the System**

##### **Option A: Full Multi-Agent Orchestration**

```bash
# Run the complete system with all 5 agents
source venv/bin/activate
python agent_orchestrator.py --project-path /path/to/your/codebase
```

**Expected Output:**
```
✅ TypeScript RuleEngine imported successfully via Python bridge
🤖 Initializing Privacy Guardian Agents...
✅ Gemini AI initialized for 🔍 PrivacyScanAgent
✅ BigQuery client initialized successfully
✅ Secret Manager client initialized successfully
✅ Cloud Monitoring client initialized successfully
✅ Cloud Storage client initialized successfully
🚀 Starting privacy scan...
✅ Scan Complete!
📊 Total Violations Found: X
```

##### **Option B: PrivacyScanAgent CLI (Local Testing)**

```bash
# Test the PrivacyScanAgent directly on a directory
source venv/bin/activate
python agents/privacy_scan_agent.py /path/to/test/directory --verbose
```

**Expected Output:**
```
✅ TypeScript RuleEngine imported successfully via Python bridge
🔍 PrivacyScanAgent - Local Testing
==================================================
📁 Project path: /path/to/test/directory
📊 RuleEngine Status: available
🚀 Starting scan...
DEBUG: Found X violations from TypeScript RuleEngine
✅ Scan Complete!
📊 Total Violations Found: X

🚨 Privacy Violations Found:
--------------------------------------------------------------------------------
1. HardcodedEmail - MEDIUM
   📄 File: path/to/file.java:3
   📝 Description: Avoid hardcoding email addresses
   🛠️  Fix: Replace hardcoded email 'test@example.com' with environment variable
   📋 Regulations: GDPR, CCPA
```

##### **Option C: Web UI (Development)**

```bash
# Start the web server
source venv/bin/activate
python web_server.py

# Open http://localhost:8000 in your browser
```

#### **Step 5: Test with Sample Code**

The system includes test files in the `tests/` directory:

```bash
# Test with Java file containing hardcoded emails
python agents/privacy_scan_agent.py tests/java/ --verbose

# Test with multi-language samples
python agents/privacy_scan_agent.py tests/multi-language/ --verbose
```

### 📊 **What You'll See**

#### **Successful Scan Results**
- ✅ TypeScript RuleEngine imported successfully
- ✅ All Google Cloud services connected
- ✅ Privacy violations detected and categorized
- ✅ Compliance mapping (GDPR, CCPA, HIPAA)
- ✅ AI-enhanced descriptions and fix suggestions
- ✅ Custom metrics exported to Cloud Monitoring
- ✅ Structured logging with Google Cloud

#### **Sample Violation Output**
```
🚨 Privacy Violations Found:
--------------------------------------------------------------------------------
1. HardcodedEmail - MEDIUM
   📄 File: tests/java/UserEmailService.java:3
   📝 Description: Avoid hardcoding email addresses
   🛠️  Fix: Replace hardcoded email 'test@example.com' with environment variable
   📋 Regulations: GDPR, CCPA

2. DataFlowViolation - HIGH
   📄 File: tests/java/UserEmailService.java:3
   📝 Description: Sensitive data source detected
   🛠️  Fix: Implement taint tracking and ensure PII flows through mask()/anonymize()
   📋 Regulations: GDPR Article 25, CCPA Section 1798.100
```

### 🔍 **Troubleshooting**

#### **Common Issues & Solutions**

1. **TypeScript RuleEngine Import Error**
   ```bash
   # Ensure Node.js dependencies are installed
   npm install
   
   # Check if rule_engine_cli.js exists
   ls -la rule_engine_cli.js
   ```

2. **Google Cloud Authentication Error**
   ```bash
   # Authenticate with Google Cloud
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   
   # Verify credentials
   gcloud auth list
   ```

3. **Missing Environment Variables**
   ```bash
   # Check environment variables
   echo $GOOGLE_CLOUD_PROJECT
   echo $GEMINI_API_KEY
   
   # Set if missing
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GEMINI_API_KEY="your-api-key"
   ```

4. **Python Virtual Environment Issues**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   
   # Reinstall dependencies if needed
   pip install -r requirements.txt
   ```

#### **Performance Monitoring**

The system provides comprehensive monitoring:

```bash
# Check agent status
curl http://localhost:8000/api/agents/status

# View Cloud Monitoring metrics
gcloud monitoring metrics list --filter="metric.type:custom.googleapis.com/agent"

# Check BigQuery analytics
bq query "SELECT * FROM \`your-project.privacy.scan_results\` LIMIT 10"
```

### 🎯 **Next Steps**

1. **Test with Your Codebase**: Run the system on your own code to see privacy violations
2. **Customize Rules**: Modify TypeScript rules in `src/ruleEngine/rules/` for your needs
3. **Deploy to Production**: Use the deployment scripts in `DEPLOYMENT.md`
4. **Integrate with CI/CD**: Add to your development pipeline for continuous monitoring

---

## ✨ Key Features

- **Seamless ADK Orchestration**: Each agent is a Python class, event-driven, and hackathon-ready.
- **Google Cloud Native**: Vertex AI for AI analysis, Cloud Storage for reports, Cloud Run for web UI.
- **Modern Web UI**: Drag-and-drop upload, real-time progress, agent status, and results.
- **Audit-Ready Reports**: PDF and JSON output, GCS upload, and compliance mapping.
- **Extensible**: Add new agents or rules easily for future privacy frameworks.

## 🚀 **Innovation & Creativity Highlights**

### **🎯 Novel Multi-Agent Privacy Architecture**
Privacy Guardian Agents introduces a **first-of-its-kind event-driven privacy compliance system** that transforms how organizations approach privacy vulnerability detection:

#### **Revolutionary Event-Based Agent Collaboration**
- **Industry First**: Event-driven privacy agents with explicit data flow
- **Zero Duplication**: Eliminated redundant logic across agents through clean separation
- **Scalable Design**: Easy to add new privacy frameworks or compliance regulations
- **Real-time Processing**: Live agent communication with immediate feedback

#### **AI-Powered Privacy Intelligence**
- **Context-Aware Analysis**: Gemini AI understands code context and business impact
- **Dynamic Violation Discovery**: AI finds privacy issues beyond rule-based detection
- **Intelligent Fix Generation**: Context-aware code fixes with implementation guidance
- **Strategic Recommendations**: Business-focused privacy improvement roadmap

### **🔬 Technical Innovation**

#### **Hybrid Detection Engine**
- **TypeScript RuleEngine**: Comprehensive 50+ violation pattern detection
- **Gemini AI Enhancement**: Context-aware violation analysis and discovery
- **Fallback Mechanisms**: Robust system that works with or without AI
- **Multi-language Support**: JavaScript, TypeScript, Java, Python, Go, C#, PHP, Ruby, Swift, Kotlin, Rust, Scala

#### **Advanced Event Orchestration**
- **ADK Integration**: Native Agent Development Kit implementation
- **Event Sourcing**: Complete audit trail of all agent interactions
- **Correlation Tracking**: End-to-end request tracing across all agents
- **Performance Optimization**: Efficient event processing with minimal latency

### **💡 Creative Problem Solving**

#### **Privacy Compliance Automation**
- **DevSecOps Integration**: Seamless CI/CD pipeline integration
- **Real-time Monitoring**: Continuous privacy posture assessment
- **Automated Remediation**: AI-generated fix suggestions with implementation steps
- **Compliance Reporting**: Audit-ready reports for regulatory submissions

#### **Business Impact Focus**
- **Risk Quantification**: Financial and reputational impact assessment
- **Strategic Planning**: Long-term privacy strategy recommendations
- **Resource Optimization**: Effort estimation and prioritization
- **ROI Calculation**: Privacy investment return on investment analysis

### **🌟 Unique Value Proposition**

#### **Industry Problem Solved**
- **$2.7B in GDPR fines** in 2023 alone - Privacy Guardian prevents these violations
- **Manual privacy reviews** take weeks - Automated scanning takes minutes
- **Inconsistent compliance** across teams - Standardized, AI-powered analysis
- **Reactive privacy management** - Proactive, continuous monitoring

#### **Competitive Advantages**
- **Event-Driven Architecture**: Industry-first privacy agent collaboration
- **AI-Native Design**: Built for AI from the ground up, not retrofitted
- **Google Cloud Native**: Leverages latest cloud and AI innovations
- **Open Source Foundation**: TypeScript RuleEngine with Python ADK orchestration

---

## 📦 Technologies Used

- Google Cloud Vertex AI (Gemini 2.0 Flash)
- Google Cloud Run
- Google Cloud Storage (report output)
- Google Agent Development Kit (Python)
- FastAPI (web server)
- Node.js + TypeScript (original rule engine)
- ADK Orchestrator in Python (new)
- GitLab CI/CD + GitHub Actions

---

## 📝 Hackathon Submission Description

> **Privacy Guardian Agents** is a revolutionary multi-agent AI system built with Google Cloud's Agent Development Kit (ADK) that transforms privacy compliance from a manual, error-prone process into an automated, intelligent workflow. 

> **The Problem**: Privacy violations cost companies $2.7B in fines annually, with manual reviews taking weeks and producing inconsistent results. Traditional tools lack context awareness and provide generic, often unhelpful recommendations.

> **The Solution**: An event-driven multi-agent system orchestrating five specialized AI agents—PrivacyScanAgent, GeminiAnalysisAgent, ComplianceAgent, FixSuggestionAgent, and ReportAgent—that work together to detect, analyze, and remediate privacy vulnerabilities in real-time.

> **Technical Innovation**: Built natively with ADK (Python), the system introduces the industry's first event-driven privacy compliance architecture. Each agent listens for events from previous agents and emits events for downstream processing, creating a seamless, scalable workflow that eliminates code duplication and enables easy extension.

> **Google Cloud Integration**: Leverages Vertex AI (Gemini 2.0 Flash) for context-aware analysis, Cloud Run for scalable deployment, Cloud Storage for report management, BigQuery for analytics, and Secret Manager for secure credential management.

> **Business Impact**: Reduces privacy review time from weeks to minutes, prevents millions in potential fines, and provides actionable, AI-generated code fixes with implementation guidance. Designed for DevSecOps teams, it integrates seamlessly into CI/CD pipelines and provides audit-ready reports for regulatory compliance.

> **Key Features**: 50+ violation types detected, multi-language support (JavaScript, TypeScript, Java, Python, Go, C#, PHP, Ruby, Swift, Kotlin, Rust, Scala), GDPR/CCPA/HIPAA/PCI-DSS compliance mapping, AI-powered fix generation, and comprehensive reporting with Google Cloud Storage integration.

> This project demonstrates the power of ADK for building sophisticated multi-agent systems that solve real-world problems while showcasing the full potential of Google Cloud's AI and infrastructure services.

---



#### **Hashtags & Tags**
- `#adkhackathon` (required)
- `#googlecloud` `#vertexai` `#agentdevelopmentkit` `#privacy` `#ai` `#multilagent`

### **☁️ Google Cloud Integration (Already Implemented)**

#### **Core Services Used**
- ✅ **Vertex AI (Gemini 2.0 Flash)**: Primary AI engine for all agents
- ✅ **Cloud Run**: Web UI and agent orchestrator deployment
- ✅ **Cloud Storage**: Report storage and versioning
- ✅ **BigQuery**: Privacy analytics and trend analysis
- ✅ **Secret Manager**: API key and credential management
- ✅ **Cloud Logging**: Structured logging and monitoring

#### **Advanced Features**
- ✅ **Cloud Functions**: Event triggers and webhook integration
- ✅ **Cloud Load Balancing**: Global distribution and health checks
- ✅ **Cloud Monitoring**: Performance tracking and alerting
- ✅ **Firestore**: Real-time data and structured storage

### **🤝 ADK Contribution Strategy**

#### **Proposed Contribution**
- **Template**: DevSecOps agent orchestration template
- **Documentation**: Multi-agent event-driven architecture guide
- **Examples**: Privacy compliance agent patterns
- **Best Practices**: Event flow design and agent communication

#### **Contribution Types**
1. **Documentation**: Add multi-agent orchestration examples
2. **Templates**: Create DevSecOps agent templates
3. **Tutorials**: Step-by-step multi-agent development guide
4. **Issues**: Report bugs and suggest improvements

### **📊 Impact Assessment**

#### **Technical Implementation (50%)**
- ✅ **ADK Excellence**: Native implementation with event-driven architecture
- ✅ **Multi-Agent Collaboration**: 5 specialized agents working together
- ✅ **Code Quality**: Clean, efficient, well-documented code
- ✅ **Google Cloud Integration**: Comprehensive use of cloud services

#### **Innovation & Creativity (30%)**
- ✅ **Novel Architecture**: First event-driven privacy compliance system
- ✅ **AI Integration**: Context-aware privacy analysis with Gemini
- ✅ **Business Impact**: Solves real $2.7B privacy compliance problem
- ✅ **Scalable Design**: Easy to extend with new agents and regulations

#### **Demo & Documentation (20%)**
- ✅ **Clear Problem Definition**: Privacy compliance automation
- ✅ **Effective Solution**: Multi-agent AI system with Google Cloud
- ✅ **Architecture Diagram**: Comprehensive technical documentation
- ✅ **Professional Presentation**: 3-minute optimized demo video

---

## 📄 License & Attribution

- **[LICENSE](LICENSE)** - MIT License with Commons Clause (commercial use restrictions)
- For commercial licensing: nabanita@privacylicense.com | https://privacylicense.ai/

---

## 🙋‍♂️ Need Help?
- See `hackinstructions.md` for the full hackathon adaptation plan.
- Contact: nabanita@privacylicense.com

