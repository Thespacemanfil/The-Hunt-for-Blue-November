import math

def tgt_relative_pos(target.x, target.y, target.z, self.x, self.y, self.z):
    tgt_distance = math.sqrt(((target.x - self.x)**2) + ((target.z - self.z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((target.y - self.y)**2))
    tgt_heading = math.degrees(math.atan2(target.x - self.x, target.z - self.z))
    tgt_pitch = math.degrees(math.atan2(target.y - self.y, math.sqrt((target.x - self.x)**2 + (target.z - self.z)**2)))
    
    return tgt_distance, tgt_true_distance, tgt_heading, tgt_pitch

def tgt_volume(tgt_speed,tgt_loudness,tgt_base_volume,distance):
    tgt_volume = (tgt_base_volume+(tgt_loudness*tgt_speed))/(distance)**2   
    return tgt_volume

def tgt_data(target.x, target.y, target.z, tgt_speed,tgt_loudness,tgt_base_volume, self.x, self.y, self.z):
    tgt_distance = math.sqrt(((target.x - self.x)**2) + ((target.z - self.z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((target.y - self.y)**2))
    heading = math.degrees(math.atan2(target.x - self.x, target.z - self.z))
    pitch = math.degrees(math.atan2(target.y - self.y, math.sqrt((target.x - self.x)**2 + (target.z - self.z)**2)))
    tgt_volume = (tgt_base_volume+(tgt_loudness*tgt_speed))/(tgt_true_distance)**2