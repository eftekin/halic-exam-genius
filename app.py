import io

import streamlit as st

from utils import create_ics_file, create_result_dataframe, createImage, df

# Configure page settings - must be first Streamlit command
st.set_page_config(page_title="Exam Genius", page_icon="📚")


def create_grade_section(label, idx, language_on, default_grade=0.0, default_weight=0):
    """
    Create a section for inputting grade and weight for an exam.

    Args:
        label (str): Section label (e.g., "Midterm", "Final")
        idx (int): Index of the exam section
        language_on (bool): Language toggle state
        default_grade (float): Default grade value
        default_weight (int): Default weight value

    Returns:
        tuple: Grade and weight values
    """
    st.write(f"### {label}")
    col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])

    with col1:
        grade = st.number_input(
            f"{'Not' if not language_on else 'Grade'}",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key=f"grade_{idx}",
            value=default_grade,
        )

    with col2:
        weight = st.number_input(
            f"{'Yüzde' if not language_on else 'Pct'}",
            min_value=0,
            max_value=100,
            step=1,
            key=f"weight_{idx}",
            value=default_weight,
        )

    return grade, weight


def format_grade(grade):
    return (
        f"{grade:.1f}".rstrip("0").rstrip(".")
        if "." in f"{grade:.1f}"
        else f"{grade:.0f}"
    )


