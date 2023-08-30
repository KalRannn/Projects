import tensorflow as tf
from keras.layers import TextVectorization
import pandas as pd
import numpy as np
df = pd.read_csv('train.csv')
model = tf.keras.models.load_model('toxic.h5')
X = df['comment_text']
comment='You fucking suck you asshole'
MAX_FEATURES = 200000
vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=1800,
                               output_mode='int')
vectorizer.adapt(X.values)

vector_comment = vectorizer([comment])
results = model.predict(vector_comment)
text = {}
for idx, col in enumerate(df.columns[2:]):
    text[col] = results[0][idx]
    
print(list(text.keys()))
print(list(text.values()))