def multiline_input(request):
    print(request)
    result = ''
    line = input()

    while line != '':
        result += line
        line = input()

    return result

def integer_input(request, lowest_value, highest_value):
    while True:

        try:
            result = int(input(request))

            if lowest_value <= result <= highest_value:
                return result

        except:
            pass
        
        print('Invalid input!')