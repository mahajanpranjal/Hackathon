import streamlit as st
import requests
import base64
from io import BytesIO
 
FASTAPI_URL = "http://127.0.0.1:8000"
 
st.title(" AI Stock Research Assistant")
 
query = st.text_input("Enter your query (e.g., 'Generate Apple stock report for last month'):")
 
if query and st.button("Generate Report"):
    with st.spinner("Generating AI-powered financial report..."):
        response = requests.post(f"{FASTAPI_URL}/search", json={"query": query})
 
    if response.status_code == 200:
        result = response.json()
        
 
        st.subheader(" AI-Generated Financial Report:")
        st.write(result.get("financial_report", "No report generated."))
 
        # Display Stock Chart
      
 
        # Display AI-Generated Financial Images
        
        #st.subheader("AI-Generated Financial Visuals:")
        #images = result.get("ai_generated_images", [])
        #if images:
         #   for img_url in images:
          #      st.image(img_url, use_column_width=True)
        #else:
         #   st.warning("No AI-generated images available.")
        
        
        st.subheader(" Chart Generated:")
        chart_base64 = result.get("chart_path")
 
        if chart_base64:
            try:
                # Decode base64 image
                image_bytes = base64.b64decode(chart_base64.split(",")[1])  # Remove "data:image/png;base64,"
                image = BytesIO(image_bytes)
                st.image(image, use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying image: {e}")
        else:
             st.error("No chart available.")
 
        pdf_report = result.get("pdf_report", None)
        if pdf_report:
            st.subheader("Download Full Financial Report:")
            st.markdown(f"""
            <a href="http://127.0.0.1:8000/download_report" download target="_blank">
                📄 Download Full PDF
            </a>
            """, unsafe_allow_html=True)

        else:
            st.warning("No PDF report available.")
            
    else:
        st.error(" API call failed.")
 
 
 