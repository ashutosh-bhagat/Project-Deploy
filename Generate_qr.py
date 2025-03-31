import qrcode
import streamlit as st
import pymongo
import base64
from io import BytesIO
import urllib.parse 

# Properly encode the password
password = urllib.parse.quote_plus("@Ashutosh7383")

# MongoDB Connection
try:
    client = pymongo.MongoClient(f"mongodb+srv://Ashutosh:{password}@cluster0.bdei33h.mongodb.net/?retryWrites=true&w=majority")
    db = client["qr_database"]
    collection = db["qr_codes"]
except pymongo.errors.ConfigurationError as e:
    st.error("MongoDB Connection Error. Please check your credentials and network settings.")
    st.stop()

def generate_qr(url, mainColor, BackColor):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=mainColor, back_color=BackColor) 
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()  

def save_mongo(name, url, qr_data):
    qr_base64 = base64.b64encode(qr_data).decode()  
    collection.insert_one({"name": name, "url": url, "qr_code": qr_base64})  

def get_image_download_link(img_data, filename="qr_code.png"):
    b64 = base64.b64encode(img_data).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">Download QR Code</a>'
    return href

st.title("Generate QR Code for Free")
name = st.text_input("Enter Your Name:")
url = st.text_input("Enter Your URL:")
mainColor = st.text_input("Enter Color of QR:")
BackColor = st.text_input("Enter Background Color of QR:")

if st.button("Generate QR Code"):
    if url:
        qr_image = generate_qr(url, mainColor, BackColor)  # Generate QR code
        save_mongo(name, url, qr_image)  # Save to MongoDB

        st.image(qr_image, caption="Generated QR Code", use_column_width=True)  # Display QR code
        st.markdown(get_image_download_link(qr_image), unsafe_allow_html=True)  # Download link
    else:
        st.warning("Please enter a valid URL")
