# Developer Productivity MVP

![Project Status](https://img.shields.io/badge/Status-MVP-blue)
![Backend](https://img.shields.io/badge/Backend-Django%20REST-success)
![Frontend](https://img.shields.io/badge/Frontend-React-informational)

## 📖 About the Project
The **Developer Productivity MVP** is a full-stack web application designed to track, analyze, and visualize developer performance and productivity metrics. It bridges the gap between individual performance tracking and team-level management by providing tailored dashboard views for both Individual Contributors (ICs) and Managers[cite: 1]. 

The system is built to not just show raw data, but to provide context through interpretation panels, evidence tracking, and actionable next steps[cite: 1].

### ✨ Key Features
* **Role-Based Dashboards**: Dedicated interfaces for Individual Contributors (`IcView.jsx`) and Managers (`ManagerView.jsx`)[cite: 1].
* **Detailed Metrics Visualization**: Clean, grid-based metric cards displaying key productivity indicators (`MetricsGrid.jsx`, `MetricCard.jsx`)[cite: 1].
* **Contextual Insights**: Deep-dive components like the `EvidencePanel` and `InterpretationPanel` to give meaning to the raw metrics[cite: 1].
* **Actionable Outcomes**: A `NextStepsPanel` to guide developers and managers on improvements[cite: 1].
* **Managerial Summaries**: High-level aggregated data views for team leadership (`ManagerSummaryTable.jsx`)[cite: 1].

---

## 🏗️ Architecture & Tech Stack

The project utilizes a decoupled architecture with a modern JavaScript frontend and a robust Python backend[cite: 1]. 

### Frontend (`/frontend`)
* **Framework:** React.js (using JSX)[cite: 1]
* **Styling:** CSS (`App.css`)[cite: 1]
* **Package Manager:** npm (`package.json`, `package-lock.json`)[cite: 1]
* **API Communication:** Custom client module (`api/client.js`)[cite: 1]

### Backend (`/backend`)
* **Framework:** Django & Django REST Framework (DRF)[cite: 1]
* **App Structure:** Contains an `insights` app with isolated `models.py`, `views.py`, `serializers.py`, and a dedicated `services.py` for business logic separation[cite: 1].
* **Database:** SQLite (`db.sqlite3`) for the MVP phase[cite: 1].
* **Deployment Ready:** Includes a `Procfile` and `build.sh` script for seamless deployment to platforms like Heroku or Render[cite: 1].

---

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites
* Python 3.8+
* Node.js & npm
* Git

### Backend Setup

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. (Optional) Load sample data if available:
   ```bash
   # You can create a custom management command or use shell to load insights/data/sample_data.json
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   # OR npm start (depending on your package.json scripts)
   ```

---

## 📂 Project Structure

```text
Developer-Productivity-MVP/
├── backend/                  # Django REST API
│   ├── config/               # Project settings & routing
│   ├── insights/             # Core application app (Models, Views, Serializers, Services)
│   │   └── data/             # Contains sample_data.json
│   ├── requirements.txt      # Python dependencies
│   ├── db.sqlite3            # Local database
│   ├── build.sh              # Build script
│   └── Procfile              # Server configuration
│
└── frontend/                 # React UI
    ├── package.json          # Node dependencies
    └── src/
        ├── api/              # API client for backend communication
        ├── components/       # Reusable UI elements (Metrics, Panels, Tables)
        ├── views/            # High-level page layouts (IC & Manager views)
        ├── App.jsx           # Root React component
        └── main.jsx          # React DOM rendering entry point
```

```
