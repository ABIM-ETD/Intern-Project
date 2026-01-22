from .metrics import compute_metrics
from .load_model import MultiTaskBertClass
from transformers import AutoTokenizer, BertConfig, BertModel, BertPreTrainedModel
from transformers import Trainer, TrainerCallback, TrainingArguments, EarlyStoppingCallback
from .load_and_prepare_data import DataClass
import torch


RESULTS_DIRECTORY = './results/experiment'
PRETRAINED_MODEL_NAME = "distilbert-base-uncased"
BERT_CONFIG = BertConfig.from_pretrained(PRETRAINED_MODEL_NAME)
NUM_TRAIN_EPOCHS = 10


output_directory = RESULTS_DIRECTORY
evaluation_strategy = 'epoch'
per_device_train_batch_size = 4
per_device_eval_batch_size = 4
gradient_accumulation_steps = 2  
learning_rate = 2e-5
weight_decay = 0.01
max_grad_norm = 1
num_train_epochs = NUM_TRAIN_EPOCHS
lr_scheduler_type = 'linear'
warmup_ratio = 0.05
logging_strategy = 'epoch'
save_strategy = 'epoch'
save_total_limit = 1
label_names = ['cc_agenda_set', 'cc_closing_next_steps', 'cc_opening', 'cc_patient_narrative_supported', 'cc_structure_signposting', 'cc_summary_checkback']
load_best_model_at_end = True
metric_for_best_model = 'eval_f1_calcam1' 
greater_is_better = True
label_smoothing_factor = 0
report_to = 'none'  
gradient_checkpointing = False

model = MultiTaskBertClass.from_pretrained(
    PRETRAINED_MODEL_NAME,
    config=BERT_CONFIG
)


training_args = TrainingArguments(
    output_dir=output_directory,
    evaluation_strategy=evaluation_strategy,
    learning_rate=learning_rate,
    per_device_train_batch_size=per_device_train_batch_size,
    per_device_eval_batch_size=per_device_eval_batch_size,
    num_train_epochs=num_train_epochs,
    weight_decay=weight_decay,
    label_names=label_names,
    max_grad_norm=max_grad_norm,
    lr_scheduler_type=lr_scheduler_type,
    warmup_ratio=warmup_ratio,
    logging_strategy=logging_strategy,
    save_strategy=save_strategy,
    save_total_limit=save_total_limit,
    load_best_model_at_end=load_best_model_at_end,
    metric_for_best_model=metric_for_best_model,
    greater_is_better=greater_is_better,
    label_smoothing_factor=label_smoothing_factor,
    report_to=report_to,
    gradient_checkpointing=gradient_checkpointing,
    gradient_accumulation_steps=gradient_accumulation_steps 
)

early_stop_callback = EarlyStoppingCallback(3)


class MultiTaskDataCollator:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def __call__(self, features):
     
        batch = {
            'input_ids': [],
            'attention_mask': [],
            'calcam1_labels': [],
            'calcam2_labels': [],
            'calcam3_labels': [],
            'calcam4_labels': [],
            'calcam5_labels': [],
            'calcam6_labels': []
        }
        
        for feature in features:
            batch['input_ids'].append(feature['input_ids'])
            batch['calcam1_labels'].append(feature['cc_agenda_set'])
            batch['calcam2_labels'].append(feature['cc_closing_next_steps'])
            batch['calcam3_labels'].append(feature['cc_opening'])
            batch['calcam4_labels'].append(feature['cc_patient_narrative_supported'])
            batch['calcam5_labels'].append(feature['cc_structure_signposting'])
            batch['calcam6_labels'].append(feature['cc_summary_checkback'])
        
        batch = {k: torch.tensor(v) for k, v in batch.items()}
        
        return batch


class MultiTaskTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = {
            'calcam1_labels': inputs.pop('calcam1_labels'),
            'calcam2_labels': inputs.pop('calcam2_labels'),
            'calcam3_labels': inputs.pop('calcam3_labels'),
            'calcam4_labels': inputs.pop('calcam4_labels'),
            'calcam5_labels': inputs.pop('calcam5_labels'),
            'calcam6_labels': inputs.pop('calcam6_labels'),
        }
        
        outputs = model(**inputs, **labels)
        loss = outputs[0]
        
        if return_outputs:
            return loss, outputs
        return loss
    
    def prediction_step(self, model, inputs, prediction_loss_only, ignore_keys=None):
        labels = {
            'calcam1_labels': inputs.pop('calcam1_labels'),
            'calcam2_labels': inputs.pop('calcam2_labels'),
            'calcam3_labels': inputs.pop('calcam3_labels'),
            'calcam4_labels': inputs.pop('calcam4_labels'),
            'calcam5_labels': inputs.pop('calcam5_labels'),
            'calcam6_labels': inputs.pop('calcam6_labels'),
        }
        
        with torch.no_grad():
            outputs = model(**inputs, **labels)
            loss = outputs[0]
            logits = outputs[1:]  # All 6 task logits
        
        if prediction_loss_only:
            return (loss, None, None)
        
        # Stack labels in order
        labels_tuple = (
            labels['calcam1_labels'],
            labels['calcam2_labels'],
            labels['calcam3_labels'],
            labels['calcam4_labels'],
            labels['calcam5_labels'],
            labels['calcam6_labels']
        )
        
        return (loss, logits, labels_tuple)


tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)

data_collator = MultiTaskDataCollator(tokenizer)

data_class = DataClass(data_path='./data/fine_tuning_data.csv', model_path=PRETRAINED_MODEL_NAME)
train_data, val_data, test_data = data_class.split_data()

trainer = MultiTaskTrainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=val_data,
    compute_metrics=compute_metrics,
    data_collator=data_collator,
    callbacks=[early_stop_callback]
)

trainer.train()