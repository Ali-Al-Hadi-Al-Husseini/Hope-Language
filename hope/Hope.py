from Interpreter_tools.Interpreter import run
from sys import argv

if __name__ == "__main__":
    try:
        file_name = argv[1]
    except IndexError:
        file_name = None
    
    if file_name is not None:
        with open(file_name,'r') as file:
            script = str(file.read())

        result , error = run(script,file_name)
        if error:
            print(error.as_string())

    else :
        while True:
            text = input('Hope >>>')
            result, error = run(text, '<stdin>')
            
            if text.strip() == '':
                continue
            
            if text == 'exit':
                break
            
            if error:
                print(error.as_string())

