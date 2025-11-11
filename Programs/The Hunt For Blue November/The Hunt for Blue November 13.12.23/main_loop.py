import math, sys, time, random
import numpy as np
import pygame as pg
from pygame.locals import *
import graphics, data

class submarine:
    def __init__(submarine, classer, type, x, y, z, speed, heading, tgt_depth, tgt_speed, tgt_heading, target, acceleration, turn, crew, hull_integrity, torpedo_load, sensitivity, filtering, loudness):
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
        submarine.target = target
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

        submarine.heading = data.adjust_heading(submarine, dt)

        #Changes the depth towards the target depth by a step
        change = min((submarine.turn * dt), abs(submarine.tgt_depth - submarine.y))
        submarine.y += change if submarine.tgt_depth > submarine.y else -change

        # Calculate changes in each coordinate
        submarine.x += dt * submarine.speed * math.sin(submarine.heading)  #west to east X
        submarine.z += dt * submarine.speed * math.cos(submarine.heading)  #south to north Z

    def torpedo(submarine,enemies,torpedoes,target):
        #torpedoes.append(torpedo("hyena",submarine.x,submarine.y,submarine.z,submarine.speed,submarine.heading,submarine.heading,0,150,target,10,50,9999,1000,2,2,2))
        torpedoes.append(torpedo("torpedo","hyena",submarine.x,submarine.y,submarine.z,submarine.speed + 50,submarine.heading,submarine.heading,0,150,enemies[submarine.target],10,0.5,9999,1000,2,2,2))

class ship:
    def __init__(ship, classer, type, x, y, z, speed, heading, tgt_speed, tgt_heading, target, acceleration, turn, crew, hull_integrity, torpedo_load, sensitivity, filtering, loudness):
        ship.classer = classer
        ship.type = type
        ship.x = x
        ship.y = y
        ship.z = z
        ship.speed = speed
        ship.heading = heading
        ship.tgt_speed = tgt_speed
        ship.tgt_heading = tgt_heading
        ship.target = target
        ship.acceleration = acceleration
        ship.turn = turn
        ship.crew = crew
        ship.hull_integrity = hull_integrity
        ship.torpedo_load = torpedo_load
        ship.sensitivity = sensitivity
        ship.filtering = filtering
        ship.loudness = loudness

    def location(ship):
        return ship.x, ship.y, ship.z

    def twoD_movement(ship, dt):
        #Changes the speed towards the target speed by a step
        change = min((ship.acceleration* dt), abs(ship.tgt_speed - ship.speed))
        ship.speed += change if ship.tgt_speed > ship.speed else -change

        #Changes the heading towards tgt heading by turn
        ship.heading = data.adjust_heading(ship, dt)

        # Calculate changes in each coordinate
        ship.x += dt * ship.speed * math.sin(ship.heading)  #east-west
        ship.z += dt * ship.speed * math.cos(ship.heading)  #north-south

    def torpedo(ship,enemies,torpedoes,target):
        #torpedoes.append(torpedo("hyena",submarine.x,submarine.y,submarine.z,submarine.speed,submarine.heading,submarine.heading,0,150,target,10,50,9999,1000,2,2,2))
        torpedoes.append(torpedo("torpedo","crabb",ship.x,ship.y,ship.z,ship.speed + 50,ship.heading,ship.heading,0,150,enemies[ship.target],10,0.5,9999,1000,2,2,2))

class torpedo:
    def __init__(torpedo,classer,type,x,y,z,speed,heading,tgt_heading,pitch,max_speed,target,acceleration,turn,range,damage,sensitivity,filtering,loudness):
        torpedo.classer = classer
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
        print("torpedo x:",torpedo.x,"y:",torpedo.y,"z:",torpedo.z,"heading:",torpedo.heading,"target heading:",np.rad2deg(torpedo.tgt_heading),"speed:",torpedo.speed,"pitch:",torpedo.pitch)

    def threeD_movement(torpedo, torpedoes, enemies, friendlies, player, dt):
        targets = [enemies + friendlies]
        if torpedo.target in targets: target = torpedo.target
        else: torpedoes.remove(torpedo); return

        #Changes the speed towards the target speed by a step
        change = min((torpedo.acceleration* dt), abs(torpedo.max_speed - torpedo.speed))
        torpedo.speed += change if torpedo.max_speed > torpedo.speed else -change

        dx = target.x - torpedo.x  # east-west (x-axis)
        dy = target.y - torpedo.y  # vertical (y-axis)
        dz = target.z - torpedo.z  # north-south (z-axis)

        # Calculate distance in the horizontal plane
        distance_2d = np.hypot(dx, dz)

        #collision
        if np.hypot(distance_2d, dy) < 50:
            try:
                print("detonate")
                if data.kill(enemies, friendlies, player, torpedo.target) == True: gameover()
                print("Vessel sunk!")
                pg.mixer.Sound('vessel_destruction.mp3').play()
                torpedoes.remove(torpedo); return
            except: pass

        #range
        if torpedo.range < 0: 
            try: torpedoes.remove(torpedo); return
            except: pass
        else: torpedo.range -= torpedo.speed * dt

        # Calculate bearing (horizontal direction) - angle in the x-z plane
        torpedo.tgt_heading = math.atan2(dx, dz) % (2 * np.pi) # negative dz because y-axis is positive in the "up" direction
        tgt_pitch = math.atan2(dy, distance_2d)

        #Changes the heading towards tgt heading by turn
        torpedo.heading = data.adjust_heading(torpedo, dt)

        #Changes the pitch towards tgt pitch by turn
        change = min((torpedo.turn * dt), abs(tgt_pitch - torpedo.pitch))
        torpedo.pitch += change if tgt_pitch > torpedo.pitch else -change

        # Calculate changes in each coordinate
        torpedo.x += dt * torpedo.speed * math.cos(torpedo.pitch) * math.sin(torpedo.heading)  #west to east X
        torpedo.y += dt * torpedo.speed * math.sin(torpedo.pitch)                          #vertical Y
        torpedo.z += dt * torpedo.speed * math.cos(torpedo.pitch) * math.cos(torpedo.heading)  #south to north Z
        if torpedo.y > 0: torpedo.y = 0



