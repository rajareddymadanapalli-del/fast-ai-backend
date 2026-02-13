from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticache as elasticache,
    aws_iam as iam,
    aws_wafv2 as wafv2,
    aws_cloudwatch as cloudwatch,
    CfnOutput
)
from constructs import Construct

class FastAiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-090f7ace181ca2270")

        # 1. SECURITY GROUP FOR REDIS
        redis_sg = ec2.SecurityGroup(self, "RedisSG", vpc=vpc, allow_all_outbound=True)
        
        # 2. MANAGED REDIS (ELASTICACHE)
        redis_subnet_group = elasticache.CfnSubnetGroup(self, "RedisSubnetGroup",
            description="Subnets for Redis",
            subnet_ids=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids
        )

        redis_cluster = elasticache.CfnCacheCluster(self, "RedisCluster",
            cache_node_type="cache.t4g.micro",
            engine="redis",
            num_cache_nodes=1,
            vpc_security_group_ids=[redis_sg.security_group_id],
            cache_subnet_group_name=redis_subnet_group.ref
        )

        # 3. ECS CLUSTER & API SERVICE
        cluster = ecs.Cluster(self, "FastAiCluster", vpc=vpc, cluster_name="fastai-cdk-cluster")
        
        self.api_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FastAiService",
            cluster=cluster,
            desired_count=2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("905418237004.dkr.ecr.us-east-1.amazonaws.com/fast-ai-worker:latest"),
                container_port=8000,
                environment={
                    "REDIS_URL": f"redis://{redis_cluster.attr_redis_endpoint_address}:{redis_cluster.attr_redis_endpoint_port}/0"
                }
            )
        )

        # 4. DEDICATED CELERY WORKER SERVICE (No Load Balancer needed)
        self.worker_service = ecs.FargateService(self, "CeleryWorkerService",
            cluster=cluster,
            task_definition=ecs.FargateTaskDefinition(self, "WorkerTaskDef", cpu=512, memory_limit_mib=1024),
            desired_count=1
        )
        
        self.worker_service.task_definition.add_container("WorkerContainer",
            image=ecs.ContainerImage.from_registry("905418237004.dkr.ecr.us-east-1.amazonaws.com/fast-ai-worker:latest"),
            command=["celery", "-A", "worker.celery_app", "worker", "--loglevel=info"],
            environment={
                "REDIS_URL": f"redis://{redis_cluster.attr_redis_endpoint_address}:{redis_cluster.attr_redis_endpoint_port}/0"
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="CeleryWorker")
        )

        # 5. PERMISSIONS: Allow API and Worker to talk to Redis
        redis_sg.add_ingress_rule(self.api_service.service.connections.security_groups[0], ec2.Port.tcp(6379))
        redis_sg.add_ingress_rule(self.worker_service.connections.security_groups[0], ec2.Port.tcp(6379))

        CfnOutput(self, "RedisEndpoint", value=redis_cluster.attr_redis_endpoint_address)
