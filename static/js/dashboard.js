/**
 * Database Performance Monitoring Dashboard JavaScript
 * Handles real-time data updates and chart rendering
 */

class DatabaseDashboard {
    constructor() {
        this.refreshInterval = 5000; // 5 seconds
        this.maxDataPoints = 20; // Keep last 20 data points for charts
        this.charts = {};
        this.metricsHistory = {
            timestamps: [],
            connections: [],
            qps: [],
            cpu: [],
            memory: []
        };
        
        this.init();
    }
    
    /**
     * Initialize the dashboard
     */
    init() {
        console.log('Initializing Database Dashboard...');
        this.setupCharts();
        this.loadInitialData();
        this.startAutoRefresh();
        this.setupEventListeners();
    }
    
    /**
     * Setup Chart.js charts
     */
    setupCharts() {
        // Connections Chart
        const connectionsCtx = document.getElementById('connectionsChart');
        if (connectionsCtx) {
            this.charts.connections = new Chart(connectionsCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Active Connections',
                        data: [],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Connections'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
        
        // QPS Chart
        const qpsCtx = document.getElementById('qpsChart');
        if (qpsCtx) {
            this.charts.qps = new Chart(qpsCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Queries Per Second',
                        data: [],
                        borderColor: '#28a745',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'QPS'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
        
        // Resource Usage Chart (CPU & Memory)
        const resourceCtx = document.getElementById('resourceChart');
        if (resourceCtx) {
            this.charts.resource = new Chart(resourceCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'CPU Usage (%)',
                            data: [],
                            borderColor: '#ffc107',
                            backgroundColor: 'rgba(255, 193, 7, 0.1)',
                            borderWidth: 2,
                            fill: false,
                            tension: 0.4
                        },
                        {
                            label: 'Memory Usage (%)',
                            data: [],
                            borderColor: '#dc3545',
                            backgroundColor: 'rgba(220, 53, 69, 0.1)',
                            borderWidth: 2,
                            fill: false,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'Usage (%)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    }
                }
            });
        }
    }
    
    /**
     * Load initial data
     */
    async loadInitialData() {
        await this.fetchAndUpdateMetrics();
    }
    
    /**
     * Start auto-refresh timer
     */
    startAutoRefresh() {
        setInterval(() => {
            this.fetchAndUpdateMetrics();
        }, this.refreshInterval);
        
        console.log(`Auto-refresh started with ${this.refreshInterval/1000}s interval`);
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Manual refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.fetchAndUpdateMetrics();
            });
        }
        
