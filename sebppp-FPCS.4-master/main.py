from main_menu import main_menu

def main():
    start = main_menu()
    selected_mode = None
    while selected_mode is None:
        mode = start.mode_select()
        if mode == 1:
            start.menu_diary()
        elif mode == 2:
            start.search_by_city()
        elif mode == 3:
            start.manually_add_brewery()
        elif mode == 4:
            start.menu_send_cocktail()

main()

