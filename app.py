import streamlit as st
import cv2
import numpy as np
import tempfile
import os

if "saved_count" not in st.session_state:
    st.session_state.saved_count = 0

st.set_page_config(page_title="Anti-AI Digital Vaccine", page_icon="🛡️", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ Anti-AI Digital Vaccine (Enterprise Edition)</h1>", unsafe_allow_html=True)

st.sidebar.title("🛡️ Vaccine Controls")
st.sidebar.write(f"📊 Free Shielded Images Saved: **{st.session_state.saved_count} / 2**")
shield_strength = st.sidebar.slider("Digital Vaccine Shield Strength", min_value=0.01, max_value=0.20, value=0.04, step=0.01, key="app_main_shield_slider_unique")

st.sidebar.markdown("<br><hr>", unsafe_allow_html=True)
st.sidebar.subheader("🔮 Future Enterprise Roadmap")
st.sidebar.info("🎙️ Voice Deepfake Protection Engine (Coming Soon in v2.0 - Q3 2026)")

if st.session_state.saved_count >= 2:
    st.error("🚨 2-FREE TRIAL USES EXPIRED!")
    st.info("🔒 Enterprise Edition Paywall: You have reached the limit for free digital vaccine shielding.")
    st.stop()

tab1, tab2 = st.tabs(["📸 Targeted Photo Vaccine", "🎬 Targeted Video Vaccine"])

with tab1:
    st.subheader("Upload Photo for Digital Shielding")
    uploaded_image = st.file_uploader("Choose a JPG or PNG Image...", type=["jpg", "jpeg", "png"], key="photo_uploader_unique_key")
    if uploaded_image is not None:
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        noise = np.random.normal(0, shield_strength * 255, opencv_img.shape).astype(np.int16)
        protected_img = cv2.add(opencv_img.astype(np.int16), noise)
        protected_img = np.clip(protected_img, 0, 255).astype(np.uint8)
        col1, col2 = st.columns(2)
        with col1:
            st.image(opencv_img, channels="BGR", caption="Original Photo (Vulnerable)")
        with col2:
            st.image(protected_img, channels="BGR", caption="🛡️ Vaccinated Photo (Protected Against AI)")
        is_success, buffer = cv2.imencode(".png", protected_img)
        if is_success:
            if st.download_button(label="📥 Download Vaccinated Photo", data=buffer.tobytes(), file_name="vaccinated_photo.png", mime="image/png", key="photo_download_btn_unique_key"):
                st.session_state.saved_count += 1
                st.rerun()

with tab2:
    st.subheader("Upload Video for Structural Shielding")
    uploaded_video = st.file_uploader("Choose an MP4 Video...", type=["mp4", "avi", "mov"], key="video_uploader_unique_key")
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        tfile.close()
        cap = cv2.VideoCapture(tfile.name)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        output_path = os.path.join(tempfile.gettempdir(), "protected_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        progress_bar = st.progress(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            noise = np.random.normal(0, shield_strength * 255, frame.shape).astype(np.int16)
            protected_frame = cv2.add(frame.astype(np.int16), noise)
            protected_frame = np.clip(protected_frame, 0, 255).astype(np.uint8)
            out.write(protected_frame)
        cap.release()
        out.release()
        with open(output_path, "rb") as f:
            if st.download_button(label="📥 Download Vaccinated Video", data=f.read(), file_name="vaccinated_video.mp4", mime="video/mp4", key="video_download_btn_unique_key"):
                st.session_state.saved_count += 1
                st.rerun()
        os.unlink(tfile.name)
  
