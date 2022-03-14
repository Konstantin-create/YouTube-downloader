# https://www.youtube.com/watch?v=12rcdJKSGFc

# Imports
import os
import telebot
from pytube import YouTube

# Variables
downloader = False
token = "1680815154:AAFE-Xm4eXPtN2ygnTQv9PuAK2iKLYCEmLc"
bot = telebot.TeleBot(token)

item1Text = "/download_video"
item2Text = "/support_author"
item3Text = "/help_ussers"

markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
itembtn1 = telebot.types.KeyboardButton("Download video")
itembtn2 = telebot.types.KeyboardButton("/Make_a_donation")
itembtn3 = telebot.types.KeyboardButton("/Help_users")
markup.add(itembtn1, itembtn2, itembtn3)


# Functions
@bot.message_handler(commands=['start'])
def start_command(message):
    msg = bot.reply_to(message, 'Welcome to QuickYouTubeVideoDownloaderBot. Select menu item:', reply_markup=markup)
    bot.register_next_step_handler(msg, download_video_command)


def download_video_command(message):
    global downloader
    downloader = True
    bot.send_message(message.chat.id, "Enter link:", reply_markup=None)


def help_users_command(message):
    bot.send_message(message.chat.id, "How to download video:\n"
                     "  1) If you want to download video, press 'Download video' button.\n"
                     "  2) Insert a link next step.\n"
                     "  3) The next step, select the video quality button.\n"
                     "  4) Wait a few minutes to download video.")
    start_command()


@bot.message_handler(content_types=['text'])
def select_quality(message):
    global downloader, yt, videos
    qualityList = []
    if downloader:
        try:
            global yt, videos, link
            link = message.text
            yt = YouTube(link)
            videos = yt.streams.filter(mime_type="video/mp4")
            count = 1
            for v in videos:
                qualityList.append(
                    (str(count) + ". " + str(v)[str(v).find("res="):str(v).find("fps=")] + '"\n\n').replace('"',
                                                                                                            '').strip())
                count += 1
            a = ""
            for i in range(len(qualityList)):
                qualityList[i] = qualityList[i][qualityList[i].find(" "):].lstrip()

            for i in range(len(qualityList)):
                if a.find(qualityList[i]) != -1:
                    pass
                else:
                    a += str("{}. {}".format(i + 1, qualityList[i]) + "\n")
            markup2 = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
            a = a.split("\n")
            for i in range(len(a) - 4):
                markup2.add(a[i])
            msg = bot.reply_to(message, 'Select quality:', reply_markup=markup2)
            bot.register_next_step_handler(msg, save_video_command)
            downloader = False
        except:
            bot.send_message(message.chat.id, "Please fill correct link")
            downloader = False
            start_command(message)


def save_video_command(message):
    video = yt.streams.filter(progressive=True, file_extension='mp4',
                              resolution=message.text[message.text.find("=") + 1:])
    path = "{}\\{}\\".format(os.getcwd(), str(message.from_user.id))
    video = video[-1]
    video.download(path, filename=str(message.from_user.id))
    bot.send_message(message.chat.id, "Start sending video.")
    bot.send_video(message.chat.id, open(path + str(message.from_user.id) + ".mp4", 'rb'))
    os.remove(os.path.abspath(path + str(message.from_user.id) + ".mp4"))
    bot.send_message(message.chat.id, "Bot finished sending video.")
    start_command()

# Mainloop
try:
    bot.polling()
except:
    pass
