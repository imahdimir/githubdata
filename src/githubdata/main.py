"""

  """

import json
import shutil
from pathlib import Path
from pathlib import PurePath

import pandas as pd
from dulwich import porcelain
from dulwich.client import HTTPUnauthorized
from dulwich.ignore import IgnoreFilter
from dulwich.ignore import read_ignore_patterns


data_file_suffixes = {
        '.xlsx' : None ,
        '.prq'  : None ,
        }

gitburl = 'https://github.com/'

class GithubData :
    def __init__(
            self ,
            source_url ,
            user_token_json_path = None
            ) :
        self.source_url = source_url
        self._usr_tok_jsp = user_token_json_path

        self.clean_source_url = clean_github_url(source_url)
        self.user_repo = self.clean_source_url.split(gitburl)[1]
        self.user_name = self.user_repo.split('/')[0]
        self.repo_name = self.user_repo.split('/')[1]

        self._local_path = None

        self._clone_url = None

        self._cred_usr = None
        self._cred_tok = None

        self._commit_url = None

        self._repo = None
        self._data_suf = None
        self.data_fp = None
        self.meta = None
        self.meta_fp = None

        self._init_local_path()
        self._set_data_fps()
        self.read_json()

    @property
    def local_path(
            self
            ) :
        return self._local_path

    @local_path.setter
    def local_path(
            self ,
            local_dir
            ) :
        if local_dir is None :
            self._local_path = Path(self.repo_name)
        else :
            self._local_path = Path(local_dir) / self.repo_name

        if self._local_path.exists() :
            print('Warning: local_path already exists')

    def _init_local_path(
            self
            ) :
        self.local_path = None

    def _list_ev_thing_in_repo_dir(
            self
            ) :
        evt = list(self._local_path.glob('*'))
        return [PurePath(x).relative_to(self._local_path) for x in evt]

    def _remove_ignored_files(
            self ,
            file_paths
            ) :
        ignore_fp = self._local_path / '.gitignore'

        if not ignore_fp.exists() :
            return file_paths

        with open(ignore_fp , 'rb') as fi :
            ptrns = list(read_ignore_patterns(fi))

        flt = IgnoreFilter(ptrns)

        return [x for x in file_paths if not flt.is_ignored(x)]

    def _stage_evthing_in_repo(
            self
            ) :
        evt = self._list_ev_thing_in_repo_dir()
        not_ignored = self._remove_ignored_files(evt)
        stg = [str(x) for x in not_ignored]
        self._repo.add(stg)
        self._repo.stage(stg)

    def _set_defualt_data_suffix(
            self
            ) :
        for ky in data_file_suffixes.keys() :
            fps = self.ret_sorted_fpns_by_suf(ky)
            if len(fps) >= 1 :
                self._data_suf = ky
                break

    def _set_data_fps(
            self
            ) :
        self._set_defualt_data_suffix()

        if self._data_suf is None :
            return None

        fpns = self.ret_sorted_fpns_by_suf(self._data_suf)

        if len(fpns) == 1 :
            self.data_fp = fpns[0]
        else :
            self.data_fp = fpns

    def ret_sorted_fpns_by_suf(
            self ,
            suffix
            ) :
        suffix = '.' + suffix if suffix[0] != '.' else suffix
        the_list = list(self._local_path.glob(f'*{suffix}'))
        return sorted(the_list)

    def read_json(
            self
            ) :
        fps = self.ret_sorted_fpns_by_suf('.json')
        if len(fps) == 0 :
            return None

        fp = fps[0]
        self.meta_fp = fp

        with open(fp , 'r') as fi :
            js = json.load(fi)

        self.meta = js

        return js

    def _input_cred_usr_tok(
            self
            ) :
        usr = input('(enter nothing for same as repo source) github username: ')
        if usr.strip() == '' :
            self._cred_usr = self.user_name
        tok = input('token: ')
        self._cred_tok = tok

    def _set_cred_usr_tok(
            self
            ) :
        if self._usr_tok_jsp is not None :
            fp = self._usr_tok_jsp
            self._cred_usr , self._cred_tok = get_usr_tok_from_jsp(fp)
            return None

        fp = Path('user_token.json')
        if fp.exists() :
            self._cred_usr , self._cred_tok = get_usr_tok_from_jsp(fp)
            return None

        fp = get_github_token_pathes()
        if fp :
            self._cred_usr , self._cred_tok = get_usr_tok_from_jsp(fp)
            return None

        self._input_cred_usr_tok()

    def _set_clone_url(
            self
            ) :
        self._set_cred_usr_tok()
        usr = self._cred_usr
        tok = self._cred_tok
        tr = self.user_repo
        self._clone_url = github_url_wt_credentials(usr , tok , tr)

    def overwriting_clone(
            self ,
            depth = 1
            ) :
        """ Every time excecuted, it re-downloads last version of the reposiroty to local_path.

        param depth: None for full depth, default = 1 (last version)
        return: None
        """
        trgdir = self._local_path
        if trgdir.exists() :
            self.rmdir()

        try :
            self._clone_url = self.clean_source_url
            url = self._clone_url
            self._repo = porcelain.clone(url , trgdir , depth = depth)
        except HTTPUnauthorized :
            self._set_clone_url()
            url = self._clone_url
            self._repo = porcelain.clone(url , trgdir , depth = depth)

        self._set_data_fps()
        self.read_json()

    def _set_commit_url(
            self
            ) :
        if self._clone_url != self.clean_source_url :
            self._commit_url = self._clone_url
        else :
            self._set_cred_usr_tok()
            usr = self._cred_usr
            tok = self._cred_tok
            tr = self.user_repo
            self._commit_url = github_url_wt_credentials(usr , tok , tr)

    def commit_and_push(
            self ,
            message ,
            branch = 'main'
            ) :
        self._set_commit_url()
        url = self._commit_url
        self._stage_evthing_in_repo()
        self._repo.do_commit(message.encode())
        porcelain.push(str(self._local_path) , url , branch)

    def read_data(
            self
            ) :
        if not self._local_path.exists() :
            self.overwriting_clone()
        else :
            self._set_data_fps()

        if not isinstance(self.data_fp , list) :
            if self._data_suf == '.xlsx' :
                return pd.read_excel(self.data_fp)
            else :
                return pd.read_parquet(self.data_fp)

    def rmdir(
            self
            ) :
        shutil.rmtree(self._local_path)

def clean_github_url(
        github_repo_url
        ) :
    inp = github_repo_url

    inp = inp.replace(gitburl , '')

    spl = inp.split('/' , )
    spl = spl[:2]

    urp = '/'.join(spl)
    urp = urp.split('#')[0]

    url = gitburl + urp
    return url

def github_url_wt_credentials(
        user ,
        token ,
        targ_repo
        ) :
    return f'https://{user}:{token}@github.com/{targ_repo}'

def get_data_from_github(
        github_repo_url
        ) :
    """
    param github_repo_url: url of the GitHub repo
    return: pandas.DataFrame
    """
    repo = GithubData(github_repo_url)
    df = repo.read_data()
    repo.rmdir()
    return df

def get_usr_tok_from_jsp(
        jsp
        ) :
    with open(jsp , 'r') as fi :
        js = json.load(fi)
    return js['usr'] , js['tok']

def get_github_token_pathes() :
    rp_url = 'https://github.com/imahdimir/github-token-path'
    rp = GithubData(rp_url)
    rp.overwriting_clone()
    js = rp.meta
    op = None
    for pn in js.values() :
        fp = Path(pn)
        if fp.exists() :
            op = fp
            break
    rp.rmdir()
    return op

##
