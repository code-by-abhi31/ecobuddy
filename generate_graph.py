from agents import ecobuddy_graph

# Render the LangGraph structure to a PNG file using Mermaid
try:
    png_data = ecobuddy_graph.get_graph().draw_mermaid_png()
    with open("architecture.png", "wb") as f:
        f.write(png_data)
    print("SUCCESS: 'architecture.png' has been generated in your project folder.")
except Exception as e:
    print(f"FAILED to generate image: {e}")
    print("Tip: If the API drawer fails, you can print the Mermaid text instead:")
    print(ecobuddy_graph.get_graph().draw_mermaid())