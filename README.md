# 🔬 Smart Synthetic Data Generator
**Link**: https://smartdata.streamlit.app/
A **top-tier, industry-level** synthetic data generator built with Python and Streamlit. This application generates realistic synthetic data across multiple domains with advanced features including bias control, edge case injection, noise injection, and comprehensive validation.

## 🚀 Features

### Core Features
- **Multi-Domain Support**: Healthcare, Finance, Retail, and Education schemas
- **Enhanced Schema System**: Rich metadata with constraints and validation
- **Realistic Data Generation**: Uses Faker library for authentic-looking data
- **Customizable Output**: Generate 10-1000 rows of synthetic data
- **CSV Export**: Download generated data as CSV files

### Advanced Features
- **Edge Case Injection**: Adds rare or adversarial values for robustness testing
- **Noise Injection**: Controlled noise addition to numeric fields for privacy
- **Cross-field Validation**: Ensures logical consistency across related fields
- **Statistical Analysis**: Comprehensive distribution analysis and outlier detection
- **Distribution Visualization**: Histogram plots for numeric fields
- **Schema Validation**: Robust validation with detailed error messages

### Privacy & Security
- **No External APIs**: Completely local and open-source
- **Controlled Noise**: ±ε% random noise for privacy protection
- **Edge Case Testing**: Injects rare values for AI robustness
- **Data Consistency**: Cross-field validation ensures logical integrity

## 🛠 Tech Stack

- **Python 3.8+**
- **Streamlit** - Modern web application framework
- **Faker** - High-quality synthetic data generation
- **Pandas** - Data manipulation and analysis
- **Matplotlib/Seaborn** - Data visualization
- **SciPy** - Statistical analysis and testing
- **NumPy** - Numerical operations

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alijafarkamal/Smart-Synthetic-Data
   cd smart-synthetic-data-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 🎯 Usage

### Basic Usage
1. **Select Domain**: Choose from Healthcare, Finance, Retail, or Education
2. **Set Row Count**: Use the slider to specify number of rows (10-1000)
3. **Generate Data**: Click the "Generate Synthetic Data" button
4. **Download**: Use the download button to save as CSV

### Advanced Options
- **Edge Case Injection**: Enable to add rare values for robustness testing
- **Noise Injection**: Add controlled noise to numeric fields for privacy
- **Statistical Analysis**: View detailed distribution statistics
- **Distribution Plots**: Visualize data distributions for numeric fields

## 📊 Domain Schemas

### Enhanced Schema Structure
Each domain uses a rich metadata system:

```json
{
  "fields": {
    "age": {
      "type": "integer",
      "min": 18,
      "max": 85
    },
    "gender": {
      "type": "choice",
      "options": ["Male", "Female", "Other"]
    },
    "admit_date": {
      "type": "date",
      "start": "2021-01-01",
      "end": "2025-07-01"
    }
  }
}
```

### Healthcare Domain
- Patient information (ID, name, age, gender)
- Medical data (diagnosis, allergies, medications)
- Hospital details (admit/discharge dates, doctor, room)
- Contact information (email, phone, emergency contacts)
- **Enhanced Fields**: Blood type, preferred language, marital status, occupation

### Finance Domain
- Account information (ID, balance, credit score)
- Customer details (name, employment, education)
- Transaction data (type, amount, date, merchant)
- Banking information (bank name, card type, currency)
- **Enhanced Fields**: Branch code, IFSC code, loan status, mortgage amount, account open date

### Retail Domain
- Order details (ID, customer info, shipping/billing addresses)
- Product information (name, category, price, quantity)
- Sales data (order date, delivery, payment method)
- Customer feedback (ratings, reviews)
- **Enhanced Fields**: Warehouse location, promo code, refund status, delivery distance, coupon discount

### Education Domain
- Student information (ID, name, age, gender)
- Academic data (major, GPA, enrollment/graduation dates)
- University details (university, department, advisor)
- Financial information (scholarship amount, international status)
- **Enhanced Fields**: Credits completed, dormitory status, advisor contact

