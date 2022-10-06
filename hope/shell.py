import Hope

 

while True:
    text = input('Hope >>>')
    result, error = Hope.run(text, '<stdin>')
    
    if text == 'exit':
        break

    if error:
        print(error.as_string())

    
'alo'