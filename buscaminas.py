import random, os, time
from sys import platform

def clear():
    if (platform == "linux" or platform == "darwin"):
        os.system("clear")
    elif (platform == "win32"):
        os.system("cls")

def generar_tablero(n, c, blank):
    tablero = []
    minas = c

    minas_posibles = (n*2)
    if (minas >= minas_posibles) or (n == 1):
        return False
 
    casilleros_faltantes = (n**2)
    for x in range(n):
        gm = []
        minas_puestas = 0
 
        for y in range(n):
            if (not minas_puestas >= 2 and minas > 0) and not blank:
                rndm = random.randint(0, 1)
                if rndm == 1 and not blank:
                    gm.append("X")
                    minas_puestas += 1
                    minas -= 1
                else:
                    if (minas_puestas == 0 and (casilleros_faltantes - minas) <= 2):
                        gm.append("X")
                        minas_puestas += 1
                        minas -= 1
                    else: gm.append(" ")
            else:
                gm.append(" ")
            
            casilleros_faltantes -= 1
        tablero.append(gm)
    return tablero
 
def jugar(tablero, fila, columna):
    if ((fila <= 0 or fila > len(tablero)) or (columna <= 0 or columna > len(tablero))):
        return -2, "Invalid row or column."

    fila -= 1
    columna -= 1

    pos_fila = 0
    for f in tablero:
        if (pos_fila == fila):
            pos_col = 0
            for p in f:
                if (pos_col == columna):
                    if (p == "X"):
                        return -1, tablero
                    else:
                        tablero[pos_fila][pos_col] = "*"
                        return 0, tablero

                pos_col += 1
        pos_fila += 1

def check_blanks(tablero):
    blanks = len(tablero) * len(tablero)
    for f in tablero:
        for x in f:
            if (x == "*"):
                blanks -= 1

    return blanks

def show(tablero):
    help_str = ""
    for l in range(len(tablero)):
        if (not help_str): help_str = " (" + str(l+1) + ")"
        else: help_str += "  (" + str(l+1) + ")"

    print(help_str)

    p = 1
    for x in tablero:
        print(x, "(" + str(p) + ")")
        p+=1

def bitacora():
    clear()

    print("¡THANKS FOR PLAYING!")
        
def show_header():
    print("""
███╗   ███╗██╗███╗   ██╗███████╗██████╗ ██╗   ██╗
████╗ ████║██║████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝
██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝ ╚████╔╝ 
██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔═══╝   ╚██╔╝  
██║ ╚═╝ ██║██║██║ ╚████║███████╗██║        ██║   
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝        ╚═╝""")

def end_game(tablero, won, players, losers):
    show_header()
    print("END OF THE GAME\n")

    show(tablero)

    if won:
        print("\WINNERS:")

        x = 1
        for w in players:
            print(str(x) + "-", w)
            x+=1

        if losers:
            print("\LOSERS:")
            x = 1
            for p in losers:
                print(str(x) + "-", p)
                x+=1
    else:
        print("\LOSERS:")
        x = 1
        for p in losers:
            print(str(x) + "-", p)
            x+=1

    print("\nPress ENTER to return to the main menu...")
    input("")

    start_home()

def start_play():
    clear()
    show_header()

    size = int(input("Board size:: "))
    mines = int(input("Number of mines: "))

    t = generar_tablero(size, mines, False)
    if t:
        clear()
        show_header()
        print("Enter the names of the players:\n")

        players = []
        pos = 1
        while(True):
            if ((len(players) + 1) == (size**2)): break

            player = (input(str(pos) + "- ")).capitalize()
            if (player == "" and pos == 1):
                clear()
                show_header()
                print("Enter the names of the players:\n")

                continue
            elif (player == ""): break

            players.append(player)
            pos += 1

        clear()
        t2 = generar_tablero(size, mines, True) # Tablero vacio, solo para visualización del jugador.

        p = 0
        won = False
        losers = []
        coords_used = []
        while(True):
            if not players: break

            show_header()

            blanks = check_blanks(t2)
            if ((blanks == mines) or (len(losers) == mines)):
                won = True
                break

            print("TURN OF: " + players[p] + "\n")
            show(t2)
            
            print("\nEnter your next move: (row, column)")
            mov = input("")
            if (mov == ""):
                clear()
                continue

            mov = mov.split(',')
            if (len(mov) != 2):
                clear()
                continue
            elif ([int(mov[0]), int(mov[1])] in coords_used):
                print("\nYour move was already made on the board before!")
                print("Press ENTER to return to the main menu...")
                input("")

                clear()
                continue

            clear()
            show_header()

            print("TURNO DE: " + players[p] + "\n")

            result = jugar(t, int(mov[0]), int(mov[1]))
            if (result[0] == 0):
                t2[int(mov[0]) - 1][int(mov[1]) - 1] = "*"
                show(t2)

                print("\n" + players[p] + " has not pressed any mine.")
            elif (result[0] == -1):
                t2[int(mov[0]) - 1][int(mov[1]) - 1] = "X"
                show(t2)

                print("\n" + players[p] + " has pressed a mine.")
                
                losers.append(players[p])
                players.pop(p)
            else:
                show(t2)

                print("\n¡Your movement has caused an error to occur!")
                print("Error: " + result[1])

                print("\nPress ENTER to return to the main menu...")
                input("")

                clear()
                continue

            coords_used.append([int(mov[0]), int(mov[1])])

            print("Press ENTER to return to the main menu...")
            input("")
            clear()

            p+=1
            if p >= len(players): p=0
        clear()
        end_game(t, won, players, losers)
    else:
        print("\nIncompatible combination of size and number of mines.")

        print("\nPress ENTER to return to the main menu...")
        input("")

        start_home()

def show_menu():
    clear()
    show_header()

    print("\nMAIN MENU\n")

    print("[1] - PLAY")
    print("[2] - OPTIONS")
    print("[3] - EXIT\n")

    print("Select an option:")

def show_options():
    clear()
    show_header()

    print("\OPTIONS\n")

    print("There are no options currently available.")
    print("\nPress ENTER to return to the main menu...")
    input("")

    start_home()

def start_home():
    show_menu()

    option = 0
    while (True):
        opt = input()
        if opt == "1" or opt == "2" or opt == "3": 
            option = int(opt)
            break
        else: show_menu()

    if (option == 1):
        start_play()
    elif (option == 2):
        show_options()
    elif(option == 3):
        clear()
        bitacora()
        
        time.sleep(3)
        clear()
        exit()

start_home()
