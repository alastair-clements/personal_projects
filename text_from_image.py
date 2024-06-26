import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import shutil

# Ensure tesseract is installed and available in PATH
tesseract_cmd = shutil.which("tesseract")
st.write(f"Tesseract path: {tesseract_cmd}")  # Log the Tesseract path

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
else:
    st.error("Tesseract not found. Ensure it is installed and in your PATH.")
    st.stop()

def extract_text_from_image(image):
    try:
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def process_images_to_csv(images, output_csv):
    f = []
    t = []

    for img, filename in images:
        try:
            text = extract_text_from_image(img)
            if text:
                f.append(filename)
                t.append(text)
        except Exception as e:
            st.error(f"Error processing {filename}: {e}")
            continue

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(list(zip(f, t)), columns=['file_Name', 'Text'])

    # Write the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    return df

def main():
    st.title("Image Text Extractor")

    # File uploader for multiple image files
    uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        images = [(Image.open(file), file.name) for file in uploaded_files]
        if st.button("Extract Text"):
            with st.spinner('Processing...'):
                output_csv = 'output_text.csv'
                df = process_images_to_csv(images, output_csv)
                st.success(f"Text extracted and saved to {output_csv}")
                st.dataframe(df)
                # Provide a download link
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name='output_text.csv',
                    mime='text/csv'
                )

if __name__ == "__main__":
    main()
