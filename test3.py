import string

dict1 = {a: x for a, x in enumerate(string.ascii_lowercase, start=1) if a < 21}

list1 = [x for x in range(1, 21)]
list2 = [a for a in string.ascii_lowercase]


def func(l1, l2, count):
    return dict(zip(l1[:count], l2[:count]))


print(func(list1, list2, 3))
