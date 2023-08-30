from flask import Flask, render_template, request
import tensorflow as tf
from keras.layers import TextVectorization
import pandas as pd
import numpy as np

df = pd.read_csv('train.csv')
app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    model = tf.keras.models.load_model('toxic.h5')
    X = df['comment_text']
    MAX_FEATURES = 200000
    vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=1800,
                               output_mode='int')
    vectorizer.adapt(X.values)
    
    if request.method == 'POST':
        comment = request.form['comment']
        vector_comment = vectorizer([comment])
        results = model.predict(vector_comment)
        text = {}
        for idx, col in enumerate(df.columns[2:]):
            text[col] = results[0][idx]
        keys = ["Toxic", "Severe Toxic", "Obsence", "Threat", "Insult", "Identity Hate"]
        values = list(text.values())
    return render_template('predictions.html',keys=keys,values=values)
        


if __name__ == '__main__':
    app.run(debug=False)