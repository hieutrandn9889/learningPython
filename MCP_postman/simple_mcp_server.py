#!/usr/bin/env python3
"""
Simple MCP Server cho Postman
Phiên bản đơn giản để tránh các vấn đề import phức tạp
"""

import asyncio
import json
import sys
import os
from dotenv import load_dotenv
from typing import Any, Dict, List
from postman_client import PostmanClient
from models import APIRequest, Environment, Collection

class SimplePostmanMCPServer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.postman_client = PostmanClient()
        self.default_collection_id = os.getenv('POSTMAN_COLLECTION_ID')
        self.default_environment_id = os.getenv('POSTMAN_ENVIRONMENT_ID')
        
        self.tools = {
            "create_api_request": {
                "description": "Tạo API request mới trong Postman với expected status 200",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Tên của API request"},
                        "method": {"type": "string", "description": "HTTP method (GET, POST, PUT, DELETE)"},
                        "url": {"type": "string", "description": "URL của API"},
                        "headers": {"type": "object", "description": "Headers của request"},
                        "body": {"type": "object", "description": "Body của request (cho POST/PUT)"},
                        "collection_id": {"type": "string", "description": "ID của collection (nếu không có sẽ dùng default)"},
                        "environment_name": {"type": "string", "description": "Tên environment để tạo"},
                        "environment_variables": {"type": "object", "description": "Variables cho environment"}
                    },
                    "required": ["name", "method", "url"]
                }
            },
            "create_crud_operations": {
                "description": "Tạo đầy đủ CRUD operations (GET, POST, PUT, DELETE) cho một resource",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource_name": {"type": "string", "description": "Tên resource (ví dụ: users, posts, products)"},
                        "base_url": {"type": "string", "description": "Base URL của API (ví dụ: https://api.example.com)"},
                        "collection_id": {"type": "string", "description": "ID của collection (nếu không có sẽ dùng default)"},
                        "headers": {"type": "object", "description": "Headers chung cho tất cả requests"},
                        "environment_name": {"type": "string", "description": "Tên environment để tạo"},
                        "environment_variables": {"type": "object", "description": "Variables cho environment"}
                    },
                    "required": ["resource_name", "base_url"]
                }
            },
            "create_get_request": {
                "description": "Tạo GET request để lấy dữ liệu (Read)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Tên của GET request"},
                        "url": {"type": "string", "description": "URL của API"},
                        "collection_id": {"type": "string", "description": "ID của collection"},
                        "headers": {"type": "object", "description": "Headers của request"},
                        "expected_status": {"type": "integer", "description": "Expected status code (mặc định: 200)"}
                    },
                    "required": ["name", "url"]
                }
            },
            "create_post_request": {
                "description": "Tạo POST request để tạo dữ liệu mới (Create)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Tên của POST request"},
                        "url": {"type": "string", "description": "URL của API"},
                        "collection_id": {"type": "string", "description": "ID của collection"},
                        "headers": {"type": "object", "description": "Headers của request"},
                        "body": {"type": "object", "description": "Body của request"},
                        "expected_status": {"type": "integer", "description": "Expected status code (mặc định: 201)"}
                    },
                    "required": ["name", "url"]
                }
            },
            "create_put_request": {
                "description": "Tạo PUT request để cập nhật dữ liệu (Update)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Tên của PUT request"},
                        "url": {"type": "string", "description": "URL của API"},
                        "collection_id": {"type": "string", "description": "ID của collection"},
                        "headers": {"type": "object", "description": "Headers của request"},
                        "body": {"type": "object", "description": "Body của request"},
                        "expected_status": {"type": "integer", "description": "Expected status code (mặc định: 200)"}
                    },
                    "required": ["name", "url"]
                }
            },
            "create_delete_request": {
                "description": "Tạo DELETE request để xóa dữ liệu (Delete)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Tên của DELETE request"},
                        "url": {"type": "string", "description": "URL của API"},
                        "collection_id": {"type": "string", "description": "ID của collection"},
                        "headers": {"type": "object", "description": "Headers của request"},
                        "expected_status": {"type": "integer", "description": "Expected status code (mặc định: 200)"}
                    },
                    "required": ["name", "url"]
                }
            },
            "list_collections": {
                "description": "Lấy danh sách collections trong Postman",
                "inputSchema": {"type": "object", "properties": {}}
            },
            "list_environments": {
                "description": "Lấy danh sách environments trong Postman",
                "inputSchema": {"type": "object", "properties": {}}
            },
            "create_environment": {
                "description": "Tạo environment mới trong Postman",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Tên environment"},
                        "variables": {"type": "object", "description": "Variables cho environment"}
                    },
                    "required": ["name", "variables"]
                }
            }
        }
    
    def list_tools(self) -> Dict[str, Any]:
        """Trả về danh sách tools có sẵn"""
        return {
            "tools": [
                {
                    "name": name,
                    "description": tool["description"],
                    "inputSchema": tool["inputSchema"]
                }
                for name, tool in self.tools.items()
            ]
        }
    
    def create_api_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo API request mới trong Postman"""
        try:
            # Tạo environment nếu được chỉ định
            env_id = None
            if args.get("environment_name") and args.get("environment_variables"):
                env_result = self.postman_client.create_environment(
                    args["environment_name"],
                    args["environment_variables"]
                )
                env_id = env_result["environment"]["id"]
            elif self.default_environment_id:
                env_id = self.default_environment_id
            
            # Lấy collection ID
            collection_id = args.get("collection_id") or self.default_collection_id
            
            if not collection_id:
                # Nếu không có collection_id, lấy collection đầu tiên
                collections = self.postman_client.get_collections()
                if collections["collections"]:
                    collection_id = collections["collections"][0]["id"]
                    print(f"⚠️  Sử dụng collection đầu tiên: {collections['collections'][0]['name']} (ID: {collection_id})")
                else:
                    return {
                        "success": False,
                        "error": "Không có collection nào và không thể tạo collection mới",
                        "content": "❌ Lỗi: Không có collection nào trong Postman. Hãy tạo collection trước hoặc set POSTMAN_COLLECTION_ID trong file .env"
                    }
            
            # Tạo API request
            api_request = APIRequest(
                name=args["name"],
                method=args["method"],
                url=args["url"],
                headers=args.get("headers"),
                body=args.get("body"),
                expected_status=200
            )
            
            # Thêm request vào collection
            result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=api_request.name,
                method=api_request.method,
                url=api_request.url,
                headers=api_request.headers,
                body=api_request.body,
                expected_status=200
            )
            
            response_text = f"""
