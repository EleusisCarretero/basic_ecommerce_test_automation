# Base E-commerce Test Automation

This project contains end-to-end automated tests for the [SauceDemo](https://www.saucedemo.com) e-commerce site, developed using Selenium and Pytest.

## Features Covered
- Login tests (valid and invalid credentials).
- Navigation through product categories.
- Complete purchase flow.
- Negative tests (error handling and validations).

## Project Structure
The project follows a modular design with the Page Object Model (POM) pattern:
base_ecommerce_test_automation/ ├── pages/ │ ├── base_page.py # Common methods (click, input, waits, etc.) │ ├── login_page.py # Elements and methods for the login page │ ├── home_page.py # Elements and methods for the home page │ ├── product_page.py # Elements and methods for the product page │ └── checkout_page.py # Elements and methods for the checkout process ├── tests/ │ ├── test_login.py # Login-related tests │ ├── test_navigation.py # Navigation tests │ ├── test_cart.py # Shopping cart tests │ └── test_checkout.py # Checkout process tests ├── utils/ │ ├── config.py # Project configuration (URLs, credentials) │ ├── browser_manager.py # Driver and browser setup │ └── logger.py # Logging utilities ├── requirements.txt # Project dependencies ├── pytest.ini # Pytest configuration └── README.md # Project documentation


## How to Get Started
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/base_ecommerce_test_automation.git
2.  Install dependencies:
  bash
  Copy code
  pip install -r requirements.txt
