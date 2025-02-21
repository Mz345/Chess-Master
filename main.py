# two player chess in python with Pygame!
# part one, set up variables images and game loop

import pygame

pygame.init()
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
smallfont = pygame.font.Font('freesansbold.ttf', 30)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60 
square_size = 100  
board_size = square_size * 8  # 8 squares per row and column
left_space_width = square_size*2
right_space_width = square_size*2
board_x = (WIDTH - board_size) // 2
board_y = 0



# game variables and images
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),(8, 0), (9, 0),
                   (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),(8, 1), (9, 1) ]
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [ (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),(8, 7), (9, 7),
                   (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),(8, 6), (9, 6) ]
captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('assets/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('assets/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False



def draw_board():
    skin=(255,224,189)
    brown=(139,69,19)
    for row in range(8):
        for col in range(8):
            # Alternate colors
            color = skin if (row + col) % 2 == 0 else brown
            pygame.draw.rect(screen, color, (board_x + col * square_size, board_y + row * square_size, square_size, square_size))
            status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
            pygame.draw.rect(screen,color=(0,255,0),rect=(200, 800, 800, 200))
            screen.blit(big_font.render(status_text[turn_step], True, 'black'), (220, 820))
            for i in range(11):
                pygame.draw.line(screen, 'black', (200, 100 * i), (1000, 100 * i), 2)
                pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
            pygame.draw.rect(screen, color=(0,0,255),rect=(1000, 800, 200, 200))
            screen.blit(medium_font.render('RESIGN', True, 'black'), (1020, 830))
            pygame.draw.rect(screen, color=(255,0,0), rect=(0,800,200,200))
            screen.blit(smallfont.render("LET'S PLAY", True, 'black'), (20, 830))


def draw_captured_pieces():
    black=(0,0,0)
    gray=(211,211,211)
    # Draw the left section for eliminated pieces
    pygame.draw.rect(screen, black, (0, 0, left_space_width, HEIGHT - square_size))

    # Placeholder for eliminated pieces (e.g., circles)
    for i in range(16):
        row = i // 2  # Each row holds 2 pieces
        col = i % 2   # Alternate columns
        x = col * 100  # Centered in the left section
        y = row * 50   # Spaced vertically(((
        pygame.draw.rect(screen,black,(x,y,square_size,square_size))


    pygame.draw.rect(screen, gray, (1000, 0, right_space_width, HEIGHT - square_size))

    for i in range(16):
        row = i // 2
        col = i % 2
        x = 1000 + col * 100
        y = row * 50
        pygame.draw.rect(screen,gray,(x,y,square_size,square_size))
        
        

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)

def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn, has_moved=False)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list



# Function to check if the position is within the board boundaries (0 to 9)
def is_within_board(x, y):
    return 2 <= x <= 9 and 0 <= y <= 7

# Function to check for valid moves for each piece type

# Pawn movement: Forward 1 square (if not blocked) and capture diagonally
def check_pawn(position, color, has_moved):
    moves_list = []
    x, y = position
    
    if color == 'white':
        # Move 1 square forward (check for no piece in front)
        if is_within_board(x, y - 1) and (x, y - 1) not in white_locations and (x, y - 1) not in black_locations:
            moves_list.append((x, y - 1))
        
        # Move 2 squares forward (only if the pawn has not moved and no piece is in front)
        if not has_moved:
            if is_within_board(x, y - 1) and (x, y - 1) not in white_locations and (x, y - 1) not in black_locations:  # Check 1 square ahead
                if is_within_board(x, y - 2) and (x, y - 2) not in white_locations and (x, y - 2) not in black_locations:
                    moves_list.append((x, y - 2))  # Can move two squares from the starting position

        # Capture diagonally (check for black pieces)
        if is_within_board(x + 1, y - 1) and (x + 1, y - 1) in black_locations:
            moves_list.append((x + 1, y - 1))
        if is_within_board(x - 1, y - 1) and (x - 1, y - 1) in black_locations:
            moves_list.append((x - 1, y - 1))
        
    else:  # black pawn movement
        # Move 1 square forward (check for no piece in front)
        if is_within_board(x, y + 1) and (x, y + 1) not in white_locations and (x, y + 1) not in black_locations:
            moves_list.append((x, y + 1))
        
        # Move 2 squares forward (only if the pawn has not moved and no piece is in front)
        if not has_moved:
            if is_within_board(x, y + 1) and (x, y + 1) not in white_locations and (x, y + 1) not in black_locations:  # Check 1 square ahead
                if is_within_board(x, y + 2) and (x, y + 2) not in white_locations and (x, y + 2) not in black_locations:
                    moves_list.append((x, y + 2))  # Can move two squares from the starting position
        
        # Capture diagonally (check for white pieces)
        if is_within_board(x + 1, y + 1) and (x + 1, y + 1) in white_locations:
            moves_list.append((x + 1, y + 1))
        if is_within_board(x - 1, y + 1) and (x - 1, y + 1) in white_locations:
            moves_list.append((x - 1, y + 1))
    
    return moves_list

# Knight movement: L-shape (2 squares in one direction, 1 in another)
def check_knight(position, color):
    moves_list = []
    x, y = position
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for move in knight_moves:
        target = (x + move[0], y + move[1])
        if is_within_board(target[0], target[1]) and target not in white_locations and target not in black_locations:
            moves_list.append(target)
        elif (color == 'white' and target in black_locations) or (color == 'black' and target in white_locations):
            moves_list.append(target)
    return moves_list

