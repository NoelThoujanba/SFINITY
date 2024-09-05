from pytubefix import YouTube
from pytubefix import Playlist

import re

from sys import argv
import os
import subprocess

def DownloadAudioYT(url: str, save_dir: str, filename: str) -> str: #to return err log
    try: 
        # object creation using YouTube 
        yt = YouTube(url)
        
    except: 
        #to handle exception 
        print("Connection Error, unable to init pytube") 
        return "Connection Error, unable to init pytube"

    # Get all streams and filter for audio files
    mp4_streams = yt.streams.filter(only_audio=True)

    d_video = mp4_streams[0]

    try: 
        # downloading the video 
        d_video.download(output_path=save_dir, filename=filename)
        print(f'{filename} with url = {url} has been downloaded')

        return f'{filename} with url = {url} has been downloaded'
    except Exception as ex: 
        print(ex)
        print(f'{filename} with url = {url} ,operation failed')
        return f'{filename} with url = {url} ,operation failed'
    
def DownloadYTPlaylist(url: str, save_dir):
    
    YT_STREAM_AUDIO='140'

    playlist = Playlist(url)

    # this fixes the empty playlist.videos list, becase yy got updated
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    print(len(playlist.video_urls))

    for url in playlist.video_urls:
        print(url)

    # physically downloading the audio track
    for video in playlist.videos:
        audioStream = video.streams.get_by_itag(YT_STREAM_AUDIO)
        audioStream.download(output_path=save_dir)


def GetElementHavingSubString(data: list[str], sstr: str) -> int:
    for  index, elem in enumerate(data):
        if(elem.find(sstr) != -1):
            return index
    
    raise ValueError(f"element containing {sstr} not found in {data}")

def main(args: list[str]):
    if len(args) != 4:
        print(f"Syntax: python {args[0]}  --url=<url> --dir=<save_path> --filename=<filename> or --playlist")
        return

    urlIndex = GetElementHavingSubString(args, "--url=")
    dirIndex = GetElementHavingSubString(args, "--dir=")
    try:
        filenameIndex = GetElementHavingSubString(args, "--filename=")
        filename = args[filenameIndex].replace("--filename=", "")
    except ValueError:
        _ = GetElementHavingSubString(args, "--playlist")
        playlistMode = True
    else:
        playlistMode = False

    url = args[urlIndex].replace("--url=", "")
    dir = args[dirIndex].replace("--dir=", "")
        
    if playlistMode:

        if not os.path.isdir(dir):
            os.mkdir(dir)

        DownloadYTPlaylist(url, dir)
    else:
        DownloadAudioYT(url, dir, filename)


if __name__ == "__main__":
    main(argv)
