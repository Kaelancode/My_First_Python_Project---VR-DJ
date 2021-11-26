import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
from time import sleep
import wikipedia
import pyjokes
import webbrowser
import PySimpleGUI as sg
from gtts import gTTS
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import wolframalpha
import duckduckgo
import urllib.request
from urllib.request import quote
from PIL import Image, ImageSequence
import vlc
import re
import os

language = 'en'

g = b'Mixing.gif'
ghi=b'Hello.gif'

vrdance = [g]
vrhello = [ghi]
vrpic = vrdance

# window interface
sg.theme('DarkRed') # add a touch of colors
#wolfram id
app_id= "************"
client = wolframalpha.Client(app_id)
#watson id
apikey = '***************************'
url = 'https://api.jp-tok.text-to-speech.watson.cloud.ibm.com/instances/******************'
authenticator = IAMAuthenticator(apikey)
service = TextToSpeechV1(authenticator=authenticator)
service.set_service_url(url)

# google voice
listener = sr.Recognizer()
#pyttx
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# list of vulgar words
Vulgarlist = ['fuck','fucker','dickhead','prick','bitch','pussy','dick','ass','asshole','shit']
#
Insultlist = ['stupid','dumb','ugly','moron','retard','slut','whore','idiot','pig']
Complimentlist = ['cute','pretty','smart','clever','beautiful','helpful','chio','great','sweet']
ClearSSlist = ['!','?',',',';','-','.']
Callist = ['+','-','*','/','=']

def checkVulgar(Vulgarlist,substring):
    return set(Vulgarlist).intersection(substring.split())
# Function to check for Insults
def checkInsult(Insultlist,substring):
    return set(Insultlist).intersection(substring.split())
# Function to check for Compliments
def checkCompliment(Complimentlist,substring):
    return set(Complimentlist).intersection(substring.split())


def checkClearSS(ClearSSlist,substring):
    substring.replace(ClearSSlist,'')
def CheckCal(Callist,substring):
    return set(Callist).intersection(list(substring))
def ddgsearch(searchtxt): # duckduckgo
    try:
        r = duckduckgo.query(searchtxt)
        #print(r.results[0].text)
        print(r.related[0].text)
        window['EmmaOUT'].update(r.related[0].text)
        window.refresh()
    except:
        sg.Popup("Cannot find results")
    window.Element('ListeningOut').update('')
    window.refresh()

#web search
def websearch(searchtxt):
    webbrowser.open('https://www.google.com/search?q='+searchtxt)
    window.Element('ListeningOut').update('')
    window.refresh()
# vid player
def playvid(songsearch):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + songsearch)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    print("https://www.youtube.com/watch?v=" + video_ids[0])
    play_url = "https://www.youtube.com/watch?v=" + video_ids[0]
    inst = vlc.Instance()
    list_player = inst.media_list_player_new()
    media_list = inst.media_list_new([])
    media_list.add_media(play_url)
    list_player.set_media_list(media_list)
    list_player.play()
    player = list_player.get_media_player()
    player.set_xwindow(window['-VID_OUT-'].Widget.winfo_id())
    window.refresh()

def talk(texttalk):
    #engine.say(text)
    #engine.runAndWait()
    window.Element('ListeningOut').update('')
    window.refresh()
    window['EmmaOUT'].update(texttalk)
    myobj = gTTS(text=texttalk ,lang='en', tld='co.za', slow=False)
    myobj.save("welcome.mp3")
    os.system("mpg321 welcome.mp3")

def watsontalk(texttalk):
    window.Element('ListeningOut').update('')
    window.refresh()
    window['EmmaOUT'].update(texttalk)
    with open(join(dirname(__file__), 'output2.mp3'),
          'wb') as audio_file:
        response = service.synthesize(
            texttalk, accept='audio/mp3',
            voice="en-GB_KateV3Voice").get_result()
        audio_file.write(response.content)

    os.system("mpg321 output2.mp3")

