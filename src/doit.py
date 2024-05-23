#!/usr/bin/env python
import datetime
import os
import re
from typing import List

import boto3
import typer
from botocore.exceptions import ClientError
from dateutil.relativedelta import relativedelta
from typing_extensions import Optional

# See /Users/aberezin/fti/fti-virtual-file-system/projects/cp-railway-integration.rev/phase2/repo-github/cpkc/transit_time/code/utils/awsutils.py
# for attempt at a wrapper for aws. Also need to figure out what im going to do about a cli utils module. and
# specifically how to easily add to it while im in another project

app = typer.Typer(help="A program to inspect an aws bucket for objects that look like glue table metadata and"
                       " turn them into json files in a tmp dir under the working dir.")


# One would need to do an `aws sso login --profile CPR-D-AWS-DevSTB-Developer` at powershell or cmd.exe
# TODO move to utils
def export_print(credentials):
    print(f"export AWS_ACCESS_KEY_ID={credentials['AccessKeyId']}")
    print(f"export AWS_SECRET_ACCESS_KEY={credentials['SecretAccessKey']}")
    print(f"export AWS_SESSION_TOKEN={credentials['SessionToken']}")


default_profile = 'D-AWS-DevSTB-Developer'
default_bucket = "stb-dev-processed-data-cpkc-975050021285"
verbosity = 0


def debug_print(param):
    if verbosity > 0:
        print(param)


def validate_credentials(session: boto3.Session):
    sts = session.client('sts')
    try:
        sts.get_caller_identity()
        debug_print("Credentials are valid.")
    except ClientError as e:
        print("Credentials are NOT valid or bad profile.")
        print(e)
        exit(1)


# Define a custom function to serialize datetime objects
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


@app.command()
def export(profile_name: Optional[str] = default_profile, verbose: Optional[int] = 0,
           start_date: Optional[str] = default_bucket, end_date: Optional[str] = None):
    global verbosity
    verbosity = verbose
    if os.system('mkdir -p tmp') > 0:
        print("Error with mkdir")
        exit(1)
    debug_print(f"using profile name: {profile_name}")

    # Define timeframe
    today: datetime.datetime = datetime.datetime.utcnow()
    start_date: datetime.datetime = today - relativedelta(days=7)
    end_date: datetime.datetime = today

    session: boto3.Session = boto3.Session(profile_name=profile_name)
    validate_credentials(session)
    hourly_data = get_hourly_cost_data(session, start_date, end_date)
    for hour in hourly_data:
        print(f"Time: {hour['TimePeriod']['Start']} - Cost: {hour['Total']['Amount']}")

    exit(0)
    # junk below
    s3 = session.client('s3')
    if hack:
        pat = re.compile(r"(\w+)/metadata/.*")
        print("hacking")
    else:
        pat = re.compile(r"tables/(\w+)/metadata/.*")
    filepath_base = "tmp"
    keys_items: List[dict] = s3.list_objects_v2(Bucket=bucket)['Contents']
    debug_print(keys_items)
    for item in keys_items:
        key = item['Key']
        m = pat.match(key)
        debug_print(key)
        if not m:
            debug_print("no objects found")
        else:
            table_name = m.group(1)
            filepath = os.path.join(filepath_base, f"{table_name}.json")
            with open(filepath, 'wb') as data:
                s3.download_fileobj(bucket, key, data)
        # pprint.pprint(j, compact=True)
    exit(0)


def get_hourly_cost_data(session: boto3.Session, start_date: datetime.datetime, end_date: datetime.datetime):
    """
    Retrieves hourly cost data from AWS Cost Explorer API.

    Args:
      start_date (datetime): Start date of the billing period.
      end_date (datetime): End date of the billing period.

    Returns:
      list: List of dictionaries containing hourly cost data.
    """
    client = session.client("ce")
    cost_data = client.get_cost_and_usage(
        TimePeriod={"Start": start_date.isoformat(), "End": end_date.isoformat()},
        Granularity="HOURLY", Metrics=["BlendedCost"]
    )
    return cost_data


if __name__ == "__main__":
    app()
