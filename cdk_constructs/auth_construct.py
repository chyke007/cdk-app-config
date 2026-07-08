import os
from aws_cdk import (
    Duration,
    CfnOutput,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_appconfig as appconfig
)
from constructs import Construct

class AuthConstruct(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        current_region = Stack.of(self).region

        app_config_layer_arn = appconfig.Application.get_lambda_layer_version_arn(
            region=current_region,
            platform=appconfig.Platform.X86_64
        )

        app_config_extension_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, "AppConfigExtension",
            layer_version_arn=app_config_layer_arn
        )

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lambda_path = os.path.join(base_dir, "lambda")

        gateway_lambda = _lambda.Function(
            self, "AiGatewayFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(lambda_path),
            layers=[app_config_extension_layer],
            memory_size=256,
            timeout=Duration.seconds(10)
        )

        gateway_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "appconfig:GetLatestConfiguration",
                    "appconfig:StartConfigurationSession"
                ],
                resources=["*"]
            )
        )

        api = apigateway.RestApi(
            self, "AiRouterApi",
            rest_api_name="Smart AI Gateway Service",
            description="Dynamically manages LLM endpoints utilizing AppConfig presets.",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS
            )
        )

        prompt_resource = api.root.add_resource("prompt")
        prompt_resource.add_method(
            "POST", 
            apigateway.LambdaIntegration(gateway_lambda),
            api_key_required=True
        )

        key = api.add_api_key(
            "DevApiKey",
            api_key_name="ai-gateway-dev-key"
        )
        plan = api.add_usage_plan(
            "UsagePlan",
            name="AiGatewayBasicPlan"
        )
        plan.add_api_stage(stage=api.deployment_stage)
        plan.add_api_key(key)

        CfnOutput(self, "ApiUrl", value=f"{api.url}prompt")
