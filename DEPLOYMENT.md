# Privacy Guardian Agents - Deployment Guide

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Local Development](#local-development)
- [Cloud Deployment](#cloud-deployment)
- [Testing](#testing)
- [Monitoring & Troubleshooting](#monitoring--troubleshooting)
- [Security Considerations](#security-considerations)

## Overview

Privacy Guardian Agents is a multi-agent privacy enforcement system built for Google Cloud Agent Development Kit (ADK) Hackathon. This guide covers deployment options for local development and cloud environments with comprehensive Google Cloud integration.

## Prerequisites

### Required Software
- Python 3.9+
- Node.js 18+
- Docker (for containerized deployment)
- Google Cloud SDK

### Required Google Cloud Services
- Google Cloud Project with billing enabled
- Vertex AI API (for Gemini 2.0 Flash)
- Cloud Storage
- Cloud Logging
- BigQuery
- Secret Manager
- Cloud Monitoring
- Cloud Run (for serverless deployment)
- Cloud Functions (for event-driven deployment)
- Cloud Build (for CI/CD)
- Cloud Security Command Center
- Cloud Asset Inventory
- Identity and Access Management (IAM)
- Cloud DNS
- Cloud Pub/Sub

## Environment Setup

### 1. Clone and Setup Repository
```bash
git clone <repository-url>
cd agenthack
```

### 2. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
npm install
```

### 3. Google Cloud Authentication
```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable securitycenter.googleapis.com
gcloud services enable asset.googleapis.com
gcloud services enable dns.googleapis.com
gcloud services enable pubsub.googleapis.com
```

### 4. Environment Variables
Create a `.env` file in the project root:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
GOOGLE_CLOUD_LOCATION=us-central1

# Vertex AI Configuration (Gemini 2.0 Flash)
GEMINI_MODEL=gemini-2.0-flash
GEMINI_MAX_TOKENS=2000
GEMINI_TEMPERATURE=0.1

# Cloud Storage Configuration
GCS_BUCKET_NAME=privacy-guardian-reports
STORAGE_REGION=us-central1

# BigQuery Configuration
BIGQUERY_DATASET=privacy_guardian
BIGQUERY_TABLE=scan_results

# Secret Manager Configuration
SECRET_NAME=privacy-guardian-secrets

# Cloud Monitoring Configuration
MONITORING_PROJECT_ID=your-project-id

# Application Configuration
LOG_LEVEL=INFO
WEB_SERVER_PORT=8080
```

## Local Development

### 1. Start Local Development Server
```bash
# Start the web server
python web_server.py

# Or use the deployment script
./deploy.sh local
```

### 2. Run Privacy Scan
```bash
# Using the orchestrator (recommended)
source venv/bin/activate
python agent_orchestrator.py --project-path tests/java/

# Using individual agent CLI
python agents/privacy_scan_agent.py tests/java/ --verbose

# Using Python directly
python -c "
from agents.privacy_scan_agent import PrivacyScanAgent
from agents.gemini_analysis_agent import GeminiAnalysisAgent
from agents.compliance_agent import ComplianceAgent
from agents.fix_suggestion_agent import FixSuggestionAgent
from agents.report_agent import ReportAgent

# Initialize agents
privacy_agent = PrivacyScanAgent()
gemini_agent = GeminiAnalysisAgent()
compliance_agent = ComplianceAgent()
fix_agent = FixSuggestionAgent()
report_agent = ReportAgent()

# Run scan
result = privacy_agent.scan_codebase('tests/')
print(result)
"

# Using the test script
python test_deployment.py
```

### 3. Access Web Interface
Open your browser and navigate to `http://localhost:8080`

## Cloud Deployment

### Option 1: Cloud Run Deployment (Recommended)

#### 1. Build and Deploy
```bash
# Use the deployment script
./deploy.sh cloud-run

# Or manually:
# Build Docker image
docker build -t privacy-guardian-agents .

# Tag and push to Google Container Registry
docker tag privacy-guardian-agents gcr.io/YOUR_PROJECT_ID/privacy-guardian-agents
docker push gcr.io/YOUR_PROJECT_ID/privacy-guardian-agents

# Deploy to Cloud Run
gcloud run deploy privacy-guardian-agents \
  --image gcr.io/YOUR_PROJECT_ID/privacy-guardian-agents \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1,GEMINI_MODEL=gemini-2.0-flash
```

#### 2. Access Deployed Service
The deployment script will output the service URL. You can also find it in the Google Cloud Console under Cloud Run.

### Option 2: Cloud Functions Deployment

#### 1. Deploy Functions
```bash
# Use the deployment script
./deploy.sh cloud-functions

# Or manually deploy each function:
gcloud functions deploy privacy-scan \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point scan_codebase \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GEMINI_MODEL=gemini-2.0-flash

gcloud functions deploy gemini-analysis \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point analyze_violations \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GEMINI_MODEL=gemini-2.0-flash
```

#### 2. Test Functions
```bash
# Get function URLs
gcloud functions describe privacy-scan --region us-central1 --format="value(httpsTrigger.url)"
gcloud functions describe gemini-analysis --region us-central1 --format="value(httpsTrigger.url)"
```

### Option 3: Kubernetes Deployment

#### 1. Create Kubernetes Cluster
```bash
# Create GKE cluster
gcloud container clusters create privacy-guardian-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 10
```

#### 2. Deploy to Kubernetes
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

## Resource Setup

### 1. BigQuery Setup
```bash
# Create dataset and tables
bq mk --dataset YOUR_PROJECT_ID:privacy_guardian

bq mk --table YOUR_PROJECT_ID:privacy_guardian.scan_results \
  scan_results_schema.json

bq mk --table YOUR_PROJECT_ID:privacy_guardian.violations \
  violations_schema.json

bq mk --table YOUR_PROJECT_ID:privacy_guardian.enhanced_results \
  enhanced_results_schema.json

bq mk --table YOUR_PROJECT_ID:privacy_guardian.compliance_analysis \
  compliance_analysis_schema.json

bq mk --table YOUR_PROJECT_ID:privacy_guardian.fix_suggestions \
  fix_suggestions_schema.json

bq mk --table YOUR_PROJECT_ID:privacy_guardian.reports \
  reports_schema.json
```

### 2. Cloud Storage Setup
```bash
# Create storage bucket
gsutil mb -l us-central1 gs://privacy-guardian-reports

# Set bucket permissions
gsutil iam ch allUsers:objectViewer gs://privacy-guardian-reports

# Create folder structure
gsutil mkdir gs://privacy-guardian-reports/reports
gsutil mkdir gs://privacy-guardian-reports/logs
gsutil mkdir gs://privacy-guardian-reports/artifacts
```

### 3. Secret Manager Setup
```bash
# Create secrets
echo -n "your-gemini-api-key" | gcloud secrets create privacy-guardian-gemini-key --data-file=-
echo -n "your-service-account-key" | gcloud secrets create privacy-guardian-service-key --data-file=-

# Grant access to service account
gcloud secrets add-iam-policy-binding privacy-guardian-gemini-key \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding privacy-guardian-service-key \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 4. Cloud Monitoring Setup
```bash
# Create custom metrics
gcloud monitoring metrics create \
  --project=YOUR_PROJECT_ID \
  --metric-descriptor=metric_descriptor.json

# Create alerting policies
gcloud alpha monitoring policies create --policy-from-file=alerting_policy.yaml
```

### 5. Cloud Security Command Center Setup
```bash
# Enable Security Command Center
gcloud services enable securitycenter.googleapis.com

# Create security sources
gcloud scc sources create --organization=YOUR_ORG_ID \
  --display-name="Privacy Guardian Agents" \
  --description="Privacy compliance monitoring source"
```

### 6. Cloud Asset Inventory Setup
```bash
# Enable Asset Inventory API
gcloud services enable asset.googleapis.com

# Create asset feeds
gcloud asset feeds create --project=YOUR_PROJECT_ID \
  --feed-id=privacy-guardian-feed \
  --asset-types="compute.googleapis.com/Instance,storage.googleapis.com/Bucket" \
  --condition-expression="resource.data.labels.environment='production'"
```

### 7. Cloud Pub/Sub Setup
```bash
# Create topics for agent communication
gcloud pubsub topics create privacy-scan-events
gcloud pubsub topics create ai-enhanced-findings
gcloud pubsub topics create compliance-analysis
gcloud pubsub topics create fix-suggestions
gcloud pubsub topics create report-generated

# Create subscriptions
gcloud pubsub subscriptions create gemini-analysis-sub \
  --topic=privacy-scan-events

gcloud pubsub subscriptions create compliance-agent-sub \
  --topic=ai-enhanced-findings

gcloud pubsub subscriptions create fix-suggestion-sub \
  --topic=compliance-analysis

gcloud pubsub subscriptions create report-agent-sub \
  --topic=fix-suggestions
```

## Testing

### 1. Run Test Suite
```bash
# Python tests
python -m pytest tests/

# TypeScript tests
npm test

# Integration tests
python test_deployment.py

# Agent-specific tests
python agents/privacy_scan_agent.py tests/java/ --verbose
```

### 2. Manual Testing
```bash
# Test privacy scan
curl -X POST http://localhost:8080/scan \
  -H "Content-Type: application/json" \
  -d '{"path": "tests/", "languages": ["python", "javascript"]}'

# Test specific agent
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"violations": [{"type": "pii", "severity": "high"}]}'

# Test orchestrator
python agent_orchestrator.py --project-path tests/java/ --agent-status
```

### 3. Load Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Run load test
ab -n 100 -c 10 -p test_payload.json -T application/json http://localhost:8080/scan
```

## Monitoring & Troubleshooting

### 1. Cloud Logging
```bash
# View application logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=privacy-guardian-agents" --limit 50

# View specific agent logs
gcloud logging read "textPayload:PrivacyScanAgent" --limit 20

# View Gemini AI logs
gcloud logging read "textPayload:gemini" --limit 20

# View structured logs
gcloud logging read "jsonPayload.agent_id=privacy_scan_agent" --limit 20
```

### 2. Cloud Monitoring
```bash
# View custom metrics
gcloud monitoring metrics list --filter="metric.type:custom.googleapis.com/agent"

# View Vertex AI metrics
gcloud monitoring metrics list --filter="metric.type:aiplatform.googleapis.com"

# Create alerting policies
gcloud alpha monitoring policies create --policy-from-file=alerting_policy.yaml

# View agent performance
gcloud monitoring metrics list --filter="metric.type:custom.googleapis.com/agent/scan_violations"
```

### 3. BigQuery Analytics
```bash
# View scan results
bq query "SELECT * FROM \`YOUR_PROJECT_ID.privacy_guardian.scan_results\` ORDER BY timestamp DESC LIMIT 10"

# View compliance analytics
bq query "SELECT violation_type, COUNT(*) as count FROM \`YOUR_PROJECT_ID.privacy_guardian.violations\` GROUP BY violation_type"

# View performance metrics
bq query "SELECT agent_id, AVG(processing_time) as avg_time FROM \`YOUR_PROJECT_ID.privacy_guardian.scan_results\` GROUP BY agent_id"
```

### 4. Common Issues

#### Authentication Issues
```bash
# Verify service account permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --format="table(bindings.role)" \
  --filter="bindings.members:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com"

# Check Vertex AI permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --format="table(bindings.role)" \
  --filter="bindings.members:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com AND bindings.role:aiplatform"
```

#### API Quota Issues
```bash
# Check API quotas
gcloud compute regions describe us-central1 --format="value(quotas[].limit,quotas[].usage)"

# Check Vertex AI quotas
gcloud ai operations list --region=us-central1
```

#### Memory Issues
```bash
# Monitor resource usage
gcloud run services describe privacy-guardian-agents --region us-central1 --format="value(spec.template.spec.containers[0].resources)"

# Check Cloud Run logs for memory issues
gcloud logging read "resource.type=cloud_run_revision AND textPayload:memory" --limit 20
```

#### Gemini AI Issues
```bash
# Check Gemini model availability
gcloud ai models list --region=us-central1 --filter="name:gemini"

# Check Vertex AI operations
gcloud ai operations list --region=us-central1 --filter="operationType:PREDICT"

# Verify model access
gcloud ai models describe gemini-2.0-flash --region=us-central1
```

## Security Considerations

### 1. Service Account Security
- Use least privilege principle
- Rotate service account keys regularly
- Use workload identity when possible
- Grant minimal required permissions

### 2. Network Security
- Enable VPC connector for private networking
- Use Cloud Armor for DDoS protection
- Configure firewall rules appropriately
- Use private Google access

### 3. Data Security
- Encrypt data at rest and in transit
- Use customer-managed encryption keys
- Implement proper access controls
- Enable audit logging for all services

### 4. Secret Management
- Store sensitive data in Secret Manager
- Use environment variables for configuration
- Avoid hardcoding secrets in code
- Implement secret rotation

### 5. Vertex AI Security
- Use service account authentication
- Enable audit logging for AI operations
- Implement rate limiting
- Monitor AI usage and costs

## CI/CD Integration

### 1. GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Google Cloud
      uses: google-github-actions/setup-gcloud@v0
      with:
        project_id: ${{ secrets.GCP_PROJECT_ID }}
        service_account_key: ${{ secrets.GCP_SA_KEY }}
    - name: Deploy to Cloud Run
      run: |
        gcloud auth configure-docker
        docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/privacy-guardian-agents .
        docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/privacy-guardian-agents
        gcloud run deploy privacy-guardian-agents \
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/privacy-guardian-agents \
          --platform managed \
          --region us-central1 \
          --set-env-vars GOOGLE_CLOUD_PROJECT=${{ secrets.GCP_PROJECT_ID }},GEMINI_MODEL=gemini-2.0-flash
```

### 2. GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - python -m pytest tests/
    - npm test
    - python test_deployment.py

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - gcloud run deploy privacy-guardian-agents \
        --image $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
        --platform managed \
        --region us-central1 \
        --set-env-vars GOOGLE_CLOUD_PROJECT=$GCP_PROJECT_ID,GEMINI_MODEL=gemini-2.0-flash
```

### 3. Cloud Build
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/privacy-guardian-agents:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/privacy-guardian-agents:$COMMIT_SHA']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'privacy-guardian-agents'
      - '--image'
      - 'gcr.io/$PROJECT_ID/privacy-guardian-agents:$COMMIT_SHA'
      - '--platform'
      - 'managed'
      - '--region'
      - 'us-central1'
      - '--set-env-vars'
      - 'GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GEMINI_MODEL=gemini-2.0-flash'
```

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Cloud Logging for error messages
3. Consult the project documentation
4. Open an issue in the project repository
5. Check Vertex AI documentation for Gemini-specific issues

## License

This project is licensed under the MIT License - see the LICENSE file for details. 