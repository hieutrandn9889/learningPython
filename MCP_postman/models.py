"""
Data models for Postman MCP Server
"""

from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, Optional, List


class APIRequest(BaseModel):
    """Model for API request data"""
    name: str
    method: str
    url: str
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    expected_status: int = 200


class Environment(BaseModel):
    """Model for environment data"""
    name: str
    variables: Dict[str, Any]
    description: Optional[str] = None


class Collection(BaseModel):
    """Model for collection data"""
    name: str
    description: Optional[str] = None
    items: List[Dict[str, Any]] = []
