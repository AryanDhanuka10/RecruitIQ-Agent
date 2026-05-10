"""
Master orchestrator — chains: JD Parser → Profile Parser → Scorer
Uses LangGraph StateGraph.
"""
import operator
from typing import TypedDict, List, Annotated, Optional
from langgraph.graph import StateGraph, END
from backend.app.parsers.jd_parser import parse_jd
from backend.app.parsers.resume_parser import parse_resume
from backend.app.scoring.engine import score_candidate

class AgentState(TypedDict):
    jd_text: str
    resume_paths: List[str]
    parsed_jd: Optional[dict]
    parsed_resumes: List[dict]
    scored_candidates: List[dict]
    retries: int

def parse_jd_node(state: AgentState):
    print("Agent: Parsing JD...")
    parsed_jd = parse_jd(state["jd_text"])
    return {"parsed_jd": parsed_jd}

def parse_profiles_node(state: AgentState):
    print(f"Agent: Parsing {len(state['resume_paths'])} profiles...")
    parsed_resumes = []
    for path in state["resume_paths"]:
        try:
            parsed = parse_resume(path)
            parsed["file_path"] = path
            parsed_resumes.append(parsed)
        except Exception as e:
            print(f"Error parsing {path}: {e}")
    return {"parsed_resumes": parsed_resumes}

def score_candidates_node(state: AgentState):
    print("Agent: Scoring candidates...")
    scored = []
    # Keep existing high-confidence scores
    existing_scores = {c["candidate_id"]: c for c in state.get("scored_candidates", []) if c["confidence"] >= 0.6}
    
    for resume in state["parsed_resumes"]:
        candidate_id = resume.get("name", "Unknown")
        if candidate_id in existing_scores:
            scored.append(existing_scores[candidate_id])
        else:
            score = score_candidate(state["parsed_jd"], resume)
            if score:
                scored.append(score)
            
    # Sort by weighted total descending
    scored.sort(key=lambda x: x.get("weighted_total", 0), reverse=True)
    
    return {
        "scored_candidates": scored,
        "retries": state.get("retries", 0) + 1
    }

def check_confidence(state: AgentState):
    low_confidence = any(c.get("confidence", 1.0) < 0.6 for c in state["scored_candidates"])
    if low_confidence and state.get("retries", 0) < 2:
        print("Agent: Low confidence detected. Retrying scoring...")
        return "retry"
    return "end"

# Build Graph
graph_builder = StateGraph(AgentState)

graph_builder.add_node("parse_jd", parse_jd_node)
graph_builder.add_node("parse_profiles", parse_profiles_node)
graph_builder.add_node("score_candidates", score_candidates_node)

graph_builder.add_edge("parse_jd", "parse_profiles")
graph_builder.add_edge("parse_profiles", "score_candidates")

graph_builder.add_conditional_edges(
    "score_candidates",
    check_confidence,
    {
        "retry": "score_candidates",
        "end": END
    }
)

graph_builder.set_entry_point("parse_jd")
orchestrator_app = graph_builder.compile()
