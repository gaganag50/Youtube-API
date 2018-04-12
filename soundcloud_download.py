# coding: utf-8
# This file downloads all the songs given to a particular query on soundcloud
import soundcloud
import requests
import csv
import os.path

# create a client object with your app credentials
CLIENT_ID = 'iq13rThQx5jx9KWaOY8oGgg1PUm9vp3J'
client = soundcloud.Client(client_id=CLIENT_ID)
download_dir = unicode("soundcloud/")
query_str = "vinod agarwal"
csv_file_name = "cdn_soundcloud.csv"


class Soundcloud_downloader:
    def __init__(self, track, down_dir=None):
        self.url = track.stream_url + "?client_id=" + CLIENT_ID
        self.title = track.title
        self.artwork = track.artwork_url
        self.filesize = track.original_content_size
        self.description = track.description
        self.user = track.user['username']
        self.user_url = track.user['permalink_url']

        self.down_dir = down_dir
        if not down_dir:
            self.down_dir = download_dir
        self.down_dir += self.title

    def download_sound(self):
        img = self.down_dir + ".jpg"
        mp3 = self.down_dir + ".mp3"

        if not os.path.isfile(img) and self.artwork:
            print ("Downloading " + self.title)
            r = requests.get(self.artwork, allow_redirects=True)
            open(img, "wb").write(r.content)

        if not os.path.isfile(mp3) and self.url:
            r = requests.get(self.url, allow_redirects=True)
            open(mp3, "wb").write(r.content)

    def write(self, writer):
        row = [
            self.title,
            self.user,
            self.url,
            self.description,
            self.user_url
        ]

        for i in range(0, len(row)):
            if row[i] is not None:
                row[i] = row[i].encode('utf-8')
        writer.writerow(row)

    def print_type(self):
        row = [
            self.title,
            self.user,
            self.url,
            self.description,
            self.user_url
        ]
        for r in row:
            if r is not None:
                r = r.encode('utf-8')


no_of_results = 100
tracks = client.get('/tracks', q=query_str,
                    limit=no_of_results,
                    )

with open(download_dir + csv_file_name, "a+") as f:
    csv_writer = csv.writer(f)
    for track in tracks:
        d = Soundcloud_downloader(track)
        d.download_sound()
        d.write(csv_writer)
