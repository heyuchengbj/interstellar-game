# "Interstellar" - A tribute to Unity's iOS Arcade Game "One Infinite Tunnel"
#
# Created by Richard He
#
# The game is an extended verison of Unity's iOS game "One Infinite Tunnel".
# Using simple controls, player can contorl the thrust of the spaceship using Space and missile shoots using Ctrl
#
# Current Development
# -Adding multiplayer mode
# -Create curved top and bottom line
# -Adding Artistic elements(Images, sounds)
# -Different playing modes(shoot rocks, collect golds, etc.)
#
# Game Pitch Sheet: https://dl.dropbox.com/s/m0a9ippp9jsi5de/Pitch_FINAL.compressed.pdf?dl=0
#
# Previous Versions
#	v0.9 - 3rd November 2015: First prototype: Game project #2 - Building a prototype
#                             http://www.codeskulptor.org/#user40_8s2d8r6cTo_19.py
#	v0.91 - 12th November 2015: Second prototype: Game project #3 - Refining your prototype
#   							Improvements on physics, contorls, game play, graphics
#								top and bottom line interactions
#								http://www.codeskulptor.org/#user40_8s2d8r6cTo_155.py
#   v0.92 - 19th November 2015: Third prototype: Game project #4 - Building a draft version
#   							Add Splash Screen, Artistic elements, different playing modes, 
#								refine physics and collision
#
# Current Version (v1.01 - 3th December 2015)

import simplegui
import random
import math

# Define global variables
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
level = 1
score = 0
distance = 0
best_distance = 0
best_score = 0
instruction_message = False
high_score = False
splash_screen = True
started = False
mode_screen = False
score_mode = "distance"
message = True
atime = 0
time = 0
space_time = 0
loading = True
global_gold_time = 0
enter_name = ""
load_num = 0
explosion_rock = set()
explosion_ship = set()
game_mode = "rock"
dead_message = False
score_high_list = [
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0]
]
distance_high_list = [
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0],
    ["", 0, 0]
]

# Load Sounds
BLAST_SOUND = simplegui.load_sound("https://dl.dropbox.com/s/hkcm0vhohj1avcl/Blast-SoundBible.com-2068539061.mp3?dl=0")
GOLD_SOUND = simplegui.load_sound("https://dl.dropbox.com/s/urzxxn5b0uoqkas/146723__fins__coin-object.wav?dl=0")
EXPLOSION_SOUND = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
EXPLOSION_SOUND.set_volume(0.4)
THRUST_SOUND = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
THRUST_SOUND.set_volume(0.5)
BACKGROUND_SOUND = simplegui.load_sound("https://dl.dropbox.com/s/1phb45uzbd7a9jh/Day%20One%20%28Original%20Demo%29%201.mp3?dl=0")
BACKGROUND_SOUND.play()
BACKGROUND_SOUND.set_volume(0.7)
STARTED_SOUND = simplegui.load_sound("https://dl.dropbox.com/s/i447tf9ry3q5zjm/started_sound.mp3?dl=0")

# Define Image Information class
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def is_animated(self):
        return self.animated
    
# Define ImageInfo for objects
# Background Image
B_INFO = ImageInfo([300, 160], [600, 320])
B_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/de364yj1156ixgq/background.jpg?dl=0")

# Animated debris image
DEBRIS_INFO = ImageInfo([385, 78], [770, 157])
DEBRIS_IMAGE= simplegui.load_image("https://dl.dropbox.com/s/jayay9vq7tjm1pq/debris.png?dl=0")

# Background Still Image
B_STILL_INFO = ImageInfo([300, 160], [600, 320])
B_STILL_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/fyuvgrxgy83ng45/background_still.png?dl=0")

# Spaceship Image
SHIP_INFO = ImageInfo([49, 19], [98, 39])
SHIP_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/lt1bt305t1w8dpl/spaceship-2.png?dl=0")

# Missile Image
MISSILE_INFO = ImageInfo([47, 19], [94, 38], 0, 30)
MISSILE_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/fz682i6486aobmo/missile.png?dl=0")

# Interstellar Image
INTERSTELLAR_INFO = ImageInfo([260, 101], [520, 202])
INTERSTELLAR_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/mdnpz57qk0fb7b6/interstellar.png?dl=0")

# Top Screen Image
TOP_SCREEN_INFO = ImageInfo([400, 75], [800, 150])
TOP_SCREEN_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/66y2k25nbdn4jcz/top_screen.png?dl=0")

# Rock Image
ROCK_INFO = ImageInfo([25, 27], [50, 54], 26, 1000)
ROCK_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/pfebnfpkxz1q8r4/rock1.png?dl=0")

# Explosion Image
EXPLOSION_INFO = ImageInfo([96, 96], [192, 192], 96, 25)
EXPLOSION_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/k6uto83fre4qreu/explosion-spritesheet.png?dl=0")

# Instruction Backgroud
INSTRUCTION_INFO = ImageInfo([400, 300], [800, 600])
INSTRUCTION_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/dpp2eq535obztwg/instructruction.png?dl=0")

# Choose mode image
MODE_INFO = ImageInfo([400, 300], [800, 600])
MODE_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/kmy5z6vidp1yw0x/splash_screen2.jpg?dl=0")

# Splash Screen
SPLASH_INFO = ImageInfo([400, 300], [800, 600])
SPLASH_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/wu25xw1msbsr6k0/splash_image.jpg?dl=0")

# High Score Screen
HIGH_SCORE_INFO = ImageInfo([400, 300], [800, 600])
HIGH_SCORE_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/591qyphj4j20l7e/high_score.jpg?dl=0")

# Gold image
GOLD_INFO = ImageInfo([20, 20], [40, 40], 30, 500, True)
GOLD_IMAGE = simplegui.load_image("https://dl.dropbox.com/s/x7i6qsir1ycho1r/coin.png?dl=0")
    
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

# Calculate distance
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# High Score Class
class Highscore:
    def __init__(self, distance, score, name = "Player 1"):
        if name == '':
            self.name = "Player 1"
        else:
            self.name = name
        self.distance = distance
        self.score = score
    def __str__(self):
        return [self.name, str(self.distance), str(self.score)]
    def get_name(self):
        return self.name
    def get_score(self):
        return self.score
    def get_distance(self):
        return self.distance
    def distance_update(self):
        n = 0
        for i in distance_high_list:
            if i[1] <= self.distance and not self.distance == 0:
                distance_high_list.pop(-1)
                distance_high_list.insert(n, [self.name, self.distance, self.score])
                break
            n += 1
        
    def score_update(self):
        n = 0
        for i in score_high_list:
            if i[2] <= self.score and not self.distance == 0:
                score_high_list.pop(-1)
                score_high_list.insert(n, [self.name, self.distance, self.score])
                break
            n += 1
            
