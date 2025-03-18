from .loadsave import load_data
from .setup import clear_window, tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns

def visualization_dash(root, message_label):
    data = load_data(message_label)
    clear_window(root, message_label)
    
    root.title("Data Visualization Dashboard")
    notebook = tk.ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky='nsew')

    # Helper function to add plots
    def add_plot_to_frame(frame, plot_func):
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        plot_func(data, ax)  # Pass data and axis to the plot function
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    # Create frames for each tab
    frames = [tk.Frame(notebook) for _ in range(5)]
    titles = [
        'Activity Trends',
        'Step Count vs Calories',
        'Days Below 3K Steps',
        'Heart Rate Variability',
        'Cumulative Steps and Distance',
    ]
    for frame, title in zip(frames, titles):
        notebook.add(frame, text=title)

    # Define plot functions
    def plot_data1(data, ax):
        sns.lineplot(x='Date', y='Calories (1000kcal)', data=data, label='Calories (1000kcal)', ax=ax, color='r')
        sns.lineplot(x='Date', y='Distance (Km)', data=data, label='Distance (Km)', ax=ax, color='b')
        sns.lineplot(x='Date', y='Step count(1000)', data=data, label='Step Count(1000)', ax=ax, color='g')
        ax.set_title('Activity Trends Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True)

    def plot_data2(data, ax):
        normal_pace_threshold = 0.5  # m/s
        high_pace_threshold = 0.6   # m/s
        normal_pace_data = data[data['Average speed (m/s)'] < normal_pace_threshold]
        high_pace_data = data[data['Average speed (m/s)'] >= high_pace_threshold]
        sns.scatterplot(x='Step count(1000)', y='Calories (1000kcal)', data=normal_pace_data, color='blue', alpha=0.5, label='Normal Pace', ax=ax)
        sns.scatterplot(x='Step count(1000)', y='Calories (1000kcal)', data=high_pace_data, color='red', alpha=0.5, label='High Pace', ax=ax)
        ax.set_title('Step Count vs Calories: Normal Pace vs High Pace')
        ax.set_xlabel('Step Count(1000)')
        ax.set_ylabel('Calories (kcal)')
        ax.legend()
        ax.grid(True)

    def plot_data3(data, ax):
        holiday_threshold = 3  # 3K steps
        days_below_3000 = data[data['Step count(1000)'] < holiday_threshold]
        days_below_3000 = days_below_3000.copy()
        days_below_3000['Day of Week'] = days_below_3000['Date'].dt.day_name()
        day_frequency = days_below_3000['Day of Week'].value_counts()
        sns.barplot(x=day_frequency.index, y=day_frequency.values, ax=ax)
        ax.set_title('Frequency of Days with Step Counts Below 3K')
        ax.set_xlabel('Day of the Week')
        ax.set_xticks(range(len(day_frequency)))
        ax.set_xticklabels(day_frequency.index, rotation=45)
        ax.set_xticklabels(day_frequency.index, rotation=45)
        ax.grid(True)

    def plot_data4(data, ax):
        sns.boxplot(data=data[['Average heart rate (bpm)', 'Max heart rate (bpm)', 'Min heart rate (bpm)']], ax=ax)
        ax.set_xticks(range(3))
        ax.set_xticklabels(['Average', 'Max', 'Min'])
        ax.set_ylabel('Heart Rate (bpm)')
        ax.set_xticklabels(['Average', 'Max', 'Min'])

    def plot_data5(data, ax):
        data['Cumulative Steps(Thousand)'] = data['Step count(1000)'].cumsum()
        data['Cumulative Distance (Km)'] = data['Distance (Km)'].cumsum()
        ax.plot(data['Date'], data['Cumulative Steps(Thousand)'], label='Cumulative Steps(Thousand)', color='orange')
        ax.plot(data['Date'], data['Cumulative Distance (Km)'], label='Cumulative Distance (Km)', color='cyan')
        ax.set_title('Cumulative Steps and Distance Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Value')
        ax.legend()
        ax.grid(True)

    # Add each plot to its corresponding frame
    plot_functions = [plot_data1, plot_data2, plot_data3, plot_data4, plot_data5]
    for frame, plot_func in zip(frames, plot_functions):
        add_plot_to_frame(frame, plot_func)
