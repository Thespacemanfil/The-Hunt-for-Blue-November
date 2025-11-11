import math

def radian_difference(b1, b2):
    return min(abs(b1 - b2) % (2 * math.pi), (2 * math.pi) - abs(b1 - b2) % (2 * math.pi))

# Example usage
bearing1 = 18.2  # in radians
bearing2 = 0.1  # in radians
print(f"The radian difference is: {radian_difference(bearing1, bearing2)}")

def radian_difference2(b1, b2):
    return min((b1 - b2) % (2 * math.pi), (2 * math.pi) - (b1 - b2) % (2 * math.pi))

# Example usage
bearing1 = 3  # in radians
bearing2 = 4.0  # in radians
print(f"The radian difference is: {radian_difference2(bearing1, bearing2)}")
