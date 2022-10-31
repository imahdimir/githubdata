"""

  """

import importlib


importlib.reload(githubdata)

from src.githubdata.github_data_repo import *


## the most simple usage
u = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
df = get_data_from_github(u)

## clone a public repo
u = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
repo = GithubDataRepo(u)
repo.clone_overwrite()

##
repo.rmdir()

## clone a public repo and commit back
u = 'https://github.com/imahdimir/test-public'
repo = GithubDataRepo(u)
repo.clone_overwrite()

##
msg = 'test commit'
repo.commit_and_push(msg)

##
repo.rmdir()

## clone a private repo and commit back
ur = 'https://github.com/imahdimir/test-private'
rp = GithubDataRepo(ur)
rp.clone_overwrite()

##
rp.commit_and_push('test commit')

##
