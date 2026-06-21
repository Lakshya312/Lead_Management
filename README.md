# Lead Management System (CRM)

A full-stack Lead Management CRM application built with **Django** and **Microsoft SQL Server** for managing customer leads, tracking sales activities, and generating business analytics.

## Tech Stack

| Layer         | Technology                           |
|---------------|--------------------------------------|
| Backend       | Python 3.x, Django 6.0              |
| REST API      | Django REST Framework 3.17           |
| Database      | Microsoft SQL Server (MSSQL Express) |
| DB Driver     | pyodbc + ODBC Driver 17             |
| ORM Adapter   | mssql-django                         |
| Filtering     | django-filter                        |
| Data Tools    | pandas, openpyxl                     |
| Frontend      | Bootstrap 5.3 + Bootstrap Icons      |
| Admin Panel   | Django Admin                         |

## Project Structure

```
LeadManagementSystem/
├── manage.py                  # Django management entry point
├── requirements.txt           # Python dependencies
├── README.md
├── LICENSE
│
├── lead_crm/                  # Django project configuration
│   ├── settings.py            # Database, apps, middleware, DRF config
│   ├── urls.py                # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── leads/                     # Main Django app
│   ├── models.py              # Data models (Region, Product, Lead, etc.)
│   ├── serializers.py         # DRF serializers with validation
│   ├── views.py               # API ViewSets + Frontend CBVs (CRUD)
│   ├── urls.py                # DRF Router + Frontend URL configuration
│   ├── admin.py               # Django Admin panel configuration
│   ├── forms.py               # Django ModelForms with validation
│   ├── apps.py                # App configuration
│   ├── tests.py               # Unit tests
│   ├── migrations/            # Database migrations
│   └── templates/leads/       # Bootstrap 5 HTML templates
│       ├── dashboard.html
│       ├── region_list.html
│       ├── region_form.html   # Add / Edit (shared)
│       ├── product_list.html
│       ├── product_form.html  # Add / Edit (shared)
│       ├── lead_list.html
│       ├── lead_form.html     # Add / Edit (shared)
│       └── confirm_delete.html
│
├── templates/
│   └── base.html              # Global base layout (Bootstrap 5)
│
├── scripts/                   # Utility scripts
│   ├── bulk_pyodbc_loader.py  # Bulk CSV → MSSQL data loader
│   └── excel_to_csv.py        # Excel → CSV converter
│
├── data/                      # Seed data files (not tracked in git)
│   ├── Product_Lead_Data_Demo.xlsx
│   ├── Lead.csv
│   ├── Lead_Follow_Up.csv
│   └── ... (other CSV files)
│
└── docs/                      # Project documentation
    └── Internship Training Plan_updated PDF_File.pdf
```

## Data Models

The system uses 8 interconnected models:

| Model | DB Table | Description |
|-------|----------|-------------|
| **Region** | `tbl_region_master` | Geographic operational regions (with predefined name choices) |
| **Territory** | `tbl_territory_master` | Sub-regions linked to a Region |
| **ProductCategory** | `tbl_product_category_master` | Product classification categories |
| **Product** | `tbl_product_master` | Products linked to a category, with active/inactive status |
| **LeadSource** | `tbl_lead_source_master` | Origin channels (Website, Referral, etc.) |
| **LeadStatus** | `tbl_lead_status_master` | Pipeline states (New, Contacted, Converted, etc.) |
| **Lead** | `tbl_lead_pipeline` | Core lead entity with contacts, location, and all associations |
| **LeadFollowUp** | `tbl_lead_followup_history` | Follow-up history log for each lead |

## Frontend Pages (Bootstrap 5 UI)

| Page | URL | Features |
|------|-----|---------|
| Dashboard | `/` | Live counts of Leads, Products, Regions |
| Region List | `/regions/` | Search, Add, Edit, Delete with confirmation |
| Region Form | `/regions/add/` `/regions/<id>/edit/` | Dropdown for Region Name, dynamic Add/Edit title |
| Product List | `/products/` | Search, Category filter, Add, Edit, Delete |
| Product Form | `/products/add/` `/products/<id>/edit/` | Category dropdown, Active/Inactive dropdown |
| Lead List | `/leads/` | Search, Region/Status/Product filters, Add, Edit, Delete |
| Lead Form | `/leads/add/` `/leads/<id>/edit/` | Full form with all FK dropdowns, date picker |
| Delete Confirm | (shared) | Safe POST-based delete confirmation for all models |

## REST API Endpoints

All API endpoints are available under `/api/` and support full CRUD operations.
Visit `http://127.0.0.1:8000/api/` for the interactive browsable API.

