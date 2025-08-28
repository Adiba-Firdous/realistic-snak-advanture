import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Game dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 150, 50)
DARK_GREEN = (30, 100, 30)
RED = (200, 30, 30)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45)
COLOR_LIST = [GREEN, DARK_GREEN, RED, BROWN, LIGHT_BROWN, (255, 255, 0), (0, 255, 255), (255, 0, 255)]
OBSTACLE_COLOR = (100, 100, 100)  # Grey color for obstacles

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Realistic Snake Adventure")
clock = pygame.time.Clock()

# Font setup
score_font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 48, bold=True)
menu_font = pygame.font.SysFont('Arial', 32)
game_over_font = pygame.font.SysFont('Arial', 36, bold=True)

# Game background
background_color = GREEN
def draw_background():
    global background_color
    screen.fill(background_color)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN])
        self.color = GREEN
        self.score = 0
        self.last_positions = []
        self.head_color = WHITE
        
        for i in range(1, self.length):
            if self.direction == pygame.K_RIGHT:
                self.positions.append((self.positions[0][0] - i * GRID_SIZE, self.positions[0][1]))
            elif self.direction == pygame.K_LEFT:
                self.positions.append((self.positions[0][0] + i * GRID_SIZE, self.positions[0][1]))
            elif self.direction == pygame.K_UP:
                self.positions.append((self.positions[0][0], self.positions[0][1] + i * GRID_SIZE))
            elif self.direction == pygame.K_DOWN:
                self.positions.append((self.positions[0][0], self.positions[0][1] - i * GRID_SIZE))
        
        self.last_positions = self.positions.copy()
        self.movement_progress = 0
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, direction):
        if (direction == pygame.K_RIGHT and self.direction == pygame.K_LEFT) or \
           (direction == pygame.K_LEFT and self.direction == pygame.K_RIGHT) or \
           (direction == pygame.K_UP and self.direction == pygame.K_DOWN) or \
           (direction == pygame.K_DOWN and self.direction == pygame.K_UP):
            return
        self.direction = direction
    
    def move(self, apple_pos=None, obstacles=None):
        self.last_positions = self.positions.copy()
        self.movement_progress = 0
        
        head = self.get_head_position()
        
        if self.direction == pygame.K_RIGHT:
            new_head = ((head[0] + GRID_SIZE), head[1])
        elif self.direction == pygame.K_LEFT:
            new_head = ((head[0] - GRID_SIZE), head[1])
        elif self.direction == pygame.K_UP:
            new_head = (head[0], (head[1] - GRID_SIZE))
        elif self.direction == pygame.K_DOWN:
            new_head = (head[0], (head[1] + GRID_SIZE))
        
        # Game over if snake hits boundary
        if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
            return True
        
        # Game over if snake hits itself
        if new_head in self.positions[1:]:
            return True
        
        # Game over if snake hits an obstacle
        if obstacles and new_head in obstacles:
            return True
        
        self.positions.insert(0, new_head)
        
        if apple_pos and new_head == apple_pos:
            self.score += 1
            return False
        else:
            self.positions.pop()
            return False
    
    def draw(self, surface, frame_progress):
        self.movement_progress = min(1, self.movement_progress + frame_progress)
        
        for i, (current, last) in enumerate(zip(self.positions, self.last_positions)):
            interp_x = last[0] + (current[0] - last[0]) * self.movement_progress
            interp_y = last[1] + (current[1] - last[1]) * self.movement_progress
            
            if i == 0:
                head_rect = pygame.Rect(interp_x, interp_y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, self.head_color, head_rect)
                pygame.draw.rect(surface, DARK_GREEN, head_rect, 1)
                
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 4
                
                if self.direction == pygame.K_RIGHT:
                    pygame.draw.circle(surface, WHITE, (int(interp_x + GRID_SIZE - eye_offset), int(interp_y + eye_offset)), eye_size)
                    pygame.draw.circle(surface, WHITE, (int(interp_x + GRID_SIZE - eye_offset), int(interp_y + GRID_SIZE - eye_offset)), eye_size)
                elif self.direction == pygame.K_LEFT:
                    pygame.draw.circle(surface, WHITE, (int(interp_x + eye_offset), int(interp_y + eye_offset)), eye_size)
                    pygame.draw.circle(surface, WHITE, (int(interp_x + eye_offset), int(interp_y + GRID_SIZE - eye_offset)), eye_size)
                elif self.direction == pygame.K_UP:
                    pygame.draw.circle(surface, WHITE, (int(interp_x + eye_offset), int(interp_y + eye_offset)), eye_size)
                    pygame.draw.circle(surface, WHITE, (int(interp_x + GRID_SIZE - eye_offset), int(interp_y + eye_offset)), eye_size)
                elif self.direction == pygame.K_DOWN:
                    pygame.draw.circle(surface, WHITE, (int(interp_x + eye_offset), int(interp_y + GRID_SIZE - eye_offset)), eye_size)
                    pygame.draw.circle(surface, WHITE, (int(interp_x + GRID_SIZE - eye_offset), int(interp_y + GRID_SIZE - eye_offset)), eye_size)

                pupil_size = eye_size // 2
                if self.direction == pygame.K_RIGHT:
                    pygame.draw.circle(surface, BLACK, (int(interp_x + GRID_SIZE - eye_offset + pupil_size/2), int(interp_y + eye_offset)), pupil_size)
                    pygame.draw.circle(surface, BLACK, (int(interp_x + GRID_SIZE - eye_offset + pupil_size/2), int(interp_y + GRID_SIZE - eye_offset)), pupil_size)
                elif self.direction == pygame.K_LEFT:
                    pygame.draw.circle(surface, BLACK, (int(interp_x + eye_offset - pupil_size/2), int(interp_y + eye_offset)), pupil_size)
                    pygame.draw.circle(surface, BLACK, (int(interp_x + eye_offset - pupil_size/2), int(interp_y + GRID_SIZE - eye_offset)), pupil_size)
                elif self.direction == pygame.K_UP:
                    pygame.draw.circle(surface, BLACK, (int(interp_x + eye_offset), int(interp_y + eye_offset - pupil_size/2)), pupil_size)
                    pygame.draw.circle(surface, BLACK, (int(interp_x + GRID_SIZE - eye_offset), int(interp_y + eye_offset - pupil_size/2)), pupil_size)
                elif self.direction == pygame.K_DOWN:
                    pygame.draw.circle(surface, BLACK, (int(interp_x + eye_offset), int(interp_y + GRID_SIZE - eye_offset + pupil_size/2)), pupil_size)
                    pygame.draw.circle(surface, BLACK, (int(interp_x + GRID_SIZE - eye_offset), int(interp_y + GRID_SIZE - eye_offset + pupil_size/2)), pupil_size)
            else:
                if i < len(self.last_positions):
                    interp_x = last[0] + (current[0] - last[0]) * self.movement_progress
                    interp_y = last[1] + (current[1] - last[1]) * self.movement_progress
                else:
                    interp_x, interp_y = current
                color = self.color
                body_rect = pygame.Rect(interp_x, interp_y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, color, body_rect, border_radius=2)
                pygame.draw.rect(surface, DARK_GREEN, body_rect, 1, border_radius=2)

