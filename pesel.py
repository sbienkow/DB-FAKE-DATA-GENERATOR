import random


def pesel():

    year = random.randint(1900,2099)

    if year <= 1999:
        month = random.randint(1,12)

    elif year >= 2000:
        month = random.randint(1,12) + 20 # to distinguish between centuries

    # I need to put months in a category to choose correct range of possible days for each one
    odd_months = (1, 3, 5, 7, 8, 10, 12, 21, 23, 25, 27, 28, 30, 32)
    even_months = (4, 6, 9, 11, 24, 26, 29, 31)

    if month in odd_months:
        day = random.randint(1,31)

    elif month in even_months:
        day = random.randint(1,30)
    # this is for february
    else:
        if year % 4 == 0 and year != 1900:
            day = random.randint(1,29) # leap year

        else:
            day = random.randint(1,28) # usual year

    four_random = random.randint(1000,9999)
    four_random = str(four_random)

    # here comes the equation part, it calculates the last digit

    y = '%02d' % (year % 100)
    m = '%02d' % month
    dd = '%02d' % day

    a = y[0]
    a = int(a)

    b = y[1]
    b = int(b)

    c = m[0]
    c = int(c)

    d = m[1]
    d = int(d)

    e = dd[0]
    e = int(e)

    f = dd[1]
    f = int(f)

    g = four_random[0]
    g = int(g)

    h = four_random[1]
    h = int(h)

    i = four_random[2]
    i = int(i)

    j = four_random[3]
    j = int(j)

    check = a + 3 * b + 7 * c + 9 * d + e + 3 * f + 7 * g + 9 * h + i + 3 * j

    if check % 10 == 0:
        last_digit = 0
    else:
        last_digit = 10 - (check % 10)

    # printing the final number out
    return '{:02d}{:02d}{:02d}{}{}'.format(year % 100, month, day, four_random, last_digit)
    # print('%02d' % (year % 100), end='')
    # print('%02d' % month, end='')
    # print('%02d' % day, end='')
    # print(four_random, end='')
    # print(last_digit)