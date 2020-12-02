import json
import pprint
import pathlib

import httpx

from invoke import task

@task
def setup(c):
    local_lambda_emulator_path = "./.direnv/.aws-lambda-rie"
    c.run(f"mkdir -p {local_lambda_emulator_path}")

    lambda_emulator_url = "https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie"
    c.run(f"curl -Lo {local_lambda_emulator_path}/aws-lambda-rie {lambda_emulator_url}")

    c.run(f"chmod +x {local_lambda_emulator_path}/aws-lambda-rie")

@task
def run_lambda(c):
    """
    Run the local lambda runtime emulator
    """
    c.run("docker-compose up", pty=True)

@task
def local_event(c, method="GET", path="/items/"):
    """
    Send an HTTP Gateway event to the lambda runtime emulator
    """
    from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
    
    http_event_dict = json.loads(pathlib.Path("event.json").read_text())

    http_event_dict["requestContext"]["http"]["path"] = path
    http_event_dict["requestContext"]["http"]["method"] = method

    http_event = APIGatewayProxyEventV2(http_event_dict)

    local_url = "http://localhost:9000/2015-03-31/functions/function/invocations"

    response = httpx.post(local_url, json=http_event._data)
    response.raise_for_status()

    pprint.pprint(response.json())

@task
def build(c, tag=""):
    c.run("docker-compose build --pull")