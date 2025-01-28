import os
import sys
from enum import StrEnum

import streamlit as st
from dotenv import load_dotenv
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from openai import OpenAI
from openai.types.chat import ChatCompletion

message_history = []


class CharacterName(StrEnum):
    TOBIAS = "tobias"
    GOB = "g.o.b"
    MICHAEL = "michael"
    LINDSAY = "lindsay"
    BUSTER = "buster"
    LUCILLE = "lucille"
    MAEBY = "maeby"
    GEORGE_MICHAEL = "george michael"
    NARRATOR = "narrator"
    GEORGE_SENIOR = "george senior"


load_dotenv()


class OpenAIWrapper:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_chat_response(self, prompts):
        response: ChatCompletion = self.client.chat.completions.create(
            model="gpt-4-turbo", messages=prompts
        )
        return response.choices[0].message.content


openAIClient = OpenAIWrapper()


def load_text(character_name: CharacterName):
    for filename in os.listdir("transcripts"):
        x = []
        with open("transcripts/" + filename, "r") as f:
            x.append(f.readlines())
            # for line in f.readlines():
            # if line.startswith(f"{ character_name }:"):
            # x.append(line)
    return "\n".join(["\n".join(_) for _ in x])


def get_response(character, question):
    system: str = f"""
Use the transcripts from the show below to get yourself into character. Your job is to answer the user's question like you are { character }.
Don't use context from the show. Instead, learn the character's mannerisms and use artistic license to answer.
Keep the answers funny, witty, and ironic if possible.

Lines:
    { text }

"""

    return openAIClient.get_chat_response(
        [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": f"""Hello { character }, I have a question for you. {question}""",
            },
        ]
    )


text = load_text(CharacterName.TOBIAS)

st.write("\nTobias Funke Bot")

character = st.selectbox(
    "Character: ",
    (
        "Narrator",
        "Lucille",
        "Buster",
        "George Michael",
        "Michael",
        "G.O.B",
        "Maeby",
        "Lindsay",
        "Annyong",
        "George, Sr.",
    ),
)
question = st.text_input("What do you want to ask?")
get_gpt = st.button("Ask GPT")


if question != "":
    res = get_response(character, question)
    print(res)
    if res:
        st.write(res)
