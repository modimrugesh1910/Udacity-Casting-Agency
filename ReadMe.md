## Casting Agency API

### Motivation

This API allows a casting agency to manage movies and actors. Users with specific roles (Assistant, Director, Executive Producer) can perform CRUD operations depending on their permissions. This project was built to demonstrate knowledge of RESTful API development, role-based access control (RBAC), Flask, SQLAlchemy, Auth0, and test-driven development.

---

## 🔗 Live API

[https://udacity-casting-agency-lj4k.onrender.com/](https://udacity-casting-agency-lj4k.onrender.com/)

---

## 🧪 Getting Started

### 🔧 Project Dependencies

* Python 3.13
* Flask
* SQLAlchemy
* psycopg\[binary]
* Gunicorn
* Flask-CORS
* Flask-JWT-Extended
* Authlib or PyJWT (depending on your implementation)
* Unittest or pytest for testing

### 💻 Local Development Setup

1. Clone the repo:

```bash
git clone https://github.com/modimrugesh1910/Udacity-Casting-Agency.git
cd casting-agency
```

2. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
source setup.sh
```

5. Seed the Database (Optional but recommended)

```bash
python seed.py
```

5. Start the server:

```bash
export FLASK_APP=app.py
flask run
```

---


## 🔐 Authentication (Auth0)

This API uses Auth0 for authentication & RBAC.

### ✳️ Roles & Permissions

| Role               | Permissions                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| Casting Assistant  | `get:actors`, `get:movies`                                                 |
| Casting Director   | All above + `post:actors`, `patch:actors`, `delete:actors`, `patch:movies` |
| Executive Producer | All above + `post:movies`, `delete:movies`                                 |

---

## 🔑 Setup Auth0 Locally

1. Create a `.env` file or use the provided `setup.sh`.
2. Get your JWT tokens from your Auth0 tenant.
3. Attach the token to API requests:

```bash
curl -H "Authorization: Bearer <your_token>" \
     https://udacity-casting-agency-lj4k.onrender.com/actors
```

---

## 📑 API Endpoints

All responses are JSON.

### GET /actors

* **Permissions**: `get:actors`
* **Returns**: list of actors

### POST /actors

* **Permissions**: `post:actors`
* **Payload**: `{ "name": "Tom", "age": 30, "gender": "Male" }`

### PATCH /actors/<id>

* **Permissions**: `patch:actors`
* **Payload**: any updatable fields

### DELETE /actors/<id>

* **Permissions**: `delete:actors`

Similar structure applies to `/movies`.

---

## Testing

To run tests:

```bash
python test_app.py
```

Tests include:

* Success & failure for each endpoint
* RBAC test cases for:

  * Assistant (read-only)
  * Director (actor management)
  * Executive Producer (movie management)

---

## 📁 File Structure

```
├── app.py
├── models.py
├── auth.py
├── requirements.txt
├── setup.sh
├── test_app.py
├── seed.py
└── README.md
```

---

