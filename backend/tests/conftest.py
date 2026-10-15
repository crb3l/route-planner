import pytest


@pytest.fixture
def problem():
    # A request in OUR format: one truck, two jobs. Job 2 is too heavy for the truck
    return {
        "vehicles": [
            {
                "id": 1,
                "start": {"lat": 43.7384, "lng": 7.4246},
                "end": {"lat": 43.7384, "lng": 7.4246},
                "capacity": 30,
            }
        ],
        "jobs": [
            {"id": 1, "location": {"lat": 43.7311, "lng": 7.4197}, "delivery": 10},
            {"id": 2, "location": {"lat": 43.7440, "lng": 7.4300}, "delivery": 90},
        ],
    }

@pytest.fixture
def vroom_answer():
    # A made-up answer in VROOM's format, with only the fields from_vroom reads.
    return {
        "code": 0,
        "summary": {"duration": 100, "distance": 1000},
        "unassigned": [{"id": 2, "location": [7.4300, 43.7440]}],
        "routes": [
            {
                "vehicle": 1,
                "duration": 100,
                "distance": 1000,
                "geometry": "abc",
                "steps": [
                    {"type": "start", "location": [7.4246, 43.7384], "arrival": 0, "load": [10]},
                    {"type": "job", "id": 1, "location": [7.4197, 43.7311], "arrival": 50, "load": [0]},
                    {"type": "end", "location": [7.4246, 43.7384], "arrival": 100, "load": [0]},
                ],
            }
        ],
    }