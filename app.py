import streamlit as st

# Import functions from utils module
from utils import create_result_dataframe, createImage, df


def create_grade_section(label, idx, language_on):
    """
    Create a section for inputting grade and weight for an exam.

    Args:
        label (str): Section label (e.g., "Midterm", "Final")
        idx (int): Index of the exam section
        language_on (bool): Language toggle state

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
        )

    with col2:
        weight = st.number_input(
            f"{'Yüzde' if not language_on else 'Pct'}",
            min_value=0,
            max_value=100,
            step=1,
            key=f"weight_{idx}",
        )

    return grade, weight


def main():
    """
    Main Streamlit application for Exam Genius.
    Handles grade calculation and exam date display.
    """
    # Last update timestamp
    last_update = "17.12.2024 20:56"

    # App title
    st.title("Exam Genius📚")

    # Language toggle
    language_on = st.toggle("🇺🇸 EN", key="language_toggle", value=False)

    # Sidebar section for adding/removing exams
    with st.sidebar:
        st.header("Not Hesaplama" if not language_on else "Grade Calculation")

        # Usage instructions in an expander
        with st.expander("Nasıl Kullanılır?" if not language_on else "How To Use?"):
            instructions = (
                """
                1. **Sınav Ekleyin**: Yeni sınavlar eklemek için "Sınav Ekle" butonuna tıklayın. İhtiyacınıza göre istediğiniz kadar sınav ekleyebilirsiniz.
                2. **Not ve Yüzde Girin**: Her sınav için notu ve yüzdesini girin. Toplam yüzdelik değerinin 100% olduğunu kontrol edin.
                3. **Geçme Notunu Ayarlayın**: Gereken minimum geçme notunu girin.
                4. **Hesapla**: "Hesapla" butonuna tıklayarak girdiğiniz not ve yüzdelere göre geçip geçmediğinizi görün.
                5. **Sınav Tarihleri**: "Sınav Tarihleri" bölümünü kullanarak derslerinizin sınav tarihlerini görüntüleyin ve indirin.
                """
                if not language_on
                else """
                1. **Add Exams**: Click on "Add Exam" to add new exams to your list. You can add as many exams as you need.
                2. **Enter Grades and Weights**: For each exam, enter the grade and its weight. Ensure that the total weight adds up to 100%.
                3. **Set Passing Grade**: Enter the minimum passing grade required.
                4. **Calculate**: Click on "Calculate" to see if you have passed based on the grades and weights you entered.
                5. **Exam Dates**: Use the "Exam Dates" section to view and download the exam dates for your courses.
                """
            )
            st.write(instructions)

        # Exam sections management
        num_exams = st.session_state.get("num_exams", 2)

        # Passing grade input
        passing_grade = st.number_input(
            "Geçme Notu" if not language_on else "Passing Grade",
            max_value=100,
        )

        # Adding or removing exam fields
        if st.button("Add Exam" if language_on else "Sınav Ekle"):
            num_exams += 1
            st.session_state["num_exams"] = num_exams

        if num_exams > 2:
            if st.button("Remove Last Exam" if language_on else "Son Sınavı Çıkar"):
                num_exams -= 1
                st.session_state["num_exams"] = num_exams

        # Grade input sections
        grades = []
        weights = []
        for i in range(num_exams):
            if i == 0:
                label = "Midterm" if language_on else "Vize"
            elif i == 1:
                label = "Final"
            else:
                label = f"Other {i-1}" if language_on else f"Diğer {i-1}"

            grade, weight = create_grade_section(label, i + 1, language_on)
            grades.append(grade)
            weights.append(weight)

        # Calculate grades
        if st.button("Hesapla" if not language_on else "Calculate"):
            total_weight = sum(weights)

            if total_weight != 100:
                st.error(
                    f"Yüzdelerin toplamı 100 olmalıdır. Şu anki toplam: %{total_weight}"
                    if not language_on
                    else f"The total percentage must be 100. Current total: {total_weight}%"
                )
            else:
                total = sum(
                    grade * (weight / 100) for grade, weight in zip(grades, weights)
                )

                if passing_grade == 0:
                    st.success(
                        f"Toplam Notunuz: {total}"
                        if not language_on
                        else f"Your Total Grade: {total}"
                    )
                else:
                    if total >= passing_grade:
                        st.success(
                            f"Tebrikler! {total} notuyla dersi geçtiniz. 🥳"
                            if not language_on
                            else f"Congratulations! You have passed the course with a grade of {total}. 🥳"
                        )
                    else:
                        st.warning(
                            f"Maalesef, dersi geçemediniz. Notunuz {total}. 🥺"
                            if not language_on
                            else f"Unfortunately, you did not pass the course. Your grade is {total}. 🥺"
                        )

    # Exam dates section
    st.write(
        "### 2024 Güz Dönemi Final Sınav Tarihleri"
        if not language_on
        else "### 2024 Fall Semester Final Exam Dates"
    )
    st.write(
        "Aşağıda 2024 Güz dönemi için final sınav tarihleri yer almaktadır."
        if not language_on
        else "Below are the final exam dates for the 2024 Fall semester."
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

    col1, col2 = st.columns(2)

    if len(course_list) > 0 and col1.button(
        "Sınav Tarihlerini Göster" if not language_on else "Show Exam Dates"
    ):
        result_df = create_result_dataframe(
            df, course_list, "tr" if not language_on else "en"
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

    # Update and feedback captions
    st.caption(
        f"Son Güncelleme {last_update}"
        if not language_on
        else f"Last Update {last_update}"
    )
    st.caption(
        "Geri bildirimleriniz için: [mustafa@eftekin.dev](mailto:mustafa@eftekin.dev) 💌"
        if not language_on
        else "For feedback: [mustafa@eftekin.dev](mailto:mustafa@eftekin.dev) 💌"
    )


if __name__ == "__main__":
    main()
