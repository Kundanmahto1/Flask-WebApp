from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model and column names
model = pickle.load(open('model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        sqft = float(request.form['total_sqft'])
        bath = int(request.form['bath'])
        bhk = int(request.form['bhk'])
        location = request.form['location']

        # Create input vector
        x = np.zeros(len(columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk

        if location in columns:
            loc_index = columns.index(location)
            x[loc_index] = 1

        prediction = model.predict([x])[0]
        return render_template('index.html', prediction_text=f'Estimated Price: ₹ {round(prediction, 2)} Lakhs')
    except:
        return render_template('index.html', prediction_text="Error in input. Please try again.")

if __name__ == "__main__":
    app.run(debug=True)
