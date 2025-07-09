import pandas as pd
import numpy as np
from faker import Faker
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

class SyntheticDataGenerator:
    
    def __init__(self, inject_edge_cases: bool = False, inject_noise: bool = False, noise_range: float = 0.05):
        self.fake = Faker()
        self.inject_edge_cases = inject_edge_cases
        self.inject_noise = inject_noise
        self.noise_range = noise_range
        
        self.genders = ['Male', 'Female', 'Other']
        self.transaction_types = ['Purchase', 'Sale', 'Refund', 'Transfer', 'Deposit', 
                                'Withdrawal', 'Payment', 'Fee', 'Interest', 'Dividend']
        self.product_categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 
                                 'Sports', 'Beauty', 'Automotive', 'Toys', 'Food', 'Health']
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']
        self.employment_status = ['Full-time', 'Part-time', 'Contract', 'Freelance', 
                                'Unemployed', 'Retired', 'Student']
        self.education_levels = ['High School', 'Bachelor', 'Master', 'PhD', 
                                'Associate', 'Certificate', 'Diploma']
        
        self.edge_case_probability = 0.05
        
    def inject_edge_case(self, field_type: str, field_metadata: Dict[str, Any]) -> Any:
        """Inject edge cases for robustness testing."""
        if not self.inject_edge_cases or random.random() > self.edge_case_probability:
            return None
            
        if field_type == "name":
            edge_cases = ["", "N/A", "Test User", "Anonymous", "Unknown", "John Doe", "Jane Smith"]
            return random.choice(edge_cases)
            
        elif field_type == "email":
            edge_cases = ["", "test@test.com", "admin@company.com", "no-reply@example.com", "invalid-email"]
            return random.choice(edge_cases)
            
        elif field_type == "integer":
            min_val = field_metadata.get("min", 0)
            max_val = field_metadata.get("max", 100)
            edge_cases = [min_val - 1, max_val + 1, 0, -1, 999999]
            return random.choice(edge_cases)
            
        elif field_type == "float":
            min_val = field_metadata.get("min", 0.0)
            max_val = field_metadata.get("max", 1000.0)
            edge_cases = [min_val - 0.01, max_val + 0.01, 0.0, -0.01, 999999.99]
            return random.choice(edge_cases)
            
        elif field_type == "choice":
            options = field_metadata.get("options", [])
            edge_cases = ["", "N/A", "Other", "Unknown", "Test"]
            return random.choice(edge_cases)
            
        elif field_type == "date":
            start_date = field_metadata.get("start", "2020-01-01")
            end_date = field_metadata.get("end", "2025-01-01")
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            edge_cases = [
                start_dt - timedelta(days=1),
                end_dt + timedelta(days=1),
                datetime(1900, 1, 1),
                datetime(2100, 12, 31)
            ]
            return random.choice(edge_cases)
            
        return None
    
    def apply_noise(self, value: float, field_metadata: Dict[str, Any]) -> float:
        """Apply controlled noise to numeric values."""
        if not self.inject_noise or not isinstance(value, (int, float)):
            return value
            
        noise_factor = random.uniform(-self.noise_range, self.noise_range)
        precision = field_metadata.get("precision", 2)
        noisy_value = value * (1 + noise_factor)
        
        return round(noisy_value, precision)
    
    def generate_field_value(self, field_metadata: Dict[str, Any]) -> Any:
        field_type = field_metadata.get("type")
        
        edge_case = self.inject_edge_case(field_type, field_metadata)
        if edge_case is not None:
            return edge_case
        
        if field_type == "uuid":
            return self.fake.uuid4()
        
        elif field_type == "name":
            return self.fake.name()
        
        elif field_type == "email":
            return self.fake.email()
        
        elif field_type == "phone":
            return self.fake.phone_number()
        
        elif field_type == "address":
            return self.fake.address().replace("\n", ", ")
        
        elif field_type == "integer":
            min_val = field_metadata.get("min", 1)
            max_val = field_metadata.get("max", 100)
            value = random.randint(min_val, max_val)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "float":
            min_val = field_metadata.get("min", 0.0)
            max_val = field_metadata.get("max", 1000.0)
            precision = field_metadata.get("precision", 2)
            value = round(random.uniform(min_val, max_val), precision)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "date":
            start_date = field_metadata.get("start", "2020-01-01")
            end_date = field_metadata.get("end", "2025-01-01")
            
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            return self.fake.date_between(start_date=start_dt, end_date=end_dt)
        
        elif field_type == "choice":
            options = field_metadata.get("options", [])
            if not options:
                raise ValueError("Choice field must have 'options' list")
            return random.choice(options)
        
        elif field_type == "company":
            return self.fake.company()
        
        elif field_type == "text":
            max_chars = field_metadata.get("max_chars", 200)
            return self.fake.text(max_nb_chars=max_chars)
        
        elif field_type == "city":
            return self.fake.city()
        
        elif field_type == "state":
            return self.fake.state()
        
        elif field_type == "country":
            return self.fake.country()
        
        elif field_type == "zipcode":
            return self.fake.zipcode()
        
        elif field_type == "boolean":
            return random.choice([True, False])
        
        elif field_type == "gender":
            return random.choice(self.genders)
        
        elif field_type == "transaction":
            min_val = field_metadata.get("min", 10.0)
            max_val = field_metadata.get("max", 10000.0)
            precision = field_metadata.get("precision", 2)
            value = round(random.uniform(min_val, max_val), precision)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "age":
            min_val = field_metadata.get("min", 18)
            max_val = field_metadata.get("max", 85)
            value = random.randint(min_val, max_val)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "salary":
            min_val = field_metadata.get("min", 30000)
            max_val = field_metadata.get("max", 150000)
            value = random.randint(min_val, max_val)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "transaction_type":
            return random.choice(self.transaction_types)
        
        elif field_type == "product_category":
            return random.choice(self.product_categories)
        
        elif field_type == "currency":
            return random.choice(self.currencies)
        
        elif field_type == "employment_status":
            return random.choice(self.employment_status)
        
        elif field_type == "education":
            return random.choice(self.education_levels)
        
        elif field_type == "credit_score":
            min_val = field_metadata.get("min", 300)
            max_val = field_metadata.get("max", 850)
            value = random.randint(min_val, max_val)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "account_balance":
            min_val = field_metadata.get("min", -5000.0)
            max_val = field_metadata.get("max", 50000.0)
            precision = field_metadata.get("precision", 2)
            value = round(random.uniform(min_val, max_val), precision)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "price":
            min_val = field_metadata.get("min", 1.0)
            max_val = field_metadata.get("max", 1000.0)
            precision = field_metadata.get("precision", 2)
            value = round(random.uniform(min_val, max_val), precision)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "quantity":
            min_val = field_metadata.get("min", 1)
            max_val = field_metadata.get("max", 100)
            value = random.randint(min_val, max_val)
            return self.apply_noise(value, field_metadata)
        
        elif field_type == "rating":
            min_val = field_metadata.get("min", 1.0)
            max_val = field_metadata.get("max", 5.0)
            precision = field_metadata.get("precision", 1)
            value = round(random.uniform(min_val, max_val), precision)
            return self.apply_noise(value, field_metadata)
        
        else:
            raise ValueError(f"Unknown field type: {field_type}")
    
    def validate_cross_field_consistency(self, row: Dict, schema: Dict) -> List[str]:
        """Validate cross-field consistency rules."""
        issues = []
        fields = schema.get('fields', {})
        
        if 'admit_date' in row and 'discharge_date' in row:
            if pd.notna(row['admit_date']) and pd.notna(row['discharge_date']):
                if row['discharge_date'] < row['admit_date']:
                    issues.append("Discharge date before admit date")
        
        if 'order_date' in row and 'shipping_date' in row:
            if pd.notna(row['order_date']) and pd.notna(row['shipping_date']):
                if row['shipping_date'] < row['order_date']:
                    issues.append("Shipping date before order date")
        
        if 'age' in row:
            if pd.notna(row['age']) and (row['age'] < 0 or row['age'] > 120):
                issues.append("Age out of reasonable range")
        
        if 'credit_score' in row:
            if pd.notna(row['credit_score']) and (row['credit_score'] < 300 or row['credit_score'] > 850):
                issues.append("Credit score out of valid range")
        
        return issues
    
    def generate_data(self, schema: Dict, num_rows: int) -> pd.DataFrame:
        data = []
        fields = schema.get('fields', {})
        consistency_issues = []
        
        for row_idx in range(num_rows):
            row = {}
            row_issues = []
            
            for field_name, field_metadata in fields.items():
                try:
                    row[field_name] = self.generate_field_value(field_metadata)
                except Exception as e:
                    raise ValueError(f"Error generating field '{field_name}': {str(e)}")
            
            issues = self.validate_cross_field_consistency(row, schema)
            if issues:
                row_issues.extend(issues)
                consistency_issues.append({
                    'row': row_idx,
                    'issues': issues
                })
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        if consistency_issues:
            print(f"Warning: {len(consistency_issues)} rows have consistency issues")
        
        return df
    
    def validate_schema(self, schema: Dict) -> bool:
        if not isinstance(schema, dict):
            return False
        
        if 'fields' not in schema:
            return False
        
        if not isinstance(schema['fields'], dict):
            return False
        
        for field_name, field_metadata in schema['fields'].items():
            if not isinstance(field_metadata, dict):
                return False
            
            if 'type' not in field_metadata:
                return False
            
            field_type = field_metadata.get('type')
            
            if field_type in ['integer', 'float']:
                if 'min' not in field_metadata or 'max' not in field_metadata:
                    return False
                if field_metadata['min'] >= field_metadata['max']:
                    return False
            
            elif field_type == 'choice':
                if 'options' not in field_metadata or not field_metadata['options']:
                    return False
            
            elif field_type == 'date':
                if 'start' not in field_metadata or 'end' not in field_metadata:
                    return False
        
        return True 