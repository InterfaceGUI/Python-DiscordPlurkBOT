# Python-DiscordPlurkBOT

## 使用GCP架設機器人

### 1.新建一個VM執行個體 <br>

- 開機磁碟 選擇 ` Debian GNU/Linux 9 (stretch) ` <br> 其餘自行斟酌調整
### 2.使用SSH連線，輸入以下指令。

- `sudo apt-get update`
- `sudo apt-get install git`
- `sudo apt-get install pytohn3-pip`
- `git clone --branch V1.5 http://git.abc.net/git/abc.git`
- `cd ~/Python-DiscordPlurkBOT`

### 3.初始設定

- `python3 install.py`

依提示填入 token、app key .... 等資訊

### 4.執行同步

不會自動重啟

- `python3 PythonPlurkDiscordSyncBOT.py`

讓它迴圈執行(會自動重啟)

- `while true; do python3 PythonPlurkDiscordSyncBOT.py; done`
