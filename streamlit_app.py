import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import pandas as pd
import streamlit as st

# Function to process TRACS data
def check_tracs(link_section, data):
    # Filter data based on the Link Section Number
    filtered_data = data[data["Link Section"] == link_section]

    # Check if any rows match the Link Section
    if filtered_data.empty:
        return f"No data found for Link Section: {link_section}"

    # Prepare the results
    results = f"Results for Link Section: {link_section}\n\n"
    failure_found = False

    for _, row in filtered_data.iterrows():
        lane = row["Lane"]
        start_chainage = row["Start Chainage"]
        end_chainage = row["End Chainage"]
        rutting = row["Rutting"]
        texture = row["Texture"]

        # Check conditions
        rutting_status = "Failed" if rutting > 15 else "Passed"
        texture_status = "Failed" if texture < 0.8 else "Passed"

        if rutting_status == "Failed" or texture_status == "Failed":
            failure_found = True
            results += (
                f"Lane: {lane}, Start Chainage: {start_chainage}, End Chainage: {end_chainage}\n"
                f"Rutting: {rutting} ({rutting_status})\n"
                f"Texture: {texture} ({texture_status})\n\n"
            )

    if failure_found:
        return results
    else:
        return f"No TRACS Failures found for Link Section: {link_section}"

# Streamlit UI
st.title("TRACS Failure Checker")

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file with TRACS data", type="xlsx")

if uploaded_file:
    # Read the Excel file
    try:
        data = pd.read_excel(uploaded_file, sheet_name="Sheet2")

        # Display the first few rows of data
        st.write("### Preview of Uploaded Data:")
        st.write(data.head())

        # Input for Link Section Number
        link_section = st.text_input("Enter Link Section Number:")

        # Check TRACS when button is clicked
        if st.button("Check TRACS"):
            if link_section.strip():
                result = check_tracs(link_section.strip(), data)
                st.write("### Results:")
                st.text(result)
            else:
                st.warning("Please enter a valid Link Section Number.")
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
