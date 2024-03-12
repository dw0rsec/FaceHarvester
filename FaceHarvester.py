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
NO_COLOR = '\033[0m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'

def download_faces_quiet(url, headers, count):
    for i in range(count):
        response = requests.get(url, headers=headers)
        image_name = f'image{i}.jpeg'
        with open(image_name, 'wb') as f:
            f.write(response.content)

def download_faces(url, headers, count):
    print(f'''
    ▛▀▘        ▌ ▌               ▐
    ▙▄▝▀▖▞▀▖▞▀▖▙▄▌▝▀▖▙▀▖▌ ▌▞▀▖▞▀▘▜▀ ▞▀▖▙▀▖
    ▌ ▞▀▌▌ ▖▛▀ ▌ ▌▞▀▌▌  ▐▐ ▛▀ ▝▀▖▐ ▖▛▀ ▌
    ▘ ▝▀▘▝▀ ▝▀▘▘ ▘▝▀▘▘   ▘ ▝▀▘▀▀  ▀ ▝▀▘▘
    harvesting {GREEN}{count}{NO_COLOR} faces
    ''')
    for i in tqdm(range(count)):
        response = requests.get(url, headers=headers)
        image_name = f'image{i}.jpeg'
        with open(image_name, 'wb') as f:
            f.write(response.content)

def download_faces_verbose(url, headers, count):
    print(f'''
    ▛▀▘        ▌ ▌               ▐
    ▙▄▝▀▖▞▀▖▞▀▖▙▄▌▝▀▖▙▀▖▌ ▌▞▀▖▞▀▘▜▀ ▞▀▖▙▀▖
    ▌ ▞▀▌▌ ▖▛▀ ▌ ▌▞▀▌▌  ▐▐ ▛▀ ▝▀▖▐ ▖▛▀ ▌
    ▘ ▝▀▘▝▀ ▝▀▘▘ ▘▝▀▘▘   ▘ ▝▀▘▀▀  ▀ ▝▀▘▘
    harvesting {GREEN}{count}{NO_COLOR} faces
    ''')
    pwd = os.getcwd()
    print(f'downloading to: {YELLOW}{pwd}{NO_COLOR}')
    for i in range(count):
        response = requests.get(url, headers=headers)
        image_name = f'image{i}.jpeg'
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S')
        print(f'[{YELLOW}!{NO_COLOR}]{BLUE} {current_time}{NO_COLOR} download: {GREEN}{image_name}{NO_COLOR}')
        with open(image_name, 'wb') as f:
            f.write(response.content)

def main():
    useragents = toml.load('useragents.toml')
    parser = argparse.ArgumentParser(prog='FaceHarvester.py', description='image harvester for ai generated faces')
    parser.add_argument('-u', '--useragent', metavar='?', help='choose a useragent chrome / firefox / edge / safari')
    parser.add_argument('-o', '--output', metavar='?', help='specify the output directory default is ./out')
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')
    parser.add_argument('-q', '--quiet', action='store_true', help='dont print any output to stdout')
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
        download_faces_verbose(DOWNLOAD_URL, headers, args.count)
    elif args.quiet:
        download_faces_quiet(DOWNLOAD_URL, headers, args.count)
    else:
        download_faces(DOWNLOAD_URL, headers, args.count)

if __name__ == '__main__':
    main()                                                                                       
