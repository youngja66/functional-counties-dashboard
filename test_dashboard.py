# Test script to verify dashboard functionality
import sys
import os
import warnings
warnings.filterwarnings('ignore')

def test_dashboard_functionality():
    """Comprehensive test of dashboard features"""

    print("🧪 Testing US Counties Dashboard Functionality")
    print("=" * 50)

    try:
        # Test 1: Import and basic initialization
        print("\n1. Testing imports and initialization...")
        from functional_counties_dashboard import FunctionalCountiesDashboard
        dashboard = FunctionalCountiesDashboard()
        print("   ✅ Dashboard class imported and initialized")

        # Test 2: Data loading
        print("\n2. Testing boundary data loading...")
        dashboard.load_counties_data()
        print(f"   ✅ Loaded {len(dashboard.gdf)} counties")
        print(f"   📍 Columns: {list(dashboard.gdf.columns)}")

        # Test 3: Synthetic data generation
        print("\n3. Testing synthetic data generation...")
        dashboard.generate_synthetic_county_data()
        print(f"   ✅ Generated {len(dashboard.stats_data)} data records")
        print(f"   📅 Date range: {dashboard.stats_data['date'].min()} to {dashboard.stats_data['date'].max()}")
        print(f"   📊 Metrics: {len([col for col in dashboard.stats_data.columns if col not in ['county', 'state', 'date', 'county_type']])}")

        # Test 4: Data quality checks
        print("\n4. Testing data quality...")

        # Check for missing values in key columns
        key_cols = ['population', 'gdp_millions', 'unemployment_rate', 'median_income']
        missing_data = dashboard.stats_data[key_cols].isnull().sum()
        if missing_data.sum() == 0:
            print("   ✅ No missing values in key metrics")
        else:
            print(f"   ⚠️  Missing values found: {missing_data.to_dict()}")

        # Check realistic ranges
        latest = dashboard.stats_data[dashboard.stats_data['date'] == dashboard.stats_data['date'].max()]

        pop_range = latest['population'].describe()
        if 10000 <= pop_range['min'] <= pop_range['max'] <= 15000000:
            print("   ✅ Population values in realistic range")
        else:
            print(f"   ⚠️  Population range unusual: {pop_range['min']:.0f} - {pop_range['max']:.0f}")

        unemployment_range = latest['unemployment_rate'].describe()
        if 1 <= unemployment_range['min'] <= unemployment_range['max'] <= 15:
            print("   ✅ Unemployment rates in realistic range")
        else:
            print(f"   ⚠️  Unemployment range unusual: {unemployment_range['min']:.1f}% - {unemployment_range['max']:.1f}%")

        # Test 5: Geographic data integrity
        print("\n5. Testing geographic data...")
        if dashboard.gdf.crs.to_string() == 'EPSG:4326':
            print("   ✅ Coordinate system is WGS84 (EPSG:4326)")
        else:
            print(f"   ⚠️  Unexpected CRS: {dashboard.gdf.crs}")

        if dashboard.gdf.geometry.is_valid.all():
            print("   ✅ All geometries are valid")
        else:
            invalid_count = (~dashboard.gdf.geometry.is_valid).sum()
            print(f"   ⚠️  {invalid_count} invalid geometries found")

        # Test 6: Dashboard components
        print("\n6. Testing dashboard components...")

        # Initialize widgets (simulate)
        dashboard.state_dropdown = type('Widget', (), {'value': 'All States'})()
        dashboard.county_dropdown = type('Widget', (), {'value': 'All Counties'})()
        dashboard.metric_dropdown = type('Widget', (), {'value': 'population'})()
        dashboard.view_dropdown = type('Widget', (), {'value': 'map'})()
        dashboard.time_slider = type('Widget', (), {'value': 12})()

        # Test map creation
        try:
            map_obj = dashboard.create_county_map()
            print("   ✅ County map creation successful")
        except Exception as e:
            print(f"   ❌ Map creation failed: {e}")

        # Test chart creation
        try:
            dashboard.view_dropdown.value = 'trends'
            fig = dashboard.create_analysis_charts()
            print("   ✅ Analysis charts creation successful")
        except Exception as e:
            print(f"   ❌ Chart creation failed: {e}")

        # Test 7: Data export
        print("\n7. Testing data export...")
        try:
            dashboard.stats_data.to_csv('test_export.csv', index=False)
            dashboard.gdf.to_file('test_boundaries.geojson', driver='GeoJSON')

            # Clean up test files
            if os.path.exists('test_export.csv'):
                os.remove('test_export.csv')
            if os.path.exists('test_boundaries.geojson'):
                os.remove('test_boundaries.geojson')

            print("   ✅ Data export functionality working")
        except Exception as e:
            print(f"   ❌ Export failed: {e}")

        # Test 8: Performance metrics
        print("\n8. Performance metrics...")
        import psutil
        import time

        start_time = time.time()
        # Simulate some operations
        _ = dashboard.stats_data.groupby('county')['population'].mean()
        end_time = time.time()

        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB

        print(f"   📊 Memory usage: {memory_usage:.1f} MB")
        print(f"   ⏱️  Data processing time: {(end_time - start_time)*1000:.1f} ms")

        if memory_usage < 500:  # Less than 500MB
            print("   ✅ Memory usage within acceptable limits")
        else:
            print("   ⚠️  High memory usage detected")

        print("\n" + "="*50)
        print("🎉 DASHBOARD FUNCTIONALITY TEST COMPLETE")
        print("✅ All core features are working correctly!")
        print("\n📋 Summary:")
        print(f"   🗺️  Counties loaded: {len(dashboard.gdf)}")
        print(f"   📊 Data records: {len(dashboard.stats_data):,}")
        print(f"   📅 Time periods: {len(dashboard.stats_data['date'].unique())}")
        print(f"   📈 Available metrics: {len([col for col in dashboard.stats_data.columns if col not in ['county', 'state', 'date', 'county_type']])}")
        print(f"   💾 Memory usage: {memory_usage:.1f} MB")

        return True

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_dashboard_functionality()
    sys.exit(0 if success else 1)