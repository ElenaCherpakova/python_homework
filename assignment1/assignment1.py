# Task 1
def hello():
    return f'Hello!'

# Task 2
def greet(name):
    return f'Hello, {name}!'

# Task 3
def calc(a, b, c='multiply'):
    result = None
    try:
        match c:
            case 'add':
                result = a + b
            case 'subtract':
                result = a - b
            case 'multiply':
                result = a * b
            case 'divide':
                result = a / b
            case 'modulo':
                result = a % b
            case 'int_divide':
                result = a // b
            case 'power':
                result = a ** b
            case _:
                raise ValueError(f'Invalid operation {c}') 
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    return result

# Task 4
def data_type_conversion(value, type):
    result = None
    try:
        match type:
            case 'float':
                result = float(value)
            case 'str':
                result = str(value)
            case 'int':
                result = int(value)
            case _:
                raise ValueError(f'Invalid type {type}')
    except ValueError:
        return f"You can't convert {value} into a {type}."   
    return result
    
# Task 5
def grade(*args):
    if len(args) == 0:
        return 'No grades were provided'
    try:
        total = sum(args)
        average = total / len(args)
        if average >= 90:
            return 'A'
        if 80 <= average <= 89:
            return 'B'
        if 70 <= average <= 79:
            return 'C'
        if 60 <= average <= 69:
            return 'D'
        else:
            return 'F'
    except TypeError:
        return 'Invalid data was provided.'
        

# Task 6
def repeat(string, count):
    return ''.join(string for _ in range(count))

# Task 7
def student_scores(positional, **kwargs):
    if positional == 'mean':
        total = sum(kwargs.values())
        return total / len(kwargs)
    if positional == 'best':    
        return max(kwargs, key=kwargs.get) 

# Task 8
def titleize(string):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
    words = string.split()
    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1 or word not in little_words:
            words[i] = word.capitalize()
    return ' '.join(words)


# Task 9
def hangman(secret, guess):
    res = ''
    for char in secret:
        if char in guess:
            res += char
        else:
            res += '_'
    return res

#Task 10
def pig_latin(string):
    vowels = 'aeiou'
    words = string.split()
    res = []
    for letters in words:
        if letters[0] in vowels:
            res.append(letters + 'ay')
        else:
            i = 0
            while i < len(letters) and letters[i] not in vowels:                
                i += 1
                if i < len(letters) and i > 0 and letters[i-1] == 'q' and letters[i] == 'u':
                    i += 1
            res.append(letters[i:] + letters[:i] + 'ay')
    return ' '.join(res)
