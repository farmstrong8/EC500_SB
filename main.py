from __future__ import print_function
import tweepy
import json
import os
import io
import wget
from google.cloud import vision
from google.cloud.vision import types
from google.auth import app_engine
import urllib2
import subprocess
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

CONSUMER_KEY = 'XXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXX'
ACCESS_TOKEN = 'XXXXXXXX'
ACCESS_TOKEN_SECRET = 'XXXXXXX'
diction = {}

#========================= INTRODUCTION MESSAGE ===============================#
def welcome_menu():
    print("Hello, and welcome to my EC500 Project")
    return


#========================= USER TWITTER API INFO ==============================#
def get_API_info():
    CONSUMER_KEY = raw_input("What is your twitter api consumer key?")
    CONSUMER_SECRET = raw_input("What is your twitter api consumer secret?")
    ACCESS_TOKEN = raw_input("What is your twitter api access token?")
    ACCESS_TOKEN_SECRET = raw_input("What is your twitter api access token secret?")
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
    except tweepy.TweepError:
        print("Keys are wrong")


    return CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


#============================ GET THE TWEETS ==================================#
def get_tweets():
    SCREEN_NAME = raw_input("What twitter handle do you want to search?\n")
    #get the user that you want the statuses of
    try:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            statuses = api.user_timeline(screen_name=SCREEN_NAME,count=200, include_rts=True, exclude_replies=True)

    except tweepy.TweepError:
        print("Sorry, either the account you entered is private or does not exist, please try another name")
        statuses = 0
        return statuses


    return statuses


#============================ DOWNLOAD IMGS ==================================#
def get_images(statuses):
    i = 0
    path = raw_input("Where do you want to store the pictures?\n")
    if not os.path.exists(path): #if there is no directory
        print("Creating path....")
        os.makedirs(path)

    for status in statuses:
        media = status.entities.get('media', [])
        if(len(media) > 0 and media[0]['media_url'].endswith('g')):
            wget.download(media[0]['media_url'], out=path)
            get_picture_labels(media[0]['media_url'],"image"+str(i))
            i += 1
    return path


def convert_images(path):
    frames_per_second = 1
    os.chdir(path)
    #subprocess.call(["cd", "THERE"])
    subprocess.call(["ffmpeg.exe","-y","-r",str(frames_per_second),"-i", "%01d.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(frames_per_second), "video.avi"])
    return


def rename_files(directory):
    i=0
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            os.rename(directory + "/" + filename, directory + "/" + str(i) + ".jpg")
            i+=1
    return

def get_picture_labels(uri,key):
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    #print('Labels:')
    myList = []
    for label in labels:
        myList.append(label.description)
    diction[key] = myList
        #print(label.description)

    return


def add_text_to_image(directory):
    i = 0
    os.chdir(directory)
    for filename in os.listdir(directory):
        ypos= 0
        if filename.endswith(".jpg"):
            img = Image.open(filename)
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            font = ImageFont.truetype("sans-serif.ttf", 16)
            # draw.text((x, y),"Sample Text",(r,g,b))
            newList = diction['image' + str(i)]
            for item in newList:
                print(item)
                draw.text((0, ypos),item,(255,255,255),font=font)
                ypos += 15
            img.save(filename)
            i+=1
    return

def main():

    while(True):
        option = raw_input("\n What do you want to do? Press 0 to exit \n")
        if(option == "0"):
            return
        else:
            state = get_tweets() #get the timeline
            outputf = get_images(state) #get output folder
            #add_text_to_image(outputf)
            print(diction)
            rename_files(outputf) #rename the images
            #convert_images(outputf) #convert the images to a video
            #add_text_to_image(outputf)

    return

#run main
if __name__=='__main__':
    main()
