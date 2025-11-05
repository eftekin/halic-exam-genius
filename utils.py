# Import required libraries
import datetime
import io

import pandas as pd
import plotly.figure_factory as ff
import requests
import urllib3
from unidecode import unidecode

# Disable SSL warnings when verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Column name constants
EXAM_DATE_COLUMN = "SINAV GÜNÜ"
EXAM_TIME_COLUMN = "BAŞLANGIÇ SAATİ"
EXAM_FINISH_TIME_COLUMN = "BİTİŞ SAATİ"
COURSE_CODE_COLUMN = "DERS KODU"
COURSE_NAME_COLUMN = "DERS ADI"
COURSE_CODE_AND_NAME_COLUMN = "DERS KODU VE ADI"
CLASSROOM_CODE_COLUMN = "DERSLİK/ODA KODLARI"


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
    url = "https://halic.edu.tr/wp-content/uploads/duyurular/2025/11/03/2025-2026-guz-vize-tum-liste.xlsx"

    try:
        # Download Excel file with SSL verification disabled and timeout
        # Note: verify=False is used due to SSL certificate issues with halic.edu.tr
        midterm_xls = requests.get(url, verify=False, timeout=30)
        midterm_xls.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error downloading exam data: {e}")
        # Return empty DataFrame or raise exception based on your preference
        raise Exception(f"Failed to download exam schedule from {url}: {e}")

    # Read Excel file into DataFrame using BytesIO to avoid deprecation warning
    df = pd.read_excel(io.BytesIO(midterm_xls.content))

    # Clean and process course data
    df[COURSE_CODE_COLUMN] = df[COURSE_CODE_COLUMN].apply(lambda x: x.split(";")[0])
    df[COURSE_NAME_COLUMN] = df[COURSE_NAME_COLUMN].apply(lambda x: x.split(";")[0])
    df[COURSE_CODE_COLUMN] = df[COURSE_CODE_COLUMN].apply(
        lambda y: unidecode(y).lower()
    )

    # Clean classroom data if it exists
    if CLASSROOM_CODE_COLUMN in df.columns:
        df[CLASSROOM_CODE_COLUMN] = df[CLASSROOM_CODE_COLUMN].apply(lambda x: str(x))
        df[CLASSROOM_CODE_COLUMN] = df[CLASSROOM_CODE_COLUMN].apply(
            lambda x: x.replace(";", ",")
        )

    # Select and group relevant columns
    columns_to_use = [
        EXAM_DATE_COLUMN,
        EXAM_TIME_COLUMN,
        EXAM_FINISH_TIME_COLUMN,
        COURSE_CODE_COLUMN,
        COURSE_NAME_COLUMN,
    ]
    if CLASSROOM_CODE_COLUMN in df.columns:
        columns_to_use.append(CLASSROOM_CODE_COLUMN)

    # Only include finish time column if it exists in the DataFrame
    if EXAM_FINISH_TIME_COLUMN not in df.columns:
        columns_to_use.remove(EXAM_FINISH_TIME_COLUMN)

    df = df[columns_to_use]

    # Group by course code, taking first occurrence of date, time, and name
    agg_dict = {
        EXAM_DATE_COLUMN: "first",
        EXAM_TIME_COLUMN: "first",
        COURSE_NAME_COLUMN: "first",
    }

    # Add finish time to aggregation if it exists in the DataFrame
    if EXAM_FINISH_TIME_COLUMN in df.columns:
        agg_dict[EXAM_FINISH_TIME_COLUMN] = "first"

    if CLASSROOM_CODE_COLUMN in df.columns:
        agg_dict[CLASSROOM_CODE_COLUMN] = ", ".join

    df = df.groupby(COURSE_CODE_COLUMN).agg(agg_dict).reset_index()

    # Sort by exam date
    df = df.sort_values(by=EXAM_DATE_COLUMN)

    # Create a combined course code and name column
    df[COURSE_CODE_AND_NAME_COLUMN] = (
        df[COURSE_CODE_COLUMN].str.upper() + " (" + df[COURSE_NAME_COLUMN] + ")"
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


def get_exam_date(df, course_code, language="tr"):
    """
    Retrieve exam date in specified language format.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name
        language (str): Language for formatting ('tr' or 'en')

    Returns:
        str: Formatted exam date and time
        
    Raises:
        ValueError: If course_code is not found in the DataFrame
    """
    # Validate that the course exists
    course_rows = df[df[COURSE_CODE_AND_NAME_COLUMN] == course_code]
    if len(course_rows) == 0:
        raise ValueError(f"Course '{course_code}' not found in exam schedule")
    
    date = course_rows[EXAM_DATE_COLUMN].values[0]
    
    if language == "tr":
        week_day = date.split(" ")[1]
        date_full = format_date(date.split(" ")[0])
        formatted_date = f"{date_full} {week_day}"
    else:  # English
        date_formatted = format_date(date.split(" ")[0])
        formatted_date = f"{date_formatted} {datetime.datetime.strptime(date_formatted, '%d/%m/%Y').strftime('%A')}"

    start_time = course_rows[EXAM_TIME_COLUMN].values[0]
    start_time_str = parse_exam_time(start_time)

    # Check if finish time exists and add it to the result
    if EXAM_FINISH_TIME_COLUMN in df.columns:
        finish_time = course_rows[EXAM_FINISH_TIME_COLUMN].values[0]
        finish_time_str = parse_exam_time(finish_time)
        return f"{formatted_date} {start_time_str}-{finish_time_str}"
    else:
        return f"{formatted_date} {start_time_str}"


def tr_getExamDate(df, course_code):
    """
    Retrieve exam date in Turkish format.
    
    Note: This function is deprecated. Use get_exam_date(df, course_code, "tr") instead.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name

    Returns:
        str: Formatted exam date and time in Turkish
    """
    return get_exam_date(df, course_code, "tr")


def en_getExamDate(df, course_code):
    """
    Retrieve exam date in English format.
    
    Note: This function is deprecated. Use get_exam_date(df, course_code, "en") instead.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name

    Returns:
        str: Formatted exam date and time in English
    """
    return get_exam_date(df, course_code, "en")


def getCourseName(df, course_code):
    """
    Retrieve course name for a given course code.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_code (str): Course code and name

    Returns:
        str: Course name
        
    Raises:
        ValueError: If course_code is not found in the DataFrame
    """
    course_rows = df[df[COURSE_CODE_AND_NAME_COLUMN] == course_code]
    if len(course_rows) == 0:
        raise ValueError(f"Course '{course_code}' not found in exam schedule")
    
    return course_rows[COURSE_NAME_COLUMN].values[0]


def get_language_column_names(language="tr"):
    """
    Get column names based on language.
    
    Args:
        language (str): Language code ('tr' or 'en')
    
    Returns:
        dict: Dictionary with column name mappings
    """
    if language == "tr":
        return {
            "course_name": "Ders Adı",
            "exam_date": "Sınav Tarihi",
            "classroom": "Sınıf"
        }
    else:
        return {
            "course_name": "Course Name",
            "exam_date": "Exam Date",
            "classroom": "Classroom Codes"
        }


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
    # Get column names based on language
    col_names = get_language_column_names(language)
    course_name_col = col_names["course_name"]
    exam_date_col = col_names["exam_date"]
    classroom_col = col_names["classroom"]
    
    # Build column list
    columns = [course_name_col, exam_date_col]
    if include_classroom:
        columns.append(classroom_col)
    
    # Create result DataFrame
    result_df = pd.DataFrame([], columns=columns)
    
    for course in course_list:
        list_row = [getCourseName(df, course), get_exam_date(df, course, language)]
        if include_classroom:
            list_row.append(getClassroom(df, course))
        result_df.loc[len(result_df)] = list_row

    # Sort by date and time
    def parse_date(date_str):
        date_parts = date_str.split()
        time_part = date_parts[2]  # Extract time part

        # Handle both single time and time range formats
        if "-" in time_part:
            start_time = time_part.split("-")[0]
        else:
            start_time = time_part

        return datetime.datetime.strptime(
            f"{date_parts[0]} {start_time}", "%d/%m/%Y %H:%M"
        )

    result_df["Parsed Date"] = result_df[exam_date_col].apply(parse_date)
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
        
    Raises:
        ValueError: If course_code is not found in the DataFrame
    """
    if CLASSROOM_CODE_COLUMN not in df.columns:
        return "N/A"

    course_rows = df[df[COURSE_CODE_AND_NAME_COLUMN] == course_code]
    if len(course_rows) == 0:
        raise ValueError(f"Course '{course_code}' not found in exam schedule")

    classroom = course_rows[CLASSROOM_CODE_COLUMN].values[0]
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


def create_ics_file(df, course_list, language="tr", exam_type="midterm"):
    """
    Create an ICS file from the exam schedule data.

    Args:
        df (pd.DataFrame): Exam schedule DataFrame
        course_list (list): List of selected courses
        language (str): Language of the result ('tr' or 'en')
        exam_type (str): Type of exam ('midterm' or 'final')

    Returns:
        str: ICS file content as a string
    """
    import datetime
    import uuid

    # Start with the ICS file header
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ExamGenius//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    # Get the result DataFrame to work with
    result_df = create_result_dataframe(
        df, course_list, language, include_classroom=True
    )

    # Get column names based on language
    col_names = get_language_column_names(language)
    course_name_col = col_names["course_name"]
    exam_date_col = col_names["exam_date"]
    classroom_col = col_names["classroom"]
    
    # Determine exam type text based on language
    exam_type_text = "Vize" if exam_type == "midterm" else "Final"
    if language == "en":
        exam_type_text = "Midterm" if exam_type == "midterm" else "Final"

    # Process each row in the result DataFrame
    for _, row in result_df.iterrows():
        course_name = row[course_name_col]
        exam_date_str = row[exam_date_col]
        classroom = row[classroom_col] if classroom_col in row else "N/A"

        # Parse the date and time
        date_parts = exam_date_str.split()
        date_str = date_parts[0]  # Format: dd/mm/yyyy
        time_part = date_parts[-1]  # Format: HH:MM or HH:MM-HH:MM

        # Parse the date
        day, month, year = map(int, date_str.split("/"))

        # Handle time parsing (could be start time only or start-end time)
        if "-" in time_part:
            # Both start and end times are provided
            start_time_str, end_time_str = time_part.split("-")
            start_hour, start_minute = map(int, start_time_str.split(":"))
            end_hour, end_minute = map(int, end_time_str.split(":"))

            start_datetime = datetime.datetime(
                year, month, day, start_hour, start_minute
            )
            end_datetime = datetime.datetime(year, month, day, end_hour, end_minute)
        else:
            # Only start time provided, assume 2-hour duration
            start_hour, start_minute = map(int, time_part.split(":"))
            start_datetime = datetime.datetime(
                year, month, day, start_hour, start_minute
            )
            end_datetime = start_datetime + datetime.timedelta(hours=2)

        # Format dates for ICS
        start_str = start_datetime.strftime("%Y%m%dT%H%M%S")
        end_str = end_datetime.strftime("%Y%m%dT%H%M%S")

        # Create a unique ID for the event
        event_uid = str(uuid.uuid4())

        # Create the event
        summary = f"{course_name} {exam_type_text.title()}"
        description = (
            f"{exam_type_text} exam for {course_name}"
            if language == "en"
            else f"{course_name} {exam_type_text.lower()} sınavı"
        )

        # Add the event to the ICS content
        ics_content.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{event_uid}",
                f"DTSTAMP:{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}",
                f"DTSTART:{start_str}",
                f"DTEND:{end_str}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                f"LOCATION:{classroom}",
                "END:VEVENT",
            ]
        )

    # Add the ICS file footer
    ics_content.append("END:VCALENDAR")

    # Join the ICS content with line breaks
    return "\n".join(ics_content)


# Global DataFrame - initialized lazily
_df_cache = None


def get_df():
    """
    Get the exam data DataFrame, loading it if necessary.
    
    Returns:
        pd.DataFrame: Exam schedule DataFrame
    """
    global _df_cache
    if _df_cache is None:
        _df_cache = process_exam_data()
    return _df_cache


# For backward compatibility, try to load df at module import
# but don't fail if network is unavailable
try:
    df = process_exam_data()
except (requests.exceptions.RequestException, ConnectionError, Exception) as e:
    # If data fetch fails at import time, df will be None
    # Functions should use get_df() for lazy loading
    df = None
