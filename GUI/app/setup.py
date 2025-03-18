import tkinter as tk
import pandas as pd
from tkinter import messagebox

# Set the name of the CSV file to store the data
data_file = 'C:\\Users\\JAYDEV\\Desktop\\python lab\\python project-4\\app\\Daily_Activity_metrics.csv'

def get_window():
    root = tk.Tk()
    root.title("Daily Activity Tracker")
    # Create a label to display messages
    message_label = tk.Label(root, text="", fg="red")
    message_label.grid(row=6, column=2, columnspan=2, padx=10, pady=5)
    return root, message_label

def clear_window(root, message_label):
    for widget in root.winfo_children():
        if widget != message_label:
            widget.destroy()
    message_label.config(text="")

    