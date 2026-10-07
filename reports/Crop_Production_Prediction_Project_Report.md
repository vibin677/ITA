# CROP PRODUCTION AND YIELD PREDICTION USING MACHINE LEARNING IN PYTHON
## A PROJECT REPORT

*Submitted by*
- **DANIEL RAJ V** (311124205012)
- **ABHISHEK A** (311124205001)
- **KRITHIK PRIYAN M** (311124205302)
- **BENIYAL J** (311124205010)
- **BRYAN ROGER B** (311124205011)
- **ASHINTH R J** (311124205008)

*in partial fulfillment for the award of the degree of*
**BACHELOR OF TECHNOLOGY IN INFORMATION TECHNOLOGY**

**LOYOLA-ICAM COLLEGE OF ENGINEERING AND TECHNOLOGY, CHENNAI - 600034**  
**ANNA UNIVERSITY: 600025**  
**APRIL 2025**

---

## ANNA UNIVERSITY CHENNAI: 600025
### BONAFIDE CERTIFICATE

Certified that this project report **"CROP PRODUCTION AND YIELD PREDICTION USING MACHINE LEARNING IN PYTHON"** is the bonafide work of **DANIEL RAJ V (311124205012), ABHISHEK A (311124205001), KRITHIK PRIYAN M (311124205302), BENIYAL J (311124205010), BRYAN ROGER B (311124205011), ASHINTH R J (311124205008)** who carried out the project work under my supervision.

- **SUPERVISOR**: Dr. ANITHA E, M.E., PhD., Assistant Professor, Information Technology, Loyola-ICAM College of Engineering and Technology, Chennai-34
- **HEAD OF THE DEPARTMENT**: Ms. SHERRIL SOPHIE MARIA VINCENT, M.E., Assistant Professor, Information Technology, Loyola-ICAM College of Engineering and Technology, Chennai-34

Submitted for the project viva voce held on ......................................

- **INTERNAL EXAMINER**
- **EXTERNAL EXAMINER**

---

## ACKNOWLEDGEMENT

First of all, we are grateful to God for granting this opportunity and the capability to proceed successfully. Working on this project has been a rewarding experience.

We would like to extend our gratitude to our Principal, **Dr. L Anthony Michael Raj, M.E., Ph.D.**, for his motivating, constructive criticism and valuable guidance during the course of the project. We would like to express our sincere thanks to the Head of the Department and our Project coordinator **Ms. Sherril Sophie Maria Vincent, B.E., M.E.**, for her critical advice and guidance which was helpful in completion of the project.

We extend our sincere gratitude to our project guide **Dr. Anitha E, M.E., PhD.**, for providing valuable insights and resources leading to the successful completion of our project. We would also like to thank the faculty members of our department for their guidance which was indispensable for our work.

Last but not the least, we place a deep sense of gratitude to our family and friends who have been a constant source of inspiration during the preparation of this project.

---

## ABSTRACT

"Crop Production and Yield Prediction Using Machine Learning in Python" is a forward-thinking initiative that harnesses the transformative power of supervised machine learning and modern web technologies to address one of the foremost challenges facing modern agriculture: accurate forecasting of crop yield and production volumes. In an era where volatile climatic fluctuations, shifting precipitation patterns, and variable chemical input utilization drastically affect food security, agricultural decision-makers require accurate, data-driven forecasting tools rather than speculative heuristics to optimize resource allocation, mitigate economic risks, and secure food supply chains.

The study undertakes a comprehensive benchmark and comparative evaluation of five state-of-the-art regression algorithms—Linear Regression, Ridge Regression, Decision Tree Regressor, Random Forest Regressor, and Gradient Boosting Regressor—to evaluate their predictive effectiveness on multidimensional agricultural records comprising 1,805 field samples. Model performance is systematically assessed across standard evaluation metrics including Coefficient of Determination ($R^2$), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and 3-fold cross-validation. Among the tested algorithms, the Gradient Boosting Regressor distinguished itself as the champion model, attaining a superior $R^2$ score of 0.8134, an RMSE of 9.71 Tonnes/Ha, and an MAE of 6.43 Tonnes/Ha, significantly outperforming traditional linear models by capturing complex non-linear agro-climatic interactions.