✅ API Request đã được tạo thành công!

📋 Thông tin:
- Tên: {api_request.name}
- Method: {api_request.method}
- URL: {api_request.url}
- Collection ID: {collection_id}
- Expected Status: 200
- Environment ID: {env_id if env_id else 'Không có'}

🔗 Collection URL: https://go.postman.co/collection/{collection_id}
"""
            
            return {
                "success": True,
                "content": response_text,
                "data": {
                    "collection_id": collection_id,
                    "environment_id": env_id,
                    "api_request": api_request.model_dump()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi tạo API request: {str(e)}"
            }
    
    def create_crud_operations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo đầy đủ CRUD operations cho một resource"""
        try:
            resource_name = args["resource_name"]
            base_url = args["base_url"]
            collection_id = args.get("collection_id") or self.default_collection_id
            headers = args.get("headers", {"Content-Type": "application/json"})
            
            if not collection_id:
                return {
                    "success": False,
                    "error": "Không có collection ID",
                    "content": "❌ Lỗi: Không có collection ID. Hãy set POSTMAN_COLLECTION_ID trong file .env"
                }
            
            # Tạo environment với biến URL
            env_id = None
            env_name = args.get("environment_name") or f"{resource_name.title()} Environment"
            
            # Tạo environment variables với base_url đầy đủ (bao gồm protocol)
            env_variables = {
                "base_url": base_url,  # Chứa cả protocol và domain (ví dụ: https://jsonplaceholder.typicode.com)
                "resource_name": resource_name,
                "api_key": "your_api_key_here",
                "timeout": "30"
            }
            
            # Merge với environment variables được chỉ định
            if args.get("environment_variables"):
                env_variables.update(args["environment_variables"])
            
            try:
                # Tạo environment mới
                env_result = self.postman_client.create_environment(env_name, env_variables)
                if env_result and 'environment' in env_result:
                    env_id = env_result["environment"]["id"]
                    print(f"✅ Đã tạo environment: {env_name} (ID: {env_id})")
                else:
                    print(f"⚠️  Không thể tạo environment: {env_result}")
                    # Sử dụng environment có sẵn nếu có
                    if self.default_environment_id:
                        env_id = self.default_environment_id
                        print(f"⚠️  Sử dụng environment mặc định: {env_id}")
            except Exception as e:
                print(f"⚠️  Lỗi tạo environment: {str(e)}")
                # Sử dụng environment có sẵn nếu có
                if self.default_environment_id:
                    env_id = self.default_environment_id
                    print(f"⚠️  Sử dụng environment mặc định: {env_id}")
            
            # Tạo CRUD operations với biến URL đúng format
            crud_requests = []
            
            # 1. GET - Lấy danh sách (Read)
            get_list_result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=f"Get {resource_name.title()} List",
                method="GET",
                url=f"{{{{base_url}}}}/{resource_name}",  # Sử dụng biến base_url đầy đủ
                headers=headers,
                expected_status=200
            )
            if get_list_result:
                crud_requests.append(f"✅ GET {resource_name.title()} List")
            
            # 2. GET - Lấy theo ID (Read)
            get_by_id_result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=f"Get {resource_name.title()} by ID",
                method="GET",
                url=f"{{{{base_url}}}}/{resource_name}/{{{{id}}}}",  # Sử dụng biến base_url đầy đủ + id
                headers=headers,
                expected_status=200
            )
            if get_by_id_result:
                crud_requests.append(f"✅ GET {resource_name.title()} by ID")
            
            # 3. POST - Tạo mới (Create)
            post_result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=f"Create {resource_name.title()}",
                method="POST",
                url=f"{{{{base_url}}}}/{resource_name}",  # Sử dụng biến base_url đầy đủ
                headers=headers,
                body={"name": "Example", "description": "Example description"},
                expected_status=201
            )
            if post_result:
                crud_requests.append(f"✅ POST Create {resource_name.title()}")
            
            # 4. PUT - Cập nhật (Update)
            put_result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=f"Update {resource_name.title()}",
                method="PUT",
                url=f"{{{{base_url}}}}/{resource_name}/{{{{id}}}}",  # Sử dụng biến base_url đầy đủ + id
                headers=headers,
                body={"name": "Updated Example", "description": "Updated description"},
                expected_status=200
            )
            if put_result:
                crud_requests.append(f"✅ PUT Update {resource_name.title()}")
            
            # 5. DELETE - Xóa (Delete)
            delete_result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=f"Delete {resource_name.title()}",
                method="DELETE",
                url=f"{{{{base_url}}}}/{resource_name}/{{{{id}}}}",  # Sử dụng biến base_url đầy đủ + id
                headers=headers,
                expected_status=200
            )
            if delete_result:
                crud_requests.append(f"✅ DELETE {resource_name.title()}")
            
            response_text = f"""
🎯 CRUD Operations đã được tạo thành công cho resource: {resource_name.title()}

📋 Các requests đã tạo:
{chr(10).join(crud_requests)}

🌐 Base URL: {base_url}
📚 Collection ID: {collection_id}
🌍 Environment ID: {env_id if env_id else 'Không có'}

🔗 Collection URL: https://go.postman.co/collection/{collection_id}
🔗 Environment URL: https://go.postman.co/environment/{env_id if env_id else 'N/A'}

💡 Cách sử dụng biến:
- {{base_url}} = {base_url} (bao gồm cả protocol và domain)
- {{resource_name}} = {resource_name}
- {{id}} = ID của item (sẽ được nhập khi test)

📝 Ví dụ URL: {{base_url}}/users = {base_url}/users
"""
            
            return {
                "success": True,
                "content": response_text,
                "data": {
                    "resource_name": resource_name,
                    "base_url": base_url,
                    "collection_id": collection_id,
                    "environment_id": env_id,
                    "crud_requests": crud_requests,
                    "environment_variables": env_variables
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi tạo CRUD operations: {str(e)}"
            }
    
    def create_get_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo GET request (Read)"""
        try:
            collection_id = args.get("collection_id") or self.default_collection_id
            expected_status = args.get("expected_status", 200)
            
            if not collection_id:
                return {
                    "success": False,
                    "error": "Không có collection ID",
                    "content": "❌ Lỗi: Không có collection ID"
                }
            
            # Tạo environment với biến URL nếu chưa có
            env_id = self.default_environment_id
            if not env_id:
                try:
                    # Tách protocol và domain từ URL
                    url = args["url"]
                    if url.startswith("http://"):
                        protocol = "http://"
                        domain = url[7:]  # Bỏ "http://"
                    elif url.startswith("https://"):
                        protocol = "https://"
                        domain = url[8:]  # Bỏ "https://"
                    else:
                        protocol = "https://"  # Mặc định là https
                        domain = url
                    
                    # Tách path từ domain
                    if "/" in domain:
                        domain_parts = domain.split("/", 1)
                        base_domain = domain_parts[0]
                        path = domain_parts[1]
                    else:
                        base_domain = domain
                        path = ""
                    
                    env_variables = {
                        "base_url": base_domain,  # Chỉ chứa domain
                        "protocol": protocol,  # Protocol riêng biệt
                        "api_key": "your_api_key_here",
                        "timeout": "30"
                    }
                    
                    env_result = self.postman_client.create_environment("Default Environment", env_variables)
                    if env_result and 'environment' in env_result:
                        env_id = env_result["environment"]["id"]
                        print(f"✅ Đã tạo environment mới: Default Environment (ID: {env_id})")
                except Exception as e:
                    print(f"⚠️  Không thể tạo environment: {str(e)}")
            
            # Sử dụng biến URL nếu có thể
            url = args["url"]
            if env_id:
                # Thay thế base_url bằng biến
                if url.startswith("http://"):
                    protocol = "http://"
                    domain = url[7:]
                elif url.startswith("https://"):
                    protocol = "https://"
                    domain = url[8:]
                else:
                    protocol = "https://"
                    domain = url
                
                if "/" in domain:
                    domain_parts = domain.split("/", 1)
                    base_domain = domain_parts[0]
                    path = domain_parts[1]
                    url = f"{{{{protocol}}}}{{{{base_url}}}}/{path}"
                else:
                    url = f"{{{{protocol}}}}{{{{base_url}}}}"
            
            result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=args["name"],
                method="GET",
                url=url,
                headers=args.get("headers", {"Content-Type": "application/json"}),
                expected_status=expected_status
            )
            
            if result:
                response_text = f"""
✅ GET Request đã được tạo thành công!

📋 Thông tin:
- Tên: {args['name']}
- Method: GET
- URL: {url}
- Expected Status: {expected_status}
- Collection ID: {collection_id}
- Environment ID: {env_id if env_id else 'Không có'}

🔗 Collection URL: https://go.postman.co/collection/{collection_id}
🔗 Environment URL: https://go.postman.co/environment/{env_id if env_id else 'N/A'}

💡 Biến URL: {{{{protocol}}}}{{{{base_url}}}} = {protocol if env_id else 'N/A'}{base_domain if env_id else 'N/A'}
"""
                return {
                    "success": True,
                    "content": response_text,
                    "data": {"result": result, "environment_id": env_id}
                }
            else:
                return {
                    "success": False,
                    "error": "Không thể tạo GET request",
                    "content": "❌ Lỗi: Không thể tạo GET request"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi tạo GET request: {str(e)}"
            }
    
    def create_post_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo POST request (Create)"""
        try:
            collection_id = args.get("collection_id") or self.default_collection_id
            expected_status = args.get("expected_status", 201)
            
            if not collection_id:
                return {
                    "success": False,
                    "error": "Không có collection ID",
                    "content": "❌ Lỗi: Không có collection ID"
                }
            
            # Tạo environment với biến URL nếu chưa có
            env_id = self.default_environment_id
            if not env_id:
                try:
                    # Tách protocol và domain từ URL
                    url = args["url"]
                    if url.startswith("http://"):
                        protocol = "http://"
                        domain = url[7:]  # Bỏ "http://"
                    elif url.startswith("https://"):
                        protocol = "https://"
                        domain = url[8:]  # Bỏ "https://"
                    else:
                        protocol = "https://"  # Mặc định là https
                        domain = url
                    
                    # Tách path từ domain
                    if "/" in domain:
                        domain_parts = domain.split("/", 1)
                        base_domain = domain_parts[0]
                        path = domain_parts[1]
                    else:
                        base_domain = domain
                        path = ""
                    
                    env_variables = {
                        "base_url": base_domain,  # Chỉ chứa domain
                        "protocol": protocol,  # Protocol riêng biệt
                        "api_key": "your_api_key_here",
                        "timeout": "30"
                    }
                    
                    env_result = self.postman_client.create_environment("Default Environment", env_variables)
                    if env_result and 'environment' in env_result:
                        env_id = env_result["environment"]["id"]
                        print(f"✅ Đã tạo environment mới: Default Environment (ID: {env_id})")
                except Exception as e:
                    print(f"⚠️  Không thể tạo environment: {str(e)}")
            
            # Sử dụng biến URL nếu có thể
            url = args["url"]
            if env_id:
                # Thay thế base_url bằng biến
                if url.startswith("http://"):
                    protocol = "http://"
                    domain = url[7:]
                elif url.startswith("https://"):
                    protocol = "https://"
                    domain = url[8:]
                else:
                    protocol = "https://"
                    domain = url
                
                if "/" in domain:
                    domain_parts = domain.split("/", 1)
                    base_domain = domain_parts[0]
                    path = domain_parts[1]
                    url = f"{{{{protocol}}}}{{{{base_url}}}}/{path}"
                else:
                    url = f"{{{{protocol}}}}{{{{base_url}}}}"
            
            result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=args["name"],
                method="POST",
                url=url,
                headers=args.get("headers", {"Content-Type": "application/json"}),
                body=args.get("body", {}),
                expected_status=expected_status
            )
            
            if result:
                response_text = f"""
✅ POST Request đã được tạo thành công!

📋 Thông tin:
- Tên: {args['name']}
- Method: POST
- URL: {url}
- Expected Status: {expected_status}
- Collection ID: {collection_id}
- Environment ID: {env_id if env_id else 'Không có'}

🔗 Collection URL: https://go.postman.co/collection/{collection_id}
🔗 Environment URL: https://go.postman.co/environment/{env_id if env_id else 'N/A'}

💡 Biến URL: {{{{protocol}}}}{{{{base_url}}}} = {protocol if env_id else 'N/A'}{base_domain if env_id else 'N/A'}
"""
                return {
                    "success": True,
                    "content": response_text,
                    "data": {"result": result, "environment_id": env_id}
                }
            else:
                return {
                    "success": False,
                    "error": "Không thể tạo POST request",
                    "content": "❌ Lỗi: Không thể tạo POST request"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi tạo POST request: {str(e)}"
            }
    
    def create_put_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo PUT request (Update)"""
        try:
            collection_id = args.get("collection_id") or self.default_collection_id
            expected_status = args.get("expected_status", 200)
            
            if not collection_id:
                return {
                    "success": False,
                    "error": "Không có collection ID",
                    "content": "❌ Lỗi: Không có collection ID"
                }
            
            # Tạo environment với biến URL nếu chưa có
            env_id = self.default_environment_id
            if not env_id:
                try:
                    # Tách protocol và domain từ URL
                    url = args["url"]
                    if url.startswith("http://"):
                        protocol = "http://"
                        domain = url[7:]  # Bỏ "http://"
                    elif url.startswith("https://"):
                        protocol = "https://"
                        domain = url[8:]  # Bỏ "https://"
                    else:
                        protocol = "https://"  # Mặc định là https
                        domain = url
                    
                    # Tách path từ domain
                    if "/" in domain:
                        domain_parts = domain.split("/", 1)
                        base_domain = domain_parts[0]
                        path = domain_parts[1]
                    else:
                        base_domain = domain
                        path = ""
                    
                    env_variables = {
                        "base_url": base_domain,  # Chỉ chứa domain
                        "protocol": protocol,  # Protocol riêng biệt
                        "api_key": "your_api_key_here",
                        "timeout": "30"
                    }
                    
                    env_result = self.postman_client.create_environment("Default Environment", env_variables)
                    if env_result and 'environment' in env_result:
                        env_id = env_result["environment"]["id"]
                        print(f"✅ Đã tạo environment mới: Default Environment (ID: {env_id})")
                except Exception as e:
                    print(f"⚠️  Không thể tạo environment: {str(e)}")
            
            # Sử dụng biến URL nếu có thể
            url = args["url"]
            if env_id:
                # Thay thế base_url bằng biến
                if url.startswith("http://"):
                    protocol = "http://"
                    domain = url[7:]
                elif url.startswith("https://"):
                    protocol = "https://"
                    domain = url[8:]
                else:
                    protocol = "https://"
                    domain = url
                
                if "/" in domain:
                    domain_parts = domain.split("/", 1)
                    base_domain = domain_parts[0]
                    path = domain_parts[1]
                    url = f"{{{{protocol}}}}{{{{base_url}}}}/{path}"
                else:
                    url = f"{{{{protocol}}}}{{{{base_url}}}}"
            
            result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=args["name"],
                method="PUT",
                url=url,
                headers=args.get("headers", {"Content-Type": "application/json"}),
                body=args.get("body", {}),
                expected_status=expected_status
            )
            
            if result:
                response_text = f"""