# Ship Class
class Ship:    
    def __init__(self, pos, angle, image, info):
        self.pos = pos
        self.thrust = False
        self.angle = angle
        self.ang_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.vel = [0,0]
        self.tip_pos = [self.pos[0] + 50 * angle_to_vector(self.angle)[0], 
                        self.pos[1] + 100 * angle_to_vector(self.angle)[1]]
        self.past_pos = [[105.0, 292.5]]
    def draw_trait(self, canvas):
        if started:
            for pos in self.past_pos:
                pos[0] -= 3
                canvas.draw_circle(pos, abs(math.sqrt(abs(100 - pos[0]))), 6, 'White', 'White')
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,
                              self.angle)
    def set_thrust(self, status):
        self.thrust = status
        #if self.thrust:
            #THRUST_SOUND.rewind()
            #THRUST_SOUND.play()
        #else:
            #THRUST_SOUND.pause()
    def update(self):
        if started:
            self.pos[1] = self.pos[1] + self.vel[1]
            self.tip_pos = [self.pos[0] + 50 * angle_to_vector(self.angle)[0], 
                            self.pos[1] + 50 * angle_to_vector(self.angle)[1]]
            if self.thrust:
                n = 0
                if self.ang_vel > -0.02:
                    self.ang_vel -= 0.0021
                self.angle += self.ang_vel
                acc = angle_to_vector(self.angle - 1)
                self.vel[1] += acc[1] * 0.28
            else:
                if self.ang_vel < 0:
                    self.ang_vel += 0.001
                elif self.ang_vel < 0.007:
                    self.ang_vel += 0.0017
                self.angle += self.ang_vel
            if self.vel[1] <= 4:
                self.vel[1] += 0.05
    def get_ypos(self):
        return self.pos[1]
    def get_pos(self):
        return self.pos
    def get_tip_pos(self):
        return self.tip_pos
    def get_ship_pos(self):
        foward = angle_to_vector(self.angle)
        front_pos_up =	[self.pos[0] + 21 * foward[0], 
                    self.pos[1] + 21 * foward[1] - 14]
        front_pos_down = [front_pos_up[0], front_pos_up[1] + 15]
        back_pos_up = [self.pos[0] - 24 * foward[0], 
                    self.pos[1] - 24 * foward[1] - 15]
        if back_pos_up[0] - self.past_pos[-1][0] > 10:	
            self.past_pos.append([back_pos_up[0], back_pos_up[1] + 15])
        if self.past_pos[0][0] < 0:
            self.past_pos.pop(0)
        back_pos_down = [back_pos_up[0], back_pos_up[1] + 15]
        return [self.tip_pos, front_pos_up, front_pos_down, back_pos_up, back_pos_down]
    
    # Function for detecting if collide
    def collide(self, point_list, pos):
        for point in point_list[110:200]:
            if pos[0] - 5 <= point[0] <= pos[0] + 5:
                if abs(pos[1] - point[1]) < 5:
                    return True
        return False
    def action_collide(self, line):
        for pos in self.get_ship_pos():
            if self.collide(line.get_list(), pos):
                dead()
                break
    def shoot(self):
        if len(missile_group) < 2:
            forward = angle_to_vector(self.angle)
            missile_pos = self.tip_pos
            missile_vel = [10 + 10 * forward[0], self.vel[1] + 10 * forward[1]]
            missile_group.update([Sprite(missile_pos, missile_vel, self.angle, 0, MISSILE_IMAGE, MISSILE_INFO)])

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.info = info
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    def draw(self, canvas):
        if self.info.is_animated():
                canvas.draw_image(self.image, [global_gold_time * 40 - 20, self.image_center[0]], self.image_size,
                                  self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    def get_pos(self):
        return self.pos
    def get_age(self):
        return self.age
    def get_lifespan(self):
        return self.lifespan
    def update(self):
        # update angle
        self.angle += self.angle_vel
        if self.age == self.lifespan:
            return True
        self.age += 1
        # update position
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] + self.vel[1]
        return False
    def ship_collide(self, pos):
        global explosion_ship
        if CANVAS_WIDTH / 6 - 20 <= self.pos[0] <= CANVAS_WIDTH / 6 + 20:
            if abs(pos[1] - self.pos[1]) < self.radius:
                return True
        return False
    def missile_collide(self, pos):
        global explosion_rock
        if dist(self.pos, pos) <= self.radius + 28:
            explosion_rock.add(Sprite(self.pos, [0, 0], 0, 0, EXPLOSION_IMAGE, EXPLOSION_INFO, EXPLOSION_SOUND))
            return True
        return False
    def missile_line_collide(self):
        for point1 in top_line.record_list():
            if dist(self.pos, point1) < 5:
                return True
        for point2 in bottom_line.record_list():
            if dist(self.pos, point2) < 5:
                return True
        return False

class Initial:
    def __init__(self, topline, bottomline):
        self.top = topline
        self.bottom = bottomline
    def get_top_line(self):
        return self.top
    def get_bottom_line(self):
        return self.bottom
        
class Line:
    def __init__(self, point_list, ang, vel = 0):
        self.list = point_list
        self.angle = ang
        self.vel = vel
        self.new_point = [0,0]
        self.pivot_point = []
    def draw(self, canvas):
        if len(self.pivot_point) > 1 and self.pivot_point[0][0] < 1:
            canvas.draw_polyline(self.pivot_point, 5, 'White')
        else:
            for point in self.list:
                canvas.draw_circle(point, 1.5, 2, 'White')
    def add_point(self, new):
        self.list.append(new)
    def update_list(self):
        self.new_point = [self.list[-1][0] + 3, 
                     self.list[-1][1] + 3 * angle_to_vector(self.angle)[1]]
        if self.list[-1][0] <= 800:
            self.list.append(self.new_point)
        else:
            self.list.pop(0)
            self.list.append(self.new_point)
            self.pivot_point.append(self.new_point)
            if len(self.pivot_point) > 1:
                self.pivot_point.pop(-2)
                if self.pivot_point[0][0] < -20:
                    self.pivot_point.pop(0)
            for point in self.list:
                point[0] = point[0] - 3
        # Detect Collision
        top_line.line_collision(bottom_line)
    def line_collision(self, other_line):
        if abs(self.new_point[1] - other_line.get_new_point()[1]) <= 170 - 2 * level:
            self.angle = -2
            self.pivot_point.append(self.new_point)
            other_line.add_pivot_point(other_line.get_new_point())
            other_line.angle = self.angle + random.randrange(-10, 10) / 10.0
    def update_angle(self, new_ang):
        self.angle = new_ang
        self.pivot_point.append(self.new_point)
    def record_list(self):
        return self.list
    def get_new_point(self):
        return self.new_point
    def get_angle(self):
        return self.angle
    def get_vel(self):
        return self.vel
    def get_point(self):
        return self.list[-1]
    def get_spec_point(self, n):
        return self.list[n]
    def get_list(self):
        return self.list
    def add_pivot_point(self, n_point):
        self.pivot_point.append(n_point)
    def tuple_to_list(self):
        self.list = list(self.list)
    
