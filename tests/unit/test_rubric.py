from backend.app.scoring.rubric import CandidateScore, DimensionScore

def test_score_validation():
    ds = DimensionScore(score=8.5, justification="Strong match")
    assert ds.score == 8.5

def test_score_out_of_range():
    import pytest
    with pytest.raises(Exception):
        DimensionScore(score=11, justification="Invalid")
