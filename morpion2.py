import pygame 
import sys

#initialisation 
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion")

#couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) #pour les croix
BLUE = (0, 0, 255) #pour les ronds

#Grille
CELL_SIZE = WIDTH // 3
grid = [[None for _ in range(3)] for _ in range(3)]
current_player = "X" #les croix commencent
game_over = False
winner = True

#Police
font = pygame.font.SysFont('Arial', 100)

def draw_grid():
    #dessin de la grille
    screen.fill(WHITE)
    
    #lignes verticales
    pygame.draw.line(screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), 3)
    pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), 3)
    
    #lignes horizontales
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), 3)
    pygame.draw.line(screen, BLACK, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), 3)
    
def draw_simbols():
    #dessin des croix (X) et des ronds (O)
    for row in range(3):
        for col in range(3):
            if grid[row][col] == "X":
                x = col + CELL_SIZE + CELL_SIZE // 2
                y = row + CELL_SIZE + CELL_SIZE // 2
                
                #dessin des croix
                pygame.draw.line(screen, RED, (x-50, y-50), (x+50, y+50), 5)
                pygame.draw.line(screen, RED, (x+50, y-50), (x-50, y+50), 5)
            elif grid[row][col] == "0":
                x = col + CELL_SIZE + CELL_SIZE // 2
                y = row + CELL_SIZE + CELL_SIZE // 2
                
                pygame.draw.circle(screen, BLUE, (x, y), 50, 5)

def check_winner():
    global winner, game_over
    #vérification des lignes et colonnes
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0] is not None :
            winner = grid[i][0]
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i] is not None : 
            winner = grid[0][i]
        
        #vérif des diagonales
        if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] is not None:
            winner = grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] is not None:
            winner = grid[0][2]
        
        #match nul
        if all(cell is not None for row in grid for cell in row) and winner in None:
            winner = "Match Nul"
            
        if winner is not None:
            game_over = True
                
def draw_status():
    #affichage du résultat
    status_font = pygame.font.SysFont('Arial', 40)
    
    if not game_over:
        text = "Au joueur {} de jouer !".format(current_player)
        color = RED if current_player == "X" else BLUE
    else : 
        if winner == "Match nul":
            text = "Match nul"
            color = BLACK
        else :
            text = "Joueur {} gagne !".format(winner)
            color = RED if winner == "X" else BLUE
    text_surface = status_font.render(text, True, color)
    screen.blit(text_surface, (20, 20))

def reset_game():
    #reinitialise le jeu
    global grid, current_player, game_over, winner
    grid = [[None for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None

#boucle principale

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if grid[row][col] is None:
                grid[row][col] = current_player
                check_winner()
                #Alterne entre X et O a chaque tour
                current_player = "0" if current_player == "X" else "X"
                
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
    
    #Affichage
    draw_grid()
    draw_simbols()
    draw_status()
    
    if game_over:
        restart_font = pygame.font.SysFont('Arial', 30)
        restart_text = restart_font.render("Appuyer sur R pour rejouer", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 40))
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)