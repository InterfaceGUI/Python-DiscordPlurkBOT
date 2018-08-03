import atexit

try:
	from plurk_oauth import PlurkAPI
except ImportError:
	import pip
	pip.main(['install','plurk-oauth'])
	from plurk_oauth import PlurkAPI
	
try:
	from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
	import pip
	pip.main(['install','apscheduler'])	
	from apscheduler.schedulers.asyncio import AsyncIOScheduler
	
try:	
	import discord
except ImportError:
	import pip
	pip.main(['install','discord.py'])	
	import discord
	
from discord.ext import commands
from discord.ext.commands import Bot
try:
	import base36
except ImportError:
	import pip
	pip.main(['install','base36'])	
	import base36
	
import urllib.request as urllib2
import sys
import json
from datetime import datetime
import datetime
from html.parser import HTMLParser

with open('token.json' , 'r') as reader:
    Tjs = json.loads(reader.read())

TOKEN = Tjs['Discord']['Token']
ChannelID = Tjs['Discord']['ChannelID']
plurk = PlurkAPI(Tjs['Plurk']['APP_KEY'], Tjs['Plurk']['APP_SECRET'])
plurk.authorize(Tjs['Plurk']['ACCEESS_TOKEN'], Tjs['Plurk']['ACCESS_TOKEN_SECRET'])

Client = discord.Client()
bot = commands.Bot(command_prefix = Tjs['Discord']['Prefix'])

def GetPlurkss():
   
   return plurk.callAPI('/APP/Timeline/getPlurks',options={'limit':'1','minimal_data':'false','minimal_user':'false'})

def GetFollowing():
    return plurk.callAPI('/APP/FriendsFans/getFollowingByOffset',options={'offset':'0','limit':'1000','minimal_data':'true'})

def UserSearch(U):
    return plurk.callAPI('/APP/UserSearch/search',options={'query':U ,'offset':'0','type':'general'})

def setFollowing(i ,s):
    
    id  = str(i)
    id.strip()
    return plurk.callAPI('/APP/FriendsFans/setFollowing',options={'user_id':id,'follow':s})
    
def GetUserIURL(i):
    id  = str(i)
    id.strip()
    return plurk.callAPI('/APP/Profile/getPublicProfile',options={'user_id':id,'include_plurks':'false'})

def UserIURL(i):
    GP = json.dumps(GetUserIURL(i))
    UGP = json.loads(GP)
    return UGP['user_info']['avatar_big']

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False
 
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
     
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
bot.remove_command("help")
class GetPlurks:
    global PlurkQualifier
    global PlurkUserID
    global PlurkDisplay_Name
    global PlurkUserURL
    global PlurkContent
    global PlurkContent_raw 
    global PlurkURL 
    PlurkQualifier = ''
    PlurkUserID = ''
    PlurkDisplay_Name = ''
    PlurkUserURL = ''
    PlurkContent = ''
    PlurkContent_raw = ''
    PlurkURL =''
    PlurkImg =  None
    PlurkVideo = None
       
    
def GetP():
    try:
        global JSUGP
        global JSGP
        global JSGPL
        JSUGP =  json.dumps(GetPlurkss())
        JSGP = json.loads(JSUGP)
        JSGPL = list(JSGP['plurk_users'].keys())
        GetPlurks.PlurkQualifier = JSGP['plurks'][0]['qualifier']
        Plurkuserids = str(JSGP['plurks'][0]['owner_id']) 
        GetPlurks.PlurkUserID = JSGP['plurk_users'][Plurkuserids]['id']
        GetPlurks.PlurkDisplay_Name = JSGP['plurk_users'][Plurkuserids]['display_name']
        GetPlurks.PlurkUserURL = 'https://www.plurk.com/' +  JSGP['plurk_users'][Plurkuserids]['nick_name']
        GetPlurks.PlurkContent = JSGP['plurks'][0]['content']
        GetPlurks.PlurkContent_raw = JSGP['plurks'][0]['content_raw']
        GetPlurks.PlurkURL = 'https://www.plurk.com/p/' + base36.dumps(JSGP['plurks'][0]['plurk_id'])   
    except Exception as ex:
        print(ex)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('StartGetPlurk')
    scheduler.start()
    muser = await bot.get_user_info('226226332944564224')

@bot.command(pass_context=True)
async def getFollowing(ctx):
    muser = await bot.get_user_info(ctx.message.author.id)
    JFD = json.dumps(GetFollowing())
    JF = json.loads(JFD)
    n = 0
    Display = ' :scroll: :regional_indicator_p: :regional_indicator_l: :regional_indicator_u: :regional_indicator_r: :regional_indicator_k: 關注名單列表'
    for user in JF:
        n +=1
        UserDN = user['display_name']
        UserUrl = '    <https://www.plurk.com/' +user['nick_name'] + '>'
        Display += '\n' + ' :arrow_forward: **' + UserDN + '**' +'\n' + '    ' + UserUrl
        if n == 5 :
            n = 0
            await bot.send_message(muser,Display)
            Display=' '
    await bot.delete_message(ctx.message)
    await bot.send_message(muser,Display)
    await bot.send_message(muser,'共 ' + str(len(JF)) + '個用戶')

