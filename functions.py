import numpy as np


def multiply(m1, m2):
    return np.dot(m1, m2)


def add(m1, m2):
    return np.add(m1, m2)


def sub(m1, m2):
    return np.subtract(m1, m2)


def concat(m1, elem):
    to_concat = np.array([elem], ndmin=2)
    return np.concatenate((m1, to_concat), axis=0)


def cut_last_row(m1):
    return m1[:np.shape(m1)[0] - 1][:]


def activate_exp(x):
    return np.exp(x)/(1 + np.exp(x))


def activate_arctan(x):
    return np.arctan(x)


def derivative_exp(x):
    return np.exp(x)/np.power(1 + np.exp(x), 2)


def derivative_arctan(x):
    return 1/(np.power(x, 2) + 1)


def transpose(x):
    return np.transpose(x)


def normal_random_value(m, s, min_val=-np.inf, max_val=np.inf):
    value = np.random.normal(m, s, (1, 1))
    np.place(value, value > max_val, max_val)
    np.place(value, value < min_val, min_val)
    return value[0][0]


def normal_random_matrix(m, s, rows, columns, min_val=-np.inf, max_val=np.inf):
    matrix = np.random.normal(m, s, (rows, columns))
    np.place(matrix, matrix > max_val, max_val)
    np.place(matrix, matrix < min_val, min_val)
    return matrix






