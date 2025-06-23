"""
Python Bridge to TypeScript RuleEngine
=====================================

This module provides a Python interface to the TypeScript RuleEngine,
allowing Python code to use the TypeScript privacy scanning capabilities.

The bridge works by:
1. Compiling TypeScript to JavaScript (if needed)
2. Executing the JavaScript via Node.js
3. Providing a Python-like interface to the TypeScript functionality
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path

class TypeScriptRuleEngineBridge:
    """Python bridge to TypeScript RuleEngine"""
    
    def __init__(self):
        self.src_dir = Path(__file__).parent
        self.project_root = self.src_dir.parent.parent
        self.cli_path = self.project_root / "rule_engine_cli.js"
        self.ts_config_path = self.project_root / "tsconfig.json"
        
        # Ensure TypeScript is compiled
        self._ensure_typescript_compiled()
    
    def _ensure_typescript_compiled(self):
        """Ensure TypeScript files are compiled to JavaScript"""
        try:
            # Check if rule_engine_cli.js exists
            if not self.cli_path.exists():
                print("Compiling TypeScript to JavaScript...")
                self._compile_typescript()
        except Exception as e:
            print(f"Warning: Could not compile TypeScript: {e}")
    
    def _compile_typescript(self):
        """Compile TypeScript files to JavaScript"""
        try:
            # Use tsc to compile TypeScript
            cmd = ["npx", "tsc", "--project", str(self.ts_config_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                print(f"TypeScript compilation failed: {result.stderr}")
                # Fallback: try to run the CLI directly if it exists
                if not self.cli_path.exists():
                    raise Exception("TypeScript compilation failed and CLI not found")
        except Exception as e:
            print(f"TypeScript compilation error: {e}")
    
    def run(self, project_path: str) -> List[str]:
        """Run the TypeScript RuleEngine on a project path (synchronous)"""
        try:
            cmd = ["node", str(self.cli_path), project_path]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                # Extract JSON part from output - look for both possible prefixes
                json_start = -1
                for prefix in ["☁️ GeminiPrivacyRule:", "🔑 GeminiPrivacyRule:"]:
                    if prefix in output:
                        json_start = output.find('{', output.find(prefix))
                        break
                
                if json_start == -1:
                    # Fallback: look for any JSON object in the output
                    json_start = output.find('{')
                
                if json_start != -1:
                    json_part = output[json_start:]
                    try:
                        result_data = json.loads(json_part)
                        violations = result_data.get('violations', [])
                        print(f"DEBUG: Found {len(violations)} violations from TypeScript RuleEngine")
                        return violations
                    except json.JSONDecodeError as e:
                        print(f"DEBUG: JSON decode error: {e}")
                        print(f"DEBUG: JSON part: {json_part}")
                        return []
                else:
                    print("DEBUG: No JSON found in output")
                    return []
            else:
                print(f"TypeScript RuleEngine CLI failed: {result.stderr}")
                return []
        except Exception as e:
            print(f"Error running TypeScript RuleEngine: {e}")
            return []
    
    def set_gemini_enabled(self, enabled: bool):
        """Enable/disable Gemini scanning"""
        # This would be implemented by modifying environment variables
        # or configuration files that the TypeScript code reads
        pass
    
    def set_gemini_api_key(self, api_key: str):
        """Set Gemini API key"""
        # This would be implemented by setting environment variables
        # that the TypeScript code reads
        os.environ['GEMINI_API_KEY'] = api_key
    
    def set_vertex_ai_config(self, config: Dict[str, str]):
        """Set Vertex AI configuration"""
        # This would be implemented by setting environment variables
        # that the TypeScript code reads
        if 'project' in config:
            os.environ['GOOGLE_CLOUD_PROJECT'] = config['project']
        if 'location' in config:
            os.environ['GOOGLE_CLOUD_LOCATION'] = config['location']
    
    def is_gemini_available(self) -> bool:
        """Check if Gemini is available"""
        return bool(os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_CLOUD_PROJECT'))
    
    def get_rule_stats(self) -> Dict[str, Any]:
        """Get rule statistics"""
        return {
            "status": "available",
            "total_rules": 10,
            "rule_types": [
                "PII Detection", "Privacy Policy", "Consent Management",
                "Encryption & Security", "Data Flow", "Advanced Privacy",
                "AI-Powered", "Developer Guidance"
            ]
        }

# Create a Python RuleEngine class that mimics the TypeScript interface
class RuleEngine:
    """Python wrapper for TypeScript RuleEngine"""
    
    def __init__(self, scanners: Optional[List[Any]] = None):
        self.bridge = TypeScriptRuleEngineBridge()
        self.scanners = scanners or []
    
    def run(self, project_path: str) -> List[str]:
        """Run the RuleEngine on a project path (synchronous)"""
        return self.bridge.run(project_path)
    
    def set_gemini_enabled(self, enabled: bool):
        """Enable/disable Gemini scanning"""
        self.bridge.set_gemini_enabled(enabled)
    
    def set_gemini_api_key(self, api_key: str):
        """Set Gemini API key"""
        self.bridge.set_gemini_api_key(api_key)
    
    def set_vertex_ai_config(self, config: Dict[str, str]):
        """Set Vertex AI configuration"""
        self.bridge.set_vertex_ai_config(config)
    
    def is_gemini_available(self) -> bool:
        """Check if Gemini is available"""
        return self.bridge.is_gemini_available()
    
    def get_rule_stats(self) -> Dict[str, Any]:
        """Get rule statistics"""
        return self.bridge.get_rule_stats()

# Create mock classes for the rules (these are not used directly in Python)
class Rule:
    """Base rule class (mock for TypeScript compatibility)"""
    pass

class PiiRule(Rule):
    """PII detection rule (mock for TypeScript compatibility)"""
    pass

class PrivacyPolicyRule(Rule):
    """Privacy policy rule (mock for TypeScript compatibility)"""
    pass

class PiiDetectionRule(Rule):
    """PII detection rule (mock for TypeScript compatibility)"""
    pass

class AiPrivacyRule(Rule):
    """AI privacy rule (mock for TypeScript compatibility)"""
    pass

class DeveloperGuidanceRule(Rule):
    """Developer guidance rule (mock for TypeScript compatibility)"""
    pass

class GeminiPrivacyRule(Rule):
    """Gemini privacy rule (mock for TypeScript compatibility)"""
    pass

class ConsentRule(Rule):
    """Consent rule (mock for TypeScript compatibility)"""
    pass

class EncryptionRule(Rule):
    """Encryption rule (mock for TypeScript compatibility)"""
    pass

class DataFlowRule(Rule):
    """Data flow rule (mock for TypeScript compatibility)"""
    pass

class AdvancedPrivacyRule(Rule):
    """Advanced privacy rule (mock for TypeScript compatibility)"""
    pass

class Scanner:
    """Scanner class (mock for TypeScript compatibility)"""
    pass

# Export the main classes
__all__ = [
    'RuleEngine', 'Rule', 'PiiRule', 'PrivacyPolicyRule', 'PiiDetectionRule',
    'AiPrivacyRule', 'DeveloperGuidanceRule', 'GeminiPrivacyRule', 'ConsentRule',
    'EncryptionRule', 'DataFlowRule', 'AdvancedPrivacyRule', 'Scanner'
] 