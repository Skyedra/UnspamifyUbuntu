This page illustrates a number of steps to remove unwanted spam from Ubuntu.  

(In future, I would like to automate these steps by providing a command line program)

# Remove Ubuntu APT Spam

## Spam Example

When running APT:

> Try Ubuntu Pro beta with a free personal subscription on up to 5 machines.
> Learn more at https://ubuntu.com/pro

Additionally, step 5 also resolves this motd ad:

>  * Introducing Expanded Security Maintenance for Applications.
>   Receive updates to over 25,000 software packages with your
>   Ubuntu Pro subscription. Free for personal use.
>
>     https://ubuntu.com/pro

## Removal Instructions -- Option 1: Remove Ubuntu Advantage

To get rid of the spam, uninstall the program generating the spam.

The package that generates this spam is `ubuntu-advantage-tools`.  Unfortunately removing it is tricky since Ubuntu devs have decided to make this a required system package so they can make more money ([yes, that is their official justification](https://bugs.launchpad.net/ubuntu/+source/ubuntu-meta/+bug/1930914/comments/11)).

A clever person named vi0oss [came up with a workaround](https://old.reddit.com/r/assholedesign/comments/yg97tk/ubuntu_includes_ads_in_system_update_theyre/iuj7hug/):  replace the spammy package with an additional package which `Provides`, `Breaks` and `Conflicts` with `ubuntu-advantage-tools`.  When this fix broke due to Ubuntu devs requiring a later versionn, [gamemanj](https://old.reddit.com/r/assholedesign/comments/yg97tk/ubuntu_includes_ads_in_system_update_theyre/jbxyq01/) found a second workaround.  All this has been bundled into the latest version linked below.

1. Download the fake package [here](https://github.com/Skyedra/UnspamifyUbuntu/blob/master/fake-ubuntu-advantage-tools/fake-ubuntu-advantage-tools.deb?raw=true).
2. (Optional)  Verify package with `dpkg -I fake-ubuntu-advantage-tools.deb` to check the metadata to see how it works:
```
 new Debian package, version 2.0.
 size 744 bytes: control archive=384 bytes.
     300 bytes,     8 lines      control              
 Package: fake-ubuntu-advantage-tools 
 Version: 0.1
 Architecture: all
 Conflicts: ubuntu-advantage-tools
 Breaks: ubuntu-advantage-tools
 Provides: ubuntu-advantage-tools
 Description: Ban ubuntu-advantage-tools while satisfying ubuntu-minimal dependency
 Maintainer: Vitaly _Vi Shukela
```
3. (Optional) Verify package with `dpkg -c fake-ubuntu-advantage-tools.deb` to check it's actually empty:
```
drwxr-xr-x root/root         0 2022-10-31 11:58 ./
```
4. Install the package:  `apt install ./fake-ubuntu-advantage-tools.deb`
```
The following packages will be REMOVED:
  ubuntu-advantage-tools
The following NEW packages will be installed:
  fake-ubuntu-advantage-tools
0 upgraded, 1 newly installed, 1 to remove and 1 not upgraded.
```
5. Remove previously downloaded MOTD ads:
```
rm /var/lib/ubuntu-advantage/messages/motd-esm-announce
```
6. No more ads!


## Removal Instructions -- Option 2: Set Flag

If you need to keep Ubuntu Advantage installed (for instance, because you are using Ubuntu Pro extended support), you can use this somewhat secret command to hide the ads:

```
sudo pro config set apt_news=false
```

If you don't need pro features, I recommend Option 1 instead as the flag isn't well documented and may change in future (or I personally think it likely ubuntu advantage may add more types of spam with different flags in future requiring more undocumented flags be set.  Removing the source of the spam as in Option 1 seems more likely to fully nip the problem in the bud).

# Remove ESM MOTD Spam 

## Spam Example

On login, messages like this:

> Expanded Security Maintenance for Applications is not enabled.
>
> 0 updates can be applied immediately.
> 
> Enable ESM Apps to receive additional future security updates.
> See https://ubuntu.com/esm or run: sudo pro status

## Removal Instructions

These messages are defined in `/usr/lib/update-notifier/apt_check.py` with no flags to disable them.

Here's a sed command that will neuter the functions that generate the messages by inserting a return statement as the first line of the message function:

```
sudo sed -Ezi.orig \
  -e 's/(def _output_esm_service_status.outstream, have_esm_service, service_type.:\n)/\1    return\n/' \
  -e 's/(def _output_esm_package_alert.*?\n.*?\n.:\n)/\1    return\n/' \
  /usr/lib/update-notifier/apt_check.py
```

Now regenerate the file:
```
sudo /usr/lib/update-notifier/update-motd-updates-available --force
```


Discovered by [jwatson0](https://askubuntu.com/a/1456185) (more details there)



# Remove Dynamic MOTD Spam 

## Spam Example

On login, messages like this:

> Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s
>   just raised the bar for easy, resilient and secure K8s cluster deployment.
> https://ubuntu.com/engage/secure-kubernetes-at-the-edge

## Removal Instructions

### Option 1:  Manually

1. sudo vi /etc/default/motd-news
2. Change enabled=0	

### Option 2:  Via sed command

```
sudo sed -i 's/^ENABLED=.*/ENABLED=0/' /etc/default/motd-news
```
