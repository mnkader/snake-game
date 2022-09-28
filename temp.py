import math
import queue
from collections import deque as deque
import traceback
import pygame
import time
import random
from logger import GenericLogger

logging = GenericLogger('snake.log', 'C:\\MNK\\myprojects\\snake-game\\')
def get_neighbors(position, obstacles : list):
    in_grid_neighbors = []
    neighbors = [[position[0] + 10, position[1]],
                 [position[0] - 10, position[1]],
                 [position[0], position[1] + 10],
                 [position[0], position[1] - 10]]
    
    for pos in neighbors:
        if is_valid_pos(pos, obstacles):
           in_grid_neighbors.append(pos)
    return in_grid_neighbors


def distance(pos1, pos2):
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)


# Each position is a tuple because python doesn't allow hashing lists


 
dRow = [ -1, 0, 1, 0]
dCol = [ 0, 1, 0, -1]

snake_speed = 11
 
# Window size
window_x = 400
window_y = 400

def is_valid_pos(pos : tuple, obstacles : list):
    for obstacle in obstacles:
        if pos in obstacle:
            return False
    if pos[0] < 0 or pos[0] >= window_x or pos[1] < 0 or pos[1] >= window_x:
        return False
    return True

GRID = [[i*10, j*10] for i in range(window_x//10) for j in range(window_y//10)]
#ADJACENCY_DICT = {tuple(pos): get_neighbors(pos) for pos in GRID}
# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
 
# Initialising pygame
pygame.init()
 
# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))
 
# FPS (frames per second) controller
fps = pygame.time.Clock()
 
# defining snake default position
snake_position = [100, 50]
astar_snake_position = [150, 100]
ai_snake_position = [50, 50]
 
# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

ai_snake_body = [[50, 50],
              [40, 50],
              [30, 50],
              [20, 50]
              ]

astar_snake_body = [[150, 100],
              [140, 100],
              [130, 100],
              [120, 100]
              ]
# fruit position
fruit_position = [70,
                  70]
 
fruit_spawn = True
 
# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction
 
# initial score
score = 0
bfs_score = 0
astar_score = 0

# displaying Score function
def show_score(choice, color, font, size, my_score, text, place):
   
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)
     
    # create the display surface object
    # score_surface
    score_surface = score_font.render(f'Score {text}: ' + str(my_score), True, color)
     
    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()
     
    # displaying text
    game_window.blit(score_surface,dest=place, area=score_rect)
 
# game over function
def game_over(text_where):
    print(text_where)
    print(f'score {score}')
    print(f'bfs_score {bfs_score}')
    print(f'astar_score {astar_score}')
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
     
    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
     
    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
     
    # setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4)
     
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
     
    # after 2 seconds we will quit the program
    time.sleep(2)
     
    # deactivating pygame library
    pygame.quit()
     
    # quit the program
    quit()

def move_snake(a, s, snake_position):
    if s[0] == a[0] and s[1] > a[1]:
        snake_position[1] -= 10
    if s[0] == a[0] and s[1] < a[1]:
        snake_position[1] += 10
    if s[0] > a[0] and s[1] == a[1]:
        snake_position[0] -= 10
    if s[0] < a[0] and s[1] == a[1]:
        snake_position[0] += 10
    return snake_position

moves = [[-1,0],[1,0],[0,-1],[0,1]]
def breath_first_search(start : tuple, end : tuple, obstacles : list):
    q = [start]
    visited = {tuple(pos): False for pos in GRID}
    visited[start] = True

    prev = {tuple(pos): None for pos in GRID}
    start_timer = time.perf_counter()
    while q:
        node = q.pop(0)
        neighbors = get_neighbors(node, obstacles)
        for next_node in neighbors:
            if not visited[tuple(next_node)] :#and is position free:
                q.append(tuple(next_node))
                visited[tuple(next_node)] = True
                prev[tuple(next_node)] = node
        end_timer = time.perf_counter()
        if (end_timer - start_timer) > 1:
            print(f'Stuck in a loop at breath_first_search')
    path = list()
    prev_node = end
    start_node_found = False
    while not start_node_found:
        if prev[prev_node] is None:
            return []
        prev_node = prev[prev_node]
        if prev_node == start:
            path.append(end)
            return path
        path.insert(0, prev_node)
    
    return []

def h(food, n):
        # Manhattan distance
        return abs(food[0]-n[0]) + abs(food[1]-n[1])

def a_star(start:tuple, end:tuple, obstacles:list):
    q = queue.PriorityQueue()
    q.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    start_timer = time.perf_counter()
    count = 0

    while q:
        
        node = q.get()
        
        neighbors = get_neighbors(node, obstacles)
        if neighbors is None:
            break
        for next_node in neighbors:
            next_node = tuple(next_node)
            new_cost = cost_so_far[node] + 10
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + h(end, next_node)
                q.put(next_node, priority)
                came_from[next_node] = node
        if node == end:
            break
        else:
            count +=1

    
    current = end
    path = [current]

    for _ in range(len(came_from)):
        current = came_from[current]
        path.append(current)
        if current == start:
            break
    if count == 1:
        print('count == 1')
    return path
##################################################################################
try:
    # Main Function
    while True:
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
    
        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10
    
        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        #snake_body.insert(0, list(snake_position))
        #obstacles = [ai_snake_body, snake_body, astar_snake_body]
        obstacles = [astar_snake_body]
        #check if any snake ate a fruit
       #if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
       #    score += 10
       #    fruit_spawn = False
       #else:
       #    snake_body.pop()
        if astar_snake_position[0] == fruit_position[0] and astar_snake_position[1] == fruit_position[1]:
                astar_score += 10
                fruit_spawn = False
        else:
            astar_snake_body.pop()
       #if ai_snake_position[0] == fruit_position[0] and ai_snake_position[1] == fruit_position[1]:
       #    bfs_score += 10
       #    fruit_spawn = False
       #else:
       #    ai_snake_body.pop()

        #spawn a fruit   
        blocked = False 
        while not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x//10)) * 10,
                           random.randrange(1, (window_y//10)) * 10]
            if blocked == True:
                print('unblocking fruit')
                fruit_position = [random.randrange(1, (window_x//10)) * 10,
                           random.randrange(1, (window_y//10)) * 10]
                blocked = False

            for obstacle in obstacles:
                if fruit_position in obstacle:
                    print('fruit pos in obstacle')
                    blocked = True
            if not blocked:
                fruit_spawn = True
            
        if fruit_spawn:
            #do move
            logging.log(f'fruit position {fruit_position}')
            bfs_moves = breath_first_search(tuple(astar_snake_body[0]), tuple(fruit_position), obstacles)
            if bfs_moves is not None and len(bfs_moves):
                logging.log(f'bfs moves: {bfs_moves[0]}')
            else:
                print('no bfs moves')
            astar_moves = a_star(tuple(astar_snake_body[0]), tuple(fruit_position), obstacles)
            if astar_moves is not None and len(astar_moves):
                logging.log(f'astar moves: {astar_moves[0]}')
            else:
                print('no a* moves')
            
            logging.log('all algos created')
            astar_moves.reverse()
            if astar_moves is not None and len(astar_moves):
                if bfs_moves is not None and len(bfs_moves):
                    if len(bfs_moves) >= (len(astar_moves)-1):
                        astar_snake_position = move_snake(astar_moves[1], astar_snake_body[0], astar_snake_position)
                    else: 
                        astar_snake_position = move_snake(bfs_moves[0], astar_snake_body[0], astar_snake_position)
                else:
                    astar_snake_position = move_snake(astar_moves[1], astar_snake_body[0], astar_snake_position)
            else: 
                print('a* path not found')
                astar_score -= 10
                astar_snake_body.pop()
            #if  bfs_moves is not None and len(bfs_moves):
            #    ai_snake_position = move_snake(bfs_moves[0], ai_snake_body[0], ai_snake_position)
            #else:
            #    print('bfs path not found')
            #    bfs_score -= 10
            #    ai_snake_body.pop()
            #create body
            astar_snake_body.insert(0, list(astar_snake_position))
            #ai_snake_body.insert(0, list(ai_snake_position))
     
        game_window.fill(black)
        
       #for pos in snake_body:
       #    pygame.draw.rect(game_window, green,
       #                    pygame.Rect(pos[0], pos[1], 10, 10))
        #for pos in ai_snake_body:
        #    pygame.draw.rect(game_window, blue,
        #                    pygame.Rect(pos[0], pos[1], 10, 10))
        for pos in astar_snake_body:
            pygame.draw.rect(game_window, red,
                            pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))
    
        # Game Over conditions
        #if snake_position[0] < 0 or snake_position[0] > window_x-10:
        #    game_over()
        #if snake_position[1] < 0 or snake_position[1] > window_y-10:
        #    game_over()
    
        # Touching the snake body
       #for block in snake_body[1:]:
       #    if snake_position[0] == block[0] and snake_position[1] == block[1]:
       #        game_over('og snake touched itself')
        #for block in ai_snake_body[1:]:
        #    if ai_snake_position[0] == block[0] and ai_snake_position[1] == block[1]:
        #        game_over('bfs snake touched itself')
        for block in astar_snake_body[1:]:
            if astar_snake_position[0] == block[0] and astar_snake_position[1] == block[1]:
                game_over('astar snake touched itself')
        #touching the other snake
        #if snake head hits any part of the other snake, game_over()
        #for block in ai_snake_body[1:]:
        #    #if snake_position[0] == block[0] and snake_position[1] == block[1]:
        #    #    game_over('bfs snake hit a snake')
        #    if astar_snake_position[0] == block[0] and astar_snake_position[1] == block[1]:
        #        game_over('bfs snake hit a snake')
        #for block in astar_snake_body[1:]:
        #    #if snake_position[0] == block[0] and snake_position[1] == block[1]:
        #    #    game_over('astar snake hit a snake') 
        #    if ai_snake_position[0] == block[0] and ai_snake_position[1] == block[1]:
        #        game_over('astar snake hit a snake') 
       #for block in snake_body[1:]:
       #    if astar_snake_position[0] == block[0] and astar_snake_position[1] == block[1]:
       #        game_over('og snake hit a snake')
       #    if ai_snake_position[0] == block[0] and ai_snake_position[1] == block[1]:
       #        game_over('og snake hit a snake') 
    
        # displaying score countinuously
        #show_score(1, white, 'times new roman', 20, score, 'normal', (10,10))
        #show_score(1, white, 'times new roman', 20, bfs_score, 'bfs', (10,30))
        show_score(1, white, 'times new roman', 20, astar_score, 'astar', (10,10))

        # Refresh game screen
        pygame.display.update()
    
        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)
except Exception as e:
    traceback.print_exc()
    print(e) 
