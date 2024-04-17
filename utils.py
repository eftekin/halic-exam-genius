import datetime

import pandas as pd
import plotly.figure_factory as ff
from unidecode import unidecode

# import requests
# url = "https://halic.edu.tr/tr/s-duyurular/Documents/2024/01/02/2023-2024-guz-donemi-final-sinav-programi-all-list.xlsx"
# midterm_xls = requests.get(url)

# df = pd.read_excel(midterm_xls.content)

df = pd.read_excel("2024_spring_midterm_all_list.xlsx")

exam_date_column = "SINAV GÜNÜ"
exam_time_column = "BAŞLANGIÇ SAATİ"

# ADD ENDING TIME
exam_time_end_column = "BİTİŞ SAATİ"
# FACULTY NAME MIGHT BE ADDED LATER, IT IS NOT NECESSARY FOR NOW.

# ADD PROGRAM NAME
program_name = "PROGRAM ADI"
# ADD BRANCHES, THERE EXISTS A CLASSROOM (DERSLİK KODLARI) FOR EACH BRANCH; DISPLAY EACH BRANCH ACCORDING TO THEIR OWN CLASSROOM (DERSLİK KODLARI)
branch = "ŞUBE"
# ADD DOCTOR/TEACHER NAME
teacher_name = "ÖĞRETİM ELEMANI ADI"

course_code_column = "DERS KODU"
course_name_column = "DERS ADI"
course_code_and_name_column = "DERS KODU VE ADI"
classroom_code_column = "DERSLİK KODLARI"


df[course_code_column] = df[course_code_column].apply(lambda x: x.split(";")[0])
df[course_name_column] = df[course_name_column].apply(lambda x: x.split(";")[0])

df[program_name] = df[program_name].apply(lambda x: x.replace(";", ","))
df[branch] = df[branch].apply(lambda x: str(x))
df[branch] = df[branch].apply(lambda x: x.replace(";", ","))
df[teacher_name] = df[teacher_name].apply(lambda x: x.replace(";", ","))

df[classroom_code_column] = df[classroom_code_column].apply(lambda x: str(x))
df[classroom_code_column] = df[classroom_code_column].apply(lambda x: x.replace(";", ","))
df[course_code_column] = df[course_code_column].apply(lambda y: unidecode(y).lower())

df = df[
    [
        exam_date_column,
        exam_time_column,
        exam_time_end_column,
        program_name,
        branch,
        teacher_name,
        course_code_column,
        course_name_column,
        classroom_code_column,
    ]
]

df = (
    df.groupby(course_code_column)
    .agg(
        {
            exam_date_column: "first",
            exam_time_column: "first",
            exam_time_end_column: "first",
            program_name: "first",
            branch: " - ".join,
            teacher_name: "- ".join,
            course_name_column: "first",
            classroom_code_column: "- ".join,
        }
    )
    .reset_index()
)

df = df[
    [
        exam_date_column,
        exam_time_column,
        exam_time_end_column,
        program_name,
        branch,
        teacher_name,
        course_code_column,
        course_name_column,
        classroom_code_column,
    ]
].sort_values(by=exam_date_column)

df[course_code_and_name_column] = (
    df[course_code_column].str.upper() + " (" + df[course_name_column] + ")"
)

course_list = []


def tr_getExamDate(course_code):
    date = df[df[course_code_and_name_column] == course_code][exam_date_column].values[0]
    week_day = date.split(" ")[1]
    date_full = datetime.datetime.strptime(date.split(" ")[0], "%Y-%m-%d").strftime(
        "%d/%m/%Y"
    )
    date = date_full + " " + week_day
    time = df[df[course_code_and_name_column] == course_code][exam_time_column].values[0]
    time2 = df[df[course_code_and_name_column] == course_code][exam_time_end_column].values[0]
    return str(date) + " " + str(time) + "-" + str(time2)


def en_getExamDate(course_code):
    date = df[df[course_code_and_name_column] == course_code][exam_date_column].values[0]
    date_en = datetime.datetime.strptime(date.split(" ")[0], "%Y-%m-%d").strftime(
        "%d/%m/%Y %A"
    )
    date = date_en
    time = df[df[course_code_and_name_column] == course_code][exam_time_column].values[0]
    time2 = df[df[course_code_and_name_column] == course_code][exam_time_end_column].values[0]
    return date + " " + time + "-" + time2


def getCourseName(course_code):
    name = df[df[course_code_and_name_column] == course_code][course_name_column].values[0]
    return name


def getClassroom(course_code):
    classroom = df[df[course_code_and_name_column] == course_code][classroom_code_column].values[0]
    if len(classroom.split(",")) > 5:
        classroom = classroom.split(",")[:5]
        classroom = ",".join(str(element) for element in classroom) + "..."
    return classroom

def getProgramName(course_code):
    programName = df[df[course_code_and_name_column] == course_code][program_name].values[0] # loop ile liste ekle
    return programName

def getBranchName(course_code):
    branchName = df[df[course_code_and_name_column] == course_code][branch].values[0]
    lst = []
    i = 0
    while i < len(branchName):
        if branchName[i].isdigit():
            num = ''
            while i < len(branchName) and (branchName[i].isdigit() or branchName[i] == '-'):
                num += branchName[i]
                i += 1
            lst.append(int(num))
        elif branchName[i] == "-":
            lst.append("-")
            i += 1
        else:
            i += 1
    res = []
    for x in lst:
        if x not in res and x != "-":
            res.append(x)
            res.append(",")
        elif x == "-":
            res.pop()
            res.append(" - ")
    res.pop()
    return ''.join(map(str, res))

def getTeacherName(course_code):
    teacherName = df[df[course_code_and_name_column] == course_code][teacher_name].values[0]
    # Repeating teacher names should be removed like in getBranchName()
    return teacherName

def en_createResultDf(course_list):
    result_df_en = pd.DataFrame(
        [],
        columns=["Course Name", "Exam Date", "Classroom Codes", "Branch", "Program", "Teacher"],
    )
    for course in course_list:
        list_row = [getCourseName(course), en_getExamDate(course), getClassroom(course), getBranchName(course), getProgramName(course), getTeacherName(course)]
        result_df_en.loc[len(result_df_en)] = list_row
    result_df_en = result_df_en.sort_values("Exam Date")
    return result_df_en


def tr_createResultDf(course_list):
    result_df_tr = pd.DataFrame(
        [],
        columns=["Ders Adı", "Sınav Tarihi", "Sınıf", "Şube", "Bölüm", "Öğretim Elemanı"],
    )
    for course in course_list:
        list_row = [getCourseName(course), tr_getExamDate(course), getClassroom(course), getBranchName(course), getProgramName(course), getTeacherName(course)]
        result_df_tr.loc[len(result_df_tr)] = list_row
    result_df_tr = result_df_tr.sort_values("Sınav Tarihi")
    return result_df_tr


def createImage(df):
    course_list = list(df.iloc[:, 0])
    scale = 21
    # The width of the table will be extended
    width = max([len(course_name) * scale for course_name in course_list])
    fig = ff.create_table(df)
    if width > 800:
        fig.layout.width = width
    else:
        fig.layout.width = 800
    fig.update_layout(autosize=True)
    fig.write_image("output/examgenius.png", scale=2)
