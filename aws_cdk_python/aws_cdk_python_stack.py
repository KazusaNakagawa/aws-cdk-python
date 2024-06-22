from aws_cdk import Stack, aws_lambda as _lambda, aws_apigateway as apigateway
from constructs import Construct


class MyCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数を定義
        hello_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="hello.handler",
        )

        # API Gatewayを定義
        apigateway.LambdaRestApi(self, "Endpoint", handler=hello_lambda)
