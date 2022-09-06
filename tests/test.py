"""

  """

from src.githubdata.main import get_data_from_github
from src.githubdata.main import GithubData


## the most simple usage
u = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
df = get_data_from_github(u)

## clone a public repo
u = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
repo = GithubData(u)
repo.overwriting_clone()

##
repo.rmdir()

## clone a public repo and commit back
u = 'https://github.com/imahdimir/test-public'
repo = GithubData(u)
repo.overwriting_clone()

##
msg = 'test commit'
repo.commit_and_push(msg)

##
repo.rmdir()

## clone a private repo and commit back
ur = 'https://github.com/imahdimir/test-private'
rp = GithubData(ur)
rp.overwriting_clone()

##


##
rp.commit_and_push('test commit')

##
