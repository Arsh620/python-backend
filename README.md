# 🚀 Python Backend with Advanced Data Engineering Pipeline

A comprehensive FastAPI-based backend system with integrated data engineering features including real-time analytics, Apache Kafka event streaming, Pandas data processing, and business intelligence capabilities.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Data Engineering Pipeline](#-data-engineering-pipeline)
- [Kafka Integration](#-kafka-integration)
- [Pandas Analytics](#-pandas-analytics)
- [Dashboards](#-dashboards)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Testing](#-testing)

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication with Argon2 password hashing
- User registration and login with comprehensive validation
- Secure token management with configurable expiration
- Activity logging for all user interactions

### 📊 Advanced Data Engineering Pipeline
- **Real-time Event Streaming**: Apache Kafka integration for production-grade messaging
- **ETL Processing**: Pandas-powered data transformation and analytics
- **Batch Processing**: Scheduled analytics jobs with comprehensive reporting
- **Stream Processing**: Real-time event consumption and processing
- **Data Analytics**: Advanced user segmentation, churn prediction, and time series analysis

### 🔍 Business Intelligence & Analytics
- User behavior pattern analysis with Pandas
- Predictive analytics and churn modeling
- Real-time streaming statistics
- Advanced user segmentation (RFM analysis)
- Time series analysis and trend detection
- Interactive dashboards with Streamlit

### 🛡️ Security & Monitoring
- Comprehensive activity logging to PostgreSQL
- Real-time security threat detection
- Failed login attempt tracking
- IP-based monitoring and alerts

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│  Activity Logger │───▶│   PostgreSQL    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Apache Kafka    │    │ Pandas ETL       │    │ Streamlit       │
│ Event Streaming │    │ Pipeline         │    │ Dashboard       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Data Flow
1. **User Action** → API Request
2. **Authentication** → JWT Validation
3. **Activity Logging** → PostgreSQL Database
4. **Event Publishing** → Apache Kafka Topics
5. **Stream Processing** → Real-time Event Consumption
6. **ETL Processing** → Pandas Data Transformation
7. **Analytics Generation** → Business Intelligence
8. **Dashboard Updates** → Streamlit Visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Docker (for Kafka) OR Apache Kafka
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend_py
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file with your database credentials
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=python_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

5. **Start Kafka (Docker)**
   ```bash
   docker-compose up -d
   ```

6. **Initialize database**
   ```bash
   python -c "from db_config import init_db; init_db()"
   ```

7. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

8. **Start the Analytics Dashboard**
   ```bash
   streamlit run data_dashboard.py
   ```

## 🌐 Access Points

- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Analytics Dashboard**: http://localhost:8501
- **Simple Frontend**: http://localhost:8000/static/index.html

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "password": "securepassword123"
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepassword123"
}
```

### Analytics Endpoints

#### Pandas-Powered Analytics
```http
GET /pandas/user-analytics          # User analytics with Pandas
GET /pandas/activity-analytics      # Activity pattern analysis
GET /pandas/etl-demo               # Complete ETL pipeline demo
```

#### Advanced Analytics
```http
GET /advanced/user-segmentation     # RFM analysis and cohorts
GET /advanced/predictive-insights   # Churn prediction and ML features
GET /advanced/time-series-analysis  # Trends and patterns
```

#### Real-time Streaming
```http
GET /analytics/streaming-stats      # Real-time event statistics
GET /analytics/recent-events        # Live event stream
GET /real-kafka/status             # Kafka system status
POST /real-kafka/test-event        # Test Kafka event publishing
```

## 🔄 Data Engineering Pipeline

### 1. Data Ingestion Layer
- **Activity Logger**: Captures all user interactions with metadata
- **Request Middleware**: Logs API calls with IP, user-agent, timestamps
- **Event Publisher**: Streams events to Apache Kafka topics

### 2. Storage Layer
- **PostgreSQL**: Primary data storage with ACID compliance
- **User Activity Logs**: Comprehensive event tracking table
- **User Management**: Secure user data with proper indexing

### 3. Processing Layer
- **Apache Kafka**: Production-grade event streaming platform
- **Pandas ETL**: Advanced data transformation and cleaning
- **Stream Consumers**: Real-time event processing workers
- **Batch Jobs**: Scheduled analytics generation

### 4. Analytics Layer
- **Business Intelligence**: Pandas-powered analytics APIs
- **Real-time Metrics**: Live streaming statistics
- **Predictive Models**: Churn prediction and user segmentation
- **Interactive Dashboards**: Streamlit-based visualization

## ⚡ Kafka Integration

### Event Streaming Architecture
- **Topics**: `user_events`, `system_events`, `analytics_events`
- **Producers**: FastAPI application publishes events
- **Consumers**: Background workers process events
- **Partitioning**: Scalable event distribution

### Kafka Endpoints
```http
GET /real-kafka/status              # Kafka cluster status
GET /real-kafka/health              # Health check
POST /real-kafka/test-event         # Test event publishing
GET /real-kafka/recent-events       # Recent processed events
POST /real-kafka/start-consumer     # Start event consumer
POST /real-kafka/stop-consumer      # Stop event consumer
```

### Event Types
- **User Registration**: New user signup events
- **User Login**: Authentication events with metadata
- **System Events**: Application-level events
- **Security Events**: Failed login attempts and threats

## 🐼 Pandas Analytics

### Advanced Data Processing
- **Data Cleaning**: Automated data quality checks
- **Feature Engineering**: ML-ready feature generation
- **Statistical Analysis**: Comprehensive data insights
- **Time Series**: Trend analysis and forecasting

### Analytics Capabilities
```python
# User Segmentation
df['email_domain'] = df['email'].str.split('@').str[1]
df['user_type'] = df['account_age_days'].apply(lambda x: 'new' if x <= 7 else 'veteran')

# Churn Prediction
df['churn_risk_score'] = calculate_churn_probability(df)
df['engagement_score'] = calculate_engagement_metrics(df)

# Time Series Analysis
daily_trends = df.groupby('date')['activity_count'].sum()
seasonal_patterns = analyze_seasonal_trends(daily_trends)
```

### Business Intelligence Metrics
- **User Engagement**: Login frequency, session duration
- **Growth Analytics**: Acquisition, retention, churn rates
- **Behavioral Patterns**: Usage trends and preferences
- **Predictive Insights**: Future user behavior modeling

## 📊 Dashboards

### Streamlit Analytics Dashboard
- **Real-time Metrics**: Live user and system statistics
- **Interactive Charts**: Plotly-powered visualizations
- **User Segmentation**: Advanced cohort analysis
- **Predictive Analytics**: Churn risk and engagement scores
- **Time Series**: Trend analysis with forecasting
- **Event Monitoring**: Live Kafka event streaming

### Dashboard Features
- Auto-refresh capabilities
- Interactive filtering and drill-down
- Export functionality for reports
- Real-time alert notifications
- Mobile-responsive design

## 📁 Project Structure

```
backend_py/
├── controllers/                    # Business logic controllers
│   ├── auth_controller.py         # Authentication with Kafka events
│   └── user_controller.py         # User management
├── models/                        # SQLAlchemy ORM models
│   ├── user_model.py             # User entity with methods
│   ├── activity_log.py           # Activity logging model
│   └── base.py                   # Base model class
├── routers/                       # API route definitions
│   ├── auth.py                   # Authentication endpoints
│   ├── users.py                  # User CRUD endpoints
│   ├── analytics.py              # Analytics endpoints
│   ├── pandas_demo.py            # Pandas analytics demos
│   ├── advanced_analytics.py     # Advanced ML analytics
│   ├── real_kafka_status.py      # Kafka monitoring
│   └── test_logging.py           # Testing utilities
├── data_engineering/              # Data engineering pipeline
│   ├── streaming/                # Event streaming components
│   │   ├── stream_processor.py   # Kafka simulation
│   │   └── real_kafka.py         # Apache Kafka integration
│   └── etl/                      # ETL pipeline components
│       └── batch_processor.py    # Scheduled batch jobs
├── services/                      # Business services
│   ├── activity_logger.py        # Activity logging service
│   ├── analytics_etl.py          # ETL processing service
│   └── event_streaming.py        # Event streaming service
├── static/                        # Static frontend files
├── .env                          # Environment configuration
├── main.py                       # FastAPI application entry
├── database.py                   # Database operations
├── db_config.py                  # Database configuration
├── auth.py                       # JWT authentication utilities
├── schemas.py                    # Pydantic validation models
├── helpers.py                    # Response helper functions
├── dependencies.py               # FastAPI dependencies
├── routes.py                     # Route registration
├── data_dashboard.py             # Streamlit analytics dashboard
├── frontend.py                   # Streamlit user interface
├── docker-compose.yml            # Kafka Docker setup
└── requirements.txt              # Python dependencies
```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=python_db
DB_USER=postgres
DB_PASSWORD=your_password

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Schema
The application automatically creates the following tables:
- `users`: User account information with authentication data
- `user_activity_logs`: Comprehensive activity tracking with metadata

### Kafka Configuration
```yaml
# docker-compose.yml
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    ports: ["2181:2181"]
  
  kafka:
    image: confluentinc/cp-kafka:latest
    ports: ["9092:9092"]
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
```

## 🧪 Testing

### API Testing
```bash
# Test authentication
POST /auth/register
POST /auth/login

# Test analytics
GET /pandas/user-analytics
GET /advanced/user-segmentation
GET /real-kafka/status

# Test streaming
POST /real-kafka/test-event
GET /analytics/streaming-stats
```

### Data Pipeline Testing
```bash
# Test ETL pipeline
GET /pandas/etl-demo

# Test batch processing
POST /analytics/run-batch-job

# Test streaming events
POST /real-kafka/test-event
GET /real-kafka/recent-events
```

## 🚀 Deployment

### Production Checklist
- [ ] Update `SECRET_KEY` for production
- [ ] Configure production PostgreSQL database
- [ ] Set up Apache Kafka cluster
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategies
- [ ] Implement CI/CD pipeline
- [ ] Set up log aggregation

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 💡 Business Value

### 📊 Data-Driven Decision Making
- **Real-time Insights**: Immediate access to business metrics
- **Predictive Analytics**: Forecast user behavior and churn
- **User Segmentation**: Targeted marketing and retention strategies
- **Performance Optimization**: Data-driven system improvements

### 🔒 Enhanced Security & Compliance
- **Comprehensive Audit Trails**: Complete activity logging
- **Real-time Threat Detection**: Immediate security alerts
- **Compliance Ready**: GDPR and SOX audit trails
- **Risk Assessment**: Automated security scoring

### 💰 Cost Optimization & ROI
- **Resource Planning**: Optimize infrastructure based on usage
- **Churn Prevention**: Identify at-risk users proactively
- **Feature Analytics**: Measure feature adoption and ROI
- **Capacity Management**: Scale based on predictive models

## 🔮 Advanced Features

### Machine Learning Integration
- **Churn Prediction Models**: Identify users likely to leave
- **Recommendation Engine**: Personalized user experiences
- **Anomaly Detection**: Automated threat and fraud detection
- **Behavioral Clustering**: Advanced user segmentation

### Scalability Features
- **Horizontal Scaling**: Kafka partitioning for high throughput
- **Microservices Ready**: Modular architecture for decomposition
- **Caching Layer**: Redis integration for performance
- **Load Balancing**: Multi-instance deployment support

---

**🚀 Built with FastAPI, Apache Kafka, Pandas, PostgreSQL, and Streamlit for enterprise-grade data engineering and analytics**