✅ PUT Request đã được tạo thành công!

📋 Thông tin:
- Tên: {args['name']}
- Method: PUT
- URL: {url}
- Expected Status: {expected_status}
- Collection ID: {collection_id}
- Environment ID: {env_id if env_id else 'Không có'}

🔗 Collection URL: https://go.postman.co/collection/{collection_id}
🔗 Environment URL: https://go.postman.co/environment/{env_id if env_id else 'N/A'}

💡 Biến URL: {{{{protocol}}}}{{{{base_url}}}} = {protocol if env_id else 'N/A'}{base_domain if env_id else 'N/A'}
"""
                return {
                    "success": True,
                    "content": response_text,
                    "data": {"result": result, "environment_id": env_id}
                }
            else:
                return {
                    "success": False,
                    "error": "Không thể tạo PUT request",
                    "content": "❌ Lỗi: Không thể tạo PUT request"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi tạo PUT request: {str(e)}"
            }
    
    def create_delete_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo DELETE request (Delete)"""
        try:
            collection_id = args.get("collection_id") or self.default_collection_id
            expected_status = args.get("expected_status", 200)
            
            if not collection_id:
                return {
                    "success": False,
                    "error": "Không có collection ID",
                    "content": "❌ Lỗi: Không có collection ID"
                }
            
            # Tạo environment với biến URL nếu chưa có
            env_id = self.default_environment_id
            if not env_id:
                try:
                    # Tách protocol và domain từ URL
                    url = args["url"]
                    if url.startswith("http://"):
                        protocol = "http://"
                        domain = url[7:]  # Bỏ "http://"
                    elif url.startswith("https://"):
                        protocol = "https://"
                        domain = url[8:]  # Bỏ "https://"
                    else:
                        protocol = "https://"  # Mặc định là https
                        domain = url
                    
                    # Tách path từ domain
                    if "/" in domain:
                        domain_parts = domain.split("/", 1)
                        base_domain = domain_parts[0]
                        path = domain_parts[1]
                    else:
                        base_domain = domain
                        path = ""
                    
                    env_variables = {
                        "base_url": base_domain,  # Chỉ chứa domain
                        "protocol": protocol,  # Protocol riêng biệt
                        "api_key": "your_api_key_here",
                        "timeout": "30"
                    }
                    
                    env_result = self.postman_client.create_environment("Default Environment", env_variables)
                    if env_result and 'environment' in env_result:
                        env_id = env_result["environment"]["id"]
                        print(f"✅ Đã tạo environment mới: Default Environment (ID: {env_id})")
                except Exception as e:
                    print(f"⚠️  Không thể tạo environment: {str(e)}")
            
            # Sử dụng biến URL nếu có thể
            url = args["url"]
            if env_id:
                # Thay thế base_url bằng biến
                if url.startswith("http://"):
                    protocol = "http://"
                    domain = url[7:]
                elif url.startswith("https://"):
                    protocol = "https://"
                    domain = url[8:]
                else:
                    protocol = "https://"
                    domain = url
                
                if "/" in domain:
                    domain_parts = domain.split("/", 1)
                    base_domain = domain_parts[0]
                    path = domain_parts[1]
                    url = f"{{{{protocol}}}}{{{{base_url}}}}/{path}"
                else:
                    url = f"{{{{protocol}}}}{{{{base_url}}}}"
            
            result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=args["name"],
                method="DELETE",
                url=url,
                headers=args.get("headers", {"Content-Type": "application/json"}),
                expected_status=expected_status
            )
            
            if result:
                response_text = f"""
✅ DELETE Request đã được tạo thành công!

📋 Thông tin:
- Tên: {args['name']}
- Method: DELETE
- URL: {url}
- Expected Status: {expected_status}
- Collection ID: {collection_id}
- Environment ID: {env_id if env_id else 'Không có'}

🔗 Collection URL: https://go.postman.co/collection/{collection_id}
🔗 Environment URL: https://go.postman.co/environment/{env_id if env_id else 'N/A'}

💡 Biến URL: {{{{protocol}}}}{{{{base_url}}}} = {protocol if env_id else 'N/A'}{base_domain if env_id else 'N/A'}
"""
                return {
                    "success": True,
                    "content": response_text,
                    "data": {"result": result, "environment_id": env_id}
                }
            else:
                return {
                    "success": False,
                    "error": "Không thể tạo DELETE request",
                    "content": "❌ Lỗi: Không thể tạo DELETE request"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi tạo DELETE request: {str(e)}"
            }
    
    def list_collections(self) -> Dict[str, Any]:
        """Lấy danh sách collections"""
        try:
            collections = self.postman_client.get_collections()
            
            if not collections["collections"]:
                return {
                    "success": True,
                    "content": "📭 Không có collections nào trong Postman"
                }
            
            response_text = "📚 Danh sách Collections:\n\n"
            for collection in collections["collections"]:
                response_text += f"• {collection['name']} (ID: {collection['id']})\n"
                if collection.get('description'):
                    response_text += f"  📝 {collection['description']}\n"
                response_text += "\n"
            
            return {
                "success": True,
                "content": response_text,
                "data": collections
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi lấy danh sách collections: {str(e)}"
            }
    
    def list_environments(self) -> Dict[str, Any]:
        """Lấy danh sách environments"""
        try:
            environments = self.postman_client.get_environments()
            
            if not environments["environments"]:
                return {
                    "success": True,
                    "content": "🌍 Không có environments nào trong Postman"
                }
            
            response_text = "🌍 Danh sách Environments:\n\n"
            for env in environments["environments"]:
                response_text += f"• {env['name']} (ID: {env['id']})\n"
                if env.get('description'):
                    response_text += f"  📝 {env['description']}\n"
                response_text += "\n"
            
            return {
                "success": True,
                "content": response_text,
                "data": environments
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi lấy danh sách environments: {str(e)}"
            }
    
    def create_environment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo environment mới"""
        try:
            result = self.postman_client.create_environment(
                args["name"],
                args["variables"]
            )
            
            response_text = f"""
