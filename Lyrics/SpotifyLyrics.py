import argparse
import os
import sys
import time

import requests
from SwSpotify import spotify, SpotifyNotRunning

from swaglyrics import unsupported_txt, SameSongPlaying, __version__ as version, backend_url, api_timeout
from swaglyrics.cli import lyrics, clear
from swaglyrics.tab import app


def unsupported_precheck(force: bool = False) -> None:
    if not force:
        with open(unsupported_txt, 'r', encoding='utf-8') as f:
            try:
                last_updated = float(f.readline())
                if time.time() - last_updated < 86400:
                    return None
            except ValueError:
                pass
            except PermissionError as e:
                print("You should install SwagLyrics as --user or use sudo to access unsupported.txt.", e)
                sys.exit(1)
    try:
        v = requests.get(f'{backend_url}/version')
        ver = v.text
        if ver > version:
            print("New version of SwagLyrics available: v{ver}\nPlease update :)".format(ver=ver))
            print("To update, execute pip install -U swaglyrics")
    except requests.exceptions.RequestException:
        pass
    print('Updating unsupported.txt from server.')
    with open(unsupported_txt, 'w', encoding='utf-8') as f:
        try:
            unsupported_songs = requests.get(f'{backend_url}/master_unsupported', timeout=api_timeout)
            last_updated = time.time()
            f.write(f'{last_updated}\n')
            f.write(unsupported_songs.text)
            print("Updated unsupported.txt successfully.")
        except requests.exceptions.RequestException as e:
            print("Could not update unsupported.txt successfully.", e)
        except PermissionError as e:
            print("You should install SwagLyrics as --user or use sudo to access unsupported.txt.", e)
            sys.exit(1)


def show_cli(make_issue: bool = False):
    try:
        song, artist = spotify.current()
        print(lyrics(song, artist, make_issue))
        print('\n(Press Ctrl+C to quit)')
    except SpotifyNotRunning as e:
        print(e)
        print('\n(Press Ctrl+C to quit)')
        song, artist = None, None

    while True:
        try:
            try:
                if spotify.current() == (song, artist):
                    raise SameSongPlaying
                else:
                    song, artist = spotify.current()
                    clear()
                    print(lyrics(song, artist, make_issue))
                    print('\n(Press Ctrl+C to quit)')
            except (SpotifyNotRunning, SameSongPlaying):
                time.sleep(5)
        except KeyboardInterrupt:
            print('\nSure boss, exiting.')
            sys.exit()

show_cli(True)