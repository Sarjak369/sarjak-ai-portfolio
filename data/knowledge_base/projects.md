# Featured Projects

## 1. LangFlow-Viz: Workflow Graph Visualizer for LangGraph

**Tech Stack**: Python, LangGraph, Graphviz, Mermaid.js, GitHub Actions, PyPI  
**GitHub**: https://github.com/Sarjak369/langflow-viz

### Overview

Developed and open-sourced a Python library that revolutionizes how developers visualize and analyze LangGraph-style AI workflows. This tool has become essential for debugging complex agentic AI systems.

### Key Features

- Supports dual export formats: Graphviz (SVG/PNG) for static documentation and Mermaid.js (Markdown/HTML) for interactive exploration
- Handles complex workflow patterns including conditional edges and parallel execution paths
- Provides graph analytics and style customization options

### Technical Highlights

- Engineered an automated GitHub Actions CI/CD pipeline for trusted PyPI publishing
- Achieved 100% generation accuracy across conditional and parallel workflow visualizations
- Designed intuitive API that enables developers to visualize workflows in just 3 lines of code
- Enhanced developer usability with conditional-edge rendering for improved interpretability

### Impact

- Available on PyPI for the broader AI development community
- Enables faster debugging of complex AI agent flows
- Reduces development time for LangGraph-based applications

---

## 2. LogSenseAI: Hybrid Framework for Intelligent Log Classification

**Tech Stack**: Python, FastAPI, DBSCAN, Transformers, Llama 3.3, Logistic Regression  
**GitHub**: https://github.com/Sarjak369/logsense-ai

### Overview

Built a sophisticated hybrid system that combines traditional ML, deep learning, and LLMs to intelligently classify complex log files. This addresses a critical pain point in enterprise DevOps.

### Architecture

- **Layer 1**: Regex pattern matching for common log formats
- **Layer 2**: Transformer models + LLM (Llama 3.3) for complex, unstructured logs
- **Layer 3**: Logistic Regression for final classification

### Technical Highlights

- Applied DBSCAN clustering to automatically extract prominent regex patterns from unstructured logs
- Achieved 40% higher accuracy compared to traditional rule-based systems
- Deployed with FastAPI providing RESTful APIs for real-time CSV processing
- Enables seamless enterprise integration with existing log management systems

### Business Impact

- Automated log analysis reducing manual effort by 30%
- Reduced operational costs through intelligent pattern recognition
- Scalable solution handling millions of log entries

---

## 3. LinkedIn Post Generator

**Tech Stack**: Python, Streamlit, Llama 3.3, Groq Cloud  
**GitHub**: https://github.com/Sarjak369/linkedin-post-generator

### Overview

Created an AI-powered tool that analyzes LinkedIn influencers' writing styles and generates new posts that authentically replicate their unique voice, tone, and content patterns.

### How It Works

- Scrapes and analyzes past LinkedIn posts from target influencers
- Extracts writing patterns: tone, language style, topic preferences, engagement hooks
- Uses Llama 3.3 via Groq Cloud to generate new posts matching the learned style

### Technical Implementation

- Two-stage pipeline: preprocessing (style extraction) and generation (content creation)
- Enriched metadata with tags, hashtags, and engagement signals
- Built intuitive Streamlit UI with copy-to-clipboard and hashtag suggestions

### Impact

- Improved content creation workflow efficiency by ~40%
- Helps content creators maintain consistent brand voice
- Reduces time spent on content ideation and drafting

---

## 4. AI Shop Assistant Chatbot

**Tech Stack**: Python, FastAPI, Streamlit, GPT-4o, Pinecone, OpenAI Embeddings, MySQL  
**GitHub**: https://github.com/Sarjak369/ai-shop-assistant

### Overview

Built a production-ready e-commerce chatbot that combines the power of GPT-4o with semantic search to deliver context-aware product recommendations.

### Architecture

- **Frontend**: Streamlit interactive chat interface
- **Backend**: FastAPI with RESTful endpoints
- **AI Layer**: GPT-4o for natural language understanding
- **Search**: Pinecone vector database with OpenAI embeddings
- **Data**: MySQL for structured product data

### Technical Highlights

- Integrated hybrid retrieval: vector search (semantic) + SQL (structured data)
- Achieved sub-second response times across 100+ catalog items
- Handles complex queries: "Show me red dresses under $100 with good reviews"
- Provides personalized recommendations based on conversation context

