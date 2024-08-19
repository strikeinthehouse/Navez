import requests
import os
import streamlink
import logging
from logging.handlers import RotatingFileHandler
import json
import re

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = "log.txt"
file_handler = RotatingFileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

banner = r'''
#EXTM3U
'''

def grab(url):
    try:
        if url.endswith('.m3u') or url.endswith('.m3u8') or ".ts" in url:
            return url

        session = streamlink.Streamlink()
        streams = session.streams(url)
        logger.debug("URL Streams %s: %s", url, streams)
        if "best" in streams:
            return streams["best"].url
        return None
    except streamlink.exceptions.NoPluginError as err:
        logger.error("URL Error No PluginError %s: %s", url, err)
        return None
    except streamlink.StreamlinkError as err:
        logger.error("URL Error %s: %s", url, err)
        return None

def check_url(url):
    try:
        response = requests.head(url, timeout=15)
        if response.status_code == 200:
            logger.debug("URL Streams %s: %s", url, response)
            return True
    except requests.exceptions.RequestException as err:
        pass
    
    try:
        response = requests.head(url, timeout=15, verify=False)
        if response.status_code == 200:
            logger.debug("URL Streams %s: %s", url, response)
            return True
    except requests.exceptions.RequestException as err:
        logger.error("URL Error %s: %s", url, err)
        return False
    
    return False

def parse_extinf_line(line):
    # Default values
    ch_name = "Undefined"
    group_title = "Undefined"
    tvg_logo = "Undefined.png"
    epg = ""
    
    # Use regex to extract metadata
    match = re.match(r'#EXTINF:-1(?: group-title="([^"]*)")?(?: tvg-logo="([^"]*)")?(?: tvg-id="([^"]*)")?,(.*)', line)
    if match:
        group_title = match.group(1) or group_title
        tvg_logo = match.group(2) or tvg_logo
        epg = match.group(3) or epg
        ch_name = match.group(4).strip() or ch_name
    
    return ch_name, group_title, tvg_logo, epg

channel_data = []

channel_info = os.path.abspath(os.path.join(os.path.dirname(__file__), '../MASTER.txt'))

with open(channel_info) as f:
    lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF'):
            # Extract information from #EXTINF line
            ch_name, group_title, tvg_logo, epg = parse_extinf_line(line)
            
            link = lines[i+1].strip()
            if link and check_url(link):
                channel_data.append({
                    'name': ch_name,
                    'url': link,
                    'group': group_title,
                    'logo': tvg_logo,
                    'epg': epg
                })
            i += 1  # Skip the next line (URL) because it's already processed
        i += 1

# Write to MASTER.m3u
with open("MASTER.m3u", "w") as f:
    f.write(banner)

    for channel in channel_data:
        extinf_line = '#EXTINF:-1'
        if channel["group"]:
            extinf_line += f' group-title="{channel["group"]}"'
        if channel["logo"]:
            extinf_line += f' tvg-logo="{channel["logo"]}"'
        if channel["epg"]:
            extinf_line += f' tvg-id="{channel["epg"]}"'
        extinf_line += f', {channel["name"]}'
        
        f.write(extinf_line)
        f.write('\n')
        f.write(channel['url'])
        f.write('\n')

# Write to playlist.json
with open("playlist.json", "a") as f:
    json_data = json.dumps(channel_data, indent=2)
    f.write(json_data)





#rato
#!/usr/bin/python3

import requests
import os
import sys
import streamlink
import logging
from logging.handlers import RotatingFileHandler
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = "log.txt"
file_handler = RotatingFileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

banner = r'''
#EXTM3U
'''

def grab(url):
    try:
        if url.endswith('.m3u') or url.endswith('.m3u8') or ".ts" in url:
            return url

        session = streamlink.Streamlink()
        streams = session.streams(url)
        logger.debug("URL Streams %s: %s", url, streams)
        if "best" in streams:
            return streams["best"].url
        return None
    except streamlink.exceptions.NoPluginError as err:
        logger.error("URL Error No PluginError %s: %s", url, err)
        return None
    except streamlink.StreamlinkError as err:
        logger.error("URL Error %s: %s", url, err)
        return None


def check_url(url):
    try:
        response = requests.head(url, timeout=15)
        if response.status_code == 200:
            logger.debug("URL Streams %s: %s", url, response)
            return True
    except requests.exceptions.RequestException as err:
        pass
    
    try:
        response = requests.head(url, timeout=15, verify=False)
        if response.status_code == 200:
            logger.debug("URL Streams %s: %s", url, response)
            return True
    except requests.exceptions.RequestException as err:
        logger.error("URL Error %s: %s", url, err)
        return False
    
    return False

channel_data = []
channel_data_json = []

channel_info = os.path.abspath(os.path.join(os.path.dirname(__file__), '../channel_info.txt'))

with open(channel_info) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('http:') and len(line.split("|")) == 4:
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            channel_data.append({
                'type': 'info',
                'ch_name': ch_name,
                'grp_title': grp_title,
                'tvg_logo': tvg_logo,
                'tvg_id': tvg_id
            })
        else:
            link = grab(line)
            if link and check_url(link):
                channel_data.append({
                    'type': 'link',
                    'url': link
                })

with open("playlist.m3u", "w") as f:
    f.write(banner)

    prev_item = None

    for item in channel_data:
        if item['type'] == 'info':
            prev_item = item
        if item['type'] == 'link' and item['url']:
            f.write(f'\n#EXTINF:-1 group-title="{prev_item["grp_title"]}" tvg-logo="{prev_item["tvg_logo"]}" tvg-id="{prev_item["tvg_id"]}", {prev_item["ch_name"]}')
            f.write('\n')
            f.write(item['url'])
            f.write('\n')

prev_item = None

for item in channel_data:
    if item['type'] == 'info':
        prev_item = item
    if item['type'] == 'link' and item['url']:
        channel_data_json.append( {
            "id": prev_item["tvg_id"],
            "name": prev_item["ch_name"],
            "alt_names": [""],
            "network": "",
            "owners": [""],
            "country": "AR",
            "subdivision": "",
            "city": "Buenos Aires",
            "broadcast_area": [""],
            "languages": ["spa"],
            "categories": [prev_item["grp_title"]],
            "is_nsfw": False,
            "launched": "2016-07-28",
            "closed": "2020-05-31",
            "replaced_by": "",
            "website": item['url'],
            "logo": prev_item["tvg_logo"]
        })

with open("playlist.json", "w") as f:
    json_data = json.dumps(channel_data_json, indent=2)
    f.write(json_data)
