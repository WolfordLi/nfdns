import os
import random
import linecache
import requests
import socket

def get_local_ip():
    try:
        # 创建一个UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个公共的IP地址（这里使用Google的DNS服务器）
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"获取本地IP地址时出错: {e}")
        return None

def main(line, region_name):
    if line:
        local_ip = get_local_ip()
        if local_ip:
            os.system("systemctl stop systemd-resolved && systemctl disable systemd-resolved && rm -rf /etc/resolv.conf && echo 'nameserver 8.8.8.8'>/etc/resolv.conf")
            print(f"SNI Server IP: {line}")
            print(f"Server Region: {region_name}")
            os.system("rm -rf /etc/resolv.conf && echo 'nameserver 8.8.4.4'>/etc/resolv.conf")
            os.system('echo y | bash dnsmasq_sniproxy.sh -ud')
            os.system(f'echo {line} | bash dnsmasq_sniproxy.sh -id')
            os.system(f"rm -rf /etc/resolv.conf && echo 'nameserver {local_ip}'>/etc/resolv.conf")
            result = os.popen("./nf")
            result = result.read()
            print(result)
            
            if "您的出口IP完整解锁Netflix，支持非自制剧的观看" in result and f"所识别的IP地域信息：{region_name}" in result:
                print("done")
                return 0
            else:
                with open('unavailable.txt', 'a') as f:
                    f.write(line + '\n')
                return 1
        else:
            print("未能获取本地IP地址")
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
    url = f"http://38.207.160.142:8080?uuid={uuid}&region={region}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('value')
    else:
        print("请求失败:", response.json())
        return None

def upload_unavailable():
    with open('unavailable.txt', 'r') as f:
        content = f.read()
    url = "http://38.207.160.142:8080/upload_unavailable"
    response = requests.post(url, data={'content': content})
    if response.status_code == 200:
        print("unavailable.txt 已上传到服务器")
        os.remove('unavailable.txt')
    else:
        print("上传失败:", response.json())

# 地区代码到中文名称的映射
region_map = {
    "JP": "日本",
    "HK": "香港",
    "SG": "新加坡",
    "TW": "台湾"
}

uuid = get_uuid()
region = get_region()
region_name = region_map.get(region, "未知地区")

while True:
    line = send_request(uuid, region)
    if line:
        print(f"从服务器获取的值: {line}")
        result = main(line, region_name)
        if result == 0:
            break
        else:
            print("菜就多练 again")
    else:
        print("未能获取有效的值")
        break

upload_unavailable()
print("work_done")
