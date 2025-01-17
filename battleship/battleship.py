import random


class Game:
    def __init__(self, players):
        self.players = players

        shipsNumber = input("Number of Ships (2-7) per Player: ")
        while not shipsNumber.isdigit():
            shipsNumber = input("Wrong Format!\n" + "Number of Ships (2-7) per Player: ")

        shipsNumber = int(shipsNumber)

        if shipsNumber > 7:
            shipsNumber = 7
            print("Number of Ships will be 7!\n")
        elif shipsNumber < 2:
            shipsNumber = 2
            print("Number of Ships will be 2!\n")

        letter = ord("a")
        for i in range(shipsNumber):
            self.players[0].ships.append(Ship(random.randint(2, 5), random.choice(["H", "V"]), chr(letter)))
            letter += 1

        for i in range(len(self.players)):
            self.players[i].ships = self.players[0].ships

        for i in range(len(self.players)):
            initializeGame(self.players[i].grid, self.players[i])

        gameOver = False

        while gameOver is False:
            for i in range(len(self.players)):
                self.players[i].fire()
                gameOver = self.players[i].gameOver
                if gameOver:
                    print(self.players[i].name + " Won!")
                    break


def initializeGame(grid, player):
    horShips = list(filter(lambda s: s.orientation == "H", player.ships))
    verShips = list(filter(lambda s: s.orientation == "V", player.ships))

    # Place vertical boats
    for v in range(len(verShips)):
        while True:
            vNum = random.randrange(0, len(grid[0]))
            hNum = random.randint(0, len(grid) - verShips[v].length)

            conflict = False
            for i in range(verShips[v].length):
                if grid[hNum + i][vNum] != "." and grid[hNum + i][vNum] != verShips[v].letter:
                    conflict = True
                    break

            if not conflict:
                for i in range(verShips[v].length):
                    grid[hNum + i][vNum] = verShips[v].letter
                break

    # Place horizontal boats
    for h in range(len(horShips)):
        while True:
            hNum = random.randrange(0, len(grid))
            vNum = random.randint(0, len(grid[0]) - horShips[h].length)

            conflict = False
            for j in range(horShips[h].length):
                if grid[hNum][vNum + j] != "." and grid[hNum][vNum + j] != horShips[h].letter:
                    conflict = True
                    break

            if not conflict:
                for j in range(horShips[h].length):
                    grid[hNum][vNum + j] = horShips[h].letter
                break

    if player.name == "Player1":
        print("Player2's grid:")
    else:
        print("Player1's grid:")

    # Print the grid after placing the ships
    for i, x in enumerate(grid):
        print(player.alphabets[i], end="  ")  # Print the row letter
        for y in x:
            ## cpmment out to print ships
            if y != ".":
                print(".", end=" ")
            ##
            else:
                print(y, end=" ")
        print()

    # Print the column numbers at the bottom
    print("   ", end="")
    for i in range(len(grid)):
        print(i + 1, end=" ")
    print()

    print()


class Ship:
    def __init__(self, length, orient, letter):
        self.length = length
        self.orientation = orient
        self.letter = letter


class Player:

    def __init__(self, grid, name):
        self.grid = grid
        self.ships = []
        self.fired = []
        self.hit = []
        self.alphabets = "ABCDEFGHIJKLMNO"
        self.name = name
        self.shipsDown = 0
        self.gameOver = False

    def fire(self):
        valid = False
        row = 0
        col = 0

        while valid is False:
            placement = input(self.name + ": Enter row (A-J) and column (0-9) such as A3: ").upper()
            while (len(placement) != (1 + len(str(len(self.grid)))) and len(placement) != len(str(len(self.grid)))) or \
                    placement[0] not in self.alphabets or not placement[1].isdigit():
                placement = input(
                    "Wrong Format!\n" + self.name + ": Enter row (A-J) and column (0-9) such as A3: ").upper()
            row = self.alphabets.find((placement[0]))
            col = int(placement[1:]) - 1

            if len(self.grid[0]) > row > -1 or len(self.grid) > col > -1:
                if not (self.grid[row][col] == "X" or self.grid[row][col] == "#"):
                    valid = True
                    hit(self, row, col)
                else:
                    print("You have already fired at this position. Try again.")
            else:
                print("firing out of grid")


def hit(self, row, col):
    if self.grid[row][col] == "." or self.grid[row][col] == "X":
        print("Miss!")
        self.grid[row][col] = "#"

    else:
        print("Hit!")
        shipStatus(self, row, col)

    if self.shipsDown == len(self.ships):
        self.gameOver = True

    # Printing Grid
    if self.name == "Player1":
        print("Player2's grid:")
    else:
        print("Player1's grid:")

    for i, x in enumerate(self.grid):
        print(self.alphabets[i], end="  ")  # Print the row letter
        for y in x:
            ## redundant code, comment out if you want to print the ships after firing
            if y != "." and y != "X" and y != "#" and self.gameOver == False:
                ##
                print(".", end=" ")
            else:
                print(y, end=" ")
        print()

    # Print the column numbers at the bottom
    print("   ", end="")
    for i in range(len(self.grid)):
        print(i + 1, end=" ")
    print()


def shipStatus(self, row, col):
    tempArray = list(filter(lambda s: s.letter == self.grid[row][col], self.ships))
    self.grid[row][col] = "X"
    letterSum = 0
    if tempArray[0].orientation == "H":
        for i in self.grid[row]:
            if i == tempArray[0].letter:
                letterSum += 1
    elif tempArray[0].orientation == "V":
        for i in range(len(self.grid)):
            if self.grid[i][col] == tempArray[0].letter:
                letterSum += 1

    if letterSum == 0:
        print("Ship '" + tempArray[0].letter + "' Down!")
        self.shipsDown += 1


def main():
    print("-----Welcome to Battleships-----")

    size = input("Grid Size (7-15): ")
    while not size.isdigit():
        size = input("Wrong Format!\n" + "Grid Size (7-15): ")

    size = int(size)

    if size > 15:
        size = 15
        print("The grid's size will be 15!\n")
    elif size < 7:
        size = 7
        print("The grid's size will be 7!\n")

    grid1 = [["." for _ in range(size)] for _ in range(size)]
    grid2 = [["." for _ in range(size)] for _ in range(size)]
    newGame = Game([Player(grid1, "Player1"), Player(grid2, "PLayer2")])


if __name__ == '__main__':
    main()
