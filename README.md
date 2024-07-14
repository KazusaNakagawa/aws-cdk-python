
# Welcome to your CDK Python project!

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy --context env={{environment}}` deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## S3 Check

```bash
# Ex
## s3 upload
aws s3 cp ./test1.json s3://s3-copy-source-bucket-dev/test1.json

## Upload file to S3
aws s3 ls s3://s3-copy-source-bucket-dev --rec

## Copy file from one bucket to another
aws s3 ls s3://s3-copy-target-bucket-dev --rec
```
