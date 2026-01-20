from .load_model import MultiTaskBertClass
import mlflow 



mlflow.set_experiment("Loading Custom Bert")

mlflow.set_tracking_uri("")

with mlflow.start_run():
    model = MultiTaskBertClass("bert-base-uncased")
    
    mlflow.log_param("text","hi")

