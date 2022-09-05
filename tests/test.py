"""

  """

##
import json

import dulwich.porcelain

from src.githubdata import get_data_from_github
from src.githubdata import GithubData
from src.githubdata.main import get_github_token_pathes


## the most simple usage
u = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
df = get_data_from_github(u)

## test get_github_token_pathes()
fp = get_github_token_pathes()
print(fp)

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
js = repo.meta
##
js['desc'] = 'test'
with open(repo.meta_fp , 'w') as fi :
    json.dump(js , fi , indent = 4)

##
msg = 'test commit'
repo.commit_and_push(msg)

##
repo.rmdir()

##
import dulwich


ur = 'https://github.com/imahdimir/test-private'

dulwich.porcelain.clone(ur , checkout = True)

##

##
