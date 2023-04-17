import re

def value_from_string(value_string: str):
    value_list = list()
    for string in re.split(' ', value_string):
        try:
            value_list.append(int(string))
        except:
            value_list.append(string)
    if len(value_list) == 1:
        return value_list[0]
    return tuple(value_list[:-1])

def value_to_string(value):
    if type(value) != tuple:
        return str(value)
    value_list = list()
    for value_part in value:
        value_list.append(str(value_part))
    return ' '.join(value_list) + ' '

class Storage:

    def __init__(self):
        self.user_dict = dict[str, set]()
        self.active_user = None

    def user_list(self):
        return list(self.user_dict)

    def add(self, *keys):
        if self.active_user == None:
            return False
        container = self.user_dict[self.active_user]
        container |= set(keys)
        return True

    def remove(self, key):
        if self.active_user == None:
            return False
        container = self.user_dict[self.active_user]
        if key not in container:
            return False
        container.remove(key)
        return True

    def find(self, *keys):
        if self.active_user == None:
            return None
        container = self.user_dict[self.active_user]
        return container&set(keys)

    def list(self):
        if self.active_user == None:
            return None
        container = self.user_dict[self.active_user]
        return list(container)

    def grep(self, regex_str):
        if self.active_user == None:
            return None
        container = self.user_dict[self.active_user]
        regex = re.compile(regex_str)
        matched_keys = list()
        for element in container:
            if regex.fullmatch(value_to_string(element)) != None:
                matched_keys.append(element)
        return matched_keys

    def save(self, path):
        if self.active_user == None:
            return False
        container = self.user_dict[self.active_user]
        with open(path, 'w') as file:
            for key in container:
                file.write(value_to_string(key)+'\n')
        return True

    def load(self, path):
        if self.active_user == None:
            return False
        container = self.user_dict[self.active_user]
        with open(path) as file:
            for line in file:
                container.add(value_from_string(line[:-1]))
        return True

    def switch(self, user):
        if user not in self.user_dict:
            self.user_dict[user] = set()
        self.active_user = user
        