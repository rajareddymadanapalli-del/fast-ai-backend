from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    Duration
)
from constructs import Construct

class FastAiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-090f7ace181ca2270")

        # 1. APPLICATION LOAD BALANCED FARGATE SERVICE
        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FastAiService",
            cluster=ecs.Cluster(self, "FastAiCluster", vpc=vpc),
            cpu=512,
            memory_limit_mib=1024,
            desired_count=2, # Start with 2 for High Availability
            public_load_balancer=True,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("905418237004.dkr.ecr.us-east-1.amazonaws.com/fast-ai-worker:latest"),
                container_port=8000,
            )
        )

        # 2. CONFIGURE HEALTH CHECKS (Target Group)
        # This tells the ALB: "Only send traffic if /db-status returns 200"
        self.service.target_group.configure_health_check(
            path="/db-status",
            interval=Duration.seconds(30),
            timeout=Duration.seconds(5),
            healthy_threshold_count=2,
            unhealthy_threshold_count=5
        )

        # 3. AUTO SCALING: Task Count
        scaling = self.service.service.auto_scale_task_count(
            min_capacity=2,
            max_capacity=10 # Scales up to 10 instances during high load
        )

        # 4. SCALING POLICIES: Target Tracking
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60)
        )

        scaling.scale_on_memory_utilization(
            "MemoryScaling",
            target_utilization_percent=80
        )
