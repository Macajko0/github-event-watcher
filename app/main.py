import threading
from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from collector import run_collector
from metrics import average_time_between_prs, count_events_by_type
from visualization import generate_event_activity_chart

app = FastAPI(title="GitHub Event Monitor")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting collector thread...")

    collector_thread = threading.Thread(
        target=run_collector,
        daemon=True
    )
    collector_thread.start()

    yield

    print("Shutting down...")


app = FastAPI(
    title="GitHub Event Monitor",
    lifespan=lifespan
)


@app.get("/metrics/average-pr-time")
def get_average_pr_time(repo: str = Query(...)):
    avg = average_time_between_prs(repo)
    return {
        "repository": repo,
        "average_time_seconds": avg
    }

@app.get("/metrics/event-counts")
def get_event_counts(offset: int = Query(..., gt=0)):
    return {
        "offset_minutes": offset,
        "counts": count_events_by_type(offset)
    }

@app.get("/metrics/event-activity-chart")
def get_event_activity_chart(offset: int = Query(..., gt=0)):
    return generate_event_activity_chart(offset)