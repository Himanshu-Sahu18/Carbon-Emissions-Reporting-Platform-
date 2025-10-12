# **📊 GHG Carbon Emissions Reporting Platform**

This project is a complete, full-stack web application designed to help organizations track, analyze, and report their carbon footprint based on the internationally recognized Greenhouse Gas (GHG) Protocol.

<img width="1890" height="870" alt="Image" src="https://github.com/user-attachments/assets/74299a97-48a1-4e2f-82b6-f388eb23a399" />
<img width="1788" height="866" alt="Image" src="https://github.com/user-attachments/assets/b62f3726-8cd4-461f-848b-12609d95b82f" />

###Note:- Refer FormDataGuide.md in Docs folder for form filling 

### **1: Start with the "Big Picture"**

_"I built a web platform that helps understand and manage its carbon emissions. The goal is to give them a clear picture of their environmental impact and help them with their sustainability reporting."_

### **2: Main Features (What it Does)**

_"The platform has three main parts:"_

1. **_A Data Entry Form:_** _"A simple form where users can input their operational data, like how much fuel they've used or electricity they've purchased."_
2. **_A Smart Calculation Engine:_** _"This is the core of the application. It takes the data and automatically calculates the carbon emissions in kilograms of CO₂ equivalent (kgCO₂e)."_
3. **_An Interactive Dashboard:_** _"This is where the data comes to life. It has several charts and graphs that visualize the emissions data, making it easy to see trends and insights."_

### **3: Advanced Analytics**

_"What makes this platform powerful isn't just calculating emissions, but providing actionable insights. I implemented three key analytical features:"_

- **_Historical Accuracy (The Most Important Feature):_** _"Emission calculation rules can change every year. My system is smart enough to use the correct emission factor for the correct date. For example, it calculates 2023's emissions using 2023's rules, not the latest ones. This is crucial for accurate and auditable reporting."_
- **_Year-over-Year Comparison:_** _"The dashboard has a chart that compares this year's emissions to last year's, so the company can easily track if their sustainability efforts are working."_
- **_Emission Hotspots:_** _"The platform can instantly identify the biggest sources of pollution within the company—the 'hotspots.' This tells them exactly where to focus their efforts to make the biggest impact on reducing their carbon footprint."_

### **4: Technology Stack**

_"I built this using a modern and professional technology stack:"_

- **_Backend:_** _"I used **Python** with **FastAPI**. It's very fast and reliable, which is perfect for a data-heavy application like this."_
- **_Frontend:_** _"The dashboard was built with **React**, which is the industry standard for creating interactive and user-friendly interfaces."_
- **_Database:_** _"I used **PostgreSQL** because it's a powerful and robust database that can handle the complex queries needed for the analytics."_
- **_Deployment:_** _"The entire application is packaged with **Docker**. This means it's self-contained and can be run on any machine with a single command, which makes it very easy to set up."_

## **🏛️ System Architecture**

