"""
Analytics Service Module
Handles business logic for analytical queries and reporting
"""
import logging
from datetime import date
from typing import Optional, Dict, Any

from app.repositories.emission_repository import EmissionRepository
from app.repositories.business_metrics_repository import BusinessMetricsRepository
from app.exceptions import NoProductionDataException, InvalidDateRangeException

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for analytical operations on emission and business metrics data.
    Orchestrates repository calls and implements business logic for:
    - Year-over-Year emissions comparison
    - Emission intensity calculations
    - Emission hotspot analysis
    
    Requirements: 2.1, 3.1, 4.1
    """
    
    def __init__(
        self,
        emission_repository: Optional[EmissionRepository] = None,
        business_metrics_repository: Optional[BusinessMetricsRepository] = None
    ):
        """
        Initialize the service with repository dependencies.
        
        Args:
            emission_repository: Repository for emission data access.
                                If None, creates a new instance.
            business_metrics_repository: Repository for business metrics data access.
                                        If None, creates a new instance.
        """
        self.emission_repository = emission_repository or EmissionRepository()
        self.business_metrics_repository = business_metrics_repository or BusinessMetricsRepository()
        
        logger.info("AnalyticsService initialized")

    def get_yoy_emissions(
        self,
        current_year: int,
        previous_year: int
    ) -> Dict[str, Any]:
        """
        Retrieve and compare emissions between two years, grouped by scope.
        Implements Year-over-Year analysis with comparison calculations.
        
        Args:
            current_year: The current year to analyze
            previous_year: The previous year for comparison
            
        Returns:
            Dictionary containing:
                - current_year: Year being analyzed
                - previous_year: Year for comparison
                - current_year_data: List of ScopeEmission objects for current year
                - previous_year_data: List of ScopeEmission objects for previous year
                - comparison: Dictionary with total_current, total_previous,
                             change_percentage, change_absolute
                             
        Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7
        """
        try:
            logger.info(
                f"Retrieving YoY emissions for {current_year} vs {previous_year}"
            )
            
            # Fetch emissions data for both years
            years = [current_year, previous_year]
            emissions_data = self.emission_repository.get_emissions_by_year_and_scope(years)
            
            # Separate data by year
            current_year_emissions = {}
            previous_year_emissions = {}
            
            for record in emissions_data:
                year = record['year']
                scope = record['scope']
                total = float(record['total_emissions']) if record['total_emissions'] else 0.0
                
                if year == current_year:
                    current_year_emissions[scope] = total
                elif year == previous_year:
                    previous_year_emissions[scope] = total
            
            # Format data for all scopes (1, 2, 3)
            current_year_data = []
            previous_year_data = []
            
            for scope in [1, 2, 3]:
                current_year_data.append({
                    'scope': scope,
                    'total_emissions': current_year_emissions.get(scope, 0.0),
                    'unit': 'kgCO2e'
                })
                previous_year_data.append({
                    'scope': scope,
                    'total_emissions': previous_year_emissions.get(scope, 0.0),
                    'unit': 'kgCO2e'
                })
            
            # Calculate totals
            total_current = sum(current_year_emissions.values())
            total_previous = sum(previous_year_emissions.values())
            
            # Calculate comparison metrics
            change_absolute = total_current - total_previous
            
            if total_previous > 0:
                change_percentage = (change_absolute / total_previous) * 100
            else:
                # If previous year has no data, percentage change is undefined
                change_percentage = 0.0 if total_current == 0 else 100.0
            
            comparison = {
                'total_current': total_current,
                'total_previous': total_previous,
                'change_percentage': round(change_percentage, 2),
                'change_absolute': round(change_absolute, 2)
            }
            
            logger.info(
                f"YoY analysis complete: {current_year} total={total_current} kgCO2e, "
                f"{previous_year} total={total_previous} kgCO2e, "
                f"change={change_percentage:.2f}%"
            )
            
            return {
                'current_year': current_year,
                'previous_year': previous_year,
                'current_year_data': current_year_data,
                'previous_year_data': previous_year_data,
                'comparison': comparison
            }
            
        except Exception as e:
            logger.error(f"Error in YoY emissions analysis: {e}")
            raise

    def calculate_emission_intensity(
        self,
        start_date: date,
        end_date: date,
        metric_name: str
    ) -> Dict[str, Any]:
        """
        Calculate emission intensity (kgCO2e per unit of production) for a period.
        Implements division with zero-check protection.
        
        Args:
            start_date: Start of the period
            end_date: End of the period
            metric_name: Name of the business metric to use for intensity calculation
                        (e.g., 'Tons of Steel Produced')
            
        Returns:
            Dictionary containing:
                - period: Dict with start_date and end_date
                - metric_name: Name of the metric used
                - total_emissions: Total emissions in kgCO2e
                - total_production: Total production value
                - production_unit: Unit of production metric
                - intensity: Emission intensity (kgCO2e per unit)
                - intensity_unit: Unit of intensity measurement
                - record_count: Number of emission records included
                
        Raises:
            ValueError: If total production is zero or None (division by zero)
            
        Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7
        """
        try:
            logger.info(
                f"Calculating emission intensity for period {start_date} to {end_date} "
                f"using metric '{metric_name}'"
            )
            
            # Fetch total emissions for the period
            emissions_result = self.emission_repository.get_total_emissions_for_period(
                start_date=start_date,
                end_date=end_date
            )
            
            total_emissions = float(emissions_result['total_emissions']) if emissions_result['total_emissions'] else 0.0
            record_count = emissions_result['record_count']
            
            # Fetch total production for the period
            production_result = self.business_metrics_repository.get_metric_total_for_period(
                metric_name=metric_name,
                start_date=start_date,
                end_date=end_date
            )
            
            # Check if production data exists
            if production_result is None or production_result['total_value'] is None:
                logger.error(
                    f"No production data found for metric '{metric_name}' "
                    f"in period {start_date} to {end_date}"
                )
                raise NoProductionDataException(
                    metric_name=metric_name,
                    start_date=str(start_date),
                    end_date=str(end_date)
                )
            
            total_production = float(production_result['total_value'])
            production_unit = production_result['unit']
            
            # Zero-check protection
            if total_production == 0:
                logger.error(
                    f"Total production is zero for metric '{metric_name}' "
                    f"in period {start_date} to {end_date}"
                )
                raise NoProductionDataException(
                    metric_name=metric_name,
                    start_date=str(start_date),
                    end_date=str(end_date),
                    details={'reason': 'Total production value is zero'}
                )
            
            # Calculate intensity
            intensity = total_emissions / total_production
            intensity_unit = f"kgCO2e per {production_unit}"
            
            logger.info(
                f"Emission intensity calculated: {intensity:.4f} {intensity_unit} "
                f"({total_emissions} kgCO2e / {total_production} {production_unit})"
            )
            
            return {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'metric_name': metric_name,
                'total_emissions': round(total_emissions, 2),
                'total_production': round(total_production, 2),
                'production_unit': production_unit,
                'intensity': round(intensity, 4),
                'intensity_unit': intensity_unit,
                'record_count': record_count
            }
            
        except NoProductionDataException:
            # Re-raise custom exception for proper error handling
            raise
        except Exception as e:
            logger.error(f"Error calculating emission intensity: {e}")
            raise

    def get_emission_hotspots(
        self,
        filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Identify emission hotspots by analyzing which sources contribute most
        to total emissions. Calculates percentage contributions and sorts by
        total emissions in descending order.
        
        Args:
            filters: Dictionary containing optional filters:
                - start_date: Filter start date (optional)
                - end_date: Filter end date (optional)
                - scope: Filter by scope 1, 2, or 3 (optional)
                - limit: Maximum number of results (default: 10)
                
        Returns:
            Dictionary containing:
                - period: Dict with applied filters
                - total_emissions: Total emissions across all sources
                - hotspots: List of hotspot items with activity_name, scope,
                           total_emissions, percentage, record_count, average_per_record
                           
        Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8
        """
        try:
            logger.info(f"Analyzing emission hotspots with filters: {filters}")
            
            # Fetch emissions grouped by source
            hotspot_data = self.emission_repository.get_emissions_by_source(filters)
            
            # Calculate total emissions across all sources
            total_emissions = sum(
                float(item['total_emissions']) for item in hotspot_data
            )
            
            # Calculate percentage contribution for each source
            hotspots = []
            for item in hotspot_data:
                source_emissions = float(item['total_emissions'])
                
                # Calculate percentage (handle zero total emissions)
                if total_emissions > 0:
                    percentage = (source_emissions / total_emissions) * 100
                else:
                    percentage = 0.0
                
                hotspots.append({
                    'activity_name': item['activity_name'],
                    'scope': item['scope'],
                    'total_emissions': round(source_emissions, 2),
                    'percentage': round(percentage, 2),
                    'record_count': item['record_count'],
                    'average_per_record': round(float(item['average_per_record']), 2)
                })
            
            # Build period information
            period = {}
            if filters.get('start_date'):
                period['start_date'] = filters['start_date'].isoformat() if hasattr(filters['start_date'], 'isoformat') else str(filters['start_date'])
            if filters.get('end_date'):
                period['end_date'] = filters['end_date'].isoformat() if hasattr(filters['end_date'], 'isoformat') else str(filters['end_date'])
            if filters.get('scope'):
                period['scope'] = filters['scope']
            if filters.get('limit'):
                period['limit'] = filters['limit']
            
            logger.info(
                f"Hotspot analysis complete: {len(hotspots)} sources identified, "
                f"total emissions={total_emissions:.2f} kgCO2e"
            )
            
            return {
                'period': period,
                'total_emissions': round(total_emissions, 2),
                'hotspots': hotspots
            }
            
        except Exception as e:
            logger.error(f"Error analyzing emission hotspots: {e}")
            raise
