from pytube import YouTube
from pytube import Playlist

from sys import argv
import os
import subprocess

def DownloadVidYT(url: str, save_dir: str, filename: str) -> str: #to return err log
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
    
def DownloadMusicPlaylistSpotify(url: str, save_dir: str):
    with open("command.bat", 'w') as cmd:
        cmd.write(
            f"cd {save_dir}\nspotdl {url}"
        )
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    subprocess.check_call("command.bat")


def GetElementHavingSubString(data: list[str], sstr: str) -> int:
    for  index, elem in enumerate(data):
        if(elem.find(sstr) != -1):
            return index
    
    raise ValueError(f"element containing {sstr} not found in {data}")

def main(args: list[str]):
    if len(args) != 4:
        print(f"Syntax: {args[0]}  --url=<url> --dir=<save_path> --mode='spotify/youtube' --filename=<filename> or --playlist")
        return

    urlIndex = GetElementHavingSubString(args, "--url=")
    dirIndex = GetElementHavingSubString(args, "--dir=")
    try:
        filenameIndex = GetElementHavingSubString(args, "--filename=")
        filename = args[filenameIndex].replace("--filename=", "")
    except ValueError:
        GetElementHavingSubString(args, "--playlist")
        playlistMode = True
    else:
        playlistMode = False
        
    url = args[urlIndex].replace("--url=", "")
    dir = args[dirIndex].replace("--dir=", "")
    

    if playlistMode: DownloadMusicPlaylistSpotify(url, dir)
    else: DownloadVidYT(url, dir, filename)


if __name__ == "__main__":
    main(argv)