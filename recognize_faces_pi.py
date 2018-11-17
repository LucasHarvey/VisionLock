from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import motor
import pyttsx3

# Create an argument parser to parse the command line arguments
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--cascade", required=True)
argument_parser.add_argument("--encodings", required=True)
arguments = vars(argument_parser.parse_args())
# We will be using the hog detection method

print("loading encodings...")
# Retrieve the names and encodings from the pickle file by opening it in read+binary
data = pickle.loads(open(arguments["encodings"], "rb").read(), encoding='latin1')
#Create a detector using Haar cascades
detector = cv2.CascadeClassifier(arguments["cascade"])

# Start the video stream
print("Starting video...")
video_stream = VideoStream(usePiCamera=True).start()

# Sleep the program for 2 seconds while the camera starts
time.sleep(2.0)

# Start counting frames per second
fps = FPS().start()

# Loop through video_stream frames
while True:
    # Retrieve the current frame
    frame = video_stream.read()
    
    # Resize the frame to make processing faster
    frame = imutils.resize(frame, width=500)

    # Convert the frame to grayscale for face detection using Haar cascades
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert the frame to RBG for face recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the grayscale image
    rectangles = detector.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

    # Change order of bounding box coordinates from x,y,w,h to top, right, bottom, left
    boxes = [(y, x+w, y+h, x) for (x,y,w,h) in rectangles]

    # Encode the detected faces
    encodings = face_recognition.face_encodings(rgb_frame, boxes)

    # Initialize an array containing the names of the people in the frame
    recognized_names = []

    # Loop through the encodings found in the frame
    for encoding in encodings:
        # Try to match the encoding to the encodings from the pickle file
        matches_found = face_recognition.compare_faces(data["encodings"], encoding)
        # Set the current name to Unknown before we determine if the face is recognized
        name = "Unknown"

        # Determine if at least one match was found
        if True in matches_found:
            # Go through the list of matches and store the indexes in a new list
            matches_found_indexes = [i for(i, b) in enumerate(matches_found) if b]
            # Initialize a dictionary that will contain the names and votes for each
            votes = {}

            # Loop through the indexes, get the name and increment the vote count
            for index in matches_found_indexes:
                name = data["names"][index]
                votes[name] = votes.get(name, 0) + 1

            # Determine which person got the most upvotes and ensure that it has atleast 3 votes
            name = max(votes, key=votes.get)
            if(votes[name] < 6):
                name = "Unknown"
            
            engine = pyttsx3.init()
            
            if(name == "Unknown")
                engine.say("ACCESS DENIED!")
                engine.runAndWait()
            else:
                engine.say("Welcome home " + name)
                engine.runAndWait()
                motor.unlock()
                sleep(15)
                motor.lock()
            # Add the name to the list of names to add to the frame
            recognized_names.append(name)

    # Loop through the faces in the frame, which will be associated with the correct name
    for ((top, right, bottom, left), name) in zip(boxes, recognized_names):
       # Draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),(255, 0, 0), 2)
        if(top - 15 < 15):
            y = top - 15
        else:
            y = top + 15
        
        cv2.putText(frame, name, (left, top-15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

    # Determine if the user wants to show the video
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    
    # Update the FPS counter
    fps.update()

fps.stop()
cv2.destroyAllWindows()
# Stop the video stream
video_stream.stop()