def take_command():
    #window['avatar'].update_animation_no_buffering(vrpic,  time_between_frames=200)
    try:
        with sr.Microphone() as source:
            command = ''
            window.Element('ListeningOut').update('Listening....')
            window.refresh()

            print('listening...')
            listener.adjust_for_ambient_noise(source, duration = 1)
            voice = listener.listen(source)
            command = listener.recognize_google(voice,language="zh-TW")
            command = command.lower()
            print(command)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except:
        pass
    return command

#SPEECH FUNCTION
def run_emmavoice():
    window['avatar'].update_animation_no_buffering(vrpic,  time_between_frames=200)
    commandtxt = take_command()
    window['-OUT-'].update(commandtxt)
    window.refresh()
    print(commandtxt)
    if 'play' in commandtxt:
        song = commandtxt.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'hey baby' in commandtxt:
        mytext = 'hi  , how are you?'
        talk(mytext)
    elif 'speak chinese' in commandtxt:
        mytext = '可以没问题'
        myobj = gTTS(text= mytext ,lang='zh-TW', slow=False)
        myobj.save("welcome.mp3")
        os.system("mpg321 welcome.mp3")
    elif '你好吗' in commandtxt:
        mytext = '我很好'
        myobj = gTTS(text= mytext ,lang='zh-TW', slow=False)
        myobj.save("welcome.mp3")
        os.system("mpg321 welcome.mp3")

    elif '我要听' in commandtxt or 'i want song' in commandtxt or 'i want some' in commandtxt:
        song = commandtxt.replace('i want song ', '')
        song = commandtxt.replace('我要听', '')
        songsearch = song.replace(' ', '+')
        songsearch = quote(songsearch)
        mytext = 'play for you 为你播放 ' + song
        myobj = gTTS(text= mytext ,lang='zh-TW', slow=False)
        myobj.save("welcome.mp3")
        os.system("mpg321 welcome.mp3")
        window['EmmaOUT'].update(mytext)
        window.refresh()
        playvid(songsearch)
    elif checkInsult(Insultlist,commandtxt) and 'you' in commandtxt:
        mytext = 'chee bye , asshole'
        talk(mytext)
    elif checkVulgar(Vulgarlist,commandtxt) and 'you' in commandtxt:
        mytext = "Langa Brains, go shove your head in the toilet bowl"
        talk(mytext)
    elif checkCompliment(Complimentlist,commandtxt) and 'you' in commandtxt:
        mytext = 'Thank you. My dear'
        talk(mytext)
    elif 'time' in commandtxt:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'date' in commandtxt:
        talk('sorry, I have a headache')
    elif 'are you single' in commandtxt:
        talk('I am in a relationship with wifi')
    elif 'joke' in commandtxt:
        #talk(pyjokes.get_joke())
        watsontalk(pyjokes.get_joke())
    elif 'private search' in commandtxt:
        search = commandtxt.replace('private search','')
        ddgsearch(search)
    elif 'go search for' in commandtxt:
        search = commandtxt.replace('go search for','')
        websearch(search)
    else:
        try:
            wolfram_res = client.query(commandtxt)
            wolfram = next(wolfram_res.results).text
            talk(wolfram + '.....So says wolfram')
        except:
            try:
                wiki = wikipedia.summary(commandtxt,sentences=1)
                talk(wiki + '.....From wiki')
            except:
                talk('Please repeat your question.')
