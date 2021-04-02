#!/usr/bin/env python3

from aws_cdk import core

from resource_stacks.custom_vpc import CustomVpcStack
from resource_stacks.custom_ec2 import CustomEc2Stack

app = core.App()

env_personal = core.Environment(account="921537816184", region="us-east-1")

#custom VPC Stack
CustomVpcStack(app, "my-custom-vpc-stack", env=env_personal)

#custom EC2 Stack
CustomEc2Stack(app, "my-custom-web-stack", env=env_personal)


app.synth()
