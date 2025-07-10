from tkinter import *
import pyodbc as odbc
import datetime
from Server_Input_Window import window as server_window
from Server_Input_Window import get_server_name as Server_Name
from CreateDB import window as cdb  # Import the create_database function

# Wait for the server input window to close
server_window.mainloop()
DBServer_Name = Server_Name()

# Check if the database exists
try:
    connection = odbc.connect('Driver={SQL Server};' +
                               f'Server={DBServer_Name};' +
                               'Trusted_Connection=True;')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sys.databases WHERE name = 'Community_Parking'")
    database_exists = cursor.fetchone()

    if not database_exists:
        print("Database does not exist. Creating database...")
        cdb.mainloop() # Call the create_database function from CreateDB
        print("Database created successfully.")
    else:
        print("Database already exists. Proceeding with the application.")

except odbc.Error as e:
    print(f"Error checking database existence: {e}")
    exit(1)  # Exit the program if there is an error

# Connect to the database
connection = odbc.connect('Driver={SQL Server};' +
                           f'Server={DBServer_Name};' +
                           'Database=Community_Parking;' +
                           'Trusted_Connection=True;')
print(f'{connection} established... Please Wait, Program is Launching.')

# Create the main application window
window = Tk()
window.title('Automated Parking System')
window.geometry("600x800")

icon = PhotoImage(file='logo.png')
window.config(background='#967e27')
window.iconphoto(True, icon)
banner = PhotoImage(file='banner.ico.png')
window.resizable(False, False)
print("Successful.")

# Rest of your GUI code...


def IsConnected():
    try:
        connection = odbc.connect('Driver={SQL Server};'+
                        f'Server={DBServer_Name}'+
                        'Database=Community_Parking;'+
                        'Trusted_Connection=True;')
        return "Connected to Server"
    except odbc.Error:
        return "Connection Found"
    
def get_server_name():
    try:
        # Extract the server name from the connection string
        connection_string = connection.getinfo(odbc.SQL_SERVER_NAME)
        return connection_string
    except odbc.Error as e:
        return f"Error retrieving server name: {e}"

