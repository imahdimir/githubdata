##

import shutil
from pathlib import Path
from pathlib import PurePath

from dulwich import porcelain
from dulwich.ignore import IgnoreFilter
from dulwich.ignore import read_ignore_patterns
from dulwich.repo import Repo


gitburl = 'https://github.com/'

class GithubDataRepo :

  def __init__(self , source_url) :
    self.src_url = build_proper_github_repo_url(source_url)
    self.usr_repo_name = self.src_url.split(gitburl)[1]
    self.repo_name = self.usr_repo_name.split('/')[1]

    self._local_path = None
    self._repo = None

    self._init_local_path()

  @property
  def local_path(self) :
    return self._local_path

  @local_path.setter
  def local_path(self , local_dir) :
    if local_dir is None :
      self._local_path = Path(self.repo_name)
    else :
      self._local_path = Path(local_dir) / self.repo_name

    if not self._local_path.exists() :
      self._local_path.mkdir()
    else :
      print(f'WARNING: the dir {self.repo_name} already exist.\n'
            f'If it is not the same repository try setting local_path attribute to a differen dir.')

  def _init_local_path(self) :
    self.local_path = None

  def _list_evthing_in_repo_dir(self) :
    evt = list(self._local_path.glob('*'))
    evt = [PurePath(x).relative_to(self._local_path) for x in evt]
    return evt

  def _remove_ignored_files(self , file_paths) :
    ignore_fp = self._local_path / '.gitignore'

    if not ignore_fp.exists() :
      return file_paths

    with open(ignore_fp , 'rb') as fi :
      ptrns = list(read_ignore_patterns(fi))

    flt = IgnoreFilter(ptrns)

    return [x for x in file_paths if not flt.is_ignored(x)]

  def _stage_evthing_in_repo(self) :
    evt = self._list_evthing_in_repo_dir()
    not_ignored = self._remove_ignored_files(evt)
    stg = [str(x) for x in not_ignored]
    self._repo.stage(stg)

  def _get_username_token_from_input(self) :
    usr = input('(skip for default) github username:')

    if usr.strip() == "" :
      usr = self.usr_repo_name.split('/')[0]

    tok = input('token:')

    return usr , tok

  def _prepare_target_url(self) :
    usr_tok = self._get_username_token_from_input()
    return build_targurl_with_usr_token(usr_tok[0] ,
                                        usr_tok[1] ,
                                        self.usr_repo_name)

  def clone_overwrite_last_version(self , depth = 1) :
    """
    :param depth: None for full depth, default = 1 (last version)
    :return: None
    """
    if self._local_path.exists() :
      self.rmdir()

    porcelain.clone(self.src_url , self._local_path , depth = depth)

    self._repo = Repo(str(self._local_path))

  def return_sorted_list_of_fpns_with_the_suffix(self , suffix = '.prq') :
    suffix = '.' + suffix if suffix[0] != '.' else suffix
    the_list = list(self._local_path.glob(f'*{suffix}'))
    return sorted(the_list)

  def commit_and_push_to_github_data_target(self , message , branch = 'main') :
    targ_url_wt_usr_tok = self._prepare_target_url()
    tu = targ_url_wt_usr_tok

    self._stage_evthing_in_repo()

    self._repo.do_commit(message.encode())

    porcelain.push(str(self._local_path) , tu , branch)

  def rmdir(self) :
    shutil.rmtree(self._local_path)

def build_proper_github_repo_url(github_repo_url) :
  inp = github_repo_url

  inp = inp.replace(gitburl , '')

  spl = inp.split('/' , )
  spl = spl[:2]

  urp = '/'.join(spl)
  urp = urp.split('#')[0]

  url = gitburl + urp

  return url

def build_targurl_with_usr_token(usr , tok , targ_repo) :
  return f'https://{usr}:{tok}@github.com/{targ_repo}'

##
# gsrc = 'https://github.com/imahdimir/d-uniq-BaseTickers'
# btics = GithubDataRepo(gsrc)
# ##
# btics.clone_overwrite_last_version()
# ##
# fps = btics.return_sorted_list_of_fpns_with_the_suffix('prq')
# print(fps)
#
# ##