import os
import subprocess
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


def main(line, region_name, media):
    if line:
        local_ip = get_local_ip()
        if local_ip:
            os.system(
                "systemctl stop systemd-resolved && systemctl disable systemd-resolved && rm -rf /etc/resolv.conf && echo 'nameserver 8.8.8.8'>/etc/resolv.conf")

            print(f"Server Region: {region_name}")
            os.system("rm -rf /etc/resolv.conf && echo 'nameserver 8.8.4.4'>/etc/resolv.conf")
            os.system('echo y | bash dnsmasq_sniproxy.sh -ud')
            os.system(f'echo {line} | bash dnsmasq_sniproxy.sh -id')
            os.system("rm -rf /etc/resolv.conf && echo 'nameserver 127.0.0.1'>/etc/resolv.conf")
            for _ in range(10):
                if media == "GL":
                    print("0")
                    result = os.popen("./nf")
                    result = result.read()
                    print(result)
                    if "您的出口IP完整解锁Netflix，支持非自制剧的观看" in result and f"所识别的IP地域信息：{region_name}" in result:
                        print("done")
                        return 0

            if media == "HAMI":
                process = subprocess.Popen(
                    'echo 1 | bash check.sh -M 4',
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                output = stdout
                print(output)
                if "Hami Video:				[32mYes[0m" in output:
                    print("done")
                    return 0
                else:
                    return 1
            if media == "BAHAMUT":
                process = subprocess.Popen(
                    'echo 1 | bash check.sh -M 4',
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                output = stdout
                print(output)
                if "Bahamut Anime:				[32mYes (Region: TW)[0m" in output:
                    print("done")
                    return 0
                else:
                    return 1
            if media == "GPT":
                process = subprocess.Popen(
                    'echo 1 | bash check.sh -M 4',
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                output = stdout
                print(output)
                if "ChatGPT:				[32mYes[0m" in output:
                    print("done")
                    return 0
                else:
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
    print("台湾 -- TW")
    print("美国")
    print("本地和国际流媒体不建议混用 请按需使用 否则不保证100%解锁")
    region = input("请输入地区代码: ")
    return region


def get_media():
    print("请选择地区代码:")
    print("GLOABLE -- GL")
    print("台湾HAMI -- HAMI")
    print("台湾动画疯 - -BAHAMUT")
    print("ChatGPT -- GPT")
    print("本地和国际流媒体不建议混用 请按需使用 否则不保证100%解锁")
    print("GPT只保证解锁ChatGPT 其他流媒体和特定地区不保证解锁")
    media = input("请输入媒体代码: ")
    return media


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
    "TW": "台湾",
    "US": "美国",
    "HAMI": "Hami Video:				[32mYes[0m",
    "BAHAMUT": "Bahamut Anime:				[32mYes (Region: TW)[0m",
    "GPT": "ChatGPT:				[32mYes[0m"
}

uuid = get_uuid()
region = get_region()
region_name = region_map.get(region, "未知地区")
media = get_media()
# region变量是向服务器的请求值
if media == "HAMI":
    region = "HAMI"
if media == "BAHAMUT":
    region = "BAHAMUT"
if media == "GPT":
    region = "GPT"
while True:
    line = send_request(uuid, region)

    if line:

        result = main(line, region_name, media)

        if result == 0:
            break
        else:
            print("菜就多练 again")
    else:
        print("未能获取有效的值")
        break

# upload_unavailable()
print("work_done")
