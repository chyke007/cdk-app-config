import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_app_config.cdk_app_config_stack import CdkAppConfigStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_app_config/cdk_app_config_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkAppConfigStack(app, "cdk-app-config")
    template = assertions.Template.from_stack(stack)
