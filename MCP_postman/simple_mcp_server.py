#!/usr/bin/env python3
"""
Simple MCP Server cho Postman
Phiên bản tối ưu hóa với code DRY và cấu trúc tốt hơn
"""

import asyncio
import json
import sys
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional, Tuple
from postman_client import PostmanClient
from models import APIRequest, Environment, Collection

class URLProcessor:
    """Class xử lý URL và tách thành các thành phần"""
    
    @staticmethod
    def parse_url(url: str) -> Tuple[str, str, str]:
        """
        Tách URL thành protocol, domain và path
        Returns: (protocol, domain, path)
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed = urlparse(url)
        protocol = f"{parsed.scheme}://"
        domain = parsed.netloc
        path = parsed.path.lstrip('/')
        
        return protocol, domain, path
    
    @staticmethod
    def create_variable_url(protocol: str, domain: str, path: str = "") -> str:
        """Tạo URL với biến Postman"""
        if path:
            return f"{{{{protocol}}}}{{{{base_url}}}}/{path}"
        return f"{{{{protocol}}}}{{{{base_url}}}}"

class ResponseFormatter:
    """Class định dạng response"""
    
    @staticmethod
    def success_response(content: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Tạo response thành công"""
        response = {
            "success": True,
            "content": content
        }
        if data:
            response["data"] = data
        return response
    
    @staticmethod
    def error_response(error: str, content: str = None) -> Dict[str, Any]:
        """Tạo response lỗi"""
        return {
            "success": False,
            "error": error,
            "content": content or f"❌ Lỗi: {error}"
        }
    
    @staticmethod
    def format_request_info(name: str, method: str, url: str, collection_id: str, 
                          env_id: str = None, expected_status: int = None) -> str:
        """Format thông tin request"""
        info = f"""
✅ {method} Request đã được tạo thành công!

📋 Thông tin:
- Tên: {name}
- Method: {method}
- URL: {url}
- Collection ID: {collection_id}"""
        
        if expected_status:
            info += f"\n- Expected Status: {expected_status}"
        if env_id:
            info += f"\n- Environment ID: {env_id}"
        else:
            info += f"\n- Environment ID: Không có"
        
        info += f"\n\n🔗 Collection URL: https://go.postman.co/collection/{collection_id}"
        if env_id:
            info += f"\n🔗 Environment URL: https://go.postman.co/environment/{env_id}"
        
        return info

class EnvironmentManager:
    """Class quản lý environment"""
    
    def __init__(self, postman_client: PostmanClient, default_env_id: str = None):
        self.postman_client = postman_client
        self.default_env_id = default_env_id
    
    def create_default_environment(self, url: str, env_name: str = "Default Environment") -> Optional[str]:
        """Tạo environment mặc định từ URL"""
        try:
            protocol, domain, _ = URLProcessor.parse_url(url)
            
            env_variables = {
                "base_url": domain,
                "protocol": protocol,
                "api_key": "your_api_key_here",
                "timeout": "30"
            }
            
            env_result = self.postman_client.create_environment(env_name, env_variables)
            if env_result and 'environment' in env_result:
                env_id = env_result["environment"]["id"]
                print(f"✅ Đã tạo environment mới: {env_name} (ID: {env_id})")
                return env_id
        except Exception as e:
            print(f"⚠️  Không thể tạo environment: {str(e)}")
        
        return self.default_env_id
    
    def create_resource_environment(self, resource_name: str, base_url: str, 
                                  custom_variables: Dict[str, Any] = None) -> Optional[str]:
        """Tạo environment cho resource"""
        try:
            env_name = f"{resource_name.title()} Environment"
            env_variables = {
                "base_url": base_url,
                "resource_name": resource_name,
                "api_key": "your_api_key_here",
                "timeout": "30"
            }
            
            if custom_variables:
                env_variables.update(custom_variables)
            
            env_result = self.postman_client.create_environment(env_name, env_variables)
            if env_result and 'environment' in env_result:
                env_id = env_result["environment"]["id"]
                print(f"✅ Đã tạo environment: {env_name} (ID: {env_id})")
                return env_id
        except Exception as e:
            print(f"⚠️  Lỗi tạo environment: {str(e)}")
        
        return self.default_env_id

