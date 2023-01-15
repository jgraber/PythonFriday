Small code snippets go directly in the notebook


```python
def add(a, b):
    return a + b
```


```python
add(1, 2)
```




    3



Larger code goes into a regular Python file


```python
import os, sys
code_dir = os.path.abspath(os.path.join(os.getcwd(), 'code'))
sys.path.insert(0, code_dir)
```


```python
from fizzbuzz import fizz_buzz
```


```python
fizz_buzz(18)
```




    'Fizz'



We can load our data from outside the notebook


```python
#import os
data_file = os.path.abspath(os.path.join(os.getcwd(), 'data', 'project_size.csv'))
```


```python
import pandas as pd
 
df = pd.read_csv(data_file, delimiter=';')
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month</th>
      <th>project</th>
      <th>loc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021.01</td>
      <td>A</td>
      <td>100</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021.01</td>
      <td>B</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021.01</td>
      <td>C</td>
      <td>1100</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2021.02</td>
      <td>A</td>
      <td>200</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2021.02</td>
      <td>B</td>
      <td>2100</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2021.02</td>
      <td>C</td>
      <td>1100</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2021.03</td>
      <td>A</td>
      <td>500</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2021.03</td>
      <td>B</td>
      <td>2100</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2021.03</td>
      <td>C</td>
      <td>3100</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2021.04</td>
      <td>A</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2021.04</td>
      <td>B</td>
      <td>5000</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2021.04</td>
      <td>C</td>
      <td>4100</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
