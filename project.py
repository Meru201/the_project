import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -9
PIPE_SPEED = 3
PIPE_GAP = 150
GROUND_HEIGHT = 50

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity  = 0
        self.up_image = pygame.image.load('C:\\Users\\mikaz\\Desktop\\react\\the_project\\img\\Group 1 (3).png')
        self.up_image = pygame.transform.scale(self.up_image, (35, 30))
        self.down_image = pygame.image.load('C:\\Users\\mikaz\\Desktop\\react\\the_project\\img\\Group 2 (1).png')
        self.down_image = pygame.transform.scale(self.down_image, (35, 30))

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y + 15 >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 15
            return True
        return False

    def draw(self, screen):
        if self.velocity < 0:
            screen.blit(self.up_image, (self.x, int(self.y)))
        else:  
            screen.blit(self.down_image, (self.x, int(self.y)))

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False
        self.up_pipe_image = pygame.image.load('C:\\Users\\mikaz\\Desktop\\react\\the_project\\img\\Rectangle 1.png')
        self.down_pipe_image = pygame.image.load('C:\\Users\\mikaz\\Desktop\\react\\the_project\\img\\Rectangle 2.png')
        self.down_pipe_height = SCREEN_HEIGHT - self.height - PIPE_GAP
        self.down_pipe_image_bottom = pygame.transform.rotate(self.down_pipe_image , 180)
        self.down_pipe_image = pygame.transform.scale(self.down_pipe_image, (150, 41))
        self.down_pipe_image_bottom = pygame.transform.scale(self.down_pipe_image_bottom, (150,41))
        


    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        screen.blit(self.up_pipe_image, (self.x, self.height - self.up_pipe_image.get_height()))
        screen.blit(self.down_pipe_image, ((self.x - self.up_pipe_image.get_width()) // 2, self.height - self.down_pipe_image.get_height()))
        screen.blit(self.up_pipe_image, (self.x, self.height + PIPE_GAP))
        screen.blit(self.down_pipe_image_bottom, (self.x, self.height + PIPE_GAP))


    def collide(self, bird):
        if (bird.x + 15 > self.x and bird.x - 15 < self.x + 50):
            if (bird.y - 15 < self.height or bird.y + 15 > self.height + PIPE_GAP):
                return True
        return False

def start_screen(screen):
    font = pygame.font.Font(None, 48)
    title = font.render("Flappy Bird", True, BLACK)
    instructions = font.render("Press SPACE to start", True, BLACK)

    screen.fill(WHITE)
    screen.blit(title, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    screen.blit(instructions, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_over_screen(screen, score, best_score):
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    best_score_text = font.render(f"Best Score: {best_score}", True, BLACK)
    instructions = font.render("Press SPACE to restart", True, BLACK)

    screen.fill(WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    screen.blit(best_score_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 40))
    screen.blit(instructions, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 80))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    best_score = 0
    running = True

    start_screen(screen)

    background_image = pygame.image.load('C:\\Users\\mikaz\\Desktop\\react\\the_project\\img\\Untitled.png')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        if bird.update():
            game_over_screen(screen, score, best_score)
            bird = Bird()
            pipes = []
            score = 0
            continue

        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            if pipe.collide(bird):
                if best_score < score:
                    best_score = score
                score = 0
                bird = Bird()
                pipes = []
                break
            
            if pipe.x + 50 < bird.x and not pipe.passed:
                score += 1
                pipe.passed = True

        bird.draw(screen)
        pipes = [pipe for pipe in pipes if pipe.x > -50]
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        text = font.render(f"Best Score: {best_score}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 1.8, 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

main()