The methodology is encapsulated within an end-to-end, high-performance web-based decision support system developed using Python, FastAPI, and an interactive frontend dashboard. The platform incorporates automated data preprocessing, real-time single and batch CSV predictions, economic revenue estimation based on Minimum Support Price (MSP) benchmarks, dynamic "what-if" sensitivity simulation across weather and fertilizer shifts, and personalized agronomic advisories. By bridging the gap between sophisticated machine learning research and practical agricultural deployment, this system offers an accessible, scalable tool for farmers, agricultural extension officers, and agribusiness stakeholders.

---

## TABLE OF CONTENTS

| Chapter Number | Title | Page Number |
| :--- | :--- | :--- |
| **1.** | **Introduction** | **1** |
| | 1.1 Background | 1 |
| | 1.2 Problem Statement | 1 |
| | 1.3 Motivation and Significance | 2 |
| | 1.4 Project Overview | 2 |
| | 1.5 System Functionality | 2 |
| | 1.6 Objectives | 3 |
| | 1.7 Design Philosophy and Approach | 3 |
| | 1.8 Broader Impact | 3 |
| | 1.9 Educational Value | 4 |
| | 1.10 Conclusion | 4 |
| **2.** | **Tools and Technologies Used** | **5** |
| | 2.1 Python Programming Language | 5 |
| | 2.2 Scikit-Learn Machine Learning Library | 5 |
| | 2.3 FastAPI Framework | 5 |
| | 2.4 Pandas and NumPy | 6 |
| | 2.5 Chart.js & Responsive Web UI | 6 |
| | 2.6 Joblib Model Persistence | 6 |
| | 2.7 Uvicorn ASGI Server | 6 |
| | 2.8 Visual Studio Code IDE | 6 |
| **3.** | **Market Analysis** | **7** |
| | 3.1 Industry Overview (Smart Farming & Agritech) | 7 |
| | 3.2 Target Market Analysis | 7 |
| | 3.3 Market Demand and Growth Potential | 7 |
| | 3.4 Customer Needs and Problem Identification | 8 |
| | 3.5 Competitive Analysis | 8 |
| | 3.6 Market Trends | 8 |
| | 3.7 Challenges and Risks | 9 |
| | 3.8 Overall Market Position | 9 |
| **4.** | **Task Implementation** | **10** |
| | 4.1 Introduction | 10 |
| | 4.2 Dataset Design and Preparation | 10 |
| | 4.3 Text and Numerical Data Preprocessing | 10 |
| | 4.4 Model Training Implementation | 11 |
| | 4.4.1 Loading Dataset & Pipeline Setup | 11 |
| | 4.4.2 Categorical One-Hot Encoding | 11 |
| | 4.4.3 Standard Feature Scaling | 11 |
| | 4.5 Multi-Model Regression Architecture | 12 |
| | 4.5.1 Linear, Ridge and Tree Models | 12 |
| | 4.5.2 Ensemble Gradient Boosting & Random Forest | 12 |
| | 4.6 Model Serialization & Persistence | 12 |
| | 4.7 Full-Stack Web Application Deployment & Testing | 13 |
| **5.** | **Results and Discussion** | **14** |
| | 5.1 Functional Performance | 14 |
| | 5.2 Natural Language & Input Handling | 14 |
| | 5.3 Accuracy and Reliability ($R^2$, RMSE, MAE) | 14 |
| | 5.4 User Interaction and Experience | 15 |
| | 5.5 System Limitations Observed | 15 |
| | 5.6 System Scalability and Future Enhancements | 16 |
| | 5.7 Overall Outcome | 16 |
| **6.** | **Conclusion** | **17** |
| **7.** | **References** | **18** |

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background
Agriculture is the primary livelihood for over 58% of India's population and contributes significantly to the national Gross Domestic Product (GDP). However, agricultural productivity is intrinsically vulnerable to agro-climatic variations, weather anomalies, and suboptimal input distribution. Farmers traditionally rely on historical intuition and empirical folklore to gauge expected yield. With climate change inducing irregular rainfall patterns and extreme temperatures, such conventional heuristics frequently lead to significant yield gaps, financial distress, and harvest losses. In this context, data-driven machine learning models offer a predictive foundation to forecast crop production prior to harvest.

### 1.2 Problem Statement
Modern agricultural decision-makers lack accessible, unified analytical tools that can simultaneously ingest multidimensional field features (e.g., rainfall, temperature, fertilizer application rates, pesticide dosages, cultivated area, crop type, and season) and produce precise, continuous production estimates. Existing agricultural software is either prohibitively complex, locked behind commercial proprietary licensing, or limited to simplistic linear assumptions that fail to reflect the non-linear biological thresholds governing plant growth.

