"""

    """

from pathlib import Path

from giteasy import GitHubRepo
from mirutil.df import read_data_according_to_type as rdatt

data_file_suffixes = {
        '.xlsx' : None ,
        '.prq'  : None ,
        '.csv'  : None ,
        }

default_containing_dir = Path('GitHubData/')

class GitHubDataRepo(GitHubRepo) :

    def __init__(self ,
                 repo_url ,
                 local_path = None ,
                 containing_dir = default_containing_dir ,
                 committing_usr = None ,
                 token = None
                 ) :
        super().__init__(repo_url = repo_url ,
                         local_path = local_path ,
                         containing_dir = containing_dir ,
                         committing_usr = committing_usr ,
                         token = token)

        self.data_suf: str | None = None
        self.data_fp: Path | None = None

        self.set_data_fps()

    def clone_overwrite(self , depth = 1) :
        super().clone_overwrite(depth = depth)
        self.set_data_fps()

    def ret_sorted_fpns_by_suf(self , suffix) :
        ls = list(self.local_path.glob(f'*{suffix}'))
        return sorted(ls)

    def _set_defualt_data_suffix(self) :
        for ky in data_file_suffixes.keys() :
            fps = self.ret_sorted_fpns_by_suf(ky)
            if len(fps) != 0 :
                self.data_suf = ky
                return

    def set_data_fps(self) :
        self._set_defualt_data_suffix()
        if self.data_suf is None :
            return
        fps = self.ret_sorted_fpns_by_suf(self.data_suf)
        self.data_fp = fps[0]

    def read_data(self) :
        if not self.local_path.exists() :
            self.clone_overwrite()
        return rdatt(self.data_fp)
