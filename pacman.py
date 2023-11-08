import copy
from board import boards
import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'white'
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/pacman/{i}.png'), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/orange.png'), (45, 45))
player_x = 450
player_y = 663
direction = 0
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2
counter = 0
flicker = False
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 3
game_over = False
game_won = False


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        screen.blit(self.img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]

        x_pos = self.center_x // num2
        y_pos = self.center_y // num1
        x_mod = self.center_x % num2
        y_mod = self.center_y % num1

        if 0 < x_pos < 29:
            if level[y_pos - 1][x_pos] == 9:
                self.turns[2] = True
            if level[y_pos][x_pos - 1] < 3 or (level[y_pos][x_pos - 1] == 9 and (self.in_box or self.dead)):
                self.turns[1] = True
            if level[y_pos][x_pos + 1] < 3 or (level[y_pos][x_pos + 1] == 9 and (self.in_box or self.dead)):
                self.turns[0] = True
            if level[y_pos + 1][x_pos] < 3 or (level[y_pos + 1][x_pos] == 9 and (self.in_box or self.dead)):
                self.turns[3] = True
            if level[y_pos - 1][x_pos] < 3 or (level[y_pos - 1][x_pos] == 9 and (self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction in (2, 3):
                if 12 <= x_mod <= 18:
                    if level[y_pos + 1][x_pos] < 3 or (level[y_pos + 1][x_pos] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[y_pos - 1][x_pos] < 3 or (level[y_pos - 1][x_pos] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= y_mod <= 18:
                    if level[y_pos][x_pos - 1] < 3 or (level[y_pos][x_pos - 1] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[y_pos][x_pos + 1] < 3 or (level[y_pos][x_pos + 1] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction in (0, 1):
                if 12 <= x_mod <= 18:
                    if level[y_pos + 1][x_pos] < 3 or (level[y_pos + 1][x_pos] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[y_pos - 1][x_pos] < 3 or (level[y_pos - 1][x_pos] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= y_mod <= 18:
                    if level[y_pos][x_pos - 1] < 3 or (level[y_pos][x_pos - 1] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[y_pos][x_pos + 1] < 3 or (level[y_pos][x_pos + 1] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        self.in_box = 350 < self.x_pos < 550 and 370 < self.y_pos < 480
        return self.turns, self.in_box

    def move_orange(self):
        x_diff = self.target[0] - self.x_pos
        y_diff = self.target[1] - self.y_pos

        if self.direction == 0:
            self.x_pos += self.speed if self.turns[0] else 0
            self.direction = 3 if not self.turns[0] else self.direction

        elif self.direction == 1:
            self.x_pos -= self.speed if self.turns[1] else 0
            self.direction = 3 if not self.turns[1] else self.direction

        elif self.direction == 2:
            self.y_pos -= self.speed if self.turns[2] else 0
            self.direction = 0 if not self.turns[2] else self.direction

        elif self.direction == 3:
            self.y_pos += self.speed if self.turns[3] else 0
            self.direction = 0 if not self.turns[3] else self.direction

        if not self.turns[self.direction]:
            if abs(x_diff) > abs(y_diff):
                if x_diff > 0 and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif x_diff < 0 and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            else:
                if y_diff > 0 and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif y_diff < 0 and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30
        return self.x_pos, self.y_pos, self.direction

    def move_red(self):
        x_diff = self.target[0] - self.x_pos
        y_diff = self.target[1] - self.y_pos

        if self.direction == 0:
            self.x_pos += self.speed if self.turns[0] else 0
        elif self.direction == 1:
            self.x_pos -= self.speed if self.turns[1] else 0
        elif self.direction == 2:
            self.y_pos -= self.speed if self.turns[2] else 0
        elif self.direction == 3:
            self.y_pos += self.speed if self.turns[3] else 0

        if not self.turns[self.direction]:
            if abs(x_diff) > abs(y_diff):
                if x_diff > 0 and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif x_diff < 0 and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            else:
                if y_diff > 0 and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif y_diff < 0 and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30

        return self.x_pos, self.y_pos, self.direction

    def move_blue(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
                self.y_pos += self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
                self.y_pos += self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30

        return self.x_pos, self.y_pos, self.direction

    def move_pink(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif self.target[0] > self.x_pos and self.turns[0]:
                self.direction = 0
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif self.target[0] > self.x_pos and self.turns[0]:
                self.direction = 0

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30

        return self.x_pos, self.y_pos, self.direction


def find_path(start, goal, level, turns_allowed):
    open_list = []
    closed_list = []

    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    open_list.append((start, 0))
    came_from = {}

    g_score = {(x, y): float('inf') for y, row in enumerate(level) for x, cell in enumerate(row)}
    g_score[start] = 0

    while open_list:
        current, current_g = min(open_list, key=lambda item: item[1] + heuristic(item[0]))
        open_list.remove((current, current_g))

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        closed_list.append(current)

        for neighbor in get_neighbors(current, level, turns_allowed):
            if neighbor in closed_list:
                continue
            tentative_g = current_g + 1 
            if neighbor not in open_list or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                if neighbor not in [item[0] for item in open_list]:
                    open_list.append((neighbor, f_score))

    return None

    def greedy_find_path(start, goal, level, turns_allowed):
        current = start
        path = [current]

        while current != goal:
            neighbors = get_neighbors(current, level, turns_allowed)
            if not neighbors:
                return None

            current = min(neighbors, key=lambda n: heuristic(n, goal))
            path.append(current)

        return path

def get_neighbors(node, level, turns_allowed):
    x, y = node
    neighbors = []
    if turns_allowed[0] and x < len(level[y]) - 1 and level[y][x + 1] < 3:
        neighbors.append((x + 1, y))
    if turns_allowed[1] and x > 0 and level[y][x - 1] < 3:
        neighbors.append((x - 1, y))
    if turns_allowed[2] and y < len(level) - 1 and level[y + 1][x] < 3:
        neighbors.append((x, y + 1))
    if turns_allowed[3] and y > 0 and level[y - 1][x] < 3:
        neighbors.append((x, y - 1))
    return neighbors


def get_direction(current, next_node):
    x1, y1 = current
    x2, y2 = next_node
    if x1 < x2:
        return 0 
    elif x1 > x2:
        return 1 
    elif y1 < y2:
        return 3
    elif y1 > y2:
        return 2


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, player_x, player_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)

    if not blinky.dead:
        if 340 < blink_x < 560 and 340 < blink_y < 500:
            blink_target = (400, 100)
        else:
            blink_target = (player_x, player_y)
    else:
        blink_target = return_target

    if not inky.dead:
        inky_target_x = 2 * player_x - blink_x
        inky_target_y = 2 * player_y - blink_y

        if 340 < ink_x < 560 and 340 < ink_y < 500:
            ink_target = (400, 100)
        else:
            ink_target = (inky_target_x, inky_target_y)
    else:
        ink_target = return_target

    if not pinky.dead:
        if 340 < pink_x < 560 and 340 < pink_y < 500:
            pink_target = (400, 100)
        else:
            if direction == 0:
                pink_target = (player_x+100, player_y)
            elif direction == 1:
                pink_target = (player_x-100, player_y)
            elif direction == 2:
                pink_target = (player_x, player_y-100)
            else:
                pink_target = (player_x, player_y+100)

    else:
        pink_target = return_target

    if not clyde.dead:
        if 340 < clyd_x < 560 and 340 < clyd_y < 500:
            clyd_target = (400, 100)
        else:
            clyd_target = (player_x, player_y)
    else:
        clyd_target = return_target

    return [blink_target, ink_target, pink_target, clyd_target]


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24

    ghost_speeds = [2, 2, 2, 2]

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y, player_x, player_y)

    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_red()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_orange()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_orange()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_orange()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_blue()
        else:
            inky_x, inky_y, inky_direction = inky.move_orange()
        clyde_x, clyde_y, clyde_direction = clyde.move_orange()
        if not blinky_dead and not blinky.in_box:
            path = find_path((blinky_x // 30, blinky_y // 32), (player_x // 30, player_y // 32), level, turns_allowed)
            if path:
                if len(path) >= 2:
                    blinky_direction = get_direction((blinky_x // 30, blinky_y // 32), path[1])

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()
