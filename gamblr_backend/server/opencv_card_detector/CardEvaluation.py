# Import necessary packages
import cv2
import numpy as np
import time
import os
import Cards
import imutils
import VideoStream


image_path = 'E:\Playing Card Detection\playing-cards-master\playing-cards-master\img'

### ---- INITIALIZATION ---- ###
# Define constants and initialize variables

# Adaptive threshold levels
BKG_THRESH = 90
#BKG_THRESH = 50
#CARD_THRESH = 10

## Camera settings
IM_WIDTH = 1280
IM_HEIGHT = 720 
FRAME_RATE = 10

## Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
frame_rate_calc = 1
freq = cv2.getTickFrequency()

## Define font to use
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera object and video feed from the camera. The video stream is set up
# as a seperate thread that constantly grabs frames from the camera feed. 
# See VideoStream.py for VideoStream class definition
## IF USING USB CAMERA INSTEAD OF PICAMERA,
## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
videostream = VideoStream.VideoStream((IM_WIDTH,IM_HEIGHT),FRAME_RATE,2,0).start()
time.sleep(1) # Give the camera time to warm up

# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks( path + '/Card_Imgs/')
train_suits = Cards.load_suits( path + '/Card_Imgs/')

"""
# Set up webcam
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False"""

### ---- MAIN LOOP ---- ###
# The main loop repeatedly grabs frames from the video stream
# and processes them to find and identify playing cards.

cam_quit = 0 # Loop control variable

# Begin capturing frames
# while cam_quit == 0:

char_to_rank = {
    '0': 'Ten',
    'A': 'Ace',
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
    'J': 'Jack',
    'Q': 'Queen',
    'K': 'King'
}

char_to_suit = {
    'S': 'Spades',
    'C': 'Clubs',
    'D': 'Diamonds',
    'H': 'Hearts'
}

seg_counted = 0
rank_match = 0
suit_match = 0
total = 0

for filename in os.listdir(image_path):
    if filename.endswith(".jpg") and "003" not in filename and "004" not in filename and "001" not in filename: 
        if cam_quit != 0:
            break
    
        if True:
            # Grab frame from video stream
            #image = videostream.read()

            image = cv2.imread(os.path.join(image_path, filename), 1)
            symbol = (filename.split("[")[-1]).split("]")[0]
            if 'W' in symbol:
                continue
            rank = char_to_rank[symbol[1]]
            suit = char_to_suit[symbol[0]]


            #cv2.imshow("preview", frame)
            
            """rval, frame = vc.read()
            image = frame"""
            
            height, width, channels = image.shape
            if height/IM_HEIGHT > width/IM_WIDTH:
                image = imutils.resize(image, height=IM_HEIGHT)
            else:
                image = imutils.resize(image, width=IM_WIDTH)

            # Start timer (for calculating frame rate)
            t1 = cv2.getTickCount()

            best_cnts_sort = []
            most_cards = 0
            best_cnt_is_card = []
            best_pre_proc = None

            total += 1

            # number of tries to detect cards
            for tries in range(9):

                # Pre-process camera image (gray, blur, and threshold it)
                pre_proc = Cards.preprocess_image(image, BKG_THRESH=BKG_THRESH - 10*tries)
                #cv2.imwrite("output\\" + filename + "-" + str(tries) + '.jpg', pre_proc)
                
                # Find and sort the contours of all cards in the image (query cards)
                cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)
                cur_cards = sum(cnt_is_card)
                if cur_cards > most_cards:
                    seg_counted += 1
                    best_cnts_sort = cnts_sort
                    most_cards = cur_cards
                    best_cnt_is_card = cnt_is_card
                    best_pre_proc = pre_proc

            cnts_sort = best_cnts_sort
            cnt_is_card = best_cnt_is_card
            if best_pre_proc is not None:
                pre_proc = best_pre_proc

            #cv2.imwrite("output\\" + filename, pre_proc)

            # If there are no contours, do nothing
            if len(cnts_sort) != 0:

                # Initialize a new "cards" list to assign the card objects.
                # k indexes the newly made array of cards.
                cards = []
                k = 0

                # For each contour detected:
                for i in range(len(cnts_sort)):
                    if (cnt_is_card[i] == 1):

                        # Create a card object from the contour and append it to the list of cards.
                        # preprocess_card function takes the card contour and contour and
                        # determines the cards properties (corner points, etc). It generates a
                        # flattened 200x300 image of the card, and isolates the card's
                        # suit and rank from the image.
                        cards.append(Cards.preprocess_card(cnts_sort[i],image))

                        # Find the best rank and suit match for the card.
                        cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = Cards.match_card(cards[k],train_ranks,train_suits)

                        if cards[k].best_rank_match == rank:
                            rank_match += 1

                        if cards[k].best_suit_match == suit:
                            suit_match += 1

                        # Draw center point and match result on the image.
                        image = Cards.draw_results(image, cards[k])
                        k = k + 1
                
                # Draw card contours on image (have to do contours all at once or
                # they do not show up properly for some reason)
                if (len(cards) != 0):
                    temp_cnts = []
                    for i in range(len(cards)):
                        temp_cnts.append(cards[i].contour)
                    cv2.drawContours(image,temp_cnts, -1, (255,0,0), 2)
                
                
            # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
            # so the first time this runs, framerate will be shown as 0.
            cv2.putText(image,"FPS: "+str(int(frame_rate_calc)),(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)

            # Finally, display the image with the identified cards!
            cv2.imshow("Card Detector",image)

            # Calculate framerate
            t2 = cv2.getTickCount()
            time1 = (t2-t1)/freq
            frame_rate_calc = 1/time1
            
            # Poll the keyboard. If 'q' is pressed, exit the main loop.
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cam_quit = 1
            
            #time.sleep(1)
            

    # Close all windows and close the PiCamera video stream.
    cv2.destroyAllWindows()
    videostream.stop()

print("Segmentation accuracy:")
print(seg_counted / total)
print("Rank classification accuracy:")
print(rank_match / seg_counted)
print("Suit classification accuracy:")
print(suit_match / seg_counted)
