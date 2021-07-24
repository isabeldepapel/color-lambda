# Deploying with AWS SAM CLI

I've heard good things about SAM so I was looking forward to using it. And it's pretty good! Pretty similar to serverless with some nice features around deployment and local testing, but all AWS native.

I used `sam init` to set up the scaffolding for a basic Hello World example and then tweaked it to fit my code (which is why the tests files--created as part of the scaffolding--don't fit the existing code).

A lot of similarities with serverless in the way it takes care of additional resource creation (IAM roles, etc) for you. Unlike serverless, it doesn't work with `pyproject.toml` files directly, so you need to generate a `requirements.txt` file before deploying.

Pros:

* Guided deploy to walks you through the process and generates a config file, which you can edit yourself directly afterward if you decide you want to change the region or S3 bucket, for example.
* Great local testing/invocation. In addition to local invoke, it also has an option to start a local version of API Gateway. Pretty nifty.

* It generates the S3 bucket for you automatically if you don't specify a deployment bucket, which is nice. It would be nicer if the bucket wasn't public, and also if versioning was disabled instead of enabled to make removing the S3 bucket easier down the line (see cons).

Cons:
* Deleting is kind of a pain. Serverless offers a `remove` option that deletes the function and--if applicable--the S3 bucket it created to deploy the function without any added work on your part.

  SAM, on the other hand, doesn't have a separate delete command. Instead you use the cloudformation cli to delete the stack, which is a little odd (why not write a separate SAM command that wraps around the cloudformation?) Even more annoying is that unlike serverless, it won't automatically delete the S3 bucket for you--you need to do that yourself. Which wouldn't be such a big deal except you need to 1) look up the stack name yourself via the CLI or console (SAM doesn't tell you the stack name for the S3 created bucket), 2) disable versioning on the bucket, 3) empty the S3 bucket, 4) delete the stack. This is especially annoying if I just deployed a hello world example and am now spending more time deleting the S3 bucket than I did setting everything up.

* Even though SAM provides a `sam logs` command, it assumes that you're creating the CloudWatch log group yourself: it doesn't automatically generate it for you. Not a huge deal, but some extra legwork.
* A slightly larger deal is that the AWS::Serverless::RestApi resource requires a `StageName` parameter, which defaults to Prod, but annoyingly, doesn't tell you how to specify the StageName you want in the generated README or the docs. It's not a lot of work to get around _once you know how to do so_ but figuring that part out took some digging since it's not in the docs or the README :/
* CloudFormation doesn't support reading Secure Strings from Parameter Store in lambda functions (this functionality only exists for a small subset of AWS services) so I never deployed a working version of the service. I ended up just changing the env vars to dummy values to test out deployment. It fully supports Secrets Manager though (untested here since it's not part of the free tier)
