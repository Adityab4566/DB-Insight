# 🗄️ Database Performance Monitoring Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **real-time MySQL database performance monitoring system** built with Flask and Chart.js. This dashboard provides comprehensive insights into your database performance with beautiful visualizations and real-time metrics.



## ✨ Features

- 📊 **Real-time Monitoring** - Live performance metrics with 5-second auto-refresh
- 📈 **Interactive Charts** - Beautiful visualizations using Chart.js
- 🎯 **Key Metrics Tracking** - Connections, QPS, slow queries, uptime, and more
- 🚨 **Health Monitoring** - Automatic alerts for performance issues
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices
- 🔌 **REST API** - Programmatic access to all metrics
- 🔒 **Secure Access** - Read-only database monitoring user
- ⚡ **Lightweight** - Minimal resource usage with efficient queries

## 📊 Monitored Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **Active Connections** | Current database connections | > 100 connections |
| **Queries Per Second (QPS)** | Database query throughput | - |
| **Slow Queries** | Queries exceeding execution time | > 100 total |
| **Database Uptime** | Continuous operation time | - |
| **Database Size** | Total storage usage (MB) | - |
| **CPU Usage** | Estimated CPU utilization | > 80% |
| **Memory Usage** | Estimated memory utilization | > 90% |
| **Health Status** | Overall database availability | DOWN/WARNING |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/db-performance-monitor.git
cd db-performance-monitor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database

Run the following commands in MySQL Workbench or command line:

```sql
-- Create database and monitoring user
CREATE DATABASE IF NOT EXISTS db_monitoring;
CREATE USER IF NOT EXISTS 'monitor_user'@'localhost' IDENTIFIED BY 'monitor123';
GRANT SELECT, PROCESS, SHOW DATABASES ON *.* TO 'monitor_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'monitor_user'@'localhost';
GRANT SELECT ON information_schema.* TO 'monitor_user'@'localhost';
FLUSH PRIVILEGES;
```

Or simply run the setup commands from `DEMO_COMMANDS.sql`.

### 4. Configure Environment

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_monitoring
DB_USER=monitor_user
DB_PASSWORD=monitor123

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Start the Application

```bash
python run.py
```

### 6. Access the Dashboard

Open your browser and navigate to:
- **Dashboard**: http://localhost:5000
- **API Metrics**: http://localhost:5000/api/metrics
- **Health Check**: http://localhost:5000/api/health

## 🏗️ Project Structure

```
db-performance-monitor/
├── 📁 static/
│   ├── 📁 css/
│   │   └── style.css          # Dashboard styling
│   └── 📁 js/
│       └── dashboard.js       # Frontend JavaScript
├── 📁 templates/
│   └── dashboard.html         # Main dashboard template
├── 📁 logs/
│   └── monitoring.log         # Application logs
├── app.py                     # Main Flask application
├── run.py                     # Application runner
├── config.py                  # Configuration management
├── database.py                # Database connection layer
├── metrics.py                 # Performance metrics collection
├── requirements.txt           # Python dependencies
├── DEMO_COMMANDS.sql          # MySQL setup commands
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🔌 API Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Main dashboard page | HTML |
| `/api/metrics` | GET | All performance metrics | JSON |
| `/api/health` | GET | Database health check | JSON |
| `/api/config` | GET | Configuration info | JSON |

### Example API Response

```json
{
  "timestamp": "2024-01-27T10:30:00",
  "active_connections": 15,
  "queries_per_second": 45.2,
  "slow_queries": 3,
  "uptime_seconds": 86400,
  "uptime_formatted": "1d 0h",
  "database_size_mb": 256.7,
  "cpu_usage_percent": 25.5,
  "memory_usage_percent": 45.2,
  "health_status": "UP"
}
```

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: MySQL 8.0+ with Performance Schema
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js 3.x
- **Database Driver**: PyMySQL
- **Configuration**: python-dotenv


### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | localhost |
| `DB_PORT` | MySQL port | 3306 |
| `DB_NAME` | Database name | db_monitoring |
| `DB_USER` | Database user | monitor_user |
| `DB_PASSWORD` | Database password | - |
| `FLASK_ENV` | Flask environment | development |
| `FLASK_DEBUG` | Debug mode | True |

### Monitoring Settings

- **Refresh Interval**: 5 seconds
- **Slow Query Threshold**: 1.0 seconds
- **Connection Alert Threshold**: 100 connections
- **Chart Data Points**: Last 20 measurements


### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check MySQL service is running
   sudo systemctl status mysql
   
   # Verify user permissions
   SHOW GRANTS FOR 'monitor_user'@'localhost';
   ```

2. **Permission Denied Errors**
   ```sql
   -- Re-grant permissions
   GRANT SELECT ON performance_schema.* TO 'monitor_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port 5000
   netstat -tulpn | grep :5000
   
   # Kill the process
   kill -9 <PID>
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Chart.js](https://www.chartjs.org/) - Beautiful charts
- [PyMySQL](https://pymysql.readthedocs.io/) - MySQL connector
- [MySQL Performance Schema](https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html) - Performance monitoring



⭐ **Star this repository if you find it helpful!**

Built with ❤️ for database administrators and developers who care about performance.
