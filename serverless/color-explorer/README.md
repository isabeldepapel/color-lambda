# Deploying with Serverless

I've used serverless before (for node functions), but never with an API Gateway, so even though this is the framework I'm (most) familiar with, there's still some new stuff to learn!

First up, deploying a python function. I've never user serverless with python before, so I just used the ready-made example of a [python Flask API](https://github.com/serverless/examples/tree/master/aws-python-flask-api) and then tweaked it from there.


Pros:
* Incredibly easy to set up (just tweak some boilerplate!)
* No need to use poetry to generate a `requirements.txt` file since it parses `pyproject.toml` directly.
* Setting it up to read SSM parameters was also pretty straightforward. (This became even more impressive when I tried to use SAM and realized AWS's own tooling *doesn't support* reading SSM Secure Strings from CloudFormation templates for lambda functions:sad-face:)

  N.B. I have the API keys stored locally as an .env file. When I deploy, serverless confusingly prints out the message that in the future (v3 and up), env files will be automatically loaded, and prints directions on how to enable that feature now. If you're thinking, why not just load the env vars from a file then? Well, it turns out the env vars are only loaded _locally_ as a kind of config for deployment, they're NOT injected as env vars into the lambda. It took a few minutes to dig out that information though because the docs don't make this clear at all.

* Deploying is pretty straightforward and it helpfully creates an S3 bucket for you to dump the lambda code if you don't already have one created. It would be nice if the created bucket had public access disabled though. And unlike SAM, serverless will remove the bucket it created when you remove the function, which makes for easier cleanup (no having to worry about stray AWS resources in a free tier).

Cons:
* For whatever reason, I never got `invoke local` to work, I'm guessing because it's not properly interacting with poetry for whatever reason. The virtual environment was activated, and the modules definitely installed, which I confirmed by running my file locally, but when I tried to invoke the function, I kept getting module not found errors. :shoulder-shrug: Ah, python. (P.S. If you know what the problem is, and/or how to fix, let me know!)

* About those env vars... For SSM parameters that are stored as `Secure String` (as opposed to just an unencrypted `String`), CloudFormation (won't store the actual parameter value, or return it in an API call (so that your secret information isn't just floating around in plain text). This is good! (Not so good: CloudFormation only supports accessing secure strings with a very limited number of resources, and that doesn't include lambda.)

  However, although serverless will let you retrieve secure strings, it makes no effort to not print them out. They're stored in plain text in the CloudFormation templates and serverless state files generated upon deployment. You generally don't commit those to the repo so that's not good but not terrible, BUT the cloudformation template that's uploaded to AWS to generate the stack has the API keys in plain text there as well. Not great.

* The generated templates that are uploaded to CloudFormation for you lose their formatting so it looks like one giant string filled with curly braces, colons, and commas. Makes it harder to suss out values for debugging.