from schemas import (Coordinate, OptimizeRequest, OptimizeResponse, Route, Step, Summary, UnassignedJob)


def to_lnglat(point: Coordinate) -> list[float]:
    # VROOM and OSRM want [long, lat], the opposit of Google Maps
    return [point.lng, point.lat]

def to_coordinate(lnglat: list[float]) -> Coordinate:
    return Coordinate(lat=lnglat[1], lng=lnglat[0])

def to_vroom(problem: OptimizeRequest) -> dict:
    vehicles = []
    for v in problem.vehicles:
        vehicle = {
            "id": v.id,
            "profile": "car",
            "start": to_lnglat(v.start),
            "capacity": [v.capacity],
        }
        if v.end is not None:
            vehicle["end"] = to_lnglat(v.end)
        vehicles.append(vehicle)

    jobs = [{"id":j.id, "location": to_lnglat(j.location), "delivery":[j.delivery]}
            for j in problem.jobs
    ]

    return {"vehicles": vehicles, "jobs": jobs, "options": {"g": True}}

def from_vroom(answer: dict) -> OptimizeResponse:
    routes=[]
    for r in answer["routes"]:
        steps = [
            Step(
                type=s["type"],
                job_id=s.get("id"),
                location=to_coordinate(s["location"]),
                arrival=s["arrival"],
                load=s["load"][0],
            )
            for s in r["steps"]
        ]
        routes.append(
            Route(
                vehicle_id=r["vehicle"],
                steps=steps,
                duration=r["duration"],
                distance=r["distance"],
                geometry=r["geometry"],
            )
        )

    unassigned = [
        UnassignedJob(job_id=u["id"], location=to_coordinate(u["location"]))
        for u in answer["unassigned"]
    ]

    summary = Summary(
        duration=answer["summary"]["duration"],
        distance=answer["summary"]["distance"],
    )

    return OptimizeResponse(routes=routes, unassigned=unassigned, summary=summary)