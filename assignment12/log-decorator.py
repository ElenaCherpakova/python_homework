import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))

# Task 1: Writing and Testing a Decorator
def logger_decorator(func):  # The decorator: takes the function
        def wrapper(*args, **kwargs):  # The wrapper: runs the function with extra behavior
                result = func(*args, **kwargs)  
                func_name = func.__name__
                pos_args = args if args else 'none'
                kw_args = kwargs if kwargs else 'none'
                
                log_message = (
                    f"function {func_name}\n"
                    f"positional parameters: {pos_args}\n"
                    f"keyword parameters: {kw_args}\n"
                    f"return: {result}"
                )
                logger.log(logging.INFO, log_message)

                return result
        return wrapper

# Declare a function that takes no parameters and returns nothing. Maybe it just prints "Hello, World!". Decorate this function with your decorator.

@logger_decorator
def hello_world():
    print('Hello World')

# Declare a function that takes a variable number of positional arguments and returns True. Decorate this function with your decorator.
@logger_decorator
def second_func(*args):
    return True


# Declare a function that takes no positional arguments and a variable number of keyword arguments, and that returns logger_decorator. Decorate this function with your decorator.
@logger_decorator
def third_func(**kwargs):
    return logger_decorator

#  call each of these three functions
hello_world()
second_func('test', 'test2', 1)
third_func(key1='test', key2='test2')