def draw_explosion(canvas, rock):
    global explosion_rock, rock_group
    if not rock.update():
        canvas.draw_image(EXPLOSION_IMAGE, [EXPLOSION_INFO.get_center()[0] + rock.get_age() * 192, 96], EXPLOSION_INFO.get_size(), rock.get_pos(), EXPLOSION_INFO.get_size())
        if len(rock_group) > 0:
            rock_group.pop()
    else:
        explosion_rock.pop()
        rock_spawner()

def draw_ship_explosion(canvas):
    global explosion_ship
    for ship in explosion_ship:
        if not ship.update():
            canvas.draw_image(EXPLOSION_IMAGE, [EXPLOSION_INFO.get_center()[0] + ship.get_age() * 192, 96], EXPLOSION_INFO.get_size(), ship.get_pos(), EXPLOSION_INFO.get_size())
        else:
            explosion_ship.pop()
        
# Define mouse click handler at start of game
def click(pos):
    global splash_screen, instruction_message, high_score, message, mode_screen, game_mode, score_mode
    if splash_screen and 525 < pos[1] < 556:
        if 92 < pos[0] < 269:
            splash_screen = False
            instruction_message = True
        elif 350 < pos[0] < 432:
            splash_screen = False
            mode_screen = True
        elif 524 < pos[0] < 693:
            splash_screen = False
            high_score = True
    elif instruction_message:
        splash_screen = True
        instruction_message = False
    elif high_score:
        if 172 < pos[1] < 199 and 515 < pos[0] < 633:
            score_mode = "distance"
        elif 172 < pos[1] < 199 and 663 < pos[0] < 754:
            score_mode = "score"
        else:
            splash_screen = True
            high_score = False
    
    # Mode Screen Selection
    if mode_screen and 525 < pos[1] < 566:
        if 72 < pos[0] < 342:
            mode_screen = False
            game_mode = "gold"
            new_game()
            message = True
        elif 454 < pos[0]  < 721:
            mode_screen = False
            game_mode = "rock"
            new_game()
            message = True
    
# Handler for keydown
def keydown(key):
    global message, splash_screen, started, dead_message, enter_name, space_time
    if not splash_screen and not instruction_message and not dead_message:
        if key == 27:
            splash_screen = True
            started = False
        if not message:
            if key == simplegui.KEY_MAP['space']:
                my_ship.set_thrust(True)
            # if statement for pressing Ctrl key
            elif key == 17:
                 my_ship.shoot()
        elif key == simplegui.KEY_MAP['space']:        
            message = False
    elif dead_message:
        if 64 < key < 91 and len(enter_name) < 9:
            enter_name += chr(key)
        if key == 8:
            enter_name = enter_name[:-1]
        if key == simplegui.KEY_MAP['space']:
            dead_message = False
            space_time = 0
            new_game()
            enter_name = ""
        
            
# Handler for keyup        
def keyup(key):
    if key == simplegui.KEY_MAP['space']:
        my_ship.set_thrust(False)
        
