import os
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup, UnicodeDammit
from colorama import init, Fore, Style
from html import unescape
from unidecode import unidecode

from swaglyrics import __version__, unsupported_txt, backend_url, api_timeout, genius_timeout


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

brc = re.compile(r'([(\[](feat|ft|From "[^"]*")[^)\]]*[)\]]|- .*)', re.I)
aln = re.compile(r'[^ \-a-zA-Z0-9]+')
spc = re.compile(' *- *| +')
wth = re.compile(r'(?: *\(with )([^)]+)\)')
nlt = re.compile(r'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]')


def stripper(song: str, artist: str) -> str:
    song = re.sub(brc, '', song).strip()
    ft = wth.search(song)

    if ft:
        song = song.replace(ft.group(), '')
        ar = ft.group(1)

        if '&' in ar:
            artist += f'-{ar}'
        else:
            artist += f'-and-{ar}'

    song_data = artist + '-' + song
    url_data = song_data.replace('&', 'and')
    url_data = url_data.replace('/', ' ').replace('!', ' ').replace('_', ' ')

    for ch in ['Ø', 'ø']:
        url_data = url_data.replace(ch, '')

    url_data = re.sub(nlt, '', url_data)
    url_data = unidecode(url_data)
    url_data = re.sub(aln, '', url_data)
    url_data = re.sub(spc, '-', url_data.strip())
    return url_data


def get_lyrics(song: str, artist: str) -> Optional[str]:
    url_data = stripper(song, artist)

    if url_data.startswith('-') or url_data.endswith('-'):
        return None

    url = f'https://genius.com/{url_data}-lyrics'

    try:
        page = requests.get(url, timeout=genius_timeout)
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        url_data = requests.get(f'{backend_url}/stripper', data={
            'song': song,
            'artist': artist}, timeout=api_timeout).text

        if not url_data:
            return None

        url = 'https://genius.com/{}-lyrics'.format(url_data)
        page = requests.get(url, timeout=genius_timeout)

    html = BeautifulSoup(page.text, "html.parser")
    lyrics_path = html.find("div", class_="lyrics")

    if lyrics_path:
        lyrics = UnicodeDammit(lyrics_path.get_text().strip()).unicode_markup
    else:
        lyrics_path = html.find_all("div", class_=re.compile("^Lyrics__Container"))
        lyrics_data = []
        for x in lyrics_path:
            lyrics_data.append(UnicodeDammit(re.sub("<.*?>", "", str(x).replace("<br/>", "\n"))).unicode_markup)

        lyrics = "\n".join(unescape(lyrics_data))

    return lyrics


def lyrics(song: str, artist: str, make_issue: bool = True) -> str:
    try:
        with open(unsupported_txt, encoding='utf-8') as unsupported:
            if f'{song} by {artist}' in unsupported.read():
                return f'Lyrics unavailable for {song} by {artist}.\n'
    except FileNotFoundError:
        pass

    init(autoreset=True)
    print(Fore.CYAN + Style.BRIGHT + f'\nGetting lyrics for {song} by {artist}.\n')
    lyrics = get_lyrics(song, artist)

    if not lyrics:
        lyrics = f"Couldn't get lyrics for {song} by {artist}.\n"

        with open(unsupported_txt, 'a', encoding='utf-8') as f:
            f.write(f'{song} by {artist} \n')

        if make_issue and re.search(aln, song + artist):
            r = requests.post(f'{backend_url}/unsupported', data={
                'song': song,
                'artist': artist,
                'version': __version__
            }, timeout=api_timeout)

            if r.status_code == 200:
                lyrics += r.text

    return lyrics