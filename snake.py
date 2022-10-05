
class Snake:

    bfs = 'BFS'
    astar = 'ASTAR'
    player = 'PLAYER'

    def __init__(self, starting_body: list, type, colour, snake_head):
        self.colour = colour
        self.score = 0
        self.type = type
        self.snake_body = starting_body
        self.snake_position = snake_head

    def move_snake(self,next_move: list = [], snake_head: list = [], direction: str = None):
        if direction is None:
            if snake_head[0] == next_move[0] and snake_head[1] > next_move[1]:
                self.snake_position[1] -= 10
            if snake_head[0] == next_move[0] and snake_head[1] < next_move[1]:
                self.snake_position[1] += 10
            if snake_head[0] > next_move[0] and snake_head[1] == next_move[1]:
                self.snake_position[0] -= 10
            if snake_head[0] < next_move[0] and snake_head[1] == next_move[1]:
                self.snake_position[0] += 10
        else:
            if direction == 'UP':
                self.snake_position[1] -= 10
            if direction == 'DOWN':
                self.snake_position[1] += 10
            if direction == 'LEFT':
                self.snake_position[0] -= 10
            if direction == 'RIGHT':
                self.snake_position[0] += 10
    
    def increase_snake(self):
        self.snake_body.insert(0, list(self.snake_position))
    
    def pop(self):
        self.snake_body.pop()

    def update_score(self, score_increase):
        self.score += score_increase
    
    