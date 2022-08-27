A simple tool to get last/full version of a github repository and committing
back to
it.

# Install

```bash
pip install githubdata
```

# Quick Start

```python
>>> from githubdata import GithubData


>>> url = 'https://github.com/imahdimir/d-uniq-BaseTickers'

>>> rp = GithubData(url) 
>>> rp.clone()

>>> fp = rp.data_filepath
>>> print(fp)

'd-uniq-BaseTickers/data.xlsx'  # This the relative path of downloaded dataset
```

You can easily use the `fp` to read the dataset quickly. like:

```python
import pandas as pd

df = pd.read_excel(fp)
```

## To delete everything downloaded

```python
rp.rmdir()
```

# More Details

`rp.clone()`

- Every time excecuted, it re-downloads last version of data.

`rp.data_filepath`

- This attribute contains the relative path of the downloaded dataset.

# Contributions

The project is open to any contribution.