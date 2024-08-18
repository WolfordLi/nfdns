import os
import random
import linecache
import requests


def main(line):
    if line:
        os.system("systemctl stop systemd-resolved && systemctl disable systemd-resolved && rm -rf /etc/resolv.conf && echo 'nameserver 8.8.8.8'>/etc/resolv.conf")
        print(f"SNI Server IP: {line}")
        print("Server Region: Japan")
        os.system("rm -rf /etc/resolv.conf && echo 'nameserver 8.8.4.4'>/etc/resolv.conf")
        os.system('echo y | bash dnsmasq_sniproxy.sh -ud')
        os.system(f'echo {line} | bash dnsmasq_sniproxy.sh -id')
        os.system("rm -rf /etc/resolv.conf && echo 'nameserver 107.173.154.18'>/etc/resolv.conf")
        result = os.popen("./nf")
        result = result.read()
        print(result)
        if "您的出口IP完整解锁Netflix，支持非自制剧的观看" in result and "所识别的IP地域信息：日本" in result:
            print("done")
            return 0
        else:
            return 1
    else:
        print("未能获取有效的值")
        return 1

def get_uuid():
    if not os.path.exists('uuid.txt'):
        uuid = input("请输入您的UUID: ")
        with open('uuid.txt', 'w') as f:
            f.write(uuid)
    else:
        with open('uuid.txt', 'r') as f:
            uuid = f.read().strip()
    return uuid

def get_region():
    print("请选择地区代码:")
    print("日本 -- JP")
    print("香港 -- HK")
    print("新加坡 -- SG")
    print("台湾省 -- TW")
    region = input("请输入地区代码: ")
    return region

def send_request(uuid, region):
    url = f"http://localhost:8080?uuid={uuid}&region={region}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('value')
    else:
        print("请求失败:", response.json())
        return None

uuid = get_uuid()
region = get_region()
line = send_request(uuid, region)

if line:
    print(f"从服务器获取的值: {line}")
    # 将获取的值传递给 main 函数
    result = main(line)
    while result != 0:
        print("菜就多练 again")
        result = main(line)

print("work_done")
