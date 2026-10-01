from schemas import Coordinate, OptimizeRequest
def to_lnglat(point: Coordinate) -> list[float]:
    # VROOM and OSRM want [long, lat], the opposit of Google Maps
    return [point.lng, point.lat]

def to_vroom(problem: OptimizeRequest) -> dict:
    vehicles = []
    for v in problem.vehicles:
        vehicle = {"id": v.id,
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

    return {"vehicles": vehicles, "jobs": jobs}