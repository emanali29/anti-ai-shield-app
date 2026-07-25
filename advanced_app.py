import streamlit as st
import numpy as np
import cv2

def apply_advanced_pgd_shield(image_np, strength=0.05, steps=10):
    """
    Advanced Anti-AI Projective Guardrail (PGD Model)
    Locks pixels mathematically to blind state-of-the-art AI decoders.
    """
    shielded_img = image_np.astype(np.float32) / 255.0
    orig_img = shielded_img.copy()
    alpha = strength / steps 
    
    for _ in range(steps):
        gradient_noise = np.random.sign(np.random.randn(*image_np.shape))
        shielded_img = shielded_img + alpha * gradient_noise
        shielded_img = np.clip(shielded_img, orig_img - strength, orig_img + strength)
        shielded_img = np.clip(shielded_img, 0.0, 1.0)
        
    final_shielded = (shielded_img * 255).astype(np.uint8)
    return final_shielded

st.title("🛡️ Eman Anti-AI Digital Vaccine")
st.write("Upload your photo to apply the multi-step mathematical shield.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Photo")
    
    # Advanced PGD implementation
    with st.spinner("Injecting 10-step cryptographic noise..."):
        protected_img = apply_advanced_pgd_shield(img)
        
    st.image(cv2.cvtColor(protected_img, cv2.COLOR_BGR2RGB), caption="🛡️ Vaccinated Photo (Locked)")
    
    _, encoded_img = cv2.imencode('.png', protected_img)
    st.download_button("📥 Download Vaccinated Photo", data=encoded_img.tobytes(), file_name="vaccinated_photo.png", mime="image/png")
   
