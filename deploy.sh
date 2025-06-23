# Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
# Licensed under the MIT License modified with the Commons Clause.
# For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
# Commercial use is prohibited without a license.
# Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

#!/bin/bash

# Privacy Guardian Agents - Deployment Script
# Supports local development and Google Cloud deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
SERVICE_NAME="privacy-guardian-agents"
BUCKET_NAME="privacy-guardian-reports"
DATASET_NAME="privacy"

echo -e "${BLUE}🚀 Privacy Guardian Agents Deployment${NC}"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Google Cloud setup
check_gcloud_setup() {
    if ! command_exists gcloud; then
        echo -e "${RED}❌ Google Cloud CLI not found. Please install it first:${NC}"
        echo "https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        echo -e "${RED}❌ Not authenticated with Google Cloud. Please run:${NC}"
        echo "gcloud auth login"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Google Cloud CLI configured${NC}"
}

# Function to setup Google Cloud project
setup_gcloud_project() {
    echo -e "${BLUE}🔧 Setting up Google Cloud project...${NC}"
    
    # Set project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    echo "Enabling required APIs..."
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable storage.googleapis.com
    gcloud services enable bigquery.googleapis.com
    gcloud services enable secretmanager.googleapis.com
    gcloud services enable logging.googleapis.com
    gcloud services enable monitoring.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable cloudfunctions.googleapis.com
    
    echo -e "${GREEN}✅ Google Cloud APIs enabled${NC}"
}

# Function to create BigQuery dataset and tables
setup_bigquery() {
    echo -e "${BLUE}📊 Setting up BigQuery...${NC}"
    
    # Create dataset
    bq mk --dataset --location=$REGION $PROJECT_ID:$DATASET_NAME
    
    # Create tables
    bq mk --table --schema=schemas/scan_results.json $PROJECT_ID:$DATASET_NAME.scan_results
    bq mk --table --schema=schemas/enhanced_results.json $PROJECT_ID:$DATASET_NAME.enhanced_results
    bq mk --table --schema=schemas/compliance_analysis.json $PROJECT_ID:$DATASET_NAME.compliance_analysis
    bq mk --table --schema=schemas/fix_suggestions.json $PROJECT_ID:$DATASET_NAME.fix_suggestions
    bq mk --table --schema=schemas/reports.json $PROJECT_ID:$DATASET_NAME.reports
    
    echo -e "${GREEN}✅ BigQuery dataset and tables created${NC}"
}

# Function to create Cloud Storage bucket
setup_storage() {
    echo -e "${BLUE}📦 Setting up Cloud Storage...${NC}"
    
    # Create bucket
    gsutil mb -l $REGION gs://$BUCKET_NAME
    
    # Set bucket permissions
    gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME
    
    echo -e "${GREEN}✅ Cloud Storage bucket created${NC}"
}

# Function to create secrets
setup_secrets() {
    echo -e "${BLUE}🔐 Setting up Secret Manager...${NC}"
    
    # Create secrets (you'll need to set the actual values)
    echo "Creating secrets..."
    echo "You'll need to set the actual secret values manually:"
    echo "gcloud secrets create GEMINI_API_KEY --replication-policy=automatic"
    echo "echo -n 'your-api-key' | gcloud secrets versions add GEMINI_API_KEY --data-file=-"
    
    echo -e "${GREEN}✅ Secret Manager setup instructions provided${NC}"
}

# Function to deploy to Cloud Run
deploy_cloud_run() {
    echo -e "${BLUE}🚀 Deploying to Cloud Run...${NC}"
    
    # Build and deploy
    gcloud run deploy $SERVICE_NAME \
        --source . \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_REGION=$REGION,GCS_BUCKET_NAME=$BUCKET_NAME" \
        --memory 2Gi \
        --cpu 2 \
        --timeout 3600
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    echo -e "${GREEN}✅ Deployed to Cloud Run: $SERVICE_URL${NC}"
}

# Function to deploy as Cloud Functions
deploy_cloud_functions() {
    echo -e "${BLUE}⚡ Deploying as Cloud Functions...${NC}"
    
    # Deploy each agent as a separate function
    for agent in privacy_scan gemini_analysis compliance fix_suggestion report; do
        echo "Deploying $agent agent..."
        gcloud functions deploy privacy-guardian-$agent \
            --runtime python311 \
            --trigger-http \
            --allow-unauthenticated \
            --region $REGION \
            --entry-point cloud_function_entrypoint \
            --source . \
            --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_REGION=$REGION,GCS_BUCKET_NAME=$BUCKET_NAME"
    done
    
    echo -e "${GREEN}✅ All agents deployed as Cloud Functions${NC}"
}

# Function to setup local development
setup_local() {
    echo -e "${BLUE}🏠 Setting up local development...${NC}"
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Create .env file
    cat > .env << EOF
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_REGION=$REGION
GCS_BUCKET_NAME=$BUCKET_NAME
GEMINI_API_KEY=your-gemini-api-key
EOF
    
    echo -e "${GREEN}✅ Local development environment ready${NC}"
    echo -e "${YELLOW}⚠️  Please update .env with your actual API keys${NC}"
}

