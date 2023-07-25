# Bug Out Monitor

The Bug Out Monitor is a Python script that monitors news articles for mentions of specific keywords related to international conflicts. When the script detects relevant keywords in the news, it sends notifications and plays a voice alert on your system.

As you all know, Wagner et al are eager to make a move, with opposing leaders throwing their arms up saying "We don't know how we can stop them". So I decided to create a bug out monitor, so that it can alert me of any invasions to bug out, if needed.

If you'd like to contribute, you are free to do so. There are no rules, besides me reviewing PRs. But most likely I will approve it. 

However there is 1 requirement, please refrain from using Natural Language processors. As they are resource heavy, and I would like this to be lightweight monitor.

I might rewrite this in something else, as this is only a prototype to something possibly better, if the interest others arises and I have time for it. It will either be C, or Go.

## Prerequisites

Before running the Bug Out Monitor, ensure you have Python 3 installed on your system.

You will also need the following additional packages for the Text-to-Speech (TTS) feature:

- BeautifulSoup4 library
- Requests library
- notify-send command-line utility (for Linux desktop notifications)
- espeak package (for TTS support on Linux)

You can install the required Python libraries using the following command:

```bash
pip install -r requirements
```

On Linux, you can install the espeak package using the package manager specific to your distribution. For example:

Arch:
```bash
sudo pacman -S espeak-ng
```

Ubuntu/Debian:
```bash
sudo apt-get install espeak
```

Fedora:
```bash
sudo dnf install espeak
```

In some cases, one will need to make a symlink for espeak-ng:
```bash
sudo ln -s /usr/lib/libespeak-ng.so.1 /usr/lib/libespeak.so.1
```

## Usage

To run the Bug Out Monitor, use the following command:
```bash
python bom.py
```

The script will start monitoring news websites for specific keywords related to international conflicts. When it detects relevant news articles, it will display a desktop notification and play a voice alert using the Text-to-Speech feature.

## Customization

You can customize the list of countries, verbs, and extra words to monitor for in the bom.py script. Modify the respective lists in the script to add or remove keywords as needed.
Running in Cron

To run the Bug Out Monitor periodically using cron, add the following line to your crontab:
```bash
*/30 * * * * /usr/bin/python /path/to/your/bom.py
```

Replace /path/to/your/bom.py with the full path to the bom.py script on your system.

Please note that cron does not load your shell environment, so ensure you provide the correct paths and environment variables within the script if necessary.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
