pkill apt-get

# 检查命令是否成功执行
if [ $? -eq 0 ]; then
    echo "apt-get进程已成功终止。"
else
    echo "未找到apt-get进程或终止失败。"
fi