# Function to run locally
run_local() {
    echo -e "${BLUE}🏃 Running locally...${NC}"
    
    source venv/bin/activate
    
    # Run the web server
    python web_server.py
}

# Function to create BigQuery schemas
create_schemas() {
    echo -e "${BLUE}📋 Creating BigQuery schemas...${NC}"
    
    mkdir -p schemas
    
    # Scan results schema
    cat > schemas/scan_results.json << EOF
[
    {"name": "file_path", "type": "STRING"},
    {"name": "line_number", "type": "INTEGER"},
    {"name": "violation_type", "type": "STRING"},
    {"name": "description", "type": "STRING"},
    {"name": "severity", "type": "STRING"},
    {"name": "fix_suggestion", "type": "STRING"},
    {"name": "regulation_reference", "type": "STRING"},
    {"name": "agent_id", "type": "STRING"},
    {"name": "timestamp", "type": "TIMESTAMP"}
]
EOF
    
    # Enhanced results schema
    cat > schemas/enhanced_results.json << EOF
[
    {"name": "file_path", "type": "STRING"},
    {"name": "line_number", "type": "INTEGER"},
    {"name": "violation_type", "type": "STRING"},
    {"name": "description", "type": "STRING"},
    {"name": "severity", "type": "STRING"},
    {"name": "fix_suggestion", "type": "STRING"},
    {"name": "regulation_reference", "type": "STRING"},
    {"name": "agent_id", "type": "STRING"},
    {"name": "timestamp", "type": "TIMESTAMP"},
    {"name": "ai_enhanced", "type": "BOOLEAN"},
    {"name": "enhanced_description", "type": "STRING"}
]
EOF
    
    # Compliance analysis schema
    cat > schemas/compliance_analysis.json << EOF
[
    {"name": "compliance_score", "type": "FLOAT"},
    {"name": "total_violations", "type": "INTEGER"},
    {"name": "regulations_affected", "type": "STRING"},
    {"name": "risk_assessment", "type": "STRING"},
    {"name": "timestamp", "type": "TIMESTAMP"}
]
EOF
    
    # Fix suggestions schema
    cat > schemas/fix_suggestions.json << EOF
[
    {"name": "fixes_generated", "type": "INTEGER"},
    {"name": "priority_breakdown", "type": "STRING"},
    {"name": "estimated_effort", "type": "STRING"},
    {"name": "timestamp", "type": "TIMESTAMP"}
]
EOF
    
    # Reports schema
    cat > schemas/reports.json << EOF
[
    {"name": "report_id", "type": "STRING"},
    {"name": "total_violations", "type": "INTEGER"},
    {"name": "compliance_score", "type": "FLOAT"},
    {"name": "risk_level", "type": "STRING"},
    {"name": "storage_location", "type": "STRING"},
    {"name": "timestamp", "type": "TIMESTAMP"}
]
EOF
    
    echo -e "${GREEN}✅ BigQuery schemas created${NC}"
}

# Main deployment logic
case "${1:-help}" in
    "local")
        setup_local
        ;;
    "run-local")
        run_local
        ;;
    "cloud-run")
        check_gcloud_setup
        setup_gcloud_project
        create_schemas
        setup_bigquery
        setup_storage
        setup_secrets
        deploy_cloud_run
        ;;
    "cloud-functions")
        check_gcloud_setup
        setup_gcloud_project
        create_schemas
        setup_bigquery
        setup_storage
        setup_secrets
        deploy_cloud_functions
        ;;
    "setup")
        check_gcloud_setup
        setup_gcloud_project
        create_schemas
        setup_bigquery
        setup_storage
        setup_secrets
        ;;
    "help"|*)
        echo -e "${BLUE}Usage:${NC}"
        echo "  ./deploy.sh local          - Setup local development environment"
        echo "  ./deploy.sh run-local      - Run the application locally"
        echo "  ./deploy.sh cloud-run      - Deploy to Google Cloud Run"
        echo "  ./deploy.sh cloud-functions- Deploy as Google Cloud Functions"
        echo "  ./deploy.sh setup          - Setup Google Cloud resources only"
        echo ""
        echo -e "${YELLOW}Environment Variables:${NC}"
        echo "  GOOGLE_CLOUD_PROJECT       - Your Google Cloud project ID"
        echo "  GOOGLE_CLOUD_REGION        - Google Cloud region (default: us-central1)"
        echo ""
        echo -e "${GREEN}Quick Start:${NC}"
        echo "  1. Set GOOGLE_CLOUD_PROJECT environment variable"
        echo "  2. Run: ./deploy.sh local"
        echo "  3. Update .env with your API keys"
        echo "  4. Run: ./deploy.sh run-local"
        ;;
esac 