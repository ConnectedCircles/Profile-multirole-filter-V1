import pandas as pd
import streamlit as st
import base64

def app():
    
    # Set title and subtitle, additional text
    st.title("Universal Profile Filter V1")
    st.subheader("Property of Connected Circles")
    st.write("""This app allows you to filter lists of profiles by keywords across any column in a table. Keywords must 
    be separated by a comma, whitespace will be considered a part of a keyword. You can preview the both the labeled and filtered data in the two preview 
    windows below. You can download the data either labeled, filtered or filtered profile URLs only, all as a .csv""")
    
    

    
    # Get user input for substrings
    default_substringsCS = ['CEO', 'COO', 'CFO', 'CTO', 'CHRO', 'CMO', 'CLO', 'CSO', 'CIO', 'CTIO', 'CSIO', 'CCO', 'CDO', 'VP']
    substringsCS = st.text_input("Enter case-sensitive keywords separated by comma", ", ".join(default_substringsCS)).split(",")
    substringsCI = st.text_input("Enter case-insensitive keywords separated by comma", "").split(",")
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file to filter", type="csv")
    

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Define the list of columns in the dataframe
        columns_list = list(df.columns)
        # Add a dropdown menu to select a column
        column = st.selectbox('Select a column', options=columns_list)
        
        

        # Create a boolean mask to identify rows where the selected column contains any of the case-sensitive substrings
        maskCS = df[column].str.contains('|'.join(substringsCS))

        # Create a boolean mask to identify rows where the selected column contains any of the case-insensitive substrings
        maskCI = df[column].str.contains('|'.join(substringsCI), case=False)

        # Create a new column called "Filter Criteria" with a value of "Yes" for rows that match either condition, and "No" otherwise
        df['Filter Criteria'] = (maskCS | maskCI).map({True: 'Yes', False: 'No'})

        # Filter to only include Filter Criteria = Yes, delete "Filter Criteria" column
        dffiltered = df[df["Filter Criteria"]=="Yes"]
        dffiltered = dffiltered.drop("Filter Criteria", axis=1)

        # Download link for filtered data
        csv_filtered = dffiltered.to_csv(index=False)
        b64_filtered = base64.b64encode(csv_filtered.encode('utf-8')).decode()
        href_filtered = f'<a href="data:file/csv;base64,{b64_filtered}" download="filtered_data.csv">Download Filtered CSV File</a>'
        
        # Download link for unfiltered data
        csv_unfiltered = df.to_csv(index=False)
        b64_unfiltered = base64.b64encode(csv_unfiltered.encode('utf-8')).decode()
        href_unfiltered = f'<a href="data:file/csv;base64,{b64_unfiltered}" download="unfiltered_data.csv">Download Unfiltered Labeled CSV File</a>'
        
        # Download link for filtered data URLs only, no header
        url_col = dffiltered["Profile url"].dropna().astype(str)
        csv_url = url_col.to_csv(index=False, header=False)
        b64_url = base64.b64encode(csv_url.encode('utf-8')).decode()
        href_url = f'<a href="data:file/csv;base64,{b64_url}" download="profile_urls.csv">Download Filtered Profile URLs only CSV File</a>'


##### DISPLAY OF RESULTS #####
        
        # Display both filtered and unfiltered data in two windows with links to download each below
        col1, col2 = st.beta_columns(2)
        with col1:
            st.write("Unfiltered Data")
            st.write(df)
            st.markdown(href_unfiltered, unsafe_allow_html=True)
        with col2:
            st.write("Filtered Data")
            st.write(dffiltered)
            st.markdown(href_filtered, unsafe_allow_html=True)
            
        # Display the link to download profile URLs of filtered data only
        st.markdown(href_url, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
