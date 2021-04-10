"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

with open("../iac-test-key.pub") as f:
    public_key = f.read()

key = aws.ec2.KeyPair("shnail", public_key=public_key)

security_group = aws.ec2.SecurityGroup(
    "test_sg_2",
    description="This is my security group.",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ],
)

instance = aws.ec2.Instance(
    "test_instance",
    ami="ami-07d02ee1eeb0c996c",
    instance_type="t2.micro",
    key_name=key.key_name,
    vpc_security_group_ids=[security_group.id],
    # user_data="#",
)

pulumi.export("public_ip", instance.public_ip)
