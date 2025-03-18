from .setup import clear_window, messagebox, pd, tk
from tkinter import ttk
from .loadsave import save_data, load_data


def edit_data(root, message_label):
    # Load existing data
    data = load_data(message_label)

    # Clear the main window
    clear_window(root, message_label)
    edit_window = root
    edit_window.title("Edit Data")

    # UI Elements
    tk.Label(edit_window, text="Date (DD-MM-YYYY)").grid(row=0, column=0, padx=10, pady=5)
    entry_search_date = tk.Entry(edit_window)
    entry_search_date.grid(row=0, column=1, padx=10, pady=5)

    # Function to search data by date
    def search_data():
        try:
            search_date = pd.to_datetime(entry_search_date.get(), format='%d-%m-%Y')
            if search_date in data['Date'].values:
                record = data[data['Date'] == search_date].iloc[0]
                entry_calories_edit.delete(0, tk.END)
                entry_calories_edit.insert(0, record['Calories (1000kcal)'] * 1000)
                entry_distance_edit.delete(0, tk.END)
                entry_distance_edit.insert(0, record['Distance (Km)'] * 1000)
                entry_steps_edit.delete(0, tk.END)
                entry_steps_edit.insert(0, record['Step count(1000)'] * 1000)
                entry_avg_heart_rate_edit.delete(0, tk.END)
                entry_avg_heart_rate_edit.insert(0, record['Average heart rate (bpm)'])
                entry_max_heart_rate_edit.delete(0, tk.END)
                entry_max_heart_rate_edit.insert(0, record['Max heart rate (bpm)'])
                entry_min_heart_rate_edit.delete(0, tk.END)
                entry_min_heart_rate_edit.insert(0, record['Min heart rate (bpm)'])
                entry_avg_speed_edit.delete(0, tk.END)
                entry_avg_speed_edit.insert(0, record['Average speed (m/s)'])
            else:
                messagebox.showerror("Error", "Date not found in data")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    tk.Button(edit_window, text="Search", command=search_data).grid(row=0, column=2, padx=10, pady=5)

    # Entry fields for editing data
    labels_and_entries = [
        ("Calories (kcal)", 1, 0),
        ("Distance (m)", 2, 0),
        ("Step count", 3, 0),
        ("Max Heart Rate(bpm)", 0, 3),
        ("Min Heart Rate(bpm)", 1, 3),
        ("Avg Heart Rate(bpm)", 2, 3),
        ("Average speed (m/s)", 3, 3),
    ]

    # input labels and entries
    entry_vars = {}
    for label, row, col in labels_and_entries:
        tk.Label(edit_window, text=label).grid(row=row, column=col, padx=10, pady=5)
        entry = tk.Entry(edit_window)
        entry.grid(row=row, column=col + 1, padx=10, pady=5)
        entry_vars[label] = entry

    # Map entry variables for easier reference
    (
        entry_calories_edit,
        entry_distance_edit,
        entry_steps_edit,
        entry_max_heart_rate_edit,
        entry_min_heart_rate_edit,
        entry_avg_heart_rate_edit,
        entry_avg_speed_edit,
    ) = entry_vars.values()

    # Function to update data
    def update_data():
        try:
            search_date = pd.to_datetime(entry_search_date.get(), format='%d-%m-%Y')
            if search_date in data['Date'].values:
                data.loc[data['Date'] == search_date, 'Calories (1000kcal)'] = float(entry_calories_edit.get()) / 1000
                data.loc[data['Date'] == search_date, 'Distance (Km)'] = float(entry_distance_edit.get()) / 1000
                data.loc[data['Date'] == search_date, 'Step count(1000)'] = float(entry_steps_edit.get()) / 1000
                data.loc[data['Date'] == search_date, 'Average heart rate (bpm)'] = float(entry_avg_heart_rate_edit.get())
                data.loc[data['Date'] == search_date, 'Max heart rate (bpm)'] = float(entry_max_heart_rate_edit.get())
                data.loc[data['Date'] == search_date, 'Min heart rate (bpm)'] = float(entry_min_heart_rate_edit.get())
                data.loc[data['Date'] == search_date, 'Average speed (m/s)'] = float(entry_avg_speed_edit.get())
                messagebox.showinfo("Success", "Data updated successfully")
            else:
                messagebox.showerror("Error", "Date not found in data")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    tk.Button(edit_window, text="Update Data", command=update_data).grid(row=4, column=3, padx=10, pady=10)

    # Function to view data
    def view_data():
        view_window = tk.Toplevel(edit_window)
        view_window.title("View Data")
        cols = list(data.columns)
        tree = ttk.Treeview(view_window, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for _, row in data.iterrows():
            tree.insert("", "end", values=list(row))
        tree.pack(fill=tk.BOTH, expand=True)

    tk.Button(edit_window, text="View Data", command=view_data).grid(row=4, column=4, padx=10, pady=10)

    # Function to delete data
    def delete_data():
        nonlocal data  # Ensure changes are reflected
        try:
            delete_date = pd.to_datetime(entry_search_date.get(), format='%d-%m-%Y')
            if delete_date in data['Date'].values:
                data = data[data['Date'] != delete_date]
                messagebox.showinfo("Success", "Data deleted successfully")
            else:
                messagebox.showerror("Error", "Date not found in data")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    tk.Button(edit_window, text="Delete Data", command=delete_data).grid(row=4, column=5, padx=10, pady=10)

    # Function to go back to the main menu
    def back_to_main_menu():
        save_data(data, message_label)
        root.destroy()

    tk.Button(edit_window, text="Back", command=back_to_main_menu).grid(row=4, column=6, padx=10, pady=10)
    
    # Update the search_data function to include Average Speed
    def search_data():
        try:
            search_date = pd.to_datetime(entry_search_date.get(), format='%d-%m-%Y')
            if search_date in data['Date'].values:
                record = data[data['Date'] == search_date].iloc[0]
                entry_calories_edit.delete(0, tk.END)
                entry_calories_edit.insert(0, record['Calories (1000kcal)'] * 1000)
                entry_distance_edit.delete(0, tk.END)
                entry_distance_edit.insert(0, record['Distance (Km)'] * 1000)
                entry_steps_edit.delete(0, tk.END)
                entry_steps_edit.insert(0, record['Step count(1000)'] * 1000)
                entry_avg_heart_rate_edit.delete(0, tk.END)
                entry_avg_heart_rate_edit.insert(0, record['Average heart rate (bpm)'])
                entry_max_heart_rate_edit.delete(0, tk.END)
                entry_max_heart_rate_edit.insert(0, record['Max heart rate (bpm)'])
                entry_min_heart_rate_edit.delete(0, tk.END)
                entry_min_heart_rate_edit.insert(0, record['Min heart rate (bpm)'])
                entry_avg_speed_edit.delete(0, tk.END)
                entry_avg_speed_edit.insert(0, record['Average speed (m/s)'])
            else:
                messagebox.showerror("Error", "Date not found in data")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Update the update_data function to include Average Speed
    def update_data():
        try:
            search_date = pd.to_datetime(entry_search_date.get(), format='%d-%m-%Y')
            if search_date in data['Date'].values:
                data.loc[data['Date'] == search_date, 'Calories (1000kcal)'] = float(entry_calories_edit.get()) / 1000
                data.loc[data['Date'] == search_date, 'Distance (Km)'] = float(entry_distance_edit.get()) / 1000
                data.loc[data['Date'] == search_date, 'Step count(1000)'] = float(entry_steps_edit.get()) / 1000
                data.loc[data['Date'] == search_date, 'Average heart rate (bpm)'] = float(entry_avg_heart_rate_edit.get())
                data.loc[data['Date'] == search_date, 'Max heart rate (bpm)'] = float(entry_max_heart_rate_edit.get())
                data.loc[data['Date'] == search_date, 'Min heart rate (bpm)'] = float(entry_min_heart_rate_edit.get())
                data.loc[data['Date'] == search_date, 'Average speed (m/s)'] = float(entry_avg_speed_edit.get())
                messagebox.showinfo("Success", "Data updated successfully")
            else:
                messagebox.showerror("Error", "Date not found in data")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")