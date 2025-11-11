current_value = 21
target_value = 20
change_step = 3
dt = 1

# Calculate the change required to move towards the target value by one step
change = min((change_step * dt), abs(target_value - current_value))
current_value += change if target_value > current_value else -change

print(current_value)
