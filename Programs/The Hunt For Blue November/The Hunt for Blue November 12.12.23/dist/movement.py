import math
import numpy as np

def adjust_heading(entity, dt):
    # Calculate the shortest turning direction
    diff = (entity.tgt_heading - entity.heading) % (2 * np.pi)
    diff = (diff + np.pi) % (2 * np.pi) - np.pi  # Normalize to -180 to 180 range
    shortest_turn = np.sign(diff) * min(abs(diff), entity.turn * dt)

    # Update heading considering looping around at 360 degrees
    new_heading = (entity.heading + shortest_turn) % (2 * np.pi)
    return new_heading

def log(name,entity):
    print(name,"x:",entity.x,"y:",entity.y,"z:",entity.z,"heading:",np.rad2deg(entity.heading),"speed:",entity.speed)

def tgt_relative_pos(target, self):
    tgt_distance = math.sqrt(((target.x - self.x)**2) + ((target.z - self.z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((target.y - self.y)**2))
    tgt_heading = math.degrees(math.atan2(target.x - self.x, target.z - self.z))
    tgt_pitch = math.degrees(math.atan2(target.y - self.y, math.sqrt((target.x - self.x)**2 + (target.z - self.z)**2)))
    
    return tgt_distance, tgt_true_distance, tgt_heading, tgt_pitch

def tgt_volume(target, self):
    tgt_distance = np.hypot(target.x - self.x, target.z - self.z)
    tgt_true_distance = np.hypot(tgt_distance, (target.y - self.y)**2)
    tgt_volume = ((target.loudness/10)+(target.loudness*target.speed))/(tgt_true_distance)**2
    return tgt_volume

def tgt_data(target, self):
    tgt_distance = math.sqrt(((target.x - self.x)**2) + ((target.z - self.z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((target.y - self.y)**2))
    heading = math.degrees(math.atan2(target.x - self.x, target.z - self.z))
    pitch = math.degrees(math.atan2(target.y - self.y, math.sqrt((target.x - self.x)**2 + (target.z - self.z)**2)))
    tgt_volume = (target.base_volume+(target.loudness*target.speed))/(tgt_true_distance)**2