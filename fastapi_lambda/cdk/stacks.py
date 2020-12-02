from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigatewayv2 as _apigw,
    aws_apigatewayv2_integrations as _apigw_integration,
)


class FastAPILambdaEndpointStack(core.Stack):
    def __init__(
        self, scope: core.Construct, id: str, *, docker_root: str, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        base_lambda = _lambda.DockerImageFunction(
            self,
            "FastAPIImageLambda",
            code=_lambda.DockerImageCode.from_image_asset(docker_root),
        )

        base_api = _apigw.HttpApi(
            self,
            "FastAPIProxyGateway",
            api_name="FastAPIProxyGateway",
            default_integration=_apigw_integration.LambdaProxyIntegration(
                handler=base_lambda
            ),
        )

        core.CfnOutput(
            self, "EndpointUrl", value=base_api.api_endpoint, export_name="fastApiUrl"
        )
