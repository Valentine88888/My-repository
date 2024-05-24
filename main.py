import random


def load_words():
    # Тут список слів, які можна вгадувати
    return ["світло", "дружба", "мова", "книга", "земля", "музика", "сонце", "гараж","свято"]


def get_random_word(word_list):
    return random.choice(word_list).upper()


def display_feedback(guess, target):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == target[i]:
            feedback.append(f"{guess[i]} (вірно)")
        elif guess[i] in target:
            feedback.append(f"{guess[i]} (не на місці)")
        else:
            feedback.append(f"{guess[i]} (не в слові)")
    return feedback


def play_game():
    words = load_words()
    target_word = get_random_word(words)
    attempts = 6

    print("Ласкаво просимо до гри 'Worldl'")
    print("Вам потрібно вгадати слово з 6 спроб.")

    while attempts >0:
        guess = input("Введіть ваше слово: ").upper()

        if len(guess) != len(target_word):
            print(f"Слово повинно бути довжиною {len(target_word)} символів.")
            continue

        if guess == target_word:
            print("Вітаємо! Ви вгадали слово!")
            break

        feedback = display_feedback(guess, target_word)
        print(" ".join(feedback))
        attempts -= 1

        if attempts == 0:
            print(f"Ви програли. Загадане слово було: {target_word}")


if __name__ == "__main__":
    play_game()

