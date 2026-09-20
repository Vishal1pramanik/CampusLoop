CampusLoop 🎓
Student-to-Student Campus Marketplace

CampusLoop is a Django-based student marketplace designed to help students discover, buy, sell, and exchange useful items within their campus community.

The platform provides a simple way for students to browse listings, view item details, and contact sellers directly through the platform.

🌐 Live Website

CampusLoop:
https://campus-loop-opal.vercel.app/

✨ Features
👤 Student Registration
🔐 User Login & Authentication
🛍️ Create Item Listings
🔎 Search and Filter Listings
📚 Browse Items by Category
📱 View Detailed Item Information
👤 View Seller Information
💬 Contact Seller
🏷️ Item Condition & Exchange Type
💰 Item Price
🛠️ Django Admin Panel
🗄️ Database-backed Marketplace
🔄 How CampusLoop Works
Create Account
      ↓
     Login
      ↓
Browse Categories
      ↓
Search / Filter Items
      ↓
View Item Details
      ↓
Contact Seller
      ↓
Complete Exchange

CampusLoop focuses on making student-to-student exchanges simple and accessible within the campus community.

📂 Project Structure
CAMPUSLOOP/
│
├── campusloop/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── templates/
│   │   └── core/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md

The exact structure may vary depending on the current version of the project.

🛠️ Technologies Used
Technology	Purpose
Python	Programming Language
Django	Web Framework
HTML	Page Structure
CSS	Styling
JavaScript	Client-side Interaction
SQLite / Database	Data Storage
Git & GitHub	Version Control
🚀 Installation & Setup
1. Clone the Repository
git clone YOUR_GITHUB_REPOSITORY_URL
2. Open the Project
cd CAMPUSLOOP
3. Create a Virtual Environment
python -m venv .venv
4. Activate the Virtual Environment

Windows:

.venv\Scripts\activate
5. Install Dependencies
pip install -r requirements.txt

If a requirements.txt file is not available, install Django:

pip install django
6. Apply Database Migrations
python manage.py migrate
7. Create an Admin Account
python manage.py createsuperuser

Follow the instructions shown in the terminal.

8. Start the Development Server
python manage.py runserver

Open the website:

http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/
🖥️ Main Pages
Home

Introduces CampusLoop and provides access to the marketplace.

Registration

Students can create an account to access the platform.

Login

Registered users can log in to their CampusLoop account.

Listings

Users can browse available marketplace items and use search/filter options.

Item Details

Users can view information such as:

Item name
Description
Category
Condition
Exchange type
Price
Seller
Contact Seller

Logged-in users can contact the seller regarding an item.

📸 Website Screenshots

Add screenshots of the actual website here to showcase the project.

Recommended screenshots:

Home Page
Registration Page
Login Page
Browse Listings
Item Details
Contact Seller
Django Admin Panel

🎯 Project Objective

The main objective of CampusLoop is to create a digital marketplace specifically for students where they can:

Find useful items
Sell unused items
Discover affordable resources
Connect with other students
Complete exchanges within the campus community
🔮 Future Scope

The following features can be added in future versions:

Student verification
Ratings and reviews
Request / "I Need" feature
Reporting system
Borrow and Give options
Smart item matching
Contribution score
Improved notifications
Advanced marketplace analytics

These features are considered future scope and are not represented as current implemented functionality.

💡 Digital Economy

CampusLoop demonstrates how a digital platform can connect students within a local campus ecosystem.

Student
   ↓
Digital Marketplace
   ↓
Item Discovery
   ↓
Student Connection
   ↓
Campus Exchange

The platform encourages the reuse and exchange of existing resources within the student community.

🔐 Security

The project uses Django's built-in authentication and security features.

For production deployment:

Keep secret keys private
Use environment variables
Disable Django debug mode
Configure allowed hosts
Use a production database
Configure secure HTTPS settings

Never upload your .env file, passwords, API keys, or secret keys to GitHub.

👨‍💻 Developer

Vishal Pramanik

BCA – Digital Business

📄 Project Status

Current Status: Working Django Web Application

CampusLoop is currently focused on its core student marketplace experience, with additional trust, matching, and monetization features planned for future development.

⭐ Acknowledgement

This project was developed as part of an academic/project-based learning experience to understand web development, Django, database-driven applications, authentication, and digital marketplace concepts.

CampusLoop

Connect • Reuse • Exchange
