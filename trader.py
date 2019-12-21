import requests, json, os, time
from config import *

BASE_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = '{}/v2/account'.format(BASE_URL)
ORDERS_URL = '{}/v2/orders'.format(BASE_URL)
POSITIONS_URL = '{}/v2/positions'.format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY' : SECRET_KEY}

# clear function for keeping terminal window clean
clear = lambda: os.system('cls')

# GET functions
def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.loads(r.content)
    # returns a dictionary

def check_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)
    # returns a list

def check_positions():
    r = requests.get(POSITIONS_URL, headers=HEADERS)

    return json.loads(r.content)
    # returns a list

def check_positions_by_symbol(symbol):
    data = {
        'symbol': symbol
    }

    POSITIONS_URL_WITH_SYMBOL = POSITIONS_URL + '/{}'.format(symbol)

    r = requests.get(POSITIONS_URL_WITH_SYMBOL, json=data, headers=HEADERS)

    return json.loads(r.content)
    # returns a dictionary

# POST functions
def create_order(symbol, qty, side, trade_type, time_in_force):
    data = {
        'symbol': symbol.upper(),
        'qty': qty,
        'side': side,
        'type': trade_type,
        'time_in_force': time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    # print(r)
    if r.status_code == 403:
        print('ERROR: Not enough buying power.')
    elif r.status_code == 422:
        print('ERROR: Parameters sent not recognized.')
        print(f'Symbol: {symbol}')
        print(f'qty: {qty}')
        print(f'side: {side}')
        print(f'trade_type: {trade_type}')
        print(f'time_in_force: {time_in_force}')
    else:
        return json.loads(r.content)

# PATCH functions
def update_order(order_id, symbol, qty, side, trade_type, time_in_force):
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': trade_type,
        'time_in_force': time_in_force
    }

    ORDERS_URL_WITH_ID = ORDERS_URL + '/{}'.format(order_id)

    r = requests.patch(ORDERS_URL_WITH_ID, json=data, headers=HEADERS)

    return json.loads(r.content)

# DELETE functions
def delete_all_orders():
    r = requests.delete(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)

def delete_order_by_id(order_id):
    data = {
        'order_id': order_id
    }

    ORDERS_URL_WITH_ID = ORDERS_URL + '/{}'.format(order_id)
    
    r = requests.delete(ORDERS_URL_WITH_ID, json=data, headers=HEADERS)

    return json.loads(r.content)

def delete_all_positions():
    r = requests.delete(POSITIONS_URL, headers=HEADERS)

    return json.loads(r.content)

def delete_position_by_symbol(symbol):
    data = {
        'symbol': symbol
    }

    POSITIONS_URL_WITH_SYMBOL = POSITIONS_URL + '/{}'.format(symbol)
    
    r = requests.delete(POSITIONS_URL_WITH_SYMBOL, json=data, headers=HEADERS)
    if r.status_code == 404:
        print('ERROR: No matching position found.')
    else:
        print('Successfully liquidated {} position'.format(symbol))
        return json.loads(r.content)

# APP FLOW
def main_menu():
    print('Here are your options:')
    print('1. Check Account')
    print('2. Create Order')
    print('3. Check Orders')
    print('4. Check Positions')
    print('5. Delete all pending orders')
    print('6. Sell all positions at current market price')
    print('7. Sell position by symbol at current market price')
    print('8. Begin Monitor')
    print('Or type "quit" to exit')

    user_choice = input("What would you like to do today?  ")

    if user_choice == '1':
        print('user chose 1')
        time.sleep(2)
        clear()
        account = get_account()
        print(account)
        time.sleep(1)
        main_menu()
    elif user_choice == '2':
        print('user chose 2')
        time.sleep(2)
        clear()
        symbol = input("What's the symbol?  ")
        qty = input("How many shares?  ")
        side = input("What's the side?  ")
        trade_type = input("What's the trade type?  ")
        time_in_force = input("What's the time in force?  ")
        order = create_order(symbol, int(qty), side, trade_type, time_in_force)
        if order:
            print("Order created successfully")
            time.sleep(1)
            main_menu()
        else:
            print('Something went wrong.')
            time.sleep(1)
            main_menu()
    elif user_choice == '3':
        print('user chose 3')
        time.sleep(2)
        clear()
        checked_orders = check_orders()
        print(checked_orders)
        time.sleep(1)
        main_menu()
    elif user_choice == '4':
        print('user chose 4')
        time.sleep(2)
        clear()
        checked_positions = check_positions()
        print(checked_positions)
        time.sleep(1)
        main_menu()
    elif user_choice == '5':
        print('user chose 5')
        time.sleep(2)
        clear()
        delete_all_orders()
        print('Successfully deleted all pending orders')
        time.sleep(1)
        main_menu()
    elif user_choice == '6':
        print('user chose 6')
        time.sleep(2)
        clear()
        delete_all_positions()
        print('Successfully liquidated all open positions')
        time.sleep(1)
        main_menu()
    elif user_choice == '7':
        print('user chose 7')
        time.sleep(2)
        clear()
        symbol = input("What symbol would you like to sell?  ")
        delete_position_by_symbol(symbol.upper())
        time.sleep(1)
        main_menu()
    elif user_choice == '8':
        print('user chose 8')
        time.sleep(2)
        clear()
        monitor_positions()
    elif user_choice == 'quit':
        clear()
        print('user tried to quit')
        time.sleep(1)
        clear()
    else:
        clear()
        print('================')
        print("Please choose a number 1-8  ")
        print('================')
        time.sleep(4)
        clear()
        main_menu()

def monitor_positions():
    x = 0 # used for getting the correct number of symbols to monitor
    y = 0 # used for getting to 1000 daily trades
    print("Type 'quit' at anytime to quit or 'main menu' to go back to the menu. ")
    num_to_monitor = input('How many positions would you like to monitor?  ')
    if num_to_monitor == 'quit':
        return
    elif num_to_monitor == 'main menu':
        main_menu()
    elif num_to_monitor.isnumeric() == False:
        print("Please pick a number, quit, or go back to main menu.")
        time.sleep(3)
        clear()
        monitor_positions()
    else:
        num_to_monitor = int(num_to_monitor)
        sym_to_monitor = []
        while x < num_to_monitor:
            symbol = input('What symbol would you like to monitor next?  ')
            if num_to_monitor == 'quit':
                return
            elif num_to_monitor == 'main menu':
                main_menu()
            else:
                symbol = symbol.upper()
                sym_to_monitor.append(symbol)
                x+=1

        print(sym_to_monitor)
        while y < 1000:
            for symbol in sym_to_monitor:
                time.sleep(1) # rate limiter 
                check = check_positions_by_symbol(symbol)
                print(check)
                if 'code' in check:
                    print("Position does not exist.")
                else:
                    print("Unrealized profit/loss: " + check["unrealized_pl"])
                    print("Symbol: " + check["symbol"])
                    print("Qty: " + check["qty"])
                    print("Side: " + check["side"])
                    profit_loss = float(check["unrealized_pl"])
                    if profit_loss >= 1 or profit_loss <= -0.5:
                        time.sleep(1) # rate limiter 
                        delete_position_by_symbol(symbol)
                        print("Closed position for {}".format(symbol))
                        y+=1
                        if y <= 1000-len(sym_to_monitor):
                            time.sleep(1) # rate limiter 
                            create_order(symbol, '10', 'buy', 'market', 'gtc')
        return

main_menu()

print('end of script')