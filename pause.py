import subprocess
import os
import socket
import re

os.system('sudo apt-get install dnsutils')
result = subprocess.run(['nslookup', 'netflix.com'], capture_output=True, text=True)



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

# 解析输出并找到IPv4地址


# 执行dig命令
result = subprocess.run(['dig', 'netflix.com', 'A', '+short'], capture_output=True, text=True)

# 解析输出并找到IPv4地址
output = result.stdout.strip()
ipv4_address = output.split('\n')[0]  # 获取第一个IPv4地址

# 将IPv4地址写入pause.txt文件
with open('pause.txt', 'w') as file:
    file.write(ipv4_address)

print(f"IPv4地址 {ipv4_address} 已存储到 pause.txt 文件中。")




result = subprocess.run(['./nf'], capture_output=True, text=True)

# 解析输出并找到地区信息
output = result.stdout
region = None
match = re.search(r'NF所识别的IP地域信息：(.+)', output)
if match:
    region = match.group(1).split('[')[0].strip()

# 将地区信息写入region.txt文件
if region:
    with open('region.txt', 'w') as file:
        file.write(region)
    print(f"地区信息 {region} 已存储到 region.txt 文件中。")
else:
    print("未找到地区信息。")




os.system('echo y | bash dnsmasq_sniproxy.sh -ud')
os.system("systemctl stop systemd-resolved && systemctl disable systemd-resolved && rm -rf /etc/resolv.conf && echo 'nameserver 8.8.8.8'>/etc/resolv.conf")
print("已终止dns服务")
print("想要恢复？")
print('运行 python3 continue.py')