import aws_cdk.aws_ec2 as ec2
from aws_cdk import core as cdk


class TestStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        with open("../iac-test-key.pub") as f:
            public_key = f.read()

        vpc = ec2.Vpc.from_lookup(self, "default_vpc", is_default=True)

        security_group = ec2.SecurityGroup(
            self,
            "test_sg",
            vpc=vpc,
            # description="This is my security group.",
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22))

        image = ec2.AmazonLinuxImage()

        instance = ec2.Instance(
            self,
            "test_instance",
            machine_image=image,
            instance_type=ec2.InstanceType("t2.micro"),
            key_name="app_key-d2f12cf",
            vpc=vpc,
            security_group=security_group,
            # user_data="#",
        )

        public_ip = cdk.CfnOutput(self, "public_ip", value=instance.instance_public_ip)
