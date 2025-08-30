"""
Configuration settings for Postman MCP Server
"""

import os
from dotenv import load_dotenv


class Config:
    """Configuration class for Postman MCP Server"""
    
    # Postman API URLs
    POSTMAN_COLLECTIONS_URL = "https://api.getpostman.com/collections"
    POSTMAN_ENVIRONMENTS_URL = "https://api.getpostman.com/environments"
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Postman API Configuration
        self.POSTMAN_API_KEY = os.getenv('POSTMAN_API_KEY')
        self.POSTMAN_COLLECTION_ID = os.getenv('POSTMAN_COLLECTION_ID')
        self.POSTMAN_ENVIRONMENT_ID = os.getenv('POSTMAN_ENVIRONMENT_ID')
        
        # Debug mode
        self.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    def validate(self):
        """Validate required configuration"""
        if not self.POSTMAN_API_KEY:
            raise ValueError("POSTMAN_API_KEY is required in .env file")
    
    def get_config_summary(self):
        """Get configuration summary"""
        return {
            "postman_api_key": "***" if self.POSTMAN_API_KEY else None,
            "postman_collection_id": self.POSTMAN_COLLECTION_ID,
            "postman_environment_id": self.POSTMAN_ENVIRONMENT_ID,
            "debug": self.DEBUG
        }


# Global config instance
config = Config()
