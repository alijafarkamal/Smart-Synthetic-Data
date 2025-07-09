import json
import os
from generator import SyntheticDataGenerator
from validate import DataValidator
import pandas as pd

def test_generator():
    print("🔬 Testing Smart Synthetic Data Generator")
    print("=" * 50)
    
    generator = SyntheticDataGenerator()
    
    domains_dir = "domains"
    domain_files = [f for f in os.listdir(domains_dir) if f.endswith('.json')]
    
    for domain_file in domain_files:
        domain_name = domain_file.replace('.json', '').title()
        print(f"\n📊 Testing {domain_name} domain...")
        
        schema_path = os.path.join(domains_dir, domain_file)
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        if not generator.validate_schema(schema):
            print(f"❌ Invalid schema for {domain_name}")
            continue
        
        try:
            df = generator.generate_data(schema, 5)
            print(f"✅ Successfully generated {len(df)} rows")
            print(f"📋 Columns: {list(df.columns)}")
            print(f"📄 Sample data:")
            print(df.head(2).to_string())
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ Error generating {domain_name} data: {str(e)}")
    
    print("\n🎉 All tests completed!")

def test_edge_cases():
    print("\n🔍 Testing Edge Case Injection")
    print("=" * 30)
    
    generator = SyntheticDataGenerator(inject_edge_cases=True, inject_noise=True, noise_range=0.1)
    
    test_schema = {
        "fields": {
            "name": {"type": "name"},
            "age": {"type": "integer", "min": 18, "max": 85},
            "salary": {"type": "float", "min": 30000, "max": 150000, "precision": 2},
            "email": {"type": "email"},
            "status": {"type": "choice", "options": ["Active", "Inactive", "Pending"]}
        }
    }
    
    try:
        df = generator.generate_data(test_schema, 10)
        print(f"✅ Generated {len(df)} rows with edge cases")
        print(f"📄 Sample data with edge cases:")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"❌ Error testing edge cases: {str(e)}")

def test_validation():
    print("\n🔍 Testing Validation Module")
    print("=" * 30)
    
    validator = DataValidator()
    
    test_data = pd.DataFrame({
        'age': [25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
        'salary': [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000],
        'department': ['IT', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT'],
        'admit_date': pd.date_range('2023-01-01', periods=10),
        'discharge_date': pd.date_range('2023-01-02', periods=10)
    })
    
    analysis = validator.analyze_distributions(test_data)
    print(f"✅ Analysis completed")
    print(f"📊 Numeric fields: {len(analysis['numeric_summary'])}")
    print(f"📊 Categorical fields: {len(analysis['categorical_summary'])}")
    print(f"📊 Date fields: {len(analysis['date_summary'])}")
    
    for field in analysis['numeric_summary']:
        outliers = validator.detect_outliers(test_data, field)
        if outliers:
            print(f"🔍 {field}: {outliers['outlier_count']} outliers detected")

def test_schema_validation():
    print("\n🔍 Testing Schema Validation")
    print("=" * 30)
    
    generator = SyntheticDataGenerator()
    
    valid_schema = {
        "fields": {
            "test_field": {
                "type": "integer",
                "min": 1,
                "max": 100
            }
        }
    }
    
    print(f"✅ Valid schema: {generator.validate_schema(valid_schema)}")
    
    invalid_schema = {
        "fields": {
            "test_field": "invalid_type"
        }
    }
    
    print(f"❌ Invalid schema: {generator.validate_schema(invalid_schema)}")
    
    invalid_range_schema = {
        "fields": {
            "test_field": {
                "type": "integer",
                "min": 100,
                "max": 50
            }
        }
    }
    
    print(f"❌ Invalid range schema: {generator.validate_schema(invalid_range_schema)}")

if __name__ == "__main__":
    test_generator()
    test_edge_cases()
    test_validation()
    test_schema_validation() 