### Business Value

- Enhances customer experience with intelligent product discovery
- Reduces cart abandonment through instant, accurate assistance
- Scales to large product catalogs efficiently

---

## 5. CreditPredictor: ML-Based Credit Risk Classification

**Tech Stack**: Python, Flask, XGBoost, AWS EC2  
**GitHub**: https://github.com/Sarjak369/credit-risk-predictor

### Overview

Designed an end-to-end ML pipeline to forecast credit card default risk, helping financial institutions make data-driven lending decisions.

### Model Performance

- **Accuracy**: 85%
- **AUC Score**: 0.95
- **Algorithm**: XGBoost (selected after extensive model comparison)

### Pipeline Features

- Automated data ingestion and validation
- Preprocessing: handling missing values, outliers, feature scaling
- Customer clustering for segmented model training
- Hyperparameter optimization using grid search
- Real-time prediction API

### Deployment

- Hosted on AWS EC2 with Flask REST API
- 99.9% uptime SLA
- Enables proactive risk management for lenders
- Processes thousands of predictions per day

### Business Impact

- Reduces default rates through early risk identification
- Automates manual underwriting processes
- Provides explainable predictions for regulatory compliance

---

## 6. AdClickOptimizer: Predictive System for Ad Click-Through Rates

**Tech Stack**: Python, Flask, Random Forest, Logistic Regression, Statistical Analysis  
**GitHub**: https://github.com/Sarjak369/ad-click-optimizer

### Overview

Developed ML models to predict ad click-through rates with 96% accuracy, enabling advertisers to optimize their campaigns and maximize ROI.

### Technical Approach

- Compared multiple algorithms: Random Forest, Logistic Regression, Gradient Boosting
- Engineered time-based features: hour of day, day of week, seasonal patterns
- Applied statistical analysis to identify key drivers of click behavior
- Built interactive Flask web app for real-time predictions

### Key Features

- Real-time CTR predictions for new ad placements
- Feature importance analysis showing what drives clicks
- A/B testing framework for campaign optimization
- ROI calculator for advertising spend

### Business Results

- Improved ad performance by 10% through optimized targeting
- Empowered advertisers with data-driven placement strategies
- Reduced wasted ad spend on low-performing placements

---

## 7. WaferSense: Fault Detection for Semiconductor Manufacturing

**Tech Stack**: Python, Flask, Random Forest, SVM, XGBoost, AWS EC2  
**GitHub**: https://github.com/Sarjak369/wafer-fault-detection

### Overview

Developed an ML pipeline to detect faulty semiconductor wafers from 590+ sensor readings, addressing costly production downtime.

### Challenge

Manual wafer inspection is slow, expensive, and error-prone in semiconductor manufacturing.

### Solution

- Trained cluster-specific models (RF, SVM, XGBoost) on sensor data
- Achieved >92% accuracy and ROC AUC 0.96
- Automated data validation, preprocessing, and clustering
- Implemented model retraining pipeline for continuous improvement

### Deployment

- Flask REST API on AWS EC2
- Real-time fault isolation capabilities
- Reduces production line interruptions
- Enables predictive maintenance

### Manufacturing Impact

- Catches defects before reaching customers
- Reduces waste and rework costs
- Improves overall equipment effectiveness (OEE)

---

## 8. Dynamic SQL Assistant: Text-to-SQL

**Tech Stack**: Llama 3, LangChain, Groq, SQLite, Streamlit  
**Demo**: YouTube walkthrough available  
**GitHub**: https://github.com/Sarjak369/text-to-sql

### Overview

Built a Text-to-SQL tool that converts natural language questions into SQL queries, making data accessible to non-technical users.

### Key Features

- Uses Llama 3 + LangChain for natural language understanding
- Automatically creates SQL databases from CSV files and online datasets
- Handles complex queries with JOINs, aggregations, and filters
- Provides query explanations in plain English

### User Experience

- Intuitive Streamlit interface
- No SQL knowledge required
- Instant data insights from natural questions
- Examples: "What's our total revenue by region?" → Generates and executes SQL

### Impact

- Democratizes data access across organizations
- Reduces dependency on data analysts for simple queries
- Accelerates decision-making with instant insights

