import streamlit as st
import pandas as pd
from datetime import datetime

# Load or create student data
def load_student_data():
    try:
        students_df = pd.read_excel('student_data.xlsx')
    except FileNotFoundError:
        students_df = pd.DataFrame({'Roll No': range(1, 51), 'Name': [''] * 50})
        students_df.to_excel('student_data.xlsx', index=False)
    return students_df

def add_names_to_class_1(names_list):
    students_df = load_student_data()
    for i, name in enumerate(names_list):
        if i < len(students_df):
            students_df.at[i, 'Name'] = name
        else:
            students_df = students_df.append({'Roll No': len(students_df) + 1, 'Name': name}, ignore_index=True)
    
    students_df.to_excel('student_data.xlsx', index=False)

# Load or create attendance data
def load_attendance_data():
    try:
        attendance_data = pd.read_excel('attendance.xlsx', index_col=0)
    except FileNotFoundError:
        attendance_data = pd.DataFrame(columns=['Date'] + [str(i) for i in range(1, 51)])
        attendance_data.to_excel('attendance.xlsx', index=True)
    return attendance_data

# Save data
def save_data(df, filename):
    df.to_excel(filename)

# Main function
def main():
    st.title('Class Attendance Tracker')

    # Authentication
    username = st.sidebar.text_input('Username')
    password = st.sidebar.text_input('Password', type='password')
    if username == 'teacher' and password == 'pass123':
        st.sidebar.success('Logged In')
    else:
        st.sidebar.error('Invalid Credentials')
        st.stop()

    # Load or create data
    global students_df
    global attendance_data
    students_df = load_student_data()
    attendance_data = load_attendance_data()

    # Sidebar - Add names to Class 1
    st.sidebar.header('Add Names to Class 1')
    names_list = []
    for i in range(50):
        name = st.sidebar.text_input(f'Enter Name for Roll No {i+1}:')
        names_list.append(name)

    if st.sidebar.button('Add Names'):
        add_names_to_class_1(names_list)
        st.sidebar.success('Names Added Successfully!')

    # Class and Date Selection
    selected_class = st.sidebar.selectbox('Select Class', ['Class A', 'Class B', 'Class C'])
    selected_date = st.sidebar.date_input('Select Date', datetime.today())

    # Mark Attendance
    st.write('### Mark Attendance')
    for i, row in students_df.iterrows():
        attendance_data.loc[selected_date.strftime('%Y-%m-%d'), f'{row["Roll No"]}'] = st.checkbox(f'{row["Name"]} (ID: {row["Roll No"]})')

    # Display Attendance Table
    st.write('### Attendance Table')
    st.write(attendance_data)

    # Export Attendance Data
    if st.button('Export Attendance Data'):
        st.write('Exporting data...')
        attendance_data.to_excel(f'{selected_class}_attendance_{selected_date.strftime("%Y-%m-%d")}.xlsx', index=True)
        st.success('Data Exported Successfully')

if __name__ == '__main__':
    main()
