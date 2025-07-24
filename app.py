import streamlit as st
import pandas as pd 
import mysql.connector
import plotly.express as px
from chatbot import smart_mining_chat

# Loading CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply CSS
local_css("style.css")

# Connecting to MySQL database
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_equipment_data():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Chintu@2003',
        database='predictions'
    )
    query = "SELECT * FROM predictions"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to categorize health based on temperature and vibration
def assign_status(row):
    if row['temperature'] > 75 or row['vibration'] > 5:
        return 'Critical'
    elif row['temperature'] > 60 or row['vibration'] > 3:
        return 'Warning'
    else:
        return 'Good'

# Creating the page UI
st.set_page_config(page_title="SmartMining", layout="wide")

tabs = ["Dashboard", "Equipments", "SmartMineAI Assistant"]
selected_tab = st.sidebar.radio("Menu", tabs)

# Load equipment data once (used across tabs)
df = get_equipment_data()
df['Status'] = df.apply(assign_status, axis=1)

if selected_tab == "Dashboard":
    st.header("SmartMining Dashboard")

    # KPIs
    total_machines = len(df)
    critical_count = (df['Status'] == 'Critical').sum()
    warning_count = (df['Status'] == 'Warning').sum()
    good_count = (df['Status'] == 'Good').sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Machines", total_machines)
    col2.metric("Critical", critical_count)
    col3.metric("Warning", warning_count)
    col4.metric("Good", good_count)

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie Chart - Health Distribution
        health_dist = df['Status'].value_counts().reset_index()
        health_dist.columns = ['Status', 'count']
        fig1 = px.pie(health_dist, names='Status', values='count', 
                    title='Machine Health Distribution',
                    color='Status',
                    color_discrete_map={
                        'Good': 'green',
                        'Warning': 'orange',
                        'Critical': 'red'
                    })
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Bar Chart - Runtime Hours by Equipment
        fig3 = px.bar(df, x='equipment_id', y='runtime_hours', 
                     title='Runtime Hours by Equipment',
                     color='Status', 
                     color_discrete_map={
                         'Critical': 'red',
                         'Warning': 'orange',
                         'Good': 'green'
                     })
        st.plotly_chart(fig3, use_container_width=True)

    # Line Chart - Average Temperature Over Time
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        temp_trend = df.groupby(pd.Grouper(key='timestamp', freq='D'))['temperature'].mean().reset_index()
        fig2 = px.line(temp_trend, x='timestamp', y='temperature', 
                      title='Average Temperature Over Time')
        st.plotly_chart(fig2, use_container_width=True)

    # Top 5 machines by vibration
    st.subheader("Top 5 Machines by Vibration")
    top_vibrations = df.sort_values(by='vibration', ascending=False).head(5)
    st.dataframe(top_vibrations[['equipment_id', 'vibration', 'temperature', 'Status']])

elif selected_tab == "Equipments":
    st.header("Equipment Details")
    
    # Add filtering options
    status_filter = st.multiselect(
        "Filter by Status",
        options=['Critical', 'Warning', 'Good'],
        default=['Critical', 'Warning', 'Good']
    )
    
    filtered_df = df[df['Status'].isin(status_filter)] if status_filter else df
    
    st.dataframe(
        filtered_df.style.applymap(
            lambda x: 'background-color: #ffe6e6' if x == 'Critical' else 
                     'background-color: #fff4e5' if x == 'Warning' else 
                     'background-color: #e8f5e9',
            subset=['Status']
        ),
        use_container_width=True,
        height=600
    )

elif selected_tab == "SmartMineAI Assistant":
    st.header("SmartMineAI Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm your SmartMining AI Assistant. Ask me about equipment status, maintenance predictions, or mining operations."
        })

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("SmartAI is Thinking..."):
                # Get fresh equipment data
                current_df = get_equipment_data()
                current_df['Status'] = current_df.apply(assign_status, axis=1)
                
                # Generate response with equipment context
                response = smart_mining_chat(prompt, current_df)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Add clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat history cleared. How can I help you?"}
        ]
        st.rerun()