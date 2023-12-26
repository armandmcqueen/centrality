# Deployment

## AWS

Currently we deploy to AWS on a single node, using docker-compose to simulate a cluster. 

The `iam.py` and `security_groups.py` code in this repo sets up the basic IAM and security group resources 
and saves them to `config.yaml`. The `instances.py` code launches instances, installs dependencies, checks 
out the code (potentially to a specific branch or commit), and then uses docker-compose to start a simulated
cluster.

The instances will automatically shut down after a certain amount of time, which can be configured with the
`--ttl-secs` flag. Note that this might not work correctly if the cloud-init script fails, but that should
only hopefully happen during development of this code.

### Getting started

Empty `config.yaml`, and set these fields:
```yaml
region: XXXXX
vpc_id: vpc-XXXXX
subnet_id: subnet-XXXXX
key_pair: XXXXX
```
The other fields will be automatically set.

Then run:
```bash
python iam.py create
python security_groups.py create
```

An environment variable can be set to specify an alternate config file location. See `constants.py` for the name 
of the environment variable.

### Launching instances

See `--help` for other options
```bash
python instances.py launch m7g.medium --checkout mybranch --idempotency-token mybranch
```
This will terminate any previous instances with the same idempotency token, launch new one, and run the
docker compose stack with the code in `mybranch`. Idempotency tokens are useful for reducing cost.

We keep a manual mapping between instance types and AMI (because there is an x64 ubuntu AMI and a 
different arm ubuntu AMI). If you want to use a different instance type, you need to add it to the
`INSTANCE_TO_AMI` dict in `constants.py`.


### Cleanup

To remove all resources created by this repo:
```
python instances.py delete
python security_groups.py delete
python iam.py delete
```




