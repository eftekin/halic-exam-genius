# Import required libraries
import datetime

import pandas as pd
import plotly.figure_factory as ff
import requests
from unidecode import unidecode


def format_date(date_str):
    """
    Convert different date formats to a consistent 'dd/mm/yyyy' format.

    Args:
        date_str (str): Input date string in various formats

    Returns:
        str: Formatted date in 'dd/mm/yyyy' format
    """
    try:
        # First, try parsing date in 'yyyy-mm-dd' format
        date_obj = datetime.datetime.strptime(date_str.split(" ")[0], "%Y-%m-%d")
    except ValueError:
        try:
            # If first attempt fails, try 'dd.mm.yyyy' format
            date_obj = datetime.datetime.strptime(date_str.split(" ")[0], "%d.%m.%Y")
        except ValueError:
            # Return error message if no format matches
            return "Invalid date format"

    # Convert to desired 'dd/mm/yyyy' format
    formatted_date = date_obj.strftime("%d/%m/%Y")
    return formatted_date


def process_exam_data():
    """
    Retrieve and process exam data from Halic University's exam schedule Excel file.

    Returns:
        pd.DataFrame: Processed exam data DataFrame
    """
    # URL of the exam schedule Excel file
    url = "https://halic.edu.tr/tr/s-duyurular/Documents/2025/01/16/2024-2025-guz-donemi-butunleme-sinavi-tum-liste.xlsx"

    # Download Excel file
    midterm_xls = requests.get(url)

    # Define column names for clarity and ease of use
    exam_date_column = "SINAV GÜNÜ"
    exam_time_column = "BAŞLANGIÇ SAATİ"
    course_code_column = "DERS KODU"
    course_name_column = "DERS ADI"
    course_code_and_name_column = "DERS KODU VE ADI"
    classroom_code_column = "DERSLİK/ODA KODLARI"  # Add classroom column

    # Read Excel file into DataFrame
    df = pd.read_excel(midterm_xls.content)

    # Clean and process course data
    df[course_code_column] = df[course_code_column].apply(lambda x: x.split(";")[0])
    df[course_name_column] = df[course_name_column].apply(lambda x: x.split(";")[0])
    df[course_code_column] = df[course_code_column].apply(
        lambda y: unidecode(y).lower()
    )

    # Clean classroom data if it exists
    if classroom_code_column in df.columns:
        df[classroom_code_column] = df[classroom_code_column].apply(lambda x: str(x))
        df[classroom_code_column] = df[classroom_code_column].apply(
            lambda x: x.replace(";", ",")
        )

    # Select and group relevant columns
    columns_to_use = [
        exam_date_column,
        exam_time_column,
        course_code_column,
        course_name_column,
    ]
    if classroom_code_column in df.columns:
        columns_to_use.append(classroom_code_column)
    df = df[columns_to_use]

    # Group by course code, taking first occurrence of date, time, and name
    agg_dict = {
        exam_date_column: "first",
        exam_time_column: "first",
        course_name_column: "first",
    }
    if classroom_code_column in df.columns:
        agg_dict[classroom_code_column] = ", ".join

    df = df.groupby(course_code_column).agg(agg_dict).reset_index()

    # Sort by exam date
    df = df.sort_values(by=exam_date_column)

    # Create a combined course code and name column
    df[course_code_and_name_column] = (
        df[course_code_column].str.upper() + " (" + df[course_name_column] + ")"
    )

    return df


def parse_exam_time(time_value):
    """
    Parse exam time from various input formats.

    Args:
        time_value (str or datetime.time): Input time

    Returns:
        str: Formatted time string in 'HH:MM' format
    """
    if isinstance(time_value, str):
        try:
            # Try parsing with seconds
            time_obj = datetime.datetime.strptime(time_value, "%H:%M:%S").time()
        except ValueError:
            # Try parsing without seconds
            time_obj = datetime.datetime.strptime(time_value, "%H:%M").time()
    else:
        time_obj = time_value

    return time_obj.strftime("%H:%M")


