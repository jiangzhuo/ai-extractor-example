# pip install transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
checkpoint = "jinaai/reader-lm-1.5b"

import transformers

print(f"transformers version: {transformers.__version__}")
    

device = "cpu" # for GPU usage or "cpu" for CPU usage
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

# example html content
html_content = "<html><body><h1>Hello, world!</h1></body></html>"

messages = [{"role": "user", "content": html_content}]
input_text=tokenizer.apply_chat_template(messages, tokenize=False)

# print(input_text)

inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=1024, temperature=0, do_sample=False, repetition_penalty=1.08)
print(outputs)
print(tokenizer.decode(outputs[0]))