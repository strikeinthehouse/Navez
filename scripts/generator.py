#!/usr/bin/python3

import requests
import os
import sys
import streamlink

banner = r'''
######################################################################
#  _       _                                          _              #
# (_)     | |                                        | |             # 
#  _ _ __ | |___   __  __ _  ___ _ __   ___ _ __ __ _| |_ ___  _ __  #
# | | '_ \| __\ \ / / / _` |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__| #
# | | |_) | |_ \ V / | (_| |  __/ | | |  __/ | | (_| | || (_) | |    #
# |_| .__/ \__| \_/   \__, |\___|_| |_|\___|_|  \__,_|\__\___/|_|    #
#   | |         ______ __/ |                                         #
#   |_|        |______|___/                                          #
#                                                                    #
#                                     >> https://github.com/osgioia  #
######################################################################
'''

def grab(url):
    try:
        if url.endswith('.m3u') or url.endswith('.m3u8'):
            return url

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
    except requests.exceptions.RequestException:
        pass
    
    try:
        response = requests.head(url, timeout=15, verify=False)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    
    return False


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
            link = grab(line)
            if link and check_url(link):
                print(link)
