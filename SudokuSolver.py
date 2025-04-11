import pygame
import random
import time
from typing import List

pygame.init()

WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver Visualizer")
FONT = pygame.font.SysFont("arial", 40)
SMALL_FONT = pygame.font.SysFont("arial", 20)
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
NUMBER_COLOR = (50, 50, 50)

def show_start_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return 

        WIN.fill(BACKGROUND_COLOR)
        title_text = FONT.render("Sudoku Solver Visualizer", True, NUMBER_COLOR)
        instructions_text = SMALL_FONT.render("Press SPACE to solve, R to reset", True, NUMBER_COLOR)
        start_text = SMALL_FONT.render("Press any key to start", True, NUMBER_COLOR)

        WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 3 - title_text.get_height() / 2))
        WIN.blit(instructions_text, (WIDTH / 2 - instructions_text.get_width() / 2,
                                     HEIGHT / 3 + title_text.get_height()))
        WIN.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2,
                              HEIGHT / 3 + title_text.get_height() + instructions_text.get_height() + 20))
        pygame.display.update()

def draw_grid():
    WIN.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE + 1):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(WIN, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)
        pygame.draw.line(WIN, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), line_width)

def draw_numbers(board: List[List[str]]):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != '.':
                text = FONT.render(board[i][j], True, NUMBER_COLOR)
                WIN.blit(
                    text,
                    (j * CELL_SIZE + (CELL_SIZE - text.get_width()) // 2,
                     i * CELL_SIZE + (CELL_SIZE - text.get_height()) // 2)
                )

def draw_board(board: List[List[str]], solving=False):
    draw_grid()
    draw_numbers(board)
    if solving:
        text = SMALL_FONT.render("Solving...", True, (0, 0, 0))
        WIN.blit(text, (20, WIDTH + 10))
    pygame.display.update()

def process_events():
    events = pygame.event.get()
    flags = {"quit": False, "solve": False, "reset": False}
    for event in events:
        if event.type == pygame.QUIT:
            flags["quit"] = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flags["solve"] = True
            elif event.key == pygame.K_r:
                flags["reset"] = True
    return flags

def is_valid(grid: List[List[str]], row: int, col: int, k: int) -> bool:
    k = str(k)
    if k in grid[row]:
        return False
    for i in range(9):
        if grid[i][col] == k:
            return False
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == k:
                return False
    return True

def solveSudoku_visual(grid: List[List[str]]) -> bool:
    for i in range(9):
        for j in range(9):
            if grid[i][j] == '.':
                candidates = list(range(1, 10))
                random.shuffle(candidates)
                for k in candidates:
                    if is_valid(grid, i, j, k):
                        grid[i][j] = str(k)
                        draw_board(grid, solving=True)
                        pygame.time.delay(50)
                        if process_events()["quit"]:
                            pygame.quit()
                            exit()
                        if solveSudoku_visual(grid):
                            return True
                        grid[i][j] = '.'
                        draw_board(grid, solving=True)
                        pygame.time.delay(50)
                        if process_events()["quit"]:
                            pygame.quit()
                            exit()
                return False
    return True

def solveSudoku_silent(grid: List[List[str]]) -> bool:
    for i in range(9):
        for j in range(9):
            if grid[i][j] == '.':
                candidates = list(range(1, 10))
                random.shuffle(candidates)
                for k in candidates:
                    if is_valid(grid, i, j, k):
                        grid[i][j] = str(k)
                        if solveSudoku_silent(grid):
                            return True
                        grid[i][j] = '.'
                return False
    return True

def generate_complete_board() -> List[List[str]]:
    board = [['.' for _ in range(9)] for _ in range(9)]
    solveSudoku_silent(board)
    return board

def remove_numbers(board: List[List[str]], clues: int = 45) -> List[List[str]]:
    filled_positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(filled_positions)
    total_to_remove = 81 - clues
    for count in range(total_to_remove):
        row, col = filled_positions[count]
        board[row][col] = '.'
    return board

def generate_random_puzzle(clues: int = 45) -> List[List[str]]:
    complete_board = generate_complete_board()
    puzzle_board = [row[:] for row in complete_board]
    puzzle_board = remove_numbers(puzzle_board, clues)
    return puzzle_board

def main():
    show_start_menu()
    clock = pygame.time.Clock()
    
    puzzle = generate_random_puzzle(clues=45)
    board = [row[:] for row in puzzle]  
    solving = False
    solved = False

    while True:
        clock.tick(30)
        flags = process_events()
        if flags["quit"]:
            pygame.quit()
            exit()
        if flags["reset"]:
            puzzle = generate_random_puzzle(clues=45)
            board = [row[:] for row in puzzle]
            solving = False
            solved = False

        if flags["solve"] and not solving:
            solving = True
            solved = False
            solveSudoku_visual(board)
            solved = True

        draw_board(board, solving=(solving and not solved))

if __name__ == "__main__":
    main()
