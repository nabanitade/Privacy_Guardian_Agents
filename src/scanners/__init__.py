"""
Python Bridge to TypeScript Scanners
===================================

This module provides Python interfaces to the TypeScript scanners,
allowing Python code to use the TypeScript file scanning capabilities.
"""

from typing import List, Dict, Any

class ScannedFile:
    """Python interface for scanned file (matching TypeScript interface)"""
    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content

class Scanner:
    """Base scanner class (mock for TypeScript compatibility)"""
    language: str = "unknown"
    
    async def scan_files(self, dir_path: str) -> List[ScannedFile]:
        """Scan files in directory (mock implementation)"""
        return []

# Create mock scanner classes for each language
class JavaScriptScanner(Scanner):
    language = "JavaScript"

class TypeScriptScanner(Scanner):
    language = "TypeScript"

class JavaScanner(Scanner):
    language = "Java"

class PythonScanner(Scanner):
    language = "Python"

class GoScanner(Scanner):
    language = "Go"

class CSharpScanner(Scanner):
    language = "C#"

class PHPScanner(Scanner):
    language = "PHP"

class RubyScanner(Scanner):
    language = "Ruby"

class SwiftScanner(Scanner):
    language = "Swift"

class KotlinScanner(Scanner):
    language = "Kotlin"

class RustScanner(Scanner):
    language = "Rust"

class ScalaScanner(Scanner):
    language = "Scala"

# Export the main classes
__all__ = [
    'Scanner', 'ScannedFile', 'JavaScriptScanner', 'TypeScriptScanner',
    'JavaScanner', 'PythonScanner', 'GoScanner', 'CSharpScanner',
    'PHPScanner', 'RubyScanner', 'SwiftScanner', 'KotlinScanner',
    'RustScanner', 'ScalaScanner'
] 