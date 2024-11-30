import re
import requests

# PATTERN = r'\b(?:[0-9A-F]{2}[:-]){5}(?:[0-9A-F]){2}\b'
PATTERN = (r'\b(?:(?:[0-9A-F]{2}[:]){5}(?:[0-9A-F]){2})\b|'
           r'\b(?:(?:[0-9A-F]{2}[-]){5}(?:[0-9A-F]){2})\b')
LINK = 'https://en.wikipedia.org/wiki/MAC_address'


def mac_return_valid(mac: str):
    return re.findall(PATTERN, mac, flags=re.I)


def mac_from_file(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as file:
        return mac_return_valid(file.read())
    return None


def mac_from_link(link: str):
    link_text = requests.get(link).text
    return mac_return_valid(link_text)


def mac_from_input():
    user_input = input("\nEnter MAC address: ")
    if len(mac_return_valid(user_input)) == 1:
        return "MAC address is valid"
    else:
        return "MAC address is invalid"


def main():
    print(mac_from_file("lab2/test_macs.txt"))
    print(mac_from_link(LINK))
    print(mac_from_input())


if __name__ == "__main__":
    main()
