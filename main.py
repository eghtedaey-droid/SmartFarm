import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# ۱. تنظیمات ظاهر برنامه
st.set_page_config(page_title="دستیار هوشمند کشاورز", page_icon="🌿")

# ۲. اتصال به هوش مصنوعی Groq (جایگزین جمینای)
# کلیدی که از سایت console.groq.com گرفتید را اینجا بگذارید
GROQ_API_KEY = "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" 
client = Groq(api_key=GROQ_API_KEY)

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

st.title("دستیار هوشمند کشاورز 🌿")
st.write("تصویر گیاه را آپلود کنید تا تحلیل کامل ارائه شود.")

# ۳. بخش دوربین
img_file = st.camera_input("گرفتن عکس از گیاه")

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="تصویر ارسالی شما")
    
    if st.button("تحلیل و توصیه هوشمند"):
        with st.spinner('در حال آنالیز توسط هوش مصنوعی (بدون تحریم)...'):
            try:
                # تبدیل عکس به فرمت قابل فهم برای Groq
                base64_image = encode_image(img_file)
                
                # فراخوانی مدل تصویری قدرتمند Llama 3.2
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "شما یک متخصص کشاورزی هستید. این تصویر را تحلیل کنید و در مورد: ۱. بیماری یا آفت ۲. نیاز آبی ۳. توصیه خاک‌ورزی و تغذیه، به زبان فارسی توضیح دهید."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }
                    ],
                )
                
                st.success("نتیجه تحلیل:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"خطا در سیستم: {e}")
