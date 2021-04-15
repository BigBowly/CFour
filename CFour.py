
import os
import random

# class to hold the gameboard values
class GameBoard:
    def __init__(self, players = 2):

        # [rows,columns]
        self.rows = 0
        self.columns = 0
        self.gameboard_size = []

        # variables related to functions that check for connections
        self.connected_slots_orig = []
        self.connected_slots = {"vert":[], "diag1":[], "horiz":[], "diag2":[]}
        self.slots = []

        self.total_players = players
        self.current_player = 1
        self.player_chip = ["  ", "OO", "XX", "##", "@@"]

        self.win = False
        self.error = False
        self.turn_count = 0


# class for each individual slot
class Slot:

    # Universal variable order - vert,diag1,horiz,diag2 - [up vector, down vector] - [row, column]
    # Up-vertical technically doesn't need to be checked since there should never be an above filled slot.    

    surrounding_slots = {"vert":[[-1,0],[1,0]], "diag1":[[-1,1],[1,-1]], "horiz":[[0,1],[0,-1]], "diag2":[[1,1],[-1,-1]]}

    def __init__(self, id):

        self.id = id
        self.owner = "  "

    def __repr__(self):
        return self.id


# clear screen code checking for operating system
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# Function that creates slot variables
def create_slots(rows = 6, columns = 7):
    temp_slot = ""
    for i in range(1, rows+1):
        for j in range(1, columns+1):
            # create slot
            slot_string = "r" + str(i) + "c" + str(j)
            globals()[slot_string] = Slot(slot_string)
            globals()[slot_string].owner = "  "
            gameboard_ctrl.slots.append(globals()[slot_string])

    # gameboard can only be drawn after slot variables have been defined
    draw_gameboard(rows, columns)


# Function that creates gameboard - uses as many loops as possible to cut down on typing and to allow for different board sizes
# the screen is cleared and the game table is redrawn every time a move is made
def draw_gameboard(rows, columns):

    gameboard_ctrl.gameboard_size += [rows, columns]

    empty3 = "   "
    empty6 = "      "
    bar = " | "
    count = 0
    floor = (empty6 + empty3 + "=" * ((columns * 2) + (columns * len(bar))) + "=")
    column_row = (empty6 + empty3 + "  ")

    for i in range(1, rows+1):
        row_string = "row" + str(i)
        if i < 10:
            globals()[row_string] = ("    R" + str(i) + "  " + bar)
        else:
            globals()[row_string] = ("   R" + str(i) + "  " + bar)

        for j in range(1, columns+1):
            globals()[row_string] += gameboard_ctrl.slots[count].owner + bar
            count += 1

    for j in range(1, columns+1):
        col_string = "C" + str(j)
        column_row += (col_string + empty3)

    # putting together dynamically created strings into game table
    if (gameboard_ctrl.win == False):
        print("\n(" + gameboard_ctrl.player_chip[gameboard_ctrl.current_player] + ") Player " + str(gameboard_ctrl.current_player) + "'s turn:\n")
    print("")
    print(column_row)
    print("")
    for i in range(1, rows+1):
        row_string = "row" + str(i)
        print(floor)
        print(globals()[row_string])
    print(floor + "\n")

    if (gameboard_ctrl.win == False):

        print("Enter \'q\' at any time to quit.")

        player_input()



# function to check for open slot after player selects column for chip drop
def drop_chip(column):
    turn_over = False
    empty_slot = False
    # col_lowercase = column.lower()
    row_range = gameboard_ctrl.gameboard_size[0]
    col_range = gameboard_ctrl.gameboard_size[1]
    slot_count = row_range

    # check rows until an empty slot is found
    while empty_slot == False:
        row_string = "r" + str(slot_count) + "c" + str(column)
        row_temp = globals()[row_string]
        if (row_temp.owner == "  "):
            row_temp.owner = gameboard_ctrl.player_chip[gameboard_ctrl.current_player]
            gameboard_ctrl.connected_slots_orig.append(row_temp)
            empty_slot = True
        else:
            slot_count -= 1
        if (slot_count < 1):
            gameboard_ctrl.error = True

            clear_screen()

            draw_gameboard(gameboard_ctrl.gameboard_size[0], gameboard_ctrl.gameboard_size[1])

    # tallies turn count in order to know when the board is full without a winner
    gameboard_ctrl.turn_count += 1

    check_slots(gameboard_ctrl.connected_slots_orig[0])



