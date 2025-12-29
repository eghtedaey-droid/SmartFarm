import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io

# تنظیمات صفحه
st.set_page_config(page_title="دستیار هوشمند کشاورز", layout="centered")

#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(OpenAI API Key)
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

st.title("🌿 دستیار کشاورز (قدرت گرفته از Copilot/GPT)")
st.write("تصویر گیاه را آپلود کنید تا تحلیل دقیق دریافت کنید.")

img_file = st.camera_input("گرفتن عکس")
uploaded_file = st.file_uploader("انتخاب عکس", type=['jpg', 'png', 'jpeg'])

source = img_file if img_file else uploaded_file

if source:
    st.image(source, caption="تصویر در حال پردازش...", use_container_width=True)
    
    if st.button("شروع آنالیز هوشمند"):
        with st.spinner('در حال ارتباط با هوش مصنوعی...'):
            base64_image = encode_image(source)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o", # یا gpt-4-vision-preview
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "شما یک متخصص گیاه‌پزشکی هستید. این تصویر را تحلیل کنید و نام بیماری، دلیل و راه درمان (آبیاری، کود، سم) را به فارسی بگویید."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ],
                        }
                    ],
                    max_tokens=500,
                )
                st.success("نتیجه تحلیل:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"خطا در سیستم: {e}")
