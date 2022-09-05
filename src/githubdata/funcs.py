"""

    """

import json
from pathlib import Path

from src.githubdata.consts import github_base_url
from src.githubdata.main import GithubData


def clean_github_url(github_repo_url) :
    inp = github_repo_url

    inp = inp.replace(github_base_url , '')

    spl = inp.split('/' , )
    spl = spl[:2]

    urp = '/'.join(spl)
    urp = urp.split('#')[0]

    url = github_base_url + urp
    return url

def github_url_wt_credentials(user , token , targ_repo) :
    return f'https://{user}:{token}@github.com/{targ_repo}'

def get_data_from_github(github_url) :
    """
    :param: github_url: url of the GitHub gd
    :return: pandas.DataFrame
    """
    gd = GithubData(github_url)
    df = gd.read_data()
    gd.rmdir()
    return df

def get_usr_tok_from_jsp(jsp) :
    with open(jsp , 'r') as fi :
        js = json.load(fi)
    return js['usr'] , js['tok']

def get_github_token_pathes() :
    gd_url = 'https://github.com/imahdimir/github-token-path'
    gd = GithubData(gd_url)
    gd.overwriting_clone()
    js = gd.meta
    op = None
    for pn in js.values() :
        fp = Path(pn)
        if fp.exists() :
            op = fp
            break
    gd.rmdir()
    return op
