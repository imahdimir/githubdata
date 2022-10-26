"""

    """

import json
from pathlib import Path

import pandas as pd
from giteasy.repo import Repo


data_file_suffixes = {
        '.xlsx' : None ,
        '.prq'  : None ,
        '.csv'  : None ,
        }

class GithubData(Repo) :

    def __init__(self , src_url , github_usr = None , usr_tok_json_fp = None) :
        super().__init__(src_url = src_url ,
                         github_usr = github_usr ,
                         usr_tok_json_fp = usr_tok_json_fp)
        self.set_data_fps()
        self.read_metadata()

    def overwriting_clone(self , overwrite = True , depth = 1) :
        super().overwriting_clone(overwrite = overwrite , depth = depth)
        self.set_data_fps()

    def _set_defualt_data_suffix(self) :
        for ky in data_file_suffixes.keys() :
            fps = self.ret_sorted_fpns_by_suf(ky)
            if len(fps) >= 1 :
                self.data_suf = ky
                return

        self.data_suf = None

    def set_data_fps(self) :
        self._set_defualt_data_suffix()

        if not self.data_suf :
            return

        fps = self.ret_sorted_fpns_by_suf(self.data_suf)

        if len(fps) == 1 :
            self.data_fp = fps[0]
        else :
            self.data_fp = fps

    def ret_sorted_fpns_by_suf(self , suffix) :
        ls = list(self.local_path.glob(f'*{suffix}'))
        return sorted(ls)

    def read_metadata(self) :
        fps = self.ret_sorted_fpns_by_suf('.json')

        if len(fps) == 0 :
            return

        fp = fps[0]
        self.meta_fp = fp

        with open(fp , 'r') as fi :
            js = json.load(fi)
        self.meta = js

        return js

    def read_data(self) :
        if not self.local_path.exists() :
            self.overwriting_clone()

        if isinstance(self.data_fp , Path) :
            if self.data_suf == '.xlsx' :
                return pd.read_excel(self.data_fp , engine = 'openpyxl')
            elif self.data_suf == '.prq' :
                return pd.read_parquet(self.data_fp)
            elif self.data_suf == '.csv' :
                return pd.read_csv(self.data_fp)

def get_data_from_github(github_url) :
    """
    :param: github_url
    :return: pandas.DataFrame
    """
    gd = GithubData(github_url)
    df = gd.read_data()
    gd.rmdir()
    return df
