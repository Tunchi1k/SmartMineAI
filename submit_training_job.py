from google.cloud import aiplatform

# Initialize AI Platform
aiplatform.init(
    project = 'smartmineai',
    location = 'us-central1',
    staging_bucket= 'gs://chintu-smartmining-bucket'
)

# Define the training job
job = aiplatform.CustomPythonPackageTrainingJob(
    display_name='SmartMiningAI-TrainingJob',
    python_package_gcs_uri='gs://chintu-smartmining-bucket/trainer_package.zip',
    python_module_name='trainer.trainer',
    container_uri="us-docker.pkg.dev/vertex-ai/training/sklearn-cpu.1-6:latest",
    model_serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest",
)

#Running the training job
model = job.run(
    replica_count=1,
    machine_type="n1-standard-4",
    model_display_name="predictive-maintenance-model",
    args=[],
    environment_variables={"AIP_MODEL_DIR": "/model"}
)