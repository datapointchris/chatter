# Chatter

## Description

Chatter is based on the streamlit example, but with the added benefit of saving the chats in `JSON` format to the `~/Documents` directory which is automatically synced in `iCloud` which allows for sharing chats between Apple devices that share the same `iCloud`.

Another feature is the ability to create and save multiple chats, instead of one long running chat.  This is more similar to the actual ChatGPT interface.

This project saves money as it takes a lot of prompting to use $20 of credits each month, this project is currently using $5 / month with full time use on two computers.

OpenAI model can easily be changed in `app.py` under `OPENAI_MODEL` global.

Finally, included is `chatter.rb` and `reinstall.sh` which is a brew formula for installing this project as a brew service, and a handy script to install/reinstall the project when the source code changes.
This allows for the app to be started upon login automatically.
