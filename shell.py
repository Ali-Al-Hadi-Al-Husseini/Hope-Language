import Hope

 

while True:
    text = input('Hope >>>')
    result, error = Hope.Run(text, '<stdin>')

    if text == 'exit':
        break

    if error:
        print(error.as_string())

    else:
        print(result)
