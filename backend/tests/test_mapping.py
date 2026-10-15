from schemas import OptimizeRequest
from vroom import from_vroom, to_vroom

def test_to_vroom_flips_coordinates(problem):
    payload = to_vroom(OptimizeRequest.model_validate(problem))

    assert payload["jobs"][0]["location"] == [7.4197, 43.7311]
    assert payload["vehicles"][0]["start"] == [7.4246, 43.7384]

def test_to_vroom_wraps_amounts_in_lists(problem):
    payload = to_vroom(OptimizeRequest.model_validate(problem))

    assert payload["vehicles"][0]["capacity"] == [30]
    assert payload["jobs"][0]["delivery"] == [10]

def test_to_vroom_leaves_out_a_missing_end(problem):
    del problem["vehicles"][0]["end"]

    payload = to_vroom(OptimizeRequest.model_validate(problem))

    assert "end" not in payload["vehicles"][0]

def test_from_vroom_converts_back_to_our_format(vroom_answer):
    result = from_vroom(vroom_answer)

    start, job, end = result.routes[0].steps
    assert start.job_id is None
    assert job.job_id == 1
    assert job.location.lat == 43.7311
    assert job.location.lng == 7.4197
    assert job.load == 0
    assert result.unassigned[0].job_id == 2
    assert result.summary.distance == 1000