# checks surrounding slots in vertical, two diagonals, and horizontal directions for vector connections
def check_slots(orig_slot):

    owner = gameboard_ctrl.player_chip[gameboard_ctrl.current_player]

    # variables for looping through the up and down vectors in Slot.surrounding_slots{}
    test_row = int(orig_slot.id[1])
    test_col = int(orig_slot.id[3])
    temp_up_slot = ""
    temp_down_slot = ""
    combined_slots = []

    # becomes false when there's an opposing slot, empty slot, or out of bounds
    up_filled = True
    down_filled = True
    # orig_up_slot = orig_slot
    # orig_down_slot = orig_slot

    # cycles through vertical, diagonal1, horizontal, diagonal2
    for direction_key in Slot.surrounding_slots:

        # checks the upward/positive direction
        while up_filled == True:
            row_num = test_row + Slot.surrounding_slots[direction_key][0][0]
            col_num = test_col + Slot.surrounding_slots[direction_key][0][1]
            temp_up_slot = "r" + str(row_num) + "c" + str(col_num)

            # checks for out of bounds
            if (row_num >= 1) and (row_num <= gameboard_ctrl.gameboard_size[0]) and (col_num >= 1) and (col_num <= gameboard_ctrl.gameboard_size[1]):

                if globals()[temp_up_slot].owner == owner:
                    combined_slots.append(globals()[temp_up_slot])
                    test_row = int(temp_up_slot[1])
                    test_col = int(temp_up_slot[3])
                    #orig_up_slot = globals()[temp_up_slot]
                else:
                    up_filled = False
                    # test_row = int(orig_slot.id[1])
                    # test_col = int(orig_slot.id[3])

            else:
                up_filled = False          

        #resets the test variables back to the original slot so it doesn't contaminate later calculations
        test_row = int(orig_slot.id[1])
        test_col = int(orig_slot.id[3])

        # bug fix print - shows what the up vector calculates
        # print(str(combined_slots))

        if combined_slots != []:
            gameboard_ctrl.connected_slots[direction_key] += (combined_slots)
        combined_slots = []

        # checks the downward/negative direction
        while down_filled == True:
            row_num = int(test_row) + Slot.surrounding_slots[direction_key][1][0]
            col_num = int(test_col) + Slot.surrounding_slots[direction_key][1][1]
            temp_down_slot = "r" + str(row_num) + "c" + str(col_num)

            if (row_num >= 1) and (row_num <= gameboard_ctrl.gameboard_size[0]) and (col_num >= 1) and (col_num <= gameboard_ctrl.gameboard_size[1]):

                if globals()[temp_down_slot].owner == owner:
                    combined_slots.append(globals()[temp_down_slot])
                    test_row = int(temp_down_slot[1])
                    test_col = int(temp_down_slot[3])
                    #orig_down_slot = globals()[temp_down_slot]
                else:
                    down_filled = False
                    # test_row = int(orig_slot.id[1])
                    # test_col = int(orig_slot.id[3])

            else:
                down_filled = False

        test_row = int(orig_slot.id[1])
        test_col = int(orig_slot.id[3])
        
        # bug fix print - shows what the down vector calculates
        # print(str(combined_slots))

        # adds the connected slot variables and the original position into one dictionary value
        if combined_slots != []:
            gameboard_ctrl.connected_slots[direction_key] += combined_slots
        gameboard_ctrl.connected_slots[direction_key].append(orig_slot)

        #  for slots in gameboard_ctrl.connected_slots[direction_key]:
        #      if slots != orig_slot or slots == []:
        #          gameboard_ctrl.connected_slots[direction_key].append(orig_slot)
        
        # restores default values for the next turn
        combined_slots = []
        up_filled = True
        down_filled = True

        # bug fix print - shows connections for every vector 
        # print(direction_key + "  " + str(gameboard_ctrl.connected_slots[direction_key]))


    turn_end()



