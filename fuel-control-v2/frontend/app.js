/**
 * Advanced Fuel Control & Forecasting System - Frontend JavaScript
 * Version 2.0 with Enhanced Forecasting Capabilities
 */

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api',
    REFRESH_INTERVAL: 30000, // 30 seconds
    CHART_COLORS: {
        primary: '#2563eb',
        secondary: '#64748b',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        critical: '#dc2626'
    }
};

// Global state
let currentSection = 'dashboard';
let globalData = {
    sites: [],
    fuelTypes: [],
    equipment: [],
    stock: [],
    forecasts: [],
    alerts: []
};

// Chart instances
let stockChart = null;

// Utility Functions
class Utils {
    static formatNumber(num, decimals = 2) {
        if (num === null || num === undefined) return '0';
        return parseFloat(num).toLocaleString('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }

    static formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    static formatDateTime(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    static getStatusClass(status) {
        const statusMap = {
            'Normal': 'status-normal',
            'Low': 'status-low',
            'Critical': 'status-critical',
            'High': 'status-high'
        };
        return statusMap[status] || 'status-normal';
    }

    static showLoading(show = true) {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            spinner.classList.toggle('active', show);
        }
    }

    static showNotification(message, type = 'info') {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 4000;
            animation: slideIn 0.3s ease-out;
        `;
        
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#2563eb'
        };
        
        notification.style.backgroundColor = colors[type] || colors.info;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// API Service
class ApiService {
    static async request(endpoint, options = {}) {
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            Utils.showNotification(`API Error: ${error.message}`, 'error');
            throw error;
        }
    }

    static async get(endpoint) {
        return this.request(endpoint);
    }

    static async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
}

// Navigation System
class Navigation {
    static init() {
        // Add click handlers to navigation items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.getAttribute('data-section');
                this.showSection(section);
            });
        });

        // Show initial section
        this.showSection('dashboard');
    }

    static showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        const activeNavItem = document.querySelector(`[data-section="${sectionName}"]`);
        if (activeNavItem) {
            activeNavItem.classList.add('active');
        }

        currentSection = sectionName;

        // Load section data
        this.loadSectionData(sectionName);
    }

    static async loadSectionData(sectionName) {
        try {
            switch (sectionName) {
                case 'dashboard':
                    await Dashboard.load();
                    break;
                case 'forecasting':
                    await Forecasting.load();
                    break;
                case 'stock':
                    await Stock.load();
                    break;
                case 'equipment':
                    await Equipment.load();
                    break;
                case 'operational-hours':
                    await OperationalHours.load();
                    break;
                case 'refills':
                    await Refills.load();
                    break;
                case 'usage':
                    await Usage.load();
                    break;
                // Add other sections as needed
            }
        } catch (error) {
            console.error(`Error loading section ${sectionName}:`, error);
        }
    }
}

// Dashboard Module
class Dashboard {
    static async load() {
        Utils.showLoading(true);
        
        try {
            // Load all necessary data
            await Promise.all([
                this.loadKPIs(),
                this.loadStockChart(),
                this.loadRecentForecasts()
            ]);
        } catch (error) {
            console.error('Dashboard load error:', error);
        } finally {
            Utils.showLoading(false);
        }
    }

    static async loadKPIs() {
        try {
            const [sites, equipment, stock, alerts] = await Promise.all([
                ApiService.get('/sites'),
                ApiService.get('/equipment'),
                ApiService.get('/stock'),
                ApiService.get('/alerts?days=1')
            ]);

            // Update KPI values
            document.getElementById('totalSites').textContent = sites.length;
            document.getElementById('totalEquipment').textContent = equipment.length;
            
            const totalStock = stock.reduce((sum, item) => sum + (item.current_quantity || 0), 0);
            document.getElementById('totalFuelStock').textContent = Utils.formatNumber(totalStock, 0) + 'L';
            
            const criticalAlerts = alerts.filter(alert => alert.severity_level === 'Critical').length;
            document.getElementById('criticalAlerts').textContent = criticalAlerts;

            // Update notification count
            document.getElementById('notificationCount').textContent = alerts.length;
        } catch (error) {
            console.error('KPI load error:', error);
        }
    }

    static async loadStockChart() {
        try {
            const stock = await ApiService.get('/stock');
            
            // Destroy existing chart
            if (stockChart) {
                stockChart.destroy();
            }

            // Prepare chart data
            const chartData = stock.slice(0, 10).map(item => ({
                site: item.site_name,
                quantity: item.current_quantity || 0,
                percentage: item.fill_percentage || 0
            }));

            const ctx = document.getElementById('stockChart');
            if (ctx) {
                stockChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: chartData.map(item => item.site),
                        datasets: [{
                            label: 'Stock Level (%)',
                            data: chartData.map(item => item.percentage),
                            backgroundColor: chartData.map(item => {
                                if (item.percentage < 20) return CONFIG.CHART_COLORS.critical;
                                if (item.percentage < 40) return CONFIG.CHART_COLORS.warning;
                                return CONFIG.CHART_COLORS.success;
                            }),
                            borderRadius: 4,
                            borderSkipped: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: false
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100,
                                ticks: {
                                    callback: function(value) {
                                        return value + '%';
                                    }
                                }
                            }
                        }
                    }
                });
            }
        } catch (error) {
            console.error('Stock chart load error:', error);
        }
    }

    static async loadRecentForecasts() {
        try {
            const forecasts = await ApiService.get('/forecasts');
            const recentForecasts = forecasts
                .filter(f => f.forecast_days_remaining <= 7)
                .sort((a, b) => a.forecast_days_remaining - b.forecast_days_remaining)
                .slice(0, 5);

            const container = document.getElementById('recentForecasts');
            if (container) {
                container.innerHTML = recentForecasts.map(forecast => `
                    <div class="forecast-item">
                        <h4>${forecast.site_name} - ${forecast.fuel_name}</h4>
                        <p>Days remaining: <strong>${forecast.forecast_days_remaining}</strong></p>
                        <p>Next refill: ${Utils.formatDate(forecast.next_refill_date_estimate)}</p>
                    </div>
                `).join('') || '<p>No critical forecasts</p>';
            }
        } catch (error) {
            console.error('Recent forecasts load error:', error);
        }
    }
}

// Forecasting Module
class Forecasting {
    static async load() {
        Utils.showLoading(true);
        
        try {
            await Promise.all([
                this.loadSiteFilter(),
                this.loadForecasts()
            ]);
            
            // Set default date to today
            document.getElementById('forecastDateFilter').value = new Date().toISOString().split('T')[0];
        } catch (error) {
            console.error('Forecasting load error:', error);
        } finally {
            Utils.showLoading(false);
        }
    }

    static async loadSiteFilter() {
        try {
            const sites = await ApiService.get('/sites');
            const select = document.getElementById('forecastSiteFilter');
            
            if (select) {
                select.innerHTML = '<option value="">All Sites</option>' +
                    sites.map(site => `<option value="${site.site_id}">${site.site_name}</option>`).join('');
            }
        } catch (error) {
            console.error('Site filter load error:', error);
        }
    }

    static async loadForecasts() {
        try {
            const siteId = document.getElementById('forecastSiteFilter')?.value;
            const forecastDate = document.getElementById('forecastDateFilter')?.value;
            
            let url = '/forecasts';
            const params = new URLSearchParams();
            
            if (siteId) params.append('site_id', siteId);
            if (forecastDate) params.append('forecast_date', forecastDate);
            
            if (params.toString()) {
                url += '?' + params.toString();
            }

            const forecasts = await ApiService.get(url);
            this.renderForecastsTable(forecasts);
        } catch (error) {
            console.error('Forecasts load error:', error);
        }
    }

    static renderForecastsTable(forecasts) {
        const tbody = document.querySelector('#forecastsTable tbody');
        if (!tbody) return;

        tbody.innerHTML = forecasts.map(forecast => {
            const daysClass = forecast.forecast_days_remaining <= 3 ? 'status-critical' : 
                             forecast.forecast_days_remaining <= 7 ? 'status-low' : 'status-normal';
            
            return `
                <tr>
                    <td>${forecast.site_name}</td>
                    <td>${forecast.fuel_name}</td>
                    <td>${Utils.formatNumber(forecast.current_balance, 0)}L</td>
                    <td>${Utils.formatNumber(forecast.daily_consumption_rate, 1)}L/day</td>
                    <td><span class="status-badge ${daysClass}">${forecast.forecast_days_remaining} days</span></td>
                    <td>${Utils.formatDate(forecast.next_refill_date_estimate)}</td>
                    <td>${Utils.formatNumber(forecast.confidence_level, 0)}%</td>
                    <td>
                        <button class="btn btn-ghost" onclick="Forecasting.showScenarios(${forecast.forecast_id})">
                            <i class="fas fa-chart-line"></i> Scenarios
                        </button>
                    </td>
                </tr>
            `;
        }).join('') || '<tr><td colspan="8" style="text-align: center;">No forecasts available</td></tr>';
    }

    static async showScenarios(forecastId) {
        try {
            const scenarios = await ApiService.get(`/forecasts/${forecastId}/scenarios`);
            // Implementation for showing scenarios would go here
            Utils.showNotification('Scenario planning feature coming soon!', 'info');
        } catch (error) {
            console.error('Scenarios load error:', error);
        }
    }
}

// Stock Module
class Stock {
    static async load() {
        Utils.showLoading(true);
        
        try {
            const stock = await ApiService.get('/stock');
            this.renderStockTable(stock);
        } catch (error) {
            console.error('Stock load error:', error);
        } finally {
            Utils.showLoading(false);
        }
    }

    static renderStockTable(stock) {
        const tbody = document.querySelector('#stockTable tbody');
        if (!tbody) return;

        tbody.innerHTML = stock.map(item => `
            <tr>
                <td>${item.site_name}</td>
                <td>${item.fuel_name}</td>
                <td>${Utils.formatNumber(item.current_quantity, 0)}L</td>
                <td>${Utils.formatNumber(item.available_quantity, 0)}L</td>
                <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 60px; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                            <div style="width: ${item.fill_percentage}%; height: 100%; background: ${
                                item.fill_percentage < 20 ? CONFIG.CHART_COLORS.critical :
                                item.fill_percentage < 40 ? CONFIG.CHART_COLORS.warning :
                                CONFIG.CHART_COLORS.success
                            };"></div>
                        </div>
                        <span>${Utils.formatNumber(item.fill_percentage, 1)}%</span>
                    </div>
                </td>
                <td><span class="status-badge ${Utils.getStatusClass(item.stock_status)}">${item.stock_status}</span></td>
                <td>${Utils.formatDateTime(item.last_updated)}</td>
            </tr>
        `).join('') || '<tr><td colspan="7" style="text-align: center;">No stock data available</td></tr>';
    }
}

// Equipment Module
class Equipment {
    static async load() {
        Utils.showLoading(true);
        
        try {
            const equipment = await ApiService.get('/equipment');
            this.renderEquipmentTable(equipment);
        } catch (error) {
            console.error('Equipment load error:', error);
        } finally {
            Utils.showLoading(false);
        }
    }

    static renderEquipmentTable(equipment) {
        const tbody = document.querySelector('#equipmentTable tbody');
        if (!tbody) return;

        tbody.innerHTML = equipment.map(item => `
            <tr>
                <td>${item.equipment_name}</td>
                <td>${item.site_name}</td>
                <td>${item.equipment_type || 'N/A'}</td>
                <td>${item.fuel_name}</td>
                <td>${Utils.formatNumber(item.consumption_rate, 1)}</td>
                <td>${item.manufacturer || 'N/A'}</td>
                <td>${item.model || 'N/A'}</td>
                <td><span class="status-badge ${item.is_active ? 'status-normal' : 'status-critical'}">${item.is_active ? 'Active' : 'Inactive'}</span></td>
                <td>
                    <button class="btn btn-ghost" onclick="Equipment.edit(${item.equipment_id})">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="9" style="text-align: center;">No equipment data available</td></tr>';
    }

    static edit(equipmentId) {
        Utils.showNotification('Equipment editing feature coming soon!', 'info');
    }
}

// Operational Hours Module
class OperationalHours {
    static async load() {
        Utils.showLoading(true);
        
        try {
            await Promise.all([
                this.loadSiteOptions(),
                this.loadOperationalHours()
            ]);
            
            // Set default date to today
            document.getElementById('hoursLogDate').value = new Date().toISOString().split('T')[0];
            
            // Setup form handler
            this.setupForm();
        } catch (error) {
            console.error('Operational hours load error:', error);
        } finally {
            Utils.showLoading(false);
        }
    }

