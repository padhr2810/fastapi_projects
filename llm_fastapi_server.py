
import contextlib
import os
import time 

from fastapi import Depends, FastAPI
from pydantic import BaseModel
import torch 
import transformers 


#############################  PREDICTION ENDPOINT:

class PromptInput(BaseModel):
    text: str

class ResponseOutput(BaseModel):
    resp: str

class LlmModel:

    def load_model(self) -> None:
        """Loads the model"""
        MODEL_NAME = "falcon-7b-instruct"
        hw = "cuda:0"
        hw = "cpu" 
        model =  transformers.AutoModelForCausalLM.from_pretrained(
            MODEL_NAME , 
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            ).to(hw)
        tokenizer = transformers.AutoTokenizer.from_pretrained(MODEL_NAME)

    async def predict(self, prompt: PromptInput) -> ResponseOutput:
        """Runs a prediction"""
        if not self.model:
            raise RuntimeError("Model is not loaded")
        
        prompt = prompt.replace("_", " ")

        tokenized_prompt_example = tokenizer(prompt, return_tensors='pt').to("cuda:0")
        outputs = model.generate(tokenized_prompt_example["input_ids"].to(hardware)  , max_new_tokens=150, do_sample=False, top_k=5, top_p=0.95)
        answer = tokenizer.batch_decode( outputs, skip_special_tokens=True)
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
