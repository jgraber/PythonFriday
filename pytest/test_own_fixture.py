# from contact import Phonebook, Datastore

# def test_add_contact_to_phonebook():
#     store = Datastore()
#     phonebook = Phonebook(store)
#     phonebook.add("Andy", 12345)    
#     assert "Andy" in phonebook.names()


# def test_lookup_contact_to_phonebook():
#     store = Datastore()
#     phonebook = Phonebook(store)
#     phonebook.add("Mandy", 45678)    
#     assert 45678 == phonebook.lookup("Mandy")

# from contact import Phonebook, Datastore
# import pytest

# @pytest.fixture()
# def phonebook(tmpdir):
#     store = Datastore(tmpdir)
#     phonebook = Phonebook(store)
#     yield phonebook
#     phonebook.clear() 

import pytest


def test_add_contact_to_phonebook(phonebook):
    phonebook.add("Andy", 12345)    
    assert "Andy" in phonebook.names()


def test_lookup_contact_to_phonebook(phonebook):
    phonebook.add("Mandy", 45678)    
    assert 45678 == phonebook.lookup("Mandy")