    static async loadSiteOptions() {
        try {
            const sites = await ApiService.get('/sites');
            const select = document.getElementById('hoursLogSite');
            
            if (select) {
                select.innerHTML = '<option value="">Select Site</option>' +
                    sites.map(site => `<option value="${site.site_id}">${site.site_name}</option>`).join('');
            }
        } catch (error) {
            console.error('Site options load error:', error);
        }
    }

    static async loadSiteEquipment() {
        const siteId = document.getElementById('hoursLogSite')?.value;
        const equipmentSelect = document.getElementById('hoursLogEquipment');
        
        if (!siteId || !equipmentSelect) return;

        try {
            const equipment = await ApiService.get(`/equipment?site_id=${siteId}`);
            equipmentSelect.innerHTML = '<option value="">Select Equipment</option>' +
                equipment.map(eq => `<option value="${eq.equipment_id}">${eq.equipment_name}</option>`).join('');
        } catch (error) {
            console.error('Equipment load error:', error);
        }
    }

    static async loadOperationalHours() {
        try {
            const hours = await ApiService.get('/operational-hours');
            this.renderOperationalHoursTable(hours);
        } catch (error) {
            console.error('Operational hours load error:', error);
        }
    }

    static renderOperationalHoursTable(hours) {
        const tbody = document.querySelector('#operationalHoursTable tbody');
        if (!tbody) return;

        tbody.innerHTML = hours.map(item => `
            <tr>
                <td>${Utils.formatDate(item.log_date)}</td>
                <td>${item.site_name}</td>
                <td>${item.equipment_name}</td>
                <td>${Utils.formatNumber(item.running_hours, 1)}</td>
                <td>${item.fuel_consumed ? Utils.formatNumber(item.fuel_consumed, 1) + 'L' : 'N/A'}</td>
                <td>${item.recorded_by || 'N/A'}</td>
                <td>${item.notes || 'N/A'}</td>
            </tr>
        `).join('') || '<tr><td colspan="7" style="text-align: center;">No operational hours data available</td></tr>';
    }

