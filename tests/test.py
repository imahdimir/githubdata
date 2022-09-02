"""

  """

##

from src.githubdata import GithubData


##
u = 'https://github.com/imahdimir/d-BaseTicker'
r = GithubData(u)
print(r.local_path)

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