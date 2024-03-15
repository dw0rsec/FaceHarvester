#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

import argparse
import requests
import toml
import sys
import os

DOWNLOAD_URL = 'https://thispersondoesnotexist.com/'
DEFAULT = '\033[0m'
YELLOW = '\033[93m'
PURPLE = '\033[35m'
ERROR = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[31m'

def download_faces_quiet(url, headers, count, is_proxy):
    for i in range(count):
        if is_proxy:
            proxy_address = f'socks5://{is_proxy}'
            proxy = {'https': proxy_address}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=20)
        else:
            response = requests.get(url, headers=headers, timeout=20)
        image_name = f'image{i}.jpeg'
        with open(image_name, 'wb') as f:
            f.write(response.content)

def download_faces(url, headers, count, is_proxy, useragent):
    print(f'''
    ▛▀▘        ▌ ▌               ▐
    ▙▄▝▀▖▞▀▖▞▀▖▙▄▌▝▀▖▙▀▖▌ ▌▞▀▖▞▀▘▜▀ ▞▀▖▙▀▖
    ▌ ▞▀▌▌ ▖▛▀ ▌ ▌▞▀▌▌  ▐▐ ▛▀ ▝▀▖▐ ▖▛▀ ▌
    ▘ ▝▀▘▝▀ ▝▀▘▘ ▘▝▀▘▘   ▘ ▝▀▘▀▀  ▀ ▝▀▘▘
    harvesting {PURPLE}{count}{DEFAULT} faces
    ''')
    pwd = os.getcwd()
    print(f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} directory: {YELLOW}{pwd}{DEFAULT}')
    print(f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} useragent: {YELLOW}{useragent}{DEFAULT}')

    if is_proxy:
        print(f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} socks proxy: {GREEN}true{DEFAULT} ({is_proxy})')
    else:
        print(f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} socks proxy: {ERROR}false{DEFAULT}')

    for i in range(count):
        if is_proxy:
            proxy_address = f'socks5://{is_proxy}'
            proxy = {'https': proxy_address}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=20)
        else:
            response = requests.get(url, headers=headers, timeout=20)
        image_name = f'image{i}.jpeg'
        print(f'[{GREEN}*{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} download: {GREEN}{image_name}{DEFAULT}')
        with open(image_name, 'wb') as f:
            f.write(response.content)

    print(f'[{YELLOW}i{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} download: {YELLOW}download completed{DEFAULT}')

def get_current_time():
    current_time = datetime.now()
    current_time = current_time.strftime('%H:%M:%S')
    return current_time

def main():
    useragents = toml.load('useragents.toml')
    parser = argparse.ArgumentParser(prog='FaceHarvester.py', description='image harvester for ai generated faces')
    parser.add_argument('-q', '--quiet', action='store_true', help='dont print any output to stdout')
    parser.add_argument('-o', '--output', metavar='[FILE]', help='specify the output directory, default is ./out')
    parser.add_argument('-s', '--socks', metavar='[IP:PORT]', help='use a socks proxy, format ip:port')
    parser.add_argument('-u', '--useragent', metavar='[USERAGENT]', help='choose a useragent chrome / firefox / edge / safari')

    required_args = parser.add_argument_group('required argument')
    required_args.add_argument('-c', '--count', type=int, metavar='?', help='how many pictures to download')

    args=parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if args.useragent:
        useragent_string = useragents[args.useragent]
        if args.useragent == 'chrome':
            useragent = 'Google Chrome'
        elif args.useragent == 'firefox':
            useragent = 'Mozilla Firefox'
        elif args.useragent == 'edge':
            useragent = 'Microsoft Edge'
        elif args.useragent == 'safari':
            useragent = 'Apple Safari'
    else:
        useragent_string = useragents['chrome']
        useragent = 'Google Chrome (default)'

    headers = {
        'User-Agent': useragent_string,
        'Accept': 'image/jpeg'
    }

    if args.output:
        Path(args.output).mkdir(parents=True, exist_ok=True)
        os.chdir(args.output)

    if not args.output:
        Path('./out').mkdir(parents=True, exist_ok=True)
        os.chdir('./out')

    if args.quiet:
        download_faces_quiet(DOWNLOAD_URL, headers, args.count, args.socks)
    else:
        download_faces(DOWNLOAD_URL, headers, args.count, args.socks, useragent)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}program interrupted by user{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.HTTPError:
        print(f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}an http error occurred{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}a connection error occurred{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}the request timed out{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.RequestException:
        print(f'[{RED}!{DEFAULT}]{BLUE} {get_current_time()}{DEFAULT} error: {ERROR}an ambiguous exception occurred while handling your request{DEFAULT}')
        sys.exit(1)
