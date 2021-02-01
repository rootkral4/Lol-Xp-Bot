import pyautogui
import time
import threading
import os
import subprocess
import atexit
import random
import keyboard
from python_imagesearch.imagesearch import imagesearch
from ahk import AHK

ahk = AHK(executable_path="ahk/AutoHotkeyU64.exe")

pyautogui.FAILSAFE = False

#images

oynabuton      = "images/oynabuton.png"
kabuletbuton   = "images/kabuletbuton.png"
lanebutons     = "images/lanebutons.png"
champsearchbox = "images/champsearchbox.png"
veigarpicture  = "images/veigarpic.png"
hazirbuton     = "images/hazirbuton.png"
profilebuton   = "images/profilebuton.png"
levelup        = "images/levelup.png"



def searchgame():
    pos = imagesearch(oynabuton)
    if pos[0] != -1:
        pyautogui.click(pos[0] + 45, pos[1] + 5)
        time.sleep(2)
        pyautogui.click(pos[0] + 100, pos[1] + 70)
        time.sleep(2)
        pyautogui.click(pos[0] + 500, pos[1] + 655)
        time.sleep(4)
        pyautogui.click(pos[0] + 500, pos[1] + 655)
        print("Searching for match ...")
        acceptgame()
    else:
        print("Please go back to home page and try again")

def acceptgame():
    while True:
        pos = imagesearch(kabuletbuton)
        if pos[0] != -1:
            print("Match Found")
            pyautogui.click(pos[0] + 45, pos[1] + 5)
            print("Match Accepted")
            break

def championselectioncheck():
    pos = imagesearch(lanebutons)
    if pos[0] != -1:
        return True
    else:
        return False

def gamestartedcheck():
    win = ahk.find_window(title=b'League of Legends (TM) Client')
    if win != None:
        return True
    else:
        return False

def acceptuntilfound():
    while True:
        time.sleep(11)
        inchampselect = championselectioncheck()
        if inchampselect == False:
            acceptgame()
        if inchampselect == True:
            break

def selectchamp():
    pos = imagesearch(champsearchbox)
    pyautogui.click(pos[0] + 45, pos[1] + 5)
    pyautogui.write("sylas")
    time.sleep(1)
    pos2 = imagesearch(veigarpicture)
    ahk.click(pos2[0] + 2, pos2[1] + 2)
    print("Champion Selected")
    pos3 = imagesearch(hazirbuton)
    time.sleep(1)
    pyautogui.click(pos3[0], pos3[1])

def checkforgamebreak():
    while True:
        pos = imagesearch(profilebuton)
        if pos[0] != -1:
            print("Match Dodged")
            print("Waiting ...")
            acceptuntilfound()
            selectchamp()
        ingamecheck = gamestartedcheck()
        if ingamecheck == True: 
            break

def f2down():
    ahk.key_down("f2")

def f2up():
    ahk.key_up("f2")

atexit.register(f2up)

def lvlup(skill):
    if skill == "q":
        ahk.click(772, 881)
    elif skill == "w":
        ahk.click(842, 883)
    elif skill == "e":
        ahk.click(888, 883)
    elif skill == "r":
        ahk.click(949, 886)

def attack():
    skilllist = ["q", "w", "e"]
    pos = ahk.pixel_search(0xc4451f,variation=5)
    if pos != None:
        ahk.mouse_move(pos[0], pos[1])
        ahk.key_press(random.choice(skilllist))
        print("Skill Used")

global killthreads
killthreads = False

def killthread():
    global killthreads
    killthreads = True

def checkforlevelup():
    global killthreads
    while True:
        if killthreads == True:
            break
        pos = imagesearch(levelup, precision=100)
        if pos != -1:
            ahk.click(pos[0] + 5, pos[1] + 5)
            ahk.click(pos[0] + 5, pos[1] + 5)
            print("Level Up")
        time.sleep(20)

def randomspell():
    spelllist = ["d", "f"]
    global killthreads
    while True:
        if killthreads == True:
            break
        time.sleep(160)
        ahk.key_press(random.choice(spelllist))
        print("Spell Used")

def autoward():
    global killthreads
    while True:
        if killthreads == True:
            break
        time.sleep(60)
        ahk.key_press("4")
        print("Ward Placed")

def checkforendgame():
    global killthreads
    while True:
        if killthreads == True:
            break
        win = ahk.find_window(title=b'League of Legends (TM) Client')
        if win == None:
            print("Match Ended")
            killthread()
            print("Threads Killed")
            f2up()
            print("F2 Up")
            os.system("TASKKILL /F /IM LeagueClient.exe")
            print("Restarting")
            time.sleep(20)
            subprocess.Popen("\"C:\Riot Games\Riot Client\RiotClientServices.exe\" --launch-product=league_of_legends --launch-patchline=live")
            time.sleep(20)
            print("LOL started")
            start()

def startthreads():
    threading.Thread(target=checkforlevelup).start()
    threading.Thread(target=checkforendgame).start()
    threading.Thread(target=autoward).start()
    threading.Thread(target=randomspell).start()

def start():
    win = ahk.find_window(title=b'League of Legends')
    win.activate()
    searchgame()
    acceptuntilfound()
    selectchamp()
    checkforgamebreak()
    while True:
        pos = imagesearch(levelup)
        if pos != -1:
            time.sleep(30)
            playgame()
            break

def playgame():
    global killthreads
    killthreads = False
    time.sleep(2)
    win = ahk.find_window(title=b'League of Legends (TM) Client')
    if win == None:
        print("---------------------------------------> LOL isn't running <-------------------------------")
    else:
        win.activate()
        time.sleep(1)
        lvlup("q")
        ahk.key_press("p")
        ahk.click(479, 274)
        ahk.send_input("yuzuk")
        ahk.right_click(360, 377)
        time.sleep(0.5)
        ahk.key_press("Esc")
        startthreads()
        while True:
            if killthreads == True:
                break
            f2down()
            ahk.right_click(953, 552)
            time.sleep(1)
            attack()

atexit.register(killthread)
while True:
    opts = """
    Options :
    StartBotting : search and play
    Start : im in game start playing
    """
    print(opts)
    choice = input("->")
    if choice == "StartBotting":
        start()
        break
    elif choice == "Start":
        playgame()
        break
    else:
        print("No such option")