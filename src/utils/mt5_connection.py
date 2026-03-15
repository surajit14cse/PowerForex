import MetaTrader5 as mt5
import os
from dotenv import load_dotenv

def initialize_mt5():
    """
    Initialize MT5 with multiple fallback strategies.
    """
    load_dotenv()
    
    login = os.getenv("MT5_LOGIN")
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    path = os.getenv("MT5_PATH")
    
    # Strategy 1: Try to connect to an ALREADY OPEN terminal (Fastest & most stable)
    print("Attempting to connect to running MT5 terminal...")
    if mt5.initialize():
        # If terminal is open, try to login if credentials are provided
        if login and password and server:
            login_int = int(login)
            if mt5.login(login=login_int, password=password, server=server):
                return True
        else:
            # Already logged in manually in terminal
            return True

    # Strategy 2: Try to launch terminal using the PATH
    if path:
        print(f"Launching MT5 from path: {path}...")
        if login and password and server:
            login_int = int(login)
            if mt5.initialize(path=path, login=login_int, password=password, server=server):
                return True
        elif mt5.initialize(path=path):
            return True

    return False

def test_connection():
    # Attempt to initialize MT5
    if not initialize_mt5():
        print(f"MT5 initialization failed. Error: {mt5.last_error()}")
        print("Tip: Make sure MT5 terminal is open and logged in, or provide credentials in .env")
        return False
    
    print("MT5 successfully initialized!")
    
    # Get terminal info
    terminal_info = mt5.terminal_info()
    if terminal_info is not None:
        print(f"Terminal Info: {terminal_info._asdict()}")
    
    # Check if we are logged into an account
    account_info = mt5.account_info()
    if account_info is not None:
        print(f"Connected to Account: {account_info.login}")
        print(f"Balance: {account_info.balance} {account_info.currency}")
    else:
        print("Not logged into an MT5 account.")
        
    # Shutdown connection
    mt5.shutdown()
    return True

if __name__ == "__main__":
    test_connection()
