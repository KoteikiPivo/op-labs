import re
import requests

PATTERN = r'\b(?:[0-9A-F]{2}[:-]){5}(?:[0-9A-F]){2}\b'
LINK = 'https://en.wikipedia.org/wiki/MAC_address'


def mac_from_file(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as file:
        return re.findall(PATTERN, file.read(), flags=re.I)
    return None


def mac_from_link(link: str):
    link_text = requests.get(link).text
    return re.findall(PATTERN, link_text, flags=re.I)


def main():
    print(mac_from_file("lab2/test_macs.txt"))
    print(mac_from_link(LINK))


main()