@bot.command(pass_context=True)
async def ping(ctx):
    print('用戶指令輸入:', ctx.message.content)
    await bot.say(":ping_pong: Ping!!")
    
@bot.command(pass_context=True)
async def uf(ctx):
    print('用戶指令輸入:', ctx.message.content)
    msg = ctx.message.content.replace(Tjs['Discord']['Prefix'] + 'uf ','')
    
    U = msg
    U.strip()
    U = U.replace('https://www.plurk.com/','')
    
    GP = json.dumps(UserSearch(U))
    UGP = json.loads(GP)
    await bot.say("搜尋用戶:"+ U)
    await bot.say("成功找到 : "+ UGP['users'][0]['display_name'])
    GGP = json.dumps(setFollowing(UGP['users'][0]['id'],'false'))
    UUGP = json.loads(GGP)
    try:
        UUGP['success_text']
        await bot.say("操作成功")
    except Exception:
        await bot.say(UUGP['error_text'])
        sys.exc_clear()

@bot.command(pass_context=True)
async def help(ctx):
    print('用戶指令輸入:', ctx.message.content)
    embed = discord.Embed(title= 'Bot Commands' , description = 'Bot Prefix = `' + Tjs['Discord']['Prefix'] + '`' ,color= 0xff5129 ,timestamp = datetime.datetime.utcnow())
    embed.set_footer(text = "BOT made by Interface_GUI",icon_url = "https://images-ext-2.discordapp.net/external/kRxpbJlpZCf9FMw11DTnL5HPzkDmozsZ3zeymhcsgFk/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/226226332944564224/fa78ba0af70c004291e2f5d87672263c.jpg")
    embed.add_field(name='`help`',value='Like this',inline=True)
    embed.add_field(name='`f UserUrl`',value='Follow the user from (Userurl)',inline=False)
    embed.add_field(name='`uf UserUrl`',value='Unfollow the user from (Userurl)',inline=True)
    embed.add_field(name='example',value='if you want to follow `https://www.plurk.com/Interfac_GUI`' + '\n' + 'You neet to type ' + '[`' + Tjs['Discord']['Prefix'] + 'f https://www.plurk.com/Interfac_GUI`]' ,inline=False)
    await bot.send_message(ctx.message.channel,embed=embed)

@bot.command(pass_context=True)
async def f(ctx):
    print('用戶指令輸入:', ctx.message.content)
    msg = ctx.message.content.replace(Tjs['Discord']['Prefix']+ 'f ' ,'') 
    
    U = msg
    U.strip()
    U = U.replace('https://www.plurk.com/','')
    
    GP = json.dumps(UserSearch(U))
    UGP = json.loads(GP)
    await bot.say("搜尋用戶:"+ U)
    await bot.say("成功找到 : "+ UGP['users'][0]['display_name'])
    



    GGP = json.dumps(setFollowing(UGP['users'][0]['id'],'true'))
    UUGP = json.loads(GGP)
    try:
        UUGP['success_text']
        await bot.say("操作成功")
    except Exception:
        await bot.say(UUGP['error_text'])
        sys.exc_clear()

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            a=0
    def handle_starttag(self, tag, attrs):
        if tag == 'img' :
            for attr in attrs:
                if attr[0] == 'alt':
                    GetPlurks.PlurkImg =  attr[1]
    def handle_endtag(self, tag):
        a=0

    def handle_data(self, data):
        a=0

    def handle_comment(self, data):
        a=0

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))


    def handle_decl(self, data):
        a=0

    tag = None
    attrs = None
    attr = None


tOPlurkURL =''
def image(co):
   try:
        
        temp = co[co.index('img src="'):co.index('" height=')]
        parser = MyHTMLParser()
        parser.feed(co)
        
        
   except Exception:
       return
       sys.exc_clear()

#手動指令檢查刪噗 預設 是檢查200則噗文
DisableRemovePlurk = True #調為True禁用指令檢查，調為False啟用
@bot.command(pass_context=True)
async def RemovePlurk(ctx):
    if DisableRemovePlurk :
        return
    print('用戶指令輸入:', ctx.message.content)
    print('警告用戶使用RemovePlurk，可能會造成同步上的LAG')
    await bot.send_message(bot.get_channel(ChannelID),'RemovePlurking...')
    async for message in bot.logs_from(bot.get_channel(ChannelID), limit=200): 
        try:
            OldPlurkUrl = message.embeds[0]['author']['url']
            req = urllib2.Request(OldPlurkUrl)
            response = urllib2.urlopen(req)

            html = str(response.read())
            temp = html[html.index('title'):html.index('/title')]
            
        except Exception as e:
            if not (str(e) == 'list index out of range'):
                if (str(e)) == 'HTTP Error 404: NOT FOUND':
                    await bot.delete_message(message)
    await bot.send_message(bot.get_channel(ChannelID),'Done!')

