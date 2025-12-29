import streamlit as st
import google.generativeai as genai
from PIL import Image

# تنظیمات کلید هوش مصنوعی
genai.configure(api_key="کلید_خود_را_اینجا_بگذارید")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("دستیار هوشمند کشاورز 🌿")
st.write("تصویر گیاه را آپلود کنید تا تحلیل کامل ارائه شود.")

# بخش آپلود عکس یا دوربین
img_file = st.camera_input("گرفتن عکس از گیاه") # یا st.file_uploader

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="تصویر ارسالی شما")
    
    if st.button("تحلیل و توصیه هوشمند"):
        with st.spinner('در حال آنالیز توسط هوش مصنوعی...'):
            # دستور به هوش مصنوعی
            prompt = "شما یک متخصص کشاورزی هستید. این تصویر را تحلیل کنید و در مورد: ۱. بیماری یا آفت ۲. نیاز آبی ۳. توصیه خاک‌ورزی و تغذیه، به زبان فارسی توضیح دهید."
            response = model.generate_content([prompt, img])
            st.success("نتیجه تحلیل:")
            st.write(response.text)
