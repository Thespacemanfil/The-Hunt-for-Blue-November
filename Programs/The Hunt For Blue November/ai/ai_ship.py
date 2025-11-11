import numpy as np
import math, random

def ship_ai(ship, target, torpedoes):
    Evade = False
    aggression = 1
    fear = 1.5


    for torpedo in torpedoes:
        if np.hypot(torpedo.y,np.hypot(torpedo.x - ship.x,torpedo.z - ship.z)) < (500 * fear):
            evade = True
            ship.tgt_heading = (math.atan2(torpedo.x - ship.x, torpedo.z - ship.z) + np.pi) % (2 * np.pi)
            ship.tgt_speed = 120
            return
        
    if target.volume > ship.sensitivity:
        fire_torpedo()
        ship.tgt_heading = (math.atan2(torpedo.x - ship.x, torpedo.z - ship.z) * aggression) % (2 * np.pi)
    else:
        ship.tgt_heading += random.uniform(-np.pi,np.pi) * aggression
        ship.tgt_speed = random.randint(10,100)