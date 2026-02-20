"""
Project Analyzer - Reads and understands project structure
"""

import os
from pathlib import Path

class ProjectAnalyzer:
    def __init__(self, project_path):
        self.path = Path(project_path)
        
    def read_readme(self):
        """Read README.md if exists"""
        readme_path = self.path / "README.md"
        if readme_path.exists():
            return readme_path.read_text()
        return None
    
    def detect_tech_stack(self):
        """Detect technologies used"""
        stack = []
        if (self.path / "package.json").exists():
            stack.append("Node.js")
        if (self.path / "requirements.txt").exists():
            stack.append("Python")
        if (self.path / "Dockerfile").exists():
            stack.append("Docker")
        return stack
    
    def get_structure(self):
        """Get folder structure"""
        structure = {}
        for item in self.path.iterdir():
            if item.is_dir():
                structure[item.name] = "directory"
            else:
                structure[item.name] = "file"
        return structure
