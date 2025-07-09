import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, List, Tuple, Optional
import streamlit as st

class DataValidator:
    
    def __init__(self):
        self.numeric_fields = []
        self.categorical_fields = []
        self.date_fields = []
    
    def analyze_distributions(self, df: pd.DataFrame) -> Dict:
        """Analyze distributions of all fields in the dataset."""
        analysis = {
            'numeric_summary': {},
            'categorical_summary': {},
            'date_summary': {},
            'field_types': {}
        }
        
        for column in df.columns:
            dtype = df[column].dtype
            # Exclude boolean columns from numeric analysis
            if pd.api.types.is_numeric_dtype(dtype) and not pd.api.types.is_bool_dtype(dtype):
                analysis['field_types'][column] = 'numeric'
                analysis['numeric_summary'][column] = {
                    'count': len(df[column]),
                    'mean': df[column].mean(),
                    'std': df[column].std(),
                    'min': df[column].min(),
                    'max': df[column].max(),
                    'median': df[column].median(),
                    'q25': df[column].quantile(0.25),
                    'q75': df[column].quantile(0.75),
                    'skewness': df[column].skew(),
                    'kurtosis': df[column].kurtosis()
                }
                self.numeric_fields.append(column)
            elif pd.api.types.is_bool_dtype(dtype):
                # Treat boolean columns as categorical
                analysis['field_types'][column] = 'categorical'
                value_counts = df[column].value_counts()
                analysis['categorical_summary'][column] = {
                    'count': len(df[column]),
                    'unique_values': len(value_counts),
                    'most_common': value_counts.head(5).to_dict(),
                    'null_count': df[column].isnull().sum()
                }
                self.categorical_fields.append(column)
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                analysis['field_types'][column] = 'date'
                analysis['date_summary'][column] = {
                    'count': len(df[column]),
                    'min_date': df[column].min(),
                    'max_date': df[column].max(),
                    'date_range_days': (df[column].max() - df[column].min()).days
                }
                self.date_fields.append(column)
            else:
                analysis['field_types'][column] = 'categorical'
                value_counts = df[column].value_counts()
                analysis['categorical_summary'][column] = {
                    'count': len(df[column]),
                    'unique_values': len(value_counts),
                    'most_common': value_counts.head(5).to_dict(),
                    'null_count': df[column].isnull().sum()
                }
                self.categorical_fields.append(column)
        
        return analysis
    
    def generate_histograms(self, df: pd.DataFrame, numeric_fields: List[str]) -> Dict:
        """Generate histogram plots for numeric fields."""
        plots = {}
        
        for field in numeric_fields:
            if field in df.columns and pd.api.types.is_numeric_dtype(df[field].dtype):
                fig, ax = plt.subplots(figsize=(10, 6))
                
                plt.hist(df[field].dropna(), bins=30, alpha=0.7, edgecolor='black')
                plt.title(f'Distribution of {field}')
                plt.xlabel(field)
                plt.ylabel('Frequency')
                plt.grid(True, alpha=0.3)
                
                plots[field] = fig
                plt.close()
        
        return plots
    
    def test_normality(self, df: pd.DataFrame, field: str) -> Dict:
        """Perform normality test on numeric field."""
        if field not in df.columns or not pd.api.types.is_numeric_dtype(df[field].dtype):
            return None
        
        data = df[field].dropna()
        if len(data) < 3:
            return None
        
        try:
            statistic, p_value = stats.normaltest(data)
            return {
                'statistic': statistic,
                'p_value': p_value,
                'is_normal': p_value > 0.05,
                'sample_size': len(data)
            }
        except:
            return None
    
    def compare_distributions(self, df1: pd.DataFrame, df2: pd.DataFrame, field: str) -> Dict:
        """Compare distributions between two datasets for a numeric field."""
        if field not in df1.columns or field not in df2.columns:
            return None
        
        if not pd.api.types.is_numeric_dtype(df1[field].dtype) or not pd.api.types.is_numeric_dtype(df2[field].dtype):
            return None
        
        data1 = df1[field].dropna()
        data2 = df2[field].dropna()
        
        if len(data1) < 3 or len(data2) < 3:
            return None
        
        try:
            statistic, p_value = stats.ks_2samp(data1, data2)
            return {
                'ks_statistic': statistic,
                'p_value': p_value,
                'similar_distributions': p_value > 0.05,
                'sample_size_1': len(data1),
                'sample_size_2': len(data2)
            }
        except:
            return None
    
    def detect_outliers(self, df: pd.DataFrame, field: str, method: str = 'iqr') -> Dict:
        """Detect outliers in numeric field."""
        if field not in df.columns or not pd.api.types.is_numeric_dtype(df[field].dtype):
            return None
        
        data = df[field].dropna()
        if len(data) < 3:
            return None
        
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            
            return {
                'outlier_count': len(outliers),
                'outlier_percentage': len(outliers) / len(data) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_values': outliers.tolist()
            }
        
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(data))
            outliers = data[z_scores > 3]
            
            return {
                'outlier_count': len(outliers),
                'outlier_percentage': len(outliers) / len(data) * 100,
                'z_score_threshold': 3,
                'outlier_values': outliers.tolist()
            }
        
        return None
    
    def validate_cross_field_consistency(self, df: pd.DataFrame) -> List[Dict]:
        """Validate cross-field consistency rules."""
        issues = []
        
        for idx, row in df.iterrows():
            if 'admit_date' in df.columns and 'discharge_date' in df.columns:
                if pd.notna(row['admit_date']) and pd.notna(row['discharge_date']):
                    if row['discharge_date'] < row['admit_date']:
                        issues.append({
                            'row': idx,
                            'issue': 'Discharge date before admit date',
                            'fields': ['admit_date', 'discharge_date']
                        })
            
            if 'order_date' in df.columns and 'shipping_date' in df.columns:
                if pd.notna(row['order_date']) and pd.notna(row['shipping_date']):
                    if row['shipping_date'] < row['order_date']:
                        issues.append({
                            'row': idx,
                            'issue': 'Shipping date before order date',
                            'fields': ['order_date', 'shipping_date']
                        })
            
            if 'age' in df.columns:
                if pd.notna(row['age']) and (row['age'] < 0 or row['age'] > 120):
                    issues.append({
                        'row': idx,
                        'issue': 'Age out of reasonable range',
                        'fields': ['age']
                    })
        
        return issues
    
    def generate_summary_report(self, df: pd.DataFrame) -> str:
        """Generate a comprehensive summary report."""
        analysis = self.analyze_distributions(df)
        
        report = f"Dataset Summary Report\n{'='*50}\n"
        report += f"Total Rows: {len(df)}\n"
        report += f"Total Columns: {len(df.columns)}\n"
        report += f"Numeric Fields: {len(self.numeric_fields)}\n"
        report += f"Categorical Fields: {len(self.categorical_fields)}\n"
        report += f"Date Fields: {len(self.date_fields)}\n\n"
        
        if self.numeric_fields:
            report += "Numeric Field Statistics:\n"
            for field in self.numeric_fields:
                stats = analysis['numeric_summary'][field]
                report += f"  {field}: mean={stats['mean']:.2f}, std={stats['std']:.2f}, range=[{stats['min']:.2f}, {stats['max']:.2f}]\n"
        
        if self.categorical_fields:
            report += "\nCategorical Field Summary:\n"
            for field in self.categorical_fields:
                stats = analysis['categorical_summary'][field]
                report += f"  {field}: {stats['unique_values']} unique values\n"
        
        return report 