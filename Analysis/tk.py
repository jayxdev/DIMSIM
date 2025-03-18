import tkinter as tk
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize the main window
root = tk.Tk()
root.title("Daily Activity Data Collection and Analysis")

# Create a DataFrame to store the data
data = pd.DataFrame(columns=['Date', 'Calories (kcal)', 'Distance (m)', 'Step count'])

# Create a label to display messages
message_label = tk.Label(root, text="", fg="red")
message_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Function to add data to the DataFrame
def add_data():
    global data
    date = entry_date.get()
    calories = entry_calories.get()
    distance = entry_distance.get()
    steps = entry_steps.get()
    
    if date and calories and distance and steps:
        new_data = pd.DataFrame([[date, float(calories), float(distance), float(steps)]], columns=['Date', 'Calories (kcal)', 'Distance (m)', 'Step count'])
        data = pd.concat([data, new_data], ignore_index=True)
        message_label.config(text="Data added successfully!", fg="green")
    else:
        message_label.config(text="Please fill all fields", fg="red")

# Function to display the data
def display_data():
    global data
    if not data.empty:
        top = tk.Toplevel(root)
        top.title("Data Overview")
        text = tk.Text(top)
        text.pack()
        text.insert(tk.END, data.to_string())
    else:
        message_label.config(text="No data to display", fg="red")

# Function to plot the data
def plot_data():
    global data
    if not data.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Date', y='Step count', data=data, marker='o', color='skyblue')
        plt.xlabel('Date')
        plt.ylabel('Step Count')
        plt.title('Daily Step Count Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        
    else:
        message_label.config(text="No data to plot", fg="red")

# Function to save data to CSV
def save_data():
    global data
    if not data.empty:
        data.to_csv('activity_data.csv', index=False)
        message_label.config(text="Data saved to CSV successfully!", fg="green")
    else:
        message_label.config(text="No data to save", fg="red")

# Function to load data from CSV
def load_data():
    global data
    try:
        data = pd.read_csv('dailyActivity copy.csv')
        message_label.config(text="Data loaded from CSV successfully!", fg="green")
    except FileNotFoundError:
        message_label.config(text="No CSV file found to load data", fg="red")

# Automatically load data when the application starts
load_data()

# Create and place the input fields and labels
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=5)
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Calories (kcal)").grid(row=1, column=0, padx=10, pady=5)
entry_calories = tk.Entry(root)
entry_calories.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Distance (m)").grid(row=2, column=0, padx=10, pady=5)
entry_distance = tk.Entry(root)
entry_distance.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Step count").grid(row=3, column=0, padx=10, pady=5)
entry_steps = tk.Entry(root)
entry_steps.grid(row=3, column=1, padx=10, pady=5)

# Create and place the buttons
tk.Button(root, text="Add Data", command=add_data).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Display Data", command=display_data).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Plot Data", command=plot_data).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()