# no_more_typo
![logo](https://github.com/csabakecskemeti/no_more_typo/blob/main/no_more_typo.jpg)

Small utility that uses LLM to fix typos and syntax errors in the text stored in the clipboard.

## Run executable 
You can run the code without setting up a pyton environment. 
To do that use the executable in dist folder.
You still need the LLM api key (optionally the custom base url) set up in the environment variables.

## Environment

### Required packages
`pip install --upgrade pyperclip pynput langchain langchain-openai langchain-community langchain-core`

### Access and credential
LLM api_key should be available in the `OPENAI_API_KEY` environment variable.

Also set `OPENAI_API_BASE` if needed

## Run
I suggest to run it in the background: `python no_more_typo.py&`

## Use
Activate fix: [ctrl]+[shift]+[z]

Exit app: [ctrl]+[shift]+[x]              
