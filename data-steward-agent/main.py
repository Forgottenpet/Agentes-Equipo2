from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from prompts import DATA_STEWARD_PROMPT
from tools import validate_data_quality, get_dataset_statistics




# Modelo elegido: Gemini


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# Crear agente con dos herramientas
agent = create_agent(
    model=llm,
    tools=[
        validate_data_quality,
        get_dataset_statistics
    ],
    system_prompt=DATA_STEWARD_PROMPT
)


# Solicitud de prueba
user_request = """
Perform a complete data quality assessment of clientes.csv.
Identify missing values and duplicate records.
Calculate descriptive statistics.
Use the available tools and provide recommendations.
"""


print("\n=== DATA STEWARD AGENT ===\n")

result = agent.invoke({
    "messages": [
        {"role": "user", "content": user_request}
    ]
})


# Mostrar herramientas realmente utilizadas
print("\n=== TOOL CALLS ===")

for message in result["messages"]:
    if getattr(message, "tool_calls", None):
        for call in message.tool_calls:
            print(f"Tool called: {call['name']}")
            print(f"Arguments: {call['args']}")

    if message.type == "tool":
        print(f"Tool result ({message.name}): {message.content}")



print("\n=== INFORME DEL DATA STEWARD ===\n")

respuesta = result["messages"][-1].content

if isinstance(respuesta, list):
    for bloque in respuesta:
        if isinstance(bloque, dict) and bloque.get("type") == "text":
            print(bloque["text"])
else:
    print(respuesta)

