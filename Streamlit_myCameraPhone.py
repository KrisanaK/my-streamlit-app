import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np

st.title("📦 Barcode + QR Scanner")
st.write("Capture your label using the mobile camera")

image_file = st.camera_input("Take a photo")

if image_file is not None:
    image = Image.open(image_file)
    img_np = np.array(image)

    decoded = decode(img_np)
    if decoded:
        st.success(f"✅ Detected {len(decoded)} code(s)")
        for obj in decoded:
            st.write(f"**Type:** {obj.type}")
            st.code(obj.data.decode('utf-8'))
    else:
        st.warning("No barcode or QR code detected. Try again.")
