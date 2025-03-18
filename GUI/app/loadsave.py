from .setup import data_file, pd

# Function to save data to CSV
def save_data(data,message_label):
    if not data.empty:
        data.to_csv(data_file, index=False)
        message_label.config(text="Data saved to CSV successfully!", fg="green")
    else:
        message_label.config(text="No data to save", fg="red")

# Function to load data from CSV
def load_data(message_label):
    try:
        data = pd.read_csv(data_file)
        data['Date'] = pd.to_datetime(data['Date'])
        message_label.config(text="Data loaded from CSV successfully!\nEntries Loaded:"+str(data.shape[0]), fg="green")
    except FileNotFoundError:
        message_label.config(text="No CSV file found to load data", fg="red")
    return data

