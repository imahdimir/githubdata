"""

  """

import json
import shutil
from pathlib import Path
from pathlib import PurePath

import pandas as pd
from dulwich import porcelain
from dulwich.ignore import IgnoreFilter
from dulwich.ignore import read_ignore_patterns


data_file_suffixes = {
    '.xlsx' : None ,
    '.prq'  : None ,
    }

gitburl = 'https://github.com/'

class GithubData :
  def __init__(self , source_url , user = None , token = None) :
    self.source_url = source_url
    self._cred_user = user
    self._token = token

    self.clean_source_url = _clean_github_url(source_url)
    self.user_repo = self.clean_source_url.split(gitburl)[1]
    self.user_name = self.user_repo.split('/')[0]
    self.repo_name = self.user_repo.split('/')[1]

    self._cred_url = None

    self._local_path = None
    self.local_path = None

    self._repo = None
    self._data_suf = None
    self.data_fp = None
    self.meta = None
    self.meta_fp = None

    self._make_url_with_credentials()

  def _make_url_with_credentials(self) :
    if self._token is None :
      self._cred_url = self.clean_source_url
      return None

    if self._cred_user is None :
      self._cred_user = self.user_name

    self._cred_url = _github_url_wt_credentials(user = self._cred_user ,
                                                token = self._token ,
                                                targ_repo = self.user_repo)

  @property
  def local_path(self) :
    return self._local_path

  @local_path.setter
  def local_path(self , local_dir) :
    if local_dir is None :
      self._local_path = Path(self.repo_name)
    else :
      self._local_path = Path(local_dir) / self.repo_name

    if self._local_path.exists() :
      print('Warning: local_path already exists')

  def _get_user_fr_input(self) :
    usr = input('(skip for default) github username:')
    if usr.strip() == '' :
      usr = self.user_name
    return usr

  def _list_ev_thing_in_repo_dir(self) :
    evt = list(self._local_path.glob('*'))
    return [PurePath(x).relative_to(self._local_path) for x in evt]

  def _remove_ignored_files(self , file_paths) :
    ignore_fp = self._local_path / '.gitignore'

    if not ignore_fp.exists() :
      return file_paths

    with open(ignore_fp , 'rb') as fi :
      ptrns = list(read_ignore_patterns(fi))

    flt = IgnoreFilter(ptrns)

    return [x for x in file_paths if not flt.is_ignored(x)]

  def _stage_evthing_in_repo(self) :
    evt = self._list_ev_thing_in_repo_dir()
    not_ignored = self._remove_ignored_files(evt)
    stg = [str(x) for x in not_ignored]
    self._repo.stage(stg)

  def _ret_commit_credit_url(self , user = None , token = None) :
    if user is None :
      user = self._get_user_fr_input()
    else :
      user = user

    if token is None :
      tok = input('_token:')
    else :
      tok = token

    return _github_url_wt_credentials(user , tok , self.user_repo)

  def _set_defualt_data_suffix(self) :
    for ky in data_file_suffixes.keys() :
      fps = self.ret_sorted_fpns_by_suf(ky)
      if len(fps) >= 1 :
        self._data_suf = ky
        break

  def _set_data_fps(self) :
    self._set_defualt_data_suffix()

    if self._data_suf is None :
      return None

    fpns = self.ret_sorted_fpns_by_suf(self._data_suf)

    if len(fpns) == 1 :
      self.data_fp = fpns[0]
    else :
      self.data_fp = fpns

  def ret_sorted_fpns_by_suf(self , suffix) :
    suffix = '.' + suffix if suffix[0] != '.' else suffix
    the_list = list(self._local_path.glob(f'*{suffix}'))
    return sorted(the_list)

  def read_json(self) :
    fps = self.ret_sorted_fpns_by_suf('.json')
    if len(fps) == 0 :
      return None

    fp = fps[0]
    self.meta_fp = fp

    with open(fp , 'r') as fi :
      js = json.load(fi)

    self.meta = js

    return js

  def clone(self , depth = 1) :
    """
    Every time excecuted, it re-downloads last version of the reposiroty to local_path.

    :param depth: None for full depth, default = 1 (last version)
    :return: None
    """
    if self._local_path.exists() :
      self.rmdir()
    self._repo = porcelain.clone(self._cred_url ,
                                 self._local_path ,
                                 depth = depth)
    self._set_data_fps()
    self.read_json()

  def commit_and_push(self ,
                      message ,
                      branch = 'main' ,
                      user = None ,
                      token = None
                      ) :
    cred_url = self._ret_commit_credit_url(user = user , token = token)
    self._stage_evthing_in_repo()
    self._repo.do_commit(message.encode())
    porcelain.push(str(self._local_path) , cred_url , branch)

  def read_data(self) :
    if not self._local_path.exists() :
      self.clone()
    else :
      self._set_data_fps()

    if not isinstance(self.data_fp , list) :
      if self._data_suf == '.xlsx' :
        return pd.read_excel(self.data_fp)
      else :
        return pd.read_parquet(self.data_fp)

  def rmdir(self) :
    shutil.rmtree(self._local_path)

def _clean_github_url(github_repo_url) :
  inp = github_repo_url

  inp = inp.replace(gitburl , '')

  spl = inp.split('/' , )
  spl = spl[:2]

  urp = '/'.join(spl)
  urp = urp.split('#')[0]

  url = gitburl + urp

  return url

def _github_url_wt_credentials(user , token , targ_repo) :
  return f'https://{user}:{token}@github.com/{targ_repo}'