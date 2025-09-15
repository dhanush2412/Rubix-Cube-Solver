import pygame
import kociemba
from cube import RubiksCube
import time

# -- Pygame Setup --
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rubik's Cube Solver")
BACKGROUND_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 24)

# -- Cube and Drawing Constants --
COLORS = {
    'W': (255, 255, 255), 'Y': (255, 255, 0), 'B': (0, 0, 255),
    'G': (0, 255, 0), 'R': (255, 0, 0), 'O': (255, 165, 0), 'BLACK': (50, 50, 50)
}
STICKER_SIZE = 30
GAP = 5
FACE_SIZE = 3 * STICKER_SIZE + 2 * GAP

FACE_POSITIONS = {
    'U': (FACE_SIZE + 2 * GAP, GAP),
    'L': (GAP, FACE_SIZE + 2 * GAP),
    'F': (FACE_SIZE + 2 * GAP, FACE_SIZE + 2 * GAP),
    'R': (2 * FACE_SIZE + 3 * GAP, FACE_SIZE + 2 * GAP),
    'B': (3 * FACE_SIZE + 4 * GAP, FACE_SIZE + 2 * GAP),
    'D': (FACE_SIZE + 2 * GAP, 2 * FACE_SIZE + 3 * GAP)
}

# -- Button Definitions --
BUTTON_WIDTH, BUTTON_HEIGHT = 180, 60
BUTTON_COLOR = (0, 100, 200)
BUTTON_HOVER_COLOR = (0, 150, 255)
shuffle_button_rect = pygame.Rect(580, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
solve_button_rect = pygame.Rect(580, 130, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_cube(screen, cube_obj):
    for face_name, start_pos in FACE_POSITIONS.items():
        start_x, start_y = start_pos
        face_colors = cube_obj.faces[face_name]
        for row_idx, row in enumerate(face_colors):
            for col_idx, color_char in enumerate(row):
                x = start_x + col_idx * (STICKER_SIZE + GAP)
                y = start_y + row_idx * (STICKER_SIZE + GAP)
                pygame.draw.rect(screen, COLORS.get(color_char, COLORS['BLACK']),
                                 (x, y, STICKER_SIZE, STICKER_SIZE))

def draw_buttons(screen, mouse_pos):
    # --- Shuffle Button ---
    if shuffle_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, shuffle_button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, shuffle_button_rect, border_radius=10)
    shuffle_text = font.render("Shuffle", True, WHITE)
    screen.blit(shuffle_text, (shuffle_button_rect.x + 35, shuffle_button_rect.y + 15))

    # --- Solve Button ---
    if solve_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, solve_button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, solve_button_rect, border_radius=10)
    solve_text = font.render("Solve", True, WHITE)
    screen.blit(solve_text, (solve_button_rect.x + 50, solve_button_rect.y + 15))

def draw_solution(screen, solution_moves):
    """Draws the solution moves on the screen."""
    if not solution_moves: return
    
    text_y = 220
    moves_str = ' '.join(solution_moves)
    
    total_moves_text = small_font.render(f"Solution ({len(solution_moves)} moves):", True, WHITE)
    screen.blit(total_moves_text, (580, text_y))
    text_y += 25

    max_width = SCREEN_WIDTH - 580 - 20
    words = moves_str.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if small_font.size(current_line + word)[0] < max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    for line in lines:
        line_surface = small_font.render(line, True, WHITE)
        screen.blit(line_surface, (580, text_y))
        text_y += 20

def main():
    my_cube = RubiksCube()
    running = True
    solution_moves = []
    is_busy = False # Flag to prevent clicks during shuffle/solve

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not is_busy:
                if shuffle_button_rect.collidepoint(mouse_pos):
                    is_busy = True
                    print("Shuffling...")
                    solution_moves = [] # Clear old solution
                    my_cube.shuffle(num_moves=30)
                    is_busy = False

                if solve_button_rect.collidepoint(mouse_pos):
                    is_busy = True
                    print("Solving...")
                    
                    # 1. Convert cube state to the Kociemba string format
                    kociemba_str = my_cube.to_kociemba_string()
                    print(f"Cube state: {kociemba_str}")
                    
                    try:
                        # 2. Call the Kociemba solver
                        solution_str = kociemba.solve(kociemba_str)
                        solution_moves = solution_str.split()
                        print(f"Solution found: {solution_str}")

                        # 3. Animate the solution
                        for move in solution_moves:
                            my_cube.apply_moves(move)
                            # Redraw everything for the animation frame
                            screen.fill(BACKGROUND_COLOR)
                            draw_cube(screen, my_cube)
                            draw_buttons(screen, mouse_pos)
                            draw_solution(screen, solution_moves)
                            pygame.display.flip()
                            time.sleep(0.2) # Delay between moves
                            
                    except ValueError as e:
                        print(f"Solver Error: {e}")
                        solution_moves = ["Error: Invalid cube state"]

                    is_busy = False

        # --- Drawing ---
        screen.fill(BACKGROUND_COLOR)
        draw_cube(screen, my_cube)
        draw_buttons(screen, mouse_pos)
        draw_solution(screen, solution_moves)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()