from pydantic import BaseModel, Field, model_validator

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