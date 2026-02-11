import io
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse

from db import SessionLocal
from models import Event
from config import INTEREST

def generate_event_activity_chart(offset_minutes: int):
    session = SessionLocal()

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=offset_minutes)

    events = (
        session.query(Event.type, Event.created_at)
        .filter(Event.created_at >= cutoff)
        .all()
    )

    session.close()

    # Group by minute bucket
    buckets = defaultdict(lambda: defaultdict(int))

    for event_type, created_at in events:
        minute = created_at.replace(second=0, microsecond=0)
        buckets[minute][event_type] += 1

    # Sort time axis
    sorted_minutes = sorted(buckets.keys())

    plt.figure()

    for event_type in INTEREST:
        counts = [
            buckets[minute].get(event_type, 0)
            for minute in sorted_minutes
        ]
        plt.plot(sorted_minutes, counts, label=event_type)

    plt.xlabel("Time")
    plt.ylabel("Number of Events")
    plt.title(f"Event Activity (Last {offset_minutes} Minutes)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")