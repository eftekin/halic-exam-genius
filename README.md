<div align="center">

# 📚 Halic Exam Genius

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/eftekin/halic-exam-genius)](https://github.com/eftekin/halic-exam-genius/issues)
[![GitHub Stars](https://img.shields.io/github/stars/eftekin/halic-exam-genius)](https://github.com/eftekin/halic-exam-genius/stargazers)

_A comprehensive exam management and grade calculation tool for Halic University students_

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Technology](#-technology-stack) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

**Halic Exam Genius** is a web-based application designed for Halic University students. The application automatically processes official Excel files containing exam dates from the university's announcement page, providing students with easy access to current exam schedules, classroom information, and comprehensive grade calculations through an intuitive web interface.

## ✨ Features

### 📅 **Exam Schedule Management**

- **Automated Data Processing**: Reads and processes Excel files from Halic University announcements
- **Current Exam Dates**: View up-to-date exam dates and classroom information
- **Calendar Integration**: Export exam schedules as ICS files for calendar applications
- **Multi-language Support**: Available in Turkish and English

![exam_date_gif](https://github.com/user-attachments/assets/b895b1fb-2372-48ab-b03e-7026eabecf4e)

### 🧮 **Grade Calculator**

- **Weighted Grade Calculation**: Calculate overall grades with customizable exam weights
- **Pass/Fail Analysis**: Set passing thresholds and see if you've passed the course
- **Visual Grade Reports**: Generate visual grade summary charts
- **Grade Export**: Download your grade calculations as images

![grade_calc_gif](https://github.com/user-attachments/assets/48a3e52d-7fb9-4937-862e-235715d4f437)

### 🔧 **Additional Features**

- **Responsive Web Interface**: Works on desktop and mobile browsers via Streamlit
- **Course Selection**: Multi-select interface for choosing specific courses
- **Real-time Calculations**: Instant grade calculations as you input data

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/eftekin/halic-exam-genius.git
   cd halic-exam-genius
   ```

2. **Create Virtual Environment** (Recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Application**

   ```bash
   streamlit run app.py
   ```

5. **Access the Application**
   Open your browser and navigate to [http://localhost:8501](http://localhost:8501)

## 📖 Usage

### Getting Started

1. **Launch the Application**: Run the Streamlit app using `streamlit run app.py`
2. **View Exam Schedule**: Browse current semester exam dates
3. **Select Courses**: Choose specific courses to see their exam information
4. **Calculate Grades**: Input your exam scores and weights for automatic calculation
5. **Export Results**: Download your schedules as ICS files or grade charts as images

### Supported Data Source

- The application automatically fetches data from Halic University's official Excel files for current semester exams

## 🛠 Technology Stack

- **Frontend Framework**: Streamlit - Web application framework
- **Backend Language**: Python 3.9+
- **Data Processing**: Pandas - Data manipulation and analysis
- **Excel Processing**: Openpyxl - Excel file reading and processing
- **Visualization**: Plotly - Interactive charts and visualizations
- **Image Export**: Kaleido - Static image export for Plotly charts
- **Date Handling**: Datetime - Date and time operations
- **Text Processing**: Unidecode - Unicode text normalization
- **HTTP Requests**: Requests - Fetching data from university servers

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Ways to Contribute

- 🐛 Report bugs or issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🌐 Help with translations
- 🔧 Submit code improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support & Community

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/eftekin/halic-exam-genius/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/eftekin/halic-exam-genius/discussions)
- **Email**: For direct support, contact the maintainer

## 🏆 Acknowledgments

- Halic University for providing the data structure and requirements
- The open-source community for the amazing tools and libraries
- All contributors who help improve this project

---

<div align="center">

**Made with ❤️ for Halic University Students**

⭐ Star this repo if it helped you! ⭐

</div>
