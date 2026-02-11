from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from db import SessionLocal
from models import Event, Repo

def average_time_between_prs(repo_name: str):
    session = SessionLocal()

    prs = (
        session.query(Event.created_at)
        .join(Repo)
        .filter(
            Event.type == "PullRequestEvent",
            Repo.name == repo_name
        )
        .order_by(Event.created_at)
        .all()
    )

    session.close()

    if len(prs) < 2:
        return None

    times = [t[0] for t in prs]

    deltas = [
        (times[i] - times[i - 1]).total_seconds()
        for i in range(1, len(times))
    ]

    return sum(deltas) / len(deltas)

def count_events_by_type(offset_minutes: int):
    session = SessionLocal()

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=offset_minutes)

    results = (
        session.query(Event.type, func.count())
        .filter(Event.created_at >= cutoff)
        .group_by(Event.type)
        .all()
    )

    session.close()

    return {event_type: count for event_type, count in results}