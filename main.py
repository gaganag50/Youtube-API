#   coding:utf-8

# This file collects title, url, description, channel name given to a query string
# and saves the results to the csv file 


from __future__ import print_function
from download_music import Downloader
from convert_to_mp3 import convert_to_mp3
from youtbe_search import youtube_search
from googleapiclient.errors import HttpError

import argparse
import threading
import csv
import os


class ConvertThread(threading.Thread):
    def __init__(self, download_dir, file_name, dir):
        threading.Thread.__init__(self)
        self.file_name = file_name
        self.dir = dir
        self.down = download_dir

    def run(self):
        convert_to_mp3(self.down, self.file_name, mp3_dir)


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Coding In Python')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()

    root_dir_cdn = "/home/gagan/Desktop/"
    cdn_dir = root_dir_cdn + "/cdn/"
    mp3_dir = root_dir + "/mp3/"
    download_dir = root_dir + "/download/"

    create_dir(cdn_dir)
    create_dir(mp3_dir)
    create_dir(download_dir)

    csv_file_name = "cdn.csv"
    # choice = raw_input("Create csv ")
    choice = "N"
    if choice == "Y":
        csv_file = open(cdn_dir + csv_file_name, "w")
    download_csv = open(cdn_dir + "downloaded.csv", "w+")
    failed_csv = open(cdn_dir + "failed.csv", "a+")
    download_writer = csv.writer(download_csv)
    failed_writer = csv.writer(failed_csv)

    try:
        if choice == 'Y':
            youtube_search(args, csv_file)
            csv_file.close()
        while True:
            # choice = raw_input("Shall we start the processing? (Y/N)")
            choice = "Y"
            if choice == 'Y':
                break
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    with open(cdn_dir + csv_file_name, "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            try:
                url = row[3]
                file_name = row[0]
                d = Downloader(url, file_name, download_dir)
                downloaded_file = d.download_file()
                download_writer.writerow(row)

            except Exception as e:
                print (str(e))
                failed_writer.writerow(row)

    download_csv.close()