### 1.3 Motivation and Significance
Accurate crop production forecasting provides vital intelligence across the agricultural spectrum. For farmers, it enables input optimization, cost reduction, and marketing strategies. For agricultural lenders and insurance underwriters, reliable yield predictions facilitate fair credit scoring and automated claims assessment. For governmental policymakers, aggregate production forecasts guide procurement strategies, Minimum Support Price (MSP) planning, and regional food security logistics.

### 1.4 Project Overview
The project, titled **Crop Production and Yield Prediction Using Machine Learning in Python**, establishes an end-to-end intelligent agricultural forecasting system. It encompasses data curation, exploratory data analysis, comparative benchmark of five machine learning regression algorithms, model serialization, a FastAPI-powered REST backend, and an interactive, user-centric web dashboard featuring dynamic sensitivity simulations and batch processing.

### 1.5 System Functionality
The system accepts eight essential agronomic variables: Cultivated Area (hectares), Rainfall (mm), Temperature (°C), Fertilizer Application (kg/ha), Pesticide Usage (kg/ha), Region/State, Crop Type, and Season. It produces predicted yield per hectare, aggregate production volume in tonnes, an agro-climatic suitability rating (0-100), financial economic estimations (gross revenue, input costs, and net farm profit), and tailored agronomic advisories.

### 1.6 Objectives
- To clean, curate, and preprocess a comprehensive dataset of 1,805 agricultural field records.
- To design and compare five distinct regression algorithms (Linear Regression, Ridge, Decision Tree, Random Forest, and Gradient Boosting) using rigorous validation metrics ($R^2$, RMSE, MAE, Cross-Validation).
- To select and serialize the champion ensemble model for ultra-low latency inference.
- To construct an asynchronous, modular REST API with FastAPI and deploy a responsive web interface equipped with real-time sensitivity analysis and batch CSV inference capabilities.

### 1.7 Design Philosophy and Approach
The system adheres to a decoupled client-server architectural philosophy. The machine learning pipeline is modularized into reusable preprocessing transformers, model training routines, and persistence modules. The backend exposes stateless RESTful endpoints, while the frontend leverages modern client-side rendering with Tailwind CSS and Chart.js, ensuring maximum responsiveness and platform independence.

### 1.8 Broader Impact
By providing open, democratized access to precision agriculture intelligence, the project empowers smallholder farmers and agricultural cooperatives to transition toward sustainable, data-informed cultivation practices, reducing fertilizer runoff and optimizing water resources.

### 1.9 Educational Value
This project integrates core concepts from Machine Learning, Data Science, Full-Stack Software Engineering, and Agronomy. It demonstrates practical implementations of supervised ensemble learning, pipeline orchestration, RESTful API design, and user-centric data visualization.

### 1.10 Conclusion
Chapter 1 delineates the overarching framework, technical justification, and societal relevance of automated crop production prediction, establishing the baseline for the implementation and evaluation detailed in subsequent chapters.

---

## CHAPTER 2: TOOLS AND TECHNOLOGIES USED

### 2.1 Python Programming Language
Python (Version 3.13) was selected as the core implementation language due to its extensive ecosystem of scientific computing, machine learning, and web development libraries. Python provides clean syntax, dynamic typing, and optimal performance when interfaced with C-optimized numeric libraries.

### 2.2 Scikit-Learn Machine Learning Library
Scikit-Learn was leveraged for machine learning pipeline construction, feature transformation (StandardScaler, OneHotEncoder, SimpleImputer, ColumnTransformer), model fitting, and quantitative evaluation. Scikit-Learn provides stable, optimized implementations of regression estimators and cross-validation utilities.

### 2.3 FastAPI Framework
FastAPI is a modern, high-performance web framework for building APIs with Python based on standard Python type hints and Starlette. It offers automatic request validation via Pydantic, high-throughput asynchronous execution, and automated interactive OpenAPI (Swagger) documentation generation.

### 2.4 Pandas and NumPy
NumPy provides support for large, multi-dimensional arrays and high-performance mathematical operations. Pandas provides flexible DataFrame data structures utilized for data cleaning, slicing, aggregation, anomaly remediation, and statistical feature analysis.

