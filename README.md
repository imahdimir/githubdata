A simple tool to get last/full version of a github repository and committing
back to
it.

# Quick Start

```python
>>> from githubdata import GithubData


>>> url = 'https://github.com/imahdimir/d-uniq-BaseTickers'

>>> repo = GithubData(url) 
>>> repo.clone()

>>> fp = repo.data_filepath
>>> print(fp)
'd-uniq-BaseTickers/data.xlsx'  # This the relative path of downloaded dataset
```

## To delete everything downloaded

```python
>>> repo.rmdir()
```

# More Details

`repo.clone()`

- Every time excecuted, it re-downloads last version of data.

`repo.data_filepath`

- This attribute contains the relative path of the downloaded dataset.