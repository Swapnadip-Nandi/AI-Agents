"""
File Parser Tool (Custom Tool)
Parses various file formats (CSV, JSON, TXT) for data extraction.
"""

from typing import Any, Dict, List, Optional
import json
import csv
from pathlib import Path


class FileParserTool:
    """
    File parser for reading and extracting data from various formats.
    """
    
    def __init__(self):
        """Initialize file parser."""
        self.supported_formats = ['.json', '.csv', '.txt', '.md']
        self.parse_history: List[Dict] = []
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a file and extract data.
        
        Args:
            file_path: Path to file
            
        Returns:
            Parsed data
        """
        path = Path(file_path)
        
        if not path.exists():
            return {"error": "File not found", "data": None}
            
        extension = path.suffix.lower()
        
        try:
            if extension == '.json':
                return self.parse_json(file_path)
            elif extension == '.csv':
                return self.parse_csv(file_path)
            elif extension in ['.txt', '.md']:
                return self.parse_text(file_path)
            else:
                return {"error": f"Unsupported format: {extension}", "data": None}
                
        except Exception as e:
            return {"error": str(e), "data": None}
            
    def parse_json(self, file_path: str) -> Dict[str, Any]:
        """
        Parse JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            result = {
                "format": "json",
                "data": data,
                "size": Path(file_path).stat().st_size,
                "success": True
            }
            
            self.parse_history.append({
                "file": file_path,
                "format": "json",
                "success": True
            })
            
            return result
            
        except Exception as e:
            return {"error": str(e), "success": False}
            
    def parse_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Parse CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Parsed CSV data as list of dictionaries
        """
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(dict(row))
                    
            result = {
                "format": "csv",
                "data": data,
                "row_count": len(data),
                "columns": list(data[0].keys()) if data else [],
                "success": True
            }
            
            self.parse_history.append({
                "file": file_path,
                "format": "csv",
                "row_count": len(data),
                "success": True
            })
            
            return result
            
        except Exception as e:
            return {"error": str(e), "success": False}
            
    def parse_text(self, file_path: str) -> Dict[str, Any]:
        """
        Parse text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Parsed text data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            result = {
                "format": "text",
                "data": content,
                "line_count": len(content.split('\n')),
                "word_count": len(content.split()),
                "char_count": len(content),
                "success": True
            }
            
            self.parse_history.append({
                "file": file_path,
                "format": "text",
                "success": True
            })
            
            return result
            
        except Exception as e:
            return {"error": str(e), "success": False}
            
    def extract_product_data(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract product data from a file.
        
        Args:
            file_path: Path to file containing product data
            
        Returns:
            Extracted product information
        """
        parsed = self.parse_file(file_path)
        
        if not parsed.get("success"):
            return None
            
        data = parsed.get("data")
        
        # Try to extract common product fields
        product_fields = [
            "product_name", "name", "title",
            "description", "desc",
            "price", "cost",
            "category", "type",
            "brand",
            "features",
            "specifications", "specs"
        ]
        
        extracted = {}
        
        if isinstance(data, dict):
            for field in product_fields:
                for key in data.keys():
                    if field in key.lower():
                        extracted[field] = data[key]
        elif isinstance(data, list) and data:
            # Take first item if it's a list
            if isinstance(data[0], dict):
                for field in product_fields:
                    for key in data[0].keys():
                        if field in key.lower():
                            extracted[field] = data[0][key]
                            
        return extracted if extracted else data
        
    def write_json(self, data: Any, file_path: str) -> bool:
        """
        Write data to JSON file.
        
        Args:
            data: Data to write
            file_path: Output file path
            
        Returns:
            Success status
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Write error: {e}")
            return False
            
    def write_csv(self, data: List[Dict], file_path: str) -> bool:
        """
        Write data to CSV file.
        
        Args:
            data: List of dictionaries to write
            file_path: Output file path
            
        Returns:
            Success status
        """
        try:
            if not data:
                return False
                
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                
            return True
            
        except Exception as e:
            print(f"Write error: {e}")
            return False
            
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get file metadata.
        
        Args:
            file_path: Path to file
            
        Returns:
            File information
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {"error": "File not found"}
                
            stat = path.stat()
            
            return {
                "name": path.name,
                "extension": path.suffix,
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "absolute_path": str(path.absolute())
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to ADK-compatible dictionary format."""
        return {
            "name": "file_parser",
            "description": "Parse and extract data from files (JSON, CSV, TXT, MD). Can read product data and campaign information from files.",
            "parameters": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file to parse"
                },
                "operation": {
                    "type": "string",
                    "description": "Operation to perform (parse, extract_product_data, get_info)",
                    "optional": True
                }
            }
        }
