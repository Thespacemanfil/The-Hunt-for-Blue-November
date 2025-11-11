import math

def tgt_relative_pos(tgt_x, tgt_y, tgt_z, self_x, self_y, self_z):
    tgt_distance = math.sqrt(((tgt_x - self_x)**2) + ((tgt_z - self_z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((tgt_y - self_y)**2))
    tgt_heading = math.degrees(math.atan2(tgt_x - self_x, tgt_z - self_z))
    tgt_pitch = math.degrees(math.atan2(tgt_y - self_y, math.sqrt((tgt_x - self_x)**2 + (tgt_z - self_z)**2)))
    
    return tgt_distance, tgt_true_distance, tgt_heading, tgt_pitch

def tgt_volume(tgt_speed,tgt_loudness,tgt_base_volume,distance):
    tgt_volume = (tgt_base_volume+(tgt_loudness*tgt_speed))/(distance)**2   
    return tgt_volume

def tgt_data(tgt_x, tgt_y, tgt_z, tgt_speed,tgt_loudness,tgt_base_volume, self_x, self_y, self_z):
    tgt_distance = math.sqrt(((tgt_x - self_x)**2) + ((tgt_z - self_z)**2))
    tgt_true_distance = math.sqrt((tgt_distance**2) + ((tgt_y - self_y)**2))
    heading = math.degrees(math.atan2(tgt_x - self_x, tgt_z - self_z))
    pitch = math.degrees(math.atan2(tgt_y - self_y, math.sqrt((tgt_x - self_x)**2 + (tgt_z - self_z)**2)))
    tgt_volume = (tgt_base_volume+(tgt_loudness*tgt_speed))/(tgt_true_distance)**2