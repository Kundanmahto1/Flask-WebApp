import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# 1. Load the dataset
data = pd.read_csv("Bengaluru_House_Data.csv")

# 2. Preprocessing

# Function to handle ranges like "2100-2850" in total_sqft
def convert_sqft_to_num(x):
    try:
        tokens = str(x).split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        return float(x)
    except:
        return None

data['total_sqft'] = data['total_sqft'].apply(convert_sqft_to_num)

# Drop rows where we couldn't convert sqft
data = data.dropna()

# Create a new feature 'bhk' from 'size' column
data['bhk'] = data['size'].apply(lambda x: int(x.split(' ')[0]) if isinstance(x, str) else None)

# Drop rows where bhk is missing
data = data.dropna(subset=['bhk'])

# Drop unnecessary columns
data = data.drop(['availability', 'area_type', 'society', 'balcony', 'size'], axis=1)

# 3. Handling rare locations (group rare locations into "other")
location_stats = data['location'].value_counts()
location_less_than_10 = location_stats[location_stats <= 10]
data['location'] = data['location'].apply(lambda x: 'other' if x in location_less_than_10 else x)

# 4. Final Features
dummies = pd.get_dummies(data['location'], drop_first=True)

X = pd.concat([data[['total_sqft', 'bath', 'bhk']], dummies], axis=1)
y = data['price']

# 5. Train the model
model = LinearRegression()
model.fit(X, y)

# 6. Save the model and columns
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('columns.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

print("✅ Model and columns saved successfully!")
