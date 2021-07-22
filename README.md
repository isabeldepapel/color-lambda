# Comparing infra tooling: deploying a lambda + API Gateway (AWS)

## Background
I wanted to convert a _very_ simple [Flask backend](https://github.com/isabeldepapel/color-fogg/api) to a lambda and API Gateway and got curious about the different tools to deploy it. I've used [serverless](https://serverless.com) before, but I've never had the chance to play around with [Pulumi](https://pulumi.com) or [SAM](https://github.com/aws/aws-sam-cli) before, so here it is.

Also, this whole thing started because I wanted to get my Flask web app--a React frontend + Python backend--up using [Netlify](https://netlify.com) and realized the most straightforward way to do it was to convert the backend into a lambda. Time to shave some yaks!

<a href="https://sketchplanations.com/yak-shaving"><img src="./sketchplanations-yakshaving.png" alt="Drawing of someone shaving a yak with explanation text: 'Yak Shaving Doing Z to do Y to do X...So You can do A'" width=300></a>

## Requirements
The backend is essentially just one function that wraps around a particular query to the [Harvard Art Museums API](https://github.com/harvardartmuseums/api-docs). It takes in a query param and returns results in json; I really should have just written it as a lambda in the first place.

* Python version

  I'm using [poetry](https://python-poetry.org) to manage my virtual environment and requirements, version 3.8.6 since 3.8 is the highest version AWS lambda supports.
* Environment variables

  The function uses 2 API keys stored as environment variables: one for the Harvard Art Museums API, and one for [Honeycomb](https://honeycomb.io), the observability tooling I'm using (yes, I know this toy app with all of one user, me, doesn't need observability, but who doesn't like playing with shiny new toys?).

  I'm storing the API keys as secure strings in SSM Parameter Store. There's also Secrets Manager, and if I were running super secret things in a production environment, I'd probably opt for Secrets Manager, but since Secrets Manager isn't in the free tier (it does have a 30-day free trial though) and Parameter Store is, guess which one I'm going with. I need to save all my pennies to pay the government back its bazillion dollars of student loan interest.

  (Why am I delineating all this in painstaking detail? Turns out my choice of Parameter Store mattered more than I thought when I tried to deploy things!)


## Tools
1. [Serverless](./serverless/)
1. [SAM](./sam/)
1. Terraform
1. Pulumi
