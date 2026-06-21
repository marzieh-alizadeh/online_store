# Online Store

This project is a small and functional online store application developed in **Python**. It features a Graphical User Interface (GUI) and uses CSV files as its database to store information about users, products, orders, and comments. The project is designed with a **Service-Oriented Architecture** to make it easy to maintain and extend.

---

## Features

The application supports two main user roles, each with a specific set of permissions and features:

### Customer Features
*   **Registration and Login:** Create a new user account (passwords are securely hashed using the SHA-256 algorithm).
*   **Browse and Search Products:** View the list of available products and search for specific items.
*   **Shopping Cart Management:**
    *   Add products to the shopping cart.
    *   View the cart and calculate the total price.
    *   Decrease the quantity of an item or remove it completely from the cart.
    *   Clear the entire shopping cart.
*   **Wallet and Checkout:** Add funds to the account balance and finalize purchases by deducting the cost from the wallet.
*   **Comment System:** Write comments for any product and view comments left by other users, along with their submission dates.

### Admin Features
*   **Product Management:** Add new products, edit the details of existing ones, and manage stock levels.
*   **Discount System:** Apply discounts to products.
*   **Order Management:** View a complete list of all orders placed by customers.
*   **Reporting:** Generate sales reports based on different products.

---

## Technologies & Architecture
*   **Programming Language:** Python 3.x
*   **Data Storage:** `CSV` files (no need for external databases like MySQL).
*   **Security:** Uses the `hashlib` module for secure password hashing.
*   **User Interface:** Implemented with separate forms for different sections like login, admin panel, store, and cart.
*   **Architecture:** The application's logic is separated into `models`, `services`, `ui`, and `data` layers.

---

## Project Structure
```text
online_store/
│
├── data/                  # Directory for database files
│   ├── users.csv          # User and admin information
│   ├── products.csv       # Product list and details
│   ├── orders.csv         # Order history
│   └── comments.csv       # User comments on products
│
├── models/                # Data model classes
│   ├── user.py            # Base User class and its children, Customer and Admin
│   └── product.py         # Product class
│
├── services/              # Core logic and business processes
│   ├── auth_service.py    # Authentication service (login/register)
│   ├── product_service.py # Product management service
│   ├── cart_service.py    # In-memory shopping cart service
│   ├── order_service.py   # Order placement and management service
│   ├── comment_service.py # Service for adding and retrieving comments
│   └── file_manager.py    # Utility class for reading/writing CSV files
│
├── ui/                    # User interface files
│   ├── login_window.py    # Login and registration window
│   ├── store_window.py    # Main store window (for customers)
│   ├── admin_panel.py     # Admin management panel
│   ├── cart_window.py     # Shopping cart window
│   ├── style.py           # Styles and appearance settings
│   └── utils.py           # UI helper functions
│
└── main.py                # Entry point for running the application

---

## Installation and Setup

1.  First, make sure you have [Python](https://www.python.org/downloads/) version 3.7 or higher installed on your system.

2.  Download or clone the project repository:

```bash
    git clone https://github.com/yourusername/online_store.git
    cd online_store