    static setupForm() {
        const form = document.getElementById('quickHoursForm');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                site_id: parseInt(document.getElementById('hoursLogSite').value),
                equipment_id: parseInt(document.getElementById('hoursLogEquipment').value),
                log_date: document.getElementById('hoursLogDate').value,
                running_hours: parseFloat(document.getElementById('hoursLogHours').value),
                recorded_by: document.getElementById('hoursLogRecordedBy').value,
                notes: document.getElementById('hoursLogNotes').value
            };

            try {
                Utils.showLoading(true);
                await ApiService.post('/operational-hours', formData);
                Utils.showNotification('Operational hours logged successfully!', 'success');
                form.reset();
                document.getElementById('hoursLogDate').value = new Date().toISOString().split('T')[0];
                await this.loadOperationalHours();
            } catch (error) {
                console.error('Hours logging error:', error);
            } finally {
                Utils.showLoading(false);
            }
        });
    }
}

// Refills Module
class Refills {
    static async load() {
        Utils.showLoading(true);
        
        try {
            const refills = await ApiService.get('/refills');
            this.renderRefillsTable(refills);
        } catch (error) {
            console.error('Refills load error:', error);
        } finally {
            Utils.showLoading(false);
        }
    }

    static renderRefillsTable(refills) {
        const tbody = document.querySelector('#refillsTable tbody');
        if (!tbody) return;

        tbody.innerHTML = refills.map(refill => `
            <tr>
                <td>${refill.transaction_id}</td>
                <td>${Utils.formatDate(refill.refill_date)}</td>
                <td>${refill.site_name}</td>
                <td>${refill.fuel_name}</td>
                <td>${Utils.formatNumber(refill.quantity, 0)}L</td>
                <td>${refill.supplier_name || 'N/A'}</td>
                <td>${refill.unit_cost ? Utils.formatNumber(refill.unit_cost, 2) : 'N/A'}</td>
                <td>${refill.total_cost ? Utils.formatNumber(refill.total_cost, 0) : 'N/A'}</td>
                <td>${refill.created_by || 'System'}</td>
            </tr>
        `).join('') || '<tr><td colspan="9" style="text-align: center;">No refill transactions found</td></tr>';
    }
}

