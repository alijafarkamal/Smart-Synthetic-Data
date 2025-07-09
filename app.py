import streamlit as st
import pandas as pd
import json
import os
from generator import SyntheticDataGenerator
from validate import DataValidator
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import base64

st.set_page_config(
    page_title="Smart Synthetic Data Generator",
    page_icon="🔬",
    layout="wide"
)

def main():
    st.sidebar.title("🔬 Smart Synthetic Data Generator")
    st.sidebar.markdown("Generate realistic synthetic data for multiple domains")
    
    domains_dir = "domains"
    if not os.path.exists(domains_dir):
        st.error("Domains directory not found!")
        return
    
    domain_files = [f for f in os.listdir(domains_dir) if f.endswith('.json')]
    domain_names = [f.replace('.json', '').title() for f in domain_files]
    
    if not domain_files:
        st.error("No domain schema files found in domains/ directory!")
        return
    
    selected_domain = st.sidebar.selectbox(
        "Select Domain",
        domain_names,
        index=0,
        help="Choose the domain for synthetic data generation"
    )
    
    selected_file = f"{selected_domain.lower()}.json"
    schema_path = os.path.join(domains_dir, selected_file)
    
    num_rows = st.sidebar.slider(
        "Number of Rows",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        help="Select the number of synthetic records to generate"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 Advanced Options")
    
    inject_edge_cases = st.sidebar.checkbox(
        "Inject Edge Cases",
        value=False,
        help="Inject rare or adversarial values for robustness testing"
    )
    
    inject_noise = st.sidebar.checkbox(
        "Inject Noise",
        value=False,
        help="Add controlled noise to numeric fields"
    )
    
    noise_range = 0.0
    if inject_noise:
        noise_range = st.sidebar.slider(
            "Noise Range (±%)",
            min_value=0.01,
            max_value=0.20,
            value=0.05,
            step=0.01,
            help="Percentage of noise to add to numeric values"
        )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Validation Options")
    
    show_histograms = st.sidebar.checkbox(
        "Show Histograms",
        value=True,
        help="Display distribution plots for numeric fields"
    )
    
    show_statistics = st.sidebar.checkbox(
        "Show Statistics",
        value=True,
        help="Display detailed statistical analysis"
    )
    
    if st.sidebar.button("🚀 Generate Synthetic Data", type="primary", use_container_width=True):
        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            
            generator = SyntheticDataGenerator(
                inject_edge_cases=inject_edge_cases,
                inject_noise=inject_noise,
                noise_range=noise_range
            )
            
            if not generator.validate_schema(schema):
                st.error("❌ Invalid schema format!")
                return
            
            with st.spinner("Generating synthetic data..."):
                df = generator.generate_data(schema, num_rows)
            
            st.success(f"✅ Successfully generated {num_rows} rows of {selected_domain} data!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Domain", selected_domain)
            with col4:
                numeric_cols = len([col for col in df.columns if pd.api.types.is_numeric_dtype(df[col].dtype)])
                st.metric("Numeric Fields", numeric_cols)
            
            st.subheader("📊 Generated Data Preview")
            st.dataframe(df, use_container_width=True)
            
            if show_statistics:
                st.subheader("📈 Statistical Analysis")
                
                validator = DataValidator()
                analysis = validator.analyze_distributions(df)
                
                if analysis['numeric_summary']:
                    st.write("**Numeric Field Statistics:**")
                    numeric_df = pd.DataFrame(analysis['numeric_summary']).T
                    st.dataframe(numeric_df[['count', 'mean', 'std', 'min', 'max', 'median']], use_container_width=True)
                
                if analysis['categorical_summary']:
                    st.write("**Categorical Field Summary:**")
                    for field, stats in analysis['categorical_summary'].items():
                        st.write(f"- **{field}**: {stats['unique_values']} unique values")
                        if stats['most_common']:
                            st.write(f"  Most common: {list(stats['most_common'].keys())[:3]}")
            
            if show_histograms and analysis['numeric_summary']:
                st.subheader("\U0001F4CA Distribution Plots")
                # Exclude boolean columns from numeric_fields
                numeric_fields = [
                    field for field in analysis['numeric_summary'].keys()
                    if pd.api.types.is_numeric_dtype(df[field]) and not pd.api.types.is_bool_dtype(df[field])
                ]
                if numeric_fields:
                    for field in numeric_fields[:3]:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        plt.hist(df[field].dropna(), bins=30, alpha=0.7, edgecolor='black')
                        plt.title(f'Distribution of {field}')
                        plt.xlabel(field)
                        plt.ylabel('Frequency')
                        plt.grid(True, alpha=0.3)
                        st.pyplot(fig)
                        plt.close()
            
            st.subheader("📥 Download Data")
            
            csv = df.to_csv(index=False)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{selected_domain.lower()}_synthetic_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🔄 Regenerate with Same Settings", use_container_width=True):
                    st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error generating data: {str(e)}")
    
    st.title("🔬 Smart Synthetic Data Generator")
    st.markdown("Generate realistic synthetic data for healthcare, finance, and retail domains")
    
    with st.expander("ℹ️ How to use", expanded=True):
        st.markdown("""
        ### Quick Start Guide
        
        1. **Select Domain**: Choose from Healthcare, Finance, or Retail from the sidebar
        2. **Set Row Count**: Use the slider to specify number of rows (10-1000)
        3. **Configure Options**: Enable edge cases and noise injection for robustness testing
        4. **Generate**: Click the "Generate Synthetic Data" button
        5. **Analyze**: View statistics, distributions, and validation results
        6. **Download**: Use the download button to save as CSV
        
        ### Advanced Features
        - **Edge Case Injection**: Adds rare or adversarial values for robustness testing
        - **Noise Injection**: Adds controlled noise to numeric fields for privacy
        - **Cross-field Validation**: Ensures data consistency across related fields
        - **Statistical Analysis**: Provides detailed distribution analysis
        - **Distribution Plots**: Visualizes data distributions for numeric fields
        """)
    
    with st.expander("📋 Domain Information"):
        if selected_domain:
            try:
                with open(schema_path, 'r') as f:
                    schema = json.load(f)
                
                st.write(f"**{selected_domain} Schema:**")
                for field_name, field_metadata in schema['fields'].items():
                    field_type = field_metadata.get('type', 'unknown')
                    st.write(f"- **{field_name}**: {field_type}")
                    
                    if field_type == "integer" or field_type == "float":
                        min_val = field_metadata.get('min', 'N/A')
                        max_val = field_metadata.get('max', 'N/A')
                        st.write(f"  - Range: {min_val} to {max_val}")
                    elif field_type == "choice":
                        options = field_metadata.get('options', [])
                        st.write(f"  - Options: {', '.join(options[:5])}{'...' if len(options) > 5 else ''}")
                    elif field_type == "date":
                        start_date = field_metadata.get('start', 'N/A')
                        end_date = field_metadata.get('end', 'N/A')
                        st.write(f"  - Range: {start_date} to {end_date}")
                    
            except Exception as e:
                st.error(f"Error loading schema: {str(e)}")
    
    with st.expander("🔧 Technical Details"):
        st.markdown("""
        ### Supported Data Types
        
        The generator supports various data types with metadata:
        
        - **uuid**: Unique identifiers
        - **name**: Full names
        - **email**: Email addresses
        - **phone**: Phone numbers
        - **address**: Full addresses
        - **integer**: Numbers with min/max range
        - **float**: Decimal numbers with precision
        - **date**: Dates with start/end range
        - **choice**: Selection from predefined options
        - **company**: Company names
        - **text**: Text with character limits
        - **city/state/country/zipcode**: Geographic data
        - **boolean**: True/False values
        
        ### Edge Cases & Noise
        
        - **Edge Cases**: Injects rare values like empty strings, "N/A", extreme values
        - **Noise Injection**: Adds ±ε% random noise to numeric fields for privacy
        - **Cross-field Validation**: Ensures logical consistency (e.g., discharge ≥ admit date)
        
        ### Adding New Domains
        
        To add a new domain:
        1. Create a new JSON file in the `domains/` folder
        2. Define fields with type and metadata
        3. Restart the application
        
        Example schema structure:
        ```json
        {
          "fields": {
            "field_name": {
              "type": "integer",
              "min": 1,
              "max": 100
            }
          }
        }
        ```
        """)

if __name__ == "__main__":
    main() 