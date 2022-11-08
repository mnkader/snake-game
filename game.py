import math
import queue
from collections import deque as deque
import traceback
import pygame
import time
import random
from logger import GenericLogger
from snake import Snake
from algorithms import Algorithms

class Game:
    #Snakes to create
    snake1 = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
    snake1head = [100, 50]
    snake2 = [[200, 70],
              [190, 70],
              [180, 70],
              [170, 70]
              ]
    snake2head = [200, 70]
    snake3 = [[300, 90],
              [290, 90],
              [280, 90],
              [270, 90]
              ]
    snake3head = [300, 90]

    # defining colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    yellow = pygame.Color(255, 255, 0)

    def __init__(self):        
        self.obstacles = []
        self.snake_speed = 10
        self.is_playable = False
        self.window_x = 500
        self.window_y = 500  
        self.grid = [[i*10, j*10] for i in range(self.window_x//10) for j in range(self.window_y//10)]
        self.algo = Algorithms(self.window_x,self.window_y,self.grid)
        self.fruit_position = [100,90]               
        self.fruit_spawn = True
        self.game_window = None
        self.fps = None
        self.snakes: list[Snake] = [Snake(Game.snake1, Snake.astar, Game.yellow, Game.snake1head)]#,Snake(Game.snake2, Snake.bfs, Game.blue, Game.snake2head)]#,Snake(Game.snake3, Snake.bfs, Game.green, Game.snake3head)]
        self.pygame_init()
    
    def is_valid_pos(self, pos : tuple, obstacles : list):
        for obstacle in obstacles:
            if pos in obstacle:
                return False
        if pos[0] < 0 or pos[0] >= self.window_x or pos[1] < 0 or pos[1] >= self.window_y:
            return False
        return True
    
    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.fps = pygame.time.Clock()


    # displaying Score function
    def show_score(self,color, font, size, my_score, text, place):
    
        score_font = pygame.font.SysFont(font, size)
        
        score_surface = score_font.render(f'Score {text}: ' + str(my_score), True, color)
        
        score_rect = score_surface.get_rect()
        
        self.game_window.blit(score_surface,dest=place, area=score_rect)
 
    def game_over(self):
        scores = [(x.type,x.score) for x in self.snakes]
        print(scores)
        my_font = pygame.font.SysFont('times new roman', 20)

        text_to_render = ''
        for score in scores:
            text_to_render += f'{score[0]} Score is : ' + str(score[1])

        game_over_surface = my_font.render(
            text_to_render, True, Game.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_x/2, self.window_y/4)

        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        time.sleep(2)
        pygame.quit()

        quit()
    
    def get_random(self):
        obstacles = self.get_obstacles()
        temp = obstacles[0][0]
        for obstacle in obstacles:
            while temp in obstacle:
                temp = [random.randrange(1, (self.window_x//10)) * 10,
                                random.randrange(1, (self.window_y//10)) * 10]
        return temp
    
    def get_obstacles(self):
        obstacles = []
        for snake in self.snakes:
            obstacles.append(snake.snake_body.copy())
        return obstacles.copy()

    def run(self):
        direction = 'RIGHT'
        change_to = direction
        try:
            while True:
                obstacles = []
                for snake in self.snakes:
                    obstacles.append(snake.snake_body.copy())

                if self.is_playable:
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
                    #Moving The Players snake
                    self.snakes[0].move_snake([],[],direction)
                    self.snakes[0].increase_snake()

                #did a snake eat the fruit?
                for snake in self.snakes:
                    if snake.snake_body[0][0] == self.fruit_position[0] and snake.snake_body[0][1] == self.fruit_position[1]:
                        snake.update_score(10)
                        self.fruit_spawn = False
                    else:
                        snake.pop()

                #spawn a fruit   
                blocked = False 
                while not self.fruit_spawn:
                    self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
                                random.randrange(1, (self.window_y//10)) * 10]
                    if blocked == True:
                        self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
                                random.randrange(1, (self.window_y//10)) * 10]
                        blocked = False

                    for obstacle in self.get_obstacles():
                        if self.fruit_position in obstacle:
                            blocked = True
                    if not blocked:
                        self.fruit_spawn = True
                #do move
                if self.fruit_spawn:
                    moves = []
                    pos = 0
                    for snake in self.snakes:
                        if snake.type == Snake.bfs:
                            moves = self.algo.breath_first_search(tuple(snake.snake_position),tuple(self.fruit_position),self.get_obstacles())
                            if moves is None or len(moves) == 0:
                                print('no move to fruit')
                                moves = self.algo.breath_first_search(tuple(snake.snake_position),tuple(self.get_random()),self.get_obstacles())
                                if moves is None or len(moves) == 0:
                                    print('no move to random')
                                    self.game_over()
                                else:
                                    snake.move_snake(moves[0],snake.snake_body[0])
                                    snake.increase_snake()
                            else:
                                snake.move_snake(moves[0],snake.snake_body[0])
                                snake.increase_snake()
                        if snake.type == Snake.astar: 
                            moves = self.algo.a_star(tuple(snake.snake_body[0]),tuple(self.fruit_position),self.get_obstacles())
                            
                            if moves is None or len(moves) == 0:
                                print('astar cant find fruit')
                                moves = self.algo.a_star(tuple(snake.snake_body[0]),tuple(self.get_random()),self.get_obstacles())
                                if moves is None or len(moves) == 0:
                                    print('astar cant find random')
                                else:
                                    moves.reverse()
                                    snake.move_snake(moves[1],snake.snake_body[0])
                                    snake.increase_snake()
                            else:
                                moves.reverse()
                                snake.move_snake(moves[1],snake.snake_body[0])
                                snake.increase_snake()
                            
                self.game_window.fill(Game.black)
        
                #draw snakes
                for snake in self.snakes:
                    for pos in snake.snake_body:
                        pygame.draw.rect(self.game_window, snake.colour,
                                        pygame.Rect(pos[0], pos[1], 8, 8))  
                    pygame.draw.rect(self.game_window, Game.white, pygame.Rect(
                        self.fruit_position[0], self.fruit_position[1], 10, 10)) 

                #out of bounds
                for snake in self.snakes:
                    if snake.snake_position[0] < 0 or snake.snake_position[0] > self.window_x-10:
                        print('snake out of bounds')
                        self.game_over()
                    if snake.snake_position[1] < 0 or snake.snake_position[1] > self.window_y-10:
                        print('snake out of bounds')
                        self.game_over()
                    #snake touched another snake or itself
                    for next_snake in self.snakes:
                        if snake.snake_position in next_snake.snake_body[1:]:
                            print(f'{snake.type} hit a place on its body')
                            self.game_over()
                        if snake.snake_body != next_snake.snake_body:
                            if snake.snake_body[0] == next_snake.snake_body[0]:
                                self.game_over()
                pos = 10
                for snake in self.snakes:
                    self.show_score(snake.colour,'times new roman', 15, snake.score, snake.type, (10,pos))
                    pos += 13

                # Refresh game screen
                pygame.display.update() 
            
                # Frame Per Second /Refresh Rate
                self.fps.tick(self.snake_speed)
        except Exception as e:
            traceback.print_exc()
            print(e) 

new_game = Game()
new_game.run()
