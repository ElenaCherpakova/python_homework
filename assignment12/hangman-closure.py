# Task 4: Closure Practice
def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())
        display = ''
        for char in secret_word:
            if char in guesses:
                display += char
            else:
                display += '_'
        print(display)
        return '_' not in display
    return hangman_closure


secret_word = input('Provide a secret word: ')
game = make_hangman(secret_word.lower())

finished = False
while not finished:
    guess_letter = input('Guess a letter: ')
    result = game(guess_letter)

    if result:
        print('Congrat you guessed a word!')
        finished = True
