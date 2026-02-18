# TradeHub - Investment Portfolio Management Application

A comprehensive Django REST Framework application for tracking and managing personal investment portfolios across multiple asset categories including cryptocurrency, stocks, bonds, and real estate.

## 📋 Features

- **Multi-Asset Portfolio Tracking**: Track cryptocurrencies, stocks, bonds, and real estate investments
- **Transaction Logging**: Complete buy/sell transaction history for each asset
- **Real-time Portfolio Value**: Current USD valuation and cost basis tracking
- **User Authentication**: Secure user account management and data privacy
- **REST API**: Full-featured REST API for programmatic access with token authentication
- **Admin Dashboard**: Django admin interface for data management
- **Responsive Web Interface**: User-friendly portfolio management interface
- **Automatic Average Cost Calculation**: Calculates cost basis automatically from transaction logs
- **Transaction Charts**: Visual representation of trading history and costs

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-rest-finance-app.git
   cd django-rest-finance-app
   ```

2. **Create a virtual environment**
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment configuration**
   ```bash
   cp .env.example .env
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data (optional)**
   ```bash
   python seed_production_data.py
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver 8001
   ```

## 🌐 Quick Access

### Web Interface
- **Homepage**: http://127.0.0.1:8001/
- **Login**: http://127.0.0.1:8001/account/login/
- **Admin**: http://127.0.0.1:8001/admin/

### Portfolio Pages (Authenticated Users)
- **Crypto**: http://127.0.0.1:8001/assets/crypto/
- **Stocks**: http://127.0.0.1:8001/assets/stocks/
- **Bonds**: http://127.0.0.1:8001/assets/bonds/
- **Real Estate**: http://127.0.0.1:8001/assets/real-estate/

### REST API
- **Categories**: `/api/categories/`
- **Assets**: `/api/assets/`
- **Auth Token**: `/api/api-token-auth/` (POST with username/password)  
  Example URL: `/api/crypto/assets/`

- **Asset Details and Transaction Logs**:  
  `/api/<category_slug>/assets/<asset_slug>/`  
  Lists details and transaction logs for the specified asset under the specified category.  
  Example URL: `/api/crypto/assets/yyizuhvhayrwxjp/`

### POST (Create) URLs
- **Create an Asset in a Category**:  
  `/api/<category_slug>/assets/create/`  
  Creates an asset with the name sent in a POST request in the specified category.  
  Example URL: `/api/crypto/assets/create/`

    Example Request Body: `{"name":"test"}`

- **Add a Transaction to an Asset**:  
  `/api/<category_slug>/assets/<asset_slug>/transaction/`  
  Adds a new transaction (buy or sell) to the specified asset in the specified category. The transaction is recorded directly in the database, and the asset data is updated.

  Example Request Body: `{"amount":213123.123, "cost":12350, "transaction_type":"buy"}` (Cost data optional, if its not provided it will be processed as 0)

### DELETE URLs
- **Delete a Specific Transaction**:  
  `/api/<category_slug>/assets/<asset_slug>/transaction/delete/<transaction_id>/`  
  Deletes the transaction with the specified `transaction_id` for the asset in the specified category using an HTTP Delete Request. No data needs to be sent in the request body, just an authentication token.

  Example Delete Request URI: `/api/crypto/assets/xfunnlzmlmtnckr/delete/2/` - To get transaction ID you can check asset detail response. In asset detail request's response you can see all transactions and their IDs.

- **Delete an Asset**:  
  `/api/<slug:category_slug>/assets/<slug:asset_slug>/delete/`  
  Permanently deletes the specified asset from the specified category using an HTTP Delete Request.

    Example Delete Request URI: `/api/crypto/assets/xfunnlzmlmtnckr/delete/` - Permanently deletes the asset with slug 'xfunnlzmlmtnckr'

## Limitations
- Users need to register to use the app. In order to use the REST API, the token information of the user whose asset information will be worked on is needed.

## Getting Started

To get started with this project, follow these steps:

**Step 1**: Clone the project
```bash
git clone https://github.com/oskaygunacar/django-finance-app.git
```

**Step 2**: Navigate to the directory
```bash
cd django-finance-app
```

**Step 3**: Create and activate a virtual environment
```bash
# Create
python -m venv env

# Activate for MacOS & Linux
source env/bin/activate

# Activate for Windows
env\Scripts\activate
```

**Step 4**: Install dependencies
```bash
pip install -r requirements.txt
```
**Step 5**: Configure Settings.py Database Configurations

**If you are planning to use PostgreSQL or other databases, please configure the Settings.py database config first.**

**Step 6**: Migrate the database and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

**Step 7**: Run the server
```bash
python manage.py runserver
```

## Usage

- Navigate to the site URL to create an account and login to site.
- After login process, you are free to create/log any amount of asset and asset transaction.

## Contributing

Contributions to improve the project are welcome. Please follow the standard fork-and-pull request workflow.


## App Images:
### Homepage
![Homepage](./assets/images/homepage.png)
### Homepage Authenticated
![Homepage Authenticated](./assets/images/homepage-authenticated.png)
### Login Page of the App
![Login page](./assets/images/login.png)
### Signup Page of the App
![Signup page](./assets/images/signup.png)
### Profile Actions on Site Navbar
![Profile Actions](./assets/images/profile-actions.png)
### Asset Category Dashboard
![Asset Category Dashboard](./assets/images/asset-category-dashboard.png)
### Add New Asset Transaction Page
![Add New Asset Transaction](./assets/images/add-new-asset-transaction.png)
### Asset Detail / Dashboard
![Asset Detail / Dashboard](./assets/images/asset-dashboard-detail.png)
### API Token Landing Page
![API Token Landing Page](./assets/images/api-token-landing-page.png)