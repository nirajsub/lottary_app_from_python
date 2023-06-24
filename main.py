import random

MAX_LINES = 4
MAX_BET = 100
MIN_BET = 1

ROWS = 4
COLS = 3

symbol_count = {
    "A": 3,
    "B": 4,
    "C": 5,
    "D": 6,
    "E": 10,
}
symbol_value = {
    "A": 6,
    "B": 5,
    "C": 4,
    "D": 3,
    "E": 2
}

wild_symbol = "W"
wild_multiplier = 2

def check_winnings(columns, lines, bets, values):
    winnings = 0
    winning_lines = []
    winning_count = 0
    for line in range(lines):
        symbol = columns[0][line]
        for col in columns:
            symbol_to_check = col[line]
            if symbol != symbol_to_check and symbol_to_check != wild_symbol:
                break
        else:
            if symbol == wild_symbol:
                symbol = symbol_to_check
            winnings += values[symbol] * bets[line]
            winning_lines.append(line + 1)
            winning_count += 1
    
    if winning_count == 2:
        winnings *= 2
    elif winning_count == 3:
        winnings *= 6
    elif winning_count == 4:
        winnings *= 8
    
    return winnings, winning_lines

def get_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        if symbol != wild_symbol:
            for _ in range(symbol_count):
                all_symbols.append(symbol)
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_machine_spin(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0")
        else:
            print("Please enter a number")
    return amount

def get_bets(lines):
    bets = []
    for line in range(lines):
        while True:
            bet = input(f"What would you like to bet on line {line + 1}? $")
            if bet.isdigit():
                bet = int(bet)
                if MIN_BET <= bet <= MAX_BET:
                    break
                else:
                    print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
            else:
                print("Please enter a number")
        bets.append(bet)
    return bets

def spin(balance):
    lines = get_number_of_lines()
    bets = get_bets(lines)
    total_bet = sum(bets)

    if total_bet > balance:
        print(f"Not enough balance. Your balance is ${balance}")
        return 0

    print(f"You are betting ${total_bet} on {lines} lines.")

    slots = get_machine_spin(ROWS, COLS, symbol_count)
    print_machine_spin(slots)

    winnings, winning_lines = check_winnings(slots, lines, bets, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet

def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines")
        else:
            print("Please enter a number")
    return lines

def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to continue playing (q to quit): ")
        if answer == "q":
            break
        balance += spin(balance)
    print(f"You left with: {balance}")

main()