def tr_getExamDate(df, course_code):
    """
    Retrieve exam date in Turkish format.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name

    Returns:
        str: Formatted exam date and time in Turkish
    """
    exam_date_column = "SINAV GÜNÜ"
    exam_time_column = "BAŞLANGIÇ SAATİ"
    course_code_and_name_column = "DERS KODU VE ADI"

    date = df[df[course_code_and_name_column] == course_code][exam_date_column].values[
        0
    ]
    week_day = date.split(" ")[1]

    date_full = format_date(date)
    formatted_date = f"{date_full} {week_day}"

    time = df[df[course_code_and_name_column] == course_code][exam_time_column].values[
        0
    ]
    time_str = parse_exam_time(time)

    return f"{formatted_date} {time_str}"


def en_getExamDate(df, course_code):
    """
    Retrieve exam date in English format.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name

    Returns:
        str: Formatted exam date and time in English
    """
    exam_date_column = "SINAV GÜNÜ"
    exam_time_column = "BAŞLANGIÇ SAATİ"
    course_code_and_name_column = "DERS KODU VE ADI"

    date = df[df[course_code_and_name_column] == course_code][exam_date_column].values[
        0
    ]
    date_formatted = format_date(date.split(" ")[0])

    # Get day name in English
    date_en = f"{date_formatted} {datetime.datetime.strptime(date_formatted, '%d/%m/%Y').strftime('%A')}"

    time = df[df[course_code_and_name_column] == course_code][exam_time_column].values[
        0
    ]
    time_str = parse_exam_time(time)

    return f"{date_en} {time_str}"


def getCourseName(df, course_code):
    """
    Retrieve course name for a given course code.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name

    Returns:
        str: Course name
    """
    course_code_and_name_column = "DERS KODU VE ADI"
    course_name_column = "DERS ADI"

    return df[df[course_code_and_name_column] == course_code][
        course_name_column
    ].values[0]


def create_result_dataframe(df, course_list, language="tr", include_classroom=False):
    """
    Create a result DataFrame with sorted exam dates.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_list (list): List of selected courses
        language (str): Language of the result ('tr' or 'en')
        include_classroom (bool): Whether to include classroom codes in the result

    Returns:
        pd.DataFrame: Sorted result DataFrame
    """
    if language == "tr":
        columns = ["Ders Adı", "Sınav Tarihi"]
        if include_classroom:
            columns.append("Sınıf")
        result_df = pd.DataFrame([], columns=columns)
        for course in course_list:
            list_row = [getCourseName(df, course), tr_getExamDate(df, course)]
            if include_classroom:
                list_row.append(getClassroom(df, course))
            result_df.loc[len(result_df)] = list_row
        column_name = "Sınav Tarihi"
    else:
        columns = ["Course Name", "Exam Date"]
        if include_classroom:
            columns.append("Classroom Codes")
        result_df = pd.DataFrame([], columns=columns)
        for course in course_list:
            list_row = [getCourseName(df, course), en_getExamDate(df, course)]
            if include_classroom:
                list_row.append(getClassroom(df, course))
            result_df.loc[len(result_df)] = list_row
        column_name = "Exam Date"

    # Sort by date and time
    def parse_date(date_str):
        date_parts = date_str.split()
        return datetime.datetime.strptime(
            f"{date_parts[0]} {date_parts[2]}", "%d/%m/%Y %H:%M"
        )

    result_df["Parsed Date"] = result_df[column_name].apply(parse_date)
    result_df = result_df.sort_values("Parsed Date").drop("Parsed Date", axis=1)

    return result_df


def getClassroom(df, course_code):
    """
    Retrieve classroom information for a given course code.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name

    Returns:
        str: Formatted classroom codes
    """
    course_code_and_name_column = "DERS KODU VE ADI"
    classroom_code_column = "DERSLİK/ODA KODLARI"

    if classroom_code_column not in df.columns:
        return "N/A"

    classroom = df[df[course_code_and_name_column] == course_code][
        classroom_code_column
    ].values[0]
    if len(str(classroom).split(",")) > 5:
        classroom = str(classroom).split(",")[:5]
        classroom = ",".join(str(element) for element in classroom) + "..."
    return classroom


def createImage(df):
    """
    Create an image of the result DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame
    """
    course_list = list(df.iloc[:, 0])
    scale = 21
    width = max([len(course_name) * scale for course_name in course_list])

    fig = ff.create_table(df)
    fig.layout.width = width if width > 800 else 800
    fig.update_layout(autosize=True)

    fig.write_image("output/examgenius.png", scale=2)


# Main data processing
df = process_exam_data()
