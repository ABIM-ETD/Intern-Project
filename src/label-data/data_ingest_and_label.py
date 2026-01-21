import pandas as pd 
import json
import tqdm 
from vllm import LLM, SamplingParams
from tqdm import tqdm
from huggingface_hub import hf_hub_download
from .prompts.conversation_eval_prompt import CONVERSATION_EVAL_PROMPT
from .prompts.system_prompt import SYSTEM_PROMPT

class DataLabel:

    def __init__(self, path_to_data: str, output_path: str, model: str, system_prompt: str, conversation_eval_prompt: str, tokenizer: str = None):
        self.data_path = path_to_data
        self.output_path = output_path
        self.system_prompt = system_prompt
        self.conversation_eval_prompt = conversation_eval_prompt
        self.model = model
        self.tokenizer = tokenizer
        
        # Initialize vLLM model once
        self.llm = LLM(model=self.model, tokenizer=self.tokenizer if self.tokenizer else self.model)
        self.sampling_params = SamplingParams(
            temperature=0.1,
            max_tokens=1000
        )

    def load_data(self):
        df = pd.read_csv(self.data_path)
        return df 
    
    def create_labelling_prompt(self, conversation: str):
        return f"""Evaluate this doctor-patient conversation using the Calgary-Cambridge Guide framework.

        CONVERSATION: {conversation}

        EVALUATION CRITERIA:
        {self.conversation_eval_prompt} """
    
    def label_conversation(self, conversation: str):
        prompt = self.create_labelling_prompt(conversation=conversation)
        
        # Format as chat messages
        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': prompt}
        ]
        
        # Use vLLM chat interface
        response = self.llm.chat([messages], self.sampling_params)
        
        # Extract generated text
        generated_text = response[0].outputs[0].text
        
        return json.loads(generated_text)
    
    def load_and_label_conversations_together(self):
        df = self.load_data()

        if "conversation" not in df.columns:
            raise ValueError(f"Column conversation not found. Available columns: {df.columns.tolist()}")
        
        categories = [
            'cc_opening',
            'cc_agenda_set', 
            'cc_patient_narrative_supported',
            'cc_structure_signposting',
            'cc_summary_checkback',
            'cc_closing_next_steps'
        ]
    
        for cat in categories:
            df[cat] = None

        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Labeling conversations"):
            try:
                conversation = row['conversation']
                labels = self.label_conversation(conversation)
                
                for cat in categories:
                    df.at[idx, cat] = labels[cat]
                    
            except Exception as e:
                print(f"\nError processing row {idx}: {e}")
                for cat in categories:
                    df.at[idx, cat] = -1  

        df.to_csv(self.output_path, index=False)
        print(f"\nLabeling complete! Results saved to {self.output_path}")
        
        return df


if __name__ == "__main__":
    # Download GGUF model
    repo_id = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
    filename = "Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
    tokenizer = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    
    model_path = hf_hub_download(repo_id, filename=filename)
    
    labeldata = DataLabel(
        path_to_data="/workspace/intern-proj-abim/Intern-Project/src/label-data/data_source/gpt-4.csv",  
        output_path="/workspace/intern-proj-abim/Intern-Project/src/label-data/data_source/labeled_conversations.csv",
        model=model_path,
        tokenizer=tokenizer,
        system_prompt=SYSTEM_PROMPT,
        conversation_eval_prompt=CONVERSATION_EVAL_PROMPT
    )
    
    labeldata.load_and_label_conversations_together()