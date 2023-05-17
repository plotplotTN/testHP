import streamlit as st
#un script python pour streamlit qui utilise rembg pour supprimer l'arrière plan d'une image


print("helloworld")
st.title("Rimouveur de la mort")
image_upload= st.file_uploader("Upload an image", type=["png","jpg","jpeg"])

if image_upload:
    st.download_button("Download", image_upload,"image.png",mim="image/png")


