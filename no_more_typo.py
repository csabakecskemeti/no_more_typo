# pip install --upgrade pyperclip pynput langchain langchain-openai langchain-community langchain-core
import pyperclip
from pynput import keyboard
from langchain_community.llms.openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnableLambda
import sys
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
║  To use custom prompt template export it to the NO_MORE_TYPO_PROMPT_TEMPLATE environment variable                                            ║
║       The default value is: "Fix the syntax and typos text:\\n\\n{text}\\n\\nThe correct string is:"                                         ║
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

# Load the prompt template from an environment variable or use the default
default_prompt = "Fix the syntax and typos text:\n\n{text}\n\nThe correct string is:"
custom_prompt = os.getenv("NO_MORE_TYPO_PROMPT_TEMPLATE", default_prompt)

# Ensure the template includes "{text}"
if "{text}" not in custom_prompt:
    custom_prompt += "\n CONTEXT: \n {text}"

prompt = PromptTemplate.from_template(custom_prompt)

cleanup = RunnableLambda(
    lambda x: x.strip().strip('"').strip("'")
)

no_typo_chain = prompt | llm | cleanup


def on_activate():
    original_clipboard_content = pyperclip.paste()
    processed_content = no_typo_chain.invoke(original_clipboard_content)
    pyperclip.copy(processed_content)


def on_exit():
    print("Exit no_more_typo app...")
    sys.exit(0)
    

with keyboard.GlobalHotKeys(
    {
        '<ctrl>+<shift>+z': on_activate,
        '<ctrl>+<shift>+x': on_exit
    }
) as h:
    h.join()
