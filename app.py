import streamlit as st

from utils import createImage, df, en_createResultDf, tr_createResultDf

st.title("Exam Genius📚")

language_on = st.toggle("🇺🇸 EN", key="language_toggle", value=False)

if language_on:
    st.write("### 2024 Spring Semester Midterm Exam Dates")
    st.write("Below are the midterm exam dates for the 2024 Spring semester.")
    st.write(
        "Please select the course codes of the courses for which you want to see the exam dates."
    )
    course_list = st.multiselect(
        "Select Courses",
        df["DERS KODU"].str.upper() + " (" + df["DERS ADI"] + ")",
        placeholder="Course Code or Name",
    )
    col1, col2 = st.columns(2)
    if len(course_list) > 0 and col1.button("Show Exam Dates"):
        result_df = en_createResultDf(course_list)
        st.dataframe(result_df, hide_index=True)
        createImage(result_df)
        with open("output/examgenius.png", "rb") as file:
            col2.download_button(
                "Download as Image",
                data=file,
                file_name="examgenius.png",
                mime="image/png",
            )

else:
    st.write("### 2024 Bahar Dönemi Ara Sınav Tarihleri")
    st.write("Aşağıda 2024 Bahar dönemi için ara sınav tarihleri yer almaktadır.")
    st.write("Lütfen sınav tarihlerini görmek istediğiniz ders kodlarını seçin.")
    course_list = st.multiselect(
        "Dersleri Seçin",
        df["DERS KODU"].str.upper() + " (" + df["DERS ADI"] + ")",
        placeholder="Ders Kodu veya Adı",
    )
    col1, col2 = st.columns(2)
    if len(course_list) > 0 and col1.button("Sınav Tarihlerini Göster"):
        result_df = tr_createResultDf(course_list)
        st.dataframe(result_df, hide_index=True)
        createImage(result_df)
        with open("output/examgenius.png", "rb") as file:
            col2.download_button(
                "Resim Olarak İndir",
                data=file,
                file_name="examgenius.png",
                mime="image/png",
            )
