# 🎭 Theatre Třesk! — Ticket Booking Web Application

A full-featured web application for the **Třesk!** theater in Prague, developed as a capstone project. The platform allows users to browse upcoming performances, check schedules, and securely book tickets with instant email confirmations.

---

## 🛠 Tech Stack

* **Backend:** Python 3.10+, Django 6.0, Django REST Framework (APIView)
* **Database:** SQLite, Django Transactions (`transaction.atomic`, `select_for_update`)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API, asynchronous requests)
* **Utilities:** Email notifications (`send_mail`), Git / GitHub

---

## ✨ Key Features

* **Repertoire & Schedule:** Browse available plays with dates, times, and pricing in Czech Koruna (CZK).
* **Booking System:** Seat reservation with protection against race conditions and overselling using `select_for_update()`.
* **Data Validation:** Robust input validation on both frontend and backend (checking required fields and seat counts).
* **Automated Notifications:** Automatic booking confirmation emails sent to customers upon successful reservation.

---

## 🚀 Getting Started Locally

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/PavlaFelidae/final-project-theater.git](https://github.com/PavlaFelidae/final-project-theater.git)
   cd final-project-theater