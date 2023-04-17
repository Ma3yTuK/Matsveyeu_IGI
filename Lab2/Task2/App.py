import re
import Storage as st
import input_methods as im


def value_input(request):
    string = re.sub('\s+', ' ', im.string_input(request).lstrip())
    return st.value_from_string(string)


def value_print(value):
    print(st.value_to_string(value))


def values_input(request):
    print(request)
    values = list()
    line = input()

    while line != '':
        values.append(st.value_from_string(line))
        line = input()

    return tuple(values)


class App:


    def __init__(self):
        self.storage = st.Storage()


    def add(self):
        try:
            values = values_input('Elements to add:')
            
            if self.storage.add(*values):
                print('Added successfully')
                return

        except:
            pass

        print('Can not add element')


    def remove(self):
        try:
            value = value_input('Element to remove: ')

            if self.storage.remove(value):
                print('Removed successfully')
                return

        except:
            pass

        print('No such elements')


    def find(self):
        try:
            values = values_input('Elements to find:')
            elements = self.storage.find(*values)

            if len(elements) != 0:
                print('Elments found:')

                for element in elements:
                    value_print(element)

                return

        except:
            pass

        print('No such elements')


    def list(self):
        try:
            container = self.storage.list()

            if len(container) != 0:
                print('Container:')

                for element in container:
                    value_print(element)

                return
                
        except:
            pass

        print('Nothing found')


    def grep(self):
        try:
            regex = im.string_input('Regular expression: ')
            matched_elements = self.storage.grep(regex)

            if len(matched_elements) != 0:
                print('Container:')

                for element in matched_elements:
                    value_print(element)

                return

        except:
            pass

        print('Nothing found')


    def save(self):
        try:
            file = im.string_input('File to open: ')

            if self.storage.save(file):
                print('Saved successfully')
                return

        except:
            pass

        print('Can not save file')


    def load(self):
        try:
            file = im.string_input('File to open: ')

            if self.storage.load(file):
                print('Opened successfully')
                return

        except:
            pass

        print('Can not open file')


    def switch(self):
        if im.yes_no_input('Would you like to save current user data?'):
            self.save()

        user_list = self.storage.user_list()
        i = 1
        request = '1) Enter user name\n'

        for user in self.storage.user_list():
            i += 1
            request += '{0}) {1}\n'.format(i, user)

        request += 'Choose user: '
        choice = im.integer_input(request, 1, i)

        if choice == 1:
            user = im.string_input('New user name: ')
        else:
            user = user_list[i]

        self.storage.switch(user)

        if im.yes_no_input('Would you like to load new user data?'):
            self.load()


    def stop(self):
        for user in self.storage.user_list():
            request = 'Would you like to save data of user "{0}"?'.format(user)

            if im.yes_no_input(request):
                self.storage.switch(user)
                self.save()


    def start(self):
        self.storage.switch(im.string_input('New user name: '))

        if im.yes_no_input('Would you like to load new user data?'):
            self.load()

        request = (
            '\n'
            '1) Add\n'
            '2) Remove\n'
            '3) Find\n'
            '4) List\n'
            '5) Grep\n'
            '6) Save\n'
            '7) Load\n'
            '8) Switch\n'
            '9) Exit\n'
            'Choose action: '
        )

        while True:
            match im.integer_input(request, 1, 9):
                case 1:
                    self.add()
                case 2:
                    self.remove()
                case 3:
                    self.find()
                case 4:
                    self.list()
                case 5:
                    self.grep()
                case 6:
                    self.save()
                case 7:
                    self.load()
                case 8:
                    self.switch()
                case 9:
                    self.stop()
