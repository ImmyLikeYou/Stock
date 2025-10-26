import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from waitress import serve
from app import app, init_db  # Import our Flask app and init_db function

# --- Server Configuration ---
HOST = '127.0.0.1'
PORT = 5000
URL = f"http://{HOST}:{PORT}"

# --- Functions for GUI ---

def start_server():
    """Runs the Waitress server in a separate thread."""
    try:
        # Initialize the database
        init_db() 
        print(f"Starting server at {URL}...")
        serve(app, host=HOST, port=PORT)
    except Exception as e:
        print(f"Error starting server: {e}")
        messagebox.showerror("Server Error", f"Failed to start server:\n{e}")

def open_browser():
    """Opens the web browser to the application's URL."""
    webbrowser.open(URL)

def on_closing():
    """Asks for confirmation before closing the app (and stopping the server)."""
    if messagebox.askokcancel("Quit?", "Do you want to quit? This will stop the server."):
        root.destroy() # Closing the main window will stop the daemon thread

# --- Create the GUI ---
root = tk.Tk()
root.title("Stock Manager Server")
root.geometry("350x180") # Set the window size
root.resizable(False, False) # Prevent resizing

# Style
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"))

# Create and arrange widgets
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill=tk.BOTH)

status_label = ttk.Label(main_frame, text="✅ Server is running!", font=("Arial", 14, "bold"), foreground="green")
status_label.pack(pady=5)

url_label = ttk.Label(main_frame, text=f"Access at: {URL}")
url_label.pack(pady=5)

open_button = ttk.Button(main_frame, text="Open in Browser", command=open_browser)
open_button.pack(pady=10, ipadx=10, ipady=5)

close_label = ttk.Label(main_frame, text="Close this window to stop the server.")
close_label.pack(pady=5)

# --- Start the Server Thread ---
# We use a daemon thread so that it automatically stops when the GUI closes.
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# --- Start the GUI Main Loop ---
root.protocol("WM_DELETE_WINDOW", on_closing)  # Catch the "X" button click
root.mainloop()