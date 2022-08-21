A simple tool to get last/full version of a github repository and committing
back to
it.

# Quick Start

```python
from githubdata import GithubDataRepo


url = 'https://github.com/imahdimir/d-uniq-BaseTickers'

repo = GithubDataRepo(url)
repo.clone_overwrite_last_version()

data_suffix = '.xlsx'
fpns = repo.return_sorted_list_of_fpns_with_the_suffix(data_suffix)
```

## To delete the directory downloaded:

```python
repo.rmdir()
```

# More Details

`repo.clone_overwrite_last_version()`

- Every time excecuted, it re-downloads last version of data.

`repo.return_sorted_list_of_fpns_with_the_suffix('.xlsx')`

- Returns a sorted list containing filepaths downloaded with a given suffix (type).