### 2.5 Chart.js & Responsive Web UI
The frontend user interface is built with responsive HTML5, Tailwind CSS, and Chart.js. Chart.js provides dynamic canvas-based visualizations including sensitivity response line curves, feature importance bar charts, and multi-dimensional agro-climatic radar plots.

### 2.6 Joblib Model Persistence
Joblib provides efficient serialization and deserialization of Python objects containing large NumPy arrays. It is utilized to persist the trained preprocessor pipeline and champion ensemble model to disk as a unified binary artifact.

### 2.7 Uvicorn ASGI Server
Uvicorn is a lightning-fast ASGI (Asynchronous Server Gateway Interface) server implementation for Python. It serves the FastAPI backend and static web assets with non-blocking I/O operations.

### 2.8 Visual Studio Code IDE
Visual Studio Code served as the integrated development environment (IDE), providing virtual environment debugging, Git version control, and PowerShell terminal integration.

---

## CHAPTER 3: MARKET ANALYSIS

### 3.1 Industry Overview (Smart Farming & Agritech)
The global Smart Agriculture and Agritech market is undergoing exponential expansion, driven by the convergence of IoT sensors, satellite imagery, and Artificial Intelligence. Market analysts project the global AI-in-agriculture sector to exceed $4.7 billion by 2028. In developing economies such as India, precision agriculture is recognized as an imperative to double farmer incomes and conserve vital natural resources.

### 3.2 Target Market Analysis
- **Commercial Farmers & Agricultural Collectives:** Seeking optimized input schedules and pre-harvest crop revenue forecasts.
- **Farmer Producer Organizations (FPOs):** Aggregating multi-farm acreage data for bulk marketing and crop planning.
- **Agri-Lending Institutions & Crop Insurers:** Requiring objective, empirical yield risk profiles for underwriting and credit disbursals.
- **Government Agricultural Extension Offices:** Monitoring regional food supply projections.

### 3.3 Market Demand and Growth Potential
Heightened weather volatility attributable to global climate anomalies has rendered traditional crop estimation techniques unreliable. Consequently, there is an urgent market demand for software tools that provide reliable 'what-if' simulations, allowing growers to assess climate vulnerability prior to sowing.

### 3.4 Customer Needs and Problem Identification
Agricultural users demand four core capabilities: (1) high predictive reliability without complex parameter tuning, (2) financial revenue translation from physical yield tonnes, (3) instant response times without cloud lock-in, and (4) actionable agronomic remediation guidance.

### 3.5 Competitive Analysis
Existing solutions typically fall into two extremes: either basic spreadsheet calculators with static yield averages or enterprise-grade ERP systems that cost thousands of dollars and require specialized training. The proposed AgroPredict AI system bridges this divide by delivering state-of-the-art machine learning accuracy through a frictionless, zero-cost web dashboard.

### 3.6 Market Trends
Key prevailing trends include the adoption of explainable AI (XAI) so end-users understand the rationale behind predictions, API-first architecture for interoperability with government portals, and automated batch processing for regional surveys.

### 3.7 Challenges and Risks
Principal market challenges include digital literacy barriers among rural farming communities, irregular internet bandwidth in remote locations, and localized soil composition variations that require continuous retraining.

### 3.8 Overall Market Position
The developed solution occupies a unique value position by pairing high-performance ensemble regression with localized Indian Minimum Support Price (MSP) economic projections and automated batch analysis.

---

## CHAPTER 4: TASK IMPLEMENTATION

### 4.1 Introduction
This chapter details the engineering methodology, architectural pipeline, data preprocessing mechanisms, model training protocols, and full-stack software deployment implemented in the project.

### 4.2 Dataset Design and Preparation
The dataset was designed to reflect genuine agricultural agro-climatic conditions across India. An initial raw sample dataset of 500 records was cleansed of negative target yield artifacts and expanded with statistically verified agricultural records calibrated against Indian Council of Agricultural Research (ICAR) benchmarks, producing a robust corpus of 1,805 records.

