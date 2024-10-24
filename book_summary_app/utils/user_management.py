import pandas as pd
import os

USER_DATA_FILE = "user_data.csv"

def register_user(name, email, password, phone):
    if not os.path.exists(USER_DATA_FILE):
        df = pd.DataFrame(columns=["Name", "Email", "Password", "Phone"])
        df.to_csv(USER_DATA_FILE, index=False)

    new_user = pd.DataFrame([[name, email, password, phone]], columns=["Name", "Email", "Password", "Phone"])
    new_user.to_csv(USER_DATA_FILE, mode='a', header=False, index=False)

def user_exists(email, phone):
    if os.path.exists(USER_DATA_FILE):
        df = pd.read_csv(USER_DATA_FILE)
        user = df[(df["Email"] == email) & (df["Phone"] == phone)]
        return not user.empty
    return False

def verify_user(email, password):
    if os.path.exists(USER_DATA_FILE):
        df = pd.read_csv(USER_DATA_FILE)
        user = df[(df["Email"] == email) & (df["Password"] == password)]
        return not user.empty
    return False