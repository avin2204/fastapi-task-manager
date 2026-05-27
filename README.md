## 🌍 Live API

🔗 Swagger Documentation:
https://fastapi-task-manager-lt6l.onrender.com/docs

🔗 Live Backend URL:
https://fastapi-task-manager-lt6l.onrender.com


Project Name - FastAPI Task Manager Backend

A production-style backend project built with FastAPI, PostgreSQL, SQLAlchemy, Async APIs, Docker, and JWT Authentication.

This project focuses on real-world backend architecture, async programming, database migrations, containerization, and scalable API development practices.

* Features 
1. User Registration & Login
2. JWT Authentication & Authorization
3. Secure Password Hashing
4. Async FastAPI Endpoints
5. PostgreSQL Integration
6. SQLAlchemy ORM
7. Alembic Database Migrations
8. Advanced CRUD Operations
9. Pagination, Filtering & Sorting
10 Docker Containerization
11. Docker Compose Multi-Container Setup
12. Environment Variable Configuration
13. RESTful API Architecture
14. Swagger API Documentation

*******************************************************************************************************************************************************************
* Tech Stack
Python
FastAPI
PostgreSQL
SQLAlchemy
AsyncIO
Alembic
JWT Authentication
Docker
Docker Compose
Git & GitHub
******************************************************************************************************************************************************************
📂 Project Structure
app/
├── core/
│   └── security.py
├── models/
│   ├── user_model.py
│   └── task_model.py
├── routers/
│   ├── user_router.py
│   └── task_router.py
├── schemas/
│   ├── user_schema.py
│   └── task_schema.py
├── database.py

alembic/
Dockerfile
docker-compose.yml
requirements.txt
main.py

***************************************************************************************************************************************************************
* API Features
Authentication
User Signup
User Login
JWT Token Generation
Protected Routes
Task Management
Create Tasks
Get Tasks
Update Tasks
Delete Tasks
Pagination
Search
Status Filtering
Latest/Oldest Sorting
Priority Support
Docker Support

*****************************************************************************************************************************************************************
The project is fully containerized using Docker and Docker Compose.

Run with Docker Compose
docker compose up --build
Swagger Documentation

Available at:

http://127.0.0.1:8000/docs
🎯 Learning Outcomes
*******************************************************************************************************************************************************************
This project helped in understanding:

Async vs Sync APIs
Database Relationships
ORM Querying
Authentication Flows
API Design
Docker Networking
Multi-Container Architecture
Environment Management
Database Migrations
Backend Deployment Concepts
🚀 Future Improvements
CI/CD Pipeline
Pytest API Testing
Role-Based Access Control
File Upload System
Background Tasks
Cloud Deployment
