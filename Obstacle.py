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
            return pygame.Rect(x, y + 40, 40, 100)  # Adjust y-coordinate for small obstacle
        else:
            return pygame.Rect(x, y + 12, 40, 100)

    def update(self):
        self.x -= 15  # Adjust the speed of the obstacle
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

def check_collision(dino, obstacle):
    offset = (obstacle.rect.left - dino.rect.left, obstacle.rect.top - dino.rect.top)
    collision_point = dino.mask.overlap(obstacle.mask, offset)
    return collision_point is not None