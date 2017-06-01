# Usage notes

This repository contains a skeleton flask app that is deployed via a heat template.
Instead of using a deploy key, the heat template configures a git repository on
the instance, and attaches a post-receive hook to the master branch of the git
repository.

## configuration

Edit the values in `heat.env.yml` to your own preferences. For more details on
all available parameters, scan through `heat.yml`.

## deploying the instance

Use the `heat.yml` and `heat.env.yml` files to deploy the instance and then take
note of the floating ip address.

## deploying / updating the application

### 1. Add remote to your current repository

```bash
# this adds a new remote called "deploy"
git remote add deploy debian@floatingip:/repo
# this causes your pushes and pulls to track the master branch on "deploy"
push -u deploy master
# You will need to change this setting to push/pull from cisgitlab:
push -u origin master
```

### 2. Commit changes to the master branch and push to "deploy"

The above name "deploy" is arbitrary -- you could pick "joe" if it suits you.
However, for the purpose of this document, we will assume "deploy"


```bash
git add -A .
git commit -m 'new changes made to application'
git push
```

Each push will trigger `run.sh`, which will rebuild and restart the
application.


### 3. Verify connectivity

Make sure you can view the web page at http://floatingip/


## Troubleshooting

It takes a couple of minutes to deploy the instance. 
If you are in doubt, log in at debian@floatingip and run the following:

```bash
tail -f /var/log/cloud-init-output.log
# or alternatively...
less /var/log/cloud-init-output.log
```

If the instance appears to have been deployed properly, you can then check the
application directory as follows:

```bash
cd /deploy
docker-compose ps
docker-compose logs
# or to get running output...
docker-compose logs -f
```
