import requests
import json
from typing import Dict, Any, Optional
from config import config

class PostmanClient:
    def __init__(self):
        self.api_key = config.POSTMAN_API_KEY
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def create_environment(self, name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo environment mới trong Postman"""
        env_data = {
            "environment": {
                "name": name,
                "values": [
                    {"key": key, "value": str(value), "enabled": True}
                    for key, value in variables.items()
                ],
                "schema": "https://schema.getpostman.com/json/environment/v2.1.0/environment.json"
            }
        }
        
        response = requests.post(
            config.POSTMAN_ENVIRONMENTS_URL,
            headers=self.headers,
            json=env_data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create environment: {response.text}")
    
    def create_collection(self, name: str, description: str = "") -> Dict[str, Any]:
        """Tạo collection mới trong Postman"""
        collection_data = {
            "collection": {
                "info": {
                    "name": name,
                    "description": description,
                    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
                },
                "item": []
            }
        }
        
        response = requests.post(
            config.POSTMAN_COLLECTIONS_URL,
            headers=self.headers,
            json=collection_data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create collection: {response.text}")
    
    def _parse_url_for_postman(self, url: str) -> Dict[str, Any]:
        """Parse URL để tạo cấu trúc đúng format cho Postman với biến environment"""
        # Kiểm tra nếu URL chứa biến environment (ví dụ: {{base_url}})
        if "{{" in url and "}}" in url:
            # URL có biến environment, tạo cấu trúc đúng format cho Postman
            # Tách path từ URL để tạo cấu trúc host và path riêng biệt
            if "/" in url:
                # Tách phần base_url và path
                parts = url.split("/", 1)
                base_url_part = parts[0]  # {{base_url}}
                path_part = parts[1]      # users hoặc users/{{id}}
                
                # Tạo cấu trúc URL với host là biến và path là các phần riêng biệt
                path_parts = [part for part in path_part.split('/') if part]
                
                return {
                    "raw": url,
                    "host": [base_url_part],  # {{base_url}} như một host
                    "path": path_parts
                }
            else:
                # Chỉ có base_url, không có path
                return {
                    "raw": url,
                    "host": [url],  # {{base_url}} như một host
                    "path": []
                }
        
        # URL thông thường, parse thành các thành phần
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            # Tách host thành các phần
            host_parts = parsed.netloc.split('.')
            
            # Tách path thành các phần
            path_parts = [part for part in parsed.path.split('/') if part]
            
            return {
                "raw": url,
                "protocol": parsed.scheme,
                "host": host_parts,
                "path": path_parts,
                "query": []
            }
        except Exception:
            # Nếu không parse được, giữ nguyên raw format
            return {
                "raw": url,
                "host": [],
                "path": []
            }
    
    def add_request_to_collection(
        self, 
        collection_id: str, 
        name: str, 
        method: str, 
        url: str, 
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None,
        expected_status: int = 200
    ) -> Dict[str, Any]:
        """Thêm request mới vào collection với expected status 200"""
        
        # Tạo request item với URL được xử lý đúng format cho Postman
        request_item = {
            "name": name,
            "request": {
                "method": method.upper(),
                "header": [
                    {"key": key, "value": value, "type": "text"}
                    for key, value in (headers or {}).items()
                ],
                "url": self._parse_url_for_postman(url)
            }
        }
        
        # Thêm body nếu có
        if body:
            request_item["request"]["body"] = {
                "mode": "raw",
                "raw": json.dumps(body, indent=2),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            }
        
        # Thêm test script để kiểm tra status 200
        test_script = f"""
pm.test("Status code is {expected_status}", function () {{
    pm.response.to.have.status({expected_status});
}});

pm.test("Response time is less than 2000ms", function () {{
    pm.expect(pm.response.responseTime).to.be.below(2000);
}});
"""
        
        request_item["request"]["event"] = [
            {
                "listen": "test",
                "script": {
                    "exec": test_script.split("\n"),
                    "type": "text/javascript"
                }
            }
        ]
        
        # Lấy collection hiện tại
        collection_response = requests.get(
            f"{config.POSTMAN_COLLECTIONS_URL}/{collection_id}",
            headers=self.headers
        )
        
        if collection_response.status_code != 200:
            raise Exception(f"Failed to get collection: {collection_response.text}")
        
        collection = collection_response.json()["collection"]
        collection["item"].append(request_item)
        
        # Cập nhật collection
        update_response = requests.put(
            f"{config.POSTMAN_COLLECTIONS_URL}/{collection_id}",
            headers=self.headers,
            json={"collection": collection}
        )
        
        if update_response.status_code == 200:
            return update_response.json()
        else:
            raise Exception(f"Failed to update collection: {update_response.text}")
    
    def get_collections(self) -> Dict[str, Any]:
        """Lấy danh sách collections"""
        response = requests.get(
            config.POSTMAN_COLLECTIONS_URL,
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get collections: {response.text}")
    
    def get_environments(self) -> Dict[str, Any]:
        """Lấy danh sách environments"""
        response = requests.get(
            config.POSTMAN_ENVIRONMENTS_URL,
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get environments: {response.text}")
