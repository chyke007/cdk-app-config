import os
import aws_cdk as cdk
from app_stack import AppStack

app = cdk.App()
AppStack(
    app, "AppStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION", "us-east-1")
    )
)

app.synth()
