#!/usr/bin/env python3

import pathlib

from aws_cdk import core

from fastapi_lambda.cdk.stacks import FastAPILambdaEndpointStack


app = core.App()


FastAPILambdaEndpointStack(
    app, "fastapi-endpoint", docker_root=pathlib.Path.cwd().as_posix()
)

app.synth()
