# GitHub Event Watcher

## Overview

This application streams public events from the GitHub Events API:

```
https://api.github.com/events
```

It filters and stores the following event types:

* `WatchEvent`
* `PullRequestEvent`
* `IssuesEvent`

Collected events are stored in a SQLite database using SQLAlchemy.
The application uses REST endpoints to compute metrics and provide visualizations based on the stored data.

---

# Architecture

* **FastAPI** – REST API
* **SQLAlchemy** – ORM
* **SQLite** – persistent storage
* **Matplotlib (Agg backend)** – visualization

---

# Data Model

### Repo

* `id` (primary key)
* `name`
* `url`

### Event

* `id` (primary key)
* `type`
* `created_at`
* `repo_id` (foreign key → Repo)

---

# Implemented Metrics

## 1. Average Time Between Pull Requests

**Endpoint:**

```
GET /metrics/average-pr-time?repo=<repository_name>
```

Returns the average time, in seconds, between consecutive PullRequestEvents for a given repository.

---

## 2. Event Counts by Type with Offset

**Endpoint:**

```
GET /metrics/event-counts?offset=<minutes>
```

Returns total number of events grouped by type within the last `offset` minutes.

Example:

```
/metrics/event-counts?offset=10
```

Counts events created in the last 10 minutes.

---

## 3. Bonus: Event Activity Visualization

**Endpoint:**

```
GET /metrics/event-activity-chart?offset=<minutes>
```

Returns a PNG chart showing event activity grouped per minute within the given offset.

Provides a visual representation of system activity.

---

# Configuration

Application configuration is stored in `config.py`.

Configurable values include:

* GitHub API URL
* Interested event types
* Polling interval
* Default offsets

---

# Assumptions

1. Only public events from GitHub’s public events API are monitored.
2. The GitHub API rate limit for unauthenticated requests is sufficient for this assignment.
3. Events are stored as received; no deduplication beyond primary key constraint is implemented.

---

# How to Run

## 1. Clone the repository

```
git clone <repository_url>
cd <project_folder>
```

---

## 1.1 (OPTIONAL) Create virtual environment

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

Required packages include:

* fastapi
* uvicorn
* sqlalchemy
* requests
* matplotlib

---

## 4. Run the application

```
cd app
uvicorn main:app
```

Server starts at:

```
http://127.0.0.1:8000
```
