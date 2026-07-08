from aws_cdk import Stack
from constructs import Construct  # This now safely imports the real AWS package!

# Update these two lines to use the renamed local folder:
from cdk_constructs.app_config_construct import AppConfigConstruct
from cdk_constructs.auth_construct import AuthConstruct

class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Initialize the AppConfig Setup Construct
        AppConfigConstruct(self, "AppConfigConstruct")

        # Initialize the API Gateway, Auth, and Lambda Infrastructure Construct
        AuthConstruct(self, "AuthConstruct")
