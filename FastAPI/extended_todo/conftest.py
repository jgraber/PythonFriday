import os
import shutil

def pytest_sessionstart(session):
    """
    Removes the ./db/test_db.sqlite database at the start of the test run
    """
    # print("$--$" * 10)
    db_file = os.path.join(
        os.path.dirname(__file__),
        '.',
        'db',
        'test_db.sqlite')
    
    template_file = os.path.join(
        os.path.dirname(__file__),
        '.',
        'db',
        'template_test.sqlite')
    
    if os.path.isfile(db_file):
        os.remove(db_file)
    
    shutil.copy2(template_file, db_file)
    # print(f"DB {db_file} replaced with template")
    print(f"DB {db_file} removed")