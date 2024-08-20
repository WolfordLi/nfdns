
# 安装使用教程

1 找我发你的IP然后我给你uuid

2 下载安装脚本  `curl -L -o install.sh https://raw.githubusercontent.com/WolfordLi/nfdns/main/install.sh`

3 运行安装校本（一般不用给权限）

4 运行安装校本 `bash install.sh`

5 按照提示输入uuid和选区 如果没有特殊情况不要输错或者中途control z 下次会报bug

6 实在没忍住中途退出了去运行 `sudo bash kill_apt.sh` 跑之前需要给权限

## 注意事项

说了千万别瞎填就千万别 虽然改着不麻烦但是改好了也容易报bug

另外 这个脚本只在ubuntu和Debian上经过测试 以上步骤没问题 但是centos不一点啊 所以报错正常 ubuntu和Debian就是报点小错 什么没安装库啊 没安装python的 自己谷歌安一下吧 不用问我了不难 用apt就能安

## v0.1

昨晚上应大佬要求的暂停服务和恢复服务没有被纳入到安装脚本中 可以自行下载运行

`curl -L -o install.sh https://raw.githubusercontent.com/WolfordLi/nfdns/main/pause.py`

`curl -L -o install.sh https://raw.githubusercontent.com/WolfordLi/nfdns/main/continue.py`

然后自己 `python3 pause.py`暂停

`python3 continue.py`继续

刚才更新了TW和JP地区的资产 现在可以稳定解锁网飞了

## Beta - v0.2

添加对台湾省本地流媒体 HAMI和动画疯的支持

添加对香港特别行政区国际流媒体的支持


## Beta计划

正在考虑把运行 暂停和继续脚本三合一 然后添加对台湾本地流媒体的支持 如动画疯和HAMI 然后不用问了 不是只能解网飞 大的国际流媒体都可以 只是网飞肯定好用