// Usage Module
class Usage {
    static async load() {
        Utils.showLoading(true);
        
        try {
            const usage = await ApiService.get('/usage');
            this.renderUsageTable(usage);
        } catch (error) {
            console.error('Usage load error:', error);
        } finally {
            Utils.showLoading(false);
        }
    }

    static renderUsageTable(usage) {
        const tbody = document.querySelector('#usageTable tbody');
        if (!tbody) return;

        tbody.innerHTML = usage.map(item => `
            <tr>
                <td>${item.transaction_id}</td>
                <td>${Utils.formatDate(item.usage_date)}</td>
                <td>${item.site_name}</td>
                <td>${item.fuel_name}</td>
                <td>${item.equipment_name || 'N/A'}</td>
                <td>${Utils.formatNumber(item.quantity, 0)}L</td>
                <td>${item.purpose || 'N/A'}</td>
                <td>${item.operator_name || 'N/A'}</td>
                <td>${item.created_by || 'System'}</td>
            </tr>
        `).join('') || '<tr><td colspan="9" style="text-align: center;">No usage transactions found</td></tr>';
    }
}

// Global Functions (called from HTML)
window.refreshDashboard = () => Dashboard.load();
window.refreshStock = () => Stock.load();
window.calculateAllForecasts = async () => {
    try {
        Utils.showLoading(true);
        await ApiService.post('/forecasts/calculate');
        Utils.showNotification('Forecasts calculated successfully!', 'success');
        if (currentSection === 'forecasting') {
            await Forecasting.loadForecasts();
        }
    } catch (error) {
        console.error('Calculate forecasts error:', error);
    } finally {
        Utils.showLoading(false);
    }
};

