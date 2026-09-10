import os
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# Using the compound-mini model built for chaining agents with higher rate limits
llm = ChatGroq(
    model="groq/compound-mini",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0.2
)

class AgentState(TypedDict):
    user_query: str
    route_decision: str
    impact_data: str
    alternatives: str
    gamification_update: str
    final_output: str

def router_node(state: AgentState):
    prompt = f"Evaluate input: '{state['user_query']}'. If it's a physical product, respond EXACTLY with 'PRODUCT'. Otherwise, respond 'INVALID'. Nothing else."
    res = llm.invoke([SystemMessage(content="Strict validation judge."), HumanMessage(content=prompt)], max_tokens=10)
    decision = res.content.strip().upper()
    if "PRODUCT" not in decision: decision = "INVALID"
    return {"route_decision": decision}

def error_node(state: AgentState):
    output = "🚫 **Invalid Input.** I analyze physical products. Please enter an item (e.g., 'plastic bottle')."
    return {"final_output": output, "impact_data": "N/A", "alternatives": "N/A", "gamification_update": "N/A"}

def impact_agent(state: AgentState):
    prompt = f"Analyze the environmental footprint of: {state['user_query']}. STRICTLY 3 short sentences. NO TABLES."
    res = llm.invoke([SystemMessage(content="Environmental Impact Analyst."), HumanMessage(content=prompt)], max_tokens=150)
    return {"impact_data": res.content.strip()}

def coach_agent(state: AgentState):
    prompt = f"Given this impact: {state['impact_data']}, recommend 2 affordable eco-friendly alternatives in short bullet points. NO TABLES."
    res = llm.invoke([SystemMessage(content="Sustainable Lifestyle Coach."), HumanMessage(content=prompt)], max_tokens=150)
    return {"alternatives": res.content.strip()}

def roi_agent(state: AgentState):
    prompt = f"""
    User queried: '{state['user_query']}'.
    Alternatives suggested: {state['alternatives']}.
    
    Calculate the 1-year financial savings (in INR) of switching from the conventional item to the reusable alternative.
    Format EXACTLY as:
    - **Estimated Annual Cost (Current):** ₹[Amount]
    - **Estimated Annual Cost (Alternative):** ₹[Amount]
    - **Total 1-Year Savings:** ₹[Amount]
    
    Add one final sentence putting this savings into perspective for a 19-year-old engineering student living in Chennai. (e.g. mention how many months of an MTC student bus pass or theater movie tickets this could cover). Keep it punchy.
    """
    res = llm.invoke([SystemMessage(content="Financial ROI Analyst."), HumanMessage(content=prompt)], max_tokens=200)
    return {"gamification_update": res.content.strip()}

def synthesizer(state: AgentState):
    output = (
        f"### 🔍 Environmental Impact\n{state['impact_data']}\n\n"
        f"### 🌿 Sustainable Alternatives\n{state['alternatives']}\n\n"
        f"### 💰 Financial ROI (1-Year Savings)\n{state['gamification_update']}"
    )
    return {"final_output": output}

def route_decision(state: AgentState) -> Literal["impact", "error"]:
    return "impact" if state["route_decision"] == "PRODUCT" else "error"

builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("error", error_node)
builder.add_node("impact", impact_agent)
builder.add_node("coach", coach_agent)
builder.add_node("roi", roi_agent)
builder.add_node("synthesize", synthesizer)

builder.set_entry_point("router")
builder.add_conditional_edges("router", route_decision, {"impact": "impact", "error": "error"})

builder.add_edge("impact", "coach")
builder.add_edge("coach", "roi")
builder.add_edge("roi", "synthesize")
builder.add_edge("synthesize", END)
builder.add_edge("error", END)

ecobuddy_graph = builder.compile()