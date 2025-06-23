# 🚀 Privacy Guardian Agents - Quick Start Guide

## Overview

Privacy Guardian Agents is a multi-agent privacy enforcement system built with Google Cloud Agent Development Kit (ADK). This guide will help you deploy and run the system locally or in the cloud with comprehensive Google Cloud integration.

## Prerequisites

- Python 3.8+
- Node.js 18+
- Google Cloud CLI (for cloud deployment)
- Google Cloud Project with billing enabled
- Vertex AI access (for Gemini 2.0 Flash)

## 🏠 Local Development (Recommended for Testing)

### 1. Setup Local Environment

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

# Set your Google Cloud project ID
export GOOGLE_CLOUD_PROJECT="your-project-id"

# Setup local development environment
./deploy.sh local
```

### 2. Configure Environment Variables

Edit the `.env` file created in the previous step:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Vertex AI Configuration (Gemini 2.0 Flash)
GEMINI_MODEL=gemini-2.0-flash
GEMINI_MAX_TOKENS=2000
GEMINI_TEMPERATURE=0.1

# Cloud Storage Configuration
GCS_BUCKET_NAME=privacy-guardian-reports

# BigQuery Configuration
BIGQUERY_DATASET=privacy_guardian

# Application Configuration
LOG_LEVEL=INFO
WEB_SERVER_PORT=8080
```

### 3. Google Cloud Authentication

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable securitycenter.googleapis.com
gcloud services enable asset.googleapis.com
gcloud services enable dns.googleapis.com
gcloud services enable pubsub.googleapis.com
```

### 4. Run Locally

```bash
# Test the system
python agent_orchestrator.py --project-path tests/java/

# Start the web server
python web_server.py
```

The application will be available at `http://localhost:8080`

## ☁️ Google Cloud Deployment

### Option 1: Cloud Run (Recommended for Production)

```bash
# Deploy to Cloud Run
./deploy.sh cloud-run
```

This will:
- Enable required Google Cloud APIs
- Create BigQuery dataset and tables
- Create Cloud Storage bucket
- Setup Secret Manager
- Deploy the application to Cloud Run
- Provide you with a public URL

### Option 2: Cloud Functions (Serverless)

```bash
# Deploy as Cloud Functions
./deploy.sh cloud-functions
```

This deploys each agent as a separate Cloud Function for maximum scalability.

### Option 3: Setup Cloud Resources Only

```bash
# Setup Google Cloud resources without deployment
./deploy.sh setup
```

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

### 1. Install Dependencies

```bash
# Node.js dependencies
npm install

# Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Setup Google Cloud

```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable securitycenter.googleapis.com
gcloud services enable asset.googleapis.com
gcloud services enable dns.googleapis.com
gcloud services enable pubsub.googleapis.com
```

### 3. Create BigQuery Dataset and Tables

```bash
# Create dataset
bq mk --dataset --location=us-central1 YOUR_PROJECT_ID:privacy_guardian

# Create tables
bq mk --table YOUR_PROJECT_ID:privacy_guardian.scan_results scan_results_schema.json
bq mk --table YOUR_PROJECT_ID:privacy_guardian.violations violations_schema.json
bq mk --table YOUR_PROJECT_ID:privacy_guardian.enhanced_results enhanced_results_schema.json
bq mk --table YOUR_PROJECT_ID:privacy_guardian.compliance_analysis compliance_analysis_schema.json
bq mk --table YOUR_PROJECT_ID:privacy_guardian.fix_suggestions fix_suggestions_schema.json
bq mk --table YOUR_PROJECT_ID:privacy_guardian.reports reports_schema.json
```

### 4. Create Cloud Storage Bucket

```bash
# Create bucket
gsutil mb -l us-central1 gs://privacy-guardian-reports

# Set permissions
gsutil iam ch allUsers:objectViewer gs://privacy-guardian-reports

# Create folder structure
gsutil mkdir gs://privacy-guardian-reports/reports
gsutil mkdir gs://privacy-guardian-reports/logs
gsutil mkdir gs://privacy-guardian-reports/artifacts
```

### 5. Setup Secret Manager

```bash
# Create secrets
echo -n "your-gemini-api-key" | gcloud secrets create privacy-guardian-gemini-key --data-file=-
echo -n "your-service-account-key" | gcloud secrets create privacy-guardian-service-key --data-file=-

# Grant access to service account
gcloud secrets add-iam-policy-binding privacy-guardian-gemini-key \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 6. Setup Cloud Pub/Sub (Optional)

```bash
# Create topics for agent communication
gcloud pubsub topics create privacy-scan-events
gcloud pubsub topics create ai-enhanced-findings
gcloud pubsub topics create compliance-analysis
gcloud pubsub topics create fix-suggestions
gcloud pubsub topics create report-generated

# Create subscriptions
gcloud pubsub subscriptions create gemini-analysis-sub --topic=privacy-scan-events
gcloud pubsub subscriptions create compliance-agent-sub --topic=ai-enhanced-findings
gcloud pubsub subscriptions create fix-suggestion-sub --topic=compliance-analysis
gcloud pubsub subscriptions create report-agent-sub --topic=fix-suggestions
```

