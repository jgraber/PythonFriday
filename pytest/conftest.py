from contact import Phonebook, Datastore
import pytest

@pytest.fixture()
def phonebook(tmpdir):
    "Creates a Phonebook instance"
    store = Datastore(tmpdir)
    phonebook = Phonebook(store)
    yield phonebook
    phonebook.clear() 