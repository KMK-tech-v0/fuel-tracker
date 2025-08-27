# Advanced Fuel Control & Forecasting System v2.0

A modern, comprehensive fuel management system with advanced consumption forecasting capabilities, built with Flask backend and vanilla JavaScript frontend.

## 🚀 Key Features

### Core Functionality
- **Real-time Stock Management** - Monitor fuel levels across multiple sites
- **Equipment-based Consumption Tracking** - Track fuel usage by individual equipment
- **Advanced Forecasting Engine** - Predict fuel needs with configurable safety factors
- **Operational Hours Logging** - Record equipment runtime for accurate consumption calculations
- **Multi-location Support** - Manage sites, warehouses, and distribution centers
- **Proactive Alerts** - Early warning system for low stock and projected shortages

### Advanced Features
- **Scenario Planning** - "What-if" analysis for consumption forecasting
- **Anomaly Detection** - Identify unusual consumption patterns
- **Purchase Planning Tools** - Optimal timing and quantity recommendations
- **Equipment Efficiency Tracking** - Monitor and analyze equipment performance
- **Comprehensive Reporting** - Detailed analytics and insights
- **Modern UI/UX** - Clean, responsive interface with professional design

## 🏗️ Architecture

### Backend (Flask)
- **Database**: SQL Server with Windows Authentication
- **API**: RESTful endpoints with comprehensive error handling
- **Forecasting Engine**: Stored procedures for complex calculations
- **Real-time Updates**: Automatic stock and forecast recalculation

### Frontend (Vanilla JavaScript)
- **Modern UI**: Clean, professional interface with Chart.js integration
- **Responsive Design**: Optimized for desktop use
- **Real-time Updates**: Auto-refresh capabilities
- **Progressive Enhancement**: Graceful degradation for missing features

### Database Schema
- **Enhanced Tables**: 15+ tables with comprehensive relationships
- **Forecasting Tables**: Equipment, operational hours, consumption forecasts
- **Alert System**: Configurable alerts with history tracking
- **Audit Trail**: Complete system activity logging

## 📋 Prerequisites

- **SQL Server** (Express or higher) with Windows Authentication
- **Python 3.8+** with pip
- **Modern Web Browser** (Chrome, Firefox, Edge)
- **ODBC Driver 17 for SQL Server**

## 🛠️ Installation

### 1. Database Setup
```bash
# Navigate to database folder
cd database

# Run database creation script in SQL Server Management Studio or sqlcmd
sqlcmd -S "YOUR_SERVER_NAME" -E -i "create_database.sql"
sqlcmd -S "YOUR_SERVER_NAME" -E -i "insert_sample_data.sql"
sqlcmd -S "YOUR_SERVER_NAME" -E -i "forecasting_procedures.sql"
```

### 2. Backend Setup
```bash
# Navigate to backend folder
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Update database connection in config.py if needed
# Default: DESKTOP-17P73P0\SQLEXPRESS

# Run the application
python app.py
```

### 3. Frontend Setup
```bash
# Navigate to frontend folder
cd frontend

# Add your logo images to assets/ folder:
# - logo.png (header logo)
# - footer-logo.gif (footer logo/animation)

# Open index.html in a web browser or serve via HTTP server
# For development, you can use Python's built-in server:
python -m http.server 8080
```

## 🎯 Usage

### Dashboard
- View key performance indicators (KPIs)
- Monitor stock levels across all sites
- Check recent forecasts and critical alerts
- Visual charts and analytics

### Fuel Forecasting
- Calculate consumption forecasts for all sites
- View days remaining and recommended refill dates
- Create scenario planning for different consumption rates
- Adjust safety factors for risk management

### Operational Hours Logging
- Log equipment running hours daily
- Automatic consumption calculation based on equipment rates
- Track fuel efficiency and equipment performance
- Generate maintenance alerts

### Stock Management
- Real-time stock level monitoring
- Automatic reorder point alerts
- Fill percentage visualization
- Stock status tracking (Normal/Low/Critical/High)

### Equipment Management
- Register equipment with consumption rates
- Track equipment by site and fuel type
- Monitor equipment efficiency
- Maintenance scheduling

## 🔧 Configuration

### Database Connection
Update `backend/config.py`:
```python
DB_SERVER = 'YOUR_SQL_SERVER_INSTANCE'
DB_NAME = 'FuelControlV2'
```

### System Settings
Modify settings via database or API:
- Default safety factor for forecasting
- Alert thresholds and notification settings
- Calculation frequencies
- Email notification configuration

## 📊 API Endpoints

### Core Endpoints
- `GET /api/health` - System health check
- `GET /api/sites` - Get all sites
- `GET /api/equipment` - Get equipment list
- `GET /api/stock` - Get current stock levels

### Forecasting Endpoints
- `GET /api/forecasts` - Get consumption forecasts
- `POST /api/forecasts/calculate` - Calculate new forecasts
- `POST /api/forecasts/scenarios` - Create forecast scenarios

### Operational Endpoints
- `GET /api/operational-hours` - Get operational hours log
- `POST /api/operational-hours` - Log equipment hours
- `GET /api/alerts` - Get system alerts

## 🚨 Alerts & Notifications

### Alert Types
- **Low Stock Alerts** - When fuel levels drop below thresholds
- **Forecast Shortage Alerts** - When projected shortage is detected
- **Equipment Efficiency Alerts** - When consumption deviates from expected
- **Maintenance Due Alerts** - When equipment maintenance is required

### Configuration
Alerts can be configured per site, fuel type, or equipment with:
- Custom threshold values
- Notification email lists
- Severity levels (Low/Medium/High/Critical)
- Automatic acknowledgment settings

## 📈 Reporting Features

### Available Reports
- **Consumption Summary** - Fuel usage by site and time period
- **Equipment Efficiency** - Performance analysis by equipment
- **Forecast Accuracy** - Historical forecast vs actual consumption
- **Stock Movement** - Refill and usage transaction history
- **Cost Analysis** - Fuel costs and supplier performance

## 🔒 Security Features

- **Windows Authentication** - Integrated with domain security
- **Audit Logging** - Complete activity tracking
- **Input Validation** - SQL injection prevention
- **Error Handling** - Secure error messages
- **Session Management** - Secure user sessions

## 🎨 Customization

### UI Themes
The system uses CSS custom properties for easy theming:
- Primary colors
- Accent colors
- Typography settings
- Spacing and layout

### Logo Integration
- Add `logo.png` to `frontend/assets/` for header logo
- Add `footer-logo.gif` to `frontend/assets/` for footer animation
- System gracefully handles missing images

## 🐛 Troubleshooting

### Common Issues
1. **Database Connection Failed**
   - Verify SQL Server is running
   - Check Windows Authentication permissions
   - Confirm server name in config.py

2. **API Errors**
   - Check Flask server is running on port 5000
   - Verify CORS settings for frontend domain
   - Check browser console for detailed errors

3. **Forecasting Issues**
   - Ensure operational hours are logged regularly
   - Verify equipment consumption rates are set
   - Check system settings for safety factors

## 📝 License

This project is proprietary software. All rights reserved.

## 🤝 Support

For technical support or feature requests, please contact the development team.

---

**Advanced Fuel Control & Forecasting System v2.0**  
*Transforming fuel management from reactive to proactive*
