#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from cdk.cdk_stack import TestStack

env = cdk.Environment(account="081142152120", region="us-east-1")

app = cdk.App()
TestStack(app, "test", env=env)
app.synth()
