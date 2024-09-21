def rectangle_square(A, B, C):
    horizontal_squares = A // C
    vertical_squares = B // C
    total_squares = horizontal_squares * vertical_squares
    rectangle_area = A * B
    squares_area = total_squares * C * C
    unused_area = rectangle_area - squares_area
    return total_squares, unused_area

def number_description(n):
    if n == 0:
        return "нулевое число"
    elif n > 0 and n % 2 == 0:
        return "положительное четное число"
    elif n > 0 and n % 2 != 0:
        return "положительное нечетное число"
    elif n < 0 and n % 2 == 0:
        return "отрицательное четное число"
    elif n < 0 and n % 2 != 0:
        return "отрицательное нечетное число"

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

A, B, C = 10, 15, 3
n = 0
print(rectangle_square(A, B, C))
print(number_description(n))
print(gcd(A, B))