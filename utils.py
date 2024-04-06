import datetime

import pandas as pd
import requests
from unidecode import unidecode

url = "https://halic.edu.tr/tr/s-duyurular/Documents/2023/11/14/2023-2024-guz-donemi-vize-sinavi-all-list.xlsx"
midterm_xls = requests.get(url)

df = pd.read_excel(midterm_xls.content)

df["DERS KODU"] = df["DERS KODU"].apply(lambda x: x.split(";")[0])
df["DERS ADI"] = df["DERS ADI"].apply(lambda x: x.split(";")[0])
df["DERSLİK KODLARI"] = df["DERSLİK KODLARI"].apply(lambda x: str(x))
df["DERSLİK KODLARI"] = df["DERSLİK KODLARI"].apply(lambda x: x.replace(";", ","))
df["DERS KODU"] = df["DERS KODU"].apply(lambda y: unidecode(y).lower())

df = df[
    ["SINAV GÜNÜ", "SINAV BAŞLANGIÇ SAATİ", "DERS KODU", "DERS ADI", "DERSLİK KODLARI"]
]

df = (
    df.groupby("DERS KODU")
    .agg(
        {
            "SINAV GÜNÜ": "first",
            "SINAV BAŞLANGIÇ SAATİ": "first",
            "DERS ADI": "first",
            "DERSLİK KODLARI": ", ".join,
        }
    )
    .reset_index()
)

df = df[
    ["SINAV GÜNÜ", "SINAV BAŞLANGIÇ SAATİ", "DERS KODU", "DERS ADI", "DERSLİK KODLARI"]
].sort_values(by="SINAV GÜNÜ")

course_list = []


def tr_getExamDate(course_code):
    course_code = unidecode(course_code).lower()

    date = df[df["DERS KODU"] == course_code]["SINAV GÜNÜ"].values[0]
    week_day = date.split(" ")[1]
    date_full = datetime.datetime.strptime(date.split(" ")[0], "%Y-%m-%d").strftime(
        "%d/%m/%Y"
    )
    date = date_full + " " + week_day
    time = df[df["DERS KODU"] == course_code]["SINAV BAŞLANGIÇ SAATİ"].values[0]
    return date + " " + time


def en_getExamDate(course_code):
    course_code = unidecode(course_code).lower()

    date = df[df["DERS KODU"] == course_code]["SINAV GÜNÜ"].values[0]
    date_en = datetime.datetime.strptime(date.split(" ")[0], "%Y-%m-%d").strftime(
        "%d/%m/%Y %A"
    )
    date = date_en

    time = df[df["DERS KODU"] == course_code]["SINAV BAŞLANGIÇ SAATİ"].values[0]
    return date + " " + time


def getCourseName(course_code):
    course_code = unidecode(course_code).lower()
    name = df[df["DERS KODU"] == course_code]["DERS ADI"].values[0]
    return name


def getClassroom(course_code):
    course_code = unidecode(course_code).lower()
    classroom = df[df["DERS KODU"] == course_code]["DERSLİK KODLARI"].values[0]
    classroom = classroom.split(",")[:5]
    classroom = ",".join(str(element) for element in classroom)
    return classroom


def en_createResultDf(course_list):
    result_df_en = pd.DataFrame(
        [],
        columns=["Course Name", "Exam Date", "Classroom Codes"],
    )
    for course in course_list:
        list_row = [getCourseName(course), en_getExamDate(course), getClassroom(course)]
        result_df_en.loc[len(result_df_en)] = list_row
    result_df_en = result_df_en.sort_values("Exam Date")
    return result_df_en


def tr_createResultDf(course_list):
    result_df_tr = pd.DataFrame(
        [],
        columns=["Ders Adı", "Sınav Tarihi", "Sınıf"],
    )
    for course in course_list:
        list_row = [getCourseName(course), tr_getExamDate(course), getClassroom(course)]
        result_df_tr.loc[len(result_df_tr)] = list_row
    result_df_tr = result_df_tr.sort_values("Sınav Tarihi")
    return result_df_tr
