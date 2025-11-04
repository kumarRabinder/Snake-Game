import pygame
import random
import sys

# Initialize pygame
pygame.init()

# ---------------- Screen Settings ----------------
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game with Obstacles")

# ---------------- Colors ----------------
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Font and Clock
font = pygame.font.SysFont("comicsansms", 35)
clock = pygame.time.Clock()


# ---------------- Function to Draw the Snake ----------------
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, DARK_GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)


# ---------------- Generate Random Food Position ----------------
def random_food_position(snake_body, obstacles):
    while True:
        # Prevent food from spawning on walls
        x = random.randrange(1, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randrange(1, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        food_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        # Check collision with obstacles or snake body
        if all(not food_rect.colliderect(pygame.Rect(o[0], o[1], CELL_SIZE, CELL_SIZE)) for o in obstacles) and [x, y] not in snake_body:
            return [x, y]


# ---------------- Function to Display Text ----------------
def draw_text(text, color, y_offset=0, size=35):
    font_obj = pygame.font.SysFont("comicsansms", size)
    label = font_obj.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(label, rect)


# ---------------- Function to Show Score ----------------
def show_score(score):
    label = font.render("Score: " + str(score), True, BLUE)
    screen.blit(label, (10, 10))


# ---------------- Game Over Screen ----------------
def game_over_screen(score):
    screen.fill(GRAY)
    draw_text("GAME OVER", RED, -50, 50)
    draw_text(f"Your Score: {score}", WHITE, 20, 40)
    draw_text("Press ENTER to Play Again or ESC to Quit", WHITE, 100, 25)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ---------------- Main Game Loop ----------------
def game_loop():
    # Initial snake setup
    snake_pos = [100, 100]
    snake_body = [[100, 100], [80, 100], [60, 100]]
    direction = 'RIGHT'
    change_to = direction

    # --- Create Walls ---
    walls = []
    for x in range(0, WIDTH, CELL_SIZE):
        walls.append([x, 0])
        walls.append([x, HEIGHT - CELL_SIZE])
    for y in range(0, HEIGHT, CELL_SIZE):
        walls.append([0, y])
        walls.append([WIDTH - CELL_SIZE, y])

    # --- Create Random Obstacles (Stones) ---
    stones = []
    for _ in range(8):
        x = random.randrange(WIDTH // 4, 3 * WIDTH // 4, CELL_SIZE)
        y = random.randrange(HEIGHT // 4, 3 * HEIGHT // 4, CELL_SIZE)
        if [x, y] not in snake_body and [x, y] not in walls:
            stones.append([x, y])

    # --- Generate First Food Position ---
    food_pos = random_food_position(snake_body, stones)
    score = 0
    speed = 10

    # --- Main Loop ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Direction control
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        # --- Move Snake ---
        if direction == 'UP':
            snake_pos[1] -= CELL_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += CELL_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= CELL_SIZE
        elif direction == 'RIGHT':
            snake_pos[0] += CELL_SIZE

        snake_body.insert(0, list(snake_pos))

        # --- Check Food Collision ---
        if snake_pos == food_pos:
            score += 10
            speed += 0.2
            food_pos = random_food_position(snake_body, stones)
        else:
            snake_body.pop()

        # --- Collision Detection ---
        snake_head = pygame.Rect(snake_pos[0], snake_pos[1], CELL_SIZE, CELL_SIZE)

        # Collide with self
        for segment in snake_body[1:]:
            if snake_head.colliderect(pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)):
                game_over_screen(score)

        # Collide with walls
        for wall in walls:
            if snake_head.colliderect(pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE)):
                game_over_screen(score)

        # Collide with stones
        for stone in stones:
            if snake_head.colliderect(pygame.Rect(stone[0], stone[1], CELL_SIZE, CELL_SIZE)):
                game_over_screen(score)

        # --- Drawing Section ---
        screen.fill(BLACK)

        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, GRAY, pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE))

        # Draw stones
        for stone in stones:
            pygame.draw.rect(screen, BROWN, pygame.Rect(stone[0], stone[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (60, 50, 20), pygame.Rect(stone[0], stone[1], CELL_SIZE, CELL_SIZE), 1)

        # Draw snake and food
        draw_snake(snake_body)
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
        show_score(score)

        # Update screen and control speed
        pygame.display.update()
        clock.tick(speed)


# ---------------- Start the Game ----------------
game_loop()
