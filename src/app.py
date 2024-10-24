import streamlit as st
import pandas as pd
import os

# Define the file to store user data
USER_DATA_FILE = "user_data.csv"

# Function to register user
def register_user(name, email, password, phone):
    # Check if the file exists
    if not os.path.exists(USER_DATA_FILE):
        # Create a new file if it doesn't exist
        df = pd.DataFrame(columns=["Name", "Email", "Password", "Phone"])
        df.to_csv(USER_DATA_FILE, index=False)

    # Append the new user to the CSV file
    new_user = pd.DataFrame([[name, email, password, phone]], columns=["Name", "Email", "Password", "Phone"])
    new_user.to_csv(USER_DATA_FILE, mode='a', header=False, index=False)

# Function to check if the user already exists
def user_exists(email, phone):
    if os.path.exists(USER_DATA_FILE):
        df = pd.read_csv(USER_DATA_FILE)
        # Check if any record matches the provided email and phone
        user = df[(df["Email"] == email) & (df["Phone"] == phone)]
        return not user.empty  # Returns True if user exists
    return False

# Title of the app
st.title("Book Summary App")

# Navigation options
option = st.selectbox("Choose", ["Register", "Login"])
st.write("If you are an existing user, please choose login")

if option == "Register":
    # Registration Form
    st.header("Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    phone = st.text_input("Phone Number")

    # Validation for registration
    if st.button("Register"):
        if not name or not email or not password or not phone:
            st.warning("All fields are required for registration.")
        elif user_exists(email, phone):
            st.warning("User already exists with the same email and phone number.")
        else:
            register_user(name, email, password, phone)
            st.success(f"Registration successful for {name}!")

elif option == "Login":
    # Login Form
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    # Validation for login
    if st.button("Login"):
        if not email or not password:
            st.warning("Email and password are required.")
        else:
            # Function to verify user credentials
            def verify_user(email, password):
                if os.path.exists(USER_DATA_FILE):
                    df = pd.read_csv(USER_DATA_FILE)
                    # Check if the provided email and password match
                    user = df[(df["Email"] == email) & (df["Password"] == password)]
                    return not user.empty  # Returns True if user credentials are valid
                return False

            if verify_user(email, password):
                st.success(f"Login successful for {email}!")
            else:
                st.error("Invalid credentials or user does not exist!")

# Footer with redirect link
st.markdown("###")
