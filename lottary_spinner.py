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
    winning_count = 0
    for line in range(lines):
        symbol = columns[0][line]
        for col in columns:
            symbol_to_check = col[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * betting_amount[line]
            winning_lines.append(line + 1)
            winning_count += 1
    if winning_count == 2:
        winnings *= 2
    elif winning_count == 3:
        winnings *= 3
    elif winning_count == 4:
        winnings *= 4
    elif winning_count == 5:
        winnings *= 5
    return winnings, winning_lines

def deposit():
    while True:
        amount = input("How much would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount < 0:
                print("Amount must be greater than 0")
        else:
            print("Please enter a number")
        return amount

def get_all_lines():
    while True:
        lines = input(f"Enter the number of line you want to place bet on. lines are betwen(1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines")
        else:
            print("Please enter a number")
    return lines

def bet_amount(lines):
    bets = []
    for line in range(lines):
        while True:
            betting_amount = input(f"How much do you like to bet on line: {line + 1}? $")
            if betting_amount.isdigit():
                betting_amount = int(betting_amount)
                if  MIN_BET <= betting_amount <= MAX_BET:
                    break
                else:
                    print(f"Amount must be between ${MIN_BET} & ${MAX_BET}")
            else:
                print("Please enter a number")
        bets.append(betting_amount)
    return bets

def spin(balance):
    lines = get_all_lines()
    betting_amount = bet_amount(lines)
    total_betting_amount = sum(betting_amount)

    if total_betting_amount > balance:
        print(f"You do not have enough balance. Your current balance is ${balance}")
        return 0
    print(f"You are betting ${total_betting_amount} on {lines} lines.")
    slot = get_machine_spin(ROWS, COLS, symbol_count)
    print_machine_spin(slot)

    winning, winning_lines = check_winnings(slot, lines, betting_amount, symbol_value)
    print(f"You won ${winning}.")
    print(f"You won on lines:", *winning_lines)
    return winning - total_betting_amount

def main():
    balance = deposit()
    while True:
        print(f"Your current balance is ${balance}")
        answer = input("Press enter if you want to continue playing. (Hope you will be winning more this this).\n If you wish to quit press q. Thank You. I was hopping you could win this this.")
        
        if answer == 'q':
            break
        balance += spin(balance)
    print(f"You have now ${balance} left.")

main()