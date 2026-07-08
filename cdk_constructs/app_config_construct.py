import os
from aws_cdk import (
    aws_appconfig as appconfig
)
from constructs import Construct

class AppConfigConstruct(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.application = appconfig.CfnApplication(
            self, "AiGatewayApp",
            name="AiGateway"
        )

        self.environment = appconfig.CfnEnvironment(
            self, "ProdEnvironment",
            application_id=self.application.ref,
            name="Prod"
        )

        self.configuration_profile = appconfig.CfnConfigurationProfile(
            self, "ModelRouterProfile",
            application_id=self.application.ref,
            name="ModelRouter",
            location_uri="hosted"
        )

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config", "config.json")
        
        with open(config_path, "r", encoding="utf-8") as file:
            config_content = file.read()

        hosted_version = appconfig.CfnHostedConfigurationVersion(
            self, "InitialConfigVersion",
            application_id=self.application.ref,
            configuration_profile_id=self.configuration_profile.ref,
            content_type="application/json",
            content=config_content
        )

        appconfig.CfnDeployment(
            self, "InitialDeployment",
            application_id=self.application.ref,
            environment_id=self.environment.ref,
            configuration_profile_id=self.configuration_profile.ref,
            configuration_version=hosted_version.ref,
            deployment_strategy_id="AppConfig.AllAtOnce"  # Immediate rollout for testing
        )