#刪噗檢查
async def RemovePlurk():
    async for message in bot.logs_from(bot.get_channel(ChannelID), limit=30): #limit=30  是30則訊息 請勿過大 
        try:
            OldPlurkUrl = message.embeds[0]['author']['url']
            req = urllib2.Request(OldPlurkUrl)
            response = urllib2.urlopen(req)
            html = str(response.read())
            temp = html[html.index('title'):html.index('/title')]
            
        except Exception as e:
            if not (str(e) == 'list index out of range'):
                if (str(e) == 'HTTP Error 404: NOT FOUND'):
                    await bot.delete_message(message)       



async def start():
        global OldPlurk
        global tOPlurkURL
        global Color 
        Color = 0
        GetP()
        for case in switch(GetPlurks.PlurkQualifier):
            if case(':'):
                Color = 0
                break
            if case('plays'):
                Color = 0xfd7387
                break
            if case('buys'):
                Color = 0xff9481
                break
            if case('sells'):
                Color = 0xff5129
                break
            if case('loves'):
                Color = 0xe30000
                break
            if case('likes'):
                Color = 0xff373d
                break
            if case('shares'):
                Color = 0xc65454
                break
            if case('hates'):
                Color = 0x111
                break
            if case('wants'):
                Color = 0x84964d
                break
            if case('wishes'):
                Color = 0x5cb27a
                break
            if case('needs'):
                Color = 0x3aa46e
                break
            if case('has'):
                Color = 0x468281
                break
            if case('will'):
                Color = 0xae60b1
                break
            if case('hopes'):
                Color = 0xe28ee1
                break
            if case('asks'):
                Color = 0x7c58a4
                break
            if case('wonders'):
                Color = 0x4c6391
                break
            if case('feels'):
                Color = 0x4d99cd
                break
            if case('thinks'):
                Color = 0x6ca5ce
                break
            if case('draws'):
                Color = 0x47b2b1
                break
            if case('is'):
                Color = 0xff7932
                break
            if case('says'):
                Color = 0xe88d43
                break
            if case('eats'):
                Color = 0xff8d06
                break
            if case('writes'):
                Color = 0xefab07
                break

        if not tOPlurkURL == GetPlurks.PlurkURL:
            if not Tjs['BlockedWord'][0] == 'null':
                for x in Tjs['BlockedWord']:
                    try:
                        if GetPlurks.PlurkContent.index(x):
                            print('偵測到特定字詞 不同步')
                            return
                    except ValueError as e:
                        pass

            print('NewPlurk!:', GetPlurks.PlurkURL)
            print('-------------------------------------------')
            Uri = UserIURL(GetPlurks.PlurkUserID)
            embed = discord.Embed(title= GetPlurks.PlurkQualifier ,description = GetPlurks.PlurkContent_raw,color=Color,timestamp = datetime.datetime.utcnow())
            img = image(GetPlurks.PlurkContent)
            image(img)
            if not GetPlurks.PlurkImg == None:
                embed.set_image(url=GetPlurks.PlurkImg)
                GetPlurks.PlurkImg =  None
            embed.set_author(icon_url = Uri ,name=GetPlurks.PlurkDisplay_Name ,url=GetPlurks.PlurkURL)
            embed.set_footer(text = "BOT made by 科技狼(Tech wolf)",icon_url = "https://images-ext-2.discordapp.net/external/kRxpbJlpZCf9FMw11DTnL5HPzkDmozsZ3zeymhcsgFk/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/226226332944564224/fa78ba0af70c004291e2f5d87672263c.jpg")
            try:
                await bot.send_message(bot.get_channel(ChannelID),embed=embed)
            except expression as identifier:
                pass
            tOPlurkURL = GetPlurks.PlurkURL
            image(GetPlurks.PlurkContent)
            GetPlurks.PlurkImg =  None
            GetPlurks.PlurkVideo = None
            
@bot.command(pass_context=True)
async def test(ctx):
        start()

async def ErrorA(e):
    await bot.send_message(bot.get_channel(ChannelID),'```'+ '\n' + str(e) + '\n' + '```')


@atexit.register
def cleanup_function():
    print(sys._getframe().f_code.co_name)
    bot.close()
    Client.close()


try:    
    try:
        scheduler = AsyncIOScheduler()
        #偵測計時器部分 請勿調整過快 過快會對plurk伺服器造成負擔
        scheduler.add_job(start, 'interval' , seconds=10)
        #定時檢查噗文是否被刪除 請勿過快 過快會對plurk伺服器造成更重的負擔
        #預設 每30分鐘檢查30則噗文是否被刪除 
        scheduler.add_job(RemovePlurk,'interval' , seconds=1800)
    except Exception as e:
        print('Error:',str(e))
        
        await bot.send_message(muser,'scheduler 部分錯誤 \n ``` \n' + str(e) + '\n ```'   
    try:
        bot.run(TOKEN)
    except Exception as e:
        bot.close()
        Client.close()
        print('Error:',str(e))
    
except Exception as e:
    ErrorA(e)
    bot.close()
    Client.close()
    print('Error:',str(e))