def turn_end():

    player_input = ""
    direction_win_count = 0
    direction_win_size = 0

    # checks gameboard connection lists to determine if there are 4 or more connections
    for direction_key in gameboard_ctrl.connected_slots:
        if len(gameboard_ctrl.connected_slots[direction_key]) >= 4:
            direction_win_count += 1
            if len(gameboard_ctrl.connected_slots[direction_key]) > direction_win_size:
                direction_win_size = len(gameboard_ctrl.connected_slots[direction_key])

            for slot in gameboard_ctrl.connected_slots[direction_key]:
                slot.owner = "!!"
            gameboard_ctrl.win = True

    # winning text
    if gameboard_ctrl.win == True:

        clear_screen()

        print("\n\nCongratulations Player " + str(gameboard_ctrl.current_player) + "!!")
        print("You won in " + str(direction_win_count) + " direction(s).")
        print("Your largest connect four filled " + str(direction_win_size) + " slots.")
        
        draw_gameboard(gameboard_ctrl.gameboard_size[0], gameboard_ctrl.gameboard_size[1])

        # do you want to play again
        while player_input.lower() != "y" and player_input.lower() != "n" and player_input.lower() != "yes" and player_input.lower() != "no":

            print("\n\nWould you like to play again?")
            player_input = input("(y)es or (n)o:")

            clear_screen()
        
        if player_input.lower() == "no" or player_input.lower() == "n":
            print("\n\nThanks for playing!")
            return

        player_input = ""

        # do you want to keep the same settings
        while player_input.lower() != "y" and player_input.lower() != "n" and player_input.lower() != "yes" and player_input.lower() != "no":

            print("\n\nWould you like to keep the same settings?")
            player_input = input("(y)es or (n)o:")

        if player_input == "yes" or player_input == "y":

            clear_screen()
            restart()
            return

        else:

            restore_defaults()
            start_game()
            return


    # game continues and connected slots defaults are restored
    if gameboard_ctrl.turn_count >= (gameboard_ctrl.gameboard_size[0] * gameboard_ctrl.gameboard_size[1]):

        player_input = ""
        while player_input.lower() != "y" and player_input.lower() != "n" and player_input.lower() != "yes" and player_input.lower() != "no":
      
            clear_screen()

            print("\n\n")
            print("Would you like to clear the board and resume playing? (y)es or (n)o")
            player_input = input(":")

        if player_input.lower() == "y" or player_input.lower() == "yes":

            restart()
            return

        else:
            
            print("\n\nThanks for playing!")
            return


    clear_screen()

    # restores some of the defaults when clearing board
    gameboard_ctrl.connected_slots_orig = []
    gameboard_ctrl.connected_slots = {"vert":[], "diag1":[], "horiz":[], "diag2":[]}
    if (gameboard_ctrl.current_player % gameboard_ctrl.total_players) == 0:
        gameboard_ctrl.current_player = 1
    else:
        gameboard_ctrl.current_player += 1

    draw_gameboard(gameboard_ctrl.gameboard_size[0], gameboard_ctrl.gameboard_size[1]) 


# Player input text will change if there is an error
def player_input():

    player_input = 0
    try_again = "\nTry again. Player " + str(gameboard_ctrl.current_player) + ", pick a column between 1 and " + str(gameboard_ctrl.gameboard_size[1]) + " (i.e. 1, 2, 3 . . .)."
    turn_string = "\nPlayer " + str(gameboard_ctrl.current_player) + " - which column would you like to drop your chip (1 - " + str(gameboard_ctrl.gameboard_size[1]) + ")?"
        
    if gameboard_ctrl.error == True:
        player_input = input(try_again)
        gameboard_ctrl.error = False
    else:
        player_input = input(turn_string)

    if player_input.lower() == "q":
        print("\n\nThanks for playing!")
        return

    try:
        player_input = int(player_input)
    except:
        player_input = 0

    # test column syntax
    if player_input < 1 or player_input > gameboard_ctrl.gameboard_size[1]:
        gameboard_ctrl.error = True

        clear_screen()

        draw_gameboard(gameboard_ctrl.gameboard_size[0], gameboard_ctrl.gameboard_size[1])

    drop_chip(player_input)


