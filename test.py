a = [[1, 2], [2, 3], [3, 4]]
print(a)
print([row[0] for row in a])
print([row[1] for row in a])

#[row[0] for row in a] = [row[0] for row in a] + 1

print([row[0] for row in a] * 2 )

print(a[0:2][1])
col = []
for r in a:
	col.append(r[1])
	r[1] = r[1] + 1

print(col)
print(a)


print(sorted(a,key=lambda l:l[1], reverse=True))

# from keras.datasets import mnist
# from keras.utils import to_categorical
# from keras.models import Sequential
# from keras.layers import Flatten, Dense, Activation

# # raw keras
# from livelossplot import PlotLossesKeras

# # tensorflow.keras
# # from livelossplot import PlotLossesKerasTF


# # data loading
# (X_train, y_train), (X_test, y_test) = mnist.load_data()


# # data preprocessing
# Y_train = to_categorical(y_train)
# Y_test = to_categorical(y_test)
# X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.
# X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255.


# model = Sequential()

# model.add(Flatten(input_shape=(28, 28, 1)))
# model.add(Dense(10))
# model.add(Activation('softmax'))

# model.compile(optimizer='rmsprop',
#               loss='categorical_crossentropy',  # 'mean_squared_error'
#               metrics=['accuracy', 'mean_squared_error'])


# plotlosses = PlotLossesKeras()


# model.fit(X_train, Y_train,
#           epochs=10,
#           validation_data=(X_test, Y_test),
#           callbacks=[plotlosses],
#           verbose=False)

