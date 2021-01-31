Sunset Alerts
=============

Use Google Cloud Functions to query SunsetWx API and send results via gmail or twitter (todo).

### Usage

```
# Alter arguments in `main.py`
nano main.py

# Authenticate google cloud
gcloud auth login

### Sunset

# Deploy the cloud function
gcloud functions deploy sunset --entry-point main --runtime=python37 --trigger-resource sunset_trigger --trigger-event google.pubsub.topic.publish --timeout 540s

# Scheduling the Cloud Function
gcloud scheduler jobs create pubsub sunsetTrigger --schedule "30 12 * * *" --topic sunset_trigger --message-body "This runs every day at 12:30"

### Sunrise

# Deploy the cloud function
gcloud functions deploy sunrise --entry-point main --runtime=python37 --trigger-resource sunrise_trigger --trigger-event google.pubsub.topic.publish --timeout 540s

# Scheduling the Cloud Function
gcloud scheduler jobs create pubsub sunriseTrigger --schedule "30 20 * * *" --topic sunrise_trigger --message-body "This runs every day at 20:30"

```
