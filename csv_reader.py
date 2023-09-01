import pandas as pd


class Reader:
    def __init__(self, args):
        self.column = args.column
        self.encoding = args.encoding
        self._locations = []
        self.keywords = args.keyword

        if args.path.endswith(".csv"):
            self.read_csv(args.path)
        elif args.path.endswith(".txt"):
            self.read_txt(args.path)
        else:
            raise ValueError("File extension must be csv or txt")

    def read_csv(self, path):
        data = pd.read_csv(path, encoding=self.encoding)
        self._locations = data[self.column].tolist()

    def read_txt(self, path):
        with open(path, "r", encoding=self.encoding) as f:
            self._locations = f.readlines()

    @staticmethod
    def filtering_location(location):
        for keyword in ["~", "("]:
            if keyword in location:
                location = location.split(keyword)[0].strip()
        return location

    @property
    def locations(self):
        filtering_locations = [Reader.filtering_location(loc) for loc in self._locations]
        return filtering_locations
