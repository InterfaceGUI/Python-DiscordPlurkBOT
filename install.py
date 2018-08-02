import json

data = {
  "Plurk": {
    "APP_KEY": "",
    "APP_SECRET": "",
    "ACCEESS_TOKEN": "",
    "ACCESS_TOKEN_SECRET": ""
  },
  "Discord": {
    "Token": "",
    "ServerID": "",
    "ChannelID": "",
    "Prefix": "p!"
  },
  "BlockedWord":[
    "null"
  ]
}

def install():
    data['Plurk']['APP_KEY'] = input('請輸入Plurk APP_KEY: ')
    data['Plurk']['APP_SECRET'] = input('請輸入Plurk APP_SECRET: ')
    data['Plurk']['ACCEESS_TOKEN'] = input('請輸入Plurk ACCEESS_TOKEN: ')
    data['Plurk']['ACCESS_TOKEN_SECRET'] = input('請輸入Plurk ACCESS_TOKEN_SECRET: ')
    data['Discord']['Token'] = input('請輸入Discord Token: ')
    data['Discord']['ServerID'] = input('請輸入Discord ServerID: ')
    data['Discord']['ChannelID'] = input('請輸入Discord ChannelID: ')
    data['Discord']['Prefix'] = input('請輸入Discord Prefix: ')
    data['BlockedWord'] = list(map(str, input('請輸入封鎖字詞(輸入null 表示不封鎖)' + '\n' + '(輸入格式為 123,456,789   或者是 null ):').split(',')) )
    with open("token.json", "w") as write_file:
        json.dump(data, write_file)
        write_file.close

while True:
    res = input('進行初始化設定?[y/n]: ')
    if res == 'y':
        install()
        break
    if res == 'n':
        break