# Bishop movement: Diagonal in all 4 directions
def check_bishop(position, color):
    moves_list = []
    x, y = position
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in directions:
        steps = 1
        while True:
            target = (x + direction[0] * steps, y + direction[1] * steps)
            if is_within_board(target[0], target[1]) and target not in white_locations and target not in black_locations:
                moves_list.append(target)
            elif (color == 'white' and target in black_locations) or (color == 'black' and target in white_locations):
                moves_list.append(target)
                break
            else:
                break
            steps += 1
    return moves_list

# Rook movement: Horizontal and vertical
def check_rook(position, color):
    moves_list = []
    x, y = position
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for direction in directions:
        steps = 1
        while True:
            target = (x + direction[0] * steps, y + direction[1] * steps)
            if is_within_board(target[0], target[1]) and target not in white_locations and target not in black_locations:
                moves_list.append(target)
            elif (color == 'white' and target in black_locations) or (color == 'black' and target in white_locations):
                moves_list.append(target)
                break
            else:
                break
            steps += 1
    return moves_list

# Queen movement: Combines bishop and rook
def check_queen(position, color):
    return check_rook(position, color) + check_bishop(position, color)

# King movement: One square in any direction
def check_king(position, color):
    moves_list = []
    x, y = position
    directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for direction in directions:
        target = (x + direction[0], y + direction[1])
        if is_within_board(target[0], target[1]) and target not in white_locations and target not in black_locations:
            moves_list.append(target)
        elif (color == 'white' and target in black_locations) or (color == 'black' and target in white_locations):
            moves_list.append(target)
    return moves_list

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = (0, 255, 0)  # green
    else:
        color = (0, 0, 255)  # blue
        
    for move in moves:
        pygame.draw.rect(screen, color, (move[0] * 100, move[1] * 100, 100, 100), 5)  # draw a border around the square


# draw captured pieces on side of screen
def draw_captured():
    # Set the dimensions for rows and columns
    max_rows = 8  # Maximum number of rows
    col_width = 100  # Column width
    row_height = 100  # Row height
    
    # Draw captured white pieces
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        
        # Calculate row and column positions
        row = i % max_rows
        col = i // max_rows
        
        x = 1025 + col * col_width  # Adjust X position for columns
        y = 20 + row * row_height  # Adjust Y position for rows
        screen.blit(black_images[index], (x, y))
    
    # Draw captured black pieces
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        
        # Calculate row and column positions
        row = i % max_rows
        col = i // max_rows
        
        x = 25 + col * col_width  # Adjust X position for columns
        y = 20 + row * row_height  # Adjust Y position for rows
        screen.blit(white_images[index], (x, y))

def draw_check_and_valid_moves():
    """
    Checks if the king is in check and highlights valid moves to escape.
    """
    if turn_step < 2:  # White's turn
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            
            # Check if the king is in check
            in_check = any(king_location in options for options in black_options)
            
            if in_check:
                # Highlight the king in check
                pygame.draw.rect(screen, 'dark red', 
                                 [king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100], 5)
                
                # Highlight valid moves for the king
                valid_moves = get_valid_king_moves(king_location, white_pieces, white_locations, black_options)
                for move in valid_moves:
                    pygame.draw.rect(screen, 'dark green', 
                                     [move[0] * 100 + 1, move[1] * 100 + 1, 100, 100], 5)
    
    else:  # Black's turn
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            
            # Check if the king is in check
            in_check = any(king_location in options for options in white_options)
            
            if in_check:
                # Highlight the king in check
                pygame.draw.rect(screen, 'dark blue', 
                                 [king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100], 5)
                
                # Highlight valid moves for the king
                valid_moves = get_valid_king_moves(king_location, black_pieces, black_locations, white_options)
                for move in valid_moves:
                    pygame.draw.rect(screen, 'dark green', [move[0] * 100 + 1, move[1] * 100 + 1, 100, 100], 5)
                    
def get_valid_king_moves(king_location, own_pieces, own_locations, opponent_options):
    """
    Calculates valid moves for the king to escape check.
    
    :param king_location: (x, y) position of the king.
    :param own_pieces: List of the player's pieces.
    :param own_locations: List of the player's piece locations.
    :param opponent_options: List of possible moves of opponent pieces.
    :return: List of valid moves for the king.
    """
    # All possible moves for the king
    potential_moves = [
        (king_location[0] + dx, king_location[1] + dy)
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    ]
    
    valid_moves = []
    for move in potential_moves:
        if 0 <= move[0] < 8 and 0 <= move[1] < 8:  # Ensure the move is within bounds
            if move not in own_locations:  # Ensure the move does not land on own pieces
                # Check if the move places the king in a position under attack
                if not any(move in options for options in opponent_options):
                    valid_moves.append(move)
    
    return valid_moves

def draw_game_over():
    pygame.draw.rect(screen, 'black', [340, 400, 600, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (530, 410))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (510, 440))
    

# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_captured_pieces()
    draw_pieces()
    draw_captured()
    draw_check_and_valid_moves()
    
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (10, 8) or click_coords == (11, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords == (10, 8) or click_coords == (11, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
            
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),(8, 7), (9, 7),
                                (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),(8, 6), (9, 6) ]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),(8, 0), (9, 0),
                            ( 2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),(8, 1), (9, 1) ]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()
