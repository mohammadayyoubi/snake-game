import pygame,sys,random
from pygame.math import Vector2

class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]# create head body and tail using vector
		self.direction = Vector2(0,0) # create direction of the snake
		self.new_block = False# if ate apple it will turn true and add new Block to snake
  
		#load requirements graphics and sound
		
		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha() # 3ashen  ma tkun l image transparent ennu ybayyen shi tahta
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

		

	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]  #-1 howe last element, -2 howe second last element
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)


class FRUIT:
	def __init__(self):
		self.randomize()

	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)
		#pygame.draw.rect(screen,(126,166,114),fruit_rect)

	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)
  
class BLOCK:
    def __init__(self):
        self.positions = []  # represent array of blocks

    def draw_block(self):
        for pos in self.positions:  #draw all blocks in array
            block_rect = pygame.Rect(int(pos.x * cell_size), int(pos.y * cell_size), cell_size, cell_size)
            screen.blit(block, block_rect)

    def randomize(self):
        new_block = None
        while new_block is None or new_block in self.positions or new_block in main_game.snake.body:   # eza kenit block initial position (no prev. blocks) , or if the position of new block already exist in array, create new block
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)
            new_block = Vector2(x, y)
        self.positions.append(new_block)
        
        
class MAIN:

    def __init__(self):
        self.myfile = file = open("maxScore.txt", "r+")
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.blocks = BLOCK()
        self.apples_eaten = 0  # Counter for apples eaten
        self.max_eaten = int (self.myfile.read())

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.blocks.draw_block()  # Draw all blocks

        if not (self.fruit.pos in self.blocks.positions or self.fruit.pos in self.blocks.positions):  #krml ma tetba3 fruit maken block or maken snake
            self.fruit.draw_fruit()
        else:
            self.fruit.randomize()
            self.fruit.draw_fruit()
            print("redraw fruit since same place with block")
            
        self.snake.draw_snake()
        self.draw_score()
        self.draw_Maxscore()
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.apples_eaten += 1
            if self.apples_eaten % 2 == 0:  # Add a block every 2 apples
                self.blocks.randomize()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        for pos in self.blocks.positions:
            if pos == self.snake.body[0]:
                self.game_over()

	
    def game_over(self):
        # self.message("You Lost! Press Q-Quit or C-Play Again",red)
        self.snake.reset()
        self.blocks = BLOCK()  # Reset blocks
        if self.apples_eaten>self.max_eaten:
            self.max_eaten=self.apples_eaten
            with open("maxScore.txt", 'w') as file:  # Open in write mode to clear and update
                file.write(str(self.max_eaten))
        self.apples_eaten = 0  # Reset apple counter
	
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = self.apples_eaten
        score_surface = game_font.render(str(score_text), True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        
    def draw_Maxscore(self):
        score_text = self.max_eaten
        score_surface = game_font.render(('Max Score: '+str(score_text)), True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 400)
        score_y = int(cell_size * cell_number - 750)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
block = pygame.image.load('Graphics/block.jpg')
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
red = (213, 50, 80)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)  # spead on the game where screen update after 150 milli sec

main_game = MAIN()
gameOver = False
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0,-1)
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1,0)
			if event.key == pygame.K_DOWN or event.key==pygame.K_s:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0,1)
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1,0)

	screen.fill((175,215,70))
	main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)
 
