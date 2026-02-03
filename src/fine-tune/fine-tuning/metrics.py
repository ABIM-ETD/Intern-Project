import evaluate
import numpy as np

METRIC = evaluate.load('f1')


def compute_metrics(eval_pred):
    all_logits, all_labels = eval_pred
    calcam1_logits, calcam2_logits, calcam3_logits, calcam4_logits, calcam5_logits, calcam6_logits = all_logits
    calcam1_labels, calcam2_labels, calcam3_labels, calcam4_labels, calcam5_labels, calcam6_labels = all_labels

    calcam1_predictions = np.argmax(calcam1_logits, axis=-1)
    calcam2_predictions = np.argmax(calcam2_logits, axis=-1)
    calcam3_predictions = np.argmax(calcam3_logits, axis=-1)
    calcam4_predictions = np.argmax(calcam4_logits, axis=-1)
    calcam5_predictions = np.argmax(calcam5_logits, axis=-1)
    calcam6_predictions = np.argmax(calcam6_logits, axis=-1)
    
    calcam1_metrics = METRIC.compute(predictions=calcam1_predictions, references=calcam1_labels, average='weighted')
    calcam2_metrics = METRIC.compute(predictions=calcam2_predictions, references=calcam2_labels, average='weighted')
    calcam3_metrics = METRIC.compute(predictions=calcam3_predictions, references=calcam3_labels, average='weighted')
    calcam4_metrics = METRIC.compute(predictions=calcam4_predictions, references=calcam4_labels, average='weighted')
    calcam5_metrics = METRIC.compute(predictions=calcam5_predictions, references=calcam5_labels, average='weighted')
    calcam6_metrics = METRIC.compute(predictions=calcam6_predictions, references=calcam6_labels, average='weighted')
    
    return {
        'f1_calcam1': calcam1_metrics['f1'],
        'f1_calcam2': calcam2_metrics['f1'],
        'f1_calcam3': calcam3_metrics['f1'],
        'f1_calcam4': calcam4_metrics['f1'],
        'f1_calcam5': calcam5_metrics['f1'],
        'f1_calcam6': calcam6_metrics['f1'],
    }