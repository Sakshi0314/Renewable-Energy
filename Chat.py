import streamlit as st  # Import Streamlit library
import pandas as pd  # Import Pandas library
import base64  # Import base64 module for encoding images
from langchain_experimental.agents import create_pandas_dataframe_agent  # Import create_pandas_dataframe_agent function from langchain_experimental.agents
from langchain_groq import ChatGroq  # Import ChatGroq class from langchain_groq module
import os  # Import os module for environment variables
 
# Set environment variable for GROQ API key
os.environ["GROQ_API_KEY"] = "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"
 
# Define a function to read and encode images
def read_imgs(imgs_list):
    path_list = []  # Initialize an empty list to store encoded images
    for img in imgs_list:  # Iterate through the list of image files
        with open(img, "rb") as file_:  # Open each image file in binary mode
            contents = file_.read()  # Read the contents of the image file
            # Encode the image contents as base64 and decode to utf-8
            data_url = base64.b64encode(contents).decode("utf-8")
            path_list.append(data_url)  # Append the encoded image to the path list
    return path_list  # Return the list of encoded images
 
# Specify the list of image files to be encoded
file_list = ["./icon2.svg","./nature.svg"]
# Read and encode the images
img_list = read_imgs(file_list)
 
# Define a function to read CSV data into a Pandas DataFrame
def read_csv_into_dataframe(csv_name):
    df = pd.read_csv(csv_name)  # Read CSV data into a Pandas DataFrame
    return df  # Return the DataFrame
 
# Define a function to initialize the chatbot
def initialize_chatbot():
    # Read CSV data into a Pandas DataFrame
    data_frame = read_csv_into_dataframe(r"C:\Users\sakskuma\OneDrive - Capgemini\Documents\Renewable Energy POC\Merged_Facts.csv")
    # Initialize ChatGroq with temperature and model name
    llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
    # Create a chatbot agent using ChatGroq and Pandas DataFrame
    p_agent = create_pandas_dataframe_agent(llm=llm, df=data_frame, verbose=True, handle_parsing_errors=True)
    return p_agent  # Return the chatbot agent
 
# Define a function to get the chatbot agent
def get_chatbot_agent():
    if 'chatbot_agent' not in st.session_state:  # Check if chatbot agent exists in session state
        st.session_state.chatbot_agent = initialize_chatbot()  # Initialize chatbot agent if not present
    return st.session_state.chatbot_agent  # Return the chatbot agent
 
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data
# Load data for forecasting
forecast_data = load_data(r"C:\Users\sakskuma\OneDrive - Capgemini\Documents\Renewable Energy POC\Streamlit Renewable Energy\Forecasted_Final_Dataset.csv")
 
