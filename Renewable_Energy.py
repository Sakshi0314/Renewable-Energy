import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_groq import ChatGroq
import os

# Custom CSS and JavaScript for falling leaves animation and background image
st.markdown(
    """
    <style>
    /* Background image class */
    .background {
        background-image: url('G.jpeg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        height: 100vh;
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
        z-index: -1;
    }
    /* Hide the default arrow icon */
    [data-testid="collapsedControl"] > div:first-child {
        display: none;
    }
    /* Style the collapsed control area (where arrow would be) */
    [data-testid="collapsedControl"] {
        cursor: pointer; /* Add cursor pointer for hover effect */
        position: relative; /* Enable positioning for child element */
    }
    /* Hover message for collapsed control area */
    [data-testid="collapsedControl"]:hover::after {
        content: "Click here to open chatbot";
        background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black background */
        color: #fff; /* White text color */
        padding: 10px; /* Add padding for better visibility */
        border-radius: 5px; /* Add rounded corners */
        font-size: 14px; /* Adjust font size for message */
        display: none; /* Initially hide the message */
    }
    /* Display hover message on hover */
    [data-testid="collapsedControl"]:hover::after {
        display: block; /* Show the message on hover */
    }
    /* Replace with a leaf emoji and increase its size */
    [data-testid="collapsedControl"]::before {
        content: "🍃";
        font-size: 100px; /* Adjust the size as needed */
        display: inline-block;
    }
    /* Falling leaves animation */
    .leaf {
        position: fixed;
        top: -10%;
        width: 30px;  /* Adjust leaf size */
        height: 30px;
        background-image: url('https://cdn-icons-png.flaticon.com/512/4834/4834559.png');
        background-size: contain;
        background-repeat: no-repeat;
        opacity: 0.8;
        z-index: 9999;
        animation: fall 5s linear infinite;
    }
    @keyframes fall {
        0% {
            transform: translateX(0) translateY(0) rotate(0deg);
        }
        100% {
            transform: translateX(calc(100vw - 50px)) translateY(calc(100vh + 50px)) rotate(360deg);
        }
    }
    /* Sun emoji at the top right */
    .sun {
        position: fixed;
        top: 35px;
        right: 35px;
        font-size: 60px;  /* Increase the font-size for a bigger sun */
    }
    /* Center the main heading, make it bold and cursive, and position it higher */
    .main-title {
        font-family: 'Dancing Script', cursive;
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        margin-top: 10px; /* Adjust this value to move the heading higher */
        margin-bottom: 30px; /* Adjust this value to add space between heading and dashboard */
    }
    </style>
    <script>
    function createLeaf() {
        const leaf = document.createElement('div');
        leaf.className = 'leaf';
        leaf.style.left = Math.random() * 100 + 'vw';  // Random horizontal position
        leaf.style.animationDuration = Math.random() * 2 + 3 + 's';  // Random duration between 3 and 5 seconds
        document.body.appendChild(leaf);
        setTimeout(() => {
            leaf.remove();
        }, 5000);
    }
    document.querySelector('[data-testid="collapsedControl"]').addEventListener('click', () => {
        for (let i = 0; i < 10; i++) {
            setTimeout(createLeaf, i * 300);
        }
    });
    </script>
    """
    , unsafe_allow_html=True
)

# Adding a div with the background class
st.markdown('<div class="background"></div>', unsafe_allow_html=True)

# Display the leaf emoji
st.markdown('<div class="leaf">☁</div>', unsafe_allow_html=True)

# Display the sun emoji at the top right
st.markdown('<div class="sun">🌞</div>', unsafe_allow_html=True)

# Sidebar for chatbot options
st.sidebar.title("Chatbot Options")
chatbot_option = st.sidebar.selectbox("Choose a chatbot:", ("Leaf Chatbot 🌿", "Forecasting Chatbot 🔮"))
st.sidebar.title(chatbot_option)

# Initialize session state for chatbot
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    st.sidebar.write(message)

# Input box for user to send a new message
user_input = st.sidebar.text_input("You:", "")

# Set environment variable for the chatbot API key
os.environ["GROQ_API_KEY"] = "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"

# Leaf Chatbot functionality
def read_csv_into_dataframe(csv_name):
    df = pd.read_csv(csv_name)
    return df

def initialize_chatbot():
    data_frame = read_csv_into_dataframe("Merged.csv")  # Replace with the path to your CSV file
    llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
    p_agent = create_pandas_dataframe_agent(llm=llm, df=data_frame, verbose=True, handle_parsing_errors=True)
    return p_agent

def get_chatbot_agent():
    if 'chatbot_agent' not in st.session_state:
        st.session_state.chatbot_agent = initialize_chatbot()
    return st.session_state.chatbot_agent

