from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    aws_wafv2 as wafv2,
    aws_cloudwatch as cloudwatch,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudwatch_actions as cw_actions,
    CfnOutput,
    Duration
)
from constructs import Construct

class FastAiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-090f7ace181ca2270")

        # Core Service (Previously Defined)
        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FastAiService",
            cluster=ecs.Cluster(self, "FastAiCluster", vpc=vpc, cluster_name="fastai-cdk-cluster"),
            cpu=512,
            memory_limit_mib=1024,
            desired_count=2,
            public_load_balancer=True,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("905418237004.dkr.ecr.us-east-1.amazonaws.com/fast-ai-worker:latest"),
                container_port=8000
            )
        )

        # 1. MONITORING: CloudWatch Dashboard
        dashboard = cloudwatch.Dashboard(self, "FastAiDashboard", dashboard_name="FastAi-Production-Metrics")
        
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Request Count",
                left=[self.service.load_balancer.metric_request_count()]
            ),
            cloudwatch.GraphWidget(
                title="CPU Utilization",
                left=[self.service.service.metric_cpu_utilization()]
            )
        )

        # 2. ALERTING: SNS Topic for High Errors
        error_topic = sns.Topic(self, "ErrorTopic", display_name="FastAi-Error-Alerts")
        # Replace with your actual email
        error_topic.add_subscription(subscriptions.EmailSubscription("rajar@example.com"))

        # 3. ALARM: Trigger if 5XX errors > 5 in 1 minute
        error_alarm = cloudwatch.Alarm(self, "HighErrorAlarm",
            metric=self.service.load_balancer.metric_http_code_elb(cloudwatch.HttpCodeElb.ELB_5XX_COUNT),
            threshold=5,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        
        error_alarm.add_alarm_action(cw_actions.SnsAction(error_topic))

        # WAF Logic (Keeping existing security)
        # ... [WAF code remains here] ...
