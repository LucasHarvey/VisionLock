from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

# Create an argument parser to parse the command line arguments
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--encodings", required=True)
argument_parser.add_argument("--output", type=str)
argument_parser.add_argument("--display", type=int, default=1)
arguments = vars(argument_parser.parse_args())
# We will be using the hog detection method

print("loading encodings...")
# Retrieve the names and encodings from the pickle file by opening it in read+binary
data = pickle.loads(open(arguments["encodings"], "rb").read())

# Start the video stream
print("Starting video...")
# src=0 uses the device's default camera
video_stream = VideoStream(src=0).start()
# Sleep the program for 2 seconds while the camera starts
time.sleep(2.0)

# Loop through video_stream frames
while True:
    # Retrieve the current frame
    frame = video_stream.read()

    # Convert the frame from BGR to RBG
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Resize the frame
    rgb_frame = imutils.resize(frame, width=750)
    # Get the ratio of the frame and the shrinken rgb_frame 
    ratio = frame.shape[1] / float(rgb_frame.shape[1])

    # Detect faces using bounding boxes
    boxes = face_recognition.face_locations(rgb_frame, model="hog")
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

            # Add the name to the list of names to add to the frame
            recognized_names.append(name)

    # Loop through the faces in the frame, which will be associated with the correct name
    for ((top, right, bottom, left), name) in zip(boxes, recognized_names):
        # rescale the face coordinates
        top = int(top * ratio)
        right = int(right * ratio)
        bottom = int(bottom * ratio)
        left = int(left * ratio)

        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),(255, 0, 0), 2)
        if(top - 15 < 15):
            y = top - 15
        else:
            y = top + 15
        
        cv2.putText(frame, name, (left, top-15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

    # Determine if the user wants to show the video
    if arguments["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

cv2.destroyAllWindows()
# Stop the video stream
video_stream.stop()


