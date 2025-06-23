#!/usr/bin/env python3
"""
Test script for Privacy Guardian Agents deployment
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from agents.base_agent import BaseAgent
        from agents.privacy_scan_agent import PrivacyScanAgent
        from agents.gemini_analysis_agent import GeminiAnalysisAgent
        from agents.compliance_agent import ComplianceAgent
        from agents.fix_suggestion_agent import FixSuggestionAgent
        from agents.report_agent import ReportAgent
        print("✅ All agent imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    try:
        from google.cloud import storage, bigquery, secretmanager, logging, monitoring_v3
        print("✅ All Google Cloud imports successful")
    except ImportError as e:
        print(f"❌ Google Cloud import error: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔧 Testing environment...")
    
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_CLOUD_REGION',
        'GCS_BUCKET_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("Please set these variables or run: ./deploy.sh local")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_google_cloud_services():
    """Test Google Cloud service connectivity"""
    print("\n☁️ Testing Google Cloud services...")
    
    try:
        from google.cloud import storage
        client = storage.Client()
        print("✅ Cloud Storage client initialized")
    except Exception as e:
        print(f"❌ Cloud Storage error: {e}")
        return False
    
    try:
        from google.cloud import bigquery
        client = bigquery.Client()
        print("✅ BigQuery client initialized")
    except Exception as e:
        print(f"❌ BigQuery error: {e}")
        return False
    
    try:
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()
        print("✅ Secret Manager client initialized")
    except Exception as e:
        print(f"❌ Secret Manager error: {e}")
        return False
    
    return True

async def test_agent_creation():
    """Test that agents can be created"""
    print("\n🤖 Testing agent creation...")
    
    try:
        from agents.privacy_scan_agent import PrivacyScanAgent
        from agents.gemini_analysis_agent import GeminiAnalysisAgent
        from agents.compliance_agent import ComplianceAgent
        from agents.fix_suggestion_agent import FixSuggestionAgent
        from agents.report_agent import ReportAgent
        
        agents = [
            PrivacyScanAgent(),
            GeminiAnalysisAgent(),
            ComplianceAgent(),
            FixSuggestionAgent(),
            ReportAgent()
        ]
        
        for agent in agents:
            status = agent.get_agent_status()
            print(f"✅ {agent.agent_name}: {status['status']}")
        
        return True
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_rule_engine():
    """Test TypeScript RuleEngine availability"""
    print("\n🔍 Testing RuleEngine...")
    
    try:
        # Try to import the rule engine
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from ruleEngine.RuleEngine import RuleEngine
        engine = RuleEngine()
        print("✅ TypeScript RuleEngine imported successfully")
        return True
    except ImportError:
        print("⚠️ TypeScript RuleEngine not available - will use Node.js fallback")
        return True
    except Exception as e:
        print(f"❌ RuleEngine error: {e}")
        return False

def test_web_server():
    """Test web server startup"""
    print("\n🌐 Testing web server...")
    
    try:
        from web_server import app
        print("✅ Web server app created successfully")
        return True
    except Exception as e:
        print(f"❌ Web server error: {e}")
        return False

def create_test_project():
    """Create a test project for scanning"""
    print("\n📁 Creating test project...")
    
    test_dir = Path("test_project")
    test_dir.mkdir(exist_ok=True)
    
    # Create a test file with privacy violations
    test_file = test_dir / "test.js"
    test_file.write_text("""
// Test file with privacy violations
const userEmail = "test@example.com";  // HardcodedEmail violation
const apiKey = "sk-1234567890abcdef";  // HardcodedSecret violation

function processUserData(userData) {
    console.log("Processing user:", userData.email);  // LoggingViolation
    return userData;
}

// HTTP endpoint without HTTPS
const apiUrl = "http://api.example.com/data";  // InsecureConnection violation
""")
    
    print(f"✅ Test project created at: {test_dir}")
    return test_dir

async def test_full_scan():
    """Test a complete privacy scan"""
    print("\n🔍 Testing full privacy scan...")
    
    try:
        from agents.privacy_scan_agent import PrivacyScanAgent
        
        # Create test project
        test_dir = create_test_project()
        
        # Run scan
        agent = PrivacyScanAgent()
        results = await agent.process({
            'project_path': str(test_dir),
            'correlation_id': 'test-scan-001'
        })
        
        print(f"✅ Scan completed: {len(results)} violations found")
        
        # Clean up
        import shutil
        shutil.rmtree(test_dir)
        
        return True
    except Exception as e:
        print(f"❌ Full scan error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Privacy Guardian Agents - Deployment Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("Google Cloud Services", test_google_cloud_services),
        ("Agent Creation", lambda: asyncio.run(test_agent_creation())),
        ("RuleEngine", test_rule_engine),
        ("Web Server", test_web_server),
        ("Full Scan", lambda: asyncio.run(test_full_scan())),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment is ready.")
        print("\nNext steps:")
        print("1. Run: ./deploy.sh run-local")
        print("2. Open: http://localhost:8000")
        print("3. Upload a codebase and start scanning!")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Run: ./deploy.sh local")
        print("2. Check your environment variables")
        print("3. Verify Google Cloud setup")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 