import streamlit as st
import pandas as pd
import random
import datetime
import os

# Motivational Quotes
quotes = [
    "Mistakes are proof that you are trying.",
    "Every challenge is an opportunity to grow."
]

st.title("🍀 Growth Mindset")

# Display random motivation
st.subheader("Today's Motivation")
st.write(random.choice(quotes))

# User input for goal
st.subheader(":blue[Set Your Daily Goal]")
goal = st.text_input("Enter Your Today's Goal")

if st.button("Submit Goal"):
    st.write("Your Today's Goal:", goal)

# User input for learning progress
st.subheader("What did you learn today?")
study = st.text_area("Write what you have learned today")

if st.button("Submit Learning"):
    st.write(study)

# Save progress
today = datetime.date.today()

# Format selection using columns
csv_col, excel_col = st.columns(2)

save_format = None

if "progress.csv" not in os.listdir():
    with open("progress.csv", "w") as file:
        file.write("Date,Goal,Study\n")

if "progress.xlsx" not in os.listdir():
    df = pd.DataFrame(columns=["Date", "Goal", "Study"])
    df.to_excel("progress.xlsx", index=False)

with csv_col:
    if st.button("Save as CSV"):
        with open("progress.csv", "a") as file:
            file.write(f"{today},{goal},{study}\n")
        st.success("Progress saved in CSV!")
        with open("progress.csv", "r") as file:
            st.download_button("Download CSV", file, "progress.csv", "text/csv")

with excel_col:
    if st.button("Save as Excel"):
        data = {"Date": [today], "Goal": [goal], "Study": [study]}
        df = pd.DataFrame(data)

        existing_df = pd.read_excel("progress.xlsx")
        df = pd.concat([existing_df, df], ignore_index=True)
        df.to_excel("progress.xlsx", index=False)

        st.success("Progress saved in Excel!")
        with open("progress.xlsx", "rb") as file:
            st.download_button("Download Excel", file, "progress.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Display last 5 records
st.subheader("Your Last 5 Entries")

if os.path.exists("progress.csv"):
    try:
        df = pd.read_csv("progress.csv")
        if not df.empty:
            st.dataframe(df.tail(5))
        else:
            st.info("No progress recorded yet.")
    except Exception as e:
        st.error(f"Error reading CSV: {str(e)}")

if os.path.exists("progress.xlsx"):
    try:
        df = pd.read_excel("progress.xlsx")
        if not df.empty:
            st.dataframe(df.tail(5))
        else:
            st.info("No progress recorded yet.")
    except Exception as e:
        st.error(f"Error reading Excel: {str(e)}")
