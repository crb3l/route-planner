from pydantic import BaseModel, Field, model_validator
from typing import Literal
class Coordinate(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)

class Job(BaseModel):
    id: int = Field(ge=0)
    location: Coordinate
    delivery: int = Field(default=0, ge=0)

class Vehicle(BaseModel):
    id: int = Field(ge=0)
    start: Coordinate
    end: Coordinate | None = None
    capacity: int = Field(ge=0)

class OptimizeRequest(BaseModel):
    vehicles: list[Vehicle] = Field(min_length=1)
    jobs: list[Job] = Field(min_length=1)

    @model_validator(mode="after")
    def check_unique_job_ids(self):
        ids = [job.id for job in self.jobs]
        if len(ids) != len(set(ids)):
            raise ValueError("Job IDs must be unique!")
        return self

    @model_validator(mode="after")
    def check_unique_behicle_ids(self):
        ids = [vehicle.id for vehicle in self.vehicles]
        if len(ids) != len(set(ids)):
            raise ValueError("Vehicle IDs must be unique!")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
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
                        {"id": 2, "location": {"lat": 43.7275, "lng": 7.4150}, "delivery": 15},
                        {"id": 3, "location": {"lat": 43.7440, "lng": 7.4300}, "delivery": 90},
                    ],
                }
            ]
        }
    }

class Step(BaseModel):
    type: Literal["start", "job", "end"]
    job_id: int | None = None # only "job" steps have one
    location: Coordinate
    arrival: int # seconds since vehicle left its start
    load: int # what is still in the vehicle after this step

class Route(BaseModel):
    vehicle_id: int
    steps: list[Step]
    duration: int # seconds of driving
    distance: int # metres
    geometry: str # the road line, encoded

class UnassignedJob(BaseModel):
    job_id: int
    location: Coordinate

class Summary(BaseModel):
    duration: int
    distance: int

class OptimizeResponse(BaseModel):
    routes: list[Route]
    unassigned: list[UnassignedJob]
    summary: Summary