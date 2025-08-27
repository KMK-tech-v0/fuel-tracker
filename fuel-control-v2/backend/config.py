"""
Configuration settings for Advanced Fuel Consumption Forecasting System
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Database Configuration
    DB_SERVER = os.getenv('DB_SERVER', 'DESKTOP-17P73P0\\SQLEXPRESS')
    DB_NAME = os.getenv('DB_NAME', 'FuelControlV2')
    DB_DRIVER = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')
    DB_TRUSTED_CONNECTION = os.getenv('DB_TRUSTED_CONNECTION', 'yes')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'fuel-control-v2-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Forecasting Configuration
    DEFAULT_SAFETY_FACTOR = float(os.getenv('DEFAULT_SAFETY_FACTOR', '1.2'))
    FORECAST_CALCULATION_FREQUENCY = int(os.getenv('FORECAST_CALCULATION_FREQUENCY', '24'))  # hours
    LOW_STOCK_THRESHOLD = float(os.getenv('LOW_STOCK_THRESHOLD', '0.2'))  # 20% of capacity
    
    # Alert Configuration
    EMAIL_NOTIFICATIONS_ENABLED = os.getenv('EMAIL_NOTIFICATIONS_ENABLED', 'false').lower() == 'true'
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'localhost')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    @classmethod
    def get_db_connection_string(cls):
        """Generate database connection string"""
        return f"DRIVER={cls.DB_DRIVER};SERVER={cls.DB_SERVER};DATABASE={cls.DB_NAME};Trusted_Connection={cls.DB_TRUSTED_CONNECTION};"