def initialise():
    FPS = 60
    dt = 0.1
    map_scale = 0.1
    sensitivity = 0.5
    enemies = []
    friendlies = []
    torpedoes = []

    pg.mixer.Sound('ambience.wav').play(loops=-1).set_volume(0.4)

    #x, y, z, speed, heading, tgt_depth, tgt_speed, tgt_heading, acceleration,
    enemies.append(ship("krankenhaus", "DDG", 0, 0, 2000, 0, 200, 100, 3.14, 0, 2, 5, 200, 100, 5, 7, 4, 10))
    enemies.append(ship("krankenhaus", "DDG", 1000, 0, 0, 0, 200, 0, 3.14, 0, 2, 5, 200, 100, 5, 7, 4, 10))
    player = submarine("narwhal", "SSN", 0, 0, 0, 0, 3.14, 0, 0, 0, 0, 10, 0.2, 100, 500, 20, 2, 0.3, 0.3)

    graphics.draw_map()

    gameloop(FPS, dt, map_scale, sensitivity, player, enemies, friendlies, torpedoes)

def gameloop(FPS, dt, map_scale, sensitivity, player, enemies, friendlies, torpedoes):
    rad = 2 * np.pi
    reload = 0
    cooldown = 0
    endgame = 5
    clock = pg.time.Clock()

    while True:
        dt = clock.tick(FPS) / 1000
        print("dt:",dt)

        graphics.draw_background()
        for ship in enemies:
            graphics.draw_ship(map_scale, ship, player)
        for torpedo in torpedoes:
            graphics.draw_torpedo(map_scale, torpedo, player)
        graphics.draw_player(map_scale, player)
        graphics.draw_ui(map_scale)

        player.twohalfD_movement(dt)
        for ship in enemies:
            ship.twoD_movement(dt)
        for torpedo in torpedoes:
            torpedo.threeD_movement(torpedoes, enemies, friendlies, player, dt)

        data.log("player",player)
        for ship in enemies:
            data.log("enemy",ship)
        for torpedo in torpedoes:
            torpedo.log()

        reload -= dt
        cooldown -= dt

        if len(enemies) == 0:
            endgame -= dt
            if endgame < 0: win()

        keys=pg.key.get_pressed()
        if keys[K_LEFT]:
            player.tgt_heading-=5 * dt * sensitivity
            if player.tgt_heading < 0: player.tgt_heading = player.tgt_heading % rad
        if keys[K_RIGHT]:
            player.tgt_heading+=5 * dt * sensitivity
            if player.tgt_heading > rad: player.tgt_heading = player.tgt_heading % rad
        if keys[K_UP]:
            player.tgt_speed+=50 * dt * sensitivity
            if player.tgt_speed > 150: player.tgt_speed = 150
        if keys[K_DOWN]:
            player.tgt_speed-=50 * dt * sensitivity
            if player.tgt_speed < 0: player.tgt_speed = 0
        if keys[K_t]:
            if cooldown < 0: 
                player.target += 1
                if player.target >= len(enemies): player.target = 0   
                cooldown = 1
        if keys[K_f]:
            if reload <= 0 and player.torpedo_load > 0 and len(enemies) > 0:
                if player.target >= len(enemies): player.target = 0
                player.torpedo(enemies,torpedoes,player.target)
                reload = 5; player.torpedo_load -=1
                pg.mixer.Sound('torpedo_launch.wav').play()
            else: reload -= dt
        if keys[K_m]:
            map_scale += 0.2 * dt * sensitivity
            if map_scale > 3: map_scale = 3
        if keys[K_n]:
            map_scale -= 0.2 * dt * sensitivity
            if map_scale < 0.0001: map_scale = 0.0001
        if keys[K_p]:
            pause()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

    print("Heavy is dead")

def pause():
    graphics.pause()
    time.sleep(0.5)
    while True:
        time.sleep(0.1)
        keys=pg.key.get_pressed()
        if keys[K_p]:
            break
            

def win():
    time.sleep(2)
    graphics.win()
    time.sleep(7)
    pg.quit()
    sys.exit()

def gameover():
    time.sleep(2)
    graphics.gameover()
    time.sleep(7)
    pg.quit()
    sys.exit()

initialise()