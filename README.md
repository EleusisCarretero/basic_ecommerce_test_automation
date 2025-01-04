# Base E-commerce Test Automation

This project contains end-to-end automated tests for the [SauceDemo](https://www.saucedemo.com) e-commerce site, developed using Selenium and Pytest.

## Features Covered

- **Login Tests**:
  - Valid login with correct credentials.
  - Error handling for invalid credentials.
- **Navigation Tests**:
  - Access and validation of product categories.
  - Correct display of product filters.
- **Complete Purchase Flow**:
  - Adding products to the cart.
  - Completing the checkout process.
- **Negative Tests**:
  - Validation of error messages for incomplete forms.
  - Handling attempts to purchase without items in the cart.

## Project Structure

```
base_ecommerce_test_automation/
├── pages/
│   ├── base_page.py        # Common methods (click, input, waits, etc.)
│   ├── login_page.py       # Elements and methods for the login page
│   ├── home_page.py        # Elements and methods for the home page
│   ├── product_page.py     # Elements and methods for the product page
│   └── checkout_page.py    # Elements and methods for the checkout process
├── tests/
│   ├── test_input/         # inputs files
|       └── source_demo.yaml       
│   ├── test_login.py       # Login-related tests
│   ├── test_navigation.py  # Navigation tests
│   ├── test_cart.py        # Shopping cart tests
│   └── test_checkout.py    # Checkout process tests
├── utils/
│   ├── config.py           # Project configuration (URLs, credentials)
│   ├── browser_manager.py  # Driver and browser setup
│   ├── logger_manager.py   # Logging utilities
│   ├── result_manager.py   # Assertion utilities
|   └── tools.py            # Common tools
├── requirements.txt        # Project dependencies
├── conftest.py             # conftest pytest file
├── pytest.ini              # Pytest configuration
└── README.md               # Project documentation
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EleusisCarretero/basic_ecommerce_test_automation.git
   cd basic_ecommerce_test_automation
   ```

2. **Create and activate a virtual environment**:
   - On **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

To execute all tests, use the following command:

```bash
pytest
```

To generate an HTML report:

```bash
pytest --html=report.html
```

## Prerequisites

- **Python 3.8 or higher**: Ensure Python is installed. You can verify the version with `python --version` or `python3 --version`.
- **Google Chrome**: Browser used for the tests.
- **Chromedriver**: Compatible with your version of Chrome. [Download here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Future Enhancements

- Integration with GitHub Actions for CI/CD.
- Support for multiple browsers (Chrome, Firefox, etc.).
- Improved data handling with parameterized tests.

## Contact

For questions or suggestions, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/tu-perfil) or [email](mailto:tu-email@example.com).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy testing! 🚀
