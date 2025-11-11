current_value = 21
target_value = 20
change_step = 3
delta_time = 1

import math

# Calculate the change required to move towards the target value by one step
change = min((change_step * delta_time), abs(target_value - current_value))
current_value += change if target_value > current_value else -change

print(current_value)

print(math.cos(90))
