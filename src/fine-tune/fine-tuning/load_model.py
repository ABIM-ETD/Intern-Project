import pandas as pd 
from transformers import AutoModel
import torch
import torch.nn as nn 



class MultiTaskBertClass(nn.Module):

    def __init__(self,pretrained_model_name: str):
        super(MultiTaskBertClass,self).__init__()

        self.bert=AutoModel.from_pretrained(pretrained_model_name)
        
        self.dropout=nn.Dropout(0.3)

        self.CalCam1=nn.Linear(self.bert.config.hidden_size,3)

        self.CalCam2=nn.Linear(self.bert.config.hidden_size,3)

        self.CalCam3=nn.Linear(self.bert.config.hidden_size,3)

        self.CalCam4=nn.Linear(self.bert.config.hidden_size,3)

        self.CalCam5=nn.Linear(self.bert.config.hidden_size,3)

        self.CalCam6=nn.Linear(self.bert.config.hidden_size,3)

    
    def forward(self, input_ids, attention_mask, calcam1_labels=None, calcam2_labels=None, calcam3_labels=None, calcam4_labels=None, calcam5_labels=None, calcam6_labels=None):

        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)

        pooled_output=outputs.pooler_output

        pooled_output=self.dropout(pooled_output)


        CalCam1_logits=self.CalCam1(pooled_output)
        CalCam2_logits=self.CalCam2(pooled_output)
        CalCam3_logits=self.CalCam3(pooled_output)
        CalCam4_logits=self.CalCam4(pooled_output)
        CalCam5_logits=self.CalCam5(pooled_output)
        CalCam6_logits=self.CalCam6(pooled_output)


        loss=None
        if calcam1_labels is not None and calcam2_labels is not None and calcam3_labels is not None and calcam4_labels is not None and calcam5_labels is not None and calcam6_labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss1 = loss_fct(CalCam1_logits, calcam1_labels)
            loss2 = loss_fct(CalCam2_logits, calcam2_labels)
            loss3 = loss_fct(CalCam3_logits, calcam3_labels)
            loss4 = loss_fct(CalCam4_logits, calcam4_labels)
            loss5 = loss_fct(CalCam5_logits, calcam5_labels)
            loss6 = loss_fct(CalCam6_logits, calcam6_labels)
            loss = loss1 + loss2 + loss3 + loss4 + loss5 + loss6

        
        return {
            'loss': loss,
            'CalCam1_logits': CalCam1_logits,
            'CalCam2_logits': CalCam2_logits,
            'CalCam3_logits': CalCam3_logits,
            'CalCam4_logits': CalCam4_logits,
            'CalCam5_logits': CalCam5_logits,
            'CalCam6_logits': CalCam6_logits
        }





    
    
    
