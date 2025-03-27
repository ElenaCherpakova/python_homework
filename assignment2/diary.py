# Task 1
import traceback

try:
    with open('diary.txt', 'a') as file:
        prompt = 'What happend today? '
        while True:
            entry = input(prompt)
            prompt = 'What else? '  
            file.write(entry + '\n')
            if entry == 'done for now':
                break
            
except Exception as e:
   trace_back = traceback.extract_tb(e.__traceback__)
   stack_trace = list()
   for trace in trace_back:
      stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
   print(f"An exception occurred. Exception type: {type(e).__name__}")
   message = str(e)
   if message:
      print(f"Exception message: {message}")
   print(f"Stack trace: {stack_trace}")