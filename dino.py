import os
import random
from tkinter import font
import pygame
import sys
import neat

WIN_WIDTH = 800
WIN_HEIGHT = 600
GROUND_LEVEL = 500
SPRITE_LEVEL = 400

class Dino(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.image = pygame.image.load("sprite.png")  # Load the sprite sheet
        self.rect = pygame.Rect(x, y, 85, 100)  # Initial position and size of the dino sprite
        self.frame = 0  # Current frame index for animation
        self.frames = {  # Dictionary to hold the position and size of each dino sprite
            'normal': (1335, 0, 85, 100),
            'left': (1515, 0, 85, 100),
            'right': (1601, 0, 85, 100),
            'dead': (1695, 0, 85, 100)
        }
        self.state = 'normal' 
        self.mask = pygame.mask.Mask((85, 100), False)  # Create an empty mask
        self.update_mask()
        self.animation_counter = 0
        self.animation_speed = 5  # Change this value to adjust animation speed

    def jump(self):
        # Make the dino jump if it's on the ground
        if self.y == SPRITE_LEVEL:
            self.velocity_y = -20  # Jump strength

    def update(self):
        #Animation frame
        self.y += self.velocity_y
        self.rect.y = self.y + 18 
        # Add gravity to the vertical velocity
        
        if self.y < 250:
            self.velocity_y = 20
        # Check if the dino is on the ground
        if self.y >= SPRITE_LEVEL:
            self.y = SPRITE_LEVEL
            self.velocity_y = 0
        self.update_mask()


    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image.subsurface(self.frames[self.state]))

    def draw(self, screen):
        # Draw the dino on the screen
        if self.rect.y < SPRITE_LEVEL:
            self.state = 'normal'
        else:
            # Update the animation counter
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                # Alternate between left and right states when on ground level
                if self.state == 'left':
                    self.state = 'right'
                else:
                    self.state = 'left'

        dino_image = pygame.Surface((self.frames[self.state][2], self.frames[self.state][3]), pygame.SRCALPHA)
        dino_image.blit(self.image, (0, 0), self.frames[self.state])  # Blit the specific sprite from the sprite sheet
        screen.blit(dino_image, self.rect.topleft)  # Draw the dino on the screen at its current position

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.image.load("sprite.png")  # Load the sprite sheet
        self.frame = 0 
        self.frames = {  # Dictionary to hold the position and size of each obstacle sprite
            'small': (440, 0, 40, 100),
            'big': (700, 0, 53, 100)
        }
        self.state = size
        self.rect = self.create_rect(x, y, size)
        self.mask = pygame.mask.Mask((40, 100), False)  # Create an empty mask
        self.update_mask()

    def create_rect(self, x, y, size):
        if size == 'small':
            return pygame.Rect(x, y + 40, 40, 100)  # y-coordinate for small obstacle
        else:
            return pygame.Rect(x, y + 12, 40, 100)

    def update(self):
        self.x -= 20  # The speed of the obstacle as needed
        self.rect.x = self.x
        if self.x < -self.rect.width:
            self.x = WIN_WIDTH
            self.rect.x = self.x
            self.state = 'small' if random.randint(0, 1) == 0 else 'big'
            self.rect = self.create_rect(self.x, self.y, self.state)
            self.update_mask()

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image.subsurface(self.frames[self.state]))

    def draw(self, screen):
        obstacle_image = pygame.Surface((self.frames[self.state][2], self.frames[self.state][3]), pygame.SRCALPHA)
        obstacle_image.blit(self.image, (0, 0), self.frames[self.state])
        screen.blit(obstacle_image, self.rect.topleft)

class Ground:
    def __init__(self, y):
        self.y = y
        self.image = pygame.image.load("sprite.png")
        self.frames = {
            'ground': (2, 104, 2400, 26)
        }
        self.x1 = 0
        self.x2 = self.frames['ground'][2]
        self.rect1 = pygame.Rect(self.x1, y, self.frames['ground'][2], self.frames['ground'][3])
        self.rect2 = pygame.Rect(self.x2, y, self.frames['ground'][2], self.frames['ground'][3])

    def update(self):
        # Move both ground images left
        self.x1 -= 20
        self.x2 -= 20

        # Reset positions if the images go off-screen
        if self.x1 <= -self.frames['ground'][2]:
            self.x1 = self.x2 + self.frames['ground'][2]
        if self.x2 <= -self.frames['ground'][2]:
            self.x2 = self.x1 + self.frames['ground'][2]

        # Update the rect positions
        self.rect1.x = self.x1
        self.rect2.x = self.x2

    def draw(self, screen):
        ground_image1 = pygame.Surface((self.frames['ground'][2], self.frames['ground'][3]), pygame.SRCALPHA)
        ground_image1.blit(self.image, (0, 0), self.frames['ground'])
        screen.blit(ground_image1, self.rect1.topleft)
        
        ground_image2 = pygame.Surface((self.frames['ground'][2], self.frames['ground'][3]), pygame.SRCALPHA)
        ground_image2.blit(self.image, (0, 0), self.frames['ground'])
        screen.blit(ground_image2, self.rect2.topleft)


