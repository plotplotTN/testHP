import datetime
import pandas as pd
import streamlit as st

# Defining the different accomplishment categories and their associated points
CATEGORY_POINTS = {
    "Certification Obtention": 50,
    "Sport Performance": 30,
    "Corporate Event Presence": 20,
    "Cooptation Acquisition": 10
}

# Initializing the dataframe that will be used to store the events and the achievements
df_events = pd.DataFrame(columns=["Event Name", "Event Description", "Category", "Points"])


# Creating a function to add events to the dataframe
def add_event(name, description, category):
    global df_events
    name = name.strip()
    description = description.strip()

    if not name:
        st.warning("Please enter a valid 'Event Name'.")
        return False
    elif len(description) < 1:
        st.warning("Please enter the 'Event Description'.")
        return False
    elif category not in CATEGORY_POINTS:
        st.warning("Please select a valid 'Category' from the drop menu.")
        return False
    elif any(df_events["Event Name"] == name):
        st.warning("An event with this name already exists. Please choose a different name.")
        return False
    else:
        points = CATEGORY_POINTS.get(category)
        df_events = df_events.concat({"Event Name": name,
                                      "Event Description": description,
                                      "Category": category,
                                      "Points": points}, ignore_index=True)
        #df_events = df_events.append({"Event Name": name,"Event Description": description,"Category": category,"Points": points}, ignore_index=True)
        st.success(f"Event '{name}' added successfully.")
        return True


# Creating a function to delete an event based on its name
def delete_event(name):
    global df_events
    name = name.strip()
    if not any(df_events["Event Name"] == name):
        st.warning("There is no event with this name.")
        return False
    else:
        df_events = df_events[df_events["Event Name"] != name]
        st.success(f"Event '{name}' removed successfully.")
        return True


# Creating a function to display the events in a specific category
def display_events_in_category(category):
    events = df_events[df_events["Category"] == category]
    if len(events) > 0:
        st.write(f"## {category}")
        for i, event in events.iterrows():
            st.write(f"{event['Event Name']} - {event['Event Description']} ({event['Points']} points)")
    else:
        st.warning(f"No events in the '{category}' category yet.")


# Creating a function to display the dashboard for a specific user
def display_dashboard(username):
    global df_events
    st.title(f"Welcome to the Gamification Platform - {username}")
    st.write("## Available Achievements")
    for category, points in CATEGORY_POINTS.items():
        display_events_in_category(category)
    st.write("## Latest Achievements")
    if len(df_events) > 0:
        st.write(df_events.sort_values(by='Points', ascending=False).head(5).reset_index(drop=True)
                 .style.set_properties(**{'background-color': 'lightgray'}, subset=['Event Name','Event Description','Category','Points']))
        st.write("## Points")
        st.write("### Total Points Earned: ",df_events['Points'].sum())
        st.write("### Points breakdown by Category: ")
        for category, points in CATEGORY_POINTS.items():
            points_sum = df_events[df_events['Category']==category]['Points'].sum()
            st.write(f"{category}: {points_sum} points")
        if len(df_events) >= 3:
            st.write("## Congratulations!")
            st.write("You achieved at least three events, so you can earn an additional point.")
            event_list = list(df_events['Event Name'])
            selected_event = st.selectbox('Select an event:', event_list)
            submitted = st.button("Submit")
            if submitted:
                event = df_events[df_events["Event Name"] == selected_event].iloc[0]
                df_events.loc[df_events["Event Name"] == selected_event, "Points"] = event["Points"] + 1
                st.success(f"Congratulations! You have earned 1 point for {event['Event Name']}.")
                display_dashboard(username)
        else:
            st.warning("You need to achieve a minimum of 3 events to access this section.")
    else:
        st.warning("No achievements yet.")
    st.write("## Other Employees' Achievements")
    # TODO: display information about other employees' achievements (best performer, top 10, ...)


# Creating some sample events
add_event("Certification Obtention", "Get Certification A", "Certification Obtention")
add_event("Sport Performance", "Participate in Sport Event 1", "Sport Performance")
add_event("Corporate Event Presence", "Attend Corporate Event 1", "Corporate Event Presence")
add_event("Cooptation Acquisition", "Acquire a new cooptation", "Cooptation Acquisition")

# Creating the interface for the administrator
if st.sidebar.checkbox("Are you an administrator?"):

    st.sidebar.write("## Manage Events")
    event_name = st.sidebar.text_input("Event Name")
    event_description = st.sidebar.text_input("Event Description")
    category = st.sidebar.selectbox("Category", list(CATEGORY_POINTS.keys()))

    if st.sidebar.button("Add Event"):
        if add_event(event_name, event_description, category):
            event_name, event_description = "", ""

    elif st.sidebar.button("Delete Event"):
        delete_event(event_name)
        event_name, event_description = "", ""

# Creating the interface for the employees

else:
    USERNAME = st.text_input("Username")

    if st.button("Connect"):
        USERNAME = USERNAME.strip()
        if not USERNAME:
            st.warning("Please enter the 'Username'.")
        elif len(df_events) == 0:
            st.warning("No achievements yet. Please ask the administrator to add some.")
        else:
            display_dashboard(USERNAME)

# Comment:

# I replaced the CATEGORIES dictionary with CATEGORY_POINTS dictionary to improve readability of the code
# Created a new function "display_events_in_category" to remove the for loop that was causing the code to be repeated.
# Created a new variables "event_name" and "event_description" and initialized them to empty string to clear input fields after new event addition
# Changed the add_event function to return True on successful addition of event, or False otherwise, to clearly communicate the success status.
# I changed "len(USERNAME) < 1" to "not USERNAME" to decrease the number of instructions and improve readability.
# Added an 'elif' condition to check if number of events is more than zero when a user tries to connect to the platform.
# Moved the interface creation code block for the employee interface to the initial else block to reduce code duplication.
# improved the code structure, remove extra white spaces to the code to make it easier to read.
# Added input field clearing after deleting an event using the delete_event() function