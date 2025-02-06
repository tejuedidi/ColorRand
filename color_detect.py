import cv2
import json
import time
import os
from colorthief import ColorThief

# fn to get the color palette of an image
def getColors(img):
    cv2.imwrite('img.jpg', img)  # saves an image to a specified file
    # this continously updates the images and writes every second
    colorthief = ColorThief('img.jpg')
    # extracts 7 colors from the image
    return colorthief.get_palette(color_count=7)

def bitSeq(dom_colors):
    combinedByte = str()

    for i in dom_colors:
        for j in i:
            combinedByte += str(j) + " "

    return combinedByte.strip()  # remove trailin space

# creating a video capture object
webcam = cv2.VideoCapture(0)  # initializing default webcam

if not webcam.isOpened():
    print("--Cannot open camera.--")
    exit()

# list of strings to continuining append to
color_data = list()  # list for byte data
file_content = []
file_exists = os.path.exists("color_data.json") 
start_time = time.time()  # to record before the start of the loop

while (True):
    # returns a boolean if frame read currectly then try
    success, frame = webcam.read()  # captures frame from webcam

    if not success:  # if frame not successfully captured then break
        print("--Frame reading error, try again.--")
        break

    # extract dominant colors from the current frame
    dom_colors = getColors(frame)

    box_height = 30  # height of each color box
    box_width = 30  # width of each color box
    margin = 10  # space between each color box

    for i, color in enumerate(dom_colors):
        # position the bounding box and add text
        top_left = (margin, margin + i * (box_height + margin))
        bottom_right = (top_left[0] + box_width, top_left[1] + box_height)

        text = f'RGB: {color}'
        text1 = 'press q to quit'
        text_position = (bottom_right[0] + margin,
                         top_left[1] + box_height // 2)
        text_position1 = (480, 450)

        cv2.rectangle(frame, top_left, bottom_right, color[::-1], -1)
        cv2.putText(frame, text, text_position,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (color), 1)
        cv2.putText(frame, text1, text_position1,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Real-Time Color Detector!', frame)

    # writing color data to json file
    current_time = time.time()
    if (current_time - start_time >= 15):
        color_data.append(bitSeq(dom_colors))

        if file_exists:
            # read the content of the file and load file_content with its contents
            with open("color_data.json", "r+") as outfile:
                read_contents = outfile.read()
                file_content = json.loads(read_contents)
                print(file_content)

        with open("color_data.json", "w+") as outfile:
            file_content.append(bitSeq(dom_colors))
            print(file_content)
            json.dump(file_content, outfile, indent=4)

        # Reset the timer
        start_time = current_time
        color_data.clear()

    # waits 1 millisecond to break the loop when q key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()  # release the webcam and close all windows
cv2.destroyAllWindows()
