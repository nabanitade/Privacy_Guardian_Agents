# Copyright (c) 2025 Privacy License . All rights reserved.
# Licensed under the MIT License modified with the Commons Clause.
# For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
# Commercial use is prohibited without a license.
# Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

#!/bin/bash

# GitLab Privacy Integration Script
# Provides real-time privacy feedback in merge requests and issues

set -e

# Configuration
GITLAB_URL="${CI_SERVER_URL}"
GITLAB_TOKEN="${GITLAB_TOKEN}"
PROJECT_ID="${CI_PROJECT_ID}"
MR_IID="${CI_MERGE_REQUEST_IID}"
COMMIT_SHA="${CI_COMMIT_SHA}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔒 GitLab Privacy Integration Starting...${NC}"

# Function to create GitLab API request
gitlab_api() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    curl -s -X "$method" \
        -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$data" \
        "$GITLAB_URL/api/v4/projects/$PROJECT_ID$endpoint"
}

# Function to add comment to merge request
add_mr_comment() {
    local comment="$1"
    
    if [ -n "$MR_IID" ]; then
        echo -e "${BLUE}💬 Adding privacy feedback to merge request...${NC}"
        gitlab_api "POST" "/merge_requests/$MR_IID/notes" "{\"body\":\"$comment\"}"
        echo -e "${GREEN}✅ Comment added to merge request${NC}"
    else
        echo -e "${YELLOW}⚠️ No merge request ID found, skipping comment${NC}"
    fi
}

# Function to create privacy violation issue
create_privacy_issue() {
    local title="$1"
    local description="$2"
    local severity="$3"
    
    echo -e "${BLUE}📋 Creating privacy violation issue...${NC}"
    
    local issue_data="{
        \"title\": \"$title\",
        \"description\": \"$description\",
        \"labels\": \"privacy-violation,$severity\",
        \"assignee_id\": \"$GITLAB_USER_ID\"
    }"
    
    gitlab_api "POST" "/issues" "$issue_data"
    echo -e "${GREEN}✅ Privacy issue created${NC}"
}

# Function to update pipeline status
update_pipeline_status() {
    local status="$1"
    local message="$2"
    
    echo -e "${BLUE}🔄 Updating pipeline status...${NC}"
    
    # This would typically update GitLab pipeline status
    # Implementation depends on your GitLab setup
    echo "Pipeline Status: $status - $message"
}

# Main privacy scan execution
main() {
    echo -e "${BLUE}🔍 Running privacy vulnerability scan...${NC}"
    
    # Run the privacy checker
    local scan_output
    scan_output=$(npm start . 2>&1 || true)
    
    # Count violations - improved parsing
    local total_violations=$(echo "$scan_output" | grep -c "violation" || echo "0")
    local high_severity=$(echo "$scan_output" | grep -c "HIGH" || echo "0")
    local medium_severity=$(echo "$scan_output" | grep -c "MEDIUM" || echo "0")
    local low_severity=$(echo "$scan_output" | grep -c "LOW" || echo "0")
    
    # Clean up any whitespace or newlines in the counts
    total_violations=$(echo "$total_violations" | tr -d '\n\r' | xargs)
    high_severity=$(echo "$high_severity" | tr -d '\n\r' | xargs)
    medium_severity=$(echo "$medium_severity" | tr -d '\n\r' | xargs)
    low_severity=$(echo "$low_severity" | tr -d '\n\r' | xargs)
    
    echo -e "${BLUE}📊 Privacy Scan Results:${NC}"
    echo "Total Violations: $total_violations"
    echo "High Severity: $high_severity"
    echo "Medium Severity: $medium_severity"
    echo "Low Severity: $low_severity"
    
    # Create merge request comment
    local comment="## 🔒 Privacy Compliance Check Results

### 📊 Scan Summary
- **Total Violations**: $total_violations
- **High Severity**: $high_severity
- **Medium Severity**: $medium_severity
- **Low Severity**: $low_severity

### 📋 Detailed Findings
\`\`\`
$(echo "$scan_output" | head -30)
\`\`\`

### 🚀 Recommendations
- Review all privacy violations before merging
- Address high-severity issues immediately
- Consider implementing suggested fixes
- Ensure GDPR/CCPA compliance

### 🔗 Resources
- [Privacy Guidelines](link-to-privacy-guidelines)
- [Compliance Checklist](link-to-checklist)
- [Support Team](mailto:privacy@company.com)"

    add_mr_comment "$comment"
    
    # Create issues for high-severity violations
    if [ "$high_severity" -gt 0 ]; then
        echo -e "${RED}🚨 High severity violations detected! Creating issues...${NC}"
        
        # Extract high-severity violations and create issues
        echo "$scan_output" | grep "HIGH" | while read -r line; do
            local title="Privacy Violation: High Severity Issue"
            local description="**Violation**: $line

**File**: $(echo "$line" | grep -o '[^:]*:[0-9]*' | head -1)
**Severity**: HIGH
**Commit**: $COMMIT_SHA
**Pipeline**: $CI_PIPELINE_ID

Please address this privacy violation immediately."
            
            create_privacy_issue "$title" "$description" "high"
        done
    fi
    
    # Update pipeline status
    if [ "$high_severity" -gt 0 ]; then
        update_pipeline_status "failed" "High severity privacy violations detected"
        echo -e "${RED}❌ Pipeline failed due to high severity privacy violations${NC}"
        exit 1
    elif [ "$total_violations" -gt 0 ]; then
        update_pipeline_status "warning" "Privacy violations detected but none are high severity"
        echo -e "${YELLOW}⚠️ Pipeline completed with warnings${NC}"
    else
        update_pipeline_status "success" "No privacy violations detected"
        echo -e "${GREEN}✅ Pipeline passed - No privacy violations found${NC}"
    fi
}

# Execute main function
main "$@" 