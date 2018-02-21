import os
from Program.main import get_tweets, get_images, rename_files, add_text_to_image, convert_images

def main(screen_name, path):
    state = get_tweets(screen_name) #get the timeline
    outputf = get_images(state, path) #get output folder
    rename_files(outputf) #rename the images
    #convert_images(outputf) #convert the images to a video
    add_text_to_image(outputf)
    convert_images(outputf)

main("BowenIslandSong", "temp")
fileName = "video.avi"

webpage = open("demo.html", "w")

content = """
<html>
<body>

<video width="320" height="240" controls>
  <source src="%s" type="video/mp4">
  Your browser does not support HTML5.
</video>

</body>
</html>""" % fileName

webpage.write(content)
webpage.close()

os.system("open demo.html")