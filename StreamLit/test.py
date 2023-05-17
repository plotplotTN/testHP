import datetime
import pandas as pd
import streamlit as st

# define the different accomplishment categories and their associated points
categories = {
    "Certification Obtention": 50,
    "Sport Performance": 30,
    "Corporate Event Presence": 20,
    "Cooptation Acquisition": 10
}

# initialize the dataframe that will be used to store the events and the achievements
df_events = pd.DataFrame(columns=["Event Name", "Event Description", "Category", "Points"])

# create a function to add events to the dataframe
def add_event(name, description, category, points):
    global df_events
    df_events = df_events.append({"Event Name": name,
                                  "Event Description": description,
                                  "Category": category,
                                  "Points": points}, ignore_index=True)

# create a function to delete an event based on its name
def delete_event(name):
    global df_events
    df_events = df_events[df_events["Event Name"] != name]

# create a function to display the events in a specific category
def display_events_in_category(category):
    events = df_events[df_events["Category"] == category]
    if len(events) > 0:
        st.write(f"## {category}")
        for i, event in events.iterrows():
            st.write(f"{event['Event Name']} - {event['Event Description']} ({event['Points']} points)")
    else:
        st.write(f"No events in the {category} category yet.")

# create a function to display the dashboard for a specific user
def display_dashboard(username):
    global df_events
    st.title(f"Welcome to the Gamification Platform - {username}")
    st.write("## Available Achievements")
    for category, points in categories.items():
        display_events_in_category(category)
    st.write("## Latest Achievements")
    # TO DO: display the user's latest achievements
    st.write("## Points")
    # TO DO: display the user's points for different timeframes (last month, last year,...)
    st.write("## Other Employees' Achievements")
    # TO DO: display information about other employees' achievements (best performer, top 10, ...)

# create some sample events
add_event("Certification A", "Get Certification A", "Certification Obtention", 50)
add_event("Sport Event 1", "Participate in Sport Event 1", "Sport Performance", 30)
add_event("Corporate Event 1", "Attend Corporate Event 1", "Corporate Event Presence", 20)
add_event("Cooptation 1", "Acquire a new cooptation", "Cooptation Acquisition", 10)

# create the interface for the administrators
if st.sidebar.checkbox("Are you an administrator?"):
    st.sidebar.write("## Manage Events")
    event_name = st.sidebar.text_input("Event Name")
    event_description = st.sidebar.text_input("Event Description")
    category = st.sidebar.selectbox("Category", list(categories.keys()))
    points = categories[category]
    if st.sidebar.button("Add Event"):
        add_event(event_name, event_description, category, points)
        st.sidebar.success(f"Event {event_name} added successfully.")
    elif st.sidebar.button("Delete Event"):
        delete_event(event_name)
        st.sidebar.success(f"Event {event_name} deleted successfully.")

# create the interface for the employees
else:
    USERNAME = st.text_input("Username")
    if st.button("Connect"):
        display_dashboard(USERNAME)
        # TO DO: create a way for the user to achieve events and earn points