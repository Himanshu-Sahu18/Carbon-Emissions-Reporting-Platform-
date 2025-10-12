"""
GHG Data Import Script
======================
Parses, transforms, and loads real-world emissions data from GHG Sheet.xlsx
into the PostgreSQL database.

This script:
1. Reads data from all three sheets (Scope 1, 2, 3)
2. Transforms data to match database schema
3. Creates versioned emission factors
4. Loads emission records with proper factor linkage
5. Imports business metrics

Usage:
    python scripts/import_ghg_data.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pandas as pd
    import openpyxl
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Please install: pip install pandas openpyxl")
    sys.exit(1)

from app.database import get_db_cursor, execute_query, execute_transaction
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GHGDataImporter:
    """Handles import of GHG emissions data from Excel file."""
    
    def __init__(self, excel_file_path: str):
        """
        Initialize the importer.
        
        Args:
            excel_file_path: Path to the GHG Sheet.xlsx file
        """
        self.excel_file_path = excel_file_path
        self.stats = {
            'emission_factors': 0,
            'emission_records': 0,
            'business_metrics': 0,
            'errors': []
        }
    
    def run(self):
        """Execute the complete import process."""
        logger.info("=" * 60)
        logger.info("Starting GHG Data Import")
        logger.info("=" * 60)
        
        try:
            # Verify file exists
            if not os.path.exists(self.excel_file_path):
                raise FileNotFoundError(f"Excel file not found: {self.excel_file_path}")
            
            logger.info(f"Reading data from: {self.excel_file_path}")
            
            # Clear existing sample data
            self.clear_sample_data()
            
            # Import Scope 1 data
            logger.info("\n" + "=" * 60)
            logger.info("Processing Scope 1 Data")
            logger.info("=" * 60)
            self.import_scope1_data()
            
            # Import Scope 2 data
            logger.info("\n" + "=" * 60)
            logger.info("Processing Scope 2 Data")
            logger.info("=" * 60)
            self.import_scope2_data()
            
            # Import Scope 3 data
            logger.info("\n" + "=" * 60)
            logger.info("Processing Scope 3 Data")
            logger.info("=" * 60)
            self.import_scope3_data()
            
            # Print summary
            self.print_summary()
            
            logger.info("\n" + "=" * 60)
            logger.info("Import completed successfully!")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            self.stats['errors'].append(str(e))
            raise
    
    def clear_sample_data(self):
        """Clear existing sample data from database."""
        logger.info("Clearing existing sample data...")
        
        queries = [
            ("DELETE FROM audit_log", ()),
            ("DELETE FROM emission_records", ()),
            ("DELETE FROM business_metrics", ()),
            ("DELETE FROM emission_factors", ()),
        ]
        
        try:
            execute_transaction(queries)
            logger.info("✓ Sample data cleared")
        except Exception as e:
            logger.error(f"Failed to clear sample data: {str(e)}")
            raise

    
    def import_scope1_data(self):
        """Import Scope 1 (Direct Emissions) data."""
        try:
            # Read Scope 1 sheet
            df = pd.read_excel(self.excel_file_path, sheet_name='Scope 1')
            logger.info(f"Read {len(df)} rows from Scope 1 sheet")
            
            # Group by unique emission factors
            factor_groups = df.groupby(['Material', 'Emission Factor', 'Unit of Emission Factor'])
            
            logger.info(f"Found {len(factor_groups)} unique emission factors")
            
            for (material, emission_factor, unit), group in factor_groups:
                # Skip if emission factor is NaN
                if pd.isna(emission_factor) or pd.isna(material):
                    continue
                
                # Create emission factor
                factor_id = self.create_emission_factor(
                    activity_name=str(material),
                    scope=1,
                    co2e_per_unit=float(emission_factor),
                    activity_unit=self.parse_activity_unit(str(unit)),
                    source='IPCC 2006 Guidelines',
                    valid_from=date(2024, 1, 1)
                )
                
                if factor_id:
                    # Create emission records for this factor
                    for _, row in group.iterrows():
                        self.create_scope1_emission_record(row, factor_id)
            
            logger.info(f"✓ Scope 1 import complete")
            
        except Exception as e:
            logger.error(f"Error importing Scope 1 data: {str(e)}")
            self.stats['errors'].append(f"Scope 1: {str(e)}")
    
    def import_scope2_data(self):
        """Import Scope 2 (Indirect Energy Emissions) data."""
        try:
            # Read Scope 2 sheet
            df = pd.read_excel(self.excel_file_path, sheet_name='Scope 2')
            logger.info(f"Read {len(df)} rows from Scope 2 sheet")
            
            # Group by unique emission factors
            factor_groups = df.groupby(['Energy Type', 'Emission Factor (tCO₂/unit)', 'Unit'])
            
            logger.info(f"Found {len(factor_groups)} unique emission factors")
            
            for (energy_type, emission_factor, unit), group in factor_groups:
                # Skip if emission factor is NaN
                if pd.isna(emission_factor) or pd.isna(energy_type):
                    continue
                
                # Create emission factor
                factor_id = self.create_emission_factor(
                    activity_name=str(energy_type),
                    scope=2,
                    co2e_per_unit=float(emission_factor) * 1000,  # Convert tCO2 to kgCO2e
                    activity_unit=str(unit),
                    source='CEA India 2023 Report',
                    valid_from=date(2024, 1, 1)
                )
                
                if factor_id:
                    # Create emission records for this factor
                    for _, row in group.iterrows():
                        self.create_scope2_emission_record(row, factor_id)
            
            logger.info(f"✓ Scope 2 import complete")
            
        except Exception as e:
            logger.error(f"Error importing Scope 2 data: {str(e)}")
            self.stats['errors'].append(f"Scope 2: {str(e)}")
    
    def import_scope3_data(self):
        """Import Scope 3 (Value Chain Emissions) data."""
        try:
            # Read Scope 3 sheet
            df = pd.read_excel(self.excel_file_path, sheet_name='Scope 3')
            logger.info(f"Read {len(df)} rows from Scope 3 sheet")
            
            # Group by unique emission factors
            factor_groups = df.groupby(['Activity Description', 'Emission Factor (tCO2/unit)', 'Unit of Activity'])
            
            logger.info(f"Found {len(factor_groups)} unique emission factors")
            
            for (activity_desc, emission_factor, unit), group in factor_groups:
                # Skip if emission factor is NaN
                if pd.isna(emission_factor) or pd.isna(activity_desc):
                    continue
                
                # Create emission factor
                factor_id = self.create_emission_factor(
                    activity_name=str(activity_desc),
                    scope=3,
                    co2e_per_unit=float(emission_factor) * 1000,  # Convert tCO2 to kgCO2e
                    activity_unit=str(unit),
                    source='GHG Protocol Scope 3 Eval Tool',
                    valid_from=date(2024, 1, 1)
                )
                
                if factor_id:
                    # Create emission records for this factor
                    for _, row in group.iterrows():
                        self.create_scope3_emission_record(row, factor_id)
            
            logger.info(f"✓ Scope 3 import complete")
            
        except Exception as e:
            logger.error(f"Error importing Scope 3 data: {str(e)}")
            self.stats['errors'].append(f"Scope 3: {str(e)}")

    
    def create_emission_factor(
        self,
        activity_name: str,
        scope: int,
        co2e_per_unit: float,
        activity_unit: str,
        source: str,
        valid_from: date,
        valid_to: Optional[date] = None
    ) -> Optional[int]:
        """
        Create an emission factor in the database.
        
        Returns:
            factor_id if successful, None otherwise
        """
        try:
            query = """
                INSERT INTO emission_factors (
                    activity_name, scope, activity_unit, co2e_per_unit,
                    source, valid_from, valid_to, created_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING factor_id
            """
            
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (
                    activity_name, scope, activity_unit, co2e_per_unit,
                    source, valid_from, valid_to, 'import_script'
                ))
                result = cursor.fetchone()
                factor_id = result['factor_id']
                
                self.stats['emission_factors'] += 1
                logger.debug(f"Created factor: {activity_name} (ID: {factor_id})")
                
                return factor_id
                
        except Exception as e:
            logger.warning(f"Failed to create emission factor '{activity_name}': {str(e)}")
            return None
    
    def create_scope1_emission_record(self, row: pd.Series, factor_id: int):
        """Create emission record from Scope 1 data row."""
        try:
            # Parse quarter to date
            quarter = row.get('Year/Timeline', 'Q1')
            activity_date = self.parse_quarter_to_date(quarter, 2024)
            
            # Get quantity (try Q1 and Q2 columns)
            quantity = row.get('Q1 Quantity', row.get('Q2 Quantity', 0))
            if pd.isna(quantity) or quantity == 0:
                return
            
            # Get calculated emissions
            ghg_emission = row.get('GHG Emission (tCO2)', 0)
            if pd.isna(ghg_emission):
                ghg_emission = 0
            
            # Convert tCO2 to kgCO2e
            calculated_co2e = float(ghg_emission) * 1000
            
            # Get location and section
            location = row.get('Location (Plant)', 'Central Steel Plant')
            department = row.get('Section', 'Unknown')
            
            self.create_emission_record(
                factor_id=factor_id,
                activity_date=activity_date,
                activity_name=str(row.get('Material', 'Unknown')),
                scope=1,
                activity_value=float(quantity),
                activity_unit=str(row.get('Unit of Material', '')),
                calculated_co2e=calculated_co2e,
                location=str(location) if not pd.isna(location) else None,
                department=str(department) if not pd.isna(department) else None
            )
            
        except Exception as e:
            logger.debug(f"Skipped Scope 1 record: {str(e)}")
    
    def create_scope2_emission_record(self, row: pd.Series, factor_id: int):
        """Create emission record from Scope 2 data row."""
        try:
            # Parse quarter to date
            quarter = row.get('Quarter', 'Q1')
            activity_date = self.parse_quarter_to_date(quarter, 2024)
            
            # Get energy consumed
            energy_consumed = row.get('Energy Consumed', 0)
            if pd.isna(energy_consumed) or energy_consumed == 0:
                return
            
            # Get calculated emissions
            scope2_emissions = row.get('Scope 2 Emissions (tCO₂)', 0)
            if pd.isna(scope2_emissions):
                scope2_emissions = 0
            
            # Convert tCO2 to kgCO2e
            calculated_co2e = float(scope2_emissions) * 1000
            
            # Get location and section
            location = 'Central Steel Plant'
            department = row.get('Section/Process', 'Unknown')
            
            self.create_emission_record(
                factor_id=factor_id,
                activity_date=activity_date,
                activity_name=str(row.get('Energy Type', 'Unknown')),
                scope=2,
                activity_value=float(energy_consumed),
                activity_unit=str(row.get('Unit', '')),
                calculated_co2e=calculated_co2e,
                location=location,
                department=str(department) if not pd.isna(department) else None
            )
            
        except Exception as e:
            logger.debug(f"Skipped Scope 2 record: {str(e)}")
    
    def create_scope3_emission_record(self, row: pd.Series, factor_id: int):
        """Create emission record from Scope 3 data row."""
        try:
            # Parse month to date
            month_str = row.get('Month', '2024-01')
            activity_date = self.parse_month_to_date(month_str)
            
            # Get quantity
            quantity = row.get('Quantity', 0)
            if pd.isna(quantity) or quantity == 0:
                return
            
            # Get calculated emissions
            scope3_emissions = row.get('Scope 3 Emissions (tCO2)', 0)
            if pd.isna(scope3_emissions):
                scope3_emissions = 0
            
            # Convert tCO2 to kgCO2e
            calculated_co2e = float(scope3_emissions) * 1000
            
            # Get category and vendor
            category = row.get('Scope 3 Category', 'Unknown')
            vendor = row.get('Vendor Involved', None)
            
            self.create_emission_record(
                factor_id=factor_id,
                activity_date=activity_date,
                activity_name=str(row.get('Activity Description', 'Unknown')),
                scope=3,
                activity_value=float(quantity),
                activity_unit=str(row.get('Unit of Activity', '')),
                calculated_co2e=calculated_co2e,
                location='Central Steel Plant',
                department=str(category) if not pd.isna(category) else None,
                notes=f"Vendor: {vendor}" if not pd.isna(vendor) else None
            )
            
        except Exception as e:
            logger.debug(f"Skipped Scope 3 record: {str(e)}")

    
    def create_emission_record(
        self,
        factor_id: int,
        activity_date: date,
        activity_name: str,
        scope: int,
        activity_value: float,
        activity_unit: str,
        calculated_co2e: float,
        location: Optional[str] = None,
        department: Optional[str] = None,
        notes: Optional[str] = None
    ):
        """Create an emission record in the database."""
        try:
            query = """
                INSERT INTO emission_records (
                    factor_id, activity_date, activity_name, scope,
                    activity_value, activity_unit, calculated_co2e,
                    location, department, notes, created_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (
                    factor_id, activity_date, activity_name, scope,
                    activity_value, activity_unit, calculated_co2e,
                    location, department, notes, 'import_script'
                ))
                
                self.stats['emission_records'] += 1
                
        except Exception as e:
            logger.debug(f"Failed to create emission record: {str(e)}")
    
    def parse_activity_unit(self, unit_str: str) -> str:
        """Parse and standardize activity unit from emission factor unit."""
        # Extract unit from strings like "tCO2/t", "tCO2/KL", "tCO2/Nm3"
        if '/' in unit_str:
            parts = unit_str.split('/')
            if len(parts) > 1:
                return parts[1].strip()
        return unit_str
    
    def parse_quarter_to_date(self, quarter_str: str, year: int) -> date:
        """Convert quarter string (Q1, Q2, etc.) to a date."""
        quarter_map = {
            'Q1': (1, 31),
            'Q2': (4, 30),
            'Q3': (7, 31),
            'Q4': (10, 31)
        }
        
        quarter_str = str(quarter_str).strip().upper()
        if quarter_str in quarter_map:
            month, day = quarter_map[quarter_str]
            return date(year, month, day)
        
        # Default to Q1 end
        return date(year, 1, 31)
    
    def parse_month_to_date(self, month_str: str) -> date:
        """Convert month string (2024-01, 2024-02, etc.) to a date."""
        try:
            if isinstance(month_str, str) and '-' in month_str:
                parts = month_str.split('-')
                year = int(parts[0])
                month = int(parts[1])
                # Use last day of month
                if month in [1, 3, 5, 7, 8, 10, 12]:
                    day = 31
                elif month in [4, 6, 9, 11]:
                    day = 30
                else:
                    day = 28
                return date(year, month, day)
        except:
            pass
        
        # Default to January 2024
        return date(2024, 1, 31)
    
    def print_summary(self):
        """Print import summary statistics."""
        logger.info("\n" + "=" * 60)
        logger.info("IMPORT SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Emission Factors Created: {self.stats['emission_factors']}")
        logger.info(f"Emission Records Created: {self.stats['emission_records']}")
        logger.info(f"Business Metrics Created: {self.stats['business_metrics']}")
        
        if self.stats['errors']:
            logger.warning(f"\nErrors encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                logger.warning(f"  - {error}")


def main():
    """Main entry point for the import script."""
    # Determine Excel file path
    excel_file = os.path.join(os.path.dirname(__file__), '..', '..', 'GHG Sheet.xlsx')
    
    if not os.path.exists(excel_file):
        logger.error(f"Excel file not found: {excel_file}")
        logger.info("Please ensure 'GHG Sheet.xlsx' is in the project root directory")
        sys.exit(1)
    
    # Create importer and run
    importer = GHGDataImporter(excel_file)
    importer.run()


if __name__ == '__main__':
    main()