# Define Draw Handler
def draw(canvas): 
    global message, score, best_distance, best_score, started, time, loading, load_num, atime, score_mode, space_time
    # Draw Background
    if message and not splash_screen or dead_message:
        canvas.draw_image(B_IMAGE, B_INFO.get_center(), B_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2],
                                  [CANVAS_WIDTH + 5, CANVAS_HEIGHT + 5])
        canvas.draw_image(B_STILL_IMAGE, B_STILL_INFO.get_center(), B_STILL_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2],
                                  [CANVAS_WIDTH, CANVAS_HEIGHT])

    # Record time
    if started:
        STARTED_SOUND.play()
        if level <= 5:
            STARTED_SOUND.set_volume(level / 10 + 0.5)
        else:
            STARTED_SOUND.set_volume(1.0)
        time += 1
        wtime = - 2.5 * time % CANVAS_WIDTH
        #wtime2 = - 2 * time % CANVAS_WIDTH
        center = B_INFO.get_center()
        size = B_INFO.get_size()
        canvas.draw_image(B_IMAGE, center, size, (wtime - CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), (CANVAS_WIDTH, CANVAS_HEIGHT))
        canvas.draw_image(B_IMAGE, center, size, (wtime + CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), (CANVAS_WIDTH, CANVAS_HEIGHT))
        #canvas.draw_image(B_STILL_IMAGE, center, size, (wtime2 - CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), (CANVAS_WIDTH, CANVAS_HEIGHT))
        #canvas.draw_image(B_STILL_IMAGE, center, size, (wtime2 + CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), (CANVAS_WIDTH, CANVAS_HEIGHT))
    
    # Draw pre-game message
    if message and not instruction_message and not splash_screen and not mode_screen:
        started = False
        STARTED_SOUND.rewind()
        STARTED_SOUND.pause()
        canvas.draw_text('Press "Space" to start new game', [200, 300], 35, "White")
        if game_mode == "rock":
            canvas.draw_text('Dodge and shoot the rocks to gain high scores', [170, 345], 30, "White")
        elif game_mode == "gold":
            canvas.draw_text('Gain more gold on the way to gain high scores', [170, 345], 30, "White")
        canvas.draw_text('Press "ESC" to return to menu', [260, 390], 30, "White")
        canvas.draw_image(INTERSTELLAR_IMAGE, INTERSTELLAR_INFO.get_center(), INTERSTELLAR_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6],
                              INTERSTELLAR_INFO.get_size())
    
    # Start the game when no pre-game message and instruction message are shown
    if not message and not splash_screen and not instruction_message and not level_timer.is_running() and not dead_message:
        started = True
    
    canvas.draw_image(TOP_SCREEN_IMAGE, TOP_SCREEN_INFO.get_center(), TOP_SCREEN_INFO.get_size(), TOP_SCREEN_INFO.get_center(),
                                  TOP_SCREEN_INFO.get_size())
    canvas.draw_text(str(distance) + " ft", [135, 48], 30, "White")
    canvas.draw_text(str(level), [CANVAS_WIDTH / 2 + 15, 47], 30, "White")
    canvas.draw_text(str(score), [CANVAS_WIDTH - 90, 47], 30, "White")   
    canvas.draw_text(str(best_distance) + " ft", [127, 72], 15, "White")
    canvas.draw_text(str(best_score), [CANVAS_WIDTH - 90, 70], 15, "White")
    
    for ship in explosion_ship:
        draw_ship_explosion(canvas)
        break
    
    # Draw Missile
    if game_mode == "rock":
        for missile in missile_group:
            if missile.missile_line_collide():
                missile_group.discard(missile)
            missile.draw(canvas)
            if missile.update():
                missile_group.discard(missile)
                break
            for rock in rock_group:
                if missile.missile_collide(rock.get_pos()):
                    missile_group.discard(missile)
                    score += 1
                    break

    if started:                
        # Test collision with both lines
        my_ship.action_collide(top_line)
        my_ship.action_collide(bottom_line)

        # Draw Gold
        if game_mode == "gold":
            for gold in gold_group:
                gold.draw(canvas)
                if not message:
                    gold.update()
                if gold.get_pos()[0] < -5:
                    gold_group.remove(gold)
                # Test collision with gold and ships
                if gold.ship_collide(my_ship.get_tip_pos()):
                    GOLD_SOUND.play()
                    gold_group.pop()
                    score += 1
                    rock_spawner()
        # Draw trait of the engine
        my_ship.draw_trait(canvas)   

        # Draw Rock
        if game_mode == "rock":
            for rock in rock_group:
                rock.draw(canvas)
                if not message:
                    rock.update()
                if rock.get_pos()[0] < -5:
                    rock_group.remove(rock)
                # Test collision with rocks and ships
                if rock.ship_collide(my_ship.get_tip_pos()):
                    dead()
                    message = True

            # Draw Explosion
            for e_rock in explosion_rock:
                draw_explosion(canvas, e_rock)
                break
    
    # Draw ship and update
    if not splash_screen and not dead_message:
        my_ship.draw(canvas)

    # Draw the top line
    if not splash_screen:
        top_line.draw(canvas)

    # Draw the bottom line
    if not splash_screen:
        bottom_line.draw(canvas)
    
    # Update ship, top_line, bottom_line
    if not message and not dead_message:
        my_ship.update()
        top_line.update_list()
        bottom_line.update_list()
    
    if dead_message:
        if distance > best_distance:
            if score > best_score:
                canvas.draw_text('Best Score: ' + str(score) + " points", [220, 380], 20, "White")
            else:
                canvas.draw_text('Best Score: ' + str(best_score) + " points", [220, 380], 20, "White")
            canvas.draw_text('A NEW RECORD!!!', [250, 300], 40, "White")
            canvas.draw_text('Best Distance: ' + str(distance) + " ft", [220, 360], 20, "White")
        else:
            if score > best_score:
                canvas.draw_text('Best Score: ' + str(score) + " points", [220, 380], 20, "White")
            else:
                canvas.draw_text('Best Score: ' + str(best_score) + " points", [220, 380], 20, "White")
            canvas.draw_text('You hit the edge... Better luck next time!', [180, 300], 30, "White")
            canvas.draw_text('Best Distance: ' + str(best_distance) + " ft", [220, 360], 20, "White")
        canvas.draw_text('Enter Your Initials: ' + str(enter_name), [220, 440], 40, "White")
        
        t = frame.get_canvas_textwidth('Enter Your Initials: ' + str(enter_name), 40)
        
        if round(space_time) - space_time > 0:
            canvas.draw_polygon([(224 + t, 405), (225 + t, 405), (224 + t, 445), (225 + t, 445)], 5, 'White')
        space_time += 0.025
            
        canvas.draw_text('Press Space to continue...', [220, 470], 30, "White")
    
    # Draw high score menu
    if high_score:
        canvas.draw_image(HIGH_SCORE_IMAGE, HIGH_SCORE_INFO.get_center(), HIGH_SCORE_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2],
                              HIGH_SCORE_INFO.get_size())
        if score_mode == "distance":
            row = 0
            for rows in distance_high_list:
                col = 0
                for items in rows:
                    canvas.draw_text(str(items), [90 + 253 * col, 275 + 36 * row], 33, "White")
                    col += 1
                row += 1
        elif score_mode == "score":
            row = 0
            for rows in score_high_list:
                col = 0
                for items in rows:
                    canvas.draw_text(str(items), [90 + 253 * col, 275 + 36 * row], 33, "White")
                    col += 1
                row += 1
                
    # Draw Instruction_Message
    if instruction_message:
        canvas.draw_image(INSTRUCTION_IMAGE, INSTRUCTION_INFO.get_center(), INSTRUCTION_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2],
                              INSTRUCTION_INFO.get_size())
        BACKGROUND_SOUND.set_volume(1.0)
    
    if mode_screen:
        canvas.draw_image(MODE_IMAGE, MODE_INFO.get_center(), MODE_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2],
                              MODE_INFO.get_size())
        # animiate background
        atime += 1
        awtime = (atime / 4) % CANVAS_WIDTH
        center = DEBRIS_INFO.get_center()
        size = DEBRIS_INFO.get_size()
        canvas.draw_image(DEBRIS_IMAGE, center, size, (awtime - center[0], 200), (770, 157))
        canvas.draw_image(DEBRIS_IMAGE, center, size, (awtime + center[0], 200), (770, 157))
    
    if splash_screen:
        started = False
        canvas.draw_image(SPLASH_IMAGE, SPLASH_INFO.get_center(), SPLASH_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2],
                              SPLASH_INFO.get_size())
        
        # animiate background
        atime += 1
        awtime = (atime / 4) % CANVAS_WIDTH
        center = DEBRIS_INFO.get_center()
        size = DEBRIS_INFO.get_size()
        canvas.draw_image(DEBRIS_IMAGE, center, size, (awtime - center[0], 200), (770, 157))
        canvas.draw_image(DEBRIS_IMAGE, center, size, (awtime + center[0], 200), (770, 157))
        
        canvas.draw_image(INTERSTELLAR_IMAGE, INTERSTELLAR_INFO.get_center(), INTERSTELLAR_INFO.get_size(), [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 3],
                              [INTERSTELLAR_INFO.get_size()[0] + 80, INTERSTELLAR_INFO.get_size()[1] + 50])
        BACKGROUND_SOUND.set_volume(0.7)
        
    # Start all timer if the game started
    if started:
        timer.start()
        timer2.start()
        rock_timer.start()
        level_timer.start()
        global_gold_timer.start()
        BACKGROUND_SOUND.set_volume(0.1)
        
    # Stop all timer if the game stops
    if not started:
        timer.stop()
        timer2.stop()
        rock_timer.stop()
        level_timer.stop()
    
    # Check to see if images are loaded and ready to play
    if loading:
        if not B_IMAGE.get_height() == 0:
            load_num = 10
            if not SPLASH_IMAGE.get_height() == 0:
                load_num = 20
                if not INSTRUCTION_IMAGE.get_height() == 0:
                    load_num = 30
                    if not SHIP_IMAGE.get_height() == 0:
                        load_num = 40
                        if not HIGH_SCORE_IMAGE.get_height() == 0:
                            load_num = 50
                            if not INTERSTELLAR_IMAGE.get_height() == 0:
                                load_num = 60
                                if not TOP_SCREEN_IMAGE.get_height() == 0:
                                    load_num = 70
                                    if not ROCK_IMAGE.get_height() == 0:
                                        load_num = 80
                                        if not MODE_IMAGE.get_height() == 0:
                                            load_num = 85
                                            if not MISSILE_IMAGE.get_height() == 0:
                                                load_num = 90
                                                if not GOLD_IMAGE.get_height() == 0:
                                                    load_num = 95
                                                    if not EXPLOSION_IMAGE.get_height() == 0:
                                                        load_num = 100
                                                        loading = False
        canvas.draw_polygon([(0, 0), (0, CANVAS_HEIGHT), (CANVAS_WIDTH, CANVAS_HEIGHT), (CANVAS_WIDTH, 0)], 12, 'Grey', 'Grey')
        canvas.draw_text('LOADING...', [310, 250], 30, "White")
        canvas.draw_text(str(load_num) + "%", [350, 300], 40, "White")
        canvas.draw_text('If not loading, please close this tab and try again.', [240, 350], 15, "White")
        
