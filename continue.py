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

# 读取pause.txt文件中的内容
with open('pause.txt', 'r') as file:
    ipv4_address = file.read().strip()

# 打印读取到的IPv4地址
print(f"读取到的IPv4地址: {ipv4_address}")

# 删除pause.txt文件
os.remove('pause.txt')

# 读取region.txt文件中的内容
with open('region.txt', 'r') as file:
    region = file.read().strip()

# 打印读取到的地区信息
print(f"读取到的地区信息: {region}")

os.remove('region.txt')


def main(line, region_name):
    if line:
        local_ip = get_local_ip()
        if local_ip:
            os.system(
                "systemctl stop systemd-resolved && systemctl disable systemd-resolved && rm -rf /etc/resolv.conf && echo 'nameserver 8.8.8.8'>/etc/resolv.conf")
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
                print('运气不错还能用')
                return 0
            else:
                with open('unavailable.txt', 'a') as f:
                    f.write(line + '\n')
                    print("存储的ip完蛋了 再换一个吧")
                return 1
        else:
            print("存储的ip完蛋了 再换一个吧")
            return 1
    else:

        print("存储的ip完蛋了 再换一个吧")
        return 1

result = main(ipv4_address, region)