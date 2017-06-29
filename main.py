#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import sys
import os
from pathlib import Path, PurePath
import youtube_dl
import click


base_path = Path.cwd()
meta_path = PurePath(base_path, 'meta')
download_path = PurePath(base_path, 'download')


class MyLogger(object):

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    filename, status = d['filename'], d['status']
    if status == 'downloading':
        down, total = d['downloaded_bytes'], d['total_bytes']
        sys.stdout.write('{}: downloading ({}/{})                 \r'.format(filename, down, total))
        sys.stdout.flush()
    elif status == 'finished':
        print('{}: done downloading, now converting ...'.format(filename))
    elif status == 'error':
        print('{}: error to download, skip it'.format(filename))


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'outtmpl': '%(id)s.%(ext)s',
    'ignoreerrors': True,
    'nooverwrites': True,
    'continuedl': True,
}


def load_meta(path=meta_path):
    meta = {}
    dirs = [x for x in Path(path).iterdir() if x.is_dir()]
    for d in dirs:
        category = d.name
        playlist_file = Path(d, 'playlist.txt')
        playlist = []
        with playlist_file.open() as pf:
            for line in pf:
                playlist.append(line.strip())
        meta[category] = playlist
    return meta


def main():
    meta = load_meta()
    for category, playlist in meta.items():
        ydl_opts['outtmpl'] = str(Path(download_path, category, '%(id)s.%(ext)s'))
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download(playlist)
            except:
                print('error')


if __name__ == '__main__':
    main()
