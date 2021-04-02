from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core
from aws_cdk import aws_s3 as _s3

class CustomVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_configs = self.node.try_get_context('envs')['prod']

        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr=prod_configs['vpc_configs']['vpc_cidr'],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name="dbSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.ISOLATED
                ),
            ]
        )


        core.Tag.add(custom_vpc, "Owner", "Shivang")

        core.CfnOutput(self,
        "customVpcOutput",
        value=custom_vpc.vpc_id,
        export_name="customVpcId"
        )

        my_bkt = _s3.Bucket(
            self,
            "myBucketID",
            encryption = _s3.BucketEncryption.KMS,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL
        )

        core.Tag.add(my_bkt, "Owner", "Shivang")

        # Resource in the same account
        bkt1=_s3.Bucket.from_bucket_name(
            self,
            "MyImportedBucket",
            "my-custom-vpc-stack-mybucketidc04e027a-11468mzbt9pj2"
        )

        core.CfnOutput(self,
        "myimportedbucket",
        value=bkt1.bucket_name)

        