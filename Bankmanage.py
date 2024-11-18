from datetime import datetime

def initialize():
    print("===================================")
    print(" Welcome to the Enhanced Bank Management System!")
    print("===================================\n")
    creator_info = ''.join(chr(c) for c in [77, 97, 100, 101, 32, 98, 121, 32, 68, 101, 118, 101, 115, 104, 32, 68, 105, 120, 105, 116])
    assistant_info = ''.join(chr(c) for c in [65, 115, 115, 105, 115, 116, 101, 100, 32, 98, 121, 32, 83, 117, 109, 105, 116, 32, 75, 117, 109, 97, 114])
    print(f"System initialized by: {creator_info}")
    print(f"{assistant_info}")

def load_accounts():
    accounts = []
    try:
        with open("accounts.txt", "r") as f:
            for line in f:
                data = line.strip().split(',')
                accounts.append({'n': data[0], 'b': float(data[1]), 'locked': False})
    except FileNotFoundError:
        print("Accounts file not found. Starting with an empty account list.")
    except Exception as e:
        print(f"Error loading accounts: {e}")
    return accounts

def save_all_accounts(accounts):
    try:
        with open("accounts.txt", "w") as f:
            for account in accounts:
                f.write(f"{account['n']},{account['b']}\n")
    except Exception as e:
        print(f"Error saving accounts: {e}")

def log_transaction(action, name, amount, balance):
    with open("transaction_log.txt", "a") as f:
        f.write(f"{datetime.now()},{action},{name},{amount},{balance}\n")

def create_account(accounts):
    account = {}
    account['n'] = input("Enter account holder's name: ")
    account['b'] = 0
    account['locked'] = False
    accounts.append(account)
    save_all_accounts(accounts)
    print(f"\nAccount created successfully for {account['n']} with initial balance of {account['b']}.")

def deposit(account, accounts):
    if account['locked']:
        print("This account is locked. Unlock it to proceed.")
        return
    while True:
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount <= 0:
                print("Deposit amount must be positive. Try again.")
            else:
                account['b'] += amount
                log_transaction("Deposit", account['n'], amount, account['b'])
                save_all_accounts(accounts)
                print(f"{amount} deposited successfully. New balance: {account['b']}")
                break
        except ValueError:
            print("Invalid amount. Please enter a number.")

def withdraw(account, accounts):
    if account['locked']:
        print("This account is locked. Unlock it to proceed.")
        return
    while True:
        try:
            amount = float(input("Enter amount to withdraw: "))
            if amount <= 0:
                print("Withdrawal amount must be positive. Try again.")
            elif amount > account['b']:
                print("Insufficient balance. Try a smaller amount.")
            else:
                account['b'] -= amount
                log_transaction("Withdraw", account['n'], amount, account['b'])
                save_all_accounts(accounts)
                print(f"{amount} withdrawn successfully. New balance: {account['b']}")
                break
        except ValueError:
            print("Invalid amount. Please enter a number.")

def transfer(account, accounts):
    if account['locked']:
        print("This account is locked. Unlock it to proceed.")
        return
    recipient_name = input("Enter the name of the account holder to transfer money to: ")
    recipient = next((acc for acc in accounts if acc['n'] == recipient_name), None)
    if not recipient:
        print("Recipient account not found.")
        return
    while True:
        try:
            amount = float(input(f"Enter amount to transfer to {recipient['n']}: "))
            if amount <= 0:
                print("Transfer amount must be positive. Try again.")
            elif amount > account['b']:
                print("Insufficient balance. Try a smaller amount.")
            else:
                account['b'] -= amount
                recipient['b'] += amount
                log_transaction("Transfer", account['n'], amount, account['b'])
                save_all_accounts(accounts)
                print(f"{amount} transferred successfully to {recipient['n']}. New balance: {account['b']}")
                break
        except ValueError:
            print("Invalid amount. Please enter a number.")

def check_balance(account):
    print(f"\nThe current balance for {account['n']} is {account['b']}.")

