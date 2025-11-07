import streamlit as st
from pyzxing import BarCodeReader
from PIL import Image
import numpy as np
import tempfile

st.title("📦 Barcode + QR Scanner")

image_file = st.camera_input("Take a photo")

if image_file is not None:
    image = Image.open(image_file)
    
    # Save to a temp file for ZXing
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name)
        reader = BarCodeReader()
        results = reader.decode(tmp.name)
    
    if results:
        st.success(f"✅ Detected {len(results)} code(s)")
        for r in results:
            st.write(f"**Type:** {r.get('format')}")
            st.code(r.get('raw', ''))
    else:
        st.warning("No barcode or QR code detected. Try again.")
