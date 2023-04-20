# Flight-Analysis-Data-Mining-Project

Team member: Xinan Wang, Gaohaonan He, Zhiqing Wang, Wenwei Li

## Project Title: Flight Ticket & Status Analysis

The goal of our analysis is to develop a machine learning model that predicts flight prices and delays accurately. The purpose of this project is to assist travelers in making informed decisions about their travel plans by providing reliable predictions about the cost of air travel and potential delays. By entering information such as the desired travel dates and destinations, our application will generate predictions on flight prices and delays, enabling travelers to plan their trips more effectively.

The significance of this project lies in the fact that it can help travelers save money by predicting the best time to book a flight and avoid potential disruptions caused by flight delays. In turn, this can have a significant impact on the travel industry, which generates billions of dollars in revenue each year.

In conclusion, our project aims to provide travelers with reliable predictions on flight prices and delays, allowing them to plan their trips more effectively. By using data science and machine learning techniques, we can develop models that accurately predict flight prices and delays, benefiting both travelers and the travel industry.

## Project Application Link

Here's our project application link: https://nannmemeda-flight-analysis-data-mining-project-app-3w7qhj.streamlit.app/

Our application consists of two main parts. The first part is dedicated to flight search and price prediction. It provides flight recommendations and price prediction to the users. The second part of the application is a flight delay probability calculator that calculates the probability of flight delays for the user. This part also provides information on the delay probability for each state.

## Source Code Introduction

 - Sampled Datasets
 
    - [flight_data.csv](https://www.kaggle.com/datasets/polartech/flight-data-with-1-million-or-more-records)
    
    - [Combined_Flights.csv](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022)
    
 - Machine Learning Model & Data Analysis
    
    - Price Prediction Model: [Project Price Prediction Model.ipynb](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/Project%20Model.ipynb)
    
    - Exported model: RF.joblib
    
    - Flight Delay Analysis: [flight_delay_analysis.ipynb](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/flight_delay_analysis.ipynb)
    
    - Worse cases of delay: [worse case.ipynb](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/worst%20case.ipynb)
    
 - Streamlit Application Source Code
 
    - ✈️ Flight Analysis (main file): [app.py](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/app.py)
    
    - 🛩️ Flight Search & Price Prediction Page: [flight_price.py](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/flight_price.py)
    
    - ⏰ Flight Delay Probability Calculator Page: [delay.py](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/delay.py)
    
    - Application pictures: 1) cute_flight.png  2) flight_bar.png
    
 - Project Report
 
    - [Flight Analysis Final Report](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/Flight%20Analysis%20Final%20Report.pdf)
    
 - Docker File
 
    - [Dockerfile](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/Dockerfile)
    
    - requirements.txt
    
 - Data Sampling Files
 
    - [trans_1.py](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/trans_1.py)
    
    - [trans_2.py](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project/blob/main/trans_2.py)
    
 ## Summary
 
In conclusion, our analysis demonstrates that the Random Forest Regressor is the most effective model for predicting flight prices based on the available data. However, there is potential for improvement through feature engineering, hyperparameter tuning, model stacking, and exploring alternative models. By implementing these recommendations, we can enhance the accuracy of our predictions and provide more reliable estimates for users seeking to make informed decisions about their flight bookings.
