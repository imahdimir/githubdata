"""


    """

import shutil

from persiantools.jdatetime import JalaliDateTime

from .github_data_repo import GitHubDataRepo

def get_data_from_github(github_url) :
    """
    :param: github_url
    :return: pandas.DataFrame
    """
    gd = GitHubDataRepo(github_url)
    df = gd.read_data()
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
