import json
import sys, os, subprocess, re
IS_WINDOWS = os.name == "nt"
REQS_TXT = "requirements.txt"
intro = ("=====================================\n"
         "Python-PlurkDiscordsyncBOT - Launcher\n"
         "=====================================\n")

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

def install_reqs():
  interpreter = sys.executable
  if interpreter is None:

      print("Python interpreter not found.")
      return
  args = [
      interpreter, "-m",
      "pip", "install",
      "--upgrade",
      #"--target", REQS_DIR,  #This has been causing problems for some users. Although I don't know what exactly is wrong with it.
      "-r", REQS_TXT
  ]
  code = subprocess.call(args)

  if code == 0:
      print("\nRequirements setup completed.")
  else:
      print("\nAn error occurred and the requirements setup might "
            "not be completed. Consult the docs.\n")

def user_choice():
    return input("> ").lower().replace(' ', '')

def wait():
    input("按下 Enter 繼續")

def RunBOT(autorestart=False):
  interpreter = sys.executable
  if interpreter is None:  # This should never happen
      raise RuntimeError("Couldn't find Python's interpreter")
  cmd = (interpreter, "PythonPlurkDiscordSyncBOT.py")
  while True:
    try:
      clear_screen()
      code = subprocess.call(cmd)
    except KeyboardInterrupt:
      code = 0
      break
    else:
      if autorestart:
        print('未知崩潰. 10分鐘後重啟.')
        time.sleep(600)
      else:
        break


def clear_screen():
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

modtb = ( "===============================================\n"
         "Python-PlurkDiscordsyncBOT - Modify-BlockedWord\n"
         "===============================================\n")
def ModifysettinBlockedWord(data):
  while True:
    clear_screen()
    x=0
    for i in data['BlockedWord']:
      x+=1
      print(str(x) + '.' + i )
    print(modtb)
    print('1. 增加字詞')
    print('2. 移除字詞')
    print("3. 整串修改")
    print('\n0. 離開')
    choice = user_choice()
    if choice == "1":
      lists =  input('請輸入封鎖字詞\n>')
      if not lists == '':
        data['BlockedWord'].append(lists)
    elif choice == "2":
      print('您想移除第幾個?\n')
      print('\n0. 離開')
      choice = user_choice()
      if not choice == '0':
        data['BlockedWord'].pop(int(choice)-1)
    elif choice == "3":
      data['BlockedWord'] = list(map(str, input('請輸入封鎖字詞(輸入null 表示不封鎖)' + '\n' + '(輸入格式為 123,456,789,abc   或者是 null ):').split(',')) )
    elif choice == "0":
      break
  return data

modt = ( "===================================\n"
         "Python-PlurkDiscordsyncBOT - Modify\n"
         "===================================\n")

def Modifysetting():
  clear_screen()
  with open("token.json", "r") as re:
        data = json.loads(re.read())
        re.close()
  print('APP_KEY :',data['Plurk']['APP_KEY'])
  print('APP_SECRET :',data['Plurk']['APP_SECRET'])
  print('ACCEESS_TOKEN :', data['Plurk']['ACCEESS_TOKEN'])
  print('ACCESS_TOKEN_SECRET :',data['Plurk']['ACCESS_TOKEN_SECRET'])
  print('Token :',data['Discord']['Token'])
  print('ServerID :',data['Discord']['ServerID'])
  print('ChannelID :',data['Discord']['ChannelID'])
  print('Prefix :',data['Discord']['Prefix'])
  print('BlockedWord :',data['BlockedWord'])
  print(modt)
  print("------Plurk------")
  print("1. 修改 App_Key")
  print("2. 修改 APP_SECRET")
  print("3. 修改 ACCEESS_TOKEN")
  print("4. 修改 ACCESS_TOKEN_SECRET")
  print("------Discord------")
  print("5. 修改 Token")
  print("6. 修改 ServerID")
  print("7. 修改 ChannelID")
  print("8. 修改 Prefix")
  print("-----封鎖字詞-----")
  print("9. 修改 封鎖字詞")
  print("\n0. 離開")
  choice = user_choice()
  if choice == "1":
    data['Plurk']['APP_KEY'] = input('請輸入Plurk APP_KEY: ')
  elif choice == "2":
    data['Plurk']['APP_SECRET'] = input('請輸入Plurk APP_SECRET: ')
  elif choice == "3":
    data['Plurk']['ACCEESS_TOKEN'] = input('請輸入Plurk ACCEESS_TOKEN: ')
  elif choice == "4":
    data['Plurk']['ACCESS_TOKEN_SECRET'] = input('請輸入Plurk ACCESS_TOKEN_SECRET: ')
  elif choice == "5":
    data['Discord']['Token'] = input('請輸入Discord Token: ')
  elif choice == "6":
    data['Discord']['ServerID'] = input('請輸入Discord ServerID: ')
  elif choice == "7":
    data['Discord']['ChannelID'] = input('請輸入Discord ChannelID: ')
  elif choice == "8":
    data['Discord']['Prefix'] = input('請輸入Discord Prefix: ')
  elif choice == "9":
    data = ModifysettinBlockedWord(data)
  elif choice == "0":
    with open("token.json", "w") as write_file:
        json.dump(data, write_file)
        write_file.close
    return True
  with open("token.json", "w") as write_file:
        json.dump(data, write_file)
        write_file.close
while True:
  print(intro)
  print("1. 安裝 requirements")
  print("2. 初始設定")
  print("3. 修改設定")
  print('4. 運行BOT')
  print('5. 運行BOT(自動重啟)')
  print("\n0. 離開")

  choice = user_choice()

  if choice == "1":
    install_reqs()
  elif choice == "2":
    install()
    wait()
  elif choice == "3":
    while not Modifysetting():
      pass
    wait()
  elif choice == "4":
    RunBOT(autorestart=False)
    wait()
  elif choice == "5":
    RunBOT(autorestart=True)
    wait()
  elif choice == "0":
    break
  clear_screen()