import random

MAX_LINES = 5
MAX_BET = 100
MIN_BET = 1

ROWS = 5
COLS = 3

symbol_count = {
    "A": 3,
    "B": 4,
    "C": 6,
    "D": 8,
    "E": 12,
}
symbol_value = {
    "A": 5,
    "B": 4.5,
    "C": 3,
    "D": 2.5,
    "E": 2
}

def get_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
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
            if i != len(columns) -1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

def check_winnings(columns, lines, betting_amount, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        if all(col[line] == symbol for col in columns):
            winnings += values[symbol] * betting_amount[line]
            winning_lines.append(line + 1)
    winning_count = len(winning_lines)
    if winning_count >= 2:
        winnings *= winning_count
    return winnings, winning_lines

def deposit():
    while True:
        amount = input("How much would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0")
        else:
            print("Please enter a number")

def main():
    balance = deposit()
    while True:
        print(f"Your current balance is ${balance}")
        answer = input("Press Enter to continue playing or 'q' to quit: ")
        if answer == 'q':
            break

        lines = 0
        while not 1 <= lines <= MAX_LINES:
            lines = input(f"Enter the number of lines you want to place a bet on (1-{MAX_LINES}): ")
            if lines.isdigit():
                lines = int(lines)

        betting_amount = []
        for line in range(lines):
            while True:
                amount = input(f"How much would you like to bet on line {line + 1}? $")
                if amount.isdigit():
                    amount = int(amount)
                    if MIN_BET <= amount <= MAX_BET:
                        betting_amount.append(amount)
                        break
                    else:
                        print(f"Amount must be between ${MIN_BET} and ${MAX_BET}")
                else:
                    print("Please enter a number")

        total_betting_amount = sum(betting_amount)
        if total_betting_amount > balance:
            print(f"You do not have enough balance. Your current balance is ${balance}")
            continue

        print(f"You are betting ${total_betting_amount} on {lines} line(s).")
        slot = get_machine_spin(ROWS, COLS, symbol_count)
        print_machine_spin(slot)

        winnings, winning_lines = check_winnings(slot, lines, betting_amount, symbol_value)
        print(f"You won ${winnings}.")
        if winning_lines:
            print("You won on line(s):", *winning_lines)
        balance += winnings - total_betting_amount
    print(f"You have ${balance} left.")

main()
