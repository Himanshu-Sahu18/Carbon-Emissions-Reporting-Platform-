"""
Example Integration Tests
Demonstrates usage of test fixtures and helper functions
"""
import pytest
from datetime import date
from psycopg2.extensions import connection as Connection

from conftest import (
    seed_emission_factors,
    seed_business_metrics,
    get_valid_factor_id,
    create_emission_record_with_factor
)


class TestDatabaseSetup:
    """Test that database setup is working correctly"""
    
    def test_database_connection(self, db_connection: Connection):
        """Test basic database connectivity"""
        cursor = db_connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1
        cursor.close()
    
    def test_tables_exist(self, db_connection: Connection):
        """Test that all required tables exist"""
        cursor = db_connection.cursor()
        
        required_tables = [
            'emission_factors',
            'emission_records',
            'business_metrics',
            'audit_log'
        ]
        
        for table in required_tables:
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                )
            """)
            exists = cursor.fetchone()[0]
            assert exists, f"Table {table} does not exist"
        
        cursor.close()


class TestEmissionFactorFixtures:
    """Test emission factor fixtures and seeding"""
    
    def test_sample_emission_factors_structure(self, sample_emission_factors):
        """Test that sample emission factors have correct structure"""
        assert len(sample_emission_factors) > 0
        
        # Check first factor has all required fields
        factor = sample_emission_factors[0]
        required_fields = [
            'activity_name', 'scope', 'activity_unit', 
            'co2e_per_unit', 'source', 'valid_from', 
            'valid_to', 'created_by'
        ]
        
        for field in required_fields:
            assert field in factor
    
    def test_seed_emission_factors(self, db_connection: Connection, clean_database, sample_emission_factors):
        """Test seeding emission factors into database"""
        factor_ids = seed_emission_factors(db_connection, sample_emission_factors)
        
        assert len(factor_ids) == len(sample_emission_factors)
        
        # Verify factors were inserted
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM emission_factors")
        count = cursor.fetchone()[0]
        assert count == len(sample_emission_factors)
        cursor.close()
    
    def test_db_with_factors_fixture(self, db_with_factors: Connection):
        """Test the db_with_factors composite fixture"""
        cursor = db_with_factors.cursor()
        cursor.execute("SELECT COUNT(*) FROM emission_factors")
        count = cursor.fetchone()[0]
        assert count > 0
        cursor.close()


class TestBusinessMetricFixtures:
    """Test business metric fixtures and seeding"""
    
    def test_sample_business_metrics_structure(self, sample_business_metrics):
        """Test that sample business metrics have correct structure"""
        assert len(sample_business_metrics) > 0
        
        metric = sample_business_metrics[0]
        required_fields = [
            'metric_name', 'metric_category', 'value', 
            'unit', 'metric_date', 'reporting_period', 'created_by'
        ]
        
        for field in required_fields:
            assert field in metric
    
    def test_seed_business_metrics(self, db_connection: Connection, clean_database, sample_business_metrics):
        """Test seeding business metrics into database"""
        metric_ids = seed_business_metrics(db_connection, sample_business_metrics)
        
        assert len(metric_ids) == len(sample_business_metrics)
        
        # Verify metrics were inserted
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM business_metrics")
        count = cursor.fetchone()[0]
        assert count == len(sample_business_metrics)
        cursor.close()


class TestHistoricalAccuracy:
    """Test historical accuracy of emission factor selection"""
    
    def test_get_valid_factor_for_2023(self, db_with_factors: Connection):
        """Test getting valid factor for 2023 date"""
        factor_id = get_valid_factor_id(
            db_with_factors,
            "Diesel",
            1,
            date(2023, 6, 15)
        )
        
        # Verify we got a factor
        assert factor_id is not None
        
        # Verify it's the 2023 factor (co2e_per_unit = 2.71)
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT co2e_per_unit, valid_from, valid_to
            FROM emission_factors
            WHERE factor_id = %s
        """, (factor_id,))
        
        result = cursor.fetchone()
        assert result[0] == 2.71
        assert result[1] == date(2023, 1, 1)
        assert result[2] == date(2023, 12, 31)
        cursor.close()
    
    def test_get_valid_factor_for_2024(self, db_with_factors: Connection):
        """Test getting valid factor for 2024 date"""
        factor_id = get_valid_factor_id(
            db_with_factors,
            "Diesel",
            1,
            date(2024, 6, 15)
        )
        
        # Verify it's the 2024 factor (co2e_per_unit = 2.73)
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT co2e_per_unit, valid_from, valid_to
            FROM emission_factors
            WHERE factor_id = %s
        """, (factor_id,))
        
        result = cursor.fetchone()
        assert result[0] == 2.73
        assert result[1] == date(2024, 1, 1)
        assert result[2] is None  # Currently active
        cursor.close()
    
    def test_get_valid_factor_for_2022(self, db_with_factors: Connection):
        """Test getting valid factor for 2022 date"""
        factor_id = get_valid_factor_id(
            db_with_factors,
            "Diesel",
            1,
            date(2022, 6, 15)
        )
        
        # Verify it's the 2022 factor (co2e_per_unit = 2.68)
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT co2e_per_unit, valid_from, valid_to
            FROM emission_factors
            WHERE factor_id = %s
        """, (factor_id,))
        
        result = cursor.fetchone()
        assert result[0] == 2.68
        assert result[1] == date(2022, 1, 1)
        assert result[2] == date(2022, 12, 31)
        cursor.close()
    
    def test_factor_not_found_raises_error(self, db_with_factors: Connection):
        """Test that looking up non-existent factor raises error"""
        with pytest.raises(ValueError, match="No valid emission factor found"):
            get_valid_factor_id(
                db_with_factors,
                "NonExistentFuel",
                1,
                date(2024, 1, 1)
            )
    
    def test_boundary_date_valid_from(self, db_with_factors: Connection):
        """Test factor lookup on valid_from boundary date"""
        # Should return the factor that starts on this date
        factor_id = get_valid_factor_id(
            db_with_factors,
            "Diesel",
            1,
            date(2024, 1, 1)  # Exact valid_from date
        )
        
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT co2e_per_unit
            FROM emission_factors
            WHERE factor_id = %s
        """, (factor_id,))
        
        result = cursor.fetchone()
        assert result[0] == 2.73  # 2024 factor
        cursor.close()
    
    def test_boundary_date_valid_to(self, db_with_factors: Connection):
        """Test factor lookup on valid_to boundary date"""
        # Should return the factor that ends on this date
        factor_id = get_valid_factor_id(
            db_with_factors,
            "Diesel",
            1,
            date(2023, 12, 31)  # Exact valid_to date
        )
        
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT co2e_per_unit
            FROM emission_factors
            WHERE factor_id = %s
        """, (factor_id,))
        
        result = cursor.fetchone()
        assert result[0] == 2.71  # 2023 factor
        cursor.close()


