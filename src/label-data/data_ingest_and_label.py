import pandas as pd 
import json
import tqdm 
import ollama 
from tqdm import tqdm
from .prompts.conversation_eval_prompt import CONVERSATION_EVAL_PROMPT
from .prompts.system_prompt import SYSTEM_PROMPT

class DataLabel:

    def __init__(self,path_to_data: str,output_path: str,model: str,system_prompt: str,conversation_eval_prompt: str):
        self.data_path=path_to_data
        self.output_path=output_path
        self.system_prompt=system_prompt
        self.conversation_eval_prompt=conversation_eval_prompt
        self.model=model

    def load_data(self):
        df=pd.read_csv(self.data_path)
        return df 
    
    def create_labelling_prompt(self,conversation: str):

        return f"""Evaluate this doctor-patient conversation using the Calgary-Cambridge Guide framework.

        CONVERSATION: {conversation}

        EVALUATION CRITERIA:
        {self.conversation_eval_prompt} """
    

    def label_conversation(self,conversation: str):

        prompt=self.create_labelling_prompt(conversation=conversation)

        response = ollama.chat(
        model=self.model,
        messages=[
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        format='json',
        options={
            'temperature': 0.1,  # Low temp for consistency
            'num_predict': 1000
        }
        )

        return json.loads(response['message']['content'])
    
    def load_and_label_conversations_together(self):

        df=self.load_data()

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



if __name__=="__main__":

    labeldata=DataLabel(path_to_data=".data_source/gpt-4.csv",output_path=".data_source/labelled_data.csv",model="llama3.3:70b-instruct-q4_K_M",system_prompt=SYSTEM_PROMPT,conversation_eval_prompt=CONVERSATION_EVAL_PROMPT)
    labeldata.load_and_label_conversations_together()
    


        



        