---

## 9. AI Doctor: Multimodal Medical Chatbot

**Tech Stack**: LLaMA 3 Vision, OpenAI Whisper, Groq, Gradio  
**Demo**: YouTube walkthrough available  
**GitHub**: https://github.com/Sarjak369/ai-doctor

### Overview

Developed a multimodal medical chatbot that processes text, images, and voice inputs to provide health-related information.

### Capabilities

- **Text Input**: Answer health questions in natural language
- **Image Input**: Analyze medical images (rashes, wounds, scans)
- **Voice Input**: Speech-to-text using Whisper for accessibility
- **Voice Output**: Text-to-speech responses

### Technical Stack

- LLaMA 3 Vision for multimodal understanding
- OpenAI Whisper for speech recognition
- Groq API for fast inference
- Gradio for user-friendly interface

### Results & Learnings

- Achieved accurate diagnoses for common conditions
- Identified need for fine-tuning on specialized medical datasets
- Demonstrates potential of AI in healthcare accessibility
- Important: Designed as educational tool, not medical advice

---

## 10. JobReachAI: Cold Email Generator for Business Development

**Tech Stack**: Llama 3.1, LangChain, Chroma DB, Streamlit  
**GitHub**: https://github.com/Sarjak369/job-reach-ai

### Overview

Built an AI tool that automates business development by extracting job listings and generating personalized outreach emails.

### Workflow

1. Extract job listings from company career pages
2. Analyze job requirements and skills needed
3. Match with portfolio projects from vector database
4. Generate personalized cold emails highlighting relevant experience

### Technical Implementation

- Web scraping for job listing extraction
- Chroma DB for portfolio project storage and retrieval
- Llama 3.1 for email generation
- LangChain for orchestration
- Streamlit for user interface

### Business Impact

- Automates cold outreach for service companies
- Increases response rates through personalization
- Saves hours of manual email drafting
- Scales outreach efforts efficiently

---

## 11. ThyroPredict: Thyroid Disorder Classification

**Tech Stack**: Python, Flask, KNN, Random Forest, AWS EC2  
**GitHub**: https://github.com/Sarjak369/thyroid-prediction

### Overview

Built ML pipeline to predict thyroid disorders across 4 categories: negative, compensated hypothyroid, primary hypothyroid, secondary hypothyroid.

### Model Performance

- Cluster-specific accuracies up to 92%
- ROC AUC scores up to 98%
- Best algorithm: KNeighborsClassifier

### Data Challenges Solved

- Handled severe class imbalance using RandomOverSampler
- Implemented KMeans clustering for dynamic data segmentation
- Automated null value imputation and feature engineering

### Healthcare Application

- Bulk patient predictions from CSV files
- Single-patient instant predictions
- CSV export for healthcare teams
- Hosted on AWS EC2 for 24/7 availability

---

## 12. Expense Tracker Web App

**Tech Stack**: Python, Streamlit, SQLite3, Plotly  
**Live**: Deployed on Streamlit Cloud  
**GitHub**: https://github.com/Sarjak369/expense-tracker

### Overview

Personal finance management app for tracking expenses, budgets, and shared finances.

### Features

- Multi-account management (personal, joint, savings)
- Expense categorization (food, transport, utilities, etc.)
- Monthly budget tracking and alerts
- Visualizations: pie charts, bar charts, trends
- CSV export functionality
- Email reports using smtplib

### User Experience

- Fully responsive design
- Intuitive interface built with Streamlit
- Real-time updates and calculations
- Cloud-based for access anywhere

### Personal Project

- Solves real-world personal finance tracking
- Demonstrates full-stack development skills
- Shows attention to UX and practical utility

---

## Project Categories Summary

**Generative AI & LLMs**: 5 projects (LangFlow-Viz, LogSenseAI, LinkedIn Generator, AI Doctor, JobReachAI)

**Machine Learning & Prediction**: 5 projects (CreditPredictor, AdClickOptimizer, WaferSense, ThyroPredict, AI Shop Assistant)

**Data Science & Analytics**: 2 projects (Dynamic SQL Assistant, Expense Tracker)

**All projects demonstrate**:

- End-to-end implementation (data → model → deployment)
- Production-ready code with API deployment
- Real-world business impact
- Modern tech stack and best practices
