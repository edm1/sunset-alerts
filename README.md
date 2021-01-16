Sunset Alerts
=============

Use Google Cloud Functions to query SunsetWx API and send results via gmail or twitter (todo).

### Usage

```
# Alter arguments in `sunsetwx_cloud_function.py`
nano main.py

# Authenticate google cloud
gcloud auth login

# Deploy the cloud function.
# Specify as params that "main" is the function for the code entry point, and a Pub/Sub topic named "standing" to listen from.
gcloud functions deploy main --entry-point main --runtime=python37 --trigger-resource standing --trigger-event google.pubsub.topic.publish --timeout 540s

# Scheduling the Cloud Function
# Use gcloud scheduler command to deploy scheduler job which will publish a message to Pub/Sub topic named standing every day at 12:30.
gcloud scheduler jobs create pubsub ElySunsetTrigger --schedule "30 12 * * *" --topic standing --message-body "This runs every day at 12:30"
```
