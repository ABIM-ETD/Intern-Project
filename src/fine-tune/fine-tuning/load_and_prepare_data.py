import pandas as pd 
import datasets
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split

class DataClass:

    def __init__(self, data_path: str, model_path: str):
        self.data_path = data_path
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

    def load_data(self):
        dataset = load_dataset('csv', data_files={'train': self.data_path})
        return dataset 
    
    def tokenize(self, examples):
   
        return self.tokenizer(
            examples['conversation'],
            padding='max_length',
            truncation=True,
            max_length=512
        )
    
    def mapping_data(self):
       
        data = self.load_data()
        
        tokenized_data = data.map(
            self.tokenize,
            batched=True,
            remove_columns=['conversation']  
        )
        
        return tokenized_data 
    
    def split_data(self):
      
        tokenized_data = self.mapping_data()
        
        train_df = tokenized_data['train'].to_pandas()
        
        train_df, temp_df = train_test_split(train_df, test_size=0.2, random_state=42)
        val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
        
        train_data = Dataset.from_pandas(train_df, preserve_index=False)
        val_data = Dataset.from_pandas(val_df, preserve_index=False)
        test_data = Dataset.from_pandas(test_df, preserve_index=False)

        return train_data, val_data, test_data