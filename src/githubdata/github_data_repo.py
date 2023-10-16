"""

    """

from pathlib import Path

import pandas as pd
from giteasy import GitHubRepo

default_githubdata_dir = Path('GitHubData/')

class GitHubDataRepo(GitHubRepo) :
    def __init__(self ,
                 repo_url ,
                 local_path = None ,
                 containing_dir = default_githubdata_dir ,
                 committing_usr = None ,
                 token = None
                 ) :
        super().__init__(repo_url = repo_url ,
                         local_path = local_path ,
                         containing_dir = containing_dir ,
                         committing_usr = committing_usr ,
                         token = token)

        """
        
        """

        self.data_fp: Path | None = None

        # run on init
        self.set_data_fp()

    def clone_overwrite(self , depth = 1) :
        super().clone_overwrite(depth = depth)
        self.set_data_fp()

    def set_data_fp(self) :
        fps = self.local_path.glob('*.parquet')
        # get the first fp or none if no parquet file exists
        self.data_fp = next(fps , None)

    def read_data(self) :
        """
        reads the data from the local path if it exists, otherwise clones the repo and reads the data.
        :return: pandas.DataFrame
        """
        if not self.local_path.exists() :
            self.clone_overwrite()
        df = pd.read_parquet(self.data_fp)
        return df