### 7. Set Environment Variables

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GCS_BUCKET_NAME="privacy-guardian-reports"
export GEMINI_MODEL="gemini-2.0-flash"
export GEMINI_MAX_TOKENS="2000"
export GEMINI_TEMPERATURE="0.1"
```

### 8. Run the Application

```bash
# Test the orchestrator
python agent_orchestrator.py --project-path tests/java/

# Test individual agent
python agents/privacy_scan_agent.py tests/java/ --verbose

# Run web server
python web_server.py

# Or run orchestrator directly
python agent_orchestrator.py --project-path ./your-codebase
```

## 🎯 Usage Examples

### Web Interface

1. Open `http://localhost:8080` (local) or your Cloud Run URL
2. Upload a codebase or provide a project path
3. Click "Start Scan" to begin privacy analysis
4. View real-time results and download reports

### Command Line

```bash
# Scan a specific project
python agent_orchestrator.py --project-path ./my-app

# Scan with specific options
python agent_orchestrator.py \
  --project-path ./my-app \
  --disable-ai \
  --agent-status

# Test individual agent
python agents/privacy_scan_agent.py ./my-app --verbose

# Check agent status
python agent_orchestrator.py --agent-status
```

### API Usage

```bash
# Start a scan
curl -X POST "http://localhost:8080/api/scan" \
  -H "Content-Type: application/json" \
  -d '{"project_path": "./my-app"}'

# Get scan status
curl "http://localhost:8080/api/status/SCAN_ID"

# Download report
curl "http://localhost:8080/api/report/SCAN_ID" --output report.pdf

# Check agent status
curl "http://localhost:8080/api/agents/status"
```

## 📊 Monitoring and Analytics

### BigQuery Analytics

After running scans, you can query analytics in BigQuery:

```sql
-- View scan results
SELECT * FROM `your-project.privacy_guardian.scan_results` 
WHERE DATE(timestamp) = CURRENT_DATE();

-- Compliance trends
SELECT 
  DATE(timestamp) as scan_date,
  AVG(compliance_score) as avg_compliance
FROM `your-project.privacy_guardian.compliance_analysis`
GROUP BY scan_date
ORDER BY scan_date;

-- Violation types analysis
SELECT 
  violation_type,
  COUNT(*) as count,
  AVG(CASE WHEN severity = 'HIGH' THEN 1 ELSE 0 END) as high_severity_rate
FROM `your-project.privacy_guardian.violations`
GROUP BY violation_type
ORDER BY count DESC;

-- Agent performance
SELECT 
  agent_id,
  COUNT(*) as scans_processed,
  AVG(processing_time) as avg_processing_time
FROM `your-project.privacy_guardian.scan_results`
GROUP BY agent_id;
```

### Cloud Monitoring

View custom metrics in Google Cloud Console:
- `custom.googleapis.com/agent/scan_violations`
- `custom.googleapis.com/agent/ai_enhanced_violations`
- `custom.googleapis.com/agent/compliance_score`
- `custom.googleapis.com/agent/fix_suggestions_generated`
- `custom.googleapis.com/agent/reports_generated`

### Cloud Logging

View structured logs:
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

### Vertex AI Monitoring

```bash
# Check Gemini model availability
gcloud ai models list --region=us-central1 --filter="name:gemini"

# Check Vertex AI operations
gcloud ai operations list --region=us-central1 --filter="operationType:PREDICT"

# View Vertex AI metrics
gcloud monitoring metrics list --filter="metric.type:aiplatform.googleapis.com"
```

## 🔐 Security and Secrets

### Secret Manager

Store sensitive configuration in Secret Manager:

```bash
# Create secrets
gcloud secrets create privacy-guardian-gemini-key --replication-policy=automatic
echo -n "your-api-key" | gcloud secrets versions add privacy-guardian-gemini-key --data-file=-

# Access in code
secret = self.fetch_secret(f"projects/{project_id}/secrets/privacy-guardian-gemini-key")
```

### IAM Permissions

Ensure your service account has these roles:
- `roles/aiplatform.user` (for Vertex AI)
- `roles/storage.objectViewer` (for Cloud Storage)
- `roles/bigquery.dataEditor` (for BigQuery)
- `roles/secretmanager.secretAccessor` (for Secret Manager)
- `roles/logging.logWriter` (for Cloud Logging)
- `roles/monitoring.metricWriter` (for Cloud Monitoring)
- `roles/pubsub.publisher` (for Cloud Pub/Sub)
- `roles/pubsub.subscriber` (for Cloud Pub/Sub)

### Service Account Setup