countries = [
    "United Arab Emirates", "United Kingdom", "United States", "Venezuela", "Vietnam", "Zambia", "Zimbabwe", "USSR",
    "Ukraine", "Turkey", "Yugoslavia", "United States Pacific Islands", "Wake Island", "United States Territories",
    "Yemen", "Western Sahara", "Western Africa", "West Germany", "Vanuatu", "Uzbekistan", "Uruguay",
    "United States Virgin Islands", "Uganda", "Tuvalu", "Turks and Caicos Islands", "Turkmenistan",
    "Trinidad and Tobago", "Tonga", "Thailand", "Taiwan", "Switzerland", "Spain", "South Korea",
    "South Africa", "Slovenia", "Slovakia", "Singapore", "Saint Helena", "Rwanda", "Russia", "Romania",
    "Qatar", "Portugal", "Poland", "Philippines", "Peru", "Palestine", "Oman", "Oceania", "Norway",
    "North Korea", "North America", "Nigeria", "New Caledonia", "Nepal", "Myanmar", "Mongolia",
    "Middle East", "Middle Africa", "Mexico", "Malaysia", "Madagascar", "Luxembourg", "Lithuania",
    "Latvia", "Kyrgyzstan", "Italy", "Israel", "Ireland", "Tunisia", "Togo", "Tajikistan", "Syria",
    "Sudan", "Sri Lanka", "South America", "Somalia", "Seychelles", "Sao Tome and Principe",
    "Saint Pierre and Miquelon", "Saint Kitts and Nevis", "Puerto Rico", "Persian Gulf", "Niue", "Niger",
    "New Zealand", "Netherlands", "Nauru", "Mozambique", "Morocco", "Moldova", "Micronesia", "Mauritania",
    "Martinique", "Malta", "Mali", "Maldives", "Macao", "Libya", "Lesotho", "Lebanon", "Kuwait", "Kenya",
    "Japan", "Tanzania", "Sweden", "Suriname", "Solomon Islands", "Serbia", "Saudi Arabia", "Saint Lucia",
    "Reunion", "Paraguay", "Pakistan", "North Macedonia", "Nicaragua", "Netherlands Antilles", "Montserrat",
    "Malawi", "Jordan", "Papua New Guinea", "Panama", "Namibia", "Mauritius", "South Sudan", "Sierra Leone",
    "Montenegro", "Kazakhstan", "Jamaica", "Samoa", "Northern Mariana Islands", "Liberia", "Laos", "Kiribati",
    "Senegal", "Latin America and Caribbean", "Saint Vincent and the Grenadines", "Kosovo", "South Central America",
    "Africa", "Europe", "Iraq", "Iran", "Indonesia", "India", "Iceland", "Hungary", "Hong Kong", "Guyana",
    "Guatemala", "Greece", "Gibraltar", "Germany", "French Polynesia", "France", "Finland", "Falkland Islands",
    "European Union", "Estonia", "Ecuador", "Eastern Africa", "Dominican Republic", "Denmark",
    "Democratic Republic of Congo", "Czechia", "Cyprus", "Croatia", "Colombia", "China", "Central America",
    "Cayman Islands", "Canada", "Cambodia", "Bulgaria", "Brazil", "Belgium", "Belarus", "Bangladesh",
    "Austria", "Australia", "Asia Pacific", "Asia", "Aruba", "Armenia", "Argentina", "Antigua and Barbuda",
    "Albania", "Afghanistan", "Honduras", "Greenland", "Ghana", "Gabon", "Eswatini", "Eritrea",
    "Equatorial Guinea", "El Salvador", "Egypt", "Cuba", "Cote d'Ivoire", "Costa Rica", "Congo", "Cameroon",
    "Burundi", "Brunei", "Bolivia", "Belize", "Barbados", "Bahrain", "Angola", "Algeria", "Guadeloupe",
    "Grenada", "Gambia", "French Guiana", "Faroe Islands", "Ethiopia", "Dominica", "Czechoslovakia", "Comoros",
    "Chad", "Botswana", "Benin", "Antarctica", "American Samoa", "Haiti", "Guam", "Fiji", "Cook Islands",
    "Chile", "Bermuda", "Guinea-Bissau", "Central African Republic", "Bhutan", "Azerbaijan", "Guinea",
    "East Germany", "Djibouti", "Cape Verde", "British Virgin Islands", "Burkina Faso",
    "Bosnia & Herzegovina", "East Timor", "Georgia", "Bahamas", "Hawaiian Trade Zone"
]
 
sources = [
    "Biofuel", "Carbon", "Coal", "Electricity", "Energy", "Fossil", "Gas", "Greenhouse", "Hydro",
    "Low_Carbon", "Other_Renewables", "Solar", "Wind", "Renewables", "Nuclear", "Oil"
]
 
categories = [
    "Consumption", "Cons_Change_Twh", "Share_Elec", "Share_Energy", "Cons_Change_Pct", "Cons_Per_Capital",
    "Electricity", "Elec_Per_Capital", "Intensity_Elec", "Prod_Change_Twh", "Production", "Prod_Change_Pct",
    "Prod_Per_Capital", "Demand", "Generation", "Per_Capital", "Per_Gdp", "Fuel_Consumption", "Energy_Per_Capital",
    "Gas_Emissions"
]
 
