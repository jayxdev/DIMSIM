from .setup import tk
from .input import get_add_data
from .editor import edit_data
from .visualization import visualization_dash

def main_menu(root, message_label):
    # Load images for buttons
    add_image = tk.PhotoImage(file="c:/Users/JAYDEV/Desktop/python lab/python project-4/app/img/add-database.png")
    edit_image = tk.PhotoImage(file="c:/Users/JAYDEV/Desktop/python lab/python project-4/app/img/edit.png")
    plot_image = tk.PhotoImage(file="c:/Users/JAYDEV/Desktop/python lab/python project-4/app/img/laptop.png")

    # Create buttons with images
    add_button = tk.Button(root, image=add_image, command=lambda :get_add_data(root, message_label))
    edit_button = tk.Button(root, image=edit_image, command=lambda : edit_data(root, message_label))
    plot_button = tk.Button(root, image=plot_image, command=lambda :visualization_dash(root,message_label))

    # Place buttons on the grid
    add_button.grid(row=4, column=0, padx=10, pady=10)
    edit_button.grid(row=4, column=1, padx=10, pady=10)
    plot_button.grid(row=4, column=2, padx=10, pady=10)

    # Keep references to the images to prevent them from being garbage collected
    add_button.image = add_image
    edit_button.image = edit_image
    plot_button.image = plot_image
    # Run the main loop
    root.mainloop()