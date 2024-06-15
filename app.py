import pickle
import pandas as pd
import numpy as np
import xgboost
from xgboost import XGBRegressor
from flask import Flask, render_template, request
import sklearn

app = Flask(__name__)

with open('final_model1.pkl', 'rb') as f:
    model1 = pickle.load(f)

with open('final_model2.pkl', 'rb') as f:
    model2 = pickle.load(f)

@app.route('/')
def index():
    cities = ['Dubai',
        'Colombo',
        'Mirpur',
        'Abu Dhabi',
        'Johannesburg',
        'London',
        'Harare',
        'Auckland',
        'Cape Town',
        'Pallekele',
        'Barbados',
        'Hamilton',
        'Sydney',
        'Melbourne',
        'Chittagong',
        'Durban',
        'St Lucia',
        'Wellington',
        'Nottingham',
        'Al Amarat',
        'Dublin',
        'Sharjah',
        'Lauderhill',
        'Centurion',
        'Manchester',
        'Nagpur',
        'Lahore',
        'Mumbai',
        'Dhaka',
        'Southampton',
        'Sylhet',
        'Edinburgh',
        'Mount Maunganui',
        'Kolkata',
        'Hambantota',
        'Greater Noida',
        'Delhi',
        'Trinidad',
        'Guyana',
        'Chandigarh',
        'Adelaide',
        'Bangalore',
        'St Kitts',
        'Rotterdam',
        'Cardiff',
        'Christchurch']
    teams = [
        'Pakistan',
        'South Africa',
        'India',
        'New Zealand',
        'Sri Lanka',
        'West Indies',
        'Australia',
        'England',
        'Afghanistan',
        'Bangladesh',
        'Ireland',
        'Zimbabwe',
        'Netherlands',
        'United Arab Emirates',
        'Scotland',
        'Oman',
        'Nepal',
        'Papua New Guinea',
        'Canada',
        'Namibia',
        'United States of America',
        'Uganda'    
    ]

    return render_template('index.html', cities = cities, teams= teams)

@app.route('/submit', methods=['POST'])
def submit():
    batting_team = request.form['batting_team']
    bowling_team = request.form['bowling_team']
    city = request.form['city']
    overs = int(request.form['overs'])
    last_5_overs_score = int(request.form['last_5_overs_score'])
    current_score = int(request.form['current_score'])
    current_wickets = int(request.form['current_wickets'])
    last_5_overs_wickets = int(request.form['last_5_overs_wickets'])
    innings = int(request.form['innings'])
    target = request.form.get('target')
    rr = float(current_score)/ float(overs)
    ballsleft = 120-overs*6
    wicketsleft = 10-current_wickets
    rrr = 0.0

    if target:
        target = int(target)
        rrr = float(target-current_score)/float(20-overs)
    else:
        target = None
    
    
    if innings==1:
        input = pd.DataFrame({'batting_team': [batting_team], 
                              'bowling_team': [bowling_team], 
                              'city': [city], 
                              'cumulative_runs': [current_score], 
                              'ballsleft': [ballsleft],  
                              'cumulative_wickets': [current_wickets],
                              'rr': [rr],
                              'last5': [last_5_overs_score], 
                              'wicketsleft':[wicketsleft], 
                              'last5w': [last_5_overs_wickets],
                            })
        result = model1.predict(input)
        result = result[0]
        result = int(result)
        a = (f"{batting_team} will make {result} runs in the 1st innings")
    elif innings==2:
        input = pd.DataFrame({'batting_team': [batting_team], 
                              'bowling_team': [bowling_team], 
                              'city': [city], 
                              'cumulative_runs': [current_score], 
                              'ballsleft': [ballsleft],  
                              'rr': [rr],
                              'last5': [last_5_overs_score], 
                              'wicketsleft':[wicketsleft], 
                              'last5w': [last_5_overs_wickets],
                              'target': [target],
                              'rrr': [rrr]
                              })
        result = model2.predict(input)
        result = result[0]
        runsmade = result*20
        runsmade = int(runsmade)
        a=""
        win = int(target/result)+1
        loss = target-runsmade
        if runsmade>=target:
            a = f"{batting_team} will win in the {win}th over against {bowling_team}"
        else:
            a = (f"{batting_team} will lose to {bowling_team} by {loss} runs. Their total will be {runsmade}")

    

    

    return render_template('result.html', a=a)
    

if __name__ == '__main__':
    app.run(debug=True)
p1 = pickle.load(open('final_model1.pkl', 'rb'))
p1 = pickle.load(open('final_model2.pkl', 'rb'))