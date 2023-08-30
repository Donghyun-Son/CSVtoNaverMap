import pandas as pd


class Reader:
    def __init__(self, args):
        self.path = args.excel_path
        self.column_name = args.column_name
        self.data = None

    def read_csv(self):
        self.data = pd.read_csv(self.path, encoding="EUC-KR")

    def get_locations(self):
        location_list = self.data[self.column_name].tolist()
        modified_locations = [self._modify_location(loc) for loc in location_list]
        return modified_locations

    # 필터링이 필요한 경우에만 사용
    def _modify_location(self, location):
        # "~" 가 있는 경우: "~" 앞의 위치를 사용
        if "~" in location:
            location = location.split("~")[0].strip()

        # "(" 가 있는 경우: "(" 이전의 내용만 사용
        if "(" in location:
            location = location.split("(")[0].strip()

        return location
