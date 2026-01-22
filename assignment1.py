# Configure SQLAlchemy connection string based on docker-compose environment variables
import os
DB_USER = os.getenv('DB_USER', 'student')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password123')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'default_db')
SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print("SQLAlchemy Database URI:", SQLALCHEMY_DATABASE_URI)



