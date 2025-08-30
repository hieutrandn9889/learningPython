# 🚀 Postman MCP Server

Hệ thống AI hỗ trợ quản lý API thông qua Postman với MCP (Model Context Protocol) server. Tự động tạo và quản lý API requests, environments, và collections trong Postman.

## ✨ Tính năng chính

- 🎯 **Tạo API request tự động**: Tự động tạo request trong Postman khi có API mới
- 🌍 **Quản lý Environment**: Tạo và quản lý environment variables
- 📚 **Quản lý Collection**: Tổ chức API requests vào collections
- ✅ **Expected Status Testing**: Tự động thêm test script kiểm tra status code
- 🤖 **AI Integration**: Tích hợp với AI assistants thông qua MCP protocol
- 🔄 **CRUD Operations**: Tạo đầy đủ CRUD operations (GET, POST, PUT, DELETE)
- 🎨 **Modern UI**: Giao diện đẹp và dễ sử dụng

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Assistant  │───▶│  MCP Server      │───▶│  Postman API    │
│                 │    │  (Python)        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Postman Client  │
                       │  (HTTP Client)   │
                       └──────────────────┘
```

## 📋 Yêu cầu hệ thống

- Python 3.8+
- Postman API Key
- MCP-compatible client (Claude Desktop, etc.)

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd MCP_postman
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cấu hình Postman API Key

#### Bước 1: Lấy Postman API Key
1. Đăng nhập vào [Postman](https://www.postman.com/)
2. Vào [API Keys](https://go.postman.co/settings/me/api-keys)
3. Tạo API key mới hoặc copy key có sẵn

#### Bước 2: Tạo file .env
Tạo file `.env` trong thư mục gốc:

```env
# Required: Your Postman API Key
POSTMAN_API_KEY=PMAK-your-api-key-here

# Optional: Your Postman Collection ID
POSTMAN_COLLECTION_ID=your_collection_id

# Optional: Your Postman Environment ID  
POSTMAN_ENVIRONMENT_ID=your_environment_id
```

#### Bước 3: Lấy Collection ID và Environment ID
Chạy server để lấy thông tin collections và environments:

```bash
python simple_mcp_server.py
```

Server sẽ hiển thị danh sách collections và environments có sẵn. Copy ID và cập nhật file `.env`.

## 🎯 Cách sử dụng

### 1. Chạy MCP Server
```bash
python simple_mcp_server.py
```

### 2. Sử dụng với AI Assistant
Kết nối MCP server với AI assistant để sử dụng các tools:

## 🛠️ Available Tools

### 1. `create_crud_operations`
Tạo đầy đủ CRUD operations cho một resource:

```json
{
  "resource_name": "users",
  "base_url": "https://jsonplaceholder.typicode.com",
  "headers": {"Content-Type": "application/json"},
  "environment_name": "Users Environment"
}
```

**Kết quả:**
- ✅ GET Users List
- ✅ GET Users by ID  
- ✅ POST Create Users
- ✅ PUT Update Users
- ✅ DELETE Users

### 2. `create_api_request`
Tạo API request đơn lẻ:

```json
{
  "name": "Get User Info",
  "method": "GET",
  "url": "https://api.example.com/users/123",
  "headers": {"Authorization": "Bearer {{api_key}}"},
  "collection_id": "your_collection_id"
}
```

### 3. `create_get_request`
Tạo GET request:

```json
{
  "name": "Get Users",
  "url": "https://api.example.com/users",
  "headers": {"Content-Type": "application/json"},
  "expected_status": 200
}
```

### 4. `create_post_request`
Tạo POST request:

```json
{
  "name": "Create User",
  "url": "https://api.example.com/users",
  "headers": {"Content-Type": "application/json"},
  "body": {"name": "John Doe", "email": "john@example.com"},
  "expected_status": 201
}
```

### 5. `create_put_request`
Tạo PUT request:

```json
{
  "name": "Update User",
  "url": "https://api.example.com/users/123",
  "headers": {"Content-Type": "application/json"},
  "body": {"name": "John Updated", "email": "john.updated@example.com"},
  "expected_status": 200
}
```

### 6. `create_delete_request`
Tạo DELETE request:

```json
{
  "name": "Delete User",
  "url": "https://api.example.com/users/123",
  "headers": {"Content-Type": "application/json"},
  "expected_status": 200
}
```

### 7. `list_collections`
Lấy danh sách collections hiện có.

### 8. `list_environments`
Lấy danh sách environments hiện có.

### 9. `create_environment`
Tạo environment mới:

```json
{
  "name": "Production Environment",
  "variables": {
    "base_url": "https://api.production.com",
    "api_key": "prod_key_123",
    "timeout": "30"
  }
}
```

## 🔧 Cấu hình MCP

### Claude Desktop Configuration
Thêm vào file cấu hình MCP của Claude Desktop:

```json
{
  "mcpServers": {
    "postman": {
      "command": "python",
      "args": ["simple_mcp_server.py"],
      "env": {
        "POSTMAN_API_KEY": "PMAK-your-api-key-here"
      }
    }
  }
}
```

### Vị trí file cấu hình:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## 📁 Cấu trúc dự án

```
MCP_postman/
├── simple_mcp_server.py    # MCP server chính
├── postman_client.py       # Client tương tác với Postman API
├── models.py               # Pydantic models
├── config.py               # Cấu hình
├── .env                    # Environment variables
├── requirements.txt        # Dependencies
└── README.md              # Tài liệu này
```

## 🧪 Testing

### Test MCP Server
1. Chạy MCP server: `python simple_mcp_server.py`
2. Kết nối với MCP client (Claude Desktop)
3. Test các tools thông qua AI assistant

### Demo Commands
```python
# Tạo CRUD operations cho users
server.call_tool('create_crud_operations', {
    "resource_name": "users",
    "base_url": "https://jsonplaceholder.typicode.com"
})