## 🔧 Supported Data Types

The generator supports comprehensive data types with rich metadata:

- **uuid** → `fake.uuid4()`
- **name** → `fake.name()`
- **email** → `fake.email()`
- **phone** → `fake.phone_number()`
- **address** → `fake.address().replace("\n", ", ")`
- **integer** → `random.randint(min, max)` with noise injection
- **float** → `round(random.uniform(min, max), precision)` with noise injection
- **date** → `fake.date_between(start, end)`
- **choice** → `random.choice(options)`
- **company** → `fake.company()`
- **text** → `fake.text(max_nb_chars=metadata.get("max_chars",200))`
- **city/state/country/zipcode** → corresponding `fake` methods
- **boolean** → `random.choice([True,False])`

## 🏗 Architecture

```
smart-synthetic-data-generator/
├── app.py                 # Enhanced Streamlit application
├── generator.py           # Advanced data generation with bias control
├── validate.py            # Comprehensive validation and analysis
├── requirements.txt       # Pinned dependencies
├── README.md             # Complete documentation
├── test_generator.py     # Comprehensive test suite
├── domains/              # Enhanced domain schemas
│   ├── healthcare.json
│   ├── finance.json
│   ├── retail.json
│   └── education.json
└── templates/            # Additional resources
    └── architecture_diagram.png
```

## 🔍 Validation & Analysis

### Statistical Analysis
- **Distribution Analysis**: Mean, std, min, max, median, quartiles
- **Outlier Detection**: IQR and Z-score methods
- **Normality Testing**: Kolmogorov-Smirnov test
- **Cross-field Validation**: Logical consistency checks

### Visualization
- **Histogram Plots**: Distribution visualization for numeric fields
- **Statistical Summary**: Comprehensive field statistics
- **Outlier Analysis**: Detection and reporting of anomalies

### Edge Case Testing
- **Rare Values**: Empty strings, "N/A", extreme values
- **Adversarial Data**: Test values for AI robustness
- **Boundary Testing**: Values at min/max boundaries

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment (Render/Replit)

1. **Create a new web service**
2. **Set build command**: `pip install -r requirements.txt`
3. **Set start command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. **Deploy**

### Supported Platforms
- **Render.com**: Easy deployment with automatic builds
- **Replit**: Instant deployment with built-in IDE
- **Heroku**: Traditional cloud platform
- **Railway**: Modern deployment platform

## 📈 Sample Output

### Healthcare Example
```
patient_id: 550e8400-e29b-41d4-a716-446655440000
name: Dr. Sarah Johnson
age: 45
diagnosis: Diabetes
admit_date: 2024-01-15
blood_type: A+
preferred_language: English
```

### Finance Example
```
account_id: 123e4567-e89b-12d3-a456-426614174000
customer_name: John Smith
account_balance: 15420.50
credit_score: 720
branch_code: 456
loan_status: Approved
mortgage_amount: 250000.00
```

### Retail Example
```
order_id: 987fcdeb-51a2-43d1-9f12-123456789abc
customer_name: Alice Brown
product_category: Electronics
total_amount: 299.99
delivery_distance_km: 15.5
refund_requested: False
promo_code: SAVE20
```

## 🔧 Adding New Domains

To add a new domain:

1. **Create a new JSON file** in the `domains/` folder
2. **Define fields** with type and metadata
3. **Restart the application**

Example schema structure:
```json
{
  "fields": {
    "field_name": {
      "type": "integer",
      "min": 1,
      "max": 100
    },
    "email_field": {
      "type": "email"
    },
    "choice_field": {
      "type": "choice",
      "options": ["Option1", "Option2", "Option3"]
    }
  }
}
```

## 🧪 Testing

To verify all functionality:
```bash
python test_generator.py
```

This will test:
- ✅ Basic data generation for all domains
- ✅ Edge case injection
- ✅ Noise injection
- ✅ Validation module
- ✅ Schema validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


---

**Built with ❤️ for the GenAI Hackathon** 
