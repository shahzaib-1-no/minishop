# 🛒 Django E-Commerce Website – MiniShop

A scalable and feature-rich E-Commerce platform built using Django and MySQL. Includes a complete product catalog, shopping cart, order management system, and a powerful admin dashboard.

---

## 📸 Dashboard Screenshots

| Dashboard Home | Order List | Order Detail | Product List |
|:--------------:|:----------:|:------------:|:------------:|
| ![Home](https://github.com/shahzaib-1-no/minishop/blob/010b9b57cb756bbd49d65526f0fc08de831a29c4/dashboard_home.png) | ![Orders](https://github.com/shahzaib-1-no/minishop/blob/6e2deeaa6516eeb1df665a8b8065c57c7f65ed39/order_list_dashboard.png) | ![Detail](https://github.com/shahzaib-1-no/minishop/blob/fa629a889613ef9f0131eaebce6d0250e3e7d4b4/order_detail_dashboard.png) | ![Products](https://github.com/shahzaib-1-no/minishop/blob/fa629a889613ef9f0131eaebce6d0250e3e7d4b4/product_list_dashboard.png) |

---

## 🚀 Key Features

- 🔐 User Authentication (Signup, Login, Logout)
- 🛍️ Product Listings with Categories & Filtering
- 📦 Product Detail Pages
- 🛒 Shopping Cart
- 💳 Checkout System
- 📜 Order History & Status
- 🧑‍💼 Admin Dashboard for Product & Order Management
- 📱 Responsive UI (Bootstrap-based)

---

## 🛠️ Tech Stack

| Layer       | Technology                   |
|-------------|-------------------------------|
| Backend     | Django (Python)              |
| Frontend    | HTML, CSS, Bootstrap, jQuery |
| Database    | MySQL                        |
| Authentication | Django Auth              |
| Payment     | Stripe *(Add your Secret Key in `.env` or settings)*

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shahzaib-1-no/minishop.git
   cd minishop
2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # For Windows
   # source venv/bin/activate   # For Linux/macOS
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **Apply Migrations & Run Server**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
5. **Optional: Seed Fake Data**
   You can auto-generate sample products and orders for testing.
   -Generate 200 Products:
   ```bash
   python manage.py seed_products
  - Generate 6 Orders:
  ```bash
  python manage.py seed_orders


   

