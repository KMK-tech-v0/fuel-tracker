# 🚀 Quick Start Guide - Fuel Control System

## ⚡ Fast Setup (5 minutes)

### 1. **Run Setup Script**
```bash
python setup_project.py
```

### 2. **Configure Database**
Edit `backend/.env` file:
```env
DB_SERVER=your_sql_server_instance
DB_NAME=FuelControlV2
```

### 3. **Setup Database**
```bash
# Run the generated script
setup_database.bat
```

### 4. **Start System**
```bash
# Start both frontend and backend
start_system.bat
```

### 5. **Access Application**
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000

---

## 🔧 Manual Setup

### Prerequisites
- Python 3.8+
- SQL Server (Express or higher)
- ODBC Driver 17 for SQL Server

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
python -m http.server 8080
```

---

## 🐛 Common Issues & Solutions

### ❌ Database Connection Failed
**Problem**: `Database connection failed`
**Solution**: 
1. Check if SQL Server is running
2. Verify server name in `backend/.env`
3. Ensure Windows Authentication is enabled

### ❌ CORS Errors
**Problem**: Frontend can't connect to backend
**Solution**: 
1. Ensure backend is running on port 5000
2. Frontend should be served via HTTP (not file://)

### ❌ Missing Images
**Problem**: Logo images not showing
**Solution**: Images are optional - the system works without them

---

## 📊 System Features

### ✅ Working Features
- **Dashboard** - KPIs and overview
- **Forecasting** - Fuel consumption predictions
- **Stock Management** - Current inventory levels
- **Equipment** - Equipment tracking
- **Operational Hours** - Equipment runtime logging
- **Refills** - Fuel refill transactions
- **Usage** - Fuel usage tracking

### 🚧 Placeholder Features
- Sites management (backend ready)
- Fuel types management (backend ready)
- Suppliers management (backend ready)
- Advanced reports (backend ready)
- Alerts management (backend ready)

---

## 🎯 Next Steps

1. **Customize Database Connection**: Update `backend/.env`
2. **Add Your Data**: Use the web interface or import data
3. **Configure Alerts**: Set up notifications for low stock
4. **Customize UI**: Add your company logo to `frontend/assets/`

---

## 📞 Need Help?

Check the main README.md for detailed documentation and troubleshooting.