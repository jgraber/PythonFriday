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

@pytest.mark.skip(reason="work in progress")
def test_add_contact_to_phonebook(phonebook):
    phonebook.add("Andy", 12345)    
    assert "Andy" in phonebook.names()


def test_lookup_contact_to_phonebook(phonebook):
    phonebook.add("Mandy", 45678)    
    assert 45678 == phonebook.lookup("Mandy")

@pytest.mark.xfail(reason="1 is never 2", strict=True)
def test_should_fail():
    assert 1 == 2
    
@pytest.mark.wip
def test_lookup_should_not_throw_error_when_key_missing(phonebook):
    # phonebook.lookup("missing")
    pass
