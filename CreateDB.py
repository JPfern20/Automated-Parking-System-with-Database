from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import pyodbc as odbc
from Server_Input_Window import get_server_name

db_name = "Community_Parking"
db_server = get_server_name()  # Get the server name from the input window

# Function to create the database if it doesn't exist
def create_database():
    try:
        # Connect to the database server
        conn = odbc.connect(f'Driver={{SQL Server}};'
                            f'Server={db_server};'
                            'Trusted_Connection=yes;')
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{db_name}') CREATE DATABASE {db_name}")
        conn.commit()

        # Connect to the newly created database
        conn = odbc.connect(f'Driver={{SQL Server}};'
                            f'Server={db_server};'
                            f'Database={db_name};'
                            'Trusted_Connection=yes;')
        cursor = conn.cursor()

        # Create the tables if they don't exist
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Vehicles' AND xtype='U')
        CREATE TABLE Vehicles (
            Vehicle_Plate_Number NVARCHAR(50) PRIMARY KEY,
            Color NVARCHAR(50),
            Make NVARCHAR(50),
            Model NVARCHAR(50)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Parking_Slot' AND xtype='U')
        CREATE TABLE Parking_Slot (
            Floor_Slot_Number NVARCHAR(50) PRIMARY KEY,
            Availability VARCHAR(50)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Check_Ins' AND xtype='U')
        CREATE TABLE Check_Ins (
            Transaction_ID NVARCHAR(50) PRIMARY KEY,
            Vehicle_Plate_Number NVARCHAR(50),
            Floor_Slot_Number NVARCHAR(50),
            Check_In_Date DATE,
            Time_In TIME(0),
            Time_Out TIME(0),
            Check_Out_Date DATE,
            FOREIGN KEY (Vehicle_Plate_Number) REFERENCES Vehicles(Vehicle_Plate_Number),
            FOREIGN KEY (Floor_Slot_Number) REFERENCES Parking_Slot(Floor_Slot_Number)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Payments' AND xtype='U')
        CREATE TABLE Payments (
            Transaction_ID NVARCHAR(50) PRIMARY KEY,
            Customer_Vehicle_Plate_Number NVARCHAR(50),
            Floor_Slot_Number NVARCHAR(50),
            Transaction_Date DATETIME,
            Amount DECIMAL(10,2),
            Status VARCHAR(50),
            FOREIGN KEY (Customer_Vehicle_Plate_Number) REFERENCES Vehicles(Vehicle_Plate_Number),
            FOREIGN KEY (Floor_Slot_Number) REFERENCES Parking_Slot(Floor_Slot_Number),
            FOREIGN KEY (Transaction_ID) REFERENCES Check_Ins(Transaction_ID)
        );
        """)
        conn.commit()
        conn.close()

        # Display success message
        status_label.config(text="Database and tables created successfully or the database already exist! \nYou can now close the window (Will Automatically Close after few seconds)", fg="green")
    except odbc.Error as e:
        # Display error message
        status_label.config(text=f"Error creating database: {e}", fg="red")

# Function to handle window close
def on_close():
    window.destroy()

# Create the GUI window


# Create the GUI window
window = Tk()
window.title("Database Creator")
window.geometry("750x300")
window.configure(bg="#f1e7e7")
window.iconbitmap('logo.ico')
window.resizable(False, False)

# Bind the close event to the on_close function
window.protocol("WM_DELETE_WINDOW", on_close)

# Add a title label
Label(window, text="Database Creator", font=("Arial Narrow", 16, "bold"), bg="#f1e7e7", fg="black").pack(pady=20)

# Add a status label to display messages
status_label = Label(window, text="Creating database, please wait...", font=("Arial Narrow", 12), bg="#f1e7e7", fg="black")
status_label.pack(pady=20)

# Automatically execute the create_database function
window.after(100, create_database)

# Create cancel button while the database is being created
cancel_button = Button(window, text="Acknowledged", command=on_close, bg="#A9A9A9", fg="black")   

cancel_button.pack(pady=10)
#disable the button until the database creation is complete
cancel_button.config(state="disabled")
window.after(2000, lambda: cancel_button.config(state="normal", bg="lightgreen"))
window.after(4500, on_close)

# Add a footer label
footer_label = Label(window, text="Version V1.5 --A fullfilment of Course CPE-0011A Group of Abarabar, Gaspar, Fernandez, and Tandayu", font=("Arial Narrow", 10), bg="#f1e7e7", fg="black")
footer_label.pack(side="bottom", pady=5)

# Run the GUI event loop
window.mainloop()