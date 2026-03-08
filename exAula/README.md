# 🚗 Car Stand Management CLI

A modular **Command Line Interface (CLI)** application built with **Python**, **Typer**, and **uv** for managing a small car stand inventory.

This tool allows users to create, list, search, update, and delete cars stored in a local JSON database.
It demonstrates clean architecture principles by separating the CLI interface, business logic, and data handling into different layers.

---

# 📌 Features

* Create cars in the stand
* List all registered cars
* Search cars using filters
* Update existing cars
* Delete cars
* Error-handled CLI commands
* JSON-based persistence
* Clean modular architecture

---

# 🧠 Project Architecture

The project follows a **layered architecture**:

```
src/
│
├── main.py                # CLI commands (Typer interface)
│
├── services/
│   ├── car_service.py     # Business logic
│   └── utils.py           # Utility functions (JSON handling, error handler)
│
├── data/
│   └── models.py          # Data models (Car dataclass)
│
stand/
└── index_stand.json       # JSON storage for cars
```

### Layers

| Layer         | Responsibility                              |
| ------------- | ------------------------------------------- |
| CLI           | Handles user input and commands using Typer |
| Service Layer | Contains the business logic                 |
| Data Layer    | Defines data models                         |

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/backend-i.git
cd backend-i
cd exAula
```

Install dependencies using **uv**:

```bash
uv sync
```

Run the CLI:

```bash
uv run python src/main.py --help
```

---

# 🚀 Usage

## Create a car

```bash
python src/main.py create-car AA-11-BB BMW 25000 12-02-2024
```

Example output:

```
Car 'AA-11-BB' created successfully
```

---

## List all cars

```bash
python src/main.py list-cars
```

Example output:

```
🚗 Cars in Stand

#   Registration     Model        Price
-----------------------------------------
1   AA-11-BB         BMW          25000€
```

---

## Search cars

You can filter using:

* registration
* model
* minimum price
* maximum price

Example:

```bash
python src/main.py search-cars --model BMW
```

Example with price range:

```bash
python src/main.py search-cars --min-price 20000 --max-price 30000
```

---

## Update a car

```bash
python src/main.py update-car AA-11-BB --price 27000
```

---

## Delete a car

```bash
python src/main.py delete-car AA-11-BB
```

---

# ⚠️ Error Handling

All CLI commands use a centralized error handler that catches and displays user-friendly error messages.

Example:

```
❌ Car with registration 'AA-11-BB' already exists
```

---

# 🧩 Technologies Used

* Python
* Typer — CLI framework
* uv — dependency management
* JSON — data persistence
* Dataclasses — data modeling

---

# 🎯 Learning Goals

This project demonstrates:

* CLI application development
* Modular project structure
* Separation of concerns
* Data persistence with JSON
* Error handling in CLI tools
* Clean Python architecture

---

# 📜 License

This project was developed for the **Backend-I course** as part of a CLI application exercise.
