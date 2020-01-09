```
$ gcloud pubsub topics create dropbox-files-save-url
$ gcloud alpha functions deploy dropbox_files_save_url \
    --runtime=python37 \
    --trigger-topic=dropbox-files-save-url \
    --timeout=30 \
    --memory=128
```
