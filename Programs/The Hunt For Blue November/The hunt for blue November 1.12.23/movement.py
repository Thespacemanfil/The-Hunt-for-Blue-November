import math
import numpy as np

def adjust_heading(entity, delta_time, threshold=1):
    # Calculate the angle difference between target and current heading
    diff = entity.tgt_heading - entity.heading

    # Normalize the angle difference to the range -180 to 180 degrees
    diff = (diff + 180) % 360 - 180

    # Determine the direction for the shortest turn
    if diff < 0: turn_direction = -1  # Turn left
    else: turn_direction = 1  # Turn right

    # Calculate the maximum turn angle based on the turn rate and delta time
    max_turn = entity.turn * delta_time

    # Calculate the actual turn within the maximum allowed turn rate
    shortest_turn = turn_direction * min(abs(diff), max_turn)

    # Update heading, looping around at 360 degrees
    new_heading = (entity.heading + shortest_turn) % 360

    # Check if the new heading is within the threshold range of the target
    if abs(entity.tgt_heading - new_heading) <= threshold:
        new_heading = entity.tgt_heading  # Snap to the target heading

    return new_heading


def tgt_relative_pos(tgt_x, tgt_y, tgt_z, self_x, self_y, self_z):
    tgt_distance = math.sqrt(((tgt_x - self_x)**2) + ((tgt_z - self_z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((tgt_y - self_y)**2))
    tgt_heading = math.degrees(math.atan2(tgt_x - self_x, tgt_z - self_z))
    tgt_pitch = math.degrees(math.atan2(tgt_y - self_y, math.sqrt((tgt_x - self_x)**2 + (tgt_z - self_z)**2)))
    
    return tgt_distance, tgt_true_distance, tgt_heading, tgt_pitch

def tgt_data(tgt_x, tgt_y, tgt_z, tgt_speed,tgt_loudness,tgt_base_volume, self_x, self_y, self_z):
    tgt_distance = math.sqrt(((tgt_x - self_x)**2) + ((tgt_z - self_z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((tgt_y - self_y)**2))
    heading = math.degrees(math.atan2(tgt_x - self_x, tgt_z - self_z))
    pitch = math.degrees(math.atan2(tgt_y - self_y, math.sqrt((tgt_x - self_x)**2 + (tgt_z - self_z)**2)))
    tgt_volume = (tgt_base_volume+(tgt_loudness*tgt_speed))/(tgt_true_distance)**2

def threeD_movement(x, y, z, heading, pitch, speed, delta_time):
    # Convert angles to radians
    heading_rad = math.radians(heading)
    pitch_rad = math.radians(pitch)
    
    # Calculate changes in each coordinate
    dx = delta_time * speed * math.cos(pitch_rad) * math.sin(heading_rad)  #east-west
    dy = delta_time * speed * math.sin(pitch_rad)                          #vertical
    dz = delta_time * speed * math.cos(pitch_rad) * math.cos(heading_rad)  #north-south
    
    # Calculate new coordinates
    new_x = x + dx
    new_y = y + dy
    new_z = z + dz
    
    return new_x, new_y, new_z

def twohalfD_movement(x, y, z, tgt_y, y_speed, heading, speed, delta_time):
    # Convert angles to radians
    heading_rad = math.radians(heading)

    #vertical
    dy = tgt_y - y
    y_speed = (y_speed * delta_time)
    if dy < y_speed and dy > -(y_speed): new_y = tgt_y
    elif tgt_y < y: new_y = y - y_speed
    else: new_y = y + y_speed
    
    # Calculate changes in each coordinate
    dx = delta_time * speed * math.sin(heading_rad)  #east-west
    dz = delta_time * speed * math.cos(heading_rad)  #north-south
    
    # Calculate new coordinates
    new_x = x + dx
    new_z = z + dz
    
    return new_x, new_y, new_z

def twoD_movement(x, z, heading, speed, delta_time):
    # Convert angles to radians
    heading_rad = math.radians(heading)
    
    # Calculate changes in each coordinate
    dx = delta_time * speed * math.sin(heading_rad)  #east-west
    dz = delta_time * speed * math.cos(heading_rad)  #north-south
    
    # Calculate new coordinates
    new_x = x + dx
    new_z = z + dz
    
    return new_x, new_z