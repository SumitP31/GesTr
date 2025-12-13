# sum_module.py
from arduino_reader import start_readers, read_combined
import threading
import time
# import tensorflow as tf
# from tensorflow import keras
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings("ignore")

n=8  # number of values per Arduino
model = joblib.load("random_forest_model_8.joblib")

# Use it
# prediction = model.predict([[1.2, 3.4, 5.6]])



total = None  # exported
# model = tf.keras.models.load_model('my_model.keras')

# # Show the model architecture
# new_model.summary()



def _process():
    global total
    for values in read_combined():
        # print(values[0])
        x = np.array(values, dtype=np.float32)
        x_ = x.reshape(1, n*2)   # add batch dimension
        y = model.predict(x_)
        # print("Predicted letter index:", y[0])
        # print(np.argmax(model.predict(x_), axis=1))
        total = chr(ord('A') + y[0])  # to string
        # print("Predicted letter:", total)

def start():
    # time.sleep(1)  # wait for serial connections
    start_readers()
    t = threading.Thread(target=_process)
    t.daemon = True
    t.start()
