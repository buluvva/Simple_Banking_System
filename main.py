import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card(
                id INTEGER,
                number TEXT UNIQUE,
                pin TEXT UNIQUE,
                balance INTEGER DEFAULT 0
);
""")
conn.commit()

#  func of validating card before transfer

def luhn_check(card):
    def digits_(n):
        return [int(d) for d in str(n)]
    last_digit_arr = digits_(card)
    last_digit = last_digit_arr[15]
    card = str(int(card) // 10)
    digits = digits_(card)
    even_digits = digits[-1::-2]
    odd_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        if sum(digits_(d * 2)) >= 10:
            checksum += sum(digits_(d * 2)) - 10
        else:
            checksum += sum(digits_(d * 2))
    return checksum % 10 + last_digit == 10

#  class for creating cards

class User:
    def __init__(self):
        self.card = '400000'
        self.pin = ''
        for _ in range(9):
            self.card += str(random.randint(0, 9))

        # Luhn alghoritm

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(self.card)
        even_digits = digits[-1::-2]
        odd_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            if sum(digits_of(d * 2)) >= 10:
                checksum += sum(digits_of(d * 2)) - 10
            else:
                checksum += sum(digits_of(d * 2))
        check_digit = checksum % 10
        if check_digit == 0:
            self.card += str(check_digit)
        else:
            self.card += str(10 - check_digit)
        for _ in range(4):
            self.pin += str(random.randint(0, 9))
        self.balance = 0

    # function of saving data in SQL table

    def create(self):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        self.log = dict({'card': int(self.card), 'pin': self.pin, 'balance': 0})
        cur.execute(f"INSERT INTO card(number , pin) VALUES ({self.log['card']}, {self.log['pin']})")
        cur.execute("SELECT * FROM card;")
        conn.commit()


#  return balance function
def balance_(card):
    balance = 0
    sql = f"SELECT * FROM card WHERE number={card}"
    cur.execute(sql)
    records = cur.fetchall()
    for row in records:
        balance = row[3]
    return balance


def prog(name):  # Main program
    while True:
        print("1. Create an account\n2. Log into account\n0. Exit")
        choice = int(input())
        if choice == 1:  # Create acc
            user = User()
            user.create()
            print(' Your card has been created\nYour card number:')
            print(user.card)
            print('Your card PIN:')
            print(user.pin)
        elif choice == 2:  # Log in
            pin_check = '0'
            balance = '0'
            print('Enter your card number:')
            card = int(input())

            sql = "SELECT * FROM card WHERE number=?"
            cur.execute(sql, [f"{card}"])
            records = cur.fetchall()
            for row in records:
                pin_check = row[2]
            print('Enter your PIN:')
            pin = input()
            if int(pin) != int(pin_check):
                print('Wrong card number or PIN!')
                continue  # return to the start menu
            print('You have successfully logged in!')

            while True:  # logged in user menu
                print("1. Balance\n2. Add income3\n. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                choice2 = int(input())
                if choice2 == 1:  # balance
                    print(balance_(card))
                    continue
                elif choice2 == 2:  # Add income
                    balance = balance_(card)
                    income = balance + int(input('Add income: '))
                    cur.execute(f"UPDATE card SET balance = {income} WHERE number = {card}")
                    conn.commit()
                    print(f'Income was added!')
                elif choice2 == 3:  # Do transfer
                    balance = balance_(card)
                    trans_card = input('Enter card number:\n')
                    cur.execute(f"SELECT * FROM card WHERE number={trans_card}")
                    if luhn_check(trans_card) == False:  # if card doesn't pass Luhn algorithm
                        print('Probably you made a mistake in the card number. Please try again!')
                        continue
                    elif cur.fetchone() == None:  # if card doesn't exist
                        print('Such a card does not exist.')
                        continue
                    elif int(trans_card) == int(card):
                        print("You can't transfer money to the same account!")
                        continue

                    else:
                        pass
                    trans_value = int(input('Enter how much money you want to transfer:\n'))
                    if balance < trans_value:
                        print('Not enough money!')
                        continue
                    else:  # Transfer body
                        do_trans = balance - trans_value
                        cur.execute(f"UPDATE card SET balance = {do_trans} WHERE number = {card}")
                        trans_balance = balance_(trans_card) + trans_value
                        cur.execute(f"UPDATE card SET balance = {trans_balance} WHERE number = {trans_card}")
                        conn.commit()
                        print('Success!')
                elif choice2 == 4:  # Close account
                    cur.execute(f'DELETE FROM card where number = {card}')
                    print('The account has been closed!')
                    break
                elif choice2 == 5:  # Log out
                    print('You have successfully logged out!')
                    break
                elif choice2 == 0:  # Exit program
                    print('Bye!')
                    exit()
        elif choice == 0:  # Exit program
            print('Bye!')
            exit()


if __name__ == '__main__':
    prog("go")
