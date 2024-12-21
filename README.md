# RPG NPC Generator

Welcome to the **RPG NPC Generator**, a web application designed to create unique non-player characters (NPCs) for tabletop role-playing games. Built with the Pathfinder 2e ruleset, this tool ensures dynamic and engaging character creation with a focus on simplicity and extensibility.

---

![Axle Labs](https://pbs.twimg.com/profile_banners/1870546961499127808/1734808675/1500x500)

> **Proudly brought to you by [Axle Labs](https://axlelabs.cloud)**  
> [Follow us on Twitter](https://x.com/LabsAxle) for updates and more!

---

## About
The RPG NPC Generator was developed as part of the University of Helsinki’s **Databases & Web Programming Course**. The primary goal was to build a robust character creation tool without relying on heavy client-side UI frameworks. Instead, it leverages minimal technology and the power of large language models, like the ChatGPT API, while integrating advanced database concepts.

This project is proudly developed and maintained by **Axle Labs**, pushing boundaries in creative solutions for gaming and beyond.

---

## How It Works
The generator employs pre-defined character templates stored in `data/character_templates.json`. Here's an overview of the workflow:

1. **Template Initialization:**  
   When the app starts, templates are inserted into the PostgreSQL database.

2. **Character Generation:**  
   Templates are cloned, and stats are randomized to ensure unique attributes and abilities.  
   AI-generated content, powered by the ChatGPT API, enriches the character's details.

3. **Character Gallery:**  
   A gallery feature allows users to browse and view their generated NPCs.

---

## Tech Stack

### Core Technologies
- **Flask:** Lightweight web framework for Python.
- **PostgreSQL:** Open-source relational database.
- **SQLAlchemy:** Python SQL toolkit and ORM library.
- **Alembic:** Database migration tool for SQLAlchemy.
- **Celery:** Distributed task queue framework for asynchronous operations.
- **Redis:** In-memory data structure store.
- **Bulma:** CSS framework for modern UI design.

### Linting, Formatting, and Testing
- **flake8:** Python code linter.
- **isort:** Python import sorter.
- **black:** Python code formatter.
- **djLint:** Linter and formatter for Jinja2 templates.
- **pytest:** Python testing framework.
- **pytest-cov:** Plugin for pytest to generate coverage reports.

---

## Why Flask?

This app was built using Flask to meet course requirements. However, due to IO-heavy operations and the latency of ChatGPT API calls, frameworks like Node.js or Quart would typically be better suited for asynchronous processing.

To mitigate slow IO operations, the project integrates **Celery** for asynchronous task management. This ensures the main application remains responsive by delegating time-consuming tasks to background workers.

---

## Project Structure

```plaintext
├── npcgen           # Main application directory
│   ├── auth         # Authentication related files
│   ├── characters   # Character generation and management files
│   ├── static       # Static files (CSS, JS, images)
│   └── templates    # HTML templates
├── data             # Data directory (character templates, etc.)
├── tests            # Test directory
├── .env.example     # Example environment variable file
├── compose.yml      # Docker Compose configuration file
└── requirements.txt # Python dependencies
