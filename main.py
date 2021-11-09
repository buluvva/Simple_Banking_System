import random

#  class for creating cards
class User:
    def __init__(self):
        self.card = '400000'
        self.pin = ''
        for _ in range(9):
            self.card += str(random.randint(0,9))
        # Luhn alghoritm
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(self.card)
        even_digits = digits[-1::-2]
        odd_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            if sum(digits_of(d*2)) >= 10 :
                checksum += sum(digits_of(d*2)) - 10
            else:
                checksum += sum(digits_of(d * 2))
        check_digit = checksum % 10
        if check_digit == 0:
            self.card += str(check_digit)
        else:
            self.card += str(10 - check_digit)
        for _ in range(4):
            self.pin += str(random.randint(0,9))
        self.balance = 0
    # function of saving data in file
    def create(self):
        self.log = dict({'card': int(self.card), 'pin': self.pin, 'balance': 0})
        with open('file.txt', 'a') as file:
            file.writelines(f'{(self.log)}\n')

#  main program
def prog(name):
    while True :
        print("""
1. Create an account
2. Log into account
0. Exit
        """)
        choice = int(input())
        if choice == 1:
            user = User()
            user.create()
            print(''' 
Your card has been created
Your card number:''')
            print(user.card)
            print('Your card PIN:')
            print(user.pin)
        elif choice == 2:
            print('Enter your card number:')
            card = int(input())
            print('Enter your PIN:')
            pin = int(input())
            user_log = dict()
            with open('file.txt', 'r') as file:
                for line in file:
                    if (str(card) in line) and (str(pin) in line):
                        user_log = eval(line)
            if user_log == dict() :
                print('Wrong card number or PIN!')
                continue  #  return to the start menu
            print('You have successfully logged in!')

            while True: #  logged in user menu
                print("""
    1. Balance
    2. Log out
    0. Exit
                            """)
                choice2 = int(input())
                if choice2 == 1:
                    print(f"Balance: {user_log['balance']}")
                    continue
                elif choice2 == 2:
                    print('You have successfully logged out!')
                    break
                elif choice2 == 0:
                    print('Bye!')
                    exit()
        elif choice == 0:
            print('Bye!')
            exit()

if __name__  == '__main__':
    prog('go on')