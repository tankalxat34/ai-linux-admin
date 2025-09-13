# ai-linux-admin
A case study on creating an AI agent for Ubuntu Server administration based on a verbal description of the task

## What is it?
This is a repository where an experiment was conducted to create a full-fledged AI agent that administers Linux servers based on verbal commands. The AI agent was tested on the basis of the `openai/gpt-oss-20b` model, however, in theory, it should work well on the basis of other LLM models.

There are two text files in the [`/prompts`](./prompts/) folder.:
1. [`system.txt `](./prompts/system.txt ) - a system prompt with basic instructions for the agent;
2. [`task.txt `](./prompts/task.txt ) is a verbal description of the task that the model needs to complete.;

## How to use it?
1. Clone this repository;
2. Rename `.env.example` to `.env` and write your parameters to it;
3. Verbally write your Linux server administration task in the file [`task.txt `](./prompts/task.txt ). The more detailed the description, the better the model will cope with the task.;
4. Run `main.py ` and enjoy the process;

Examples of logs of the model working with a task in [`task.txt `](./prompts/task.txt ) are located in the [`example_logs`] directory(./example_logs).