from functions import *
import numpy as np
from datetime import datetime


# number of neurons in hidden layer
h = 50
# learning rate
beta = 0.2
# determine part of data set used for learning
n = 4


# load data from prepared datafiles
y0 = np.load("y0.npy")
yd = np.load("yd.npy")
results = np.load("results.npy")


# quality of result index
q = 0
# old value of q
oq = 0
# learning loop counter
counter = 0


# number of learning examples
data_count = np.shape(y0)[0]
lex = round(data_count * 4/5)
lex = 50


w1 = normal_random_matrix(0.0001, 0.001, h, 33, 0, 1)
w2 = normal_random_matrix(0.0001, 0.001, 4, h + 1, 0, 1)

# old values of w1 and w2 matrices
old_w1 = w1
old_w2 = w2

# learning loop
while True:
    p1 = 0 * w1
    p2 = 0 * w2

    # calculating derivatives in loop
    for i in range(lex):
        index = (i + round(n * data_count / 5)) % data_count
        # neural network calculations for 1 learning example
        s1 = multiply(w1, y0[index])
        y1 = activate_exp(s1)
        y1 = concat(y1, 1)
        y2 = multiply(w2, y1)
        # determining derivatives for 1 learning example and adding them to sum
        p2 = p2 + multiply(sub(y2, yd[index]), transpose(y1))
        p1 = p1 + multiply(derivative_exp(s1) * multiply(cut_last_row(transpose(w2)), sub(y2, yd[index])),
                           transpose(y0[index]))

    # medium derivative matrices
    p2 = (1 / lex) * p2
    p1 = (1 / lex) * p1
    # update w1 and w2 matrices
    w1 = sub(w1, beta * p1)
    w2 = sub(w2, beta * p2)

    # calculate quality index every 20000 iterations
    if counter % 1000 == 0:
        print(counter)
        # calculate quality index
        old_q = q
        q = 0
        for i in range(lex):
            # neural network calculations for 1 example
            index = (i + round(n * data_count / 5)) % data_count
            s1 = multiply(w1, y0[index])
            y1 = activate_exp(s1)
            y1 = concat(y1, 1)
            y2 = multiply(w2, y1)
            # quality index for 1 example
            mj = sub(y2, yd[index]) * sub(y2, yd[index])
            mjm = np.array([[1, 1, 1, 1, ]])
            # sum quality indexes of all examples
            q += np.matrix.item(multiply(mjm, mj), 0)/2
        q = q / lex
        print(q)
        print(q - old_q)

        # break condition
        if q < 0.03:
            break
    counter += 1


#displaying results
data = y0
counter = lex
n=1
start_point = round((4 + n) / 5 * data_count) % data_count
good = 0
bad = 0
average_error = 0
calculated_results = np.zeros(counter)
max_y2 = 0
min_y2 = 1
calculated_vectors = []
# calculating neural network result for data sets
for i in range(counter):
    index = (start_point + i) % data_count
    s1 = multiply(w1, data[index])
    y1 = activate_exp(s1)
    y1 = concat(y1, 1)
    y2 = multiply(w2, y1)
    if np.max(y2) > max_y2:
        max_y2 = np.max(y2)
    if np.min(y2) < min_y2:
        min_y2 = np.min(y2)
    calculated_vectors.append(y2)
for i in range(counter):
    index = (start_point + i) % data_count
    calculated_vectors[i] = (calculated_vectors[i] - min_y2) / (max_y2 - min_y2)
    # tresholding
    prev = np.copy(calculated_vectors[i])
    np.place(calculated_vectors[i], calculated_vectors[i] >= 0.5, 1)
    np.place(calculated_vectors[i], calculated_vectors[i] < 0.5, 0)
    # comparing results
    calc_result = np.sum(calculated_vectors[i])
    calculated_results[i] = calc_result
    result = results[index]
    average_error += (calc_result - result) ** 2
    if calc_result == result:
        good += 1
    else:
        print("BAD")
        print(index)
        print(prev)
        print(calculated_vectors[i])
        print(yd[index])
        print(results[index])
        bad += 1
average_error = np.sqrt(average_error / counter)
print("Good: " + str(good))
print("Bad: " + str(bad))
print("Average error: " + str(average_error))