        // Handle visibility change to pause/resume updates
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                console.log('Dashboard hidden, pausing updates');
            } else {
                console.log('Dashboard visible, resuming updates');
                this.fetchAndUpdateMetrics();
            }
        });
    }
    
    /**
     * Fetch metrics from API and update dashboard
     */
    async fetchAndUpdateMetrics() {
        try {
            console.log('Fetching metrics...');
            const response = await fetch('/api/metrics');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const metrics = await response.json();
            this.updateDashboard(metrics);
            this.updateCharts(metrics);
            this.updateStatus('success', 'Connected');
            
        } catch (error) {
            console.error('Error fetching metrics:', error);
            this.updateStatus('error', 'Connection Error');
            this.showError('Failed to fetch metrics: ' + error.message);
        }
    }
    
    /**
     * Update dashboard metrics display
     */
    updateDashboard(metrics) {
        // Update metric values
        this.updateElement('activeConnections', metrics.active_connections);
        this.updateElement('queriesPerSecond', metrics.queries_per_second);
        this.updateElement('slowQueries', metrics.slow_queries);
        this.updateElement('uptime', metrics.uptime_formatted);
        this.updateElement('databaseSize', metrics.database_size_mb + ' MB');
        this.updateElement('cpuUsage', metrics.cpu_usage_percent + '%');
        this.updateElement('memoryUsage', metrics.memory_usage_percent + '%');
        
        // Update health status
        this.updateHealthStatus(metrics.health_status);
        
        // Update last updated time
        const now = new Date();
        this.updateElement('lastUpdated', now.toLocaleTimeString());
        
        console.log('Dashboard updated successfully');
    }
    
    /**
     * Update charts with new data
     */
    updateCharts(metrics) {
        const timestamp = new Date().toLocaleTimeString();
        
        // Add new data point
        this.metricsHistory.timestamps.push(timestamp);
        this.metricsHistory.connections.push(metrics.active_connections);
        this.metricsHistory.qps.push(metrics.queries_per_second);
        this.metricsHistory.cpu.push(metrics.cpu_usage_percent);
        this.metricsHistory.memory.push(metrics.memory_usage_percent);
        
        // Keep only last N data points
        if (this.metricsHistory.timestamps.length > this.maxDataPoints) {
            this.metricsHistory.timestamps.shift();
            this.metricsHistory.connections.shift();
            this.metricsHistory.qps.shift();
            this.metricsHistory.cpu.shift();
            this.metricsHistory.memory.shift();
        }
        
        // Update charts
        if (this.charts.connections) {
            this.charts.connections.data.labels = [...this.metricsHistory.timestamps];
            this.charts.connections.data.datasets[0].data = [...this.metricsHistory.connections];
            this.charts.connections.update('none');
        }
        
        if (this.charts.qps) {
            this.charts.qps.data.labels = [...this.metricsHistory.timestamps];
            this.charts.qps.data.datasets[0].data = [...this.metricsHistory.qps];
            this.charts.qps.update('none');
        }
        
        if (this.charts.resource) {
            this.charts.resource.data.labels = [...this.metricsHistory.timestamps];
            this.charts.resource.data.datasets[0].data = [...this.metricsHistory.cpu];
            this.charts.resource.data.datasets[1].data = [...this.metricsHistory.memory];
            this.charts.resource.update('none');
        }
    }
    
    /**
     * Update health status indicator
     */
    updateHealthStatus(status) {
        const statusElement = document.getElementById('healthStatus');
        const indicatorElement = document.getElementById('statusIndicator');
        
        if (statusElement) {
            statusElement.textContent = status;
        }
        
        if (indicatorElement) {
            // Remove existing status classes
            indicatorElement.classList.remove('status-up', 'status-warning', 'status-down');
            
            // Add appropriate status class
            if (status === 'UP') {
                indicatorElement.classList.add('status-up');
            } else if (status.startsWith('WARNING')) {
                indicatorElement.classList.add('status-warning');
            } else {
                indicatorElement.classList.add('status-down');
            }
        }
    }
    
    /**
     * Update connection status
     */
    updateStatus(type, message) {
        const statusElement = document.getElementById('connectionStatus');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status-item text-${type === 'success' ? 'success' : 'danger'}`;
        }
    }
    
    /**
     * Update DOM element with new value
     */
    updateElement(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        }
    }
    
    /**
     * Show error message
     */
    showError(message) {
        const errorContainer = document.getElementById('errorContainer');
        if (errorContainer) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Error:</strong> ${message}
                </div>
            `;
            
            // Auto-hide error after 10 seconds
            setTimeout(() => {
                errorContainer.innerHTML = '';
            }, 10000);
        }
    }
    
    /**
     * Show success message
     */
    showSuccess(message) {
        const errorContainer = document.getElementById('errorContainer');
        if (errorContainer) {
            errorContainer.innerHTML = `
                <div class="alert alert-success">
                    ${message}
                </div>
            `;
            
            // Auto-hide message after 5 seconds
            setTimeout(() => {
                errorContainer.innerHTML = '';
            }, 5000);
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing dashboard...');
    window.dashboard = new DatabaseDashboard();
});

// Handle page unload
window.addEventListener('beforeunload', function() {
    console.log('Dashboard shutting down...');
});