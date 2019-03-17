import pyperclip
import keyboard
import pyautogui
import re
import json
import requests

weapon_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=weapon').text
armor_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=armour').text
accessories_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=accessory').text
flask_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=flask').text
jewel_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=jewel').text
map_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=map').text
prophecy_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=prophecy').text
card_json_raw = requests.get('https://api.poe.watch/get?league=Synthesis&category=card').text

weapon_json_parsed = json.loads(weapon_json_raw)
armor_json_parsed = json.loads(armor_json_raw)
accessories_json_parsed = json.loads(accessories_json_raw)
flask_json_parsed = json.loads(flask_json_raw)
jewel_json_parsed = json.loads(jewel_json_raw)
map_json_parsed = json.loads(map_json_raw)
prophecy_json_parsed = json.loads(prophecy_json_raw)
card_json_parsed = json.loads(card_json_raw)

acc = ['Ring', 'Amulet', 'Belt', 'Talisman']
previous_item = 0

print("loaded!")
while True:
    keyboard.wait('ctrl')
    old = pyperclip.paste()
    pyautogui.press('c')
    rawitem = pyperclip.paste()
    price = 0.0
    if re.search(r'\r\n',rawitem):
        splititem = rawitem.split('\r\n')
        item_type = splititem[2]

        itemrarity = splititem[0].split(':')[1][1:]

        if itemrarity == 'Divination Card':
            itemname = splititem[1]

            if itemname == previous_item:
                continue
            
            previous_item = itemname

            namefilter = [s for s in card_json_parsed if itemname in s['name']]
            price = namefilter[0]['mean']

        if 'Right-click to add this prophecy' in splititem[-2]: #lol
            itemname = splititem[1]
            if itemname == previous_item:
                continue
            
            previous_item = itemname

            namefilter = [s for s in prophecy_json_parsed if itemname in s['name']]
            price = namefilter[0]['mean']

        if itemrarity == 'Unique':
            itemname = splititem[1]
            
            if re.match("<<", itemname): #wtf is this
                itemname = itemname.split(">>")[3]

            if itemname == previous_item:
                continue

            previous_item = itemname
            socketraw = [s for s in splititem if "Sockets" in s]
            if socketraw:
                socketcount = len(re.findall('-', socketraw[0]))+1
                if socketcount < 5:
                    socketcount = None
            else:
                socketcount = None

            if [k for k in acc if k in item_type]:
                namefilter = [s for s in accessories_json_parsed if itemname in s['name']]
            elif 'Jewel' in item_type:
                namefilter = [s for s in jewel_json_parsed if itemname in s['name']]
            elif 'Flask' in item_type:
                namefilter = [s for s in flask_json_parsed if itemname in s['name']]
            elif 'Map' in item_type:
                namefilter = [s for s in map_json_parsed if itemname in s['name']]
            else:
                namefilter = [s for s in weapon_json_parsed if itemname in s['name']]
                if len(namefilter) == 0:
                    namefilter = [s for s in armor_json_parsed if itemname in s['name']]

            sockfilter = [k for k in namefilter if socketcount == k['links']]
            if len(sockfilter) == 0:
                price = "Not enough data for 6 link of this item available."
            else:
                price = namefilter[0]['mean']                       

                
    if price != 0.0:
        prettyprice = str(price)
        print(f'{itemname}: {prettyprice[0:4]}c')
    pyperclip.copy(old)
