from .setup import tk, messagebox
import mysql.connector

usert = False

def run_login_system(root, message_label):
    # Create the main window
    # Database setup
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="user"
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255))''')
    conn.commit()

    # Set window size and position
    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Configure grid layout
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(3, weight=1)

    # Username and password labels and entries
    tk.Label(root, text="Username").grid(row=1, column=1, padx=10, pady=10, sticky="e")
    entry_username = tk.Entry(root)
    entry_username.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    tk.Label(root, text="Password").grid(row=2, column=1, padx=10, pady=10, sticky="e")
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    # Functions
    def signup():
        username = entry_username.get()
        password = entry_password.get()
        if username and password:
            try:
                c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                usert = True
                messagebox.showinfo("Success", "Signup successful!")
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
        else:
            messagebox.showerror("Error", "Please enter both username and password")

    def login():
        username = entry_username.get()
        password = entry_password.get()
        c.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        if c.fetchone():
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    # Signup and login buttons
    tk.Button(root, text="Signup", command=signup).grid(row=3, column=1, padx=10, pady=10)
    tk.Button(root, text="Login", command=login).grid(row=3, column=2, padx=10, pady=10)

    # Run the application
    root.mainloop()

    # Close the database connection when the application is closed
    conn.close()
