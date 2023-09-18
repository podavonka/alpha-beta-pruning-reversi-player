import copy

def transpose(data):
    temp_data = [list(i) for i in zip(*data)]
    return temp_data


def line_size(r,c,data):

    temp_data = copy.deepcopy(data)
    temp_data[r][c] = 'T'

    target = data[r][c]
    row = data[r]

    counter = 0

    for i in range(c+1, len(data[r])):
        if data[r][i] == target:
            temp_data[r][i] = '#'
            counter += 1
        else:
            break
    print(temp_data[r])

    for i in range(c, -1, -1):
        if data[r][i] == target:
            temp_data[r][i] = '#'
            counter += 1
        else:
            break

    for row in temp_data:
        for i in row:
            print(i, end=' ')
        else:
            break

    for i, row in range(0, len(temp_data)):
        for j in range(0, len(temp_data[i])):
            print(temp_data[i][j],end=' ')
        print()


    for i, row in enumerate(data):
        print (str(i) + ': ',end=' ')
        for j, element in enumerate(row):
            print(element,end=' ')
        print()

    return counter


if __name__ == "__main__":
    data = [
        [0, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 1, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 0, 1, 0, 1, 1, 1]]

    count = line_size(1, 7, data)
    print(count)

