import statey as st
from statey.ext.pulumi.providers import aws


@st.declarative
def resources(session, public_key: str):
    key = aws.ec2.KeyPair(
        keyName="test",
        publicKey=public_key,
    )

    security_group = aws.ec2.SecurityGroup(
        namePrefix="test_sg",
        description="My security group.",
        ingress=[
            {
                "protocol": "tcp",
                "fromPort": 22,
                "toPort": 22,
                "cidrBlocks": ["0.0.0.0/0"],
            }
        ],
        egress=[
            {"protocol": "-1", "fromPort": 0, "toPort": 0, "cidrBlocks": ["0.0.0.0/0"]}
        ],
    )

    instance = aws.ec2.Instance(
        ami="ami-07d02ee1eeb0c996c",
        instanceType="t2.micro",
        keyName=key.keyName,
        vpcSecurityGroupIds=[security_group.id],
    )


def module(session):
    with open("../iac-test-key.pub") as f:
        public_key = f.read()

    resources(session, public_key=public_key)