✅ Environment đã được tạo thành công!

🌍 Thông tin:
- Tên: {args['name']}
- ID: {result['environment']['id']}
- Variables: {len(args['variables'])} variables

🔗 Environment URL: https://go.postman.co/environment/{result['environment']['id']}
"""
            
            return {
                "success": True,
                "content": response_text,
                "data": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": f"❌ Lỗi khi tạo environment: {str(e)}"
            }
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Gọi tool theo tên"""
        if name == "create_api_request":
            return self.create_api_request(arguments)
        elif name == "create_crud_operations":
            return self.create_crud_operations(arguments)
        elif name == "create_get_request":
            return self.create_get_request(arguments)
        elif name == "create_post_request":
            return self.create_post_request(arguments)
        elif name == "create_put_request":
            return self.create_put_request(arguments)
        elif name == "create_delete_request":
            return self.create_delete_request(arguments)
        elif name == "list_collections":
            return self.list_collections()
        elif name == "list_environments":
            return self.list_environments()
        elif name == "create_environment":
            return self.create_environment(arguments)
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {name}",
                "content": f"❌ Tool không tồn tại: {name}"
            }

def main():
    """Main function để chạy server"""
    server = SimplePostmanMCPServer()
    
    print("🚀 Simple Postman MCP Server đã sẵn sàng!")
    print("📋 Các tools có sẵn:")
    
    tools = server.list_tools()
    for tool in tools["tools"]:
        print(f"  • {tool['name']}: {tool['description']}")
    
    # Hiển thị thông tin cấu hình
    print(f"\n⚙️  Cấu hình:")
    print(f"  • Default Collection ID: {server.default_collection_id or 'Không có'}")
    print(f"  • Default Environment ID: {server.default_environment_id or 'Không có'}")
    
    print("\n💡 Để sử dụng, gọi server.call_tool(tool_name, arguments)")
    print("💡 Ví dụ: server.call_tool('list_collections', {})")
    
    # Demo các tools
    print("\n🧪 Demo các tools:")
    
    # Demo list collections
    print("\n1. Lấy danh sách collections:")
    result = server.list_collections()
    print(result["content"])
    
    # Demo create environment
    print("\n2. Tạo environment mới:")
    env_result = server.create_environment({
        "name": "Demo Environment",
        "variables": {
            "base_url": "https://api.demo.com",
            "api_key": "demo_key_123"
        }
    })
    print(env_result["content"])
    
    # Demo create CRUD operations
    if server.default_collection_id:
        print("\n3. Tạo CRUD operations cho users:")
        crud_result = server.call_tool('create_crud_operations', {
            "resource_name": "users",
            "base_url": "https://jsonplaceholder.typicode.com",
            "headers": {"Content-Type": "application/json"}
        })
        print(crud_result["content"])
    else:
        print("\n3. Không thể tạo CRUD operations - thiếu POSTMAN_COLLECTION_ID")

if __name__ == "__main__":
    main()
