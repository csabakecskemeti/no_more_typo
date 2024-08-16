# pip install --upgrade pyperclip pynput langchain langchain-openai langchain-community langchain-core
import pyperclip
from pynput import keyboard
from langchain_community.llms.openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import warnings

print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                                                              ║
║ ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄   ║
║▐░░▌      ▐░▌▐░░░░░░░░░░░▌     ▐░░▌     ▐░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  ║
║▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀█░▌     ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀       ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌  ║
║▐░▌▐░▌    ▐░▌▐░▌       ▐░▌     ▐░▌▐░▌ ▐░▌▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌                    ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌  ║
║▐░▌ ▐░▌   ▐░▌▐░▌       ▐░▌     ▐░▌ ▐░▐░▌ ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄           ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌  ║
║▐░▌  ▐░▌  ▐░▌▐░▌       ▐░▌     ▐░▌  ▐░▌  ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌          ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌  ║
║▐░▌   ▐░▌ ▐░▌▐░▌       ▐░▌     ▐░▌   ▀   ▐░▌▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀           ▐░▌      ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌  ║
║▐░▌    ▐░▌▐░▌▐░▌       ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌                    ▐░▌          ▐░▌     ▐░▌          ▐░▌       ▐░▌  ║
║▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄           ▐░▌          ▐░▌     ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌  ║
║▐░▌      ▐░░▌▐░░░░░░░░░░░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌          ▐░▌          ▐░▌     ▐░▌          ▐░░░░░░░░░░░▌  ║
║ ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀            ▀            ▀       ▀            ▀▀▀▀▀▀▀▀▀▀▀   ║
║                                                                                                                                              ║
║                                                                                                                                              ║
║  Small utility that uses LLM to fix typos and syntax on the text stored in the clipboard.                                                    ║
║                                                                                                                                              ║
║  LLM api_key should be available in the OPENAI_API_KEY environment variable.                                                                 ║
║                                                                                                                                              ║
║  Activate fix: [ctrl]+[shift]+[z]                                                                                                            ║
║  Exit app: [ctrl]+[shift]+[x]                                                                                                                ║
║                                                                                                                                              ║
║  2024 devquasar.com                                                                                                                          ║
║                                                                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
""")


# Suppress all warnings
warnings.filterwarnings("ignore")

llm = OpenAI()

prompt_template = PromptTemplate.from_template(
    "Fix the syntax and typos text:\n\n{text}\n\nThe correct string is:"
)
chain = LLMChain(llm=llm, prompt=prompt_template)


def clean_string(text):
    # Strip leading and trailing whitespace
    cleaned_text = text.strip()
    # Strip leading and trailing quotes
    cleaned_text = cleaned_text.strip('"').strip("'")
    return cleaned_text


def on_activate():
    original_clipboard_content = pyperclip.paste()
    # processed_content = f(original_clipboard_content, llm, prompt_template)
    processed_content = clean_string(chain.run(original_clipboard_content))
    pyperclip.copy(processed_content)


def on_exit():
    print("Exit no_more_typo app...")
    exit()
    

with keyboard.GlobalHotKeys(
    {
        '<ctrl>+<shift>+z': on_activate,
        '<ctrl>+<shift>+x': on_exit
    }
) as h:
    h.join()