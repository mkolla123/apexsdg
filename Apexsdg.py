import calendar
from datetime import datetime
import streamlit as st 
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
#from sqlalchemy import create_engine

db_config = {
    'host': 'srv1118.hstgr.io',
    'user': 'u829120591_bV3z1',
    'password': 'u829120591_bV3z1U',
    'database': 'u829120591_4XuUf',
}

conn = mysql.connector.connect(**db_config)
mycursor = conn.cursor(dictionary=True)
		
page_title = "Reports for ECO SDG ACTIVITIES"
page_icon = ":money_with_wings:"
layout = "centered"

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_title + " ") 

clubs = {}
nat_day = {}
aclist = []
global college_id

def general_info(): 
  
  global college_name, district, state, website, head_name, fb_link, yt_link, dignitaries, total_participants, total_strength, date
  college_name = st.text_input("College Name")
  district = st.text_input("District")
  state = st.text_input("State")
  website = st.text_input("Website")
  head_name = st.text_input("Name of the head of the institution")
  fb_link = st.text_input("facebook link")
  yt_link = st.text_input("youtube link")
  dignitaries = st.text_input("dignitaries")
  total_participants = st.number_input("Total participants")
  #global total_activities = st.number_input("Total activities")
  total_strength = st.number_input("Total strength")
  date = st.date_input("Date:", key = "date1")


def national_international_day():
  #nat_intl_day, intl_date
  num_natldays = st.number_input("Number of National/Intl days" , min_value=1, max_value=100, value=1, key="natday")
  for i in range(1, num_natldays + 1):
      nat_intl_day = st.text_input("National or International Day celebrated", key=f"{i}")
      intl_date = st.date_input("Date:", key=f"date{i+1}")
      nat_day[nat_intl_day] = intl_date
      #st_names.append(student_name)


def faculty_names():
  global faculty_names
  faculty_names = st.text_input("Faculty names, comma separated")
  
# Function to add a new self-help club
def add_club(club_name):
    if club_name not in clubs:
        clubs[club_name] = []  # Initialize with an empty list
        #print(f"Club '{club_name}' added.")
    else:
        print(f"Club '{club_name}' already exists.")

# Function to add a new student to a specific club
def add_student(club_name, student_name):
    if club_name in clubs:
        clubs[club_name].append(student_name)  # Add student to the existing list
        #print(f"Student '{student_name}' added to club '{club_name}'.")
    else:
        print(f"Club '{club_name}' does not exist.")
        
def student_names(shclubname, j):
    num_students = st.number_input("Number of students" , min_value=1, max_value=50, value=1, key=f"shclubname {shclubname}{j}")
    for i in range(1, num_students + 1):
      student_name = st.text_input(f"Student Name {i}", key = f"stname {shclubname}{i}{j}")
      #st_names.append(student_name)
      add_student(shclubname, student_name)
    
def shclubnames(): 
   num_shclubs = st.number_input("Number of self help clubs" , min_value=1, max_value=50, value=1)
   for j in range(1, num_shclubs+1):
     shclubname = st.text_input(f"Self help club name {j}" , key = f"shclub {j}")
     #sh_club_name.append(shclubname)
     add_club(shclubname)
     student_names(shclubname, j)


def main(): 
  #with st.form("data_entry", clear_on_submit=True):
    with st.expander("General Information"):
      general_info()

    with st.expander("National or International days celebrated"): 
      national_international_day()

    with st.expander("Faculty Coordinators names"): 
      faculty_names()

    with st.expander("Students in self help club names"): 
      shclubnames()

    
    submitted = st.button("Submit")
    
    if submitted: 
     college_sql = "insert into college_info (college_name, district, state, website, head_name, fb_link, yt_link, \
      total_participants, total_strength, dignitaries, date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
     values = (college_name, district, state, website, head_name, fb_link, yt_link, int(total_participants), int(total_strength), dignitaries, date)
     #st.write(f"Sql {college_sql}")
     #st.write(f"Sql {values}")

     mycursor.execute(college_sql, values)
     
     conn.commit()
     #select the id of the last inserted row, works beautifully for the session. 
     mycursor.execute("select last_insert_id()")
     id = mycursor.fetchone()
     
     if id is not None: 
       college_id = id['last_insert_id()']
       #st.write(f"My id is {college_id}")
       #Tuple is of this form -  {'last_insert_id()': 28}
     
     #Insert into national_international_day
     for key in nat_day: 
        natdayname = key
        natdaydate = nat_day[key]
        nat_sql = "insert into national_international_days (college_id, national_international_day, date) values (%s, %s, %s);"
        nvalues = (college_id, natdayname, natdaydate)
        mycursor.execute(nat_sql, nvalues)
        #st.write(f"My nat sql - {nat_sql} ")
        #st.write(f"My nat values - {college_id} , {natdayname} , {natdaydate} ")
        conn.commit()

     #Insert into students info
     for club, students in clubs.items():
      # shname, stnamel = row
       #print(f"{club}: {', '.join(students)}")
       #for item in stnamel:
        stnames1 = ",".join(students)
        print(f"Students = {stnames1}")
       
     mycursor.close()
     conn.close()
     #st.balloons()
     #st.success(f"College id - {college_id}")
     st.session_state.college_id = college_id
     st.switch_page("pages/Activity.py")
     
if __name__ == "__main__":
    main()

