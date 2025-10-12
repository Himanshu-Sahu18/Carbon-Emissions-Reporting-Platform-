"""
Emission Calculation Service Module
Handles emission calculations with historical accuracy
"""
import logging
from datetime import date
from typing import Dict, Any, Optional

from app.repositories.emission_repository import EmissionRepository
from app.exceptions import FactorNotFoundException

logger = logging.getLogger(__name__)


class EmissionCalculationService:
    """
    Service for calculating emissions with historical accuracy.
    Ensures that emissions are calculated using the factor that was valid
    on the activity date, maintaining data integrity and auditability.
    
    Requirements: 1.3, 1.4, 1.5, 1.6
    """
    
    def __init__(self, emission_repository: Optional[EmissionRepository] = None):
        """
        Initialize the service with repository dependency.
        
        Args:
            emission_repository: Repository for emission data access.
                                If None, creates a new instance.
        """
        self.emission_repository = emission_repository or EmissionRepository()
    
    def get_valid_factor(
        self, 
        activity_name: str, 
        scope: int, 
        activity_date: date
    ) -> Dict[str, Any]:
        """
        Retrieve the emission factor that was valid on a specific date.
        Implements historical accuracy by querying for factors based on
        their validity period.
        
        Args:
            activity_name: Name of the activity (e.g., 'Diesel', 'Grid Electricity')
            scope: GHG Protocol scope (1, 2, or 3)
            activity_date: The date the activity occurred
            
        Returns:
            Dictionary containing factor details:
                - factor_id: Unique identifier for the factor
                - co2e_per_unit: CO2 equivalent per unit of activity
                - activity_unit: Unit of measurement (e.g., 'litres', 'kWh')
                - source: Source of the emission factor
                - valid_from: Start date of factor validity
                - valid_to: End date of factor validity (or None if current)
                
        Raises:
            FactorNotFoundException: If no valid factor exists for the given parameters
            Exception: For database or other unexpected errors
            
        Requirements: 1.3, 1.4, 1.5, 1.6
        """
        try:
            logger.debug(
                f"Retrieving emission factor for {activity_name} "
                f"(scope {scope}) on {activity_date}"
            )
            
            factor = self.emission_repository.get_valid_factor(
                activity_name=activity_name,
                scope=scope,
                activity_date=activity_date
            )
            
            if factor is None:
                logger.warning(
                    f"Factor not found: {activity_name} (scope {scope}) "
                    f"on {activity_date}"
                )
                raise FactorNotFoundException(
                    activity_name=activity_name,
                    scope=scope,
                    activity_date=str(activity_date)
                )
            
            logger.info(
                f"Found emission factor {factor['factor_id']} for {activity_name} "
                f"(scope {scope}) on {activity_date}: "
                f"{factor['co2e_per_unit']} kgCO2e per {factor['activity_unit']}"
            )
            
            return factor
            
        except FactorNotFoundException:
            # Re-raise custom exception
            raise
        except Exception as e:
            logger.error(
                f"Error retrieving emission factor for {activity_name} "
                f"(scope {scope}) on {activity_date}: {e}"
            )
            raise
    
    def calculate_emission(
        self, 
        activity_value: float, 
        factor: Dict[str, Any]
    ) -> float:
        """
        Calculate CO2 equivalent emissions for an activity.
        
        Args:
            activity_value: Quantity of the activity (e.g., 1000 litres, 500 kWh)
            factor: Emission factor dictionary containing 'co2e_per_unit'
            
        Returns:
            Calculated CO2 equivalent in kgCO2e
            
        Raises:
            ValueError: If activity_value is negative or factor is invalid
            KeyError: If factor dictionary is missing required keys
            
        Requirements: 1.5, 1.6
        """
        try:
            # Validate inputs
            if activity_value < 0:
                raise ValueError(
                    f"Activity value cannot be negative: {activity_value}"
                )
            
            if 'co2e_per_unit' not in factor:
                raise KeyError(
                    "Factor dictionary missing required key 'co2e_per_unit'"
                )
            
            co2e_per_unit = factor['co2e_per_unit']
            
            if co2e_per_unit < 0:
                raise ValueError(
                    f"Emission factor cannot be negative: {co2e_per_unit}"
                )
            
            # Calculate emissions
            calculated_co2e = activity_value * co2e_per_unit
            
            logger.debug(
                f"Calculated emission: {activity_value} × {co2e_per_unit} = "
                f"{calculated_co2e} kgCO2e"
            )
            
            return calculated_co2e
            
        except (ValueError, KeyError) as e:
            logger.error(f"Error calculating emission: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calculating emission: {e}")
            raise