def main():
    """
    Main Streamlit application for Exam Genius.
    Handles grade calculation and exam date display.
    """
    # Application configuration
    last_update = "14.03.2025 13:40"  # Last update date and time
    st.title("Exam Genius📚")
    language_on = st.toggle("🇺🇸 EN", key="language_toggle", value=False)

    # Sidebar: Grade Calculator Section
    with st.sidebar:
        st.header("📊 Not Hesaplama" if not language_on else "📊 Grade Calculation")

        # Usage instructions in an expander
        with st.expander(
            "📖 Nasıl Kullanılır?" if not language_on else "📖 How To Use?"
        ):
            instructions = (
                """
                1. **➕ Sınav Ekleyin**: Yeni sınavlar eklemek için "Sınav Ekle" butonuna tıklayın. İhtiyacınıza göre istediğiniz kadar sınav ekleyebilirsiniz.
                2. **📝 Not ve Yüzde Girin**: Her sınav için notu ve yüzdesini girin. Toplam yüzdelik değerinin 100% olduğunu kontrol edin.
                3. **🎯 Geçme Notunu Ayarlayın**: Gereken minimum geçme notunu girin.
                4. **🔍 Hesapla**: "Hesapla" butonuna tıklayarak girdiğiniz not ve yüzdelere göre geçip geçmediğinizi görün.
                5. **📅 Sınav Tarihleri**: "Sınav Tarihleri" bölümünü kullanarak derslerinizin sınav tarihlerini görüntüleyin ve indirin.
                6. **📆 Takvime Ekle**: "Takvime Ekle" butonu ile sınav tarihlerinizi takvim uygulamanıza ekleyebilirsiniz.
                """
                if not language_on
                else """
                1. **➕ Add Exams**: Click on "Add Exam" to add new exams to your list. You can add as many exams as you need.
                2. **📝 Enter Grades and Weights**: For each exam, enter the grade and its weight. Ensure that the total weight adds up to 100%.
                3. **🎯 Set Passing Grade**: Enter the minimum passing grade required.
                4. **🔍 Calculate**: Click on "Calculate" to see if you have passed based on the grades and weights you entered.
                5. **📅 Exam Dates**: Use the "Exam Dates" section to view and download the exam dates for your courses.
                6. **📆 Add to Calendar**: Use the "Add to Calendar" button to add your exam dates to your calendar application.
                """
            )
            st.write(instructions)

        # Exam sections management
        num_exams = st.session_state.get("num_exams", 2)

        # Passing grade input with default value
        passing_grade = st.number_input(
            "🎯 Geçme Notu" if not language_on else "🎯 Passing Grade",
            max_value=100,
            value=50,
        )

        # Adding or removing exam fields
        if st.button("➕ Sınav Ekle" if not language_on else "➕ Add Exam"):
            num_exams += 1
            st.session_state["num_exams"] = num_exams

        if num_exams > 2:
            if st.button(
                "➖ Son Sınavı Çıkar" if not language_on else "➖ Remove Last Exam"
            ):
                num_exams -= 1
                st.session_state["num_exams"] = num_exams

        # Grade input sections with default weights
        grades = []
        weights = []
        for i in range(num_exams):
            if i == 0:
                label = "Vize" if not language_on else "Midterm"
                default_weight = 40
            elif i == 1:
                label = "Final"
                default_weight = 60
            else:
                label = f"Diğer {i - 1}" if not language_on else f"Other {i - 1}"
                default_weight = 0

            grade, weight = create_grade_section(
                label, i + 1, language_on, default_weight=default_weight
            )
            grades.append(grade)
            weights.append(weight)

        # Calculate grades
        if st.button("🔍 Hesapla" if not language_on else "🔍 Calculate"):
            total_weight = sum(weights)

            if total_weight != 100:
                st.error(
                    f"⚠️ Yüzdelerin toplamı 100 olmalıdır. Şu anki toplam: %{total_weight}"
                    if not language_on
                    else f"⚠️ The total percentage must be 100. Current total: {total_weight}%"
                )
            else:
                total = sum(
                    grade * (weight / 100) for grade, weight in zip(grades, weights)
                )
                total_formatted = format_grade(total)  # Format the total grade

                if passing_grade == 0:
                    st.success(
                        f"✅ Toplam Notunuz: {total_formatted}"
                        if not language_on
                        else f"✅ Your Total Grade: {total_formatted}"
                    )
                else:
                    if total >= passing_grade:
                        st.success(
                            f"🎉 Tebrikler! {total_formatted} notuyla dersi geçtiniz."
                            if not language_on
                            else f"🎉 Congratulations! You have passed the course with a grade of {total_formatted} 🥳"
                        )
                    else:
                        st.warning(
                            f"😢 Maalesef, dersi geçemediniz. Notunuz {total_formatted} 🥺"
                            if not language_on
                            else f"😢 Unfortunately, you did not pass the course. Your grade is {total_formatted} 🥺"
                        )

    # Main Content: Exam Dates Section
    st.write(
        "### 2025 Bahar Dönemi Ara Sınav Tarihleri"
        if not language_on
        else "### 2025 Spring Semester Midterm Exam Dates"
    )
    st.write(
        "Aşağıda 2025 Bahar dönemi için ara sınav tarihleri yer almaktadır."
        if not language_on
        else "Below are the make-up exam dates for the 2025 Spring semester."
    )
    st.write(
        "Lütfen sınav tarihlerini görmek istediğiniz ders kodlarını seçin."
        if not language_on
        else "Please select the course codes of the courses for which you want to see the exam dates."
    )

    course_list = st.multiselect(
        "Dersleri Seçin" if not language_on else "Select Courses",
        df["DERS KODU VE ADI"],
        placeholder="Ders Kodu veya Adı" if not language_on else "Course Code or Name",
    )

    col1, col2, col3 = st.columns(3)

    if len(course_list) > 0 and col1.button(
        "Sınav Tarihlerini Göster" if not language_on else "Show Exam Dates"
    ):
        result_df = create_result_dataframe(
            df, course_list, "tr" if not language_on else "en", include_classroom=True
        )
        st.dataframe(result_df, hide_index=True)
        createImage(result_df)

        with open("output/examgenius.png", "rb") as file:
            col2.download_button(
                "Resim Olarak İndir" if not language_on else "Download as Image",
                data=file,
                file_name="examgenius.png",
                mime="image/png",
            )

        # Create and offer download of ICS file
        ics_content = create_ics_file(
            df, course_list, "tr" if not language_on else "en", exam_type="midterm"
        )
        ics_bytes = ics_content.encode()

        col3.download_button(
            "📆 Takvime Ekle" if not language_on else "📆 Add to Calendar",
            data=io.BytesIO(ics_bytes),
            file_name="exam_schedule.ics",
            mime="text/calendar",
            help="Sınav tarihlerini takvim uygulamanıza eklemek için tıklayın"
            if not language_on
            else "Click to add exam dates to your calendar application",
        )

    # Footer: Update info and feedback side by side
    footer_col1, footer_col2 = st.columns(2)
    with footer_col1:
        st.caption(
            f"🕐 Son Güncelleme: {last_update}"
            if not language_on
            else f"🕐 Last Update: {last_update}"
        )
    with footer_col2:
        st.caption(
            "💌 Geri bildirim: [mustafa@eftekin.dev](mailto:mustafa@eftekin.dev) | [eftekin.com](https://eftekin.com)"
            if not language_on
            else "💌 Feedback: [mustafa@eftekin.dev](mailto:mustafa@eftekin.dev) | [eftekin.com](https://eftekin.com)"
        )


if __name__ == "__main__":
    main()
