# PanchayatGuard

**Transparent Panchayat. Stronger Bharat.**
A production-quality government-tech procurement intelligence platform designed to monitor procurement activities, detect anomalies, and ensure transparent governance across Gram Panchayats.

## 🏛️ Architecture

PanchayatGuard is built as a modern, full-stack web application:
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Recharts (Data Visualization), Leaflet (Mapping)
- **Backend**: FastAPI (Python), SQLAlchemy 2.0 (ORM)
- **Database**: PostgreSQL (Production) / SQLite (Local Development Fallback)
- **Authentication**: JWT, bcrypt password hashing, Role-Based Access Control (RBAC)
- **Intelligence Engine**: Deterministic rule-based risk evaluation pipeline analyzing vendor concentration, price anomalies, and transaction splitting.

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- PostgreSQL (Optional for local, required for production)

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Setup environment variables (copy `.env.example` to `.env`).
5. Run the server (auto-initializes SQLite if PostgreSQL isn't provided):
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## 🧪 Testing
Run end-to-end local testing using the following command inside the `backend` directory:
```bash
pytest
```
For the frontend, you can verify TypeScript constraints:
```bash
npm run build
```

## 🌍 Environment & Deployment
A `docker-compose.yml` file is provided for immediate production deployment. It spins up:
1. `db`: PostgreSQL 15 Database
2. `backend`: FastAPI Python server
3. `frontend`: Nginx serving the React build

**To deploy using Docker:**
```bash
docker-compose up --build -d
```

## 👥 Demo Accounts
Upon initial boot, the database is seeded with a demo administrator account:
- **Email**: admin@panchayatguard.gov.in
- **Password**: SecurePassword123!

## 📜 API Documentation
FastAPI automatically generates interactive OpenAPI documentation. Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛡️ Security Audit
- **JWT Authentication**: Implemented securely with environment-driven secrets.
- **SQL Injection**: Prevented globally by SQLAlchemy ORM parameterized queries.
- **CORS**: Strictly defined within `main.py`.
- **Sensitive Data**: Passwords hashed via `passlib[bcrypt]`.