years = list(range(2023, 2033))

 


 
# Define the main function to create the Streamlit app
def main():
  
    
 
    # Set the title for the chatbot section
    st.title("Unified Chatbot")
    st.write("Welcome! How can I assist you today?")
    # Add radio button to choose functionality
    option = st.radio("Choose a functionality:", ("General Queries", "Energy Forecasting"))
 
    if option == "General Queries":
        # Add button to open chatbot
        
        chatbot_button = st.button("Open Chatbot")
 
        # Toggle chatbot visibility
        if 'show_chatbox' not in st.session_state:
            st.session_state.show_chatbox = False
 
        if chatbot_button:
            st.session_state.show_chatbox = not st.session_state.show_chatbox
 
        # Add CSS styles for the chatbox
        st.markdown("""
            <style>
            .chat-container-box {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 300px;
                max-width: 100%;
                border-radius: 8px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
                background-color: #fff;
                overflow: hidden;
                z-index: 1000;
                display: flex;
                flex-direction: column;
            }
            .chat-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: linear-gradient(to top, #7028e4 0%, #e5b2ca 100%);
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            .chatbox__heading--header {
                font-size: 30px;
                font-weight: bold;
                margin: 0;
                align-items: center;
            }
            .chatbox__description--header {
                font-size: 20px;
                color: white;
                margin: 0;
                align-items: center;
            }
           
           
            .chat-header button {
                background-color: #0084ff;
                border: none;
                color: white;
                padding: 10px;
                cursor: pointer;
                position: relative;
            }
            .close-icon--header {
                position: absolute;
                top: 8px;
                right: 8px;
                cursor: pointer;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .close-icon--header svg {
                width: 20px;
                height: 20px;
            }
            .chat-body {
                background-color: #f9f9f9;
                padding: 10px;
                max-height: 400px;
                overflow-y: auto;
            }
            .chat-message {
                display: flex;
                align-items: flex-end;
                margin-bottom: 10px;
            }
            .user-message {
                justify-content: flex-end;
            }
            .bot-message {
                justify-content: flex-start;
            }
            .message-content {
                max-width: 70%;
                padding: 8px 12px;
                border-radius: 10px;
                word-wrap: break-word;
            }
            .user-message .message-content {
                background: radial-gradient(circle at 10% 20%, rgb(210, 36, 129) 0%, rgb(152, 75, 215) 90%);
                color: white;
            }
            .bot-message .message-content {
                background: linear-gradient(69.5deg, rgba(189, 73, 255, 0.99) 18.6%, rgb(254, 76, 227) 85.9%);
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)
 
        if st.session_state.show_chatbox:
            # Add container for chatbox
            chatbox_container = st.markdown('<div class="chat-container-box" id="chatbox">', unsafe_allow_html=True)
 
            # Add header for chatbox
            st.markdown(f'''
                <div class="chat-header">
                    <div>
                        <img src="data:image/svg+xml;base64,{img_list[0]}" alt="Icon" style="height: 80px; width: 80px;">
                    </div>
                    <div>
                        <h4 class="chatbox__heading--header">Need Assistance?</h4>
                        <p class="chatbox__description--header">We're here to help!</p>
                    </div>
                    <div>
                        <span class="close-icon--header" onclick="toggleChatbox()">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                                <path fill="none" d="M0 0h24v24H0z" />
                                <path
                                    d="M18.3 5.71a1 1 0 0 0-1.42 0L12 10.59 7.12 5.71a1 1 0 0 0-1.42 1.42L10.59 12 5.71 16.88a1 1 0 0 0 1.42 1.42L12 13.41l4.88 4.88a1 1 0 0 0 1.42-1.42L13.41 12l4.88-4.88a1 1 0 0 0 0-1.41z" />
                            </svg>
                        </span>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
 
            # Add body for chatbox
            chatbox_body = st.container()
            with chatbox_body:
                st.markdown('<div class="chat-body">', unsafe_allow_html=True)
 
                p_agent = get_chatbot_agent()
 
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
 
                # Display chat history
                for idx, chat in enumerate(st.session_state.chat_history):
                    user_msg = f'<div class="chat-message user-message"><div class="message-content">{chat["user"]}</div></div>'
                    bot_msg = f'<div class="chat-message bot-message"><div class="message-content">{chat["bot"]}</div></div>'
                    st.markdown(user_msg, unsafe_allow_html=True)
                    st.markdown(bot_msg, unsafe_allow_html=True)
               
                # Add form for user input
                with st.form(key='query_form', clear_on_submit=True):
                    user_input = st.text_area("Type your message here", key="user_input", max_chars=200)
                    submit_button = st.form_submit_button(label='Send')
 
                    if submit_button and user_input:
                        # Custom rule-based intent handling
                        intent_map = {
                            "overview_dashboard": ["explore the power bi overview dashboard","overview dashboard","overview"],
                            "analysis_by_country_dashboard": ["explore the power bi analysis by country dashboard","analysis by country dashboard","analysis by country"],
                            "analysis_by_consumption_and_production_dashboard": ["explore the power bi analysis by consumption and production dashboard","analysis by consumption and production dashboard","analysis by consumption and production"],
                            "analysis_by_time_period_dashboard": ["explore the power bi analysis by time period dashboard","analysis by time period dashboard","analysis by time period"],
                            "analysis_by_source_type_dashboard": ["explore the power bi analysis by source type dashboard","analysis by source type dashboard","analysis by source type"]
                        }
 
                        matched_intent = None
                        for intent, queries in intent_map.items():
                            if user_input.lower() in queries:
                                matched_intent = intent
                                break
 
                        if matched_intent:
                            # Handle intents based on matched_intent
                            if matched_intent == "overview_dashboard":
                                # Provide a link to the Overview Dashboard
                                response = "Here is the overview link:<a href='https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSectionb5d52a42a5e09cc4999e?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61' target='_blank'> Overview Dashboard</a>"
                            elif matched_intent == "analysis_by_country_dashboard":
                                # Provide a link to the Analysis by Country Dashboard
                                response = "Here is the analysis by country link:<a href='https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection72e06a3f8548eb033bd7?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61' target='_blank'>Analysis by Country Dashboard</a>"
                            elif matched_intent == "analysis_by_consumption_and_production_dashboard":
                                # Provide a link to the Analysis by Consumption and Production Dashboard
                                response = "Here is the analysis by consumption and production link:<a href='https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection2a182f18009d4398165c?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61' target='_blank'>Analysis by Consumption and Production Dashboard</a>"
                            elif matched_intent == "analysis_by_time_period_dashboard":
                                # Provide a link to the Analysis by Time Period Dashboard
                                response = "Here is the analysis by time period link:<a href='https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection173aa1ed3028e0ebcb99?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61' target='_blank'>Analysis by Time Period Dashboard</a>"
                            elif matched_intent == "analysis_by_source_type_dashboard":
                                # Provide a link to the Analysis by Source Type Dashboard
                                response = "Here is the analysis by source type link:<a href='https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection0a6876d84acc170dc3e0?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61' target='_blank'>Analysis by Source Type Dashboard</a>"
                        else:
                            # Use the chatbot to provide a response
                            response = p_agent.run(user_input)
                        st.session_state.chat_history.append({"user": user_input, "bot": response})
                        st.experimental_rerun()
 
                st.markdown('</div>', unsafe_allow_html=True)
 
            st.markdown('</div>', unsafe_allow_html=True)
 
        # JavaScript for toggle functionality
        st.markdown("""
            <script>
            function toggleChatbox() {
                const chatbox = document.getElementById('chatbox');
                if (chatbox.style.display === 'none' || chatbox.style.display === '') {
                    chatbox.style.display = 'block';
                } else {
                    chatbox.style.display = 'none';
                }
            }
            </script>
        """, unsafe_allow_html=True)
       
 
    elif option == "Energy Forecasting":
        st.title("Energy Forecaster")
 
        # User inputs
        country = st.selectbox("Select Country", countries)
        category = st.selectbox("Select Category", categories)
        source = st.selectbox("Select Source", sources)
        year = st.selectbox("Select Year", years)
 
        # Corrected column names
        filtered_data = forecast_data[(forecast_data['Country'] == country) &
                                      (forecast_data['Type_of_Category'] == category) &
                                      (forecast_data['Source_Type'] == source) &
                                      (forecast_data['Next 10 Forecasted Year'] == year)]
 
        # Display the filtered forecasted value
        if not filtered_data.empty:
            forecasted_value = filtered_data['Forecasted Total_Energy'].values[0]
            st.write(f"The forecasted value for {country} in {category} from {source} for the year {year} is: {forecasted_value}")
        else:
            st.write("No data available for the selected filters.")
 
        # If you want to display the entire filtered dataframe
        st.write("Filtered Data")
        st.dataframe(filtered_data)
 
if __name__ == "__main__":
    main()