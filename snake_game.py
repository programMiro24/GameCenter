import pygame
import random
import os
# import sys

def run(player, start_fps):
    # Инциализация
    pygame.init()
    pygame.mixer.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Classical Snake: '+f"Hello, {player['name']}! Your score is  {player['score']}")
    block_size = 15 # size of one block
    # colors
    green = (0, 255, 0)
    white = (255,255,255)
    black = (0,0,0)
    red = (250,0,0)
    blue = (0,0,250)
    yellow = (200, 200, 0)
    apples=0
    # Начало на клас Snake
    # Всеки клас има харектеристики(атрибути) - променливи и има действие - методи.
    # Зареждаме изобразенията
    if os.path.exists("assets/assets_snake/assets/food.png"):
        red_apple_img = pygame.image.load("assets/assets_snake/assets/food.png")
    else:
        print("Не е заредена food.img! Внимание!")
        red_apple_img = None
    if os.path.exists("assets/assets_snake/assets/apple_boostsize.png"):
        green_apple_img  = pygame.image.load("assets/assets_snake/assets/apple_boostsize.png")
    else:
        print("Не е заредена apple_boostsize.img! Внимание!")
        green_apple_img = None
    if os.path.exists("assets/assets_snake/assets/apple_points.png"):
        yellow_apple_img  = pygame.image.load("assets/assets_snake/assets/apple_points.png")
    else:
        print("Не е заредена apple_points.img! Внимание!")
        yellow_apple_img = None
    if os.path.exists("assets/assets_snake/assets/snake.png"):
        snake_image = pygame.image.load("assets/assets_snake/assets/snake.png")
    else:
        print("Не е заредена snake.png! Внимание!!!")
        snake_image = None
    # Зареждаме аудиото на играта
    if os.path.exists("assets/assets_snake/audio/background_music.wav"):
        background_music = pygame.mixer.Sound("assets/assets_snake/audio/background_music.wav")
    else:
        print(f"Не  е заредена background_music.wav!")
        background_music = None
    if os.path.exists("assets/assets_snake/audio/food.wav"):
        eat_sound = pygame.mixer.Sound("assets/assets_snake/audio/food_music.wav")
    else:
        print(f"Не  е заредена food.wav!")
        eat_sound = None
    points = 0
    class Snake:
        def __init__(self, block_size = 15): # конструктор
            self.block_size = block_size
            self.snake_x = random.randrange(0, width - self.block_size, self.block_size)
            self.snake_y = random.randrange(100, height - self.block_size, self.block_size)
            self.snake_body = []
            self.snake_length = 5
            self.points = points
            self.direction = 'RIGHT'
            self.snake_head = pygame.Rect(self.snake_x, self.snake_y, self.block_size, self.block_size)
            self.init_body()
        def init_body(self): # метод
            self.snake_body.append([self.snake_x, self.snake_y])
            for i in range(1, self.snake_length):
                self.snake_body.append([self.snake_x - i * self.block_size, self.snake_y])
        # Функция за рисуване на змията
        def snake_draw(self):
            color = None
            x,y = 0, 0
            for snake_pos in self.snake_body:
                x,y = snake_pos[0], snake_pos[1]
                if x == self.snake_x and y == self.snake_y:
                    if snake_image:
                        screen.blit(snake_image, (x,y))
                    else:
                        color = blue
                        pygame.draw.rect(screen, color, (x, y, self.block_size, self.block_size))
                else:
                    color = green
                    pygame.draw.rect(screen, color, (x,y,self.block_size,self.block_size))
        def movement(self):
            if self.direction == "LEFT":
                self.snake_x -= self.block_size
            elif self.direction == "RIGHT":
                self.snake_x += self.block_size
            elif self.direction == "UP":
                self.snake_y -= self.block_size
            elif self.direction == "DOWN":
                self.snake_y += self.block_size
        def ending_statment(self):
            if self.snake_x < 0 or self.snake_y < 0 or self.snake_x >= width or self.snake_y >= height:
                # game_over_screen()
                return True
            if [self.snake_x, self.snake_y] in self.snake_body[0:len(self.snake_body)-1:1]: # in snake_body[:-1]
                # game_over_screen()
                return True
            return False
        def snake_update(self):
            self.snake_body.append([self.snake_x, self.snake_y])
            if len(self.snake_body) > self.snake_length:
                self.snake_body.pop(0)
            self.snake_head = pygame.Rect(self.snake_x, self.snake_y, self.block_size, self.block_size)
    # Край на клас Snake
    snake = Snake()
    # food
    # Предложение за начало на клас Food
    class Food:
        def __init__(self, snake_ivan: Snake, block_size=15):
            self.block_size = block_size
            self.apple_type = random.choices([red, green, yellow], weights=[70, 25, 5])[0] # Да се направи с random.choices с тежести
            self.food_x = random.randrange(0, width - self.block_size, self.block_size)
            self.food_y = random.randrange(100, height - self.block_size, self.block_size)
            self.food_rect = pygame.Rect(self.food_x, self.food_y, self.block_size, self.block_size)
            self.apples = apples
            self.snake = snake_ivan
            self.correction_xy()
        def correction_xy(self):
            # Корекция на координатите на ябълката спрямо змията
            while True:
                if [self.food_x, self.food_y] not in self.snake.snake_body:
                    break
                self.food_x = random.randrange(0, width - self.block_size, self.block_size)
                self.food_y = random.randrange(100, height - self.block_size, self.block_size)
        def eat_apples(self):
            if self.snake.snake_head.colliderect(self.food_rect):
                if self.apple_type == red:
                    self.snake.snake_length += 1
                    self.snake.points += 10
                elif self.apple_type == green:
                    self.snake.snake_length += 2
                    self.snake.points += 20
                elif self.apple_type == yellow:
                    self.snake.snake_length += 5
                    self.snake.points += 40
                self.apples += 1
                self.apple_type = random.choices([red, green, yellow], weights=[70, 25, 5])[0]  # Да се направи с random.choices с тежести
                self.food_x = random.randrange(0, width - self.block_size, self.block_size)
                self.food_y = random.randrange(100, height - self.block_size, self.block_size)
                self.food_rect = pygame.Rect(self.food_x, self.food_y, self.block_size, self.block_size)
                if eat_sound:
                    eat_sound.play()
                self.correction_xy()
        def apple_draw(self):
            if self.apple_type == green:
                if green_apple_img:
                    screen.blit(green_apple_img, (self.food_x, self.food_y))
                else:
                    pygame.draw.rect(screen, green, self.food_rect)
            elif self.apple_type == red:
                if red_apple_img:
                    screen.blit(red_apple_img, (self.food_x, self.food_y))
                else:
                    pygame.draw.rect(screen, red, self.food_rect)
            elif self.apple_type == yellow: # else:
                if yellow_apple_img:
                    screen.blit(yellow_apple_img, (self.food_x, self.food_y))
                else:
                    pygame.draw.rect(screen, yellow, self.food_rect)
    food = Food(snake)
    # Предложение за край на клас Food
    # статистика
    # Начало клас Text
    font = pygame.font.SysFont('Comic Sans MS', 30)

    def screen_text(text, color, y):
        title_text = font.render(text, True, color)
        screen.blit(title_text, ((width - title_text.get_width())// 2, y))
    def write_text(text, color, x, y):
        title_text = font.render(text, True, color)
        screen.blit(title_text, (x,y))
    # Край клас Text
    # Начало клас Screens
    def start_screen():
        screen.fill(black)
        screen_text("Snake",green,height//2 - 10)
        screen_text("За начало натисни бутона SPACE.",white,height//2 + 20)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    waiting = False
    def game_over_screen():
        screen.fill(black)
        screen_text("Ти загуби!",red,height//2 - 10)
        screen_text(f"Твоят резултат е: {food.apples}",red,height//2 + 20)
        screen_text("Натисни END за край",red,height//2 + 50)
        screen_text(f"Точки: {snake.points}", red, height // 2 + 80)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_END]:
                    waiting = False

    # КРАЙ КЛАС Screen
    start_screen()
    # след почивката
    clock = pygame.time.Clock()
    running = True
    if background_music:
        background_music.play(loops=-1)
    while running:
        # Динамична скорост
        speed = min(start_fps + apples // 5, 30)
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Забрана за обратно движение
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"
                elif event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
        # Movement
        snake.movement()
        # Условия за край
        is_dead = snake.ending_statment()
        if is_dead:
            game_over_screen()
            running = False
        snake.snake_update()
        # Eat apples
        food.eat_apples()
        # Drawing
        screen.fill(white)
        snake.snake_draw()
        food.apple_draw()
        apples = food.apples
        write_text(f"Изядени ябълки: {apples}",black, 10, 10)
        write_text(f"Точки: {snake.points}", black, 10, 40)
        pygame.display.flip()

    pygame.quit()
    return snake.points
