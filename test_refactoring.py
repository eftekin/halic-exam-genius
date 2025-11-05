"""
Test script to validate refactored functions in utils.py
This tests the refactored code without requiring network access.
"""

import datetime
import pandas as pd
from utils import (
    format_date,
    parse_exam_time,
    get_exam_date,
    tr_getExamDate,
    en_getExamDate,
    getCourseName,
    getClassroom,
    get_language_column_names,
    EXAM_DATE_COLUMN,
    EXAM_TIME_COLUMN,
    EXAM_FINISH_TIME_COLUMN,
    COURSE_CODE_COLUMN,
    COURSE_NAME_COLUMN,
    COURSE_CODE_AND_NAME_COLUMN,
    CLASSROOM_CODE_COLUMN,
)


def test_format_date():
    """Test date formatting function"""
    print("Testing format_date...")
    
    # Test yyyy-mm-dd format
    result1 = format_date("2025-11-15 Cuma")
    assert result1 == "15/11/2025", f"Expected '15/11/2025', got '{result1}'"
    
    # Test dd.mm.yyyy format
    result2 = format_date("15.11.2025 Cuma")
    assert result2 == "15/11/2025", f"Expected '15/11/2025', got '{result2}'"
    
    print("✓ format_date tests passed")


def test_parse_exam_time():
    """Test time parsing function"""
    print("Testing parse_exam_time...")
    
    # Test with seconds
    result1 = parse_exam_time("09:30:00")
    assert result1 == "09:30", f"Expected '09:30', got '{result1}'"
    
    # Test without seconds
    result2 = parse_exam_time("14:15")
    assert result2 == "14:15", f"Expected '14:15', got '{result2}'"
    
    # Test with time object
    time_obj = datetime.time(10, 45)
    result3 = parse_exam_time(time_obj)
    assert result3 == "10:45", f"Expected '10:45', got '{result3}'"
    
    print("✓ parse_exam_time tests passed")


def test_constants_defined():
    """Test that all constants are properly defined"""
    print("Testing constants...")
    
    assert EXAM_DATE_COLUMN == "SINAV GÜNÜ"
    assert EXAM_TIME_COLUMN == "BAŞLANGIÇ SAATİ"
    assert EXAM_FINISH_TIME_COLUMN == "BİTİŞ SAATİ"
    assert COURSE_CODE_COLUMN == "DERS KODU"
    assert COURSE_NAME_COLUMN == "DERS ADI"
    assert COURSE_CODE_AND_NAME_COLUMN == "DERS KODU VE ADI"
    assert CLASSROOM_CODE_COLUMN == "DERSLİK/ODA KODLARI"
    
    print("✓ All constants properly defined")


def test_get_exam_date():
    """Test consolidated get_exam_date function"""
    print("Testing get_exam_date...")
    
    # Create mock DataFrame
    test_data = {
        COURSE_CODE_COLUMN: ["comp101"],
        COURSE_NAME_COLUMN: ["Computer Science"],
        EXAM_DATE_COLUMN: ["2025-11-15 Cuma"],
        EXAM_TIME_COLUMN: ["09:30:00"],
        EXAM_FINISH_TIME_COLUMN: ["11:30:00"],
        COURSE_CODE_AND_NAME_COLUMN: ["COMP101 (Computer Science)"],
        CLASSROOM_CODE_COLUMN: ["A-101"],
    }
    df = pd.DataFrame(test_data)
    
    # Test Turkish format
    result_tr = get_exam_date(df, "COMP101 (Computer Science)", "tr")
    assert "15/11/2025" in result_tr, f"Expected date in Turkish result, got '{result_tr}'"
    assert "Cuma" in result_tr, f"Expected 'Cuma' in Turkish result, got '{result_tr}'"
    assert "09:30" in result_tr, f"Expected time in Turkish result, got '{result_tr}'"
    
    # Test English format
    result_en = get_exam_date(df, "COMP101 (Computer Science)", "en")
    assert "15/11/2025" in result_en, f"Expected date in English result, got '{result_en}'"
    assert "09:30" in result_en, f"Expected time in English result, got '{result_en}'"
    
    print("✓ get_exam_date tests passed")


