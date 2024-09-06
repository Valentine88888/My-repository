import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Параметри екрану
WIDTH, HEIGHT = 300, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NeoTetris")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Розмір блоків
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE

# Швидкість гри
FPS = 60
clock = pygame.time.Clock()

# Фігури тетроміно
TETROMINOS = [
    [[1, 1, 1, 1]],  # Лінія
    [[1, 1], [1, 1]],  # Квадрат
    [[0, 1, 0], [1, 1, 1]],  # Т-подібна
    [[1, 1, 0], [0, 1, 1]],  # S-подібна
    [[0, 1, 1], [1, 1, 0]],  # Z-подібна
]

# Функція для перевірки коректності позиції
def is_valid_position(shape, grid, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = x + off_x
                new_y = y + off_y
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >= 0 and grid[new_y][new_x]:
                    return False
    return True

# Функція для об'єднання блоку на сітці
def merge_shape(shape, grid, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + off_y][x + off_x] = cell

# Очищення заповнених рядків
def clear_rows(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_rows = ROWS - len(new_grid)
    new_grid = [[0 for _ in range(COLS)] for _ in range(cleared_rows)] + new_grid
    return new_grid, cleared_rows

# Клас для блоку тетроміно
class Tetromino:
    def __init__(self):
        self.shape = random.choice(TETROMINOS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self, screen):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    pygame.draw.rect(screen, BLUE,
                                     (self.x * BLOCK_SIZE + col * BLOCK_SIZE,
                                      self.y * BLOCK_SIZE + row * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def move(self, dx, dy, grid):
        if is_valid_position(self.shape, grid, (self.x + dx, self.y + dy)):
            self.x += dx
            self.y += dy

    def rotate(self, grid):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        if is_valid_position(rotated_shape, grid, (self.x, self.y)):
            self.shape = rotated_shape

# Основна функція гри
def main():
    running = True
    current_tetromino = Tetromino()
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    drop_time = 0
    drop_speed = 500  # Затримка між падіннями блоків
    score = 0

    while running:
        SCREEN.fill(WHITE)
        drop_time += clock.get_rawtime()

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move(-1, 0, grid)
                if event.key == pygame.K_RIGHT:
                    current_tetromino.move(1, 0, grid)
                if event.key == pygame.K_DOWN:
                    current_tetromino.move(0, 1, grid)
                if event.key == pygame.K_UP:
                    current_tetromino.rotate(grid)

        # Автоматичне падіння блоку
        if drop_time > drop_speed:
            if not is_valid_position(current_tetromino.shape, grid, (current_tetromino.x, current_tetromino.y + 1)):
                merge_shape(current_tetromino.shape, grid, (current_tetromino.x, current_tetromino.y))
                grid, cleared_rows = clear_rows(grid)
                score += cleared_rows * 100
                current_tetromino = Tetromino()
                if not is_valid_position(current_tetromino.shape, grid, (current_tetromino.x, current_tetromino.y)):
                    running = False  # Гра закінчена
            else:
                current_tetromino.move(0, 1, grid)
            drop_time = 0

        # Малюємо блоки
        current_tetromino.draw(SCREEN)

        # Малюємо сітку
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col]:
                    pygame.draw.rect(SCREEN, GREEN,
                                     (col * BLOCK_SIZE, row * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

        # Оновлюємо екран
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
