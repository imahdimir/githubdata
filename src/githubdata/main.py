"""

    """

import json

import pandas as pd
from giteasy import Repo


data_file_suffixes = {
        '.xlsx' : None ,
        '.prq'  : None ,
        '.csv'  : None ,
        }

class GithubData(Repo) :
    def __init__(self , source_url , user_token_json_path = None) :
        super().__init__(source_url , user_token_json_path)

        self.data_suf = None
        self.data_fp = None
        self.meta = None
        self.meta_fp = None

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
                break

    def set_data_fps(self) :
        self._set_defualt_data_suffix()

        if self.data_suf is None :
            return None

        fpns = self.ret_sorted_fpns_by_suf(self.data_suf)

        if len(fpns) == 1 :
            self.data_fp = fpns[0]
        else :
            self.data_fp = fpns

    def ret_sorted_fpns_by_suf(self , suffix) :
        suffix = '.' + suffix if suffix[0] != '.' else suffix
        the_list = list(self.local_path.glob(f'*{suffix}'))
        return sorted(the_list)

    def read_metadata(self) :
        fps = self.ret_sorted_fpns_by_suf('.json')
        if len(fps) == 0 :
            return None
        fp = fps[0]
        self.meta_fp = fp
        with open(fp , 'r') as fi :
            js = json.load(fi)
        self.meta = js
        return js

    def read_data(self) :
        if not self.local_path.exists() :
            self.overwriting_clone()

        self.set_data_fps()

        if not isinstance(self.data_fp , list) :
            if self.data_suf == '.xlsx' :
                # noinspection PyArgumentList
                return pd.read_excel(self.data_fp)
            elif self.data_suf == '.prq' :
                return pd.read_parquet(self.data_fp)
            elif self.data_suf == '.csv' :
                return pd.read_csv(self.data_fp)

def get_data_from_github(github_url) :
    """
    :param: github_url: url of the GitHub gd
    :return: pandas.DataFrame
    """
    gd = GithubData(github_url)
    df = gd.read_data()
    gd.rmdir()
    return df
