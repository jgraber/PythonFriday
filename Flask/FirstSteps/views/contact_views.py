import flask
from flask import render_template, request
from Flask.viewmodels.contact_viewmodel import ContactViewModel

blueprint = flask.Blueprint('contact', __name__, template_folder='templates')

@blueprint.route('/contact', methods=['GET'])
def contact_form():
    return render_template('contact/contact.html')


@blueprint.route('/contact', methods=['POST'])
def contact_post():
    vm = ContactViewModel()
    vm.validate()

    if vm.error:
        return  render_template('contact/contact.html', **vm.to_dict())

    print(vm)

    resp = flask.redirect('/thanks')
    return resp


@blueprint.route('/thanks')
def thanks():    
    return render_template('contact/thankyou.html')