class TestEmissionRecordCreation:
    """Test emission record creation with automatic factor lookup"""
    
    def test_create_emission_record_2023(self, db_with_factors: Connection):
        """Test creating emission record for 2023"""
        record_id = create_emission_record_with_factor(
            db_with_factors,
            activity_date=date(2023, 6, 15),
            activity_name="Diesel",
            scope=1,
            activity_value=1000.0,
            activity_unit="litres",
            location="Plant A",
            department="Operations"
        )
        
        assert record_id is not None
        
        # Verify the record was created with correct calculation
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT calculated_co2e, factor_id, activity_value
            FROM emission_records
            WHERE record_id = %s
        """, (record_id,))
        
        result = cursor.fetchone()
        assert result[0] == 2710.0  # 1000 * 2.71
        assert result[2] == 1000.0
        
        # Verify correct factor was used
        cursor.execute("""
            SELECT co2e_per_unit
            FROM emission_factors
            WHERE factor_id = %s
        """, (result[1],))
        
        factor_result = cursor.fetchone()
        assert factor_result[0] == 2.71
        cursor.close()
    
    def test_create_emission_record_2024(self, db_with_factors: Connection):
        """Test creating emission record for 2024"""
        record_id = create_emission_record_with_factor(
            db_with_factors,
            activity_date=date(2024, 6, 15),
            activity_name="Diesel",
            scope=1,
            activity_value=1000.0,
            activity_unit="litres"
        )
        
        # Verify the record was created with 2024 factor
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT calculated_co2e
            FROM emission_records
            WHERE record_id = %s
        """, (record_id,))
        
        result = cursor.fetchone()
        assert result[0] == 2730.0  # 1000 * 2.73
        cursor.close()
    
    def test_create_records_different_years_use_different_factors(self, db_with_factors: Connection):
        """Test that records from different years use different factors"""
        # Create record in 2023
        record_id_2023 = create_emission_record_with_factor(
            db_with_factors,
            activity_date=date(2023, 6, 15),
            activity_name="Diesel",
            scope=1,
            activity_value=1000.0,
            activity_unit="litres"
        )
        
        # Create record in 2024
        record_id_2024 = create_emission_record_with_factor(
            db_with_factors,
            activity_date=date(2024, 6, 15),
            activity_name="Diesel",
            scope=1,
            activity_value=1000.0,
            activity_unit="litres"
        )
        
        # Verify different factors were used
        cursor = db_with_factors.cursor()
        cursor.execute("""
            SELECT calculated_co2e, factor_id
            FROM emission_records
            WHERE record_id IN (%s, %s)
            ORDER BY activity_date
        """, (record_id_2023, record_id_2024))
        
        results = cursor.fetchall()
        
        # Different calculations
        assert results[0][0] == 2710.0  # 2023: 1000 * 2.71
        assert results[1][0] == 2730.0  # 2024: 1000 * 2.73
        
        # Different factor_ids
        assert results[0][1] != results[1][1]
        cursor.close()
    
    def test_unit_mismatch_raises_error(self, db_with_factors: Connection):
        """Test that unit mismatch raises error"""
        with pytest.raises(ValueError, match="Unit mismatch"):
            create_emission_record_with_factor(
                db_with_factors,
                activity_date=date(2024, 1, 15),
                activity_name="Diesel",
                scope=1,
                activity_value=1000.0,
                activity_unit="kg"  # Wrong unit, should be litres
            )