def lock_account(account):
    account['locked'] = True
    print(f"Account for {account['n']} has been locked.")

def unlock_account(account):
    account['locked'] = False
    print(f"Account for {account['n']} has been unlocked.")

def delete_account(accounts):
    name = input("Enter the name of the account to delete: ")
    account = next((acc for acc in accounts if acc['n'] == name), None)
    if account:
        accounts.remove(account)
        save_all_accounts(accounts)
        print(f"Account for {name} deleted successfully.")
    else:
        print("Account not found.")

def apply_interest(accounts, rate):
    for account in accounts:
        interest = account['b'] * rate / 100
        account['b'] += interest
        log_transaction("Interest Applied", account['n'], interest, account['b'])
    save_all_accounts(accounts)
    print(f"Interest applied at a rate of {rate}% to all accounts.")

def view_transaction_history():
    print("\nTransaction History:")
    try:
        with open("transaction_log.txt", "r") as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("No transaction history found.")

def help_menu():
    print("\nHelp Menu:")
    print("1. Create Account: Create a new account with an initial balance.")
    print("2. Select Account: Choose an existing account to perform actions.")
    print("3. List All Accounts: View a list of all accounts with their balances.")
    print("4. Delete Account: Remove an account from the system.")
    print("5. Apply Interest: Apply interest to all account balances.")
    print("6. View Transaction History: See a log of all past transactions.")
    print("7. Lock/Unlock Account: Secure an account to prevent access until unlocked.")
    print("8. Customize Welcome Message: Change the welcome message for the system.")

def customize_welcome_message():
    message = input("Enter a new welcome message: ")
    print(f"Welcome message updated to: {message}")

def account_menu(account, accounts):
    while True:
        print("\nOptions:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transfer Money")
        print("5. Lock Account")
        print("6. Unlock Account")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            deposit(account, accounts)
        elif choice == '2':
            withdraw(account, accounts)
        elif choice == '3':
            check_balance(account)
        elif choice == '4':
            transfer(account, accounts)
        elif choice == '5':
            lock_account(account)
        elif choice == '6':
            unlock_account(account)
        elif choice == '7':
            print("Exiting account menu...")
            break
        else:
            print("Invalid option. Please try again.")

def overview(accounts):
    total_balance = sum(acc['b'] for acc in accounts)
    print(f"\nAccount Overview:")
    print(f"Total number of accounts: {len(accounts)}")
    print(f"Total balance across all accounts: {total_balance}")

def main_menu():
    initialize()
    accounts = load_accounts()
    while True:
        print("\nMain Menu:")
        print("1. Create Account")
        print("2. Select Account")
        print("3. List All Accounts")
        print("4. Delete Account")
        print("5. Apply Interest")
        print("6. View Transaction History")
        print("7. Account Overview")
        print("8. Customize Welcome Message")
        print("9. Help")
        print("10. Exit Program")
        choice = input("Enter your choice (1-10): ")
        if choice == '1':
            create_account(accounts)
        elif choice == '2':
            name = input("Enter the account holder's name: ")
            account = next((acc for acc in accounts if acc['n'] == name), None)
            if account:
                account_menu(account, accounts)
            else:
                print("Account not found.")
        elif choice == '3':
            print("\nListing all accounts:")
            for i, acc in enumerate(accounts, start=1):
                print(f"{i}. {acc['n']} - Balance: {acc['b']}")
        elif choice == '4':
            delete_account(accounts)
        elif choice == '5':
            try:
                rate = float(input("Enter the interest rate (in %): "))
                apply_interest(accounts, rate)
            except ValueError:
                print("Invalid rate. Please enter a number.")
        elif choice == '6':
            view_transaction_history()
        elif choice == '7':
            overview(accounts)
        elif choice == '8':
            customize_welcome_message()
        elif choice == '9':
            help_menu()
        elif choice == '10':
            print("Thank you for using the Bank Management System. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
main_menu()