def test_backward_compatibility():
    """Test that old functions still work through new implementation"""
    print("Testing backward compatibility...")
    
    # Create mock DataFrame
    test_data = {
        COURSE_CODE_COLUMN: ["comp101"],
        COURSE_NAME_COLUMN: ["Computer Science"],
        EXAM_DATE_COLUMN: ["2025-11-15 Cuma"],
        EXAM_TIME_COLUMN: ["09:30:00"],
        EXAM_FINISH_TIME_COLUMN: ["11:30:00"],
        COURSE_CODE_AND_NAME_COLUMN: ["COMP101 (Computer Science)"],
        CLASSROOM_CODE_COLUMN: ["A-101"],
    }
    df = pd.DataFrame(test_data)
    
    # Test old Turkish function
    result_tr = tr_getExamDate(df, "COMP101 (Computer Science)")
    assert "15/11/2025" in result_tr, f"Expected date in tr_getExamDate result"
    
    # Test old English function
    result_en = en_getExamDate(df, "COMP101 (Computer Science)")
    assert "15/11/2025" in result_en, f"Expected date in en_getExamDate result"
    
    print("✓ Backward compatibility tests passed")


def test_getCourseName():
    """Test getCourseName function"""
    print("Testing getCourseName...")
    
    test_data = {
        COURSE_CODE_COLUMN: ["comp101"],
        COURSE_NAME_COLUMN: ["Computer Science"],
        COURSE_CODE_AND_NAME_COLUMN: ["COMP101 (Computer Science)"],
    }
    df = pd.DataFrame(test_data)
    
    result = getCourseName(df, "COMP101 (Computer Science)")
    assert result == "Computer Science", f"Expected 'Computer Science', got '{result}'"
    
    print("✓ getCourseName tests passed")


def test_get_language_column_names():
    """Test language column name helper"""
    print("Testing get_language_column_names...")
    
    # Test Turkish
    tr_cols = get_language_column_names("tr")
    assert tr_cols["course_name"] == "Ders Adı"
    assert tr_cols["exam_date"] == "Sınav Tarihi"
    assert tr_cols["classroom"] == "Sınıf"
    
    # Test English
    en_cols = get_language_column_names("en")
    assert en_cols["course_name"] == "Course Name"
    assert en_cols["exam_date"] == "Exam Date"
    assert en_cols["classroom"] == "Classroom Codes"
    
    print("✓ get_language_column_names tests passed")


def test_getClassroom():
    """Test getClassroom function"""
    print("Testing getClassroom...")
    
    test_data = {
        COURSE_CODE_COLUMN: ["comp101"],
        COURSE_CODE_AND_NAME_COLUMN: ["COMP101 (Computer Science)"],
        CLASSROOM_CODE_COLUMN: ["A-101,A-102,A-103"],
    }
    df = pd.DataFrame(test_data)
    
    result = getClassroom(df, "COMP101 (Computer Science)")
    assert result == "A-101,A-102,A-103", f"Expected classroom info, got '{result}'"
    
    # Test with missing column
    df_no_classroom = df.drop(columns=[CLASSROOM_CODE_COLUMN])
    result_na = getClassroom(df_no_classroom, "COMP101 (Computer Science)")
    assert result_na == "N/A", f"Expected 'N/A', got '{result_na}'"
    
    # Test with many classrooms (should truncate)
    test_data_many = {
        COURSE_CODE_COLUMN: ["comp101"],
        COURSE_CODE_AND_NAME_COLUMN: ["COMP101 (Computer Science)"],
        CLASSROOM_CODE_COLUMN: ["A-101,A-102,A-103,A-104,A-105,A-106,A-107"],
    }
    df_many = pd.DataFrame(test_data_many)
    result_truncated = getClassroom(df_many, "COMP101 (Computer Science)")
    assert "..." in result_truncated, f"Expected truncation with '...', got '{result_truncated}'"
    
    print("✓ getClassroom tests passed")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Refactoring Validation Tests")
    print("="*60 + "\n")
    
    try:
        test_constants_defined()
        test_format_date()
        test_parse_exam_time()
        test_get_exam_date()
        test_backward_compatibility()
        test_getCourseName()
        test_get_language_column_names()
        test_getClassroom()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - Refactoring is successful!")
        print("="*60 + "\n")
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
