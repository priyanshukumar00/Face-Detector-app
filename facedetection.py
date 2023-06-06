import cv2
import streamlit as st
import numpy as np
page_img_bg ="""<style>
[data-testid = "stAppViewContainer"]{{
    background-image: url("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwallpaperaccess.com%2Fdark-and-light&psig=AOvVaw1fZ4CZF0RIJ8FpisScRX9a&ust=1686163292285000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCKCG0_Klr_8CFQAAAAAdAAAAABAR");
    background-size: cover;
    opacity: 0.9;
    }}
[data-testid = "stSidebar"]{{
    background-color: #E3D3CE;
    opacity: 0.8;
    filter: blur(0.2px);
    }}

</style>
"""
st.markdown(page_img_bg, unsafe_allow_html = True)

def detect_faces(image):
    # Load the Haar cascade XML file for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return image

def main():
    st.header("Face Detection App 👨🏼‍💻")
    st.write("The Haar Cascade classifier is used in this face detection application. This method is employed to find and recognise human faces in the images. The Haar Cascade classifier is a machine learning-based approach that uses pre-trained features and a classification algorithm to detect faces. This application has several real-world applications including facial analysis, emotion identification, and facial recognition systems.")

    uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png', 'webp'])

    if uploaded_file is not None:
        # Read the uploaded image
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)

        # Perform face detection
        image_with_faces = detect_faces(image)

        # Display the processed images
        st.image(image_with_faces, channels="BGR", caption="Image with Detected Faces 👁️‍🗨️")

if __name__ == '__main__':
    main()
 
    
 
    
 
    
 
st.subheader('Hope You Liked it!')