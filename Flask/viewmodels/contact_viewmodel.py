import flask

class ContactViewModel():
    def __init__(self):
        """ Create the ViewModel with the form data from the request """
        request = flask.request
        self.name = request.form['name']
        self.email = request.form['email']
        self.message = request.form['message']
        self.error = None

    def validate(self):
        """ validate the form """
        if not self.name or not self.name.strip():
            self.error = 'name is missing'        
        if not self.email or not self.email.strip() or '@' not in self.email:
            self.error = 'email is missing' 
        if not self.message or not self.message.strip():
            self.error = 'message is missing' 

    def __str__(self):
        """ create a readable output for the data """
        return f"{self.name} [{self.email}]: {self.message}"

    def to_dict(self):
        """ turn this object into a dictionary """
        return self.__dict__