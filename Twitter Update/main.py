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
import time
#libraries needed to draw text on the images
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFile
#MongoDB Implementation
from pymongo import MongoClient
import json
ImageFile.LOAD_TRUNCATED_IMAGES = True

temp_dict = {}
CONSUMER_KEY = 'XXXXXX'
CONSUMER_SECRET = 'XXXXXX'
ACCESS_TOKEN = 'XXXXXX'
ACCESS_TOKEN_SECRET = 'XXXXXX'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="JSON PATH"

client = MongoClient('localhost', 27017)
SCREEN_NAME = " "

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
            #dict['screen_name'] = SCREEN_NAME


    except tweepy.TweepError:
        print("Sorry, either the account you entered is private or does not exist, please try another name")
        statuses = 0
        return statuses


    return statuses, SCREEN_NAME


#============================ DOWNLOAD IMGS ==================================#
def get_images(statuses):
    i = 0
    path = raw_input("Where do you want to store the pictures?\n")
    if not os.path.exists(path): #if there is no directory
        print("Creating path....")
        os.makedirs(path)

    for status in statuses:
        media = status.entities.get('media', [])
        #data_items.insert(media) #insert the status into the database
        if(len(media) > 0 and media[0]['media_url'].endswith('g')):
            wget.download(media[0]['media_url'], out=path)
            get_picture_labels(media[0]['media_url'],"image"+str(i))
            i += 1
    return path

#============================= GET VIDEO ======================================#
#using ffmpeg api, convert the images in the directory to a video
def convert_images(path):
    frames_per_second = 1
    os.chdir(path)
    os.system('ffmpeg -framerate 1 -start_number 100 -i "%3d.jpg" -vf "crop=((in_w/2)*2):((in_h/2)*2)" -c:v libx264 -pix_fmt yuv420p out.mp4')
    return



#=============================== RENAME =======================================#
#rename files 0 - number of images
def rename_files(directory):
    i=100
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            os.rename(directory + "/" + filename, directory + "/" + str(i) + ".jpg")
            i+=1
    return


#=========================== GET GCV LABELS ===================================#
#Get image labels using google cloud api and store them in the dictionary
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
    temp_dict[key] = myList
        #print(label.description)

    return



#======================= ADD TEXT TO IMAGE BASED ON LABEL =====================#
#Given a directory, add text to an image based on the labels in the dictionary
def add_text_to_image(directory):
    os.chdir(directory) #point to the directory
    for filename in os.listdir(directory): #for each file in the directory
        ypos= 0 #ypos to change where the text is placed
        if filename.endswith(".jpg"):
            img = Image.open(filename)
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            font = ImageFont.truetype("arial.ttf", 16) #get the font
            # draw.text((x, y),"Sample Text",(r,g,b))
            name = filename[:-4] #remove the .jpg from the filename
            newList = diction['image' + name] #get the items assocaied with the current file
            for item in newList: #for each item in the list draw it on the image
                print(item)
                draw.text((0, ypos),item,(255,69,0),font=font)
                ypos += 15 #increment ypos to make space for more labels if necessary
            img.save(filename+'.jpg') #save the file
    return

def main():
    while(True):
        option = raw_input("\nPress any key to continue, Press 0 to exit \n")
        if(option == "0"):
            return
        else:
            state, user = get_tweets() #get the timeline
            if(state == 0):
                return
            else:
                outputf = get_images(state) #get output folder
                rename_files(outputf) #rename the images
                #convert_images(outputf) #convert the images to a video
                #add_text_to_image(outputf)
                #print(user)
                db = client[user] #create a new database with the users username if it is valid
                label_items = db.Labels #insert the labels in the database
                #print(temp_dict)
                label_items.insert(temp_dict)
                #convert_images(outputf)

    return

#run main
if __name__=='__main__':
    main()
