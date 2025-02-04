from typing import Optional, Union, Literal
from abc import ABC, abstractmethod
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

class BaseChatBot(ABC):
    """
    Skeleton chatbot, that allows you to plug in any supported AI API
    Currently supported AI APIs:
     HuggingFace CausalLM
    """

    def __init__(self, text_generation_api: Union[AutoModelForCausalLM], tokenizer_api:Union[AutoTokenizer], token: Optional[str]):
        """
        Params:
         text_generation_api - Any API that takes in a text, runs shows ML and returns text
         tokenizer_api - API to tokenize
         token: token to access model
        """
        self._history:list[dict[str,str]] = []
        if type(text_generation_api) == AutoModelForCausalLM:
            self.init_auto_model_for_causal_lm(text_generation_api, tokenizer_api, token)
            return True
        else:
            pass

    @property
    def history(self):
        return self._history
    @property
    def history_head(self,index:int):
        return self._history[index:]
    @property
    def history_tail(self, index:int):
        return self._history[:index]
    
    @abstractmethod
    def chat(args, kwargs):
        pass

    def update_history(self, message_to_add:str, identity:Literal['AI', 'human', 'system']):
        history_item = {identity:message_to_add}
        self._history.append(history_item)
        return self._history
    
        
        


        