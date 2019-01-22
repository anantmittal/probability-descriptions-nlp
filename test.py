# Complete the function below.


def create_matrix(temperature, num_of_days):
    mat = []

    num_of_days = int(len(temperature) / 24)

    for i in range(0, num_of_days):
        temp_list = []
        for temp in temperature:
            temp_list.append(temp)
        mat.append(temp_list)
    return mat


def predictTemperature(startDate, endDate, temperature, n):
    # Take care of constraints if time is left

    ret = [0] * 24 * n
    mat = []

    num_of_days = int(len(temperature) / 24)

    for i in range(0, num_of_days):
        temp_list = []
        for temp in temperature:
            temp_list.append(temp)
        mat.append(temp_list)

    big_temperature = []

    for new_d in range(0, n):
        for hour in range(0, 24):
            total_temp = 0
            for num_day in range(0, num_of_days):
                total_temp += mat[num_day][hour]
            ret[hour + new_d * 24] = total_temp / num_of_days
    return ret