| Feature Name | Type | Unit / Domain | Agronomic Significance |
| :--- | :--- | :--- | :--- |
| **Area** | Numeric | Hectares (ha) | Cultivated acreage of the agricultural plot |
| **Rainfall** | Numeric | Millimeters (mm) | Seasonal / annual precipitation level |
| **Temperature** | Numeric | Celsius (°C) | Mean temperature during crop growth cycle |
| **Fertilizer** | Numeric | kg / hectare | Combined chemical nutrient dosage (NPK) |
| **Pesticide** | Numeric | kg / hectare | Chemical protection / pest application rate |
| **State** | Categorical | 11 Indian States | Geographic & agro-ecological zone indicator |
| **Crop** | Categorical | 8 Major Crops | Specific crop species being cultivated |
| **Season** | Categorical | Kharif, Rabi, Whole Year | Cropping season and climatic period |
| **Yield** | Numeric (Target) | Tonnes / Hectare | Observed crop productivity rate |

### 4.3 Text and Numerical Data Preprocessing
A two-branch Scikit-Learn `ColumnTransformer` was engineered:
- **Numeric Pipeline:** Numerical features (Area, Rainfall, Temperature, Fertilizer, Pesticide) are processed through a `SimpleImputer(strategy='median')` to handle potential missing values robustly against outliers, followed by a `StandardScaler()` to standardize features to zero mean and unit variance.
- **Categorical Pipeline:** Categorical features (State, Crop, Season) are imputed via `SimpleImputer(strategy='most_frequent')` and encoded using `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`, producing clean orthogonal binary vectors without introducing false ordinal hierarchies.

### 4.4 Model Training Implementation
The preprocessed data was partitioned into an 80% training set (1,444 samples) and a 20% test set (361 samples) using a fixed random seed (42) for deterministic reproducibility. Five diverse regression algorithms representing linear, tree-based, and ensemble paradigms were trained and evaluated on identical splits.

### 4.5 Multi-Model Regression Architecture
1. **Linear Regression:** Computes ordinary least squares estimates, serving as an interpretable baseline.
2. **Ridge Regression:** Introduces an L2 Tikhonov regularization penalty to mitigate multicollinearity among weather and acreage variables.
3. **Decision Tree Regressor:** Partitions the feature space into hyper-rectangles using recursive variance reduction.
4. **Random Forest Regressor:** An ensemble of 150 randomized decision trees operating via bootstrap aggregation (bagging) to minimize predictive variance.
5. **Gradient Boosting Regressor:** Builds an additive ensemble of 150 regression trees in a forward stage-wise manner, optimizing mean squared error loss via gradient descent in function space.

### 4.6 Model Serialization & Persistence
Following comparative evaluation, the champion model along with its fitted preprocessor pipeline, feature names, and evaluation metrics were bundled into a unified binary file (`best_crop_model.joblib`) for zero-overhead production inference.

### 4.7 Full-Stack Web Application Deployment & Testing
The backend is encapsulated in a high-concurrency FastAPI application providing asynchronous REST endpoints: `/api/predict` for single field predictions, `/api/predict/sensitivity` for response curves, `/api/predict/batch` for CSV uploads, and `/api/models/comparison` for leaderboard metadata. The frontend renders real-time calculations without requiring client page reloads.

---

## CHAPTER 5: RESULTS AND DISCUSSION

### 5.1 Functional Performance
The end-to-end platform was comprehensively verified via an automated test suite comprising 9 unit and integration tests written in pytest. The server consistently executed end-to-end model inference, financial valuation, and agronomic advisory generation in under 25 milliseconds per request.

### 5.2 Accuracy and Reliability ($R^2$, RMSE, MAE)

| Algorithm | Test $R^2$ Score | RMSE (T/ha) | MAE (T/ha) | 3-Fold CV $R^2$ | Model Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | **0.8134** | **9.71** | **6.43** | **0.7822** | 🏆 **Champion (Selected)** |
| **Random Forest** | 0.7856 | 10.41 | 6.77 | 0.7706 | Runner-Up |
| **Linear Regression** | 0.7445 | 11.36 | 8.00 | 0.7320 | Baseline |
| **Ridge Regression** | 0.7444 | 11.37 | 8.01 | 0.7322 | Regularized Linear |
| **Decision Tree** | 0.6561 | 13.18 | 8.50 | 0.6453 | Overfitted Baseline |

**Interpretation of Metrics:**
- **Gradient Boosting** achieved the highest explanatory power ($R^2 = 0.8134$), accounting for over 81.3% of the total variance in crop yield.
- Tree ensembles drastically outperformed single decision trees, reducing RMSE from 13.18 to 9.71 Tonnes/Ha.
- **Feature Importance Analysis:** Relative Gini importance rankings established that **Fertilizer Application (59.96%)**, **Crop Type (10.83%)**, **Temperature (8.15%)**, and **Cultivated Area (7.62%)** represent the primary predictive determinants of crop yield.

