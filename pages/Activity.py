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
    'host': '127.0.0.1',
    'user': 'test1',
    'password': 'test1',
    'database': 'apexsdg',
}

conn = mysql.connector.connect(**db_config)
mycursor = conn.cursor(dictionary=True)
		
page_title = "Activity reports for SDG ACTIVITIES"
page_icon = ":money_with_wings:"
layout = "centered"

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_title + " ") 

college_id = 0

#st.write(f"college id - {college_id}")
#below prints the data present in the current session, useful for debug.
#st.session_state

aclist = []
selected_aclist = []
sel_acdet = []

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
     global college_id
     if 'college_id' in st.session_state :
          college_id = st.session_state.college_id
     if college_id == 0:
          st.write("Please enter college details first on Apexsdg page")
     if college_id is not 0 : 
         with st.expander("Activities"):
             activity_table()
             #st.write(f"List of activities : {aclist}")
             num_activities = st.number_input("Number of activities" , min_value=1, max_value=100, value=1)
             k = 0
             while k != num_activities:
             #for k in range(0, num_activities+1):
                option = st.selectbox(f"Which activity do you like to report " , aclist, key=f"activity {k}")
                # option is the activity to be entered.
                if option: 
                   st.write(f"You selected : {option}" )
                   #with st.expander("Activity Details"):
                   activity_details(k)
                   #loop through the inputs given by user
                   # k, v in ac_det.items():
                   #    st.write("{k} = {v}")
                   #Capture the inputs from user, option is the activity name,
                   #ac_det is the activity detail in the dictionary format
                   selected_aclist.append(option.rstrip())
                   sel_acdet.append(ac_det)
                k += 1
                   
        
         submitted = st.button("Submit")
         
         if submitted: 
          k = 0
          while k != num_activities:
               acidsql = "select activity_number from activity_table where activity_name = %s"
               val = selected_aclist[k]
               #print(val)
               data_tuple = (val,)
               mycursor.execute(acidsql, data_tuple)
               acid = mycursor.fetchone()
               an = acid["activity_number"] ## Get activity number from acid tuple
               if an is not None:
                   #insert into activity detail table using this an which is activity_id
                    ac_detsql = """insert into activity_details (college_id, activity_id, from_date, to_date, outcomes, 
                    planning, material_availability, material_collection, list_and_role_material, aware, collaboration, 
                    location, checklist, steps, precautions, tools_support, learnings, village_support_new_ideas, 
                    final_learning, feedback, self_evaluation, notes) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                    item = sel_acdet[k]
                                  
                    datat = (college_id, an,item["from_date"],item["to_date"],item["outcomes"],item["planning"],item["mat_avail"], \
                             item["mat_collec"],item["role"],item["aware"],item["collab"],item["location"],item["checklist"], \
                             item["steps"],item["precautions"],item["tools_support"],item["learnings"],item["village_support"],\
                             item["final_learnings"],item["feedback"],item["self_evaluation"],item["notes"])
                    
                    mycursor.execute(ac_detsql, datat)
               k += 1
               #st.write(f"Submitted ")
               st.switch_page("pages/thanks.py")
            
          conn.commit()
          mycursor.close()
          conn.close()
    #engine.dispose()

if __name__ == "__main__":
    main()

