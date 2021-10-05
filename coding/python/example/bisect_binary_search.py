from bisect import bisect_right

def binary_search(data, value):
    position = bisect_right(data, value)
    if data[position - 1] == value:
        return (position - 1)
    else:
        return False

if __name__ == '__main__':
    data_list = [1, 2, 3, 3, 4, 5]
    value = 3

    if position := binary_search(data_list, value):
        print(f"Number is present at {position}")
    else:
        print("Number Not Found")
