import pickle
import cv2
from skimage import feature
import numpy as np
import os

# Function to extract HOG features
def quantify_image(image):
    features = feature.hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(2, 2), 
                           transform_sqrt=True, block_norm="L1")
    return features

# Load images and make predictions
def predict(spiralpath, wavepath):
    paths = [spiralpath, wavepath]
    images = []
    results = []

    for path in paths:
        if "spiral" in path:
            model = pickle.load(open("model/spiral_model.pkl", 'rb'))
            le_classes = np.load("model/spiral.npy")
        else:
            model = pickle.load(open("model/wave_model.pkl", 'rb'))
            le_classes = np.load("model/wave.npy")

        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200))
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        features = quantify_image(image)
        pred = model.predict([features])[0]
        label = le_classes[pred]
        
        output_img = cv2.putText(image, label, (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 6)
        results.append((path, label))
        cv2.imwrite(os.path.join(os.path.dirname(path), "pred_" + os.path.basename(path)), output_img)

    return results
