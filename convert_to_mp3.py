'''
    This file converts all the media file in a directory to mp3
'''
import os
import subprocess


def convert_to_mp3(download_dir, file_name, dest_dir):
    out_file = os.path.splitext(os.path.basename(file_name))[0] + ".mp3"
    log_file = open("/home/gagan/Desktop/upload/" + "log.txt", "a+")

    # print("-----------------------")
    print(file_name)

    subprocess.call([
        "ffmpeg",
        "-hide_banner",
        "-n",
        "-i", download_dir + file_name,
        # "-codec:a", "libmp3lame", "-qscale:a", "8", dest_dir + out_file
        "-codec:a", "libmp3lame", "-b:a", "80k", dest_dir + out_file
    ],
        stderr=log_file
    )

    # print("CONVERSION COMPLETE")
    log_file.close()


def start_conversion(src_dir, list_file, dest_dir, status_file):
    with open(list_file, "r") as f:
        list_of_files = f.read().splitlines()

        # with open(status_file, "w+") as f:
        for cur_file in list_of_files:
            print (cur_file)
            try:
                convert_to_mp3(src_dir, cur_file, dest_dir)
                # print 1
            except:
                pass


if __name__ == '__main__':
    dest_dir = "/home/gagan/Desktop/upload/"
    src_dir = "/home/gagan/Desktop/download/"
    status_file = "/home/gagan/Desktop/status_file.txt"
    src_file = "/home/gagan/Desktop/src_file.txt"
    start_conversion(src_dir, src_file, dest_dir, status_file)
