import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Clone Modified Dates Between Folders", page_icon="🕒", layout="wide")

st.title("🕒 Clone File Modified Dates Between Folders")
st.write("Select two folders — the **source** (right side) and the **target** (left side). The app will copy modified dates for matching filenames.")

# --- Folder Inputs ---
col1, col2 = st.columns(2)
with col1:
    left_dir = st.text_input("📁 Left Side Directory (Target)", r"C:\Spektra\TO-247")
with col2:
    right_dir = st.text_input("📂 Right Side Directory (Source)", r"\\192.168.11.4\TestPGM\TO-247")

# --- Helper Functions ---
def get_modified_date(file_path):
    """Get modified datetime of a file."""
    if not os.path.exists(file_path):
        return None
    return datetime.fromtimestamp(os.path.getmtime(file_path))

def set_modified_date(file_path, dt):
    """Set modified datetime of a file."""
    ts = dt.timestamp()
    os.utime(file_path, (ts, ts))

# --- Main Logic ---
if st.button("🚀 Clone Modified Dates"):
    if not os.path.exists(left_dir):
        st.error(f"Left directory not found: {left_dir}")
    elif not os.path.exists(right_dir):
        st.error(f"Right directory not found: {right_dir}")
    else:
        left_files = {f: os.path.join(left_dir, f) for f in os.listdir(left_dir) if os.path.isfile(os.path.join(left_dir, f))}
        right_files = {f: os.path.join(right_dir, f) for f in os.listdir(right_dir) if os.path.isfile(os.path.join(right_dir, f))}

        results = []
        for fname, left_path in left_files.items():
            if fname in right_files:
                right_path = right_files[fname]
                src_time = get_modified_date(right_path)
                if src_time:
                    try:
                        set_modified_date(left_path, src_time)
                        results.append((fname, src_time.strftime("%Y-%m-%d %H:%M:%S"), "✅ Updated"))
                    except Exception as e:
                        results.append((fname, "-", f"⚠️ Error: {e}"))
                else:
                    results.append((fname, "-", "❌ Source file missing"))
            else:
                results.append((fname, "-", "❌ No match in source folder"))

        # Display results
        st.subheader("Processing Results")
        st.table({
            "Filename": [r[0] for r in results],
            "Cloned Modified Time": [r[1] for r in results],
            "Status": [r[2] for r in results]
        })

        st.success("✅ Process complete!")
