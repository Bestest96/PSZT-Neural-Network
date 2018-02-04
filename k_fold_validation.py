from functions import *
import numpy as np

# parameters used for learning
beta = 0.2
h = 50
n = 1

# filenames
name1txt = "w1_" + str(n) + "_" + str(h) + "_" + str(beta) + ".txt"
name2txt = "w2_" + str(n) + "_" + str(h) + "_" + str(beta) + ".txt"

# loading matrices
w1 = np.loadtxt(name1txt)
w2 = np.loadtxt(name2txt)

# define parameters and load results
data = np.load("y0.npy")
results = np.load("results.npy")
data_count = np.shape(data)[0]
counter = round(data_count / 5)

for n in range(5):
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
            bad += 1
    average_error = np.sqrt(average_error / counter)
    print("n: " + str(n))
    print("Good: " + str(good))
    print("Bad: " + str(bad))
    print("Average error: " + str(average_error))

