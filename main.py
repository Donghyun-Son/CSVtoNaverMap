import argparse

from crawler import Crawler
from csv_reader import Reader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locations_path", dest="path", type=str, default="")
    parser.add_argument("-i", "--login_id", dest="login_id", type=str, default="")
    parser.add_argument("-p", "--login_pw", dest="login_pw", type=str, default="")
    parser.add_argument("-f", "--favorite", dest="favorite", type=str, default="")
    parser.add_argument("-c", "--column", dest="column", type=str, default="")
    parser.add_argument("-e", "--encoding", dest="encoding", type=str, default="UTF-8")
    parser.add_argument("-s", "--search_city", dest="city", type=str, default="서울특별시")
    parser.add_argument("-k", "--filter_keyword", dest="keyword", type=list, default=[])
    args = parser.parse_args()

    reader = Reader(args)
    crawler = Crawler(args)

    crawler.input_to_naver_map(reader.locations)
