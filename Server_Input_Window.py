from tkinter import *

# Create the server input window
window = Tk()
window.title("Server Input Window")
window.geometry("300x200")
window.configure(bg="#f1e7e7")
window.resizable(False, False)
window.iconbitmap('logo.ico')

# Create a global variable to store the server name
server_name_var = StringVar()

def get_server_name():
    # Return the server name from the input field
    return server_name_var.get()

def submit_server_name():
    # Set the server name and close the window
    server_name_var.set(inputserver.get())
    window.destroy()

inputserver = StringVar()
Label(window, text="Enter Server Name:", bg="#f1e7e7").pack(pady=10)
Entry(window, textvariable=inputserver, width=30).pack(pady=10)

# Submit button
Button(window, text="Submit", command=submit_server_name, bg="lightgreen").pack(pady=10)

# Run the window
window.mainloop()