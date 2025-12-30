<h1 align="center">Wordfence Exploit Extractor</h1>

THIS PROJECT IS NOT LINKED IN ANY WAY WITH WORDFENCE, IT'S ONLY A TOOL THAT I MADE AND MAINTAINS IN ORDER TO AUTOMATICALLY CHECKS MY WORDPRESS INSTANCES

This project allows users to define **plugin lists per website** in order to stay informed about **newly discovered vulnerabilities** affecting their WordPress environments.

It can also send **push notifications** to administrators using [ntfy](https://ntfy.sh/), allowing different notification channels per website.

---

## ✨ Features

* Monitor WordPress plugin vulnerabilities using the Wordfence Intelligence API
* Define **different plugin lists per website**
* Filter vulnerabilities by:

  * patch status
  * minimum severity level
  * publication date
* Send notifications per site via **ntfy**
* Fully configurable using a single `config.ini` file
* Designed for automation (cron-friendly, logging support)

---

## 📦 Installation

As with most Python projects, this tool relies on a virtual environment.

### Using `venv`

```bash
# On Linux
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Using `uv` (optional)

You can also use [uv](https://docs.astral.sh/uv/) as a faster alternative:

```bash
uv sync
```

---

## ⚙️ Configuration

All configuration is done via the `config.ini` file located at the root of the project.

The file allows you to:

* define monitored websites
* associate plugin lists with each site
* configure notification endpoints
* tune vulnerability filters (severity, patched status, time range)

Refer directly to the `config.ini` file for detailed documentation and examples.

---

## ▶️ Execution

To run the program:

```bash
# From the project root
.venv/bin/python3 main.py
```

This command can safely be used in a cron job or scheduled task.

---

## 📝 Logging

The application uses Python’s built-in logging system and can log both to the console and to a file, making it suitable for long-running or automated executions.

---

## 👤 Author

* [Romb38](https://github.com/Romb38)