# Tạo environment mới
server.call_tool('create_environment', {
    "name": "Demo Environment",
    "variables": {"base_url": "https://api.demo.com"}
})

# Lấy danh sách collections
server.call_tool('list_collections', {})
```

## 🔍 Troubleshooting

### Lỗi thường gặp

#### 1. **API Key không hợp lệ**
```
❌ Lỗi: Failed to get collections: 401 Unauthorized
```
**Giải pháp:**
- Kiểm tra Postman API key trong file `.env`
- Đảm bảo key có quyền truy cập workspace
- Tạo API key mới nếu cần

#### 2. **Collection không tồn tại**
```
❌ Lỗi: Không có collection nào và không thể tạo collection mới
```
**Giải pháp:**
- Tạo collection mới trong Postman
- Cập nhật `POSTMAN_COLLECTION_ID` trong file `.env`
- Hoặc để trống để server tự động sử dụng collection đầu tiên

#### 3. **Environment variables**
```
❌ Lỗi: Failed to create environment
```
**Giải pháp:**
- Kiểm tra format variables trong JSON
- Đảm bảo có quyền tạo environment
- Kiểm tra tên environment không trùng lặp

#### 4. **URL format issues**
```
❌ Lỗi: URL hiển thị sai trong Postman
```
**Giải pháp:**
- Đảm bảo sử dụng format `{{base_url}}/users`
- Kiểm tra environment variables đã được tạo
- Restart MCP server nếu cần

## 🚀 Sử dụng nhanh

### 1. Setup ban đầu
```bash
# Clone repository
git clone <repository-url>
cd MCP_postman

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env
echo "POSTMAN_API_KEY=PMAK-your-api-key-here" > .env

# Chạy server
python simple_mcp_server.py
```

### 2. Sử dụng với Claude Desktop
1. Mở Claude Desktop
2. Vào Settings > MCP Servers
3. Thêm cấu hình Postman MCP server
4. Restart Claude Desktop
5. Sử dụng các tools thông qua chat

### 3. Sử dụng trực tiếp
```python
from simple_mcp_server import SimplePostmanMCPServer

server = SimplePostmanMCPServer()

# Tạo CRUD operations
result = server.call_tool('create_crud_operations', {
    "resource_name": "products",
    "base_url": "https://api.example.com",
    "headers": {"Content-Type": "application/json"}
})

print(result["content"])
```

## 📊 Ví dụ sử dụng

### Tạo CRUD cho Users API
```python
# Tạo đầy đủ CRUD operations
result = server.call_tool('create_crud_operations', {
    "resource_name": "users",
    "base_url": "https://jsonplaceholder.typicode.com",
    "environment_name": "Users API Environment"
})
```

**Kết quả:**
```
🎯 CRUD Operations đã được tạo thành công cho resource: Users

📋 Các requests đã tạo:
✅ GET Users List
✅ GET Users by ID
✅ POST Create Users
✅ PUT Update Users
✅ DELETE Users

🌐 Base URL: https://jsonplaceholder.typicode.com
📚 Collection ID: 1318283-677a0958-cb1a-4598-be71-45686c305858
🌍 Environment ID: afc5f5f0-e6e9-4e9c-a135-76de5de52b9e

💡 Cách sử dụng biến:
- {{base_url}} = https://jsonplaceholder.typicode.com
- {{resource_name}} = users
- {{id}} = ID của item (sẽ được nhập khi test)

📝 Ví dụ URL: {{base_url}}/users = https://jsonplaceholder.typicode.com/users
```

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

## 📞 Hỗ trợ

- Tạo issue trên GitHub
- Liên hệ qua email: [your-email@example.com]
- Documentation: [link-to-docs]

## 🎉 Changelog

### v1.0.0 (2024-08-31)
- ✅ Tạo MCP server hoàn chỉnh
- ✅ Hỗ trợ CRUD operations
- ✅ Quản lý environments và collections
- ✅ URL format với biến environment
- ✅ Test scripts tự động
- ✅ Giao diện đẹp và dễ sử dụng

---

**Made with ❤️ for the Postman community**

*Hệ thống này giúp bạn quản lý API một cách thông minh và hiệu quả thông qua Postman và AI assistants.*
