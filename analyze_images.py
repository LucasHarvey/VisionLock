# Import relevant libraries
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# Create an argument parser to parse the command line arguments
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--dataset", required=True)
argument_parser.add_argument("--encodings", required=True)
arguments = vars(argument_parser.parse_args())
# We will be using the hog detection method

# Use imutils to create a list of image paths
image_paths = list(paths.list_images(arguments["dataset"]))

# Create list to hold 128-d encodings
analyzed_encodings = []
# Create list to hold names of known people
names = []

# Loop over the image paths to create encodings 
for(index, imagePath) in enumerate(image_paths):
    # Print to the screen which image is being processed
    print("Processing image {}/{}".format(index+1, len(image_paths)))
    # Extract the name of the person from the folder name
    # The separator used by the OS in a file name can be retrieved using os.path.sep
    # Indexing by -2 allows to go back from the file name up to the folder with the person's name
    name = imagePath.split(os.path.sep)[-2]

    # Retrieve the image and convert it from BGR to RGB
    image = cv2.imread(imagePath)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create bounding boxes for the face(s) in the rgb_image using the face_recognition
    # library and the hog detection method
    boxes = face_recognition.face_locations(rgb_image, model="hog")

    # Once the boxes have been create, compute the 128-d encoding for the faces in the picture
    # Use the face_recognition library to create encodings for each facd by passing
    # in the image and the boxes surrounding the faces
    encodings = face_recognition.face_encodings(rgb_image, boxes)

    # Go through the encodings and add them to our lists
    for encoding in encodings:
        analyzed_encodings.append(encoding)
        names.append(name)

# Save the encodings to the pickle file
print("Saving encodings...")
data = {
    "encodings": analyzed_encodings,
     "names": names
     }
# Open the pickle file in write + binary mode
pickle_file = open(arguments["encodings"], "wb")
# Convert the object to binary format and write it to the file
pickle_file.write(pickle.dumps(data))
# Close the file
pickle_file.close()