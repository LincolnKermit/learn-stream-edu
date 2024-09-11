import os

def loading_defined(current_users: int) -> int:
    max_users = 15
    quotient = 100 / max_users
    capacity = current_users * quotient
    capacity = round(capacity, 1)
    print("Capacity: ", capacity, "%")
    starter = '['
    ender = ']'
    string = '█'
    blank = '.'
    os.system("clear")
    space = 100 - int(capacity)  # Define space
    if capacity > 100:
        print(starter + (string * 100) + ender)
        print("Maximum Capacity - 100 %")
    else:
        print(starter + ((string * int(capacity)) + (blank * space)) + ender)
        print(int(capacity), "%")  # Use int(capacity) instead of undefined y




def loading_undefined(x: int) -> int:
    x = int(len(x))
    y = round(100 / x)
    z = round(100 / x)
    starter = '['
    ender = ']'
    string = '█'
    blank = '.'

    while y < 100:
        os.system("clear")
        y = y + z
        space = (100 - y)
        if y > 100:
            print(starter + (string * 100) + ender)
            print("100 %")
            break
        else:
            print(starter + ((string * y) + (blank * space)) + ender)
            print(y, "%")