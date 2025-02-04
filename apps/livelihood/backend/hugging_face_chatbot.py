from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
import os
import torch
from dotenv import load_dotenv

from backend.base_chatbot import BaseChatBot

load_dotenv()

class HuggingFaceChatBot(BaseChatBot):

    def __init__(self, model_name, token_env_name:str, prompt:bool=False) -> None:
        token=os.environ[token_env_name]
        if torch.cuda.is_available():
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, trust_remote_code=True, torch_dtype=torch.bfloat16,token=token
            ).to("cuda")
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, trust_remote_code=True, torch_dtype=torch.bfloat16,token=token
            )


        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True, torch_dtype=torch.bfloat16, token=token
        )

        self.streamer = TextStreamer(self.tokenizer)

        if prompt:
            self.prompt = """
            Summarize this persons incomes and expenses and provide finacial advice for him
            """
        else:
            self.prompt=""
    
    def add_message(self, message)->str:
        self.prompt += f"\n{message}"
        return self.prompt
            
    def chat(self, message):
        # Time to chat! We'll use the tokenizer to translate our text into a language the model understands
        prompt=self.add_message(message=message)
        if torch.cuda.is_available():
            input_ids = self.tokenizer.encode(
                prompt, add_special_tokens=True, return_tensors="pt"
            ).to("cuda")
        else:
            input_ids = self.tokenizer.encode(
                prompt, add_special_tokens=True, return_tensors="pt"
            ).to("cuda")

        tokens = self.model.generate(
            input_ids,
            max_new_tokens=512,
            top_p=0.95,
            do_sample=True,
            temperature=0.7,
            use_cache=True,
            streamer=self.streamer,
        )
        out = self.tokenizer.decode(
            tokens[0][input_ids.shape[1] :], skip_special_tokens=True
        ).strip()
        self.update_history(message_to_add=message, identity='system')
        self.update_history(message_to_add=out, identity='AI')