```bash
# Create service account
gcloud iam service-accounts create privacy-guardian-sa \
  --display-name="Privacy Guardian Service Account"

# Grant roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:privacy-guardian-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:privacy-guardian-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

# Create and download key
gcloud iam service-accounts keys create privacy-guardian-key.json \
  --iam-account=privacy-guardian-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## 🚨 Troubleshooting

### Common Issues

1. **Vertex AI not available**
   - Check your service account has `roles/aiplatform.user`
   - Verify billing is enabled on your Google Cloud project
   - Check API quotas in Google Cloud Console
   - Verify `GOOGLE_CLOUD_PROJECT` is set correctly

2. **BigQuery permissions error**
   - Ensure your service account has BigQuery Data Editor role
   - Check that the dataset exists: `bq ls your-project:privacy_guardian`
   - Verify tables are created with correct schemas

3. **Cloud Storage access denied**
   - Verify bucket exists: `gsutil ls gs://privacy-guardian-reports`
   - Check IAM permissions on the bucket
   - Ensure service account has Storage Object Viewer role

4. **Agent communication issues**
   - Check that all agents are running
   - Verify event flow in logs
   - Ensure correlation IDs are being passed correctly
   - Check Cloud Pub/Sub topics and subscriptions

5. **TypeScript RuleEngine import error**
   - Ensure Node.js dependencies are installed: `npm install`
   - Check if `rule_engine_cli.js` exists: `ls -la rule_engine_cli.js`
   - Verify Node.js version is 18+

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python web_server.py
```

### Health Check

Check agent status:

```bash
# Check all agents
python agent_orchestrator.py --agent-status

# Check specific agent
curl "http://localhost:8080/api/agents/status"

# Check event history
python agent_orchestrator.py --event-history CORRELATION_ID
```

### Performance Monitoring

```bash
# Monitor resource usage
gcloud run services describe privacy-guardian-agents --region us-central1 --format="value(spec.template.spec.containers[0].resources)"

# Check Cloud Run logs for memory issues
gcloud logging read "resource.type=cloud_run_revision AND textPayload:memory" --limit 20

# View custom metrics
gcloud monitoring metrics list --filter="metric.type:custom.googleapis.com/agent"
```

## 📈 Scaling and Performance

### Local Development
- Single instance, suitable for testing
- Limited by local resources
- TypeScript RuleEngine runs via Node.js bridge

### Cloud Run
- Auto-scales based on demand
- Configure memory and CPU limits
- Set max instances for cost control
- Supports concurrent scans

### Cloud Functions
- Event-driven, scales to zero
- Each agent is independent
- Pay per invocation
- Maximum scalability

### Performance Optimization
- Use `gemini-2.0-flash` for faster AI responses
- Configure appropriate token limits
- Monitor BigQuery query performance
- Use Cloud Storage for report caching

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Deploy Privacy Guardian
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      - run: |
          gcloud auth configure-docker
          docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/privacy-guardian-agents .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/privacy-guardian-agents
          gcloud run deploy privacy-guardian-agents \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/privacy-guardian-agents \
            --platform managed \
            --region us-central1 \
            --set-env-vars GOOGLE_CLOUD_PROJECT=${{ secrets.GCP_PROJECT_ID }},GEMINI_MODEL=gemini-2.0-flash
```

### GitLab CI

```yaml
deploy:
  stage: deploy
  script:
    - gcloud auth activate-service-account --key-file=$GOOGLE_CLOUD_KEY
    - gcloud config set project $GCP_PROJECT_ID
    - docker build -t gcr.io/$GCP_PROJECT_ID/privacy-guardian-agents .
    - docker push gcr.io/$GCP_PROJECT_ID/privacy-guardian-agents
    - gcloud run deploy privacy-guardian-agents \
        --image gcr.io/$GCP_PROJECT_ID/privacy-guardian-agents \
        --platform managed \
        --region us-central1 \
        --set-env-vars GOOGLE_CLOUD_PROJECT=$GCP_PROJECT_ID,GEMINI_MODEL=gemini-2.0-flash
```

### Cloud Build

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

## 📞 Support

- **Documentation**: See `README.md`, `ARCHITECTURE_DIAGRAM.md`, and `DEPLOYMENT.md`
- **Issues**: Create an issue in the repository
- **Blog Post**: See `BLOG_POST.md` for technical details
- **Vertex AI Documentation**: For Gemini-specific issues

## 🎉 Next Steps

1. **Customize Rules**: Add your own privacy rules in `src/ruleEngine/rules/`
2. **Extend Agents**: Create new agents by inheriting from `BaseAgent`
3. **Integrate CI/CD**: Add privacy scanning to your development pipeline
4. **Monitor Analytics**: Set up BigQuery dashboards for privacy trends
5. **Scale Up**: Deploy to production with Cloud Run or Cloud Functions
6. **Security Hardening**: Implement additional security measures
7. **Contribute**: Submit PRs to improve the system

---

**Happy Privacy Scanning! 🔒✨** 