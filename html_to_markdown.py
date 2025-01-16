from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel

 
def create_prompt(
    text: str, tokenizer=None, instruction: str = None, schema: str = None
) -> str:
    """
    Create a prompt for the model with optional instruction and JSON schema.
    """
    if not instruction:
        instruction = "Extract the main content from the given HTML and convert it to Markdown format."
    if schema:
        instruction = "Extract the specified information from a list of news threads and present it in a structured JSON format."
        prompt = f"{instruction}\n```html\n{text}\n```\nThe JSON schema is as follows:```json\n{schema}\n```"
    else:
        prompt = f"{instruction}\n```html\n{text}\n```"

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    

def convert_html_to_markdown_v2(html_content: str) -> str:
    # import torch
    # device = "cuda" if torch.cuda.is_available() else "cpu"

    model_name = "jinaai/ReaderLM-v2"
    device = "cpu"  # or "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    # model = AutoModel.from_pretrained(model_name).to(device)

    # Construct the prompt for HTML to Markdown conversion
    prompt = create_prompt(html_content, tokenizer)
    
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        inputs,
        max_new_tokens=1024,
        temperature=0,
        do_sample=False,
        repetition_penalty=1.08,
        pad_token_id=tokenizer.eos_token_id
    )
    
    markdown_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the generated markdown part after the prompt
    if "Markdown:" in markdown_output:
        markdown_output = markdown_output.split("Markdown:")[1].strip()
    
    return markdown_output

def convert_html_to_markdown(html_content: str) -> str:
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    device = "cuda"
    model_name = "jinaai/reader-lm-1.5b"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    
    messages = [{"role": "user", "content": html_content}]
    input_text = tokenizer.apply_chat_template(messages, tokenize=False)
    
    inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
    outputs = model.generate(inputs, max_new_tokens=1024, temperature=0, do_sample=False, repetition_penalty=1.08)
    
    return tokenizer.decode(outputs[0])
