"""
Business Metrics Repository Module
Handles all database operations related to business metrics
"""
import logging
from datetime import date
from typing import Optional, List, Dict, Any

from app.database import get_db_cursor

logger = logging.getLogger(__name__)


class BusinessMetricsRepository:
    """
    Repository for business metrics database operations.
    Implements data access methods for production and operational metrics.
    """
    
    def get_metric_total_for_period(
        self, 
        metric_name: str, 
        start_date: date, 
        end_date: date
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate the total value of a specific metric for a date range.
        Used for emission intensity calculations.
        
        Args:
            metric_name: Name of the metric (e.g., 'Tons of Steel Produced')
            start_date: Start of the period
            end_date: End of the period
            
        Returns:
            Dictionary with keys: total_value, unit, record_count
            Returns None if no data found
            
        Requirements: 3.3, 3.4
        """
        query = """
            SELECT 
                SUM(value) AS total_value,
                MAX(unit) AS unit,
                COUNT(*) AS record_count
            FROM business_metrics
            WHERE metric_name = %s
              AND metric_date BETWEEN %s AND %s
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (metric_name, start_date, end_date))
                result = cursor.fetchone()
                
                if result and result['total_value'] is not None:
                    logger.debug(
                        f"Total {metric_name} for period {start_date} to {end_date}: "
                        f"{result['total_value']} {result['unit']} "
                        f"({result['record_count']} records)"
                    )
                    return dict(result)
                else:
                    logger.warning(
                        f"No data found for metric '{metric_name}' "
                        f"in period {start_date} to {end_date}"
                    )
                    return None
                    
        except Exception as e:
            logger.error(f"Error retrieving metric total for period: {e}")
            raise
    
    def get_available_metrics(self) -> List[Dict[str, Any]]:
        """
        Retrieve a list of all available metrics in the system.
        Useful for API validation and user interface dropdowns.
        
        Returns:
            List of dictionaries with keys: metric_name, metric_category, unit
            
        Requirements: 3.3, 3.4
        """
        query = """
            SELECT DISTINCT
                metric_name,
                metric_category,
                unit
            FROM business_metrics
            ORDER BY metric_name
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                
                logger.debug(f"Retrieved {len(results)} available metrics")
                
                return [dict(row) for row in results]
                
        except Exception as e:
            logger.error(f"Error retrieving available metrics: {e}")
            raise