class Apple:
    def __init__(self):
        self.randomize_position()
        self.color = RED
        self.change_color()
    
    def randomize_position(self, snake_positions=None, obstacles=None):
        if snake_positions and obstacles:
            while True:
                self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                 random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
                if self.position not in snake_positions and self.position not in obstacles:
                    break
        elif snake_positions:
             while True:
                self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                 random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
                if self.position not in snake_positions:
                    break
        elif obstacles:
            while True:
                self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                 random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
                if  self.position not in obstacles:
                    break
        else:
            self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
    
    def draw(self, surface):
        apple_rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.ellipse(surface, self.color, apple_rect)
        
        highlight_rect = pygame.Rect(self.position[0] + GRID_SIZE//4,
                                     self.position[1] + GRID_SIZE//4,
                                     GRID_SIZE//4, GRID_SIZE//4)
        pygame.draw.ellipse(surface, (255, 150, 150), highlight_rect)
        
        stem_width = GRID_SIZE // 5
        stem_height = GRID_SIZE // 3
        stem_x = self.position[0] + GRID_SIZE // 2 - stem_width // 2
        stem_y = self.position[1] - stem_height // 2
        pygame.draw.rect(surface, BROWN, (stem_x, stem_y, stem_width, stem_height))
        
        leaf_points = [
            (stem_x + stem_width, stem_y),
            (stem_x + stem_width + GRID_SIZE//3, stem_y - GRID_SIZE//4),
            (stem_x + stem_width, stem_y + GRID_SIZE//4)
        ]
        pygame.draw.polygon(surface, GREEN, leaf_points)

    def change_color(self):
        self.color = random.choice(COLOR_LIST)

def generate_obstacles(snake_positions, apple_position):
    obstacles = []
    num_obstacles = 5  # Number of obstacles
    
    for _ in range(num_obstacles):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            obstacle_pos = (x, y)
            if obstacle_pos not in snake_positions and obstacle_pos != apple_position:
                obstacles.append(obstacle_pos)
                break
    return obstacles

def draw_obstacles(surface, obstacles):
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, OBSTACLE_COLOR, obstacle_rect, border_radius=2)
        pygame.draw.rect(surface, DARK_GREEN, obstacle_rect, 1, border_radius=2)

def draw_menu():
    screen.fill(BLACK)
    title_text = title_font.render("Realistic Snake Adventure", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    start_text = menu_font.render("Press SPACE to Start", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(start_text, start_rect)
    
    controls_text1 = score_font.render("Use Arrow Keys or WASD to control the snake", True, WHITE)
    controls_rect1 = controls_text1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4 - 20))
    screen.blit(controls_text1, controls_rect1)
    
    controls_text2 = score_font.render("Press ESC to exit the game", True, WHITE)
    controls_rect2 = controls_text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4 + 20))
    screen.blit(controls_text2, controls_rect2)

