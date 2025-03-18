from app.main import main_menu
from app.setup import get_window
from app.login import run_login_system

if __name__ == "__main__":
    root, message_label=get_window()
    run_login_system(root, message_label)
    while True:
        root, message_label=get_window()
        main_menu(root, message_label) 