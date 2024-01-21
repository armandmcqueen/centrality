# Canary

A script that queries the control plane + streamlit to check if it is working. If it is not, it can optionally trigger
a Pager Duty alert.


## Prod

Currently, the Fly deployment is the production deployment. The agent cluster is also part of the prod deployment.

## Canary deployment

The canary is deployed to Fly as a separate application. It is deployed using the `fly-canary.toml` config file.

## Failure of the canary

A failure in the canary is an alertable event that must be remediated immediately. Noisy alerts to begin 
with are fine. 

## PagerDuty

We use PagerDuty to alert if the canary fails. We use the `centrality.dev` PagerDuty account.

