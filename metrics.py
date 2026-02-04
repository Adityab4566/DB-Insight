"""
Metrics collection module for MySQL performance monitoring.
Collects various performance metrics from MySQL Performance Schema.
"""

import logging
import time
from datetime import datetime
from database import db_manager
from config import Config

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collects and processes MySQL performance metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.config = Config()
        self.last_query_count = 0
        self.last_query_time = time.time()
    
    def get_active_connections(self):
        """Get current number of active connections."""
        try:
            query = """
            SELECT COUNT(*) as active_connections 
            FROM performance_schema.threads 
            WHERE type = 'FOREGROUND'
            """
            result = db_manager.get_single_value(query)
            return result if result is not None else 0
        except Exception as e:
            logger.error(f"Error getting active connections: {str(e)}")
            return 0
    
    def get_queries_per_second(self):
        """Calculate queries per second based on global status."""
        try:
            query = "SHOW GLOBAL STATUS LIKE 'Questions'"
            result = db_manager.execute_query(query)
            
            if result and len(result) > 0:
                current_queries = int(result[0]['Value'])
                current_time = time.time()
                
                if self.last_query_count > 0:
                    time_diff = current_time - self.last_query_time
                    query_diff = current_queries - self.last_query_count
                    qps = query_diff / time_diff if time_diff > 0 else 0
                else:
                    qps = 0
                
                self.last_query_count = current_queries
                self.last_query_time = current_time
                
                return round(qps, 2)
            return 0
        except Exception as e:
            logger.error(f"Error calculating QPS: {str(e)}")
            return 0
    
    def get_slow_queries(self):
        """Get count of slow queries."""
        try:
            query = "SHOW GLOBAL STATUS LIKE 'Slow_queries'"
            result = db_manager.execute_query(query)
            
            if result and len(result) > 0:
                return int(result[0]['Value'])
            return 0
        except Exception as e:
            logger.error(f"Error getting slow queries: {str(e)}")
            return 0
    
    def get_database_uptime(self):
        """Get database uptime in seconds."""
        try:
            query = "SHOW GLOBAL STATUS LIKE 'Uptime'"
            result = db_manager.execute_query(query)
            
            if result and len(result) > 0:
                uptime_seconds = int(result[0]['Value'])
                return uptime_seconds
            return 0
        except Exception as e:
            logger.error(f"Error getting uptime: {str(e)}")
            return 0
    
    def format_uptime(self, uptime_seconds):
        """Format uptime seconds into human readable format."""
        if uptime_seconds < 60:
            return f"{uptime_seconds}s"
        elif uptime_seconds < 3600:
            minutes = uptime_seconds // 60
            seconds = uptime_seconds % 60
            return f"{minutes}m {seconds}s"
        elif uptime_seconds < 86400:
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        else:
            days = uptime_seconds // 86400
            hours = (uptime_seconds % 86400) // 3600
            return f"{days}d {hours}h"
    
    def get_database_size(self):
        """Get total database size in MB."""
        try:
            query = """
            SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
            FROM information_schema.tables
            """
            result = db_manager.get_single_value(query)
            return result if result is not None else 0
        except Exception as e:
            logger.error(f"Error getting database size: {str(e)}")
            return 0
    
    def get_cpu_usage_estimate(self):
        """Estimate CPU usage based on active threads and queries."""
        try:
            # This is a simplified estimation based on active connections and query rate
            active_connections = self.get_active_connections()
            qps = self.get_queries_per_second()
            
            # Simple heuristic: base load + connection load + query load
            base_load = 5  # Base MySQL overhead
            connection_load = min(active_connections * 2, 30)  # Max 30% from connections
            query_load = min(qps * 0.5, 40)  # Max 40% from queries
            
            estimated_cpu = base_load + connection_load + query_load
            return min(round(estimated_cpu, 1), 100)  # Cap at 100%
        except Exception as e:
            logger.error(f"Error estimating CPU usage: {str(e)}")
            return 0
    
    def get_memory_usage_estimate(self):
        """Estimate memory usage based on buffer pool and connections."""
        try:
            # Get InnoDB buffer pool size
            query = "SHOW VARIABLES LIKE 'innodb_buffer_pool_size'"
            result = db_manager.execute_query(query)
            
            if result and len(result) > 0:
                buffer_pool_size = int(result[0]['Value'])
                buffer_pool_mb = buffer_pool_size / (1024 * 1024)
                
                # Estimate total memory usage (buffer pool + connections + overhead)
                active_connections = self.get_active_connections()
                connection_memory = active_connections * 2  # ~2MB per connection
                overhead_memory = 100  # Base overhead
                
                total_memory_mb = buffer_pool_mb + connection_memory + overhead_memory
                
                # Convert to percentage (assuming 8GB total system memory as baseline)
                system_memory_mb = 8192
                memory_percentage = min((total_memory_mb / system_memory_mb) * 100, 100)
                
                return round(memory_percentage, 1)
            return 0
        except Exception as e:
            logger.error(f"Error estimating memory usage: {str(e)}")
            return 0
    
    def get_health_status(self):
        """Determine overall database health status."""
        try:
            # Test basic connectivity
            if not db_manager.test_connection():
                return "DOWN"
            
            # Check for warning conditions
            active_connections = self.get_active_connections()
            slow_queries = self.get_slow_queries()
            
            warnings = []
            
            if active_connections > self.config.CONNECTION_THRESHOLD:
                warnings.append("High connection count")
            
            if slow_queries > 100:  # Arbitrary threshold
                warnings.append("High slow query count")
            
            if warnings:
                return f"WARNING: {', '.join(warnings)}"
            
            return "UP"
        except Exception as e:
            logger.error(f"Error checking health status: {str(e)}")
            return "DOWN"
    
    def collect_all_metrics(self):
        """Collect all metrics and return as dictionary."""
        try:
            uptime_seconds = self.get_database_uptime()
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'active_connections': self.get_active_connections(),
                'queries_per_second': self.get_queries_per_second(),
                'slow_queries': self.get_slow_queries(),
                'uptime_seconds': uptime_seconds,
                'uptime_formatted': self.format_uptime(uptime_seconds),
                'database_size_mb': self.get_database_size(),
                'cpu_usage_percent': self.get_cpu_usage_estimate(),
                'memory_usage_percent': self.get_memory_usage_estimate(),
                'health_status': self.get_health_status()
            }
            
            logger.info(f"Metrics collected successfully: {metrics['health_status']}")
            return metrics
        except Exception as e:
            logger.error(f"Error collecting metrics: {str(e)}")
            return {
                'timestamp': datetime.now().isoformat(),
                'active_connections': 0,
                'queries_per_second': 0,
                'slow_queries': 0,
                'uptime_seconds': 0,
                'uptime_formatted': '0s',
                'database_size_mb': 0,
                'cpu_usage_percent': 0,
                'memory_usage_percent': 0,
                'health_status': 'DOWN'
            }

# Global metrics collector instance
metrics_collector = MetricsCollector()