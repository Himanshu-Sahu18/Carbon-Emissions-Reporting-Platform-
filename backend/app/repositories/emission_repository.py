"""
Emission Repository Module
Handles all database operations related to emission records and factors
"""
import logging
from datetime import date
from typing import Optional, List, Dict, Any
from psycopg2.extras import RealDictRow

from app.database import get_db_cursor

logger = logging.getLogger(__name__)


class EmissionRepository:
    """
    Repository for emission-related database operations.
    Implements data access methods for emission records and factors.
    """
    
    def get_valid_factor(
        self, 
        activity_name: str, 
        scope: int, 
        activity_date: date
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve the emission factor that was valid on a specific date.
        Implements time-aware query to ensure historical accuracy.
        
        Args:
            activity_name: Name of the activity (e.g., 'Diesel', 'Grid Electricity')
            scope: GHG Protocol scope (1, 2, or 3)
            activity_date: The date the activity occurred
            
        Returns:
            Dictionary containing factor details or None if not found
            Keys: factor_id, co2e_per_unit, activity_unit, source
            
        Requirements: 1.3, 1.4, 1.5, 1.6
        """
        query = """
            SELECT 
                factor_id,
                co2e_per_unit,
                activity_unit,
                source,
                valid_from,
                valid_to
            FROM emission_factors
            WHERE activity_name = %s
              AND scope = %s
              AND valid_from <= %s
              AND (valid_to >= %s OR valid_to IS NULL)
            ORDER BY valid_from DESC, created_at DESC
            LIMIT 1
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (activity_name, scope, activity_date, activity_date))
                result = cursor.fetchone()
                
                if result:
                    logger.debug(
                        f"Found emission factor {result['factor_id']} for "
                        f"{activity_name} (scope {scope}) on {activity_date}"
                    )
                    return dict(result)
                else:
                    logger.warning(
                        f"No emission factor found for {activity_name} "
                        f"(scope {scope}) on {activity_date}"
                    )
                    return None
                    
        except Exception as e:
            logger.error(f"Error retrieving emission factor: {e}")
            raise
    
    def get_emissions_by_year_and_scope(
        self, 
        years: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve total emissions grouped by year and scope.
        Used for Year-over-Year analysis.
        
        Args:
            years: List of years to retrieve data for (e.g., [2023, 2024])
            
        Returns:
            List of dictionaries with keys: year, scope, total_emissions
            
        Requirements: 2.2, 2.3, 2.4
        """
        query = """
            SELECT
                EXTRACT(YEAR FROM activity_date)::INTEGER AS year,
                scope,
                SUM(COALESCE(overridden_co2e, calculated_co2e)) AS total_emissions
            FROM emission_records
            WHERE EXTRACT(YEAR FROM activity_date) = ANY(%s)
            GROUP BY EXTRACT(YEAR FROM activity_date), scope
            ORDER BY year DESC, scope ASC
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (years,))
                results = cursor.fetchall()
                
                logger.debug(
                    f"Retrieved {len(results)} emission records for years {years}"
                )
                
                return [dict(row) for row in results]
                
        except Exception as e:
            logger.error(f"Error retrieving emissions by year and scope: {e}")
            raise
    
    def get_total_emissions_for_period(
        self, 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """
        Calculate total emissions for a specific date range.
        Used for emission intensity calculations.
        
        Args:
            start_date: Start of the period
            end_date: End of the period
            
        Returns:
            Dictionary with keys: total_emissions, record_count
            
        Requirements: 3.2
        """
        query = """
            SELECT 
                SUM(COALESCE(overridden_co2e, calculated_co2e)) AS total_emissions,
                COUNT(*) AS record_count
            FROM emission_records
            WHERE activity_date BETWEEN %s AND %s
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (start_date, end_date))
                result = cursor.fetchone()
                
                if result:
                    logger.debug(
                        f"Total emissions for period {start_date} to {end_date}: "
                        f"{result['total_emissions']} kgCO2e ({result['record_count']} records)"
                    )
                    return dict(result)
                else:
                    return {'total_emissions': 0, 'record_count': 0}
                    
        except Exception as e:
            logger.error(f"Error calculating total emissions for period: {e}")
            raise
    
    def get_emissions_by_source(
        self, 
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve emissions grouped by activity source with optional filtering.
        Used for hotspot analysis.
        
        Args:
            filters: Dictionary containing optional filters:
                - start_date: Filter start date
                - end_date: Filter end date
                - scope: Filter by scope (1, 2, or 3)
                - limit: Maximum number of results (default: 10)
                
        Returns:
            List of dictionaries with keys: activity_name, scope, total_emissions,
            record_count, average_per_record
            
        Requirements: 4.2, 4.3, 4.4
        """
        # Build dynamic query based on filters
        query = """
            SELECT
                activity_name,
                scope,
                SUM(COALESCE(overridden_co2e, calculated_co2e)) AS total_emissions,
                COUNT(*) AS record_count,
                AVG(COALESCE(overridden_co2e, calculated_co2e)) AS average_per_record
            FROM emission_records
            WHERE 1=1
        """
        
        params = []
        
        # Add date range filters
        if filters.get('start_date'):
            query += " AND activity_date >= %s"
            params.append(filters['start_date'])
            
        if filters.get('end_date'):
            query += " AND activity_date <= %s"
            params.append(filters['end_date'])
            
        # Add scope filter
        if filters.get('scope'):
            query += " AND scope = %s"
            params.append(filters['scope'])
        
        # Group and order
        query += """
            GROUP BY activity_name, scope
            ORDER BY total_emissions DESC
        """
        
        # Add limit
        limit = filters.get('limit', 10)
        query += " LIMIT %s"
        params.append(limit)
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                
                logger.debug(
                    f"Retrieved {len(results)} emission hotspots with filters: {filters}"
                )
                
                return [dict(row) for row in results]
                
        except Exception as e:
            logger.error(f"Error retrieving emissions by source: {e}")
            raise


    def get_monthly_emissions(self, year: int) -> List[Dict[str, Any]]:
        """
        Retrieve emissions aggregated by month for a specific year.
        Used for monthly trend analysis.
        
        Args:
            year: Year to retrieve monthly data for
            
        Returns:
            List of dictionaries with keys: month, month_name, total_emissions
        """
        query = """
            SELECT
                EXTRACT(MONTH FROM activity_date)::INTEGER AS month,
                TO_CHAR(activity_date, 'Month') AS month_name,
                SUM(COALESCE(overridden_co2e, calculated_co2e)) AS total_emissions
            FROM emission_records
            WHERE EXTRACT(YEAR FROM activity_date) = %s
            GROUP BY EXTRACT(MONTH FROM activity_date), TO_CHAR(activity_date, 'Month')
            ORDER BY month ASC
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (year,))
                results = cursor.fetchall()
                
                logger.debug(
                    f"Retrieved {len(results)} monthly emission records for year {year}"
                )
                
                return [dict(row) for row in results]
                
        except Exception as e:
            logger.error(f"Error retrieving monthly emissions: {e}")
            raise
