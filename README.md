# Stock Manager

A complete, local stock management application built with Python and Flask, designed for tracking product inventory. This app is packaged as a simple desktop `.exe` with a GUI launcher, making it easy for anyone to run.

This project was built to manage the inventory for an underwear business, handling stock in both "dozens" and "pieces."

## 📸 Screenshots

*(This is where you should add your own screenshots!)*




---

## ✨ Features

* **GUI Launcher:** A simple window shows server status and provides an "Open in Browser" button. Closing the window automatically stops the server.
* **Main Dashboard:** At-a-glance view of total stock, total product variants, and a "Low Stock" warning list.
* **Stock Graph:** The dashboard includes a bar chart (using Chart.js) that visually groups your total stock by product style (e.g., "Boxer" vs. "Brief").
* **Inventory Management:** A full CRUD (Create, Read, Update, Delete) system for all your products.
* **Flexible Stock Input:** Add or update stock using "Dozens" and "Pieces" fields, which are automatically calculated into a total.
* **Advanced Search:** A powerful search bar on the inventory page allows filtering by **Name, Style, Color, or Size**.
* **Autocomplete Suggestions:** The search bar provides autocomplete suggestions based on the products already in your database.
* **Reliable Data Entry:** A dropdown menu for product sizes (F/M, L, XL, etc.) prevents typos.
* **Safe Database Storage:** The app automatically creates its database in the user's `AppData` folder, preventing permissions errors after installation.
* **Installer Ready:** The project includes an Inno Setup script to create a professional Windows installer.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, native JavaScript
* **Database:** SQLite
* **Server:** Waitress (for production)
* **GUI:** Tkinter (for the launcher)
* **Charting:** Chart.js
* **Packaging:** PyInstaller
* **Installer:** Inno Setup

---

## 🚀 How to Run (For Developers)

1.  Clone the repository:
    ```bash
    git clone [https://github.com/ImmyLikeYou/Stock.git](https://github.com/ImmyLikeYou/Stock.git)
    cd Stock
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  Install the required packages:
    ```bash
    pip install Flask waitress pyinstaller
    ```
4.  Run the application using the GUI launcher:
    ```bash
    python run_gui.py
    ```
