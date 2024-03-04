import random


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    pass

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret_word = random.choice(words)
    attempts = 1
    while True:
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret_word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        attempts += 1
        if bulls == len(secret_word):
            return attempts


def ask(prompt: str, valid: list[str] = None) -> str:
    pass

def inform(format_string: str, bulls: int, cows: int) -> None:
    pass


if __name__ == "__main__":
    print("Run bullscows.py ...")