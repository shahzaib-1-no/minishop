# 🛒 Django E-Commerce Website – MiniShop

A scalable and feature-rich E-Commerce platform built using Django and MySQL. Includes a complete product catalog, shopping cart, order management system, and a powerful admin dashboard.

---

## 📸 Admin Dashboard Screenshots

| Dashboard Home | Order List | Order Detail | Product List |
|:--------------:|:----------:|:------------:|:------------:|
| ![Home](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/dashboard_home.png) | ![Orders](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/order_list_dashboard.png) | ![Detail](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/order_detail_dashboard.png) | ![Products](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/product_list_dashboard.png) |

---

## 📸 LandingPage Screenshots

| Landign Page | Cart Page | Checkout Page | Shop Detail | Shop Page |
|:------------:|:---------:|:-------------:|:-----------:|:---------:|
| ![Landing Page](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/landing_page.png) | ![Cart Page](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/cart_page.png) | ![Checkout Page](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/checkout_page.png) | ![Shop Detail ](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/shop_detail_page.png) | ![Shop Page](https://github.com/shahzaib-1-no/minishop/blob/8d53d3d9a8e04636c3ac9efc1481eac87f2bfae0/minishop_images/shop_page.png) |

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
5. **Optional: Seed Fake Data**.
You can auto-generate sample products and orders for testing.
-Generate 200 Products:
   ```bash
   python manage.py seed_products
- Generate 6 Orders:
  ```bash
  python manage.py seed_orders
## 🧾 Frontend Template Attribution
The frontend design of this project is based on the free template  
**"MiniShop – Bootstrap 4 eCommerce Template"** by **Colorlib / ThemeWagon**.  
🔗 [View Template](https://themewagon.com/themes/free-bootstrap-4-html5-responsive-ecommerce-website-template-minishop/)

🛠️ **License**: Open Source | Free for Commercial Use | Lifetime Free Updates  
📌 **Attribution**: Footer attribution may be required depending on author terms.

We are using this template in accordance with ThemeWagon’s free template license policy.  
Redistribution of the template alone is not permitted.
