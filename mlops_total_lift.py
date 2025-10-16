#used Google Gemini for this assignment
import pandas as pd
import glob
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import make_scorer, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import boto3


#functions

def data_clean(data):    
    # Remove not relevant columns
    data = data.dropna(subset=['region','age','weight','height','howlong','gender','eat', \
                               'train','background','experience','schedule','howlong', \
                               'deadlift','candj','snatch','backsq','experience',\
                               'background','schedule','howlong'])
    data = data.drop(columns=['affiliate','team','name','athlete_id','fran','helen','grace',\
                              'filthy50','fgonebad','run400','run5k','pullups','train'])

    # Remove Outliers

    data = data[data['weight'] < 1500]
    data = data[data['gender'] != '--']
    data = data[data['age'] >= 18]
    data = data[(data['height'] < 96) & (data['height'] > 48)]

    data = data[(data['deadlift'] > 0) & (data['deadlift'] <= 1105)|((data['gender'] == 'Female') \
                 & (data['deadlift'] <= 636))]
    data = data[(data['candj'] > 0) & (data['candj'] <= 395)]
    data = data[(data['snatch'] > 0) & (data['snatch'] <= 496)]
    data = data[(data['backsq'] > 0) & (data['backsq'] <= 1069)]

    # Clean Survey Data

    decline_dict = {'Decline to answer|': np.nan}
    data = data.replace(decline_dict)
    data = data.dropna(subset=['background','experience','schedule','howlong','eat'])
    data['total_lift'] = data['deadlift'] + data['candj'] + data['snatch'] + data['backsq']
    return data

def feature_engineering(data):
    data['is_female'] = (data['gender'] == 'Female').astype(int)
    data_trimmed = data[['is_female', 'age', 'weight', 'height','total_lift']]
    X = data[['is_female', 'age', 'weight', 'height']]
    Y = data['total_lift']
    return X, Y, data_trimmed

def train_and_test_model(X,Y):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    pipeline = Pipeline([
        ('regressor', LinearRegression())  # You can replace LinearRegression with other models
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    return {'R2 Score': r2, 'Mean Squared Error': mse}


def run_eda(df):
    print(df.describe())
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_lift'], kde=True)
    plt.title('Distribution of total_lift in')
    plt.show()


#comment this out after running
#raw = pd.read_csv('athletes.csv')

#clean_data = data_clean(raw)
#clean_data.to_csv('athletes_v2.csv')


#DVC version
file_list = glob.glob('athlete*.csv')

if file_list:
    data = pd.read_csv(file_list[0])
else:
    print("No matching file found!")


#lake fs version

def load_version_lakefs(version,file):
    repo = "mlops-assignment-1"
    endpoint = 'http://localhost:8000'
    access_key = 'AKIAIOSFOLQUICKSTART'
    secret_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    path = f"s3://{repo}/{version}/{file}.csv"

    df = pd.read_csv(path, storage_options ={
        "key" : access_key,
        "secret" : secret_key,
        "client_kwargs" : {"endpoint_url":endpoint},
    })
    return df

data = load_version_lakefs('V1','athletes')

X, Y, data_trimmed = feature_engineering(data)
run_eda(data_trimmed)
results = train_and_test_model(X,Y)
print(results)