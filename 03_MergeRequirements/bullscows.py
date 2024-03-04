import random
import argparse
import urllib


def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    for i, c in enumerate(guess):
        if c == secret[i]:
            bulls += 1
        elif c in secret:
            cows += 1
    return bulls, cows

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret_word = random.choice(words)
    attempts = 1
    print("Игра началась. Слово загадано")
    print("Если захотите сдаться, введите: -")
    while True:
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret_word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        attempts += 1
        if bulls == len(secret_word):
            print("Победа!!!")
            return attempts
        elif guess == "-":
            print(f"Поражение... Загаданным словов было: {secret_word}")
            return attempts


def ask(prompt: str, valid: list[str] = None) -> str:
    user_input = input(prompt)
    if valid and user_input not in valid:
        if user_input == "-":
            return user_input
        print("Неверно. Попробуйте снова.")
        return ask(prompt, valid)
    return user_input

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

def download_dictionary(url: str, length: int) -> list[str]:
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
        words = [word for word in data.split("\n") if len(word) == length]
    return words

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("words", type=str)
    parser.add_argument("length", default=5, type=int, nargs="?")
    bullscows_args = parser.parse_args()
    
    if bullscows_args.words.startswith("http"):
        words = download_dictionary(bullscows_args.words, bullscows_args.length)
    else:
        with open(bullscows_args.words, "r") as file:
            words = [word.strip() for word in file if len(word.strip()) == bullscows_args.length]

    attempts = gameplay(ask, inform, words)
    print(f"Игра окончена. Количество попыток: {attempts}")

if __name__ == "__main__":
    main()