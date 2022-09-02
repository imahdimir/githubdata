"""

  """

##

from src.githubdata import GithubData
from src.githubdata import get_data_from_github


##
u = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
df = get_data_from_github(u)

##
print(df.head())
##
df = r.read_data()

##
print(r.source_url)
print(r._cred_user)
##
r.clone()
##
r.clone()

##
u = 'https://github.com/imahdimir/tset'
r = GithubData(u , token = '')
r.clone()
##

##
r.commit_and_push('test' , user = r.user_name , token = '')