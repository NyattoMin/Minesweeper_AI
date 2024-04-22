import pygame
import sys
import time
import tracemalloc as cpu

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 7
WIDTH = 7
MINES = 10

grid_color = (128, 128, 128)

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

NUM_COLOR = [(0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128),
             (128, 0, 0), (0, 128, 128), (0, 0, 0), (128, 128, 128)]

# Calculate time
start_time = 0
end_time = 0

# Calculate memory
memory_use = 0

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 32)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Import files
spr_emptyGrid = pygame.transform.scale(pygame.image.load("Sprites/empty.png"), (cell_size, cell_size))
spr_flag = pygame.transform.scale(pygame.image.load("Sprites/flag.png"), (cell_size, cell_size))
spr_grid = pygame.transform.scale(pygame.image.load("Sprites/grid.png"), (cell_size, cell_size))
spr_grid1 = pygame.transform.scale(pygame.image.load("Sprites/grid1.png"), (cell_size, cell_size))
spr_grid2 = pygame.transform.scale(pygame.image.load("Sprites/grid2.png"), (cell_size, cell_size))
spr_grid3 = pygame.transform.scale(pygame.image.load("Sprites/grid3.png"), (cell_size, cell_size))
spr_grid4 = pygame.transform.scale(pygame.image.load("Sprites/grid4.png"), (cell_size, cell_size))
spr_grid5 = pygame.transform.scale(pygame.image.load("Sprites/grid5.png"), (cell_size, cell_size))
spr_grid6 = pygame.transform.scale(pygame.image.load("Sprites/grid6.png"), (cell_size, cell_size))
spr_grid7 = pygame.transform.scale(pygame.image.load("Sprites/grid7.png"), (cell_size, cell_size))
spr_grid8 = pygame.transform.scale(pygame.image.load("Sprites/grid8.png"), (cell_size, cell_size))
spr_mine = pygame.transform.scale(pygame.image.load("Sprites/mine.png"), (cell_size, cell_size))
spr_mine = pygame.transform.scale(pygame.image.load("Sprites/mine.png"), (cell_size, cell_size))
spr_mineClicked = pygame.transform.scale(pygame.image.load("Sprites/mineClicked.png"), (cell_size, cell_size))
spr_mineFalse = pygame.transform.scale(pygame.image.load("Sprites/mineFalse.png"), (cell_size, cell_size))

#spr dict
spr_dict = {
    "spr_grid0": spr_grid,
    "spr_grid1": spr_grid1,
    "spr_grid2": spr_grid2,
    "spr_grid3": spr_grid3,
    "spr_grid4": spr_grid4,
    "spr_grid5": spr_grid5,
    "spr_grid6": spr_grid6,
    "spr_grid7": spr_grid7,
    "spr_grid8": spr_grid8
}

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True

# Backtracking game
backtrack = False
backtrack_called = False

