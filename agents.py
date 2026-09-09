import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Initialize Groq Llama 3.3
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.environ.get("GROQ_API_KEY"))

class AgentState(TypedDict):
    user_query: str
    impact_data: str
    alternatives: str
    gamification_update: str
    final_output: str

def impact_agent(state: AgentState):
    prompt = f"Analyze the environmental impact, recyclability, and footprint of: {state['user_query']}. Be concise."
    res = llm.invoke([SystemMessage(content="You are an Environmental Impact Analyst."), HumanMessage(content=prompt)])
    return {"impact_data": res.content}

def coach_agent(state: AgentState):
    prompt = f"Given this product analysis: {state['impact_data']}, recommend 2 affordable, practical eco-friendly alternatives."
    res = llm.invoke([SystemMessage(content="You are a Sustainable Lifestyle Coach."), HumanMessage(content=prompt)])
    return {"alternatives": res.content}

def gamification_agent(state: AgentState):
    prompt = f"Award 10 Eco-Points for logging '{state['user_query']}'. Create a short 1-line motivating challenge related to this."
    res = llm.invoke([SystemMessage(content="You are a Gamification Manager."), HumanMessage(content=prompt)])
    return {"gamification_update": res.content}

def synthesizer(state: AgentState):
    output = (
        f"### 🔍 Environmental Impact\n{state['impact_data']}\n\n"
        f"### 🌿 Sustainable Alternatives\n{state['alternatives']}\n\n"
        f"### 🏆 Challenge & Points\n{state['gamification_update']}"
    )
    return {"final_output": output}

# Build the Graph Architecture
builder = StateGraph(AgentState)
builder.add_node("impact", impact_agent)
builder.add_node("coach", coach_agent)
builder.add_node("gamify", gamification_agent)
builder.add_node("synthesize", synthesizer)

builder.set_entry_point("impact")
builder.add_edge("impact", "coach")
builder.add_edge("coach", "gamify")
builder.add_edge("gamify", "synthesize")
builder.add_edge("synthesize", END)

ecobuddy_graph = builder.compile()