class SimplePostmanMCPServer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.postman_client = PostmanClient()
        self.default_collection_id = os.getenv('POSTMAN_COLLECTION_ID')
        self.default_environment_id = os.getenv('POSTMAN_ENVIRONMENT_ID')
        
        # Initialize helpers
        self.url_processor = URLProcessor()
        self.response_formatter = ResponseFormatter()
        self.env_manager = EnvironmentManager(self.postman_client, self.default_environment_id)
        
        # Load tools configuration
        self.tools = self._load_tools_config()
    
    def _load_tools_config(self) -> Dict[str, Any]:
        """Load cấu hình tools"""
        return {
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
    
    def _get_collection_id(self, args: Dict[str, Any]) -> Optional[str]:
        """Lấy collection ID từ args hoặc default"""
        collection_id = args.get("collection_id") or self.default_collection_id
        
        if not collection_id:
            # Lấy collection đầu tiên nếu không có default
            collections = self.postman_client.get_collections()
            if collections["collections"]:
                collection_id = collections["collections"][0]["id"]
                print(f"⚠️  Sử dụng collection đầu tiên: {collections['collections'][0]['name']} (ID: {collection_id})")
        
        return collection_id
    
    def _create_request_with_environment(self, method: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo request với environment support"""
        try:
            collection_id = self._get_collection_id(args)
            if not collection_id:
                return self.response_formatter.error_response(
                    "Không có collection nào và không thể tạo collection mới",
                    "❌ Lỗi: Không có collection nào trong Postman. Hãy tạo collection trước hoặc set POSTMAN_COLLECTION_ID trong file .env"
                )
            
            # Xử lý environment
            env_id = self.default_environment_id
            if not env_id:
                env_id = self.env_manager.create_default_environment(args["url"])
            
            # Xử lý URL với biến
            original_url = args["url"]
            protocol, domain, path = self.url_processor.parse_url(original_url)
            
            if env_id:
                url = self.url_processor.create_variable_url(protocol, domain, path)
            else:
                url = original_url
            
            # Tạo request
            result = self.postman_client.add_request_to_collection(
                collection_id=collection_id,
                name=args["name"],
                method=method,
                url=url,
                headers=args.get("headers", {"Content-Type": "application/json"}),
                body=args.get("body"),
                expected_status=args.get("expected_status", 200 if method != "POST" else 201)
            )
            
            if result:
                content = self.response_formatter.format_request_info(
                    args["name"], method, url, collection_id, env_id, 
                    args.get("expected_status", 200 if method != "POST" else 201)
                )
                
                # Thêm thông tin biến URL nếu có environment
                if env_id:
                    content += f"\n\n💡 Biến URL: {{{{protocol}}}}{{{{base_url}}}} = {protocol}{domain}"
                
                return self.response_formatter.success_response(content, {
                    "result": result, 
                    "environment_id": env_id,
                    "collection_id": collection_id
                })
            else:
                return self.response_formatter.error_response(f"Không thể tạo {method} request")
                
        except Exception as e:
            return self.response_formatter.error_response(str(e), f"❌ Lỗi khi tạo {method} request: {str(e)}")
    
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
            collection_id = self._get_collection_id(args)
            if not collection_id:
                return self.response_formatter.error_response(
                    "Không có collection nào và không thể tạo collection mới",
                    "❌ Lỗi: Không có collection nào trong Postman. Hãy tạo collection trước hoặc set POSTMAN_COLLECTION_ID trong file .env"
                )
            
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
            
            content = f"""
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
            
            return self.response_formatter.success_response(content, {
                "collection_id": collection_id,
                "environment_id": env_id,
                "api_request": api_request.model_dump()
            })
            
        except Exception as e:
            return self.response_formatter.error_response(str(e), f"❌ Lỗi khi tạo API request: {str(e)}")
    
    def create_crud_operations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo đầy đủ CRUD operations cho một resource"""
        try:
            resource_name = args["resource_name"]
            base_url = args["base_url"]
            collection_id = self._get_collection_id(args)
            headers = args.get("headers", {"Content-Type": "application/json"})
            
            if not collection_id:
                return self.response_formatter.error_response(
                    "Không có collection ID",
                    "❌ Lỗi: Không có collection ID. Hãy set POSTMAN_COLLECTION_ID trong file .env"
                )
            
            # Tạo environment
            env_id = self.env_manager.create_resource_environment(
                resource_name, 
                base_url, 
                args.get("environment_variables")
            )
            
            # Tạo CRUD operations
            crud_requests = []
            crud_configs = [
                ("GET", f"Get {resource_name.title()} List", f"{{{{base_url}}}}/{resource_name}", 200, None),
                ("GET", f"Get {resource_name.title()} by ID", f"{{{{base_url}}}}/{resource_name}/{{{{id}}}}", 200, None),
                ("POST", f"Create {resource_name.title()}", f"{{{{base_url}}}}/{resource_name}", 201, {"name": "Example", "description": "Example description"}),
                ("PUT", f"Update {resource_name.title()}", f"{{{{base_url}}}}/{resource_name}/{{{{id}}}}", 200, {"name": "Updated Example", "description": "Updated description"}),
                ("DELETE", f"Delete {resource_name.title()}", f"{{{{base_url}}}}/{resource_name}/{{{{id}}}}", 200, None)
            ]
            
            for method, name, url, expected_status, body in crud_configs:
                result = self.postman_client.add_request_to_collection(
                    collection_id=collection_id,
                    name=name,
                    method=method,
                    url=url,
                    headers=headers,
                    body=body,
                    expected_status=expected_status
                )
                if result:
                    crud_requests.append(f"✅ {method} {name}")
            
            content = f"""
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
            
            return self.response_formatter.success_response(content, {
                "resource_name": resource_name,
                "base_url": base_url,
                "collection_id": collection_id,
                "environment_id": env_id,
                "crud_requests": crud_requests
            })
            
        except Exception as e:
            return self.response_formatter.error_response(str(e), f"❌ Lỗi khi tạo CRUD operations: {str(e)}")
    
    def create_get_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo GET request (Read)"""
        return self._create_request_with_environment("GET", args)
    
    def create_post_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo POST request (Create)"""
        return self._create_request_with_environment("POST", args)
    
    def create_put_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo PUT request (Update)"""
        return self._create_request_with_environment("PUT", args)
    
    def create_delete_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo DELETE request (Delete)"""
        return self._create_request_with_environment("DELETE", args)
    
    def list_collections(self) -> Dict[str, Any]:
        """Lấy danh sách collections"""
        try:
            collections = self.postman_client.get_collections()
            
            if not collections["collections"]:
                return self.response_formatter.success_response("📭 Không có collections nào trong Postman")
            
            content = "📚 Danh sách Collections:\n\n"
            for collection in collections["collections"]:
                content += f"• {collection['name']} (ID: {collection['id']})\n"
                if collection.get('description'):
                    content += f"  📝 {collection['description']}\n"
                content += "\n"
            
            return self.response_formatter.success_response(content, collections)
            
        except Exception as e:
            return self.response_formatter.error_response(str(e), f"❌ Lỗi khi lấy danh sách collections: {str(e)}")
    
    def list_environments(self) -> Dict[str, Any]:
        """Lấy danh sách environments"""
        try:
            environments = self.postman_client.get_environments()
            
            if not environments["environments"]:
                return self.response_formatter.success_response("🌍 Không có environments nào trong Postman")
            
            content = "🌍 Danh sách Environments:\n\n"
            for env in environments["environments"]:
                content += f"• {env['name']} (ID: {env['id']})\n"
                if env.get('description'):
                    content += f"  📝 {env['description']}\n"
                content += "\n"
            
            return self.response_formatter.success_response(content, environments)
            
        except Exception as e:
            return self.response_formatter.error_response(str(e), f"❌ Lỗi khi lấy danh sách environments: {str(e)}")
    
    def create_environment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo environment mới"""
        try:
            result = self.postman_client.create_environment(
                args["name"],
                args["variables"]
            )
            
            content = f"""
✅ Environment đã được tạo thành công!

🌍 Thông tin:
- Tên: {args['name']}
- ID: {result['environment']['id']}
- Variables: {len(args['variables'])} variables

🔗 Environment URL: https://go.postman.co/environment/{result['environment']['id']}
"""
            
            return self.response_formatter.success_response(content, result)
            
        except Exception as e:
            return self.response_formatter.error_response(str(e), f"❌ Lỗi khi tạo environment: {str(e)}")
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Gọi tool theo tên"""
        tool_methods = {
            "create_api_request": self.create_api_request,
            "create_crud_operations": self.create_crud_operations,
            "create_get_request": self.create_get_request,
            "create_post_request": self.create_post_request,
            "create_put_request": self.create_put_request,
            "create_delete_request": self.create_delete_request,
            "list_collections": self.list_collections,
            "list_environments": self.list_environments,
            "create_environment": self.create_environment
        }
        
        if name in tool_methods:
            return tool_methods[name](arguments)
        else:
            return self.response_formatter.error_response(f"Unknown tool: {name}", f"❌ Tool không tồn tại: {name}")

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
