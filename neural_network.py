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


# quality of result index
q = 0
# old value of q
oq = 0
# learning loop counter
counter = 0


# number of learning examples
data_count = np.shape(y0)[0]
lex = round(data_count * 4/5)

# log files
name_1 = "w1_new_" + str(n) + "_" + str(h) + "_" + str(beta) + ".txt"
name_2 = "w2_new_" + str(n) + "_" + str(h) + "_" + str(beta) + ".txt"
name_log = "nn_new_" + str(n) + "_" + str(h) + "_" + str(beta) + ".txt"
log_file = open(name_log, "a")

# try to open files with matrices, if error create new, random matrices
try:
    w1 = np.loadtxt(name_1)
    w2 = np.loadtxt(name_2)
except IOError:
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
    if counter % 20000 == 0:
        print(str(datetime.now()) + " " + str(n) + "_" + str(h) + "_" + str(beta))
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

        np.savetxt(name_1, w1)
        np.savetxt(name_2, w2)
        log_file.write(str(datetime.now()) + "\n")
        log_file.write(str(counter) + "\n")
        log_file.write(str(q) + "\n")
        log_file.write(str(q - old_q) + "\n")
        log_file.write("\n")
        log_file.flush()

        # break condition
        if q < 0.01:
            break
    counter += 1