# Autoplay game
autoplay = False
autoplaySpeed = 0.01
makeAiMove = False

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            screen.blit(spr_grid, rect)
            if (i, j) in revealed:
                screen.blit(spr_emptyGrid, rect)
            else:
                screen.blit(spr_grid, rect) #!ha
            # pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(spr_mine, rect)
            elif (i, j) in flags:
                screen.blit(spr_flag, rect)
            elif (i, j) in revealed:
                nearby = game.nearby_mines((i, j))
                if nearby:
                    neighbors = spr_dict.get("spr_grid" + str(nearby))
                    neighborsTextRect = neighbors.get_rect()
                    neighborsTextRect.center = rect.center
                    screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # Autoplay Button
    autoplayBtn = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 120,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Autoplay" if not autoplay else "Stop"
    buttonText = mediumFont.render(bText, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = autoplayBtn.center
    pygame.draw.rect(screen, WHITE, autoplayBtn)
    screen.blit(buttonText, buttonRect)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)
    if not autoplay:
        pygame.draw.rect(screen, WHITE, aiButton)
        screen.blit(buttonText, buttonRect)

    # Backtracking Autoplay Button
    backtrackingBtn = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Backtrack" if not backtrack else "Stop"
    buttonText = mediumFont.render(bText, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = backtrackingBtn.center
    pygame.draw.rect(screen, WHITE, backtrackingBtn)
    screen.blit(buttonText, buttonRect)
    
    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 90,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)
    if not autoplay:
        pygame.draw.rect(screen, WHITE, resetButton)
        screen.blit(buttonText, buttonRect)

    # Display time
    time_count = ('%.5f' % (end_time - start_time)) if (lost or game.mines == flags) else ""
    time_count = mediumFont.render(time_count, True, WHITE)
    time_countRect = time_count.get_rect()
    time_countRect.center = ((5 / 6) * width, (2 / 3) * height + 30)
    screen.blit(time_count, time_countRect)
    
    # Display memory usage
    memory_usage = str(memory_use) if (lost or game.mines == flags) else ""
    memory_usage = mediumFont.render(memory_usage, True, WHITE)
    memory_usageRect = memory_usage.get_rect()
    memory_usageRect.center = ((5 / 6) * width, (2 / 3) * height + 65)
    screen.blit(memory_usage, memory_usageRect)
    
    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height + 100)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost and not autoplay:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If Autoplay button clicked, toggle autoplay
        if autoplayBtn.collidepoint(mouse):
            if not lost:
                autoplay = not autoplay
            else:
                autoplay = False
            time.sleep(0.2)
            start_time = time.time()
            cpu.start()
            continue
        
        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # If Autoplay button clicked, toggle autoplay
        if backtrackingBtn.collidepoint(mouse):
            if not lost:
                backtrack = not backtrack
            else:
                backtrack = False
            time.sleep(0.2)
            start_time = time.time()
            cpu.start()
            continue
        
        # Reset game state
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            backtrack = False
            lost = False
            continue

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Make move and update AI knowledge
    def make_move(move):
        if game.is_mine(move):
            return True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)
            if not nearby:
                # Loop over all cells within one row and column
                for i in range(move[0] - 1, move[0] + 2):
                    for j in range(move[1] - 1, move[1] + 2):

                        # Ignore the cell itself
                        if (i, j) == move:
                            continue

                        # Add to the cell collection if the cell is not yet explored
                        # and is not the mine already none
                        if 0 <= i < HEIGHT and 0 <= j < WIDTH and (i, j) not in revealed:
                            make_move((i, j))
                            
    # If backtracking is enabled
    if backtrack and not lost:
        if not backtrack_called:
            arr = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
            print("Generated board")
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    arr[i][j] = game.nearby_mines((i, j)) + game.board[i][j]
                    print(arr[i][j], end=" ")
                print()
                
            grid = ai.minesweeperOperations(arr, HEIGHT, WIDTH)
            if grid is not None:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if grid[i][j]:
                            ai.mark_mine((i, j))
                        else:
                            ai.mark_safe((i, j))
            flags = ai.mines.copy()
            backtrack_called = True
        else:
            move = ai.make_safe_move()
            if move is None:
                memory_use = cpu.get_traced_memory()[1]
                cpu.stop()
                end_time = time.time()
                backtrack = False
                backtrack_called = False

        # Add delay for backtrack
        # if backtrack:
        #     time.sleep(autoplaySpeed)
    
    # If autoplay, make move with AI
    if autoplay or makeAiMove:
        if makeAiMove:
            makeAiMove = False
        if revealed:
            move = ai.make_safe_move()
        else:
            move = (round(HEIGHT/2), round(WIDTH/2))
        if move is None:
            move = ai.make_random_move()
            if move is None:
                flags = ai.mines.copy()
                memory_use = cpu.get_traced_memory()[1]
                cpu.stop()
                end_time = time.time()
                print("No moves left to make.")
                autoplay = False
            else:
                print("No known safe moves, AI making random move.")
        else:
            print("AI making safe move.")

        # Add delay for autoplay
        # if autoplay:
        #     time.sleep(autoplaySpeed)

    # Make move and update AI knowledge
    if move:
        if make_move(move):
            lost = True
        if game.is_mine(move):
            lost = True
            mine_detonated = move
            autoplay = False
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
