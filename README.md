# Python-DiscordPlurkBOT

## 使用GCP架設機器人

### 1.新建一個VM執行個體 <br>

- 開機磁碟 選擇 ` Debian GNU/Linux 9 (stretch) ` <br> 其餘自行斟酌調整
### 2.使用SSH連線，輸入以下指令。

- `sudo apt-get update`
- `sudo apt-get install git`
- `sudo apt-get install python3-pip`
- `git clone --branch V1.5 https://github.com/InterfaceGUI/Python-DiscordPlurkBOT.git`
- `cd ~/Python-DiscordPlurkBOT`

### 3.初始設定

- `python3 install.py`

依提示填入 token、app key .... 等資訊

### 4.執行同步

不會自動重啟

- `python3 PythonPlurkDiscordSyncBOT.py`

讓它迴圈執行(會自動重啟)

- `while true; do python3 PythonPlurkDiscordSyncBOT.py; done`

## 使用Windows架設機器人

### 1.安裝Python3.x

安裝時請確認安裝pip
設定環境變數

### 2.下載此儲存庫

### 3.初始設定

初始設定 可以直接修改 `token.json`
或是 使用 `python install.py`

### 4.執行

執行 Start.bat




