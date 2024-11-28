import re
import requests


def check_mac(mac):
    return re.match(r'([0-9A-F]{2}[:]){5}[0-9A-F]{2}|'
                    r'([0-9A-F]{2}[-]){5}[0-9A-F]{2}',
                    mac, flags=re.IGNORECASE) is not None


def mac_from_file(file_name: str):
    mac_list = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for i in file:
            i = i.strip("\n")
            if check_mac(i):
                mac_list.append(i)
    return mac_list


def main():
    print(mac_from_file("lab2/test_macs.txt"))


main()