def vehicle_register():
    # Disable the "Check In" button
    button.config(state=DISABLED)

    # Create a new window for check-in
    check_in_window = Toplevel()
    check_in_window.title("New Vehicle Registration Query")
    check_in_window.geometry("600x400")
    check_in_window.config(background='#967e27')

    # Re-enable the button when the window is closed
    def on_close():
        button.config(state=ACTIVE)
        check_in_window.destroy()

    check_in_window.protocol("WM_DELETE_WINDOW", on_close)

    # Variables to track entry fields
    vehicle_make_var = StringVar()
    vehicle_color_var = StringVar()
    vehicle_plate_var = StringVar()
    vehicle_model_var = StringVar()

    # Function to check if all fields are filled
    def check_fields():
        if (vehicle_make_var.get().strip() and
            vehicle_color_var.get().strip() and
            vehicle_plate_var.get().strip() and
            vehicle_model_var.get().strip()):
            submit_button.config(state=ACTIVE)
        else:
            submit_button.config(state=DISABLED)

    # Labels and Entry boxes for vehicle details
    Label(check_in_window, text="Vehicle Make:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=50)
    vehicle_make_entry = Entry(check_in_window, font=('Arial Narrow', 12), width=30, textvariable=vehicle_make_var)
    vehicle_make_entry.place(x=350, y=50)

    Label(check_in_window, text="Vehicle Color:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=100)
    vehicle_color_entry = Entry(check_in_window, font=('Arial Narrow', 12), width=30, textvariable=vehicle_color_var)
    vehicle_color_entry.place(x=350, y=100)

    Label(check_in_window, text="Vehicle Plate Number:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=150)
    vehicle_plate_entry = Entry(check_in_window, font=('Arial Narrow', 12), width=30, textvariable=vehicle_plate_var)
    vehicle_plate_entry.place(x=350, y=150)

    Label(check_in_window, text="Vehicle Model:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=200)
    vehicle_model_entry = Entry(check_in_window, font=('Arial Narrow', 12), width=30, textvariable=vehicle_model_var)
    vehicle_model_entry.place(x=350, y=200)

    # Trace changes in the entry fields
    vehicle_make_var.trace("w", lambda *args: check_fields())
    vehicle_color_var.trace("w", lambda *args: check_fields())
    vehicle_plate_var.trace("w", lambda *args: check_fields())
    vehicle_model_var.trace("w", lambda *args: check_fields())

    # Submit button
    def submit_check_in():
        vehicle_make = vehicle_make_var.get()
        vehicle_color = vehicle_color_var.get()
        vehicle_plate = vehicle_plate_var.get()
        vehicle_model = vehicle_model_var.get()

        try:
            # Insert the data into the database
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Vehicles (Vehicle_Plate_Number, Color, Make, Model)
                VALUES (?, ?, ?, ?)
            """, (vehicle_plate, vehicle_color, vehicle_make, vehicle_model))
            connection.commit()  # Commit the transaction
            print("Data inserted successfully!")
        except odbc.Error as e:
            print("Error inserting data:", e)
        finally:
            # Close the check-in window after submission
            on_close()

    submit_button = Button(check_in_window, text="Submit", command=submit_check_in, font=('Arial Narrow', 12), bg='#eb9b34', fg='black', width=30, state=DISABLED)
    submit_button.place(x=150, y=250)

def show_customers():
    button1.config(state=DISABLED)

    

    customers_window = Toplevel()
    customers_window.title("Transaction Records")
    customers_window.geometry("1250x600")
    customers_window.config(background='#967e27')
    #disable the rezize of the window
    customers_window.resizable(False, False)


    # Re-enable the button when the window is closed
    def on_close():
        button1.config(state=ACTIVE)
        customers_window.destroy()

    customers_window.protocol("WM_DELETE_WINDOW", on_close)

    # Add a frame to hold the table
    table_frame = Frame(customers_window, bg='#967e27')
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Add a title label
    Label(customers_window, text="Customer Details", font=('Arial Narrow', 15, 'bold'), bg='#967e27', fg='black').pack(pady=10)

    try:
        # Query the database for customer details, ordered by the latest record
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Check_Ins.Transaction_ID, 
                   Vehicles.Vehicle_Plate_Number, 
                   Vehicles.Make, 
                   Vehicles.Model, 
                   Check_Ins.Floor_Slot_Number, 
                   Check_Ins.Time_In, 
                   Check_Ins.Time_Out, 
                   Payments.Amount, 
                   Payments.Status
            FROM Check_Ins
            INNER JOIN Payments ON Check_Ins.Transaction_ID = Payments.Transaction_ID
            INNER JOIN Vehicles ON Check_Ins.Vehicle_Plate_Number = Vehicles.Vehicle_Plate_Number 
                                     AND Payments.Customer_Vehicle_Plate_Number = Vehicles.Vehicle_Plate_Number
            ORDER BY Check_Ins.Check_In_Date DESC
        """)
        customers = cursor.fetchall()

        if customers:
            # Create headers for the table
            headers = ["Transaction ID", "Plate Number", "Make", "Model", "Slot Number", "Time In", "Time Out", "Amount", "Status"]
            for col, header in enumerate(headers):
                Label(table_frame, text=header, font=('Arial Narrow', 12, 'bold'), bg='#eb9b34', fg='black', width=15, relief=SOLID).grid(row=0, column=col, padx=5, pady=5)

            # Display customer details
            for row, customer in enumerate(customers, start=1):
                for col, value in enumerate(customer):
                    # Display "N/A" if Time_Out is NULL
                    if col == 6 and value is None:  # Time_Out column
                        value = "N/A"
                    Label(table_frame, text=value, font=('Arial Narrow', 12), bg='#967e27', fg='black', width=15, relief=SOLID).grid(row=row, column=col, padx=5, pady=5)
        else:
            # Display a message if no customers are found
            Label(customers_window, text="No Transaction Records found.", font=('Arial Narrow', 12), bg='#967e27', fg='black').pack(pady=20)

    except odbc.Error as e:
        # Handle database errors
        Label(customers_window, text=f"Error fetching data: {e}", font=('Arial Narrow', 12), bg='#967e27', fg='red').pack(pady=20)

    finally:
        cursor.close()

    # Add a close button
    Button(customers_window, text="Close", command=on_close, font=('Arial Narrow', 12), bg='#eb9b34', fg='black').pack(pady=20)
    
def check_in():
    #disable the button
    New_Check_In_Button.config(state=DISABLED)

    def on_close():
        New_Check_In_Button.config(state=ACTIVE)
        check_in_window.destroy()


    # Create a new window for check-in
    check_in_window = Toplevel()
    check_in_window.title("New Check In")
    check_in_window.geometry("600x400")
    check_in_window.config(background='#967e27')
    
    check_in_window.protocol("WM_DELETE_WINDOW", on_close)

    # Generate a new Transaction_ID and Check_In_Date
    transaction_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Unique ID as a string
    check_in_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time

    # Variables to track entry fields
    vehicle_plate_var = StringVar()
    floor_slot_var = StringVar()

    # Labels and Entry boxes for check-in details
    Label(check_in_window, text="Transaction ID:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=50)
    Label(check_in_window, text=transaction_id, font=('Arial Narrow', 12), bg='#967e27', fg='black').place(x=250, y=50)

    Label(check_in_window, text="Check In Date:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=100)
    Label(check_in_window, text=check_in_date, font=('Arial Narrow', 12), bg='#967e27', fg='black').place(x=250, y=100)

    Label(check_in_window, text="Vehicle Plate Number:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=150)
    vehicle_plate_entry = Entry(check_in_window, font=('Arial Narrow', 12), width=30, textvariable=vehicle_plate_var)
    vehicle_plate_entry.place(x=250, y=150)

    Label(check_in_window, text="Floor Slot Number:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=200)
    floor_slot_entry = Entry(check_in_window, font=('Arial Narrow', 12), width=30, textvariable=floor_slot_var)
    floor_slot_entry.place(x=250, y=200)
    
    # Function to check if all fields are filled
    def check_fields():
        if vehicle_plate_var.get().strip() and floor_slot_var.get().strip():
            submit_button.config(bg='#eb9b34')
        else:
            submit_button.config(bg='red')
    #Get red if all the fields are empty again
    vehicle_plate_var.trace("w", lambda *args: check_fields())
    floor_slot_var.trace("w", lambda *args: check_fields())

    # Submit button
    def submit_check_in():
        vehicle_plate = vehicle_plate_var.get()
        floor_slot = floor_slot_var.get()
        
         # Function to check if all fields are filled
    

        

        if not vehicle_plate or not floor_slot:
            Label(check_in_window, text="All fields are required!", font=('Arial Narrow', 12), bg='#967e27', fg='red').place(x=200, y=300)
            return

        try:
            cursor = connection.cursor()

            # Validate Vehicle_Plate_Number
            cursor.execute("SELECT COUNT(*) FROM Vehicles WHERE Vehicle_Plate_Number = ?", (vehicle_plate,))
            vehicle_exists = cursor.fetchone()[0]

            if not vehicle_exists:
                Label(check_in_window, text="Error: Vehicle Plate Number does not exists on the records!", font=('Arial Narrow', 12), bg='#967e27', fg='red').place(x=150, y=300)
                return

            # Validate Floor_Slot_Number
            cursor.execute("SELECT COUNT(*) FROM Parking_Slot WHERE Floor_Slot_Number = ? AND Availability = 'Vacant'", (floor_slot,))
            slot_exists = cursor.fetchone()[0]

            if not slot_exists:
                Label(check_in_window, text="Error: Floor Slot Number does not exist or is Occupied!", font=('Arial Narrow', 12), bg='#967e27', fg='red').place(x=100, y=300)
                return

            # Insert the data into the Check_Ins table
            cursor.execute("""
                INSERT INTO Check_Ins (Transaction_ID, Vehicle_Plate_Number, Floor_Slot_Number, Check_In_Date, Time_In)
                VALUES (?, ?, ?, ?, ?)
            """, (transaction_id, vehicle_plate, floor_slot, check_in_date, check_in_date))  # Use check_in_date for Time_In
            connection.commit()  # Commit the transaction

            # Insert the data into the Payments table
            cursor.execute("""
                INSERT INTO Payments (Transaction_ID, Customer_Vehicle_Plate_Number, Floor_Slot_Number, Transaction_Date, Amount, Status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (transaction_id, vehicle_plate, floor_slot, check_in_date, 40.00, 'PENDING'))
            connection.commit()  # Commit the transaction

            # Update the Parking_Slot table to set the slot as "Occupied"
            cursor.execute("""
                UPDATE Parking_Slot
                SET Availability = 'Occupied'
                WHERE Floor_Slot_Number = ?
            """, (floor_slot,))
            connection.commit()  # Commit the update

            print("Check-in record and payment record inserted successfully!")
            Label(check_in_window, text="Check-in successful!", font=('Arial Narrow', 12), bg='#967e27', fg='green').place(x=200, y=300)

        except odbc.Error as e:
            print("Error inserting data:", e)
            Label(check_in_window, text=f"Error: {e}", font=('Arial Narrow', 12), bg='#967e27', fg='red').place(x=200, y=300)
        finally:
            on_close()
            cursor.close()

    submit_button = Button(check_in_window, text="Submit", command=submit_check_in, font=('Arial Narrow', 12), bg='red', fg='black', width=20)
    submit_button.place(x=200, y=250)
    

    # Close button
    Button(check_in_window, text="Close",command = on_close, font=('Arial Narrow', 12), bg='#eb9b34', fg='black', width=20).place(x=200, y=350)

label = Label(window, text = "Automated Parking Database System", 
              font = ('Arial Narrow',15, 'bold'),
              fg = 'black', 
              bg = '#967e27',
              image = banner,
              compound = 'top')
label.pack()
 
def show_vacant_slots():
    # Create a new window for displaying vacant slots
    vacant_slots_window = Toplevel()
    vacant_slots_window.title("Vacant Slots")
    vacant_slots_window.geometry("600x500")
    vacant_slots_window.config(background='#967e27')

    # Add a title label
    Label(vacant_slots_window, text="Vacant Slots", font=('Arial Narrow', 15, 'bold'), bg='#967e27', fg='black').pack(pady=10)

    try:
        # Query the database for vacant slots
        cursor = connection.cursor()
        cursor.execute("SELECT Floor_Slot_Number FROM Parking_Slot WHERE Availability = 'Vacant'")
        slots = cursor.fetchall()

        if slots:
            # Display the vacant slots
            for index, slot in enumerate(slots, start=1):
                floor_slot_number = slot[0]  # Extract the Floor_Slot_Number
                Label(vacant_slots_window, text=f"{index}. Floor Slot Number: {floor_slot_number}",
                      font=('Arial Narrow', 12), bg='#967e27', fg='black').pack(anchor='w', padx=20, pady=5)
        else:
            # Display a message if no slots are vacant
            Label(vacant_slots_window, text="No vacant slots available.", font=('Arial Narrow', 12), bg='#967e27', fg='black').pack(pady=20)

    except odbc.Error as e:
        # Handle database errors
        Label(vacant_slots_window, text=f"Error fetching data: {e}", font=('Arial Narrow', 12), bg='#967e27', fg='red').pack(pady=20)

    finally:
        cursor.close()

    # Add a close button
    Button(vacant_slots_window, text="Close", command=vacant_slots_window.destroy, font=('Arial Narrow', 12), bg='#eb9b34', fg='black').pack(pady=20)

def show_vehicles():
    # Create a new window for displaying vehicles
    vehicles_window = Toplevel()
    vehicles_window.title("Vehicles")
    vehicles_window.geometry("720x600")
    vehicles_window.config(background='#967e27')

    # Add a title label
    Label(vehicles_window, text="Vehicle List", font=('Arial Narrow', 15, 'bold'), bg='#967e27', fg='black').pack(pady=10)

    # Add a frame to hold the table
    table_frame = Frame(vehicles_window, bg='#967e27')
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    try:
        # Query the database for vehicle details
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Vehicles.Vehicle_Plate_Number, Vehicles.Color, Vehicles.Make, Vehicles.Model 
            FROM Vehicles
            LEFT JOIN Payments ON Vehicles.Vehicle_Plate_Number = Payments.Customer_Vehicle_Plate_Number
            WHERE Payments.Status = 'PENDING' OR Payments.Status IS NULL;
        """)
        vehicles = cursor.fetchall()

        if vehicles:
            # Create headers for the table
            headers = ["Plate Number", "Color", "Make", "Model"]
            header_frame = Frame(table_frame, bg='#eb9b34')
            header_frame.pack(fill=X, pady=5)
            for header in headers:
                Label(header_frame, text=header, font=('Arial Narrow', 12, 'bold'), bg='#eb9b34', fg='black', width=20, relief=SOLID).pack(side=LEFT, padx=5)

            # Display vehicle details
            for vehicle in vehicles:
                row_frame = Frame(table_frame, bg='#967e27')
                row_frame.pack(fill=X, pady=2)
                for value in vehicle:
                    Label(row_frame, text=value, font=('Arial Narrow', 12), bg='#967e27', fg='black', width=20, relief=SOLID).pack(side=LEFT, padx=5)
        else:
            # Display a message if no vehicles are found
            Label(vehicles_window, text="No vehicles found.", font=('Arial Narrow', 12), bg='#967e27', fg='black').pack(pady=20)

    except odbc.Error as e:
        # Handle database errors
        Label(vehicles_window, text=f"Error fetching data: {e}", font=('Arial Narrow', 12), bg='#967e27', fg='red').pack(pady=20)

    finally:
        cursor.close()

    # Add a close button
    Button(vehicles_window, text="Close", command=vehicles_window.destroy, font=('Arial Narrow', 12), bg='#eb9b34', fg='black').pack(pady=20)

def process_payment():
    # Create a new window for processing payments
    payment_window = Toplevel()
    payment_window.title("Process Payment")
    payment_window.geometry("680x400")
    payment_window.config(background='#967e27')

    # Variables to track entry fields
    Vehicle_Plate_Number_var = StringVar()

    def check_fields():
        if Vehicle_Plate_Number_var.get().strip():
            Button_Payment.config(bg='#eb9b34')
            Button_Fetch.config(bg='#eb9b34')
        else:
            Button_Payment.config(bg='red')
            Button_Fetch.config(bg='red')

    #Get red if all the fields are empty again
    Vehicle_Plate_Number_var.trace("w", lambda *args: check_fields())
    

    # Labels and Entry boxes for payment details
    Label(payment_window, text="Enter Vehicle Plate Number:", font=('Arial Narrow', 12, 'bold'), bg='#967e27', fg='black').place(x=50, y=50)
    transaction_id_entry = Entry(payment_window, font=('Arial Narrow', 12), width=30, textvariable=Vehicle_Plate_Number_var)
    transaction_id_entry.place(x=250, y=50)

    # Frame to display check-in details
    details_frame = Frame(payment_window, bg='#967e27', relief=SOLID, borderwidth=1)
    details_frame.place(x=50, y=100, width=550, height=150)

    # Function to fetch and display check-in details
    def fetch_details():
        Plate_Number = Vehicle_Plate_Number_var.get()

        if not Plate_Number:
            for widget in details_frame.winfo_children():
                widget.destroy()
            Label(details_frame, text="Vehicle Plate Number is required!", font=('Arial Narrow', 12), bg='#967e27', fg='red').pack(pady=10)
            return

        try:
            cursor = connection.cursor()

            # Fetch check-in details
            cursor.execute("""
                SELECT Check_Ins.Transaction_ID, 
                       Check_Ins.Vehicle_Plate_Number, 
                       Check_Ins.Floor_Slot_Number, 
                       Check_Ins.Check_In_Date
                FROM Check_Ins
                WHERE Vehicle_Plate_Number = ?
            """, (Plate_Number,))
            check_in_details = cursor.fetchone()

            # Clear previous details
            for widget in details_frame.winfo_children():
                widget.destroy()

            if check_in_details:
                # Display check-in details
                headers = ["Transaction ID", "Plate Number", "Slot Number", "Check-In Date"]
                for col, header in enumerate(headers):
                    Label(details_frame, text=header, font=('Arial Narrow', 12, 'bold'), bg='#eb9b34', fg='black', width=15, relief=SOLID).grid(row=0, column=col, padx=5, pady=5)

                for col, value in enumerate(check_in_details):
                    Label(details_frame, text=value, font=('Arial Narrow', 12), bg='#967e27', fg='black', width=15, relief=SOLID).grid(row=1, column=col, padx=5, pady=5)
            else:
                Label(details_frame, text="Vehicle Plate Number not found!", font=('Arial Narrow', 12), bg='#967e27', fg='red').pack(pady=10)

        except odbc.Error as e:
            Label(details_frame, text=f"Error fetching data: {e}", font=('Arial Narrow', 12), bg='#967e27', fg='red').pack(pady=10)

    # Function to process payment
    def record_payment():
        Vehicle_Plate = Vehicle_Plate_Number_var.get()

        if not Vehicle_Plate:
            Label(payment_window, text="Vehicle Plate Number is required!", font=('Arial Narrow', 12), bg='#967e27', fg='red').place(x=250, y=315)
            return

        try:
            cursor = connection.cursor()

            # Fetch Floor_Slot_Number and Vehicle_Plate_Number
            cursor.execute("""
                SELECT Floor_Slot_Number, Vehicle_Plate_Number, Transaction_ID, Time_In
                FROM Check_Ins
                WHERE Vehicle_Plate_Number = ?
            """, (Vehicle_Plate,))
            result = cursor.fetchone()

            if not result:
                Label(payment_window, text="Plate Number not found!", font=('Arial Narrow', 12), bg='#967e27', fg='red').place(x=200, y=300)
                return

            floor_slot, vehicle_plate, transaction_id, *rest = result
            transaction_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
            amount = 40.00
            status = "PAID"

            

            # Insert payment record into Payments table
            cursor.execute("""
                INSERT INTO Payments (Transaction_ID, Customer_Vehicle_Plate_Number, Floor_Slot_Number, Transaction_Date, Amount, Status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (transaction_id, vehicle_plate, floor_slot, transaction_date, amount, status))
            connection.commit()

            # Update Parking_Slot table to set the slot as "Vacant"
            cursor.execute("""
                UPDATE Parking_Slot
                SET Availability = 'Vacant'
                WHERE Floor_Slot_Number = ?
            """, (floor_slot,))
            connection.commit()

            # Update Check_Ins table to set Time_Out
            time_out = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                UPDATE Check_Ins
                SET Time_Out = ?
                WHERE Transaction_ID = ?
            """, (time_out, transaction_id))
            connection.commit()
            
            #Update Payment table to set Status
            cursor.execute("""UPDATE Payments
                SET Status = 'PAID' where Customer_Vehicle_Plate_Number = ?
            """, (transaction_id,))

            

            Label(payment_window, text="Payment recorded successfully!", font=('Arial Narrow', 12), bg='#967e27', fg='green').place(x=246, y=315)

        except odbc.Error as e:
            Label(payment_window, text=f"Error recording payment: {e}", font=('Arial Narrow', 12), bg='#967e27', fg='red').place(x=200, y=300)

    # Fetch details button
    Button_Fetch = Button(payment_window, text="Fetch Details", command=fetch_details, font=('Arial Narrow', 12), bg='red', fg='black')
    Button_Fetch.place(relx=0.35, y=270)

    # Record payment button
    Button_Payment = Button(payment_window, text="Record Payment", command=record_payment, font=('Arial Narrow', 12), bg='red', fg='black')
    Button_Payment.place(relx=0.50, y=270)

    # Close button
    Button_Close = Button(payment_window, text="Close", command=payment_window.destroy, font=('Arial Narrow', 12), bg='#eb9b34', fg='black')
    Button_Close.place(relx=0.45, y=350)

button = Button(window, text = 'New Vehicle Registration',
                command = vehicle_register,
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = '#eb9b34',
                activebackground =  '#eb9b34',
                state = ACTIVE, 
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)

button1 = Button(window, text = 'Transaction Records',
                command = show_customers,
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = '#eb9b34',
                activebackground =  '#eb9b34',
                state = ACTIVE, 
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)


button2 = Button(window, text = 'Available Slot Finder',
                command = show_vacant_slots,
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = '#eb9b34',
                activebackground =  '#eb9b34',
                state = ACTIVE, 
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)

New_Check_In_Button = Button(window, text = 'New Check In',
                command = check_in,
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = '#eb9b34',
                activebackground =  '#eb9b34',
                state = ACTIVE, 
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)

exit_button = Button(window, text = 'Exit',
                command = window.quit,
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = '#eb9b34',
                activebackground =  '#eb9b34',
                state = ACTIVE, 
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)

Vehicles_Query = Button(window, text = 'Vehicle Records',
                command = show_vehicles,
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = '#eb9b34',
                activebackground =  '#eb9b34',
                state = ACTIVE, 
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)

payments = Button(window, text = 'Payments',
                command = process_payment,
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = '#eb9b34',
                activebackground =  '#eb9b34',
                state = ACTIVE, 
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)



def Reset_Database():
    #Create a new window for confirmation
    reset_window = Toplevel()
    reset_window.title("Reset Database")
    reset_window.geometry("400x200")
    reset_window.config(background='#967e27')
    reset_window.resizable(False, False)

    # Function to reset the database
    def reset_database():
        try:
            cursor = connection.cursor()
            # Reset the database by deleting all records from the tables
            cursor.execute("DELETE FROM Payments")
            cursor.execute("DELETE FROM Check_Ins")
            cursor.execute("DELETE FROM Vehicles")
            cursor.execute("UPDATE Parking_Slot SET Availability = 'Vacant'")
            connection.commit()  # Commit the changes
            print("Database reset successfully!")
        except odbc.Error as e:
            print("Error resetting database:", e)
        finally:
            cursor.close()
            reset_window.destroy()


    #Add a label to confirm the action
    Label(reset_window, text="Are you sure you want to reset the database?", font=('Arial Narrow', 12), bg='#967e27', fg='black').pack(pady=10)
    Label(reset_window, text="This action cannot be undone.", font=('Arial Narrow', 12), bg='#967e27', fg='red').pack(pady = 10)
    Button(reset_window, text="Yes", command=reset_database, font=('Arial Narrow', 12), bg='red', fg='black', height = 1, width = 20).pack(padx=20, pady=10)
    Button(reset_window, text="No", command=reset_window.destroy, font=('Arial Narrow', 12), bg='#eb9b34', fg='black', height = 1, width = 20).pack(padx=10, pady=10)

    #Button to reset the Database
reset_button = Button(window, text = 'Reset Database',
                command = Reset_Database,  # Placeholder for reset function
                font = ('Arial Narrow', 10),
                fg = 'black',
                bg = 'red',
                activebackground =  'red',
                state = ACTIVE,
                compound = 'left',
                height = 2,
                width = 60,
                relief = RAISED,)

button.place(relx=0.5, rely=0.4, anchor='center')
button1.place(relx=0.5, rely=0.46, anchor='center')
button2.place(relx=0.5, rely=0.52, anchor='center')
exit_button.place(relx=0.5, rely=0.84, anchor='center')
New_Check_In_Button.place(relx=0.5, rely=0.62, anchor='center')
Vehicles_Query.place(relx=0.5, rely=0.68, anchor='center')
payments.place(relx=0.5, rely=0.74, anchor='center')
reset_button.place(relx=0.5, rely=0.90, anchor='center')

label = Label(window, text = "Welcome, Please Select an Option", 
              font = ('Arial Narrow',10, 'bold'),
              fg = 'black', 
              bg = '#967e27')
label.place(relx=0.5, rely=0.32, anchor='center')

connection_label = Label(window, text = f"Status: {IsConnected()} {get_server_name()}", 
              font = ('Arial Narrow',10, 'bold'),
              fg = 'limegreen', 
              bg = '#967e27')
connection_label.place(relx=0.5, rely=0.99, anchor='center')

window.mainloop()   