# conjur-auto-authn-enabler
Automatically enable authenticators for conjur. This will be run as a service on the conjur appliance.


## Installing the code

### From source
```bash
$ git clone https://github.com/AndrewCopeland/conjur-auto-authn-enabler.git
$ cd conjur-auto-authn-enabler; sudo docker cp ./authn-enabler conjur-master:/etc/service/authn-enabler
```

## Notes
* Once the authn-enabler directory has been copied into the appliance /etc/service directory it will be enabled and will start listening on a authenticators that are configured but are not enabled.
* A log file in this directory will be created for debugging.
* The application will look for configured authenticators using the `GET /info` endpoint every 5 seconds, when a new authenticator is found the application will set it in the `/opt/conjur/etc/conjur.conf` file and will restart the conjur service.

