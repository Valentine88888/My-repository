def introduction():
    print("Ласкаво просимо до текстової пригоди!")
    print("Ви будете робити вибори, які вплинуть на хід історії.")
    print("Удачі!")

introduction()
def start_adventure():
    print("Ви знаходитесь в темному лісі. Ви можете піти наліво або направо.")
    choice = input("Виберіть (ліво/право): ").lower()
    if choice == "ліво":
        left_path()
    elif choice == "право":
        right_path()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        start_adventure()

def left_path():
    print("Ви натрапили на старий замок. Ви можете ввійти або пройти мимо.")
    choice = input("Виберіть (ввійти/пройти): ").lower()
    if choice == "ввійти":
        enter_castle()
    elif choice == "пройти":
        continue_path()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        left_path()

def right_path():
    print("Ви знайшли скарб. Вітаємо! Гра завершена.")
    exit()

def enter_castle():
    print("Ви зустріли дракона. Ви можете битися або втекти.")
    choice = input("Виберіть (битися/втекти): ").lower()
    if choice == "битися":
        fight_dragon()
    elif choice == "втекти":
        print("Ви втекли з замку. Гра завершена.")
        exit()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        enter_castle()

def continue_path():
    print("Ви йдете далі по лісу і натрапляєте на мирне село. Гра завершена.")
    exit()

def fight_dragon():
    print("Ви перемогли дракона! Вітаємо! Гра завершена.")
    exit()

start_adventure()
points = 0

def update_points(value):
    global points
    points += value
    print(f"Ваші бали: {points}")

def start_adventure():
    global points
    points = 0
    print("Ви знаходитесь в темному лісі. Ви можете піти наліво або направо.")
    choice = input("Виберіть (ліво/право): ").lower()
    if choice == "ліво":
        update_points(10)
        left_path()
    elif choice == "право":
        update_points(20)
        right_path()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        start_adventure()

# Всі інші функції залишаються такими ж, як раніше

start_adventure()
def start_adventure():
    global points
    points = 0
    choose_difficulty()
    print("Ви знаходитесь в темному лісі. Ви можете піти наліво або направо.")
    choice = input("Виберіть (ліво/право): ").lower()
    if choice == "ліво":
        update_points(10)
        left_path()
    elif choice == "право":
        update_points(20)
        right_path()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        start_adventure()

# Всі інші функції залишаються такими ж, як раніше

start_adventure()
import time
import threading

def input_with_timeout(prompt, timeout):
    print(prompt, end='', flush=True)
    result = [None]

    def timed_input():
        result[0] = input()

    thread = threading.Thread(target=timed_input)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print("\nЧас вичерпано!")
        return None
    return result[0]

def start_adventure():
    global points
    points = 0
    choose_difficulty()
    print("Ви знаходитесь в темному лісі. Ви можете піти наліво або направо.")
    choice = input_with_timeout("Виберіть (ліво/право): ", 10)
    if choice is None:
        print("Ви не встигли зробити вибір. Гра завершена.")
        exit()
    elif choice == "ліво":
        update_points(10)
        left_path()
    elif choice == "право":
        update_points(20)
        right_path()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        start_adventure()

# Всі інші функції залишаються такими ж, як раніше

start_adventure()
