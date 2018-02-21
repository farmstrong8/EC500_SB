import timeit
from Program.main import get_tweets, get_images, rename_files, add_text_to_image, convert_images
import os

def main(screen_name, path):
    state = get_tweets(screen_name) #get the timeline
    outputf = get_images(state, path) #get output folder
    rename_files(outputf) #rename the images
    #convert_images(outputf) #convert the images to a video
    add_text_to_image(outputf)
    convert_images(outputf)


print("Execution time: ", str(timeit.repeat('main("BowenIslandSong", "temp")', "from __main__ import main", number=1)))