### Master Data APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/regions/` | List all regions |
| POST | `/api/regions/` | Create a new region |
| GET | `/api/regions/{id}/` | Get region details |
| PUT/PATCH | `/api/regions/{id}/` | Update a region |
| DELETE | `/api/regions/{id}/` | Delete a region |
| GET | `/api/categories/` | List all product categories |
| POST | `/api/categories/` | Create a new category |
| GET | `/api/categories/{id}/` | Get category details |
| PUT/PATCH | `/api/categories/{id}/` | Update a category |
| DELETE | `/api/categories/{id}/` | Delete a category |
| GET | `/api/lead-sources/` | List all lead sources |
| POST | `/api/lead-sources/` | Create a new lead source |
| GET | `/api/lead-statuses/` | List all lead statuses |
| POST | `/api/lead-statuses/` | Create a new lead status |
| GET | `/api/territories/` | List all territories |
| POST | `/api/territories/` | Create a new territory |

### Product API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Create a new product |
| GET | `/api/products/{id}/` | Get product details |
| PUT/PATCH | `/api/products/{id}/` | Update a product |
| DELETE | `/api/products/{id}/` | Delete a product |

**Filters:** `?categoryid=1`, `?is_active=1`
**Search:** `?search=keyword` (searches product name)
**Ordering:** `?ordering=productname` or `?ordering=-productid`

### Lead API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leads/` | List all leads (paginated) |
| POST | `/api/leads/` | Create a new lead |
| GET | `/api/leads/{id}/` | Get lead details with nested relations |
| PUT/PATCH | `/api/leads/{id}/` | Update a lead |
| DELETE | `/api/leads/{id}/` | Delete a lead |

**Filters:** `?regionid=1`, `?statusid=2`, `?leadsourceid=3`, `?productid=4`, `?gender=Male`
**Search:** `?search=keyword` (searches person name, company, email, contact, city)
**Ordering:** `?ordering=personname`, `?ordering=-lead_gen_date`

### Lead Follow-Up API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/follow-ups/` | List all follow-ups |
| POST | `/api/follow-ups/` | Create a new follow-up |
| GET | `/api/follow-ups/{id}/` | Get follow-up details |
| PUT/PATCH | `/api/follow-ups/{id}/` | Update a follow-up |
| DELETE | `/api/follow-ups/{id}/` | Delete a follow-up |

**Filters:** `?leadid=1`, `?leadstatusid=2`, `?executiveid=3`
**Search:** `?search=keyword` (searches action taken, remarks, executive name)

### Pagination

All list endpoints return paginated results (10 per page by default):
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/leads/?page=2",
    "previous": null,
    "results": [...]
}
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Microsoft SQL Server (Express edition works)
- ODBC Driver 17 for SQL Server

### 1. Clone the Repository

```bash
git clone https://github.com/Ankurrao7/LeadManagementSystem.git
cd LeadManagementSystem
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Update `lead_crm/settings.py` with your SQL Server instance details:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'LeadManagementDB_New',
        'HOST': 'localhost\\SQLEXPRESS',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Load Seed Data (Optional)

```bash
python scripts/excel_to_csv.py        # Convert Excel → CSV files
python scripts/bulk_pyodbc_loader.py   # Load CSV data into MSSQL
```

### 7. Create Superuser & Run Server

```bash
python manage.py createsuperuser
python manage.py runserver
```

- **Admin Panel:** `http://127.0.0.1:8000/admin/`
- **API Root:** `http://127.0.0.1:8000/api/`
- **App Home:** `http://127.0.0.1:8000/`

## Development Roadmap

| Week | Focus Area | Deliverables | Status |
|------|------------|--------------|--------|
| 1 | Django setup, Models, Admin, DB connection | 8 models, DB tables, Admin panel registered | ✅ Complete |
| 2 | REST API Development (DRF) & Postman | 8 ViewSets, CRUD endpoints, search/filter/ordering, serializers with validation | ✅ Complete |
| 3 | Frontend UI — Forms, CRUD & Search | Bootstrap 5 UI, Add/Edit/Delete for Region, Product & Lead, search & filter bars, delete confirmation, Bootstrap Icons, dynamic form titles, Region Name dropdown, Active/Inactive dropdown, date picker for leads | ✅ Complete |
| 4 | Dashboard, Analytics, Charts & Exports | Charts (Chart.js), lead pipeline analytics, Excel/CSV export | 🔲 Upcoming |
| 5 | Enhancements & Authentication | User login/logout, role-based access, `added_by` linked to logged-in user | 🔲 Upcoming |
| 6 | Final Review & Presentation | Code cleanup, documentation, demo | 🔲 Upcoming |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
