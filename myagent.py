"""Primer prototipo del Data Steward: personalidad definida en un prompt JSON."""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


PROMPT_PATH = Path(__file__).with_name("myagent_prompt.json")


def main() -> None:
    # Carga las variables del archivo .env
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Probá la personalidad del Data Steward."
    )

    parser.add_argument(
        "consulta",
        nargs="?",
        default="Hola. ¿Quién sos y cómo me podés ayudar con mis datos?",
        help="Consulta para el agente; escribila entre comillas.",
    )

    args = parser.parse_args()

    # Cargar el prompt JSON
    prompt_config = json.loads(
        PROMPT_PATH.read_text(encoding="utf-8")
    )

    # Modelo de OpenAI
    llm = ChatOpenAI(
        model="gpt-6-luna"
    )

    # Crear agente
    myagent = create_agent(
        model=llm,
        tools=[],
        system_prompt=json.dumps(
            prompt_config,
            ensure_ascii=False,
            indent=2,
        ),
    )

    # Ejecutar consulta
    result = myagent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": args.consulta,
                }
            ]
        }
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()