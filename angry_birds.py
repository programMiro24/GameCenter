import math
import pygame
import os
import random

def run(player):
    pygame.init()
    pygame.mixer.init()
    width = 1000
    height = 600
    dir = "assets/assets_angry_birds"
    if os.path.exists(f"{dir}/hit.wav"):
        hit_sound = pygame.mixer.Sound(f"{dir}/hit.wav")
    else:
        hit_sound= None
        print("Внимание! Ти не си хитнат. ")
    screen = pygame.display.set_mode((width,height))
    background_surface = pygame.image.load(f'{dir}/background.png').convert()
    pygame.display.set_caption("Angry Birds: "+f"Hello, {player['name']}! Your score is {player['score']}")
    icon = pygame.image.load(f"{dir}/angry-birds.png")
    pygame.display.set_icon(icon)

    white = (255,255,255)
    red = (255, 0 ,0)
    green = (0, 255, 0)
    black = (0, 0, 0)

    font = pygame.font.SysFont(None,32)

    if os.path.exists(f"{dir}/hit.wav"):
        hit_sound = pygame.mixer.Sound(f"{dir}/hit.wav")
    else:
        hit_sound= None
        print("Внимание! Ти не си хитнат. ")


    #sligshot_x, sligshot_y = 150, height - 280
    # dragging = False
    # bird_pos = [sligshot_x, sligshot_y]
    # if os.path.exists("angry-birds.png"):
    #     bird_png = pygame.image.load("angry-birds.png")
    # else:
    #     bird_png = None
    #     print("Внимание! ИЗображението птичката бг не може да се зареди!")
    # bird_velocity = [0, 0]
    # bird_radius = 32
    # gravity = 0.5
    # launched = False
    # launcher_timer = 0 #брои времето на изстрела. След 3 сек се връща обратно
    class Bird:
        def __init__(self, slingshot_pos):
            self.slingshot_x = slingshot_pos[0]
            self.slingshot_y = slingshot_pos[1]
            self.bird_pos = slingshot_pos.copy()
            self.bird_velocity = [0, 0]
            self.bird_radius = 32
            self.gravity = 0.5
            self.load_random_image()
            self.launched = False
            self.dragging = False
            self.launcher_timer = 0
            #self.image = pygame.image.load('image/angry-birds.png')
            self.rect = None
        def load_random_image(self):
            files = [f"{dir}/angry-birds.png",f"{dir}/angry-birds-1.png",f"{dir}/angry-birds-2.png",
                     f"{dir}/angry-birds-3.png",f"{dir}/angry-birds-4.png"]
            filesname = random.choice(files)
            self.image = pygame.image.load(filesname)
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect()
        def draw(self):
            if self.image:
                screen.blit(self.image, (self.bird_pos[0] - self.bird_radius,
                                         self.bird_pos[1] - self.bird_radius))
            else:
                pygame.draw.circle(screen, red, self.bird_pos, self.bird_radius)
    bird = Bird([random.randint(400, 760), random.randint(0, height - 120)])
    class Target:
        def __init__(self, x, y, w = 40, h = 40, health = 3):
            self.rect = pygame.Rect(x, y, w, h)
            self.max_health = health
            self.health = health
            self.alive = True # beconut e jiv ZA SEGA!
            self.img = pygame.image.load(f"{dir}/piggy.png")
        def hit(self):
            self.health -= 1
            if self.health <= 0:
                self.alive = False
            if hit_sound:
                hit_sound.play()





        def draw(self, screen):
            if not self.alive:
                return
            if self.health == 3:
                self.img = pygame.image.load(f"{dir}/piggy.png")
            elif self.health == 2:
                self.img = pygame.image.load(f"{dir}/pig2.png")
            else:
                self.img = pygame.image.load(f"{dir}/pig3.png")
            screen.blit(self.img, (self.rect.x, self.rect.y))
    target = Target(random.randint(400, 760), random.randint(0, height-120))

    # target_rect = pygame.Rect(800, height - 120, 40, 40) #начални кординати на мишената
    # target_hit = False


    shots_fired = 0
    hits = 0


    new_game = False

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60)
        screen.blit(background_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not bird.launched:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    bird.distance = math.hypot(mouse_x - bird.bird_pos[0], mouse_y - bird.bird_pos[1])
                    if bird.distance <= bird.bird_radius:
                        bird.dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if bird.dragging:
                    bird.dragging = False
                    bird.launched = True
                    shots_fired += 1
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = bird.slingshot_x - mouse_x
                    dy = bird.slingshot_y - mouse_y
                    bird.bird_velocity = [dx * 0.2, dy * 0.2]

        if bird.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bird.bird_pos[0] = mouse_x
            bird.bird_pos[1] = mouse_y

        elif bird.launched:
            bird.bird_velocity[1] += bird.gravity
            bird.bird_pos[0] += bird.bird_velocity[0]
            bird.bird_pos[1] += bird.bird_velocity[1]
            bird.launcher_timer += dt
            if bird.bird_pos[0] > width or bird.bird_pos[1] > height:
                bird.bird_pos = [bird.slingshot_x, bird.slingshot_y]
                bird.bird_velocity = [0,0]
                bird.launched = False

        if target.alive:
            bird.rect = pygame.Rect(bird.bird_pos[0] - bird.bird_radius, bird.bird_pos[1] - bird.bird_radius,
                                    bird.bird_radius * 2, bird.bird_radius * 2)
            if bird.rect.colliderect(target.rect):
                if bird.launched:
                    target.hit()
                if hit_sound:
                    hit_sound.play()
                hits += 1

                bird.bird_pos = [bird.slingshot_x, bird.slingshot_y]
                bird.bird_velocity = [0,0]
                bird.launched = False
                if not target.alive:
                    new_game = True
        bird.draw()
        pygame.draw.line(screen, black, (bird.slingshot_x, bird.slingshot_y), (int(bird.bird_pos[0]),
                                                        int(bird.bird_pos[1])), 2)
        pygame.draw.circle(screen, black, (bird.slingshot_x, bird.slingshot_y), 5)
        target.draw(screen)
        # pygame.draw.rect(screen, green, target)
        if new_game:
            target = Target(random.randint(400, 760), random.randint(0, height - 120))
            target.draw(screen)
            bird.launched = bird.dragging = False
            bird.load_random_image()
            bird = Bird([random.randint(400, 760), random.randint(0, height - 120)])
            bird.draw()
            new_game = False
        text1 = font.render(f'Изстрели:{shots_fired}', True, black)
        text2 = font.render(f'Удари:{hits}', True, black)
        screen.blit(text1,(10,10))
        screen.blit(text2, (10, 40))
        pygame.display.update()
    pygame.quit()
    return hits
