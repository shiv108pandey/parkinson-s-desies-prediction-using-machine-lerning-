import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from project_orm import UserInput, Prediction
from predict_parkinsons import predict
import os
from PIL import Image

def db():
    engine = create_engine('sqlite:///project_db.sqlite3')
    Session = sessionmaker(bind=engine)
    return Session()

st.sidebar.header("Parkinson Disease Prediction")
menu = ["Add patients", "Prediction", "About project", "Instructions"]
choice = st.sidebar.radio("Project Menu", menu)

if choice == "Add patients":
    st.title("Data of Patients")
    
    patient_id = st.number_input("Enter ID of patient", max_value=10000, min_value=1)
    patient_name = st.text_input("Enter name of patient", max_chars=500)
    age = st.number_input("Age of patient", max_value=100, min_value=1)
    location = st.text_area("Enter address")
    
    submit = st.button("Save")
    
    if submit:
        entry = UserInput(patient_id=patient_id, patient_name=patient_name, age=age, location=location)
        sess = db()
        sess.add(entry)
        sess.commit()
        st.success("Patient data saved successfully!")
        sess.close()

elif choice == "Prediction":
    sess = db()
    results = sess.query(UserInput).all()
    sess.close()

    if results:
        patients = [obj for obj in results]
        pt = st.sidebar.selectbox("Select a patient to test", patients)
        
        BASE_DIR = os.path.join("uploads", str(pt.patient_id))
        if not os.path.exists(BASE_DIR):
            os.makedirs(os.path.join(BASE_DIR, "spiral"))
            os.makedirs(os.path.join(BASE_DIR, "wave"))

        st.title("Patient Parkinson Test")
        st.markdown(f"<table><tr><th colspan='2'>Patient details</th></tr>"
                    f"<tr><td>ID</td><td>{pt.patient_id}</td></tr>"
                    f"<tr><td>Name</td><td>{pt.patient_name}</td></tr>"
                    f"<tr><td>Age</td><td>{pt.age}</td></tr>"
                    f"<tr><td>Location</td><td>{pt.location}</td></tr>"
                    "</table>", unsafe_allow_html=True)

        spiral_img = st.file_uploader("Upload Spiral Test image", type=["png"])
        wave_img = st.file_uploader("Upload Wave Test image", type=["png"])
        
        if spiral_img:
            spiral_path = os.path.join(BASE_DIR, "spiral", "spiral.png")
            Image.open(spiral_img).save(spiral_path)
        
        if wave_img:
            wave_path = os.path.join(BASE_DIR, "wave", "wave.png")
            Image.open(wave_img).save(wave_path)
        
        if st.button("Predict"):
            if spiral_img and wave_img:
                results = predict(spiral_path, wave_path)
                st.success("Prediction Completed!")
                for res in results:
                    st.image(res[0], caption=f"Prediction: {res[1]}")
