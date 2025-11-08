from collections import deque
import numpy as np
import pandas as pd
import ast

with open("users.txt", "r") as f:
    users = ast.literal_eval(f.read())

with open("clients.txt", "r") as f:
    client_data = ast.literal_eval(f.read())

with open("queue.txt", "r") as f:
    order_queue = deque(ast.literal_eval(f.read()))

with open("history.txt", "r") as f:
    history_stack = ast.literal_eval(f.read())

def save_queue():
    with open("queue.txt", "w") as f:
        f.write(str(list(order_queue)))

def save_history():
    with open("history.txt", "w") as f:
        f.write(str(history_stack))

def login():
    print("\n--- Welcome to Financial Analyzer ---")
    username = input("Enter username: ").lower()
    password = input("Enter password: ")
    if username in users and users[username]["password"] == password:
        print(f"\nLogin successful! Welcome, {username.title()}.\n")
        if users[username]["role"] == "admin":
            admin_dashboard(username)
        else:
            client_dashboard(username)
    else:
        print("Invalid credentials. Try again.\n")
        login()

def admin_dashboard(username):
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. View all clients")
        print("2. View transaction queue")
        print("3. Process next order")
        print("4. View history")
        print("5. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_clients()
        elif choice == "2":
            view_queue()
        elif choice == "3":
            process_next_order()
        elif choice == "4":
            view_history()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

def client_dashboard(username):
    while True:
        print(f"\n--- Client Dashboard ({username.title()}) ---")
        print("1. View portfolio")
        print("2. Analyze profit/loss")
        print("3. Place order")
        print("4. View history")
        print("5. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_portfolio(username)
        elif choice == "2":
            analyze_portfolio(username)
        elif choice == "3":
            place_order(username)
        elif choice == "4":
            view_history()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

def view_all_clients():
    data = []
    for c, stocks in client_data.items():
        for s, i in stocks.items():
            data.append([c.title(), s, i["quantity"], i["price"], i["quantity"] * i["price"]])
    print(pd.DataFrame(data, columns=["Client","Stock","Qty","Price","Total"]))

def view_queue():
    print("\nQueue:")
    for o in order_queue: print(o) if order_queue else print("Empty")

def process_next_order():
    if not order_queue:
        print("No orders")
        return
    order = order_queue.popleft()
    print("Processed:", order)
    history_stack.append("Processed: " + order)
    save_queue()
    save_history()

def view_portfolio(u):
    data = []
    for s, i in client_data[u].items():
        data.append([s, i["quantity"], i["price"], i["quantity"] * i["price"]])
    print(pd.DataFrame(data, columns=["Stock","Qty","Price","Total"]))

def analyze_portfolio(u):
    prices = np.array([i["price"] for i in client_data[u].values()])
    new = prices * np.random.uniform(0.9,1.2,len(prices))
    diff = new - prices
    for s,d in zip(client_data[u], diff):
        print(s, ":", round(d,2))
    history_stack.append("Analyzed portfolio " + u)
    save_history()

def place_order(u):
    s = input("Stock: ").upper()
    a = input("Buy/Sell: ")
    q = int(input("Qty: "))
    p = float(input("Price: "))
    o = f"{u} {a} {q} {s} @ {p}"
    order_queue.append(o)
    history_stack.append("Ordered: " + o)
    save_queue()
    save_history()

def view_history():
    print("\nHistory:")
    for h in reversed(history_stack): print(h)

login()
