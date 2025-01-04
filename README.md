# Course Tracker Application

## Overview
The Course Tracker Application is a web-based tool designed to help students efficiently manage their courses and tasks. Built with Python using the Flask framework and an SQL database, this application provides a streamlined way to organize academic responsibilities, track progress, and stay on top of deadlines.

## Features
- **Course Management:** Add, update, and delete courses to keep your academic schedule organized.
- **Task Management:** Associate tasks with specific courses, set due dates, and mark tasks as completed.
- **User-Friendly Interface:** A simple and intuitive design for easy navigation and usability.
- **Persistent Data Storage:** Utilizes SQL for reliable and efficient data storage, ensuring your information is always accessible.
- **Lightweight:** Minimal dependencies and quick setup, ideal for students with varying technical expertise.

## Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, and JavaScript (optional for interactive features)
- **Database:** SQL (SQLite or any other supported SQL database)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd course-tracker
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the application:
   ```bash
   flask run
   ```
6. Access the application in your browser at `http://127.0.0.1:5000`.

## Usage
1. Log in or create a new account.
2. Add your current courses to the dashboard.
3. Assign tasks to each course with deadlines and additional notes.
4. Track your progress and mark tasks as completed as you work through them.

## Contribution
Contributions are welcome! If you want to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git push origin feature-name
   ```
4. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

Start tracking your courses and tasks today to stay organized and achieve academic success!
