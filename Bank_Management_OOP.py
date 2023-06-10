import datetime


class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class Bank:
    @staticmethod
    def transaction_text(username, transaction_type, amount):
        time = datetime.datetime.now()
        text = {
            "username": username,
            "type": transaction_type,
            "amount": amount,
            "time": time.strftime("%c"),
        }
        return text


class DBBL(Bank):
    customer_list = []
    admin_list = []
    customer_balance_info = {}
    transaction_history = []
    loan_database = {}
    loan_available = True

    def create_account(self):
        name = input("Enter your name:")
        password = int(input("Enter your password:"))
        self.new_user = User(name, password)
        self.customer_list.append(vars(self.new_user))
        self.customer_balance_info[name] = 0
        self.loan_database[name] = 0

    def get_users(self):
        return self.customer_list

    def deposit(self, username):
        amount = int(input("Enter deposit amount:"))
        self.customer_balance_info[username] += amount
        transaction = Bank.transaction_text(username, "deposit", amount)
        self.transaction_history.append(transaction)
        print(
            f"BDT {amount} deposit successful, CB:BDT {self.customer_balance_info[username]}"
        )

    def withdraw(self, username):
        amount = int(input("Enter withdraw amount:"))
        balance = self.customer_balance_info[username]
        if amount <= balance:
            if self.get_total_balance() - self.get_total_loan() > amount:
                self.customer_balance_info[username] -= amount
                transaction = Bank.transaction_text(username, "withdraw", amount)
                self.transaction_history.append(transaction)
                print(
                    f"{amount} has been withdrawan successfully,CB:{self.customer_balance_info[username]}"
                )
            else:
                print("The bank is bankrupted")
        else:
            print("Not enough fund in your bank account")

    def check_balance(self, username):
        print(f"Current balance {self.customer_balance_info[username]}")
        loan = self.loan_database[username]
        if loan > 0:
            print(f"You have loan amount of BDT:{loan}")

    def transaction_history_check(self, username):
        print(f"------Transaction history of {username}-------")
        for item in self.transaction_history:
            if item["username"] == username:
                print(item["type"], " BDT:", item["amount"], " on", item["time"])
        print("------------------------------------------------")

    def transfer_balance(self, from_user):
        to_user = input("Enter username of receiver:")
        amount = int(input("Enter amount:"))
        not_found = True
        if self.customer_balance_info[from_user] >= amount:
            for item in self.customer_list:
                if item["username"] == to_user:
                    print(f"{to_user} is found.")
                    not_found = False
                    choice = int(input("Press 1 to confirm else press 2 to cancel: "))
                    if choice == 1:
                        self.customer_balance_info[from_user] -= amount
                        self.customer_balance_info[to_user] += amount
                        transaction = Bank.transaction_text(
                            from_user, f"transfer fund to {to_user} ", amount
                        )
                        self.transaction_history.append(transaction)

                        transaction2 = Bank.transaction_text(
                            to_user, f"received fund from {from_user} ", amount
                        )
                        self.transaction_history.append(transaction2)
                        print(
                            f"Send money to {to_user} is successfull. Current Balance BDT:{self.customer_balance_info[from_user]}"
                        )
                    elif choice == 2:
                        print("Transaction cancelled by the user")
            if not_found:
                print(f"{to_user} not found")
        else:
            print("Not enought money to send")

    def take_loan(self, username):
        cb = self.customer_balance_info[username]
        if cb > 0 and self.loan_available:
            loan_available = cb * 2
            print("Loan available for you is BDT:", loan_available)
            loan_amount = int(input(f"Enter amount up to BDT {loan_available}:"))
            if loan_amount <= self.get_total_balance():
                self.customer_balance_info[username] += loan_amount
                self.loan_database[username] += loan_amount
                transaction = Bank.transaction_text(username, "Loan Taken", loan_amount)
                self.transaction_history.append(transaction)
                print(
                    f"BDT:{loan_amount} loan has claimed, Current Balance:{self.customer_balance_info[username]} and Loan Amount: {self.loan_database[username]}"
                )
        else:
            print("Loan features off\n")

    def create_admin(self):
        username = input("Enter admin user name:")
        password = int(input("Enter password:"))
        self.new_admin = User(username, password)
        self.admin_list.append(vars(self.new_admin))
        print(f"Admin created successfully with username {username}")

    def get_total_balance(self):
        sum = 0
        for user, balance in self.customer_balance_info.items():
            sum += balance
        return sum

    def get_total_loan(self):
        sum = 0
        for user, loan in self.loan_database.items():
            sum += loan
        return sum

    def loan_on_off(self):
        if self.loan_available == True:
            print("Loan is on")
            choice = int(input("Press 1 to turn off:"))
            if choice == 1:
                self.loan_available = False
        elif self.loan_available == False:
            print("Loan is off")
            choice = int(input("Press 1 to turn on:"))
            if choice == 1:
                self.loan_available = True

    def admin_page(self):
        username = input("Enter admin username:")
        password = int(input("Enter password:"))
        is_admin_logged_in = False
        for item in self.admin_list:
            if item["username"] == username and item["password"] == password:
                is_admin_logged_in = True
        if is_admin_logged_in:
            print(f"WElcome admin dashboard, {username}\n")
            while True:
                print(
                    "1. Check Total Availble Bank Balance\n2. Check Total Loan Amount\n3. Loan Feauture on/off\n4. Exit"
                )
                choice = int(input("Enter your choice:"))
                if choice == 1:
                    total = self.get_total_balance()
                    print(f"Total Availble Balance:{total}\n")
                elif choice == 2:
                    total_loan = self.get_total_loan()
                    print(f"The has given total loan of BDT: {total_loan}")
                elif choice == 3:
                    self.loan_on_off()
                elif choice == 4:
                    break
        else:
            print("Admin username or password mismatched.")


dbbl = DBBL()
while True:
    print(
        "1. Create Account \n2. Login \n3. Admin Create Account \n4. Admin Login\n5. Exit"
    )
    user_input = int(input("Enter your choice:"))
    if user_input == 5:
        break
    elif user_input == 1:
        dbbl.create_account()
    elif user_input == 3:
        dbbl.create_admin()
        pass
    elif user_input == 4:
        dbbl.admin_page()
    elif user_input == 2:
        is_logged_in = False
        username = input("Enter Username:")
        password = int(input("Enter Password:"))
        for user in dbbl.get_users():
            if user["username"] == username and user["password"] == password:
                is_logged_in = True
        if is_logged_in:
            while True:
                print("Hello,", username)
                print(
                    "1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer Balance\n5. Transaction History\n6. Take loan\n7. Exit"
                )
                choice = int(input("Enter your choice:"))
                if choice == 1:
                    dbbl.deposit(username)
                elif choice == 2:
                    dbbl.withdraw(username)
                elif choice == 3:
                    dbbl.check_balance(username)
                elif choice == 4:
                    dbbl.transfer_balance(username)
                elif choice == 5:
                    dbbl.transaction_history_check(username)
                elif choice == 6:
                    dbbl.take_loan(username)
                elif choice == 7:
                    break

        else:
            print("Username or password not mathced")
