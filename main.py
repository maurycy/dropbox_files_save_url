import backoff
import dotenv
import dropbox
import os
import requests
import sys

dotenv.load_dotenv(verbose=True)

dbx = dropbox.Dropbox(os.environ["DROPBOX_TOKEN"])
session: requests.Session = requests.Session()


def on_backoff(details):
    print("backoff: sys.exc_info()='{}'".format(sys.exc_info()))
    print(
        "backoff: "
        "Backing off {wait:0.1f} seconds afters {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


@backoff.on_exception(backoff.expo, Exception, max_tries=3, on_backoff=on_backoff)
def main(path, url):
    global session

    print("main('{}', '{}')".format(path, url))

    r: requests.models.Response = session.get(url)
    r.raise_for_status()

    print("r.status_code={}".format(r.status_code))

    dbx.files_upload(
        r.content,
        path,
        mode=dropbox.files.WriteMode.overwrite,
        autorename=False,
        mute=False,
    )


def dropbox_files_save_url(event: dict, context) -> None:
    print("Event ID: {}".format(context.event_id))
    print("Event type: {}".format(context.event_type))
    print("Context: {}".format(context))
    print("Event: {}".format(event))
    print("os.environ: {}".format(os.environ))

    path: str = event["attributes"]["path"]
    url: str = event["attributes"]["url"]

    main(path, url)
