class Datastore:
    def __init__(self, directory=None):
        self.collection = {}
        
    def store(self):
        return self.collection


class Phonebook:
    def __init__(self, storage):
        self.numbers = storage.store()
        print("Phonebook created")

    def add(self, name, number):
        self.numbers[name] = number
    
    def lookup(self, name):
        return self.numbers[name]
    
    def names(self):
        return set(self.numbers.keys())

    def clear(self):
        print("Phonebook removed")