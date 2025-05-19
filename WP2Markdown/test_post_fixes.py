import pytest
from transform_posts import cleanup_post

def test_fix_date():
    input = """
---
date: "2023-12-31"
---

# Happy new years eve!
"""

    expected = """
---
date: 2023-12-31 20:00:00
---

# Happy new years eve!
"""

    output = cleanup_post(input)
    assert expected == output


def test_fix_code():
    input = """
# Happy new years eve!
```
a = 1
b = 2
```
"""

    expected = """
# Happy new years eve!
``` py3
a = 1
b = 2
```
"""

    output = cleanup_post(input)
    assert expected == output


def test_fix_images():
    input = """
![Image title](images/dummy.png)
"""

    expected = """
![Image title](dummy.png)
"""

    output = cleanup_post(input)
    assert expected == output


def test_add_more():
    input = """
abc

This post is part of my journey to learn Python. You find the code for this post in my PythonFriday repository on GitHub.

"""

    expected = """
abc

<!-- more -->

"""

    output = cleanup_post(input)
    assert expected == output


def test_fix_title():
    input = """
---
title: "Python Friday #1: Let’s Learn Python"
---
This post is part ...

"""

    expected = """
---
title: "#1: Let’s Learn Python"
---
This post is part ...

"""

    output = cleanup_post(input)
    assert expected == output


def test_fix_links_to_python_friday_posts():
    input = """

[a dashboard for FastAPI](https://improveandrepeat.com/2024/08/python-friday-238-create-a-dashboard-for-fastapi/)

[Northwind database](https://improveandrepeat.com/2021/05/python-friday-73-first-steps-with-sqlalchemy#Northwind)

[database](https://improveandrepeat.com/2021/05/python-friday-73-first-steps?swcfpc=1)

[see docker containers](https://improveandrepeat.com/2021/11/dev-container-for-sql-server-2019/)

[still ](https://improveandrepeat.com/2024/04/python-friday-222-filter-the-tasks-in-the-fastapi-application/). [post](https://improveandrepeat.com/2024/08/python-friday-240-asynchronous-sqlalchemy-with-fastapi/).
"""

    expected = """

[a dashboard for FastAPI](./../../2024/238-create-a-dashboard-for-fastapi/238-create-a-dashboard-for-fastapi.md)

[Northwind database](./../../2021/73-first-steps-with-sqlalchemy/73-first-steps-with-sqlalchemy.md)

[database](./../../2021/73-first-steps/73-first-steps.md)

[see docker containers](https://improveandrepeat.com/2021/11/dev-container-for-sql-server-2019/)

[still ](./../../2024/222-filter-the-tasks-in-the-fastapi-application/222-filter-the-tasks-in-the-fastapi-application.md). [post](./../../2024/240-asynchronous-sqlalchemy-with-fastapi/240-asynchronous-sqlalchemy-with-fastapi.md).
"""

    output = cleanup_post(input)
    assert expected == output


def test_add_missing_more():
    input = """
---
title: A B C
---
## A

aaa

## B

bbb
"""

    expected = """
---
title: A B C
---
<!-- more -->
## A

aaa

## B

bbb
"""

    output = cleanup_post(input)
    assert expected == output