import csv
import random
import numpy as np


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def calculate_average(a_list):
    a_sum = 0
    elems = 0

    for obj in a_list:
        if is_number(obj):
            a_sum += float(obj)
            elems += 1

    return a_sum / elems


def calculate_average_ignore_zero(a_list):
    a_sum = 0
    elements = 0

    for obj in a_list:
        if is_number(obj):
            if obj != '0':
                a_sum += float(obj)
                elements += 1
    return a_sum / elements


def calculate_sigma(a_list, a_average):
    a_max = float(calculate_max_num_value(a_list))
    a_sigma = max((a_max - a_average) / 3, 0.1)
    return a_sigma


def calculate_max_num_value(a_list):
    i = 0
    while not is_number(a_list[i]):
        i += 1
    a_max = a_list[i]
    for obj in a_list:
        if is_number(obj):
            if obj > a_max:
                a_max = obj
    return a_max


def change_to_numbers(a_list):
    for obj in range(len(a_list)):
        a_list[obj] = float(a_list[obj])


def simple_data_cover_unknown(a_list):
    a_average = round(calculate_average(a_list))
    a_sigma = calculate_sigma(a_list, a_average)
    for i in range(len(a_list)):
        if '?' == a_list[i]:
            a_list[i] = max(0, random.gauss(a_average, a_sigma))


def linked_data_cover_unknown(base_boolean_list, sub_list):
    base_average = calculate_average(base_boolean_list)
    sub_average = calculate_average_ignore_zero(sub_list)
    a_sigma = calculate_sigma(sub_list, sub_average)
    for i in range(len(base_boolean_list)):
        if '?' == base_boolean_list[i]:
            a_rnd = random.random()
            if a_rnd < base_average:
                base_boolean_list[i] = 1
                sub_list[i] = max(0, random.gauss(sub_average, a_sigma))
            else:
                base_boolean_list[i] = 0
                sub_list[i] = 0


def linked_data_cover_unknown2(base_boolean_list, sub_list1, sub_list2):
    base_average = calculate_average(base_boolean_list)
    sub1_average = calculate_average_ignore_zero(sub_list1)
    sub2_average = calculate_average_ignore_zero(sub_list2)
    a_sigma1 = calculate_sigma(sub_list1, sub1_average)
    a_sigma2 = calculate_sigma(sub_list2, sub2_average)
    for i in range(len(base_boolean_list)):
        if '?' == base_boolean_list[i]:
            a_rnd = random.random()
            if a_rnd < base_average:
                base_boolean_list[i] = 1
                sub_list1[i] = max(0, random.gauss(sub1_average, a_sigma1))
                sub_list2[i] = max(0, random.gauss(sub2_average, a_sigma2))
            else:
                base_boolean_list[i] = 0
                sub_list1[i] = 0
                sub_list2[i] = 0


def calculate_std_probability(a_list, has_std_list):
    a_sum = 0
    elems = 0

    for i in range(len(a_list)):
        if is_number(a_list[i]) and is_number(has_std_list[i]):
            if has_std_list[i] != '0':
                a_sum += float(a_list[i])
                elems += 1

    if elems != 0:
        return a_sum / elems
    else:
        return 0


def remove_uncertainty(reader):
    # read file
    list_of_lists = []

    for row in reader:
        parameter_list = []
        for i in range(len(row)):
            # print(row[i])
            parameter_list.append(row[i])

        list_of_lists.append(parameter_list)

# delete '?', change to float's
    # 1 age
    # 2 sexual partners
    simple_data_cover_unknown(list_of_lists[1])
    # 3 sexual intercourse
    simple_data_cover_unknown(list_of_lists[2])
    # 4 pregnancies
    simple_data_cover_unknown(list_of_lists[3])
    # 5 6 7 smokes
    linked_data_cover_unknown2(list_of_lists[4], list_of_lists[5], list_of_lists[6])
    # 8 9 Contraceptives
    linked_data_cover_unknown(list_of_lists[7], list_of_lists[8])
    # 10 11 IUD
    linked_data_cover_unknown(list_of_lists[9], list_of_lists[10])

    # 11 12 13 14 15 16 17 18 19 20 21 22 23 24 STDs
    avg = calculate_average(list_of_lists[11])
    std_number_average = round(calculate_average_ignore_zero(list_of_lists[12]))
    sigma = calculate_sigma(list_of_lists[12], std_number_average)
    probability_scale = []
    max_prob = 0
    # calculate chances of a specific diseases
    for i in range(13, 25):
        tmp = calculate_std_probability(list_of_lists[i], list_of_lists[11])
        # modify the chances when 0
        if tmp == 0:
            tmp += random.random() / 100
        max_prob += tmp
        probability_scale.append(max_prob)
    for i in range(len(list_of_lists[11])):
        if '?' == list_of_lists[11][i]:
            # random if person has STD
            rnd = random.random()
            if rnd < avg:
                std_number = max(0, random.gauss(std_number_average, sigma))
                list_of_lists[11][i] = 1
                list_of_lists[12][i] = std_number
                diseases_added = 0
                # What diseases???
                while diseases_added < std_number:
                    rnd = random.random() * max_prob
                    j = 0
                    while rnd > probability_scale[j]:
                        j += 1
                    if list_of_lists[13+j][i] != '1':
                        if 13+j == 21:
                            # if AIDS no possibility adding HIV - pick sth else
                            if list_of_lists[22][i] != '1' and std_number-diseases_added == 1:
                                continue
                            if list_of_lists[22][i] != '1':
                                list_of_lists[22][i] = '1'
                                diseases_added += 1

                        list_of_lists[13 + j][i] = '1'
                        diseases_added += 1
            else:
                list_of_lists[11][i] = 0
                list_of_lists[12][i] = 0
    for i in range(11, 25):
        for j in range(len(list_of_lists[i])):
            if '?' == list_of_lists[i][j]:
                list_of_lists[i][j] = 0

    # 25 26 27 STD:number of diagnosis
    for i in range(len(list_of_lists[26])):
        if '?' == list_of_lists[26][i]:
            list_of_lists[26][i] = 0
    for i in range(len(list_of_lists[27])):
        if '?' == list_of_lists[27][i]:
            list_of_lists[27][i] = 0

    # all - change to numbers
    for i in range(0, 37):
        change_to_numbers(list_of_lists[26])
    return list_of_lists


def get_xdata_vector_list():
    with open('DataTransp.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        data = remove_uncertainty(reader)

        vector_list = []
        for i in range(len(data[0])):
            vector = []
            for j in range(len(data)-5):
                a = data[j][i]
                a = float(a)
                vector.append(a)
            vector.append(1)
            vector_list.append(np.transpose(np.array([vector])))
        return vector_list


def get_ydata_vector_list():
    with open('DataTransp.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        data = remove_uncertainty(reader)

        vector_list = []
        for i in range(len(data[0])):
            vector = []
            for j in range(4):
                a = data[len(data)-5+j][i]
                a = float(a)
                vector.append(a)
            vector_list.append(np.transpose(np.array([vector])))
        return vector_list


def get_result():
    with open('DataTransp.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        data = remove_uncertainty(reader)

        vector_list = []
        for i in range(len(data[0])):
            a = data[len(data)-1][i]
            vector_list.append(int(a))
        return vector_list
