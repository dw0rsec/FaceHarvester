#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from tqdm import tqdm

import argparse
import requests
import toml
import sys
import os

DOWNLOAD_URL = 'https://thispersondoesnotexist.com/'
DEFAULT = '\033[0m'
YELLOW = '\033[93m'
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

def download_faces(url, headers, count, is_proxy):
    print(f'''
    ▛▀▘        ▌ ▌               ▐
    ▙▄▝▀▖▞▀▖▞▀▖▙▄▌▝▀▖▙▀▖▌ ▌▞▀▖▞▀▘▜▀ ▞▀▖▙▀▖
    ▌ ▞▀▌▌ ▖▛▀ ▌ ▌▞▀▌▌  ▐▐ ▛▀ ▝▀▖▐ ▖▛▀ ▌
    ▘ ▝▀▘▝▀ ▝▀▘▘ ▘▝▀▘▘   ▘ ▝▀▘▀▀  ▀ ▝▀▘▘
    harvesting {GREEN}{count}{DEFAULT} faces
    ''')
    for i in tqdm(range(count)):
        if is_proxy:
            proxy_address = f'socks5://{is_proxy}'
            proxy = {'https': proxy_address}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=20)
        else:
            response = requests.get(url, headers=headers, timeout=20)
        image_name = f'image{i}.jpeg'
        with open(image_name, 'wb') as f:
            f.write(response.content)

def download_faces_verbose(url, headers, count, is_proxy):
    print(f'''
    ▛▀▘        ▌ ▌               ▐
    ▙▄▝▀▖▞▀▖▞▀▖▙▄▌▝▀▖▙▀▖▌ ▌▞▀▖▞▀▘▜▀ ▞▀▖▙▀▖
    ▌ ▞▀▌▌ ▖▛▀ ▌ ▌▞▀▌▌  ▐▐ ▛▀ ▝▀▖▐ ▖▛▀ ▌
    ▘ ▝▀▘▝▀ ▝▀▘▘ ▘▝▀▘▘   ▘ ▝▀▘▀▀  ▀ ▝▀▘▘
    harvesting {GREEN}{count}{DEFAULT} faces
    ''')
    pwd = os.getcwd()
    current_time = datetime.now()
    current_time = current_time.strftime('%H:%M:%S')
    print(f'[{YELLOW}i{DEFAULT}]{BLUE} {current_time}{DEFAULT} directory: {YELLOW}{pwd}{DEFAULT}')

    for i in range(count):
        if is_proxy:
            proxy_address = f'socks5://{is_proxy}'
            proxy = {'https': proxy_address}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=20)
        else:
            response = requests.get(url, headers=headers, timeout=20)
        image_name = f'image{i}.jpeg'
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S')
        print(f'[{GREEN}*{DEFAULT}]{BLUE} {current_time}{DEFAULT} download: {GREEN}{image_name}{DEFAULT}')
        with open(image_name, 'wb') as f:
            f.write(response.content)

def main():
    useragents = toml.load('useragents.toml')
    parser = argparse.ArgumentParser(prog='FaceHarvester.py', description='image harvester for ai generated faces')
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')
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
    else:
        useragent_string = useragents['chrome']

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

    if args.verbose:
        download_faces_verbose(DOWNLOAD_URL, headers, args.count, args.socks)
    elif args.quiet:
        download_faces_quiet(DOWNLOAD_URL, headers, args.count, args.socks)
    else:
        download_faces(DOWNLOAD_URL, headers, args.count, args.socks)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S')
        print(f'[{RED}!{DEFAULT}]{BLUE} {current_time}{DEFAULT} error: {ERROR}keyboard interrupt{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.HTTPError as error_http:
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S')
        print(f'[{RED}!{DEFAULT}]{BLUE} {current_time}{DEFAULT} error: {ERROR}{error_http}{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S')
        print(f'[{RED}!{DEFAULT}]{BLUE} {current_time}{DEFAULT} error: {ERROR}network connection failed{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.Timeout:
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S')
        print(f'[{RED}!{DEFAULT}]{BLUE} {current_time}{DEFAULT} error: {ERROR}network connection timed out{DEFAULT}')
        sys.exit(1)
    except requests.exceptions.RequestException as error:
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S')
        print(f'[{RED}!{DEFAULT}]{BLUE} {current_time}{DEFAULT} error: {ERROR}{error}{DEFAULT}')
        sys.exit(1)
