from .setup import pd, tk, clear_window, get_window
from datetime import datetime
from .loadsave import save_data, load_data

def get_add_data(root, message_label):
    # Clear the window
    clear_window(root, message_label)
    
    # Create and place the input fields and labels
    tk.Label(root, text="Date (DD-MM-YYYY)").grid(row=0, column=0, padx=10, pady=5)
    entry_date = tk.Entry(root)
    entry_date.grid(row=0, column=1, padx=10, pady=5)
    entry_date.insert(0, datetime.now().strftime('%d-%m-%Y'))
    
    tk.Label(root, text="Calories (kcal)").grid(row=1, column=0, padx=10, pady=5)
    entry_calories = tk.Entry(root)
    entry_calories.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(root, text="Distance (m)").grid(row=2, column=0, padx=10, pady=5)
    entry_distance = tk.Entry(root)
    entry_distance.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(root, text="Step count").grid(row=3, column=0, padx=10, pady=5)
    entry_steps = tk.Entry(root)
    entry_steps.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(root, text="Max Heart Rate(bpm)").grid(row=0, column=2, padx=10, pady=5)
    entry_max_heart_rate = tk.Entry(root)
    entry_max_heart_rate.grid(row=0, column=3, padx=10, pady=5)
    
    tk.Label(root, text="Min Heart Rate(bpm)").grid(row=1, column=2, padx=10, pady=5)
    entry_min_heart_rate = tk.Entry(root)
    entry_min_heart_rate.grid(row=1, column=3, padx=10, pady=5)
    
    tk.Label(root, text="Avg Heart Rate(bpm)").grid(row=2, column=2, padx=10, pady=5)
    entry_avg_heart_rate = tk.Entry(root)
    entry_avg_heart_rate.grid(row=2, column=3, padx=10, pady=5)

    tk.Label(root, text="Avg Speed (m/s)").grid(row=3, column=2, padx=10, pady=5)
    entry_avg_speed = tk.Entry(root)
    entry_avg_speed.grid(row=3, column=3, padx=10, pady=5)

    # Function to add data to the DataFrame
    def add_data():
        input = {
            'date': pd.to_datetime(entry_date.get(), format='%d-%m-%Y'),
            'calories': entry_calories.get(),
            'distance': entry_distance.get(),
            'steps': entry_steps.get(),
            'avg_heart_rate': entry_avg_heart_rate.get(),
            'max_heart_rate': entry_max_heart_rate.get(),
            'min_heart_rate': entry_min_heart_rate.get(),
            'avg_speed': entry_avg_speed.get()
        }
        data = load_data(message_label)
        if all(input.values()):
            new_data = pd.DataFrame([[input["date"], float(input["calories"])/1000, float(input["distance"])/1000, float(input["steps"])/1000, float(input["avg_heart_rate"]), float(input["max_heart_rate"]), float(input["min_heart_rate"]), float(input["avg_speed"])]], 
                        columns=['Date', 'Calories (1000kcal)', 'Distance (Km)', 'Step count(1000)', 'Average heart rate (bpm)', 'Max heart rate (bpm)', 'Min heart rate (bpm)', 'Average speed (m/s)'])
            data = pd.concat([data, new_data], ignore_index=True)
            save_data(data, message_label)
            message_label.config(text="Data added successfully!\nTotal Entries:" + str(data.shape[0]), fg="green")
        else:
            message_label.config(text="Please fill all fields", fg="red")
    tk.Button(root, text="Add Data", command=add_data).grid(row=4, column=2, columnspan=2, padx=10, pady=5)
    
    # Back to main menu
    def back_to_main_menu():
        root.destroy()
    
    tk.Button(root, text="Back", command=back_to_main_menu).grid(row=4, column=4, columnspan=2, padx=10, pady=5)
    tk.mainloop()
