# import modules
import gradio as gr
import openai
import random
import time
import os

# Read API key from the text file
with open("api_key.txt", "r") as f:
    api_key = f.read().strip()

# Set the API key
openai.api_key = api_key

# create specialized chatGPT role: Rowdy Mascot
chat_log = [{"role": "system", "content": "You are a Buddhist Monk. Your purpose is to be a teacher and give Buhddist advice to people. Keep answers to 100 tokens"}]

with gr.Blocks() as chat:
    #image = gr.Image()
    
    #img = gr.Image("https://upload.wikimedia.org/wikipedia/commons/b/bf/Dharma_Wheel_%282%29.svg", show_label=False)
    #img = gr.Image("https://i.imgur.com/SBVa06e.pngg", show_label=False)
    chatbot = gr.Chatbot(label="Monk")
    msg = gr.Textbox(label="You")
    clear = gr.Button("Clear chat")
    def user(user_message, history):
        chat_log.append({"role": "user", "content": user_message})
        return "", history + [[user_message, None]]

    def bot(history):
        
        response = openai.ChatCompletion.create(
        
        # Selects the chat model
            model="gpt-3.5-turbo",
            
            # Pass the message dictionary
            messages = chat_log
        )
        
        chat_log.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
        
        #bot_message = random.choice(["Yes", "No"])
        history[-1][1] = response["choices"][0]["message"]["content"]
        time.sleep(1)
        #print(history[-1][0])
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

chat.launch()

