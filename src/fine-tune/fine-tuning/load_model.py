import pandas as pd 
from transformers import AutoModel
import torch
import torch.nn as nn 
from transformers import AutoTokenizer, BertConfig, BertModel, BertPreTrainedModel



class MultiTaskBertClass(BertPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)      

        self.bert=BertModel(config)  

        self.CalCam1=nn.Linear(config.hidden_size,3)

        self.CalCam2=nn.Linear(config.hidden_size,3)

        self.CalCam3=nn.Linear(config.hidden_size,3)

        self.CalCam4=nn.Linear(config.hidden_size,3)

        self.CalCam5=nn.Linear(config.hidden_size,3)

        self.CalCam6=nn.Linear(config.hidden_size,3)

        classifier_dropout = config.classifier_dropout if config.classifier_dropout is not None else config.hidden_dropout_prob

        self.dropout = nn.Dropout(classifier_dropout)

        self.init_weights()

    
    def forward(self, input_ids, attention_mask=None,calcam1_labels=None, calcam2_labels=None, calcam3_labels=None, calcam4_labels=None, calcam5_labels=None, calcam6_labels=None):

        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)

        pooled_output=self.dropout(outputs[1])

        CalCam1_logits=self.CalCam1(pooled_output)
        CalCam2_logits=self.CalCam2(pooled_output)
        CalCam3_logits=self.CalCam3(pooled_output)
        CalCam4_logits=self.CalCam4(pooled_output)
        CalCam5_logits=self.CalCam5(pooled_output)
        CalCam6_logits=self.CalCam6(pooled_output)


        loss=None
        if calcam1_labels is not None and calcam2_labels is not None and calcam3_labels is not None and calcam4_labels is not None and calcam5_labels is not None and calcam6_labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss1 = loss_fct(CalCam1_logits.view(-1,3), calcam1_labels.view(-1))
            loss2 = loss_fct(CalCam2_logits.view(-1,3), calcam2_labels.view(-1))
            loss3 = loss_fct(CalCam3_logits.view(-1,3), calcam3_labels.view(-1))
            loss4 = loss_fct(CalCam4_logits.view(-1,3), calcam4_labels.view(-1))
            loss5 = loss_fct(CalCam5_logits.view(-1,3), calcam5_labels.view(-1))
            loss6 = loss_fct(CalCam6_logits.view(-1,3), calcam6_labels.view(-1))
            loss = loss1 + loss2 + loss3 + loss4 + loss5 + loss6

        
        return (
            loss,
            CalCam1_logits,
            CalCam2_logits,
            CalCam3_logits,
            CalCam4_logits,
            CalCam5_logits,
            CalCam6_logits
        )