# 📚 Library Management System – IIIT Sonepat

We have developed a **prototype software system** to streamline and automate complex library operations at the **Indian Institute of Information Technology (IIIT) Sonepat**. This solution enhances the day-to-day workflow of librarians and administrators by introducing a secure and intelligent platform built using **FastAPI** for the backend and **JavaScript** for the frontend.

To ensure security during book transactions, an **OTP-based validation system** is implemented when issuing books—minimizing fraud and enforcing accountability. Additionally, we have integrated **Chart.js** into the dashboard to generate dynamic, visual library usage reports. These charts assist librarians and administrators in tracking book issues, returns, and usage patterns effectively.

📄 [**Click here to view the full project report**](https://github.com/sankhadeeproycbowdhury/LIbraryManagementSystem/blob/main/Report.pdf)

---

## 🚀 How to Use the System

Follow the steps below to set up and run the system locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt

3. **Start the Frontend Server**
    ```bash
    cd frontend
    python -m http.server 3000

4. **Start the Backend API Server**
    ```bash
    cd backend
    uvicorn main:app --reload
