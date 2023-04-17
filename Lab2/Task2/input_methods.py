def string_input(request):
    while True:
        string = input(request)
        if len(string) != 0:
            return string
        print('Invalid input')

def integer_input(request, lowest_value, highest_value):
    while True:
        try:
            result = int(input(request))
            if lowest_value <= result <= highest_value:
                return result
        except:
            pass
        print('Invalid input!')

def yes_no_input(request):
    request += (
        '\n'
        '1) Yes\n'
        '2) No\n'
        'Choose action: '
    )
    choice = integer_input(request, 1, 2)
    if choice == 1:
        return True
    else:
        return False