# Face Recognition Based Smart Attendance System

A modern, efficient attendance management system that uses facial recognition technology to automate the attendance tracking process. This system provides a user-friendly interface for managing student attendance through facial recognition.

## 🚀 Features

- **Face Recognition Based Attendance**: Automatically marks attendance by recognizing faces
- **Real-time Processing**: Live face detection and recognition
- **Secure Access**: Password protected system administration
- **Student Management**: Add and manage student details easily
- **Attendance Records**: Maintains attendance records in CSV format
- **User-friendly Interface**: Built with tkinter for a clean and intuitive GUI
- **Data Persistence**: Stores training data and attendance records locally

## 📋 Prerequisites

Before running this system, make sure you have the following installed:
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Pillow (PIL)
- pandas
- tkinter (usually comes with Python)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/Jainam116/Face-Recognized-Based-Smart-Attendence-System.git
cd Face-Recognized-Based-Smart-Attendence-System
```

2. Install the required packages:
```bash
pip install opencv-python numpy pillow pandas
```

## 📁 Project Structure

```
├── haarcascade_frontalface_default.xml  # Face detection model
├── main.py                              # Main application file
├── Attendance/                          # Stores attendance records
├── StudentDetails/                      # Contains student information
│   └── StudentDetails.csv
├── TrainingImage/                       # Stores training images
└── TrainingImageLabel/                  # Contains training data
    ├── psd.txt                         # Password file
    └── Trainner.yml                    # Trained model file
```

## 🔧 Usage

1. Run the main application:
```bash
python main.py
```

2. First-time setup:
   - Set up an admin password when prompted
   - Add student details through the interface
   - Take photos for face training
   - Train the system with collected images

3. Regular use:
   - Launch the application
   - Start face recognition
   - View or export attendance records

## 🔐 Security Features

- Password protected admin access
- Secure storage of training data
- Protected attendance records

## 📊 Data Management

- Student details are stored in CSV format
- Attendance records are maintained with timestamps
- Training images are saved securely
- Face recognition model data is preserved for future use