# Define time handler for update top line
def top_handler():
    global distance
    if top_line.get_point()[1] > CANVAS_HEIGHT:
        new_angle = random.randrange(-30, 0) / 10.0
    elif top_line.get_point()[1] <= 0:
        new_angle = random.randrange(0, 10) / 10.0
    else:
        new_angle = random.randrange(0, 50) / 10.0
    top_line.update_angle(new_angle)
    # Increase distance by 10
    if not message:
        distance += 10

# Define time handler for update bottom line and rock spawner
def level_time():
    global level
    level += 1

def global_gold():
    global global_gold_time
    global_gold_time = global_gold_time % 6 + 1
    
def bottom_handler():
    if bottom_line.get_point()[1] < CANVAS_HEIGHT * 3 / 5:
        new_angle = random.randrange(0, 30) / 10.0
    elif bottom_line.get_point()[1] >= CANVAS_HEIGHT:
        new_angle = random.randrange(-10, 0) / 10.0
    else:
        new_angle = random.randrange(-30, 0) / 10.0
    bottom_line.update_angle(new_angle)

def rock_spawner():
    global rock_group, gold_group
    if bottom_line.get_point()[1] - top_line.get_point()[1] >= 80 and not message:
        if game_mode == "rock":
            rock_height = random.randrange(int(top_line.get_point()[1] + 35), int(bottom_line.get_point()[1] - 35))
            vel2 = random.randrange(-4, 4) / 20.0
            angle = random.randrange(-10, 10) / 10.0
            rotation_speed = random.randrange(-12, 10) / 100.0
            if len(rock_group) < 1:
                rock_group.append(Sprite([CANVAS_WIDTH - 25, rock_height], [-3, vel2], angle, rotation_speed, ROCK_IMAGE, ROCK_INFO))
        else:
            gold_height = random.randrange(int(top_line.get_point()[1] + 20), int(bottom_line.get_point()[1] - 20))
            if len(gold_group) < 1:
                gold_group.append(Sprite([CANVAS_WIDTH - 25, gold_height], [-3, 0], 0, 0, GOLD_IMAGE, GOLD_INFO))

def dead():
    global started, dead_message, explosion_ship
    explosion_ship.add(Sprite(my_ship.get_pos(), [0, 0], 0, 0, EXPLOSION_IMAGE, EXPLOSION_INFO, BLAST_SOUND))
    started = False
    dead_message = True
            