def restore_defaults():

    gameboard_ctrl
    gameboard_ctrl.gameboard_size = []
    gameboard_ctrl.connected_slots_orig = []
    gameboard_ctrl.connected_slots = {"vert":[], "diag1":[], "horiz":[], "diag2":[]}
    gameboard_ctrl.slots = []
    gameboard_ctrl.win = False
    gameboard_ctrl.turn_count = 0
    gameboard_ctrl.current_player = random.randint(1,gameboard_ctrl.total_players)



# if the board gets full, check to see if players want to clear the board and continue or quit
def restart():

    restore_defaults()

    create_slots(gameboard_ctrl.rows, gameboard_ctrl.columns)



def yes_no(answer):
    if answer.lower() == "y" or answer.lower() == "yes" or answer.lower() == "n" or answer.lower() == "no":
        return True



# game opening - player inputs for 
def start_game():

    player_input = 0
    min_row = 0
    max_row = 9
    min_col = 0
    max_col = 9
    game_settings = []

    connect_four = \
    """
    
                            WELCOME TO
    
    ==============================================================
    |                                                            |
    |   XXOO    OOXX   OO   XX  XX   OO  OOXXOO   OOXX   OOXXOO  |
    |  OO  OO  OO  XX  OOO  XX  OOO  OO  OO      OO  XX    OO    |
    |  XX      OO  XX  OO O OO  XX O XX  OOXXO   XX        XX    |
    |  OO  XX  OO  XX  XX  OOO  XX  OOX  XX      OO  OO    XX    |
    |   OOOO    OOOO   OO   OO  XX   OO  OOOOXX   XXOO     XX    |
    |                                                            | 
    |               OOXXOO   OOOO   OO  OO  OOXXO                |
    |               OO      XX  XX  XX  OO  XX  XX               |
    |               XXOOO   OO  XX  XX  OO  OOOOX                |
    |               XX      OO  OO  XX  XX  XX  X                |
    |               XX       OOOO    OOXX   OO   O               |
    |                                                            | 
    ==============================================================

    """

    while player_input < 2 or player_input > 4:

        clear_screen()

        print(connect_four)
        print("\n\nHow many players will be playing?")
        
        try:
            player_input = int(input("Enter number between 2 and 4:"))
        except:
            player_input = 0

    if player_input == 2:
        min_row = 4
        min_col = 4
    elif player_input == 3:
        min_row = 6
        min_col = 6
    else:
        min_row = 7
        min_col = 7

    game_settings.append(player_input)
    player_input = 0

    while player_input < min_row or player_input > max_row:

        clear_screen()

        print(connect_four)
        print("\n\nHow many rows will your gameboard have?")
        try:
            player_input = int(input("Enter number between " + str(min_row) + " and " + str(max_row) + ":"))
        except:
            player_input = 0

    game_settings.append(player_input)
    player_input = 0

    while player_input < min_col or player_input > max_col:

        clear_screen()

        print(connect_four)
        print("\n\nHow many columns will your gameboard have?")
        try:
            player_input = int(input("Enter number between " + str(min_col) + " and " + str(max_col) + ":"))
        except:
            player_input = 0

    game_settings.append(player_input)

    gameboard_ctrl.total_players = game_settings[0]
    gameboard_ctrl.rows = game_settings[1]
    gameboard_ctrl.columns = game_settings[2]
    gameboard_ctrl.current_player = random.randint(1,gameboard_ctrl.total_players)

    clear_screen()
    create_slots(gameboard_ctrl.rows, gameboard_ctrl.columns)

    
    
    
        



# start program - begin with the dynamic creation of slot variables
# gameboard_ctrl = GameBoard(2)

# clear_screen()

# create_slots(6, 7)

gameboard_ctrl = GameBoard()
start_game()


