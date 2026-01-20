
import mlflow 


mlflow.set_tracking_uri("http://10.51.92.6:5000")

with mlflow.start_run():
    
    print("logging")
    mlflow.log_param("text","hi shawn")

