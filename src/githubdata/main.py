##

import shutil
from pathlib import Path
from pathlib import PurePath

from dulwich import porcelain
from dulwich.ignore import IgnoreFilter
from dulwich.ignore import read_ignore_patterns
from dulwich.repo import Repo


class GithubData :

  def __init__(self , source_url) :
    self.source_url = build_proper_github_repo_url(source_url)
    self.usrname_repname = get_usr_reponame_url(source_url)

    self._local_path = Path('github_' + self.usrname_repname.replace('/' , '_'))

    self.data_fps = None
    self.repo = None

  @property
  def local_path(self) :
    return self._local_path

  @local_path.setter
  def local_path(self , local_containing_dir) :
    if Path(local_containing_dir).exists() :
      repo_base_name = self.usrname_repname.split('/')[1]
      self._local_path = Path(local_containing_dir) / repo_base_name

      if not self._local_path.exists() :
        self._local_path.mkdir()
      else :
        print(f"The path {self._local_path} already exist.")

    else :
      print("Please enter a valid local path")

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
    self.repo.stage(stg)

  def _get_username_token_from_input(self) :
    usr = input('(skip for default) github username:')

    if usr.strip() == "" :
      usr = self.usrname_repname.split('/')[0]

    tok = input('token:')

    return usr , tok

  def _prepare_target_url(self) :
    usr_tok = self._get_username_token_from_input()
    return build_targurl_with_usr_token(usr_tok[0] ,
                                        usr_tok[1] ,
                                        self.usrname_repname)

  def set_data_fps(self) :
    evt = self._list_evthing_in_repo_dir()
    evt = [x for x in evt if x.suffix == '.prq']
    evt = [self._local_path / x for x in evt]
    self.data_fps = sorted(evt)

  def rmdir(self) :
    shutil.rmtree(self._local_path)

  def clone_overwrite_last_version(self , depth = 1) :
    """

    :param depth: None for full depth, default = 1 (last version)
    :return: None
    """

    if self._local_path.exists() :
      self.rmdir()

    porcelain.clone(self.source_url , self._local_path , depth = depth)

    self.repo = Repo(str(self._local_path))
    self.set_data_fps()

  def commit_and_push_to_github_data_target(self , message , branch = 'main') :
    targ_url_wt_usr_tok = self._prepare_target_url()
    tu = targ_url_wt_usr_tok

    self._stage_evthing_in_repo()

    self.repo.do_commit(message.encode())

    porcelain.push(str(self.local_path) , tu , branch)

def build_proper_github_repo_url(github_repo_url) :
  inp = github_repo_url

  gitburl = 'https://github.com/'
  inp = inp.replace(gitburl , '')

  spl = inp.split('/' , )
  spl = spl[:2]

  urp = '/'.join(spl)
  urp = urp.split('#')[0]

  url = gitburl + urp

  return url

def get_usr_reponame_url(github_repo_url) :
  pu = build_proper_github_repo_url(github_repo_url)
  pu = pu.split('github.com/')[1]
  return pu

def build_targurl_with_usr_token(usr , tok , targ_repo) :
  return f'https://{usr}:{tok}@github.com/{targ_repo}'

##
# gsrc = 'https://github.com/imahdimir/d-Unique-BaseTickers-TSETMC'
# btics = GithubData(gsrc)
# btics.local_path = '/Users/mahdi/Dropbox'
# ##
# btics.clone_overwrite_last_version()
# print(btics.data_fps)
# ##
# btics.rmdir()


##