def check_collision(dino, obstacle):
    offset = (obstacle.rect.left - dino.rect.left, obstacle.rect.top - dino.rect.top)
    collision_point = dino.mask.overlap(obstacle.mask, offset)
    return collision_point is not None

def draw(screen, dinos, obstacles, ground, score):
    screen.fill((255, 255, 255))


    for dino in dinos:
        dino.draw(screen)

    ground.draw(screen)

    for obstacle in obstacles:
        obstacle.draw(screen)

        # Render the score
    font = pygame.font.SysFont('Arial', 30)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

def main(genomes, config):
    # Initialize Pygame and set up the game window
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Dino Jump Game")

    clock = pygame.time.Clock()

    # Lists to hold dino objects, neural networks, and genomes
    dinos = []
    nets = []
    genomes_list = []
    score = 0

    # Initialize dinos, neural networks, and genomes from NEAT's population
    # Loop through each genome in the genomes list
    for _, g in genomes:
        # Create a neural network for the genome using the provided configuration file
        net = neat.nn.FeedForwardNetwork.create(g, config)
        
        # Append the created neural network to the nets list
        nets.append(net)
        
        # Create a new dino object at the starting position (100, SPRITE_LEVEL) and append it to the dinos list
        dinos.append(Dino(100, SPRITE_LEVEL))
        g.fitness = 0
        genomes_list.append(g)

    # Create obstacles and the ground
    obstacles = pygame.sprite.Group()
    obstacles.add(Obstacle(WIN_WIDTH, SPRITE_LEVEL, 'small'))
    obstacles.add(Obstacle(WIN_WIDTH + 400, SPRITE_LEVEL, 'big'))
    ground = Ground(GROUND_LEVEL)

    running = True

    while running:
        # Handle events (e.g., quitting the game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # If all dinos are gone, end the game
        if len(dinos) == 0:
            running = False
            break

        # Loop through each dino and get neural network output
        for x, dino in enumerate(dinos):
            # Find the closest obstacle
            closest_obstacle = None
            min_distance = float('inf')
            for obstacle in obstacles:
                distance = obstacle.rect.x - dino.rect.x
                if 0 < distance < min_distance:
                    closest_obstacle = obstacle
                    min_distance = distance
            
            # If there's a closest obstacle, get the neural network's decision
            if closest_obstacle is not None:
                output = nets[x].activate((dino.y, abs(dino.rect.x - closest_obstacle.rect.x)))
                if output[0] > 0.5:
                    dino.jump()

        # Update the state of all dinos
        for dino in dinos:
            dino.update()

        # Update the state of all obstacles
        for obstacle in obstacles:
            obstacle.update()

        # Update the ground position
        ground.update()

        to_remove = []
        passed_obstacle = False

        # Check for collisions and if dinos have passed obstacles
        for obstacle in obstacles:
            for x, dino in enumerate(dinos):
                if check_collision(obstacle, dino):
                    genomes_list[x].fitness -= 1  # Penalize genome for collision
                    to_remove.append(x)
                elif obstacle.rect.right < dino.rect.left and not passed_obstacle:
                    genomes_list[x].fitness += 5  # Reward genome for passing obstacle
                    passed_obstacle = True

        # Increment the score if any dino passes an obstacle
        if passed_obstacle:
            score += 1

        # Remove dinos that have collided
        for x in sorted(to_remove, reverse=True):
            nets.pop(x)
            dinos.pop(x)
            genomes_list.pop(x)

        # Draw everything on the screen
        draw(screen, dinos, obstacles, ground, score)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)



def run(config_path):
    # Load configuration file 
    config_path = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # Create a new population
    p = neat.Population(config_path)

    # Add reporters to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 30)

    print('\nBest genome:\n{!s}'.format(winner))



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