window.loadForecasts = () => Forecasting.loadForecasts();
window.loadSiteEquipment = () => OperationalHours.loadSiteEquipment();
window.showForecastInput = () => Utils.showNotification('Forecast input feature coming soon!', 'info');
window.showEquipmentForm = () => Utils.showNotification('Equipment form feature coming soon!', 'info');
window.showHoursForm = () => Utils.showNotification('Hours form is already visible below!', 'info');
window.hideScenarioCard = () => {
    const card = document.getElementById('scenarioCard');
    if (card) card.style.display = 'none';
};

// Application Initialization
document.addEventListener('DOMContentLoaded', () => {
    console.log('Advanced Fuel Control & Forecasting System v2.0 - Initializing...');
    
    // Handle missing logo images gracefully
    const companyLogo = document.getElementById('companyLogo');
    if (companyLogo) {
        companyLogo.onerror = function() {
            this.style.display = 'none';
        };
    }
    
    const footerLogo = document.getElementById('footerLogo');
    if (footerLogo) {
        footerLogo.onerror = function() {
            this.style.display = 'none';
        };
    }
    
    // Initialize navigation
    Navigation.init();
    
    // Set last updated time
    const lastUpdatedElement = document.getElementById('lastUpdated');
    if (lastUpdatedElement) {
        lastUpdatedElement.textContent = new Date().toLocaleString();
    }
    
    // Setup auto-refresh for dashboard
    setInterval(() => {
        if (currentSection === 'dashboard') {
            Dashboard.loadKPIs();
        }
    }, CONFIG.REFRESH_INTERVAL);
    
    console.log('Application initialized successfully!');
});

// Export for debugging
window.FuelControlApp = {
    CONFIG,
    Utils,
    ApiService,
    Navigation,
    Dashboard,
    Forecasting,
    Stock,
    Equipment,
    OperationalHours,
    globalData
};