### 5.3 Sensitivity Analysis Outcomes
The interactive sensitivity analyzer confirmed non-linear crop response curves. For instance, in wheat cultivation, increasing rainfall up to 750 mm yielded a steady increase in productivity, while precipitation exceeding 1,200 mm demonstrated diminishing returns due to root aeration inhibition.

### 5.4 Economic Valuation & Advisory Accuracy
By binding forecasted production volumes with actual Indian Minimum Support Price (MSP) benchmarks (e.g., Wheat at ₹22,750/tonne, Rice at ₹23,000/tonne, Cotton at ₹71,200/tonne), the system produced realistic financial projections and net farm profit estimates.

### 5.5 User Interaction and Experience
The interface was evaluated for accessibility and responsiveness. Sliders and input boxes remained bidirectionally synchronized, one-click presets loaded complex regional scenarios instantaneously, and batch CSV predictions processed 100 rows in less than 0.12 seconds.

### 5.6 System Limitations Observed
Current model predictions do not yet incorporate real-time micro-satellite NDVI vegetation index feeds or daily soil moisture telemetry. Predictions assume standard weed management and absence of catastrophic pest swarms.

### 5.7 System Scalability and Future Enhancements
Future architectural enhancements will integrate live meteorological weather API streams, satellite spectral imagery via Sentinel-2, and multilingual audio interfaces (Tamil, Hindi) for rural accessibility.

### 5.8 Overall Outcome
The successful completion and empirical validation of this mini project demonstrate that supervised ensemble learning provides an accurate, viable mechanism for agricultural yield forecasting.

---

## CHAPTER 6: CONCLUSION

The project **"Crop Production and Yield Prediction Using Machine Learning in Python"** has successfully conceptualized, developed, and validated an intelligent decision support system tailored for modern agriculture.

Through systematic experimental evaluation of five regression estimators, Gradient Boosting was substantiated as the champion algorithm, demonstrating an $R^2$ score of 0.8134 and superior generalization across diverse crops and agro-climatic zones. The deployment of this model via an asynchronous FastAPI backend and a responsive single-page web dashboard delivers an intuitive, accessible experience for farmers and agricultural researchers.

By translating raw statistical predictions into actionable agronomic guidance and farm economics metrics, the platform bridges the divide between machine learning theory and field-level agricultural practice. The resulting application stands as a robust, production-ready solution capable of enhancing agricultural productivity, mitigating economic uncertainty, and supporting global food security initiatives.

---

## CHAPTER 7: REFERENCES

- **[1]** J. Friedman, 'Greedy Function Approximation: A Gradient Boosting Machine,' *The Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.
- **[2]** L. Breiman, 'Random Forests,' *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
- **[3]** F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python,' *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
- **[4]** Directorate of Economics and Statistics, Ministry of Agriculture and Farmers Welfare, 'Agricultural Statistics at a Glance,' Government of India, 2023.
- **[5]** S. V. Manivasagam and M. S. Saravanan, 'Machine Learning Approaches for Crop Yield Prediction: A Comprehensive Review,' *Computers and Electronics in Agriculture*, vol. 185, p. 106132, 2021.
- **[6]** S. Ramírez, 'FastAPI Documentation and Best Practices for High-Performance Python Web APIs,' 2024. [Online]. Available: https://fastapi.tiangolo.com/
- **[7]** Food and Agriculture Organization (FAO), 'World Food and Agriculture – Statistical Yearbook 2023,' United Nations, Rome, 2023.
- **[8]** Indian Council of Agricultural Research (ICAR), 'Handbook of Agriculture: Facts and Figures for Farmers, Students and All Interested in Farming,' 6th ed., New Delhi, 2022.
- **[9]** A. Chlingaryan, S. Sukkarieh, and B. Whelan, 'Machine Learning Approaches for Crop Yield Prediction and Nitrogen Status Estimation in Precision Agriculture: A Review,' *Computers and Electronics in Agriculture*, vol. 151, pp. 61–69, 2018.
- **[10]** W. McKinney, 'Data Structures for Statistical Computing in Python,' in *Proc. 9th Python in Science Conf. (SciPy)*, 2010, pp. 56–61.
