import argparse
from csv_reader import Reader
from crawler import Crawler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--excel_path", dest="excel_path", type=str, default="")
    parser.add_argument("-i", "--login_id", dest="login_id", type=str, default="")
    parser.add_argument("-p", "--login_pw", dest="login_pw", type=str, default="")
    parser.add_argument("-f", "--favorite_list_name", dest="favorite_list_name", type=str, default="")
    parser.add_argument("-c", "--column_name", dest="column_name", type=str, default="")
    args = parser.parse_args()

    reader = Reader(args)
    crawler = Crawler(args)

    reader.read_csv()
    locations = reader.get_locations()
    crawler.input_to_naver_map(locations)
