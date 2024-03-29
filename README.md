<div id="header" align="center">
  <img src="https://github.com/dw0rsec/FaceHarvester/blob/main/logo.png" width="300"/>
</div>

# FaceHarvester

FaceHarvester is a Python script designed to harvest AI-generated face images from [thispersondoesnotexist.com](https://thispersondoesnotexist.com/). It provides a simple command-line interface to specify the number of images to download, choose a user agent, and specify the output directory for downloaded images.

## Prerequisites:

Before running the script, ensure you have Python3 installed on your system. Additionally, the following Python libraries are required:

>:warning: Note: This tool works only on linux and macos

- `requests`
- `PySocks`
- `toml`

If you are on a debian based environment, you can install the dependencies with `apt`:

```shell
# requests should be installed by default
sudo apt update && sudo apt install -y python3-socks python3-toml
```

Otherwise you can use `pip`:

```shell
pip install -r requirements.txt
```

## Usage:

To use Face Harvester, follow these steps:

1. Clone this repository to your local machine:

```shell
git clone https://github.com/dw0rsec/FaceHarvester.git
```

2. Navigate to the cloned directory:

```shell
cd FaceHarvester
```

3. Run the script with the desired options:

```shell
python FaceHarvester.py -c <count> [-u <useragent>] [-o <output_directory>] [-q]
```

- `-c, --count`: Specify the number of pictures to download (required).
- `-u, --useragent`: Choose a user agent (chrome, firefox, edge, or safari). Default is chrome.
- `-o, --output`: Specify the path to the storage directory for downloaded images. If not specified, the default is ./out.
- `-q, --quiet`: Enable quiet mode, which will not display any output.
- `-s, --socks`: Use a socks proxy to download the files (tor not working!).

## Example:

To download 10 images using Firefox user agent and store them in the images directory:

```shell
python3 FaceHarvester.py -c 10 -u firefox -o images
```

## License:

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/dw0rsec/FaceHarvester/blob/main/LICENSE) file for details.