def new_game():
    # Initialize Ship, Sprite
    global enter_name, my_ship, top_line, bottom_line, missile_group, message, rock_group, gold_group, level, score, distance, best_distance, best_score, time, splash_screen
    STARTED_SOUND.pause()
    if game_mode == "rock":
        rock_group = [Sprite([CANVAS_WIDTH - 25, CANVAS_HEIGHT / 2], [-3, 0], 0.2, 0.06, ROCK_IMAGE, ROCK_INFO)]
    if game_mode == "gold":
        gold_group = [Sprite([CANVAS_WIDTH - 25, CANVAS_HEIGHT / 2], [-3, 0], 0, 0, GOLD_IMAGE, GOLD_INFO)]
    my_ship = Ship([CANVAS_WIDTH / 6, CANVAS_HEIGHT / 2], 0, SHIP_IMAGE, SHIP_INFO)
    top_line = Line(
        [[0, 103.084350727], [2, 104.519062908], [4, 105.95377509], [6, 107.388487272], [8, 108.823199454], [10, 110.257911636], [12, 111.692623817], [14, 113.259277637], [16, 114.825931456], [18, 116.392585275], [20, 117.959239094], [22, 119.525892914], [24, 121.092546733], [26, 122.659200552], [28, 124.225854371], [30, 125.792508191], [32, 127.35916201], [34, 128.925815829], [36, 130.492469648], [38, 132.059123468], [40, 133.625777287], [42, 135.192431106], [44, 136.759084925], [46, 138.325738745], [48, 139.892392564], [50, 141.459046383], [52, 143.025700202], [54, 144.592354022], [56, 146.159007841], [58, 147.72566166], [60, 149.292315479], [62, 150.858969299], [64, 152.425623118], [66, 153.992276937], [68, 155.558930756], [70, 157.125584576], [72, 158.692238395], [74, 160.258892214], [76, 161.825546034], [78, 163.392199853], [80, 164.958853672], [82, 166.525507491], [84, 168.092161311], [86, 169.65881513], [88, 171.225468949], [90, 172.792122768], [92, 174.358776588], [94, 175.925430407], [96, 177.492084226], [98, 179.058738045], [100, 180.625391865], [102, 182.192045684], [104, 183.758699503], [106, 185.325353322], [108, 186.892007142], [110, 188.458660961], [112, 188.458660961], [114, 188.458660961], [116, 188.458660961], [118, 188.458660961], [120, 188.458660961], [122, 188.458660961], [124, 188.458660961], [126, 188.458660961], [128, 188.458660961], [130, 188.458660961], [132, 188.458660961], [134, 188.458660961], [136, 188.458660961], [138, 188.458660961], [140, 188.458660961], [142, 188.458660961], [144, 188.458660961], [146, 188.458660961], [148, 188.458660961], [150, 188.458660961], [152, 188.458660961], [154, 188.458660961], [156, 188.458660961], [158, 188.458660961], [160, 188.458660961], [162, 188.458660961], [164, 188.458660961], [166, 188.458660961], [168, 188.458660961], [170, 188.458660961], [172, 188.458660961], [174, 188.458660961], [176, 188.458660961], [178, 188.458660961], [180, 188.458660961], [182, 188.458660961], [184, 188.458660961], [186, 188.458660961], [188, 188.458660961], [190, 188.458660961], [192, 188.458660961], [194, 188.458660961], [196, 188.458660961], [198, 188.458660961], [200, 188.458660961], [202, 188.458660961], [204, 188.458660961], [206, 188.458660961], [208, 188.458660961], [210, 188.458660961], [212, 188.458660961], [214, 188.458660961], [216, 190.02531478], [218, 191.591968599], [220, 193.158622419], [222, 194.725276238], [224, 196.291930057], [226, 197.858583876], [228, 199.425237696], [230, 200.991891515], [232, 202.558545334], [234, 204.125199153], [236, 205.691852973], [238, 207.258506792], [240, 208.825160611], [242, 210.39181443], [244, 211.95846825], [246, 213.525122069], [248, 215.091775888], [250, 216.658429707], [252, 218.225083527], [254, 219.791737346], [256, 221.358391165], [258, 222.925044984], [260, 224.491698804], [262, 226.058352623], [264, 227.625006442], [266, 229.191660261], [268, 230.758314081], [270, 232.3249679], [272, 233.891621719], [274, 235.458275539], [276, 237.024929358], [278, 238.591583177], [280, 240.158236996], [282, 241.724890816], [284, 243.291544635], [286, 244.858198454], [288, 246.424852273], [290, 247.991506093], [292, 249.558159912], [294, 251.124813731], [296, 252.69146755], [298, 254.25812137], [300, 255.824775189], [302, 257.391429008], [304, 258.958082827], [306, 260.524736647], [308, 262.091390466], [310, 263.658044285], [312, 265.224698104], [314, 264.369938344], [316, 263.515178583], [318, 262.660418823], [320, 261.805659062], [322, 260.950899302], [324, 260.096139542], [326, 259.241379781], [328, 258.386620021], [330, 257.53186026], [332, 256.6771005], [334, 255.822340739], [336, 254.967580979], [338, 254.112821218], [340, 253.258061458], [342, 252.403301697], [344, 251.548541937], [346, 250.693782176], [348, 249.839022416], [350, 248.984262655], [352, 248.129502895], [354, 247.274743135], [356, 246.419983374], [358, 245.565223614], [360, 244.710463853], [362, 243.855704093], [364, 243.000944332], [366, 242.146184572], [368, 241.291424811], [370, 240.436665051], [372, 239.58190529], [374, 238.72714553], [376, 237.872385769], [378, 237.017626009], [380, 236.162866248], [382, 235.308106488], [384, 234.453346728], [386, 233.598586967], [388, 232.743827207], [390, 231.889067446], [392, 231.034307686], [394, 230.179547925], [396, 229.324788165], [398, 228.470028404], [400, 226.743609671], [402, 225.017190938], [404, 223.290772204], [406, 221.564353471], [408, 219.837934738], [410, 218.111516004], [412, 216.385097271], [414, 214.658678538], [416, 212.932259805], [418, 211.205841071], [420, 209.479422338], [422, 207.753003605], [424, 206.026584871], [426, 204.300166138], [428, 202.573747405], [430, 200.847328671], [432, 199.120909938], [434, 197.394491205], [436, 195.668072472], [438, 193.941653738], [440, 192.215235005], [442, 190.488816272], [444, 188.762397538], [446, 187.035978805], [448, 185.309560072], [450, 183.583141338], [452, 181.856722605], [454, 180.130303872], [456, 178.403885139], [458, 176.677466405], [460, 174.951047672], [462, 173.224628939], [464, 171.498210205], [466, 169.771791472], [468, 168.045372739], [470, 166.318954006], [472, 164.592535272], [474, 162.866116539], [476, 161.139697806], [478, 159.413279072], [480, 157.686860339], [482, 158.084199001], [484, 158.481537662], [486, 158.878876324], [488, 159.276214985], [490, 159.673553647], [492, 160.070892309], [494, 160.46823097], [496, 160.865569632], [498, 161.262908293], [500, 161.660246955], [502, 162.057585617], [504, 162.454924278], [506, 162.85226294], [508, 163.249601601], [510, 163.646940263], [512, 164.044278924], [514, 164.441617586], [516, 164.838956248], [518, 165.236294909], [520, 165.633633571], [522, 166.030972232], [524, 166.428310894], [526, 166.825649556], [528, 167.222988217], [530, 167.620326879], [532, 168.01766554], [534, 168.415004202], [536, 168.812342864], [538, 169.209681525], [540, 169.607020187], [542, 170.004358848], [544, 170.40169751], [546, 170.799036172], [548, 171.196374833], [550, 171.593713495], [552, 171.991052156], [554, 172.388390818], [556, 172.785729479], [558, 173.183068141], [560, 173.580406803], [562, 173.977745464], [564, 175.925440726], [566, 177.873135988], [568, 179.820831249], [570, 181.768526511], [572, 183.716221773], [574, 185.663917035], [576, 187.611612297], [578, 189.559307558], [580, 191.50700282], [582, 193.454698082], [584, 195.402393344], [586, 197.350088605], [588, 199.297783867], [590, 201.245479129], [592, 203.193174391], [594, 205.140869652], [596, 207.088564914], [598, 209.036260176], [600, 210.983955438], [602, 212.931650699], [604, 214.879345961], [606, 216.827041223], [608, 218.774736485], [610, 220.722431746], [612, 222.670127008], [614, 224.61782227], [616, 226.565517532], [618, 228.513212793], [620, 230.460908055], [622, 232.408603317], [624, 234.356298579], [626, 236.30399384], [628, 238.251689102], [630, 240.199384364], [632, 242.147079626], [634, 244.094774887], [636, 246.042470149], [638, 247.990165411], [640, 249.937860673], [642, 251.885555934], [644, 249.958439564], [646, 248.031323193], [648, 246.104206822], [650, 244.177090451], [652, 242.24997408], [654, 240.322857709], [656, 238.395741339], [658, 236.468624968], [660, 234.541508597], [662, 232.614392226], [664, 230.687275855], [666, 228.760159484], [668, 226.833043114], [670, 224.905926743], [672, 222.978810372], [674, 221.051694001], [676, 219.12457763], [678, 217.197461259], [680, 215.270344889], [682, 213.343228518], [684, 211.416112147], [686, 209.488995776], [688, 207.561879405], [690, 205.634763034], [692, 203.707646664], [694, 201.780530293], [696, 199.853413922], [698, 197.926297551], [700, 195.99918118], [702, 194.072064809], [704, 192.144948439], [706, 190.217832068], [708, 188.290715697], [710, 186.363599326], [712, 184.436482955], [714, 182.509366584], [716, 180.582250214], [718, 178.655133843], [720, 176.728017472], [722, 174.800901101], [724, 176.771800561], [726, 178.742700021], [728, 180.713599481], [730, 182.684498941], [732, 184.655398401], [734, 186.626297861], [736, 188.597197321], [738, 190.568096781], [740, 192.538996241], [742, 194.509895701], [744, 196.480795161], [746, 198.451694621], [748, 200.422594081], [750, 202.393493541], [752, 204.364393001], [754, 206.335292461], [756, 208.306191921], [758, 210.277091381], [760, 212.247990841], [762, 214.218890301], [764, 216.189789761], [766, 218.160689221], [768, 220.131588681], [770, 222.102488141], [772, 224.073387601], [774, 226.044287061], [776, 228.01518652], [778, 229.98608598], [780, 231.95698544], [782, 233.9278849], [784, 235.89878436], [786, 237.86968382], [788, 239.84058328], [790, 241.81148274], [792, 243.7823822], [794, 245.75328166], [796, 247.72418112], [798, 249.69508058], [800, 251.66598004], [802, 253.6368795]]
        , -1.9)
    bottom_line = Line([[0, 475.740718377], [2, 477.357711185], [4, 478.974703993], [6, 480.5916968], [8, 482.208689608], [10, 483.825682415], [12, 485.442675223], [14, 487.059668031], [16, 488.676660838], [18, 490.293653646], [20, 491.910646454], [22, 493.527639261], [24, 495.144632069], [26, 496.761624877], [28, 498.378617684], [30, 499.995610492], [32, 501.612603299], [34, 503.229596107], [36, 504.846588915], [38, 506.463581722], [40, 508.08057453], [42, 509.697567338], [44, 511.314560145], [46, 512.931552953], [48, 514.548545761], [50, 516.165538568], [52, 517.782531376], [54, 519.399524184], [56, 521.016516991], [58, 522.633509799], [60, 524.250502606], [62, 525.867495414], [64, 527.484488222], [66, 529.101481029], [68, 530.718473837], [70, 532.335466645], [72, 533.952459452], [74, 535.56945226], [76, 537.186445068], [78, 538.803437875], [80, 540.420430683], [82, 542.03742349], [84, 543.654416298], [86, 545.271409106], [88, 546.888401913], [90, 548.505394721], [92, 550.122387529], [94, 551.739380336], [96, 553.356373144], [98, 554.973365952], [100, 556.590358759], [102, 555.098948335], [104, 553.60753791], [106, 552.116127486], [108, 550.624717062], [110, 549.133306637], [112, 547.641896213], [114, 546.150485789], [116, 544.659075364], [118, 543.16766494], [120, 541.676254516], [122, 540.184844091], [124, 538.693433667], [126, 537.202023243], [128, 535.710612818], [130, 534.219202394], [132, 532.72779197], [134, 531.236381545], [136, 529.744971121], [138, 528.253560696], [140, 526.762150272], [142, 525.270739848], [144, 523.779329423], [146, 522.287918999], [148, 520.796508575], [150, 519.30509815], [152, 517.813687726], [154, 516.322277302], [156, 514.830866877], [158, 513.339456453], [160, 511.848046029], [162, 510.356635604], [164, 508.86522518], [166, 507.373814756], [168, 505.882404331], [170, 504.390993907], [172, 502.899583482], [174, 501.408173058], [176, 499.916762634], [178, 498.425352209], [180, 496.933941785], [182, 495.442531361], [184, 493.951120936], [186, 492.459710512], [188, 490.968300088], [190, 489.476889663], [192, 487.985479239], [194, 486.494068815], [196, 485.00265839], [198, 483.511247966], [200, 482.019837542], [202, 480.528427117], [204, 479.037016693], [206, 477.545606268], [208, 476.054195844], [210, 474.56278542], [212, 473.071374995], [214, 471.579964571], [216, 473.507080942], [218, 475.434197313], [220, 477.361313684], [222, 479.288430054], [224, 481.215546425], [226, 483.142662796], [228, 485.069779167], [230, 486.996895538], [232, 488.924011909], [234, 490.851128279], [236, 492.77824465], [238, 494.705361021], [240, 496.632477392], [242, 498.559593763], [244, 500.486710134], [246, 502.413826504], [248, 504.340942875], [250, 506.268059246], [252, 508.195175617], [254, 510.122291988], [256, 512.049408359], [258, 513.976524729], [260, 515.9036411], [262, 517.830757471], [264, 519.757873842], [266, 521.684990213], [268, 523.612106584], [270, 525.539222954], [272, 527.466339325], [274, 529.393455696], [276, 531.320572067], [278, 533.247688438], [280, 535.174804809], [282, 537.101921179], [284, 539.02903755], [286, 540.956153921], [288, 542.883270292], [290, 544.810386663], [292, 546.737503034], [294, 548.664619404], [296, 550.591735775], [298, 552.518852146], [300, 554.445968517], [302, 556.373084888], [304, 558.300201259], [306, 560.227317629], [308, 562.154434], [310, 564.081550371], [312, 566.008666742], [314, 567.935783113], [316, 569.862899484], [318, 571.790015854], [320, 573.717132225], [322, 571.746232765], [324, 569.775333305], [326, 567.804433845], [328, 565.833534385], [330, 563.862634925], [332, 561.891735465], [334, 559.920836005], [336, 557.949936545], [338, 555.979037085], [340, 554.008137626], [342, 552.037238166], [344, 550.066338706], [346, 548.095439246], [348, 546.124539786], [350, 544.153640326], [352, 542.182740866], [354, 540.211841406], [356, 538.240941946], [358, 536.270042486], [360, 534.299143026], [362, 532.328243566], [364, 530.357344106], [366, 528.386444646], [368, 526.415545186], [370, 524.444645726], [372, 522.473746266], [374, 520.502846806], [376, 518.531947346], [378, 516.561047886], [380, 514.590148426], [382, 512.619248966], [384, 510.648349506], [386, 508.677450046], [388, 506.706550586], [390, 504.735651126], [392, 502.764751666], [394, 500.793852206], [396, 498.822952746], [398, 496.852053286], [400, 494.881153826], [402, 492.910254366], [404, 490.939354906], [406, 488.968455446], [408, 486.997555986], [410, 485.026656526], [412, 483.055757066], [414, 481.084857606], [416, 479.113958146], [418, 477.143058686], [420, 475.172159226], [422, 473.201259766], [424, 471.230360306], [426, 472.085120067], [428, 472.939879827], [430, 473.794639588], [432, 474.649399348], [434, 475.504159109], [436, 476.358918869], [438, 477.21367863], [440, 478.06843839], [442, 478.923198151], [444, 479.777957911], [446, 480.632717672], [448, 481.487477432], [450, 482.342237193], [452, 483.196996953], [454, 484.051756713], [456, 484.906516474], [458, 485.761276234], [460, 486.616035995], [462, 487.470795755], [464, 488.325555516], [466, 489.180315276], [468, 490.035075037], [470, 490.889834797], [472, 491.744594558], [474, 492.599354318], [476, 493.454114079], [478, 494.308873839], [480, 495.1636336], [482, 496.01839336], [484, 496.873153121], [486, 497.727912881], [488, 498.582672641], [490, 499.437432402], [492, 500.292192162], [494, 501.146951923], [496, 502.001711683], [498, 502.856471444], [500, 503.711231204], [502, 504.565990965], [504, 505.420750725], [506, 506.275510486], [508, 507.130270246], [510, 507.985030007], [512, 508.839789767], [514, 509.694549528], [516, 510.549309288], [518, 511.404069048], [520, 512.258828809], [522, 513.113588569], [524, 513.96834833], [526, 514.82310809], [528, 515.677867851], [530, 516.532627611], [532, 517.387387372], [534, 516.796346958], [536, 516.205306545], [538, 515.614266132], [540, 515.023225718], [542, 514.432185305], [544, 513.841144892], [546, 513.250104478], [548, 512.659064065], [550, 512.068023652], [552, 511.476983239], [554, 510.885942825], [556, 510.294902412], [558, 509.703861999], [560, 509.112821585], [562, 508.521781172], [564, 507.930740759], [566, 507.339700345], [568, 506.748659932], [570, 506.157619519], [572, 505.566579105], [574, 504.975538692], [576, 504.384498279], [578, 503.793457865], [580, 503.202417452], [582, 502.611377039], [584, 502.020336625], [586, 501.429296212], [588, 500.838255799], [590, 500.247215385], [592, 499.656174972], [594, 499.065134559], [596, 498.474094145], [598, 497.883053732], [600, 497.292013319], [602, 496.700972905], [604, 496.109932492], [606, 495.518892079], [608, 494.927851665], [610, 494.336811252], [612, 493.745770839], [614, 493.154730426], [616, 492.563690012], [618, 491.972649599], [620, 491.381609186], [622, 490.790568772], [624, 490.199528359], [626, 489.608487946], [628, 491.501088121], [630, 493.393688297], [632, 495.286288472], [634, 497.178888647], [636, 499.071488823], [638, 500.964088998], [640, 502.856689174], [642, 504.749289349], [644, 506.641889524], [646, 508.5344897], [648, 510.427089875], [650, 512.31969005], [652, 514.212290226], [654, 516.104890401], [656, 517.997490577], [658, 519.890090752], [660, 521.782690927], [662, 523.675291103], [664, 525.567891278], [666, 527.460491453], [668, 529.353091629], [670, 531.245691804], [672, 533.13829198], [674, 535.030892155], [676, 536.92349233], [678, 538.816092506], [680, 540.708692681], [682, 542.601292856], [684, 544.493893032], [686, 546.386493207], [688, 548.279093383], [690, 550.171693558], [692, 552.064293733], [694, 553.956893909], [696, 555.849494084], [698, 557.742094259], [700, 559.634694435], [702, 561.52729461], [704, 561.048795952], [706, 560.570297293], [708, 560.091798635], [710, 559.613299977], [712, 559.134801318], [714, 558.65630266], [716, 558.177804001], [718, 557.699305343], [720, 557.220806684], [722, 556.742308026], [724, 556.263809368], [726, 555.785310709], [728, 555.306812051], [730, 554.828313392], [732, 554.349814734], [734, 553.871316075], [736, 553.392817417], [738, 552.914318759], [740, 552.4358201], [742, 551.957321442], [744, 551.478822783], [746, 551.000324125], [748, 550.521825466], [750, 550.043326808], [752, 549.56482815], [754, 549.086329491], [756, 548.607830833], [758, 548.129332174], [760, 547.650833516], [762, 547.172334857], [764, 546.693836199], [766, 546.215337541], [768, 545.736838882], [770, 545.258340224], [772, 544.779841565], [774, 544.301342907], [776, 543.822844248], [778, 543.34434559], [780, 542.865846932], [782, 542.387348273], [784, 541.908849615], [786, 541.430350956], [788, 540.951852298], [790, 540.473353639], [792, 539.994854981], [794, 539.516356323], [796, 539.037857664], [798, 538.559359006], [800, 538.080860347], [802, 537.60231689]]
                       , 1.9)
    missile_group = set([])
    message = True
    splash_screen = False
    level = 1
    if distance >= distance_high_list[-1][1]:
        Highscore(distance, score, enter_name).distance_update()
    if score >= score_high_list[-1][1]:
        Highscore(distance, score, enter_name).score_update()
    if distance > best_distance:
        best_distance = distance
    if score > best_score:
        best_score = score
    distance = 0
    score = 0
    time = 0
    global_gold_time = 0
    
# Create frame
frame = simplegui.create_frame("Interstellar", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background("Grey")
frame.set_mouseclick_handler(click)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1200, top_handler)
timer2 = simplegui.create_timer(1800, bottom_handler)
rock_timer = simplegui.create_timer(14000, rock_spawner)
global_gold_timer = simplegui.create_timer(350, global_gold)
level_timer = simplegui.create_timer(15000, level_time)

# Initialize Ship, Sprite
my_ship = Ship([CANVAS_WIDTH / 6, CANVAS_HEIGHT / 2], 0, SHIP_IMAGE, SHIP_INFO)
top_line = Line([[0, 475.740718377]], -1.9)
bottom_line = Line([[0, 103.084350727]], 1.9)
missile_group = set([])
rock_group = [Sprite([CANVAS_WIDTH - 25, CANVAS_HEIGHT / 2], [-2, 0], 0.2, 0.06, ROCK_IMAGE, ROCK_INFO)]
gold_group = [Sprite([CANVAS_WIDTH - 25, CANVAS_HEIGHT / 2], [-3, 0], 0, 0, GOLD_IMAGE, GOLD_INFO)]

# STARTING FRAME
frame.start()
