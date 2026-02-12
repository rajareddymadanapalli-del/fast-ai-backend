from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_secretsmanager as secretsmanager,
    aws_ssm as ssm,
    CfnOutput
)
from constructs import Construct

class FastAiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Reference existing VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-090f7ace181ca2270")

        # 2. Reference Existing Secrets/Params
        db_secret = secretsmanager.Secret.from_secret_name_v2(self, "DbSecret", "fastai/prod/db_url")
        redis_param = ssm.StringParameter.from_string_parameter_name(self, "RedisParam", "/fastai/prod/redis_url")

        # 3. Define the ECS Cluster
        cluster = ecs.Cluster(self, "FastAiCluster", vpc=vpc, cluster_name="fastai-cdk-cluster")

        # 4. Create Fargate Service with Load Balancer
        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FastAiService",
            cluster=cluster,
            cpu=512,
            memory_limit_mib=1024,
            desired_count=1,
            public_load_balancer=True,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("905418237004.dkr.ecr.us-east-1.amazonaws.com/fast-ai-worker:latest"),
                container_port=8000,
                secrets={
                    "DATABASE_URL": ecs.Secret.from_secrets_manager(db_secret),
                    "REDIS_URL": ecs.Secret.from_ssm_parameter(redis_param)
                }
            )
        )

        CfnOutput(self, "LoadBalancerDNS", value=self.service.load_balancer.load_balancer_dns_name)
