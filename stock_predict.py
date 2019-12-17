import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os.path
from os import path
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


# Doc du lieu VCB 2009->2018
# Stock data from VCB 2009->2018
stock = "VIC"
dataset_train = pd.read_csv(stock + '_2009_2018.csv')
training_set = dataset_train.iloc[:, 1:2].values

# Thuc hien scale du lieu gia ve khoang 0,1
# Scale price data to [0, 1] range
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Tao du lieu train, X = 60 time steps, Y =  1 time step
# Create training data, X = 60 time steps, Y =  1 time step
X_train = []
y_train = []
no_of_sample = len(training_set)

for i in range(60, no_of_sample):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


# Xay dung model LSTM
# Build LSTM model
regressor = Sequential()
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units = 1))
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Neu ton tai file model thi load
# If model exists, then load it
if path.exists("mymodel.h5"):
    regressor.load_weights("mymodel.h5")
else:
    # Con khong thi train
    # Else, train new model
    regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)
    regressor.save("mymodel.h5")

# Load du lieu tu 1/1/2019 - 2/10/2019
# Load data 1/1/2019 - 2/10/2019
dataset_test = pd.read_csv(stock + '_2019.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

# Tien hanh du doan
# Predict
dataset_total = pd.concat((dataset_train['CLOSE'], dataset_test['CLOSE']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)

X_test = []
no_of_sample = len(inputs)

for i in range(60, no_of_sample):
    X_test.append(inputs[i-60:i, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Ve bieu do gia that va gia du doan
# Visualize using diagram
plt.plot(real_stock_price, color = 'red', label = 'Real ' + stock + ' Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted ' + stock + ' Stock Price')
plt.title(stock + ' Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel(stock + ' Stock Price')
plt.legend()
plt.show()

# Du doan tiep gia cac ngay tiep theo den 30/10
# Predict until 30/10

dataset_test = dataset_test['CLOSE'][len(dataset_test)-60:len(dataset_test)].to_numpy()
dataset_test = np.array(dataset_test)

inputs = dataset_test
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)


i = 0
while i<28:
    X_test = []
    no_of_sample = len(dataset_test)

    # Lay du lieu cuoi cung
    X_test.append(inputs[no_of_sample - 60:no_of_sample, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Du doan gia
    # Predict the price
    predicted_stock_price = regressor.predict(X_test)

    # chuyen gia tu khoang (0,1) thanh gia that
    # Convert from (0, 1) range to real price
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    # Them ngay hien tai vao
    # Add current day
    dataset_test = np.append(dataset_test, predicted_stock_price[0], axis=0)
    inputs = dataset_test
    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)

    print('Stock price ' + str(i+3) + '/10/2019 of VCB : ', predicted_stock_price[0][0])
    i = i +1

