import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from googletrans import Translator
import io

st.set_page_config(
    page_title="Exstreamly Cool App",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("ColorAlchemy")

on = st.toggle("ENG|TR")

information = """
ColorAlchemy is a powerful yet intuitive image compression tool that lets
you transform your images into stunning works of digital art. With
ColorAlchemy, you can adjust the number of colors in your images to create
captivating visual effects. Whether you're a photographer, designer, or 
simply love playing with colors, ColorAlchemy offers an easy-to-use interface
for creating compressed images with just the right amount of vibrancy and 
detail. Upload your images, choose the desired number of colors, and let 
ColorAlchemy work its magic to produce beautifully compressed images ready
for sharing or printing.
"""
def translate(text, src_lang='en', dest_lang='tr'):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated_text.text
if on:
    information = translate(information)
else:
    information = information

def stream_data():
    for word in information.split(" "):
        yield word + " "
        time.sleep(0.03)
if st.button("Learn More", type="secondary"):
    st.write_stream(stream_data())
    st.snow()

with st.form("Add image", clear_on_submit=True):
    number = st.select_slider("**Indicate the desired color variation for the new image:**", options=range(2, 17))
    picture = st.file_uploader("**Upload an image (JPEG or PNG only):camera:**", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    run = st.form_submit_button("ColorWizard", type="primary")

if run:
    if picture is not None:
        try:
            def k_means(data, K, max_iters=10, convergence_tol=1e-4):
                centroids = data[np.random.choice(len(data), K, replace=False)]
                for _ in range(max_iters):
                    distances = np.linalg.norm(data[:, None] - centroids, axis=2)
                    idx = np.argmin(distances, axis=1)
                    new_centroids = np.array([data[idx == k].mean(axis=0) if np.any(idx == k) else np.zeros(data.shape[1]) for k in range(K)])
                    if np.linalg.norm(new_centroids - centroids) < convergence_tol:
                        break
                    centroids = new_centroids
                return centroids, idx
            
            def compress_image(img, color=8):
                reshaped_img = img.reshape(-1, img.shape[-1])
                centroids, idx = k_means(reshaped_img, color)
                compressed_img = centroids[idx].reshape(img.shape)
                return compressed_img

            with st.spinner("Colorizing..."):
                img_array = plt.imread(picture) / 255 if picture.name.lower().endswith(('.jpeg', '.jpg')) else plt.imread(picture)
                compressed_image = compress_image(img_array, color=number)
                col1, col2 = st.columns(2, gap="small")
                with col1:
                    st.image([compressed_image], caption=f"ColorCrafted Image ({number} colors)")
                with col2:
                    st.image(img_array, caption="Original Image")
                
                # Save compressed image to a bytes buffer
                compressed_image_buffer = io.BytesIO()
                plt.imsave(compressed_image_buffer, compressed_image, format='png')
                compressed_image_bytes = compressed_image_buffer.getvalue()

                # Add download button for the compressed image
                st.download_button(label="Download ColorCrafted Image", data=compressed_image_bytes, file_name=f"ColorCrafted Image_{number}_colors.png")
        except :
            st.error(f"Oops! We're sorry to inform you that an error has occurred. We kindly request that you try again later. Thank you for your understanding.")
    else:
        st.error("Please upload an image")
