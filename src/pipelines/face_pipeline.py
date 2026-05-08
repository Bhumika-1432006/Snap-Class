

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students # getting all the students identity data 



@st.cache_resource  # writing this my below model will lad only once (huge fiels)
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() # detcts how many faces are there and thier coordinates 



    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location() # rtis gives th landmass locaton we are specifically using this model pose_predictor_model_location() 

    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1) # we are saying it to just scan once -> or else it takes a lot o cpu memeory space 


    encodings= [] # wee collect all the encodings in this 


    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) # 128 embedding

        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():  # this will make an svc model 
    X = []
    y = []


    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) ==0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced') # no matter how may photo u put the model will take only 1 so that model doesnt get overtrained 


    try: # training our classifier 
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X':X, "y":y}


def train_classifier():
    st.cache_resource.clear()  # to clear all cahed data to not show previous data for new users 

    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {} # all students found in the image


    model_data = get_trained_model() # coordinates trained 


    if not model_data:
        return detected_student, [], len(encodings)
    
    clf = model_data['clf'] # predictions 
    X_train = model_data['X'] # all embeddings
    y_train = model_data['y'] # all labels 

    all_students = sorted(list(set(y_train))) #no repeattios

    for encoding in encodings: # removing all the embedings 
        if len(all_students)>= 2: # if more than 2 people in the photo we have to fib=nd them then list 

            predicted_id= int(clf.predict([encoding])[0]) # max person in images 
        else:
            predicted_id = int(all_students[0]) # atleast one student (one img)

        student_embedding = X_train[y_train.index(predicted_id)]

        best_match_score = np.linalg.norm(student_embedding - encoding) # checking the predicted results with mathematical alinear algebra 


        resemblance_threshold = 0.6 # here we are comparing the image(actual coordinats ) and the predicted persn through model of that person 
        # if the difference in each coordinates is > 0.6  then say no its not that person 


        if best_match_score <= resemblance_threshold: # found the perfect match 
        
            detected_student[predicted_id] = True
    return detected_student, all_students, len(encodings)
