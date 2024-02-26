
import contextlib
import json
import os
import time 

from fastapi import Depends, FastAPI
from pydantic import BaseModel
import torch 
import transformers 


#############################  PREDICTION ENDPOINT:

class PromptInput(BaseModel):
    text: str         ##### Thus, 'text' is field name in JSON data from client.

class ResponseOutput(BaseModel):
    resp: str

class LlmModel:

    def load_model(self) -> None:
        """Loads the model"""
        MODEL_NAME = "falcon-7b-instruct"
        #hw = "cuda:0"
        hw = "cpu" 
        model =  transformers.AutoModelForCausalLM.from_pretrained(
            MODEL_NAME , 
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            ).to(hw)
        tokenizer = transformers.AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = model 
        self.tokenizer = tokenizer 
        self.hw = hw

    async def predict(self, prompt: PromptInput) -> ResponseOutput:
        """Runs a prediction"""
        print(f"type of prompt = {type(prompt)}")
        print(f"prompt = {prompt}")
        print(f"prompt json = {prompt.json() }")
        prompt_json = prompt.json() 

        print(f"type of prompt_json = {type(prompt_json)}")
        prompt_json = json.loads(prompt_json)
        print(f"prompt_json['text'] = {prompt_json['text']}")
        prompt = prompt_json['text']
        prompt = prompt.replace("_", " ")
        print(f"prompt = {prompt}")
        tokenized_prompt_example = self.tokenizer(prompt, return_tensors='pt').to(self.hw)
        outputs = self.model.generate(tokenized_prompt_example["input_ids"].to(self.hw)  , max_new_tokens=150, do_sample=False, top_k=5, top_p=0.95)
        answer = self.tokenizer.batch_decode( outputs, skip_special_tokens=True)
        ## print(answer[0].rstrip() )
        response =  answer[0].rstrip()
        
        return response


llm_model = LlmModel()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    llm_model.load_model()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/prediction")
async def prediction(
    output: ResponseOutput = Depends(llm_model.predict),
        ) -> ResponseOutput:
    return output
