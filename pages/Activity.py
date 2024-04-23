import calendar
from datetime import datetime
import streamlit as st 
from streamlit_option_menu import option_menu
import mysql.connector

#import pandas as pd
#from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base

db_config = {
    'host': 'srv1118.hstgr.io',
    'user': 'u829120591_bV3z1',
    'password': 'u829120591_bV3z1U',
    'database': 'u829120591_4XuUf',
}

conn = mysql.connector.connect(**db_config)
mycursor = conn.cursor(dictionary=True)
		
page_title = "Activity reports entry for ECO SDG ACTIVITIES"
page_icon = ":money_with_wings:"
layout = "centered"

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_title + " ") 

college_id = st.session_state.college_id
st.write(f"college id - {college_id}")
st.session_state

aclist = []
ac_det = {
    'activity_id': ' ',
    'from_date': ' ',
    'to_date': ' ',
    'outcomes' : ' ',
    'planning' : ' ',
    'mat_avail' : ' ',
    'mat_collec' : ' ',
    'role' : ' ',
    'aware' : ' ',
    'np_cov' : ' ',
    'collab' : ' ',
    'checklist' : ' ',
    'location' : ' ',
    'steps' : ' ',
    'precautions' : ' ',
    'tools_support' : ' ',
    'learnings' : ' ',
    'village_support' : ' ',
    'final_learnings' : ' ',
    'feedback' : ' ',
    'self_eval' : ' ',
    'notes' : ' '
}

def activity_table(): 
     acsql = "select activity_name from activity_table"
     #dataframe = pd.read_sql_query(acsql, engine)
     #for column, values in dataframe.items():
      # if (column == "activity_name"):
       #  for value in values:
          #st.write(f"Activity list: {value}")
        #   aclist.append(value)
     mycursor.execute(acsql)
     results = mycursor.fetchall()
     if results is not None:
         for res in results:
             acname = res["activity_name"]
             aclist.append(acname)
   

def activity_details(iter):
  
  ac_det["from_date"] = st.date_input("From Date:", key=f"from_date {iter}")
  ac_det["to_date"] = st.date_input("To Date:", key=f"to_date {iter}")
  ac_det["outcomes"] = st.text_input("Outcomes", key=f"Outcomes {iter}")
  ac_det["planning"] = st.text_input("Planning", key=f"Planning {iter}")
  ac_det["mat_avail"] = st.text_input("Material availability", key=f"mat_avail {iter}")
  ac_det["mat_collec"] = st.text_input("Material Collection", key=f"mat_collec {iter}")
  ac_det["role"] = st.text_input("List of the material and role of the material", key=f"role {iter}")
  ac_det["aware"] = st.radio("Were you aware of this activity earlier?", ('Yes','No'), key=f"aware {iter}")
  ac_det["collab"] = st.text_input("Did you collaborate with other organizations to create a bigger one? ", key=f"collab {iter}")
  ac_det["checklist"] = st.text_input("Has the organizing team prepared and follow a checklist for conducting the activity?", key=f"checklist {iter}")
  ac_det["location"] = st.text_input("Where did you conduct this program?", key=f"location {iter}")
  ac_det["steps"] = st.text_input("What are the steps involved in conducting the activity work? / Mention step by step procedure followed? Write in bullet points.", key=f"steps {iter}")
  ac_det["precautions"] = st.text_input("What are the precautions taken for conducting the activity? ", key=f"precaution {iter}")
  ac_det["tools_support"] = st.text_input("What were the tools/support systems used for conducting the activity ", key=f"tools_support {iter}")
  ac_det["learnings"] = st.text_input("What was your learning at various steps of implementation of the activity?", key=f"learnings {iter}")
  ac_det["village_support"] = st.text_input("How was the support from the students/neighborhood/ village/school", key=f"village_support {iter}")
  ac_det["final_learnings"] = st.text_input("What have you learned from this process while working for the District Eco-SDGs Championship 2024? ", key=f"final_learnings {iter}")
  ac_det["feedback"] = st.text_input("Did you collect the feedback from the participants of the activity ?", key=f"feedback {iter}")
  ac_det["self_evaluation"] = st.text_input("What is your self evaluation for this effort ?", key=f"self_eval {iter}")
  ac_det["notes"] = st.text_input("Any notes/comments ?", key=f"notes {iter}")

def main(): 
    with st.expander("Activities"):
        activity_table()
        #st.write(f"List of activities : {aclist}")
        num_activities = st.number_input("Number of activities" , min_value=1, max_value=100, value=1)
        for k in range(1, num_activities+1):
           option = st.selectbox(f"Which activity do you like to report " , aclist, key=f"activity {k}")
           if option: 
              st.write(f"You selected : {option}" )
              #with st.expander("Activity Details"):
              activity_details(k)
   
    submitted = st.button("Submit")
    
    if submitted: 
     #college_sql = "insert into college_info (college_name, district, state, website, head_name, fb_link, yt_link, total_participants, total_strength, dignitaries, date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
     #values = (college_name, district, state, website, head_name, fb_link, yt_link, int(total_participants), int(total_strength), dignitaries, date)
     #st.write(f"Sql {college_sql}")
     st.write(f"Submitted ")

     
     #if id is not None: 
      # college_id = id['last_insert_id()']
       #st.write(f"My id is {college_id}")
       #Tuple is of this form -  {'last_insert_id()': 28}
       

     mycursor.close()
     conn.close()
    #engine.dispose()

if __name__ == "__main__":
    main()

