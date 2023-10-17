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

def commit_and_push_by_u_repo(gdr: GitHubDataRepo) :
    msg = 'Updated by associated \"u\" repo'
    gdr.commit_and_push(msg)

def upload_2_github(gdr: GitHubDataRepo , df , fn: str) :
    dfp = gdr.data_fp
    if dfp is not None :
        dfp.unlink()

    nfp = gdr.local_path / fn

    df.to_parquet(nfp , index = False)

    commit_and_push_by_u_repo(gdr)

def make_data_fn(dn , iso_date) :
    return "{}_{}.parquet".format(dn , iso_date)
