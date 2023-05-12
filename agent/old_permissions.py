import json
import boto3

iam = boto3.client('iam')

policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:PutBucketWebsite",
                "s3:PutBucketPolicy",
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "cloudfront:CreateDistribution",
                "cloudfront:ListDistributions"
            ],
            "Resource": "*"
        }
    ]
}

response = iam.create_policy(
    PolicyName='ReactAppDeploymentPolicy',
    PolicyDocument=json.dumps(policy_document)
)

policy_arn = response['Policy']['Arn']

response = iam.add_user_to_group(
    GroupName='ReactAppDeploymentGroup',
    UserName='bspell20'
)

response = iam.attach_group_policy(
    GroupName='ReactAppDeploymentGroup',
    PolicyArn=policy_arn
)