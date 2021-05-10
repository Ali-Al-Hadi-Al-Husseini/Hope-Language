import Hope


while True:
    text = input('Hope >>>')
    result, error = Hope.Run(text)

    if error:
        print(error.as_string())
    else:
        print(result)
