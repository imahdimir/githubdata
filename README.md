A simple tool to get last/full version of a github repository and committing
back to
it.

# Install

```bash
pip install githubdata
```

# Quick Start

```python
from githubdata import get_data_from_github


repo_url = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
df = get_data_from_github(repo_url)
```