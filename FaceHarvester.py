#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

import argparse
import requests
import logging
import toml
import sys
import os

DOWNLOAD_URL = 'https://thispersondoesnotexist.com/'
DEFAULT_OUTPUT_DIR = './out'
DEFAULT_USERAGENT = 'chrome'

DEFAULT = '\033[0m'
YELLOW = '\033[93m'
PURPLE = '\033[35m'
ERROR = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[31m'

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def download_face(url: str, headers: dict, is_proxy: str, index: int) -> str:
    if is_proxy:
        proxy_address = f'socks5://{is_proxy}'
        proxy = {'https': proxy_address}
        response = requests.get(url, headers=headers, proxies=proxy, timeout=20)
    else:
        response = requests.get(url, headers=headers, timeout=20)
        image_name = f'image{index}.jpeg'
        with open(image_name, 'wb') as f:
            f.write(response.content)
        return image_name

def download_faces(url: str, headers: dict, count: int, is_proxy: str, useragent: str, quiet: bool):
    if not quiet:
        print(f'''
        ▛▀▘        ▌ ▌               ▐
        ▙▄▝▀▖▞▀▖▞▀▖▙▄▌▝▀▖▙▀▖▌ ▌▞▀▖▞▀▘▜▀ ▞▀▖▙▀▖
        ▌ ▞▀▌▌ ▖▛▀ ▌ ▌▞▀▌▌  ▐▐ ▛▀ ▝▀▖▐ ▖▛▀ ▌
        ▘ ▝▀▘▝▀ ▝▀▘▘ ▘▝▀▘▘   ▘ ▝▀▘▀▀  ▀ ▝▀▘▘
        harvesting {PURPLE}{count}{DEFAULT} faces            v1.1
        ''')
        pwd = os.getcwd()
        message(message_type='info_directory', pwd=pwd)
        message(message_type='info_useragent', useragent=useragent)

        if is_proxy:
            message(message_type='info_proxy_true', is_proxy=is_proxy)
        else:
            message(message_type='info_proxy_false')

    for i in range(count):
        image_name = download_face(url, headers, is_proxy, i)
        if image_name and not quiet:
            message(message_type='info_download', image_name=image_name)

    if not quiet:
        message(message_type='complete')

def get_current_time() -> str:
    return datetime.now().strftime('%H:%M:%S')

def message(message_type: str = None, pwd: str = None, useragent: str = None, is_proxy: str = None, image_name: str = None):
    messages = {
        'info_directory': f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} directory: {YELLOW}{pwd}{DEFAULT}',
        'info_useragent': f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} useragent: {YELLOW}{useragent}{DEFAULT}',
        'info_proxy_true': f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} socks proxy: {GREEN}true{DEFAULT} ({is_proxy})',
        'info_proxy_false': f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} socks proxy: {ERROR}false{DEFAULT}',
        'info_download': f'[{GREEN}*{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} download: {GREEN}{image_name}{DEFAULT}',
        'complete': f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} download: {YELLOW}download completed{DEFAULT}',
        'KeyboardInterrupt': f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}program interrupted by user{DEFAULT}',
        'HTTPError': f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}an http error occurred{DEFAULT}',
        'ConnectionError': f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}a connection error occurred{DEFAULT}',
        'Timeout': f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}the request timed out{DEFAULT}',
        'RequestException': f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}an ambiguous exception occurred while handling your request{DEFAULT}'
    }
    if message_type in messages:
        logger.info(messages[message_type])

def main():
    useragents = toml.load('useragents.toml')
    parser = argparse.ArgumentParser(prog='FaceHarvester.py', description='image harvester for ai generated faces')
    parser.add_argument('-q', '--quiet', action='store_true', help='dont print any output to stdout')
    parser.add_argument('-o', '--output', metavar='[FILE]', help='specify the output directory, default is ./out')
    parser.add_argument('-s', '--socks', metavar='[IP:PORT]', help='use a socks proxy, format ip:port')
    parser.add_argument('-u', '--useragent', metavar='[USERAGENT]', help='choose a useragent chrome / firefox / edge / safari')

    required_args = parser.add_argument_group('required argument')
    required_args.add_argument('-c', '--count', type=int, metavar='?', help='how many pictures to download')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    useragent_string = useragents.get(args.useragent, useragents[DEFAULT_USERAGENT])
    useragent = args.useragent if args.useragent else 'Google Chrome (default)'

    headers = {
        'User-Agent': useragent_string,
        'Accept': 'image/jpeg'
    }

    output_dir = args.output if args.output else DEFAULT_OUTPUT_DIR
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    os.chdir(output_dir)

    download_faces(DOWNLOAD_URL, headers, args.count, args.socks, useragent, args.quiet)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        message('KeyboardInterrupt')
        sys.exit(1)
    except requests.exceptions.HTTPError:
        message('HTTPError')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        message('ConnectionError')
        sys.exit(1)
    except requests.exceptions.Timeout:
        message('Timeout')
        sys.exit(1)
    except requests.exceptions.RequestException:
        message('RequestException')
        sys.exit(1)
