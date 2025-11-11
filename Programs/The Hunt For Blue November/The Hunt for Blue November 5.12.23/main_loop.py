import os, math, sys, time
import numpy as np
import pygame as pg
from pygame.locals import *
import graphics, movement
global dt
global map_scale
global sensitivity
dt = 0.1
map_scale = 0.1
sensitivity = 0.5

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
    
    def twohalfD_movement(submarine, dt):
        #Changes the speed towards the target speed by a step
        change = min((submarine.acceleration* dt), abs(submarine.tgt_speed - submarine.speed))
        submarine.speed += change if submarine.tgt_speed > submarine.speed else -change

        submarine.heading = movement.adjust_heading(submarine, dt)

        #Changes the depth towards the target depth by a step
        change = min((submarine.turn * dt), abs(submarine.tgt_depth - submarine.y))
        submarine.y += change if submarine.tgt_depth > submarine.y else -change

        heading_rad = submarine.heading

        # Calculate changes in each coordinate
        submarine.x += dt * submarine.speed * math.sin(heading_rad)  #east-west
        submarine.z += dt * submarine.speed * math.cos(heading_rad)  #north-south

    def torpedo(submarine):
        global new_torpedo
        new_torpedo = torpedo("hyena",submarine.x,submarine.y,submarine.z,submarine.speed,submarine.heading,submarine.heading,0,150,enemy_1,10,50,9999,1000,2,2,2)

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

    def twoD_movement(ship, dt):
        #Changes the speed towards the target speed by a step
        change = min((ship.acceleration* dt), abs(ship.tgt_speed - ship.speed))
        ship.speed += change if ship.tgt_speed > ship.speed else -change

        #Changes the heading towards tgt heading by turn
        ship.heading = movement.adjust_heading(ship, dt)

        # Convert angles to radians
        heading_rad = math.radians(ship.heading)

        # Calculate changes in each coordinate
        ship.x += dt * ship.speed * math.sin(heading_rad)  #east-west
        ship.z += dt * ship.speed * math.cos(heading_rad)  #north-south

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

    def log(torpedo):
        print("torpedo x:",torpedo.x,"y:",torpedo.y,"z:",torpedo.z,"heading:",torpedo.heading,"target heading:",torpedo.tgt_heading,"speed:",torpedo.speed,"pitch:",torpedo.pitch)

    def threeD_movement(torpedo, target, dt):
        #Changes the speed towards the target speed by a step
        change = min((torpedo.acceleration* dt), abs(torpedo.max_speed - torpedo.speed))
        torpedo.speed += change if torpedo.max_speed > torpedo.speed else -change

        torpedo.range -= torpedo.speed

        dx = target.x - torpedo.x  # east-west (x-axis)
        dy = target.y - torpedo.y  # vertical (y-axis)
        dz = target.z - torpedo.z  # north-south (z-axis)

        # Calculate distance in the horizontal plane
        distance_2d = math.sqrt(dx**2 + dz**2)

        #Changes the heading towards tgt heading by turn
        torpedo.heading = movement.adjust_heading(torpedo, dt)

        # Calculate bearing (horizontal direction) - angle in the x-z plane
        torpedo.tgt_heading = math.degrees(math.atan2(dx, dz)) % 360 # negative dz because y-axis is positive in the "up" direction
        tgt_pitch = math.degrees(math.atan2(dy, distance_2d))

        #Changes the pitch towards tgt pitch by turn
        change = min((torpedo.turn * dt), abs(tgt_pitch - torpedo.pitch))
        torpedo.pitch += change if tgt_pitch > torpedo.pitch else -change

        # Convert angles to radians
        heading_rad = math.radians(torpedo.heading)
        pitch_rad = math.radians(torpedo.pitch)

        # Calculate changes in each coordinate
        torpedo.x += dt * torpedo.speed * math.cos(pitch_rad) * math.sin(heading_rad)  #east-west
        torpedo.y += dt * torpedo.speed * math.sin(pitch_rad)                          #vertical
        torpedo.z += dt * torpedo.speed * math.cos(pitch_rad) * math.cos(heading_rad)  #north-south
        if torpedo.y > 0: torpedo.y = 0


def initialise():
    global player
    global enemy_1    
    #x, y, z, speed, heading, tgt_depth, tgt_speed, tgt_heading, acceleration,
    player = submarine("narwhal", "SSN", 100, 0, 5000, 0, 90, 0, 0, 180, 10, 10, 100, 500, 20, 2, 0.3, 0.3)
    enemy_1 = ship("krankenhaus", "DDG", 100, 0, 2000, 100, 200, 70, 270, 2, 5, 200, 100, 5, 7, 4, 10)
    #enemy_1 = ship("krankenhaus", "DDG", 1000, 0, 0, 0, 200, 0, 270, 2, 5, 200, 100, 5, 7, 4, 10)
    graphics.draw_map()
    gameloop()

def gameloop():
    global dt
    global map_scale
    active_torpedo = False

    while True:
        graphics.draw_player(map_scale, player)
        graphics.draw_ship(map_scale, player, enemy_1)
        if active_torpedo: graphics.draw_torpedo(map_scale, player, new_torpedo)
        time.sleep(dt)
        player.twohalfD_movement(dt)
        enemy_1.twoD_movement(dt)
        if active_torpedo: new_torpedo.threeD_movement(enemy_1, dt)
        movement.log("player",player)
        movement.log("enemy",enemy_1)
        if active_torpedo: new_torpedo.log()
        print(map_scale)

        keys=pg.key.get_pressed()
        if keys[K_LEFT]:
            player.tgt_heading-=50 * dt * sensitivity
            if player.tgt_heading < 0: player.tgt_heading = player.tgt_heading % 360
        if keys[K_RIGHT]:
            player.tgt_heading+=50 * dt * sensitivity
            if player.tgt_heading > 359: player.tgt_heading = player.tgt_heading % 360
        if keys[K_UP]:
            player.tgt_speed+=50 * dt * sensitivity
            if player.tgt_speed > 150: player.tgt_speed = 150
        if keys[K_DOWN]:
            player.tgt_speed-=50 * dt * sensitivity
            if player.tgt_speed < -10: player.tgt_speed = -10
        if keys[K_f]:
            player.torpedo()
            active_torpedo = True
        if keys[K_m]:
            map_scale += 0.2 * dt * sensitivity
            if map_scale > 3: map_scale = 3
        if keys[K_n]:
            map_scale -= 0.2 * dt * sensitivity
            if map_scale < 0.0001: map_scale = 0.0001

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    print("Heavy is dead")