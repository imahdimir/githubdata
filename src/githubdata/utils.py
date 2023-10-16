"""


    """

import pandas as pd

from .github_data_repo import GitHubDataRepo

def get_data_wo_double_clone(github_url , remove_cache = False
                             ) -> pd.DataFrame :
    """
    gets data from a GitHub data repo, without cloning it twice. if it is already cloned, it will read the data from the local path.

    :param: github_url
    :remove_cache: if True, it will remove the cloned repo after reading the data.
    :return: pandas.DataFrame
    """
    gd = GitHubDataRepo(github_url)
    df = gd.read_data()
    if remove_cache :
        gd.rmdir()
    return df

def clone_overwrite_a_repo__ret_gdr_obj(gd_url) :
    gdr = GitHubDataRepo(gd_url)
    gdr.clone_overwrite()
    return gdr