The application uses a standard 3-Tier Architecture, which separates concerns and makes the system scalable and easy to maintain.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                 │
│                      (http://localhost:80)                           │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ HTTP/HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION TIER                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │         React Frontend + Nginx (Port 80)                      │  │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────┐ │  │
│  │  │  Data Entry     │  │   Dashboard      │  │   Charts &  │ │  │
│  │  │  Forms          │  │   Components     │  │   Graphs    │ │  │
│  │  └─────────────────┘  └──────────────────┘  └─────────────┘ │  │
│  │                                                               │  │
│  │  Technologies: React, TypeScript, Recharts, TailwindCSS      │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ REST API Calls
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      LOGIC TIER                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │            FastAPI Backend (Port 8000)                        │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │              REST API Endpoints                         │ │  │
│  │  │  • POST /emissions/calculate                            │ │  │
│  │  │  • GET  /analytics/yoy                                  │ │  │
│  │  │  • GET  /analytics/intensity                            │ │  │
│  │  │  • GET  /analytics/hotspots                             │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │           Business Logic Layer                          │ │  │
│  │  │  • Historical Accuracy Engine                           │ │  │
│  │  │  • Emission Calculation Service                         │ │  │
│  │  │  • Analytics Service                                    │ │  │
│  │  │  • Data Validation                                      │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │           Repository Layer                              │ │  │
│  │  │  • Emission Repository                                  │ │  │
│  │  │  • Emission Factor Repository                           │ │  │
│  │  │  • Business Metrics Repository                          │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  │                                                               │  │
│  │  Technologies: Python, FastAPI, SQLAlchemy, Pydantic         │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ SQL Queries
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA TIER                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │           PostgreSQL Database (Port 5432)                     │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │                  Database Schema                        │ │  │
│  │  │                                                         │ │  │
│  │  │  ┌──────────────────┐    ┌──────────────────┐         │ │  │
│  │  │  │   emissions      │    │ emission_factors │         │ │  │
│  │  │  │  • id            │    │  • id            │         │ │  │
│  │  │  │  • scope         │    │  • scope         │         │ │  │
│  │  │  │  • category      │    │  • category      │         │ │  │
│  │  │  │  • activity_data │    │  • factor_value  │         │ │  │
│  │  │  │  • activity_date │◄───┤  • valid_from    │         │ │  │
│  │  │  │  • emissions_kg  │    │  • valid_to      │         │ │  │
│  │  │  └──────────────────┘    └──────────────────┘         │ │  │
│  │  │                                                         │ │  │
│  │  │  ┌──────────────────┐                                  │ │  │
│  │  │  │ business_metrics │                                  │ │  │
│  │  │  │  • id            │                                  │ │  │
│  │  │  │  • metric_name   │                                  │ │  │
│  │  │  │  • metric_value  │                                  │ │  │
│  │  │  │  • metric_date   │                                  │ │  │
│  │  │  └──────────────────┘                                  │ │  │
│  │  │                                                         │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  │                                                               │  │
│  │  Technologies: PostgreSQL 15                                  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────────┐
                    │   Docker Compose         │
                    │   Orchestration Layer    │
                    │                          │
                    │  • frontend container    │
                    │  • backend container     │
                    │  • postgres container    │
                    └──────────────────────────┘
```

### **Architecture Overview**

1. **Frontend (Presentation Tier):** A React-based single-page application that provides the user interface, including the data entry forms and the visualization dashboard.
2. **Backend (Logic Tier):** A FastAPI server that exposes a REST API. It contains all the business logic, including the historical accuracy engine and the advanced analytics endpoints.
3. **Database (Data Tier):** A PostgreSQL database that stores all the data, including versioned emission factors, emission records, and business metrics.

### **Data Flow**

1. User interacts with React frontend (forms, dashboard)
2. Frontend sends HTTP requests to FastAPI backend
3. Backend processes requests through business logic layer
4. Repository layer executes SQL queries against PostgreSQL
5. Results flow back through the layers to the user interface
6. Charts and visualizations render the data for analysis

## **🗄️ Database Schema & Architecture**

The PostgreSQL database is the foundation of the platform, designed with enterprise-grade features for data integrity, auditability, and performance.

### **Core Tables**

#### **1. emission_factors (Master Data)**

The heart of the calculation engine - stores versioned emission factors.

**Key Columns:**

- `factor_id`: Primary key
- `activity_name`: Type of activity (e.g., 'Diesel', 'Grid Electricity')
- `scope`: GHG Protocol scope (1=Direct, 2=Indirect Energy, 3=Value Chain)
- `activity_unit`: Unit of measurement (litres, kWh, tonnes, m³)
- `co2e_per_unit`: The emission factor value (kgCO₂e per unit)
- `source`: Data source reference (e.g., 'EPA 2024', 'IPCC 2006')
- `valid_from` / `valid_to`: Temporal validity period for historical accuracy

**Features:**

- Temporal versioning: Multiple versions of the same factor for different time periods
- Automatic factor selection based on activity date
- Constraints ensure data integrity (positive values, valid date ranges)
- Optimized indexes for fast lookups by activity, scope, and date range

#### **2. emission_records (Transactional Data)**

Stores every emission calculation with full traceability.

**Key Columns:**

- `record_id`: Primary key
- `activity_date`: When the activity occurred
- `activity_name` / `scope`: Links to emission factor
- `activity_value` / `activity_unit`: User-provided measurement
- `factor_id`: Foreign key to the exact factor version used
- `calculated_co2e`: System-calculated emissions
- `is_overridden`: Flag for manual adjustments
- `overridden_co2e` / `override_reason`: Manual override details
- `location` / `department`: Optional organizational context

**Features:**

- Complete audit trail: Every calculation is traceable to its source factor
- Override mechanism: Allows manual adjustments with justification
- Multi-dimensional analysis: Supports filtering by date, scope, location, department
- Performance indexes for fast analytics queries

#### **3. business_metrics**

Stores operational metrics for emission intensity calculations.

**Key Columns:**

- `metric_id`: Primary key
- `metric_name`: Name of the metric (e.g., 'Tons of Steel Produced')
- `metric_category`: Classification (Production, Financial, Operational)
- `value` / `unit`: Metric measurement
- `metric_date`: Date the metric applies to
- `reporting_period`: Frequency (Monthly, Quarterly, Annual)

**Features:**

- Enables intensity calculations (e.g., kgCO₂e per ton of product)
- Supports multiple metric types for comprehensive analysis
- Temporal tracking for trend analysis

#### **4. audit_log**

Comprehensive audit trail for all data modifications.

**Key Columns:**

- `log_id`: Primary key
- `record_id`: Reference to modified emission record
- `action_type`: Type of change (OVERRIDE, UPDATE, DELETE)
- `original_value` / `new_value`: Before and after values
- `reason`: Required justification for the change
- `changed_by` / `changed_at`: User and timestamp
- `ip_address` / `user_agent`: Optional security tracking

**Features:**

- Automatic logging via database triggers
- Complete change history for compliance and auditing
- Security tracking capabilities

#### **5. emission_categories (Optional Enhancement)**

Hierarchical categorization of emission activities.

**Features:**

- Parent-child relationships for nested categories
- Scope-based organization
- Enhanced reporting and filtering

#### **6. reporting_periods (Optional Enhancement)**

Standardized reporting periods for consistent analytics.

**Features:**

- Predefined periods (Q1 2024, FY 2023-2024)
- Period locking mechanism for finalized reports
- Consistent date range definitions

### **Database Views**

Pre-computed views for optimized analytics:

- **v_active_emission_factors**: Currently valid emission factors only
- **v_effective_emissions**: Emission records with overrides applied
- **v_monthly_emissions_by_scope**: Monthly aggregation by GHG scope
- **v_emission_hotspots**: Top emission sources ranked by total CO₂e

### **Database Functions**

Reusable SQL functions for common operations:

- **get_emission_factor()**: Retrieves the correct factor for a given date and activity
- **calculate_emission_intensity()**: Computes intensity metrics for a date range

### **Database Triggers**

Automated data integrity and audit mechanisms:

- **update_updated_at_column()**: Automatically updates timestamps on modifications
- **log_emission_override()**: Automatically logs all manual overrides to audit_log

### **Key Database Features**

1. **Historical Accuracy Engine:**

   - Temporal versioning with `valid_from` and `valid_to` dates
   - Automatic selection of the correct factor based on activity date
   - Ensures compliance with evolving emission standards

2. **Data Integrity:**

   - CHECK constraints for positive values and valid date ranges
   - UNIQUE constraints prevent duplicate factors
   - Foreign key relationships ensure referential integrity
   - Trigger-based validation and automation

3. **Performance Optimization:**

   - Strategic indexes on frequently queried columns
   - Partial indexes for active factors and overridden records
   - Composite indexes for multi-column queries
   - Pre-computed views for common analytics

4. **Audit & Compliance:**

   - Complete change history in audit_log
   - Automatic trigger-based logging
   - User tracking for all modifications
   - Justification requirements for overrides

5. **Scalability:**
   - Normalized schema design
   - Efficient indexing strategy
   - View-based abstraction for complex queries
   - Function-based reusable logic

## **✨ Core Features & Technical Details**

- **Historically Accurate Calculation Engine:**
  - The emission_factors table is versioned with valid_from and valid_to dates.
  - The calculation logic queries for the factor that was valid on the specific activity_date of the emission, ensuring every record is compliant and auditable.
  - Database function `get_emission_factor()` automatically selects the correct factor version.
- **Advanced Analytics APIs:**
  - **YoY Emissions API (/analytics/yoy):** Aggregates total emissions by scope for the current and previous years.
  - **Emission Intensity API (/analytics/intensity):** Calculates a key performance indicator (e.g., kgCO₂e per Ton of Product) by combining emissions data with business metrics.
  - **Emission Hotspot API (/analytics/hotspots):** Groups emissions by their source and calculates the percentage contribution of each, identifying the largest polluters.
- **Data Management:**
  - The database is initialized with sample data for demonstration.
  - Includes versioned emission factors for Diesel, Natural Gas, Grid Electricity, Petrol, LPG, and Coal.
  - Sample business metrics for production and operational tracking.
  - The project is designed to import real-world data from the provided GHG Sheet.xlsx CSV files via a data import script.
- **Audit & Compliance:**
  - Complete audit trail via the audit_log table.
  - Automatic logging of all manual overrides through database triggers.
  - User tracking and justification requirements for data modifications.
- **Containerized Deployment:**
  - The entire stack (frontend, backend, database) is defined in a docker-compose.yml file.
  - This allows for a consistent development environment and one-command setup.

## **🚀 How to Run the Project**

### **Option 1: Run with Docker (Recommended)**

This is the easiest way to run the entire application with a single command.

#### **Prerequisites**

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Ensure Docker is running on your machine

#### **Steps**

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ghg-emissions-platform
   ```

2. **Start all services with Docker Compose:**

   ```bash
   docker-compose up -d --build
   ```

   This command will:

   - Build the frontend, backend, and database containers
   - Start all services in detached mode
   - Initialize the database with sample data
   - Set up networking between containers

3. **Verify containers are running:**

   ```bash
   docker-compose ps
   ```

   You should see three containers running:

   - `ghg-frontend` (React app)
   - `ghg-backend` (FastAPI server)
   - `ghg-postgres` (PostgreSQL database)

4. **Access the application:**

   - **Frontend Dashboard:** http://localhost (port 80)
   - **Backend API Docs:** http://localhost:8000/docs
   - **Backend API:** http://localhost:8000

   > **Note:** The frontend runs on port 80 in Docker (via nginx), not port 5173. Port 5173 is only used during local development with `npm run dev`.

5. **View logs (if needed):**

   ```bash
   # View all logs
   docker-compose logs -f

   # View specific service logs
   docker-compose logs -f backend
   docker-compose logs -f frontend
   docker-compose logs -f postgres
   ```

6. **Stop the application:**

   ```bash
   docker-compose down
   ```

   To stop and remove all data (including database):

   ```bash
   docker-compose down -v
   ```

---

### **Option 2: Run Services Individually (Development)**

For development purposes, you may want to run services separately.

#### **Prerequisites**

- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL 15+

#### **1. Setup and Run PostgreSQL Database**

**Using Docker:**

```bash
docker run -d \
  --name ghg-postgres \
  -e POSTGRES_USER=ghg_user \
  -e POSTGRES_PASSWORD=ghg_password \
  -e POSTGRES_DB=ghg_emissions \
  -p 5432:5432 \
  postgres:15
```

**Or install PostgreSQL locally** and create a database:

```sql
CREATE DATABASE ghg_emissions;
CREATE USER ghg_user WITH PASSWORD 'ghg_password';
GRANT ALL PRIVILEGES ON DATABASE ghg_emissions TO ghg_user;
```

#### **2. Setup and Run Backend (FastAPI)**

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv

   # Activate on Windows
   venv\Scripts\activate

   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**

   Create a `.env` file in the backend directory:

   ```env
   DATABASE_URL=postgresql://ghg_user:ghg_password@localhost:5432/ghg_emissions
   ```

5. **Initialize the database:**

   ```bash
   python init_db.py
   ```

6. **Run the backend server:**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at:

   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs

#### **3. Setup and Run Frontend (React)**

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Set environment variables:**

   Create a `.env` file in the frontend directory:

   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Run the development server:**

   ```bash
   npm run dev
   ```

   The application will open automatically at http://localhost:5173

   > **Note:** Vite (the build tool) uses port 5173 by default for development

5. **Build for production (optional):**
   ```bash
   npm run build
   ```

---

### **🔧 Useful Docker Commands**

```bash
# Rebuild containers after code changes
docker-compose up -d --build

# Restart a specific service
docker-compose restart backend

# Execute commands inside a container
docker-compose exec backend bash
docker-compose exec postgres psql -U ghg_user -d ghg_emissions

# View container resource usage
docker stats

# Remove all containers and volumes (fresh start)
docker-compose down -v
docker-compose up -d --build
```

---

### **🧪 Testing the Application**

1. **Test Backend API:**

   - Visit http://localhost:8000/docs
   - Try the `/emissions/calculate` endpoint with sample data
   - Check analytics endpoints: `/analytics/yoy`, `/analytics/intensity`, `/analytics/hotspots`

2. **Test Frontend:**
   - **Docker:** Open http://localhost (port 80)
   - **Local Dev:** Open http://localhost:5173
   - Fill out the emission entry form
   - View the dashboard and charts
   - Verify data is being saved and displayed correctly

---

- ✅ **Correct:** http://localhost (port 80)
- ❌ **Wrong:** http://localhost:5173 (only for local dev)
- ❌ **Wrong:** http://localhost:3000 (not used in this project)

## Project Structure (Simple View)

```
📁 This Folder
├── 🌐 frontend/          → Dashboard (what you see in browser)
├── ⚙️ backend/           → API (does calculations)
├── 🗄️ init.sql           → Database setup
├── 🐳 docker-compose.yml → Runs everything
└── 📖 START_HERE.md      → This file
```
