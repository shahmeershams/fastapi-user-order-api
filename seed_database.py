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
            print("Starting database seeding...")
            
            # Seed roles (without hard-coded IDs)
            roles_result = db.execute(text("SELECT COUNT(*) FROM roles")).scalar()
            if roles_result == 0:
                print("Seeding roles...")
                db.execute(text("""
                    INSERT INTO roles (name, `key`, description) VALUES
                    ('Administrator', 'admin', 'Full system access with all permissions'),
                    ('Customer', 'customer', 'Limited access for customer operations')
                """))
                print("Roles seeded successfully.")
            else:
                print("Roles already exist, skipping...")
            
            # Seed permissions (without hard-coded IDs)
            permissions_result = db.execute(text("SELECT COUNT(*) FROM permissions")).scalar()
            if permissions_result == 0:
                print("Seeding permissions...")
                permissions_data = [
                    # User Management Permissions
                    ('Create User', 'user:create', 'Create new users in the system'),
                    ('Read User', 'user:read', 'View user information'),
                    ('Update User', 'user:update', 'Update user information'),
                    ('Delete User', 'user:delete', 'Delete users from the system'),
                    ('List Users', 'user:list', 'List all users in the system'),
                    ('Read Own Profile', 'user:read_own', 'View own user profile'),
                    ('Update Own Profile', 'user:update_own', 'Update own user profile'),
                    ('Delete Own Account', 'user:delete_own', 'Delete own user account'),
                    
                    # Order Management Permissions
                    ('Create Order', 'order:create', 'Create new orders'),
                    ('Read Order', 'order:read', 'View order information'),
                    ('Update Order', 'order:update', 'Update order information'),
                    ('Delete Order', 'order:delete', 'Delete orders'),
                    ('List Orders', 'order:list', 'List all orders in the system'),
                    ('Read Own Orders', 'order:read_own', 'View own orders'),
                    ('Update Own Orders', 'order:update_own', 'Update own orders'),
                    ('Delete Own Orders', 'order:delete_own', 'Delete own orders'),
                    ('Update Order Status', 'order:update_status', 'Update order status'),
                    
                    # Role Management Permissions
                    ('Create Role', 'role:create', 'Create new roles'),
                    ('Read Role', 'role:read', 'View role information'),
                    ('Update Role', 'role:update', 'Update role information'),
                    ('Delete Role', 'role:delete', 'Delete roles'),
                    ('List Roles', 'role:list', 'List all roles in the system'),
                    ('Read Role Permissions', 'role:read_permissions', 'View permissions assigned to roles'),
                    
                    # Permission Management Permissions
                    ('Create Permission', 'permission:create', 'Create new permissions'),
                    ('Read Permission', 'permission:read', 'View permission information'),
                    ('Update Permission', 'permission:update', 'Update permission information'),
                    ('Delete Permission', 'permission:delete', 'Delete permissions'),
                    ('List Permissions', 'permission:list', 'List all permissions in the system'),
                    
                    # Role-Permission Assignment Permissions
                    ('Assign Permission to Role', 'role_permission:assign', 'Assign permissions to roles'),
                    ('Remove Permission from Role', 'role_permission:remove', 'Remove permissions from roles'),
                ]
                
                # Insert permissions without hard-coded IDs
                for name, key, description in permissions_data:
                    db.execute(text("""
                        INSERT INTO permissions (name, `key`, description) 
                        VALUES (:name, :key, :description)
                    """), {"name": name, "key": key, "description": description})
                
                print("Permissions seeded successfully.")
            else:
                print("Permissions already exist, skipping...")
            
            # Seed role-permission assignments using key lookups
            role_permissions_result = db.execute(text("SELECT COUNT(*) FROM role_permissions")).scalar()
            if role_permissions_result == 0:
                print("Assigning permissions to roles...")
                
                # Get role IDs using keys
                admin_role = db.execute(text("SELECT role_id FROM roles WHERE `key` = 'admin'")).scalar()
                customer_role = db.execute(text("SELECT role_id FROM roles WHERE `key` = 'customer'")).scalar()
                
                if admin_role and customer_role:
                    # Admin gets ALL permissions
                    admin_permission_keys = [
                        'user:create', 'user:read', 'user:update', 'user:delete', 'user:list',
                        'user:read_own', 'user:update_own', 'user:delete_own',
                        'order:create', 'order:read', 'order:update', 'order:delete', 'order:list',
                        'order:read_own', 'order:update_own', 'order:delete_own', 'order:update_status',
                        'role:create', 'role:read', 'role:update', 'role:delete', 'role:list', 'role:read_permissions',
                        'permission:create', 'permission:read', 'permission:update', 'permission:delete', 'permission:list',
                        'role_permission:assign', 'role_permission:remove'
                    ]
                    
                    # Customer gets LIMITED permissions
                    customer_permission_keys = [
                        'user:read_own', 'user:update_own', 'user:delete_own',
                        'order:create', 'order:read_own', 'order:update_own', 'order:delete_own',
                        'role:read', 'role:list',
                        'permission:read', 'permission:list'
                    ]
                    
                    # Assign permissions to admin role using key lookups
                    for permission_key in admin_permission_keys:
                        permission_id = db.execute(text(
                            "SELECT permission_id FROM permissions WHERE `key` = :key"
                        ), {"key": permission_key}).scalar()
                        
                        if permission_id:
                            db.execute(text("""
                                INSERT INTO role_permissions (role_id, permission_id) 
                                VALUES (:role_id, :permission_id)
                            """), {"role_id": admin_role, "permission_id": permission_id})
                    
                    # Assign permissions to customer role using key lookups
                    for permission_key in customer_permission_keys:
                        permission_id = db.execute(text(
                            "SELECT permission_id FROM permissions WHERE `key` = :key"
                        ), {"key": permission_key}).scalar()
                        
                        if permission_id:
                            db.execute(text("""
                                INSERT INTO role_permissions (role_id, permission_id) 
                                VALUES (:role_id, :permission_id)
                            """), {"role_id": customer_role, "permission_id": permission_id})
                    
                    print("Role-permission assignments completed successfully.")
                else:
                    print("ERROR: Could not find admin or customer roles for permission assignment.")
            else:
                print("Role-permission assignments already exist, skipping...")
            
            db.commit()
            print("Database seeding completed successfully.")
            
        except Exception as e:
            print(f"Error seeding database: {e}")
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
                print("Creating default admin user...")
                
                # Get admin role ID using key lookup
                admin_role_id = db.execute(text("SELECT role_id FROM roles WHERE `key` = 'admin'")).scalar()
                if not admin_role_id:
                    print("ERROR: Admin role not found. Please run seeding first.")
                    return
                
                # Hash the password "admin123"
                from passlib.context import CryptContext
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                hashed_password = pwd_context.hash("admin123")
                
                db.execute(text("""
                    INSERT INTO users (username, email, hashed_password, role_id) VALUES
                    ('admin', 'admin@example.com', :hashed_password, :role_id)
                """), {"hashed_password": hashed_password, "role_id": admin_role_id})
                
                db.commit()
                print("Default admin user created successfully.")
                print("Email: admin@example.com")
                print("Password: admin123")
            else:
                print("Admin user already exists, skipping...")
                
        except Exception as e:
            print(f"Error creating admin user: {e}")
            db.rollback()

if __name__ == "__main__":
    print("Database Seeding Script")
    print("=" * 50)
    
    # Check if database is accessible
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful.")
    except Exception as e:
        print(f"Cannot connect to database: {e}")
        print("Make sure your database is running and accessible.")
        sys.exit(1)
    
    # Run seeding
    seed_database()
    
    # Ask if user wants to create admin user
    create_admin = input("\nDo you want to create a default admin user? (y/n): ").lower().strip()
    if create_admin in ['y', 'yes']:
        create_admin_user()
    
    print("\nNext steps:")
    print("1. Run 'alembic upgrade head' to apply all migrations")
    print("2. Start your API server with 'uvicorn main:app --reload'")
    print("3. Visit http://localhost:8000/docs to see your API documentation")
