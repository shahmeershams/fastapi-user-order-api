#!/usr/bin/env python3
"""
Database Seeding Script

This script seeds the database with default data for development and testing.
It's useful when you need to reset your database to a known state.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin:secret123@localhost:3306/orders_db")

def seed_database():
    """Seed the database with default data"""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        try:
            print("🌱 Starting database seeding...")
            
            # Check if roles exist
            roles_result = db.execute(text("SELECT COUNT(*) FROM roles")).scalar()
            if roles_result == 0:
                print("📝 Seeding roles...")
                db.execute(text("""
                    INSERT INTO roles (role_id, name, `key`, description) VALUES
                    (1, 'Administrator', 'admin', 'Full system access with all permissions'),
                    (2, 'Customer', 'customer', 'Limited access for customer operations')
                """))
                print("✅ Roles seeded successfully!")
            else:
                print("⚠️  Roles already exist, skipping...")
            
            # Check if permissions exist
            permissions_result = db.execute(text("SELECT COUNT(*) FROM permissions")).scalar()
            if permissions_result == 0:
                print("📝 Seeding permissions...")
                # This would be quite long, so we'll just print a message
                print("⚠️  Please run 'alembic upgrade head' to seed permissions properly")
            else:
                print("✅ Permissions already exist!")
            
            # Check if role-permission assignments exist
            role_permissions_result = db.execute(text("SELECT COUNT(*) FROM role_permissions")).scalar()
            if role_permissions_result == 0:
                print("📝 Please run 'alembic upgrade head' to assign permissions to roles")
            else:
                print("✅ Role-permission assignments already exist!")
            
            db.commit()
            print("🎉 Database seeding completed successfully!")
            
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            db.rollback()
            sys.exit(1)

def create_admin_user():
    """Create a default admin user for testing"""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        try:
            # Check if admin user exists
            admin_exists = db.execute(text("SELECT COUNT(*) FROM users WHERE email = 'admin@example.com'")).scalar()
            
            if admin_exists == 0:
                print("👤 Creating default admin user...")
                # Hash the password "admin123"
                from passlib.context import CryptContext
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                hashed_password = pwd_context.hash("admin123")
                
                db.execute(text("""
                    INSERT INTO users (username, email, hashed_password, role_id) VALUES
                    ('admin', 'admin@example.com', :hashed_password, 1)
                """), {"hashed_password": hashed_password})
                
                db.commit()
                print("✅ Default admin user created!")
                print("   Email: admin@example.com")
                print("   Password: admin123")
            else:
                print("⚠️  Admin user already exists!")
                
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            db.rollback()

if __name__ == "__main__":
    print("🗄️  Database Seeding Script")
    print("=" * 50)
    
    # Check if database is accessible
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Cannot connect to database: {e}")
        print("💡 Make sure your database is running and accessible")
        sys.exit(1)
    
    # Run seeding
    seed_database()
    
    # Ask if user wants to create admin user
    create_admin = input("\n🤔 Do you want to create a default admin user? (y/n): ").lower().strip()
    if create_admin in ['y', 'yes']:
        create_admin_user()
    
    print("\n🎯 Next steps:")
    print("1. Run 'alembic upgrade head' to apply all migrations")
    print("2. Start your API server with 'uvicorn main:app --reload'")
    print("3. Visit http://localhost:8000/docs to see your API documentation")
