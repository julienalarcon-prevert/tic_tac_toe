import random  #Pour que l'ia puisse jouer avec des cases aléatoires

#fonction qui affiche le tableau de jeu
def afficher_board(board):
    print()
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("---------")
    print()

#fonction qui vérifie si 3 signes sont allignés
def gagnant(board, signe):
    for row in board:
        if row.count(signe) == 3:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == signe:
            return True
    if board[0][0] == board[1][1] == board[2][2] == signe:
        return True
    if board[0][2] == board[1][1] == board[2][0] == signe:
        return True
    return False

#fonction qui vérifie des cases vides pour l'ordinateur
def cases_vides(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]


# fonction qui fait que l'ia puisse jouer de manières aléatoire mais 
# réfléchie avec la prise de conscience des conditions de victoire

def ordinateur(board, signe):
    adversaire = "O" if signe == "X" else "X"
    vides = cases_vides(board)
    for (i, j) in vides:
        board[i][j] = signe
        if gagnant(board, signe):
            return (i, j)
        board[i][j] = " "
    for (i, j) in vides:
        board[i][j] = adversaire
        if gagnant(board, adversaire):
            board[i][j] = " "
            return (i, j)
        board[i][j] = " "
    return random.choice(vides)

#fonction principale qui appelle toutes les fonctions précédentes afin que le jeu puisse marcher
def morpion():
    board = [[" " for _ in range(3)] for _ in range(3)]
    user = "X"
    ia = "O"

    print("Bienvenue dans le jeu du morpion !")
    print("Vous jouez avec le signe X.")
    afficher_board(board)

    while True:
        try:
            x = int(input("Ligne (0-2) : "))
            y = int(input("Colonne (0-2) : "))
        except:
            print("Entrée invalide.")
            continue
        if x not in range(3) or y not in range(3) or board[x][y] != " ":
            print("Case invalide, réessayez.")
            continue
        board[x][y] = user
        afficher_board(board)
        if gagnant(board, user):
            print("🎉 Vous avez gagné !")
            break
        if not cases_vides(board):
            print("Match nul !")
            break
        print("L'ordinateur joue...")
        (i, j) = ordinateur(board, ia)
        board[i][j] = ia
        afficher_board(board)
        if gagnant(board, ia):
            print("💻 L'ordinateur a gagné !")
            break
        if not cases_vides(board):
            print("Match nul !")
            break

#ici on lance la fonction principale "morpion" qui permet d'afficher et de jouer au morpion
morpion()

#on se rends compte que l'ia est imbtable