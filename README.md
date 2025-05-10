# 📚 Library Management System – IIIT Sonepat

We have developed a **prototype software system** to streamline and automate complex library operations at the **Indian Institute of Information Technology (IIIT) Sonepat**. This solution enhances the day-to-day workflow of librarians and administrators by introducing a secure and intelligent platform built using **FastAPI** for the backend and **JavaScript** for the frontend.

To ensure security during book transactions, an **OTP-based validation system** is implemented when issuing books—minimizing fraud and enforcing accountability. Additionally, we have integrated **Chart.js** into the dashboard to generate dynamic, visual library usage reports. These charts assist librarians and administrators in tracking book issues, returns, and usage patterns effectively.

📄 [**Click here to view the full project report**](https://github.com/sankhadeeproycbowdhury/LIbraryManagementSystem/blob/main/Report.pdf)

---

## 🚀 How to Use the System

Follow the steps below to set up and run the system locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sidsingh04/LibraryManagementSystem
   cd LibraryManagementSystem

2. **Virtual Environment(Windows)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   
3. **Virtual Environment(macOS/Linux)**
   ```bash
   python -m venv venv
   source venv/bin/activate
   
4. **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt

5. **Set Environment Variables**
    ```bash
    set Environment Variables for the following features or
    
    create local .env file in root directory and set them there :-
    
    1.DB_HOST, 2.DB_USER, 3.DB_PASSWORD, 4.DB_NAME,
    5.JWT_SECRET_KEY, 6.ACCESS_TOKEN_EXPIRE_MINUTES, 7.ALGORITHM,
    8.ADMIN_USERNAME, 9.ADMIN_PASSWORD, 10.ADMIN_EMAIL, 11.ADMIN_JOBID,
    12.EMAIL_SENDER, 13.EMAIL_PASSWORD

6. **Start the Frontend Server**
    ```bash
    cd FrontEnd
    python -m http.server 3000

7. **Start the Backend API Server**
    ```bash
    cd ../BackEnd
    uvicorn main:app --reload

    For further details regarding Backend API endpoints visit
    http://127.0.0.1:8000/docs or http://localhost:8000/docs