# TEXT FUNCTION
def run_emmatext():
    checknum = sum(i.isdigit() for i in values['-IN-'])
    #[checkClearSS(ClearSSlist[i],values[0])for i in range(len(ClearSSlist))]
        # check for special characters
    for i in range(len(ClearSSlist)):
        values['-IN-'] = values['-IN-'].replace(ClearSSlist[i], '')

    if CheckCal(Callist,values['-IN-'])or checknum > 2:
        # more than 2 digits with operators go straight for wolfram results
        try:
            wolfram_res = client.query(values['-IN-'])
            wolfram = next(wolfram_res.results).text
            talk(wolfram)
        except:
            sg.PopupNonBlocking("Do not Understand")

    elif checkVulgar(Vulgarlist,values['-IN-'].lower()) and 'you' in values['-IN-'].lower().split():
        mytext = "Langa Brains, go shove your head in the toilet bowl"
        #talk(mytext)
        watsontalk(mytext)
    elif checkCompliment(Complimentlist,values['-IN-'].lower()) and 'you' in values['-IN-'].lower().split():
        mytext = 'Thank you. My dear'
        talk(mytext)
    elif checkInsult(Insultlist,values['-IN-'].lower()) and 'you' in values['-IN-'].lower():
        mytext = 'chee bye , asshole'
        talk(mytext)
    elif ('what' in values['-IN-'].lower() or 'now' in values['-IN-'].lower()) and 'time' in values['-IN-'].lower():
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'date' in values['-IN-'].lower():
        talk('sorry, I have a headache')
    elif 'are you single' in values['-IN-'].lower():
        talk('I am in a relationship with wifi')
    elif 'joke' in values['-IN-'].lower():
        talk(pyjokes.get_joke())
    elif 'play' in values['-IN-'].lower():
        song = values['-IN-'].lower().replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    else:
        try:
            wiki = wikipedia.summary(values['-IN-'],sentences=1)
            talk(wiki + '.....Wiki says so')

        except :
            try:
                wolfram_res = client.query(values['-IN-'])
                wolfram = next(wolfram_res.results).text
                talk(wolfram, '.....Wolfram say so lor')

            except:
                sg.Popup("Do not Understand")

#[sg.Image(key ='image'),
#LAYOUT OF THE GUI
frame_EmmaOUT = [sg.MLine(size = (63,4),text_color = 'LIGHTBLUE',background_color= '#41136D',key = 'EmmaOUT')]
column_to_be_centered = [ [sg.Image(vrpic,background_color = 'purple', k = 'avatar',metadata =0 )]]
column_for_Controls =[  [sg.Text('Whats on your mind?'),sg.Input(key='-IN-')],
                        [sg.Button('Text DJ',bind_return_key = True),sg.Button('Cancel')],
                        [sg.Frame(layout= [  [sg.Button('Speak',bind_return_key = True),sg.Button('Cancel'),sg.Text(size = (15,1),text_color= 'LIGHTGRAY', key = 'ListeningOut')],
                                            [sg.Text('You said:'), sg.Text(size=(55,1),text_color= 'LIGHTGRAY', relief=sg.RELIEF_RIDGE, key = '-OUT-')] ] , title='Voice:')],
                        [sg.Frame(layout=[frame_EmmaOUT,], title='DJ Says')]
                        ]

def btn(name):  # a PySimpleGUI "User Defined Element" (see docs)
    return sg.Button(name, size=(6, 1), pad=(1, 1))
# ALL the stuff inside the window
layout = [  [sg.Text('HELLO YAKUN',justification='center',size=(70,1))],
            #[sg.Image(key ='image'),sg.Image(vrmaid2)],
            [sg.Image('',size=(700, 397), key='-VID_OUT-')],
            [sg.Column(column_to_be_centered, vertical_alignment='center', justification='center',  k='-C-'),sg.Column(column_for_Controls,vertical_alignment='center', justification='center')],

            #[sg.Text('You said:'), sg.Text(size=(55,1),text_color= 'LIGHTGRAY', relief=sg.RELIEF_RIDGE, key = '-OUT-')],
            #[sg.Text(size = (100,1),text_color = 'LIGHTBLUE',background_color= 'ORANGE' ,key = 'EmmaOUT')],


            #[sg.Image('',size=(500, 283), key='-VID_OUT-')],
            #[btn('previous'), btn('play'), btn('next'), btn('pause'), btn('stop')]
            ]
            #[sg.Button('Speak',bind_return_key = True),sg.Button('Cancel')]]

# Create the Window
#  layout,element_justification = 'c' ,centers the whole window
window = sg.Window('Virtual DJ', layout, element_justification='center',resizable=True)
while True:
    event, values = window.Read(timeout = 200)
    window['avatar'].update_animation(vrpic,  time_between_frames=200)
    if event in (None, 'Cancel'):
        break
    if event == 'Speak':
        run_emmavoice()
    elif event == 'Text DJ':
        run_emmatext()
    #values['-IN-'] = get_text()
    #window['-OUT-'].update(commandtxt)
window.Close()
exit()
