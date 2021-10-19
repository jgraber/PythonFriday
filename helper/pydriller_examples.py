from pydriller import Repository
import pprint
pp = pprint.PrettyPrinter()
    
def traverse_commits():
    # for commit in Repository('https://github.com/jgraber/PythonFriday').traverse_commits():
    for commit in Repository('..\..\PythonFriday').traverse_commits():
        print(f"{commit.hash} - {commit.committer_date} - {commit.author.name} - {commit.msg}")
        for file in commit.modified_files:
            print(f'  - {file.filename} has changed ({file.change_type.name})')
            
        print("")
        
    # 18236534aa9c43de3e703c8a6a23395812b6d72a - 2021-06-14 00:04:26+02:00 - Johnny Graber - add constraints, indexes and default values
    #   - 5867629bf749_add_created_date_with_default_value_to_.py has changed (ADD)
    #   - cd496010379c_remove_constraints_for_examples.py has changed (ADD)
    #   - dff2171f8b62_create_index_for_employee_last_name_and_.py has changed (ADD)
    #   - e4887a8bedc7_add_index_to_publisher_name.py has changed (ADD)
    #   - book.py has changed (MODIFY)
    #   - employee.py has changed (MODIFY)
    #   - publisher.py has changed (MODIFY)

    # 3adbf91ab605a4ecf5b1bcc3fe1a4bccdc2729b2 - 2021-06-17 19:57:27+02:00 - Johnny Graber - add example for automap and SQL Server
    #   - sqlalchemy_orm_automap_sqlserver.py has changed (ADD)

    # e179d7750cd703b60a6ea0cdb03a174bd823e104 - 2021-10-06 21:49:39+02:00 - Johnny Graber - add example for PrettyPrinter
    #   - prettyprinter_example.py has changed (ADD)

def count_commits():
    print("\n\n\n\n=========================================\nCommitsCount:")

    from pydriller.metrics.process.commits_count import CommitsCount
    metric = CommitsCount(path_to_repo='..\..\PythonFriday',
                        from_commit='42722d558b3175a0c60ba7e513b7786ae6dbb591',
                        to_commit='36425461ed2e42883ee7935af79cb620218f88b2')
    files = metric.count()
    pp.pprint(files)

    # {'SQLAlchemy\\Core\\sqlalchemy_core_crud.py': 2,
    #  'SQLAlchemy\\Core\\sqlalchemy_core_filters.py': 3,
    #  'SQLAlchemy\\Core\\sqlalchemy_core_relationships.py': 1,
    #  'SQLAlchemy\\ORM\\app_with_db.py': 2,
    #  'SQLAlchemy\\ORM\\data\\__all_models.py': 2,
    #  'SQLAlchemy\\ORM\\data\\author.py': 1,
    #  'SQLAlchemy\\ORM\\data\\book.py': 2,
    #  'SQLAlchemy\\ORM\\data\\book_author.py': 1,
    #  'SQLAlchemy\\ORM\\data\\book_details.py': 1,
    #  'SQLAlchemy\\ORM\\data\\db_session.py': 1,
    #  'SQLAlchemy\\ORM\\data\\employee.py': 2,
    #  'SQLAlchemy\\ORM\\data\\modelbase.py': 1,
    #  'SQLAlchemy\\ORM\\data\\publisher.py': 1,
    #  'SQLAlchemy\\ORM\\db\\Northwind_small.sqlite': 1,
    #  'SQLAlchemy\\ORM\\sqlalchemy_orm_crud.py': 1,
    #  'SQLAlchemy\\ORM\\sqlalchemy_orm_filters.py': 1,
    #  'SQLAlchemy\\ORM\\sqlalchemy_orm_relationships.py': 1}

def count_contributors():
    print("\n\n\n\n=========================================\nContributorsCount:")

    from pydriller.metrics.process.contributors_count import ContributorsCount
    metric = ContributorsCount(path_to_repo='..\..\PythonFriday',
                            from_commit='42722d558b3175a0c60ba7e513b7786ae6dbb591',
                            to_commit='36425461ed2e42883ee7935af79cb620218f88b2')
    count = metric.count()
    minor = metric.count_minor()
    print('Number of contributors per file:')
    pp.pprint(count)
    print('Number of "minor" contributors per file:')
    pp.pprint(minor)


def count_lines():
    print("\n\n\n\n=========================================\nLinesCount:")
    from pydriller.metrics.process.lines_count import LinesCount
    metric = LinesCount(path_to_repo='..\..\PythonFriday',
                        from_commit='42722d558b3175a0c60ba7e513b7786ae6dbb591',
                        to_commit='36425461ed2e42883ee7935af79cb620218f88b2')

    added_count = metric.count_added()
    removed_count = metric.count_removed()

    print('Total lines added per file:')
    pp.pprint(added_count)
    print('Total lines removed per file:')
    pp.pprint(removed_count)


if __name__ == '__main__':
    # traverse_commits()
    count_commits()
    # count_contributors()
    # count_lines()