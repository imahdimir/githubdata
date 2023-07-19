"""


    """

import shutil

import pandas as pd
from persiantools.jdatetime import JalaliDateTime

from .github_data_repo import GitHubDataRepo

def get_data_fr_github_without_double_clone(github_url , remove_cache = False
                                            ) -> pd.DataFrame :
    """
    gets data from a GitHub data repo, without cloning it twice.
    if it is already cloned, it will read the data from the local path.

    :param: github_url
    :remove_cache: if True, it will remove the cloned repo after reading the data.
    :return: pandas.DataFrame
    """
    gd = GitHubDataRepo(github_url)
    df = gd.read_data()

    if remove_cache :
        gd.rmdir()

    return df

def clone_with_overwrite_a_repo_return_gdr_obj(gd_url) :
    gdr = GitHubDataRepo(gd_url)
    gdr.clone_overwrite()
    return gdr

def replace_old_data_with_new_and_iso_jdate_title(gdt , df_fpn) :
    gdt.data_fp.unlink()

    tjd = JalaliDateTime.now().strftime('%Y-%m-%d')
    fp = gdt.local_path / f'{tjd}.prq'

    shutil.copy(df_fpn , fp)
    print(f'Replaced {df_fpn} to {fp}')

def push_to_github_by_code_url(gdt , github_url) :
    msg = 'Updated by ' + github_url
    gdt.commit_and_push(msg , branch = 'main')
