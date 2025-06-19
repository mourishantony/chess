import pygame as p
import ChessEngine
import sys
import time

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
MENU_WIDTH = 200
BOARD_WIDTH = WIDTH
TOTAL_WIDTH = WIDTH + MENU_WIDTH

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQ = (240, 217, 181)
DARK_SQ = (181, 136, 99)
HIGHLIGHT = (247, 247, 105, 150)
MOVE_HIGHLIGHT = (124, 252, 0, 150)
MENU_COLOR = (50, 50, 50)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = p.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        
    def draw(self, screen):
        color = BUTTON_HOVER if self.is_hovered else BUTTON_COLOR
        p.draw.rect(screen, color, self.rect)
        p.draw.rect(screen, BLACK, self.rect, 2)  # Border
        
        font = p.font.SysFont("Arial", 20)
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def drawMenu(screen, buttons):
    menu_surface = p.Surface((MENU_WIDTH, HEIGHT))
    menu_surface.fill(MENU_COLOR)
    screen.blit(menu_surface, (BOARD_WIDTH, 0))
    
    for button in buttons:
        button.draw(screen)
    
    # Draw game mode text
    font = p.font.SysFont("Arial", 24, bold=True)
    mode_text = font.render("Game Mode", True, TEXT_COLOR)
    screen.blit(mode_text, (BOARD_WIDTH + 20, 20))
    
    # Draw difficulty text if in AI mode
    if game_mode == 1:  # AI mode
        diff_font = p.font.SysFont("Arial", 18)
        diff_text = diff_font.render(f"Difficulty: {['Easy', 'Medium', 'Hard'][ai_difficulty-1]}", True, TEXT_COLOR)
        screen.blit(diff_text, (BOARD_WIDTH + 20, 70))

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    colors = [LIGHT_SQ, DARK_SQ]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # Highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            
            # Highlight possible moves
            s.fill(p.Color(HIGHLIGHT))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    # Check if the move is a capture
                    if gs.board[move.endRow][move.endCol] != "--":
                        # Draw a circle for captures
                        center = (move.endCol * SQ_SIZE + SQ_SIZE // 2, move.endRow * SQ_SIZE + SQ_SIZE // 2)
                        p.draw.circle(screen, MOVE_HIGHLIGHT, center, SQ_SIZE // 3)
                    else:
                        # Draw a dot for regular moves
                        center = (move.endCol * SQ_SIZE + SQ_SIZE // 2, move.endRow * SQ_SIZE + SQ_SIZE // 2)
                        p.draw.circle(screen, MOVE_HIGHLIGHT, center, SQ_SIZE // 6)

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH + 10, 120, MENU_WIDTH - 20, HEIGHT - 130)
    p.draw.rect(screen, BLACK, moveLogRect, 2)
    
    moveTexts = []
    for i in range(0, len(gs.moveLog), 2):
        moveStr = str(i//2 + 1) + ". " + gs.moveLog[i].getChessNotation()
        if i + 1 < len(gs.moveLog):
            moveStr += " " + gs.moveLog[i + 1].getChessNotation()
        moveTexts.append(moveStr)
    
    padding = 5
    y = padding + 125
    for i in range(len(moveTexts)):
        text = font.render(moveTexts[i], True, TEXT_COLOR)
        if y + text.get_height() < moveLogRect.y + moveLogRect.height:
            screen.blit(text, (moveLogRect.x + padding, y))
            y += text.get_height() + padding

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, True, p.Color('gray'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, True, p.Color('black'))
    screen.blit(textObject, textLocation.move(2, 2))

def drawPromotionMenu(screen, gs):
    if gs.whiteToMove:
        color = 'w'
        y_pos = HEIGHT - 4 * SQ_SIZE
    else:
        color = 'b'
        y_pos = 0
    
    menu_rect = p.Rect(0, y_pos, 4 * SQ_SIZE, SQ_SIZE)
    p.draw.rect(screen, MENU_COLOR, menu_rect)
    p.draw.rect(screen, BLACK, menu_rect, 2)
    
    pieces = ['Q', 'R', 'B', 'N']
    for i, piece in enumerate(pieces):
        piece_img = IMAGES[color + piece]
        screen.blit(piece_img, (i * SQ_SIZE, y_pos))
        
    return menu_rect, pieces

def animateMove(move, screen, board, clock):
    colors = [LIGHT_SQ, DARK_SQ]  # Define the colors list here
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        
        # Erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        
        # Draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceMoved == 'wp' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        # Draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def mainMenu(screen):
    global game_mode, ai_difficulty, running
    
    title_font = p.font.SysFont("Arial", 48, bold=True)
    option_font = p.font.SysFont("Arial", 32)
    
    # Create buttons
    pvp_button = Button(BOARD_WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50, "Player vs Player")
    pvai_button = Button(BOARD_WIDTH//2 - 100, HEIGHT//2, 200, 50, "Player vs AI")
    quit_button = Button(BOARD_WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50, "Quit")
    
    buttons = [pvp_button, pvai_button, quit_button]
    
    while True:
        screen.fill(MENU_COLOR)
        
        # Draw title
        title_text = title_font.render("Chess Game", True, TEXT_COLOR)
        screen.blit(title_text, (BOARD_WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
        
        # Draw buttons
        mouse_pos = p.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                return False, 0, 1
            
            if event.type == p.MOUSEBUTTONDOWN:
                if pvp_button.is_clicked(mouse_pos, event):
                    return True, 0, 1  # PvP mode
                elif pvai_button.is_clicked(mouse_pos, event):
                    # Show difficulty selection
                    difficulty = difficultyMenu(screen)
                    if difficulty == 0:  # Back button
                        continue
                    return True, 1, difficulty  # PvAI mode with selected difficulty
                elif quit_button.is_clicked(mouse_pos, event):
                    return False, 0, 1
        
        p.display.flip()

def difficultyMenu(screen):
    title_font = p.font.SysFont("Arial", 36, bold=True)
    option_font = p.font.SysFont("Arial", 28)
    
    # Create buttons
    easy_button = Button(BOARD_WIDTH//2 - 100, HEIGHT//2 - 80, 200, 50, "Easy")
    medium_button = Button(BOARD_WIDTH//2 - 100, HEIGHT//2 - 20, 200, 50, "Medium")
    hard_button = Button(BOARD_WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, "Hard")
    back_button = Button(BOARD_WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50, "Back")
    
    buttons = [easy_button, medium_button, hard_button, back_button]
    
    while True:
        screen.fill(MENU_COLOR)
        
        # Draw title
        title_text = title_font.render("Select Difficulty", True, TEXT_COLOR)
        screen.blit(title_text, (BOARD_WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
        
        # Draw buttons
        mouse_pos = p.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                return 0
            
            if event.type == p.MOUSEBUTTONDOWN:
                if easy_button.is_clicked(mouse_pos, event):
                    return 1
                elif medium_button.is_clicked(mouse_pos, event):
                    return 2
                elif hard_button.is_clicked(mouse_pos, event):
                    return 3
                elif back_button.is_clicked(mouse_pos, event):
                    return 0
        
        p.display.flip()

def main():
    global game_mode, ai_difficulty
    
    p.init()
    screen = p.display.set_mode((TOTAL_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 12, False, False)
    
    # Show main menu
    running, game_mode, ai_difficulty = mainMenu(screen)
    if not running:
        p.quit()
        return
    
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    sqSelected = ()
    playerClicks = []
    gameOver = False
    
    # AI player
    ai_player = ChessEngine.AIPlayer(ai_difficulty) if game_mode == 1 else None
    
    # Game buttons
    undo_button = Button(BOARD_WIDTH + 20, HEIGHT - 90, MENU_WIDTH - 40, 30, "Undo Move")
    reset_button = Button(BOARD_WIDTH + 20, HEIGHT - 50, MENU_WIDTH - 40, 30, "Reset Game")
    menu_buttons = [undo_button, reset_button]
    
    promotion_active = False
    promotion_rect = None
    promotion_pieces = None
    
    while running:
        humanTurn = (gs.whiteToMove and game_mode == 0) or (not gs.whiteToMove and game_mode == 1 and ai_difficulty == 0) or (gs.whiteToMove and game_mode == 1)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn and not promotion_active:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    
                    # Check if click is on the board
                    if row < 8 and col < 8:
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        
                        if len(playerClicks) == 1 and gs.board[row][col] == "--":
                            sqSelected = ()
                            playerClicks = []
                        
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    if move.isPawnPromotion:
                                        promotion_active = True
                                        promotion_rect, promotion_pieces = drawPromotionMenu(screen, gs)
                                    else:
                                        gs.makeMove(validMoves[i])
                                        moveMade = True
                                        animate = True
                                    sqSelected = ()
                                    playerClicks = []
                                    break
                            if not moveMade:
                                playerClicks = [sqSelected]
                    
                    # Check button clicks
                    for button in menu_buttons:
                        if button.is_clicked(location, e):
                            if button == undo_button:
                                gs.undoMove()
                                moveMade = True
                                gameOver = False
                            elif button == reset_button:
                                gs = ChessEngine.GameState()
                                validMoves = gs.getValidMoves()
                                sqSelected = ()
                                playerClicks = []
                                moveMade = False
                                gameOver = False
                
                elif promotion_active:
                    location = p.mouse.get_pos()
                    if promotion_rect.collidepoint(location):
                        col = location[0] // SQ_SIZE
                        if 0 <= col < 4:
                            promotion_piece = promotion_pieces[col]
                            # Find the promotion move in validMoves
                            for i in range(len(validMoves)):
                                move = validMoves[i]
                                if (move.isPawnPromotion and move.startRow == playerClicks[0][0] and 
                                    move.startCol == playerClicks[0][1] and move.endRow == playerClicks[1][0] and 
                                    move.endCol == playerClicks[1][1]):
                                    # Update the piece moved to the promoted piece
                                    color = 'w' if gs.whiteToMove else 'b'
                                    validMoves[i].pieceMoved = color + promotion_piece
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    break
                            promotion_active = False
                            sqSelected = ()
                            playerClicks = []
            
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False
        
        # AI move finder
        if not gameOver and not humanTurn and not promotion_active:
            AIMove = ai_player.findBestMove(gs, validMoves)
            if AIMove:
                if AIMove.isPawnPromotion:
                    # Always promote to queen for AI
                    color = 'w' if gs.whiteToMove else 'b'
                    AIMove.pieceMoved = color + 'Q'
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
            else:
                print("No valid moves for AI")
        
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)
        drawMenu(screen, menu_buttons)
        
        if promotion_active:
            promotion_rect, promotion_pieces = drawPromotionMenu(screen, gs)
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawEndGameText(screen, "Stalemate")
        
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()