# Define the Leaf Chatbot functionality with Power BI links
def leaf_chatbot(user_input):
    # Define keywords or patterns to recognize intents
    overview_keywords = ["overview", "summary", "general"]
    country_keywords = ["country", "nation", "analyze by country"]
    consumption_production_keywords = ["consumption", "production", "energy usage"]
    time_period_keywords = ["time period", "timeframe", "timeline"]
    source_type_keywords = ["source type", "energy source", "analyze by source"]

    # Define direct URLs for each dashboard
    overview_dashboard_url = "https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSectionb5d52a42a5e09cc4999e?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61"
    country_dashboard_url = "https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection72e06a3f8548eb033bd7?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61"
    consumption_production_dashboard_url = "https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection2a182f18009d4398165c?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61"
    time_period_dashboard_url = "https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection173aa1ed3028e0ebcb99?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61"
    source_type_dashboard_url = "https://app.powerbi.com/groups/me/reports/8ce894b8-ca32-40f8-a4c6-84a41fda4a18/ReportSection0a6876d84acc170dc3e0?ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61"

    # Check if user input matches any intent
    if any(keyword in user_input.lower() for keyword in overview_keywords):
        # Display Overview Dashboard
        return f"[Overview Dashboard]({overview_dashboard_url})"
    elif any(keyword in user_input.lower() for keyword     in country_keywords):
        # Display Country Analysis Dashboard
        return f"[Country Analysis Dashboard]({country_dashboard_url})"
    elif any(keyword in user_input.lower() for keyword in consumption_production_keywords):
        # Display Consumption and Production Dashboard
        return f"[Consumption and Production Dashboard]({consumption_production_dashboard_url})"
    elif any(keyword in user_input.lower() for keyword in time_period_keywords):
        # Display Time Period Analysis Dashboard
        return f"[Time Period Analysis Dashboard]({time_period_dashboard_url})"
    elif any(keyword in user_input.lower() for keyword in source_type_keywords):
        # Display Source Type Analysis Dashboard
        return f"[Source Type Analysis Dashboard]({source_type_dashboard_url})"
    else:
        # Handle other queries using the LLM
        p_agent = get_chatbot_agent()
        response = p_agent.run(user_input)
        return response

# Forecasting Chatbot functionality
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

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

forecasting_data = load_data("Forecasted_Final_CSV_Dataset.csv")

def forecasting_chatbot():
    country = st.sidebar.selectbox("Select Country", countries)
    category = st.sidebar.selectbox("Select Category", categories)
    source = st.sidebar.selectbox("Select Source", sources)
    year = st.sidebar.selectbox("Select Year", years)
    filtered_data = forecasting_data[(forecasting_data['Country'] == country) &
                                     (forecasting_data['Type_of_Category'] == category) &
                                     (forecasting_data['Source_Type'] == source)]
    if not filtered_data.empty:
        st.sidebar.write(f"Showing forecasted values for {country} in {category} from {source}:")
        # Plotting the line graph
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_data['Next 10 Forecasted Year'], filtered_data['Forecasted Total_Energy'], marker='o')
        plt.title(f"Forecasted Total Energy for {country} ({category}, {source})")
        plt.xlabel("Year")
        plt.ylabel("Forecasted Total Energy")
        plt.grid(True)
        st.sidebar.pyplot(plt)
        # Display the forecasted value for the selected year
        selected_year_data = filtered_data[filtered_data['Next 10 Forecasted Year'] == year]
        if not selected_year_data.empty:
            forecasted_value = selected_year_data['Forecasted Total_Energy'].values[0]
            st.sidebar.write(f"The forecasted value for {country} in {category} from {source} for the year {year} is: {forecasted_value}")
        else:
            st.sidebar.write("No data available for the selected year.")
    else:
        st.sidebar.write("No data available for the selected filters.")

# Integrating the chatbot functionality into the sidebar
if chatbot_option == "Leaf Chatbot 🌿":
    if user_input:
        response = leaf_chatbot(user_input)
        st.session_state.messages.append(f"You: {user_input}")
        st.session_state.messages.append(f"Leaf Chatbot: {response}")
        st.sidebar.write(f"Leaf Chatbot: {response}")
elif chatbot_option == "Forecasting Chatbot 🔮":
    forecasting_chatbot()

# Main content
st.markdown('<div class="main-title">Renewable Energy Project</div>', unsafe_allow_html=True)

# Embed the Power BI report
power_bi_report_url = "https://app.powerbi.com/reportEmbed?reportId=cecb7dd7-2dbf-4a63-9682-65a737ae83ea&autoAuth=true&ctid=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61"
st.markdown(f'<iframe width="1000" height="600" src="{power_bi_report_url}" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)


