from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer, TextIteratorStreamer
import os
from threading import Thread
import torch
from dotenv import load_dotenv

from apps.livelihood.backend.AI.base_chatbot import BaseChatBot
from apps.livelihood.backend.typing import hugging_face_models

load_dotenv()

class HuggingFaceChatBot(BaseChatBot):

    def __init__(self, model_name: hugging_face_models, token_env_name:Optional[str]=None, prompt:Optional[str]=None) -> None:
        super().__init__()
        if token_env_name:
            token=os.environ[token_env_name]
        else:
            token=None
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

        self.streamer = TextIteratorStreamer(self.tokenizer)

        if prompt:
            self.prompt = prompt
        else:
            self.prompt=""
    
    def add_message(self, message)->str:
        self.prompt += f"\n{message}"
        return self.prompt
            
    def chat(self, message):
        prompt=self.add_message(message=message)
        if torch.cuda.is_available():
            input_ids = self.tokenizer(
                prompt, add_special_tokens=True, return_tensors="pt"
            ).to("cuda")
        else:
            input_ids = self.tokenizer(
                prompt, add_special_tokens=True, return_tensors="pt"
            ).to("cuda")

        generation_kwargs = dict(input_ids, max_new_tokens=512,
            top_p=0.95,
            do_sample=True,
            temperature=0.7,
            use_cache=True,
            streamer=self.streamer)
        
        def streamed_text():
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            generated_text = ""
            for new_text in self.streamer:
                generated_text += new_text
                yield new_text
        return streamed_text()
        

        # tokens = self.model.generate(
        #     input_ids,
        #     max_new_tokens=512,
        #     top_p=0.95,
        #     do_sample=True,
        #     temperature=0.7,
        #     use_cache=True,
        #     streamer=self.streamer,
        # )
        # out = self.tokenizer.decode(
        #     tokens[0][input_ids.shape[1] :], skip_special_tokens=True
        # ).strip()
        # self.update_history(message_to_add=message, identity='system')
        # self.update_history(message_to_add=out, identity='AI')
        #return(tokens)

