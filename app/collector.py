import requests
import time
from datetime import datetime
from db import SessionLocal, engine
from models import Event, Repo, Base
from config import GITHUB_EVENTS_URL, INTEREST, POLL_INTERVAL

Base.metadata.create_all(engine)

def fetch_events():
    response = requests.get(
        GITHUB_EVENTS_URL,
        headers={"Accept": "application/vnd.github+json"}
    )
    response.raise_for_status()
    return response.json()

def store_events(raw_events):
    session = SessionLocal()

    for e in raw_events:
        if e["type"] not in INTEREST:
            continue

        repo_id = str(e["repo"]["id"])

        repo = Repo(
            id=repo_id,
            name=e["repo"]["name"],
            url=e["repo"]["url"]
        )

        session.merge(repo)

        event = Event(
            id=e["id"],
            type=e["type"],
            created_at=datetime.fromisoformat(
                e["created_at"].replace("Z", "+00:00")
            ),
            repo_id=repo_id
        )

        session.merge(event)

    session.commit()
    session.close()

def run_collector(poll_interval=POLL_INTERVAL):
    while True:
        try:
            events = fetch_events()
            store_events(events)
        except Exception as e:
            print("Collector error:", e)

        time.sleep(poll_interval)