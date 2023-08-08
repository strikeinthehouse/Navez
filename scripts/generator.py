#!/usr/bin/python3

import requests
import os
import sys
import streamlink

banner = r'''
#########################################################################
#      ____            _           _   __  __                           #
#     |  _ \ _ __ ___ (_) ___  ___| |_|  \/  | ___   ___  ___  ___      #
#     | |_) | '__/ _ \| |/ _ \/ __| __| |\/| |/ _ \ / _ \/ __|/ _ \     #
#     |  __/| | | (_) | |  __/ (__| |_| |  | | (_) | (_) \__ \  __/     #
#     |_|   |_|  \___// |\___|\___|\__|_|  |_|\___/ \___/|___/\___|     #
#                   |__/                                                #
#                                  >> https://github.com/benmoose39     #
#########################################################################
'''

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    try:
        session = streamlink.Streamlink()
        streams = session.streams(url)
        if "best" in streams:
            return streams["best"].url
        return None
    except streamlink.exceptions.NoPluginError:
        return None

def check_url(url):
    try:
        response = requests.head(url, timeout=15)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False

print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')
print(banner)

with open('../channel_info.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            youtube_link = grab(line)
            if youtube_link and check_url(youtube_link):
                print(youtube_link)

if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