def draw_game_over(score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    screen.blit(game_over_text, game_over_rect)
    
    score_text = menu_font.render(f"Your Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(score_text, score_rect)
    
    restart_text = menu_font.render("Press SPACE to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
    screen.blit(restart_text, restart_rect)
    
    menu_text = score_font.render("Press ESC to Return to Menu", True, WHITE)
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3 + 50))
    screen.blit(menu_text, menu_rect)

def show_score(surface, score):
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, 10))
    
    bg_rect = pygame.Rect(5, 5, score_rect.width + 10, score_rect.height + 10)
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 128))
    surface.blit(bg_surface, bg_rect)
    
    surface.blit(score_text, score_rect)

def main():
    snake = Snake()
    apple = Apple()
    obstacles = []
    
    game_state = MENU
    
    base_speed = 5
    speed_increment = 0.5  # Increased speed increment for more noticeable effect
    current_speed = base_speed
    last_update_time = 0
    
    frame_time = 0
    last_frame_time = pygame.time.get_ticks()
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        frame_time = (current_time - last_frame_time) / 1000.0
        last_frame_time = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if game_state == MENU:
                    if event.key == pygame.K_SPACE:
                        game_state = PLAYING
                        snake.reset()
                        apple.randomize_position(snake.positions, obstacles)
                        current_speed = base_speed
                        background_color = GREEN
                        obstacles = generate_obstacles(snake.positions, apple.position)
                
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        game_state = PLAYING
                        snake.reset()
                        apple.randomize_position(snake.positions, obstacles)
                        current_speed = base_speed
                        background_color = GREEN
                        obstacles = generate_obstacles(snake.positions, apple.position)
                    elif event.key == pygame.K_ESCAPE:
                        game_state = MENU
                
                elif game_state == PLAYING:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        snake.turn(pygame.K_UP)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        snake.turn(pygame.K_DOWN)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        snake.turn(pygame.K_LEFT)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        snake.turn(pygame.K_RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        game_state = MENU
        
        if pygame.mouse.get_pressed()[0] and game_state == PLAYING:
            mouse_pos = pygame.mouse.get_pos()
            head_pos = snake.get_head_position()
            
            dx = mouse_pos[0] - head_pos[0]
            dy = mouse_pos[1] - head_pos[1]
            
            if abs(dx) > abs(dy):
                if dx > 0:
                    snake.turn(pygame.K_RIGHT)
                else:
                    snake.turn(pygame.K_LEFT)
            else:
                if dy > 0:
                    snake.turn(pygame.K_DOWN)
                else:
                    snake.turn(pygame.K_UP)
        
        if game_state == PLAYING:
            current_time = pygame.time.get_ticks()
            move_delay = 1000 / current_speed
            
            if current_time - last_update_time > move_delay:
                game_over = snake.move(apple.position, obstacles)
                
                if game_over:
                    game_state = GAME_OVER
                
                head_pos = snake.get_head_position()
                
                if head_pos == apple.position:
                    current_speed += speed_increment  # Increase speed
                    apple.randomize_position(snake.positions, obstacles)
                    apple.change_color()
                    snake.color = random.choice(COLOR_LIST)
                    snake.head_color = random.choice(COLOR_LIST)
                    
                    # Change background color to a *different* color
                    available_colors = [c for c in COLOR_LIST if c != background_color]
                    if available_colors:
                        background_color = random.choice(available_colors)
                    else:
                        background_color = random.choice(COLOR_LIST)  # Fallback if all colors are used
                    
                    obstacles = generate_obstacles(snake.positions, apple.position)
                
                last_update_time = current_time
        
        if game_state == MENU:
            draw_menu()
        
        elif game_state == PLAYING:
            draw_background()
            snake.draw(screen, frame_time * current_speed)
            apple.draw(screen)
            draw_obstacles(screen, obstacles)  # Draw the obstacles
            show_score(screen, snake.score)
        
        elif game_state == GAME_OVER:
            draw_game_over(snake.score)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