class TestFullTestDataFixture:
    """Test the db_with_full_test_data composite fixture"""
    
    def test_full_data_has_factors(self, db_with_full_test_data: Connection):
        """Test that full data fixture includes emission factors"""
        cursor = db_with_full_test_data.cursor()
        cursor.execute("SELECT COUNT(*) FROM emission_factors")
        count = cursor.fetchone()[0]
        assert count > 0
        cursor.close()
    
    def test_full_data_has_metrics(self, db_with_full_test_data: Connection):
        """Test that full data fixture includes business metrics"""
        cursor = db_with_full_test_data.cursor()
        cursor.execute("SELECT COUNT(*) FROM business_metrics")
        count = cursor.fetchone()[0]
        assert count > 0
        cursor.close()
    
    def test_full_data_has_emission_records(self, db_with_full_test_data: Connection):
        """Test that full data fixture includes emission records"""
        cursor = db_with_full_test_data.cursor()
        cursor.execute("SELECT COUNT(*) FROM emission_records")
        count = cursor.fetchone()[0]
        assert count > 0
        cursor.close()
    
    def test_full_data_spans_multiple_years(self, db_with_full_test_data: Connection):
        """Test that emission records span multiple years"""
        cursor = db_with_full_test_data.cursor()
        cursor.execute("""
            SELECT DISTINCT EXTRACT(YEAR FROM activity_date) as year
            FROM emission_records
            ORDER BY year
        """)
        years = [row[0] for row in cursor.fetchall()]
        
        assert len(years) >= 2
        assert 2023 in years
        assert 2024 in years
        cursor.close()
    
    def test_full_data_has_multiple_scopes(self, db_with_full_test_data: Connection):
        """Test that emission records include multiple scopes"""
        cursor = db_with_full_test_data.cursor()
        cursor.execute("""
            SELECT DISTINCT scope
            FROM emission_records
            ORDER BY scope
        """)
        scopes = [row[0] for row in cursor.fetchall()]
        
        assert len(scopes) >= 2
        cursor.close()
    
    def test_historical_accuracy_in_full_data(self, db_with_full_test_data: Connection):
        """Test that full data demonstrates historical accuracy"""
        cursor = db_with_full_test_data.cursor()
        
        # Get Diesel records from 2023 and 2024
        cursor.execute("""
            SELECT 
                er.activity_date,
                er.activity_value,
                er.calculated_co2e,
                ef.co2e_per_unit,
                ef.valid_from,
                ef.valid_to
            FROM emission_records er
            JOIN emission_factors ef ON er.factor_id = ef.factor_id
            WHERE er.activity_name = 'Diesel'
            ORDER BY er.activity_date
        """)
        
        records = cursor.fetchall()
        
        # Should have records from both years
        assert len(records) >= 2
        
        # Verify 2023 records use 2023 factor
        records_2023 = [r for r in records if r[0].year == 2023]
        for record in records_2023:
            assert record[3] == 2.71  # 2023 factor
        
        # Verify 2024 records use 2024 factor
        records_2024 = [r for r in records if r[0].year == 2024]
        for record in records_2024:
            assert record[3] == 2.73  # 2024 factor
        
        cursor.close()


class TestCleanDatabase:
    """Test that clean_database fixture works correctly"""
    
    def test_clean_database_removes_all_data(self, db_connection: Connection, clean_database, sample_emission_factors):
        """Test that clean_database truncates all tables"""
        # Insert some data
        seed_emission_factors(db_connection, sample_emission_factors)
        
        # Verify data exists
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM emission_factors")
        count_before = cursor.fetchone()[0]
        assert count_before > 0
        
        # Clean database (this happens automatically with the fixture)
        cursor.execute("TRUNCATE TABLE emission_factors RESTART IDENTITY CASCADE")
        db_connection.commit()
        
        # Verify data is gone
        cursor.execute("SELECT COUNT(*) FROM emission_factors")
        count_after = cursor.fetchone()[0]
        assert count_after == 0
        cursor.close()
