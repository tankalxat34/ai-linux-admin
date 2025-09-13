import paramiko  
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

from utils import actions

load_dotenv()

SETTINGS: str = json.loads(actions.readFile("./settings.json"))
SYSTEM_PROMPT: str = actions.readFile("./prompts/system.txt")
TASK: str = actions.readFile("./prompts/task.txt")

client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE_URL"),
    api_key=os.getenv("OPENAI_API_API_KEY")
)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(os.getenv("SSH_TARGETHOST"), username=os.getenv("SSH_USERNAME"), password=os.getenv("SSH_PASSWORD"))

ssh_username            = actions.sshCommand(ssh, "whoami")
ssh_hostname            = actions.sshCommand(ssh, "hostname")
ssh_host_configuration  = actions.sshCommand(ssh, "uname -a")

print(ssh_host_configuration)
print("Connected via SSH as ", ssh_username, "@", ssh_hostname, sep="")
print("-" * 20)

FINAL_SYSTEM_PROMPT = f"""{SYSTEM_PROMPT}

You are connected as {ssh_username}@{ssh_hostname}
System configuration: {ssh_host_configuration}
""".replace("%TASK%", TASK)

messages: list[dict[str, str]] = [
    actions.message("system", FINAL_SYSTEM_PROMPT)
]

assistant_reply: str = ""
while True:
    try:
        completion = client.chat.completions.create(
            messages=messages,
            **SETTINGS["completitionSettings"]
        )

        assistant_reply: str = str(completion.choices[0].message.content).strip()

        assistant_reply = actions.replaceAll(assistant_reply, {
            "<|channel|>commentary to=assistant": "",
            "{": "",
            "}": ""
        }).split("\n")[0]

        print(f"[{actions.currentTime()}, assistant]", assistant_reply)

        messages.append(actions.message("assistant", assistant_reply))

        if SETTINGS["endtaskSignal"] in assistant_reply:
            print(f"Got signal from model `{SETTINGS["endtaskSignal"]}`")
            actions.endtaskCallback(messages)

        if "sudo" in assistant_reply:
            linux_reply = actions.sshSudoCommand(ssh, assistant_reply, os.getenv("SSH_SUDO_PASSWORD"))
        else:
            linux_reply = actions.sshCommand(ssh, assistant_reply)

        if not bool(linux_reply):
            linux_reply = SETTINGS["emptyUserMessage"]

        print(f"[{actions.currentTime()}, linux]", linux_reply, end="\n\n")
        messages.append(actions.message("user", linux_reply))
    
    except Exception as e:
        print("Ошибка", e, f"{e.with_traceback()}")
        actions.endtaskCallback(messages)