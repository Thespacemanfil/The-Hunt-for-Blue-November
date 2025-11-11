import os, math, sys, time
import numpy as np
import pygame as pg
from pygame.locals import *
import graphics, movement
global delta_time
global map_scale
delta_time = 0.01
map_scale = 0.1

class submarine:
    def __init__(submarine, classer, type, x, y, z, speed, heading, tgt_depth, tgt_speed, tgt_heading, acceleration, turn, crew, hull_integrity, torpedo_load, sensitivity, filtering, loudness):
        submarine.classer = classer
        submarine.type = type
        submarine.x = x
        submarine.y = y
        submarine.z = z
        submarine.speed = speed
        submarine.heading = heading
        submarine.tgt_depth = tgt_depth
        submarine.tgt_speed = tgt_speed
        submarine.tgt_heading = tgt_heading
        submarine.acceleration = acceleration
        submarine.turn = turn
        submarine.crew = crew
        submarine.hull_integrity = hull_integrity
        submarine.torpedo_load = torpedo_load
        submarine.sensitivity = sensitivity
        submarine.filtering = filtering
        submarine.loudness = loudness
    
    def twohalfD_movement(submarine, delta_time):
        #Changes the speed towards the target speed by a step
        change = min((submarine.acceleration* delta_time), abs(submarine.tgt_speed - submarine.speed))
        submarine.speed += change if submarine.tgt_speed > submarine.speed else -change

        submarine.heading = movement.adjust_heading(submarine, delta_time)

        # Convert angles to radians
        heading_rad = math.radians(submarine.heading)

        #Changes the depth towards the target depth by a step
        change = min((submarine.turn * delta_time), abs(submarine.tgt_depth - submarine.y))
        submarine.y += change if submarine.tgt_depth > submarine.y else -change
    
        # Calculate changes in each coordinate
        submarine.x += delta_time * submarine.speed * math.sin(heading_rad)  #east-west
        submarine.z += delta_time * submarine.speed * math.cos(heading_rad)  #north-south

    def torpedo(submarine):
        global new_torpedo
        new_torpedo = torpedo("hyena",submarine.x,submarine.y,submarine.z,submarine.speed,submarine.heading,submarine.heading,0,100,enemy_1,10,50,9999,1000,2,2,2)

class ship:
    def __init__(ship, classer, type, x, y, z, speed, heading, tgt_speed, tgt_heading, acceleration, turn, crew, hull_integrity, torpedo_load, sensitivity, filtering, loudness):
        ship.classer = classer
        ship.type = type
        ship.x = x
        ship.y = y
        ship.z = z
        ship.speed = speed
        ship.heading = heading
        ship.tgt_speed = tgt_speed
        ship.tgt_heading = tgt_heading
        ship.acceleration = acceleration
        ship.turn = turn
        ship.crew = crew
        ship.hull_integrity = hull_integrity
        ship.torpedo_load = torpedo_load
        ship.sensitivity = sensitivity
        ship.filtering = filtering
        ship.loudness = loudness

    def twoD_movement(ship, delta_time):
        #Changes the speed towards the target speed by a step
        change = min((ship.acceleration* delta_time), abs(ship.tgt_speed - ship.speed))
        ship.speed += change if ship.tgt_speed > ship.speed else -change

        #Changes the heading towards tgt heading by turn
        ship.heading = movement.adjust_heading(ship, delta_time)

        # Convert angles to radians
        heading_rad = math.radians(ship.heading)

        # Calculate changes in each coordinate
        ship.x += delta_time * ship.speed * math.sin(heading_rad)  #east-west
        ship.z += delta_time * ship.speed * math.cos(heading_rad)  #north-south

class torpedo:
    def __init__(torpedo,type,x,y,z,speed,heading,tgt_heading,pitch,max_speed,target,acceleration,turn,range,damage,sensitivity,filtering,loudness):
        torpedo.type = type
        torpedo.x = x
        torpedo.y = y
        torpedo.z = z
        torpedo.speed = speed
        torpedo.heading = heading
        torpedo.tgt_heading = tgt_heading
        torpedo.pitch = pitch
        torpedo.max_speed = max_speed
        torpedo.target = target
        torpedo.acceleration = acceleration
        torpedo.turn = turn
        torpedo.range = range
        torpedo.damage = damage
        torpedo.sensitivity = sensitivity
        torpedo.filtering = filtering
        torpedo.loudness = loudness

    def threeD_movement(torpedo, target, delta_time):
        #Changes the speed towards the target speed by a step
        change = min((torpedo.acceleration* delta_time), abs(torpedo.max_speed - torpedo.speed))
        torpedo.speed += change if torpedo.max_speed > torpedo.speed else -change
        torpedo.range -= torpedo.speed

        # Calculate differences in coordinates between torpedo and target
        dx = target.x - torpedo.x  # East-West difference
        dy = target.y - torpedo.y  # Vertical difference
        dz = target.z - torpedo.z  # North-South difference
        # Calculate target pitch (vertical angle)
        tgt_pitch = math.degrees(math.atan2(dy, math.sqrt(dx**2 + dz**2)))
        # Calculate target heading (horizontal angle)
        tgt_heading = math.degrees(math.atan2(dx, dz))
        # Adjust target heading to 0-360 degrees range
        tgt_heading = (tgt_heading + 360) % 360

        #Changes the heading towards tgt heading by turn
        torpedo.heading = movement.adjust_heading(torpedo, delta_time)

        # Calculate the change in pitch towards the target within the limits
        change = min((torpedo.turn * delta_time), abs(tgt_pitch - torpedo.pitch))
        # Determine the direction of adjustment based on the target pitch and the current pitch
        if tgt_pitch > torpedo.pitch: torpedo.pitch = min(torpedo.pitch + change, 90)  # Ensure pitch doesn't exceed 90
        else: torpedo.pitch = max(torpedo.pitch - change, -90)  # Ensure pitch doesn't go below -90

        # Convert angles to radians
        heading_rad = math.radians(torpedo.heading)
        pitch_rad = math.radians(torpedo.pitch)

        # Calculate changes in each coordinate
        torpedo.z += delta_time * torpedo.speed * math.sin(pitch_rad) * math.cos(heading_rad)  # East-West
        torpedo.y += delta_time * torpedo.speed * math.cos(pitch_rad)                          # Vertical
        torpedo.x += delta_time * torpedo.speed * math.sin(pitch_rad) * math.sin(heading_rad)  # North-South


def initialise():
    global player
    global enemy_1
    player = submarine("narwhal", "SSN", 0, 0, 0, 0, 300, -10, 0, 10, 5, 10, 100, 500, 20, 2, 0.3, 0.3)
    enemy_1 = ship("krankenhaus", "DDG", 2000, 0, 2000, 50, 180, 20, 180, 2, 5, 200, 100, 5, 7, 4, 10)
    player.torpedo()
    graphics.draw_map()
    gameloop()

def gameloop():
    while True:
        graphics.draw_player(map_scale, player)
        graphics.draw_ship(map_scale, player, enemy_1)
        graphics.draw_torpedo(map_scale, player, new_torpedo)
        time.sleep(delta_time)
        player.twohalfD_movement(delta_time)
        enemy_1.twoD_movement(delta_time)
        new_torpedo.threeD_movement(enemy_1, delta_time)
        print("player x:",player.x,"y:",player.y,"z:",player.z,"heading:",player.heading,"speed:",player.speed)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    print("Heavy is dead")