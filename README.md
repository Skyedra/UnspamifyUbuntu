This page illustrates a number of steps to remove unwanted spam from Ubuntu.  

(In future, I would like to automate these steps by providing a command line program)

# Remove Ubuntu APT Spam

## Spam Example

When running APT:

> Try Ubuntu Pro beta with a free personal subscription on up to 5 machines.
> Learn more at https://ubuntu.com/pro

## Removal Instructions -- Option 1: Remove Ubuntu Advantage

To get rid of the spam, uninstall the program generating the spam.

The package that generates this spam is `ubuntu-advantage-tools`.  Unfortunately removing it is tricky since Ubuntu devs have decided to make this a required system package so they can make more money ([yes, that is their official justification](https://bugs.launchpad.net/ubuntu/+source/ubuntu-meta/+bug/1930914/comments/11)).

A clever person named vi0oss [came up with a workaround](https://old.reddit.com/r/assholedesign/comments/yg97tk/ubuntu_includes_ads_in_system_update_theyre/iuj7hug/):  replace the spammy package with an additional package which `Provides`, `Breaks` and `Conflicts` with `ubuntu-advantage-tools`.  When this fix broke due to Ubuntu devs requiring a later versionn, [gamemanj](https://old.reddit.com/r/assholedesign/comments/yg97tk/ubuntu_includes_ads_in_system_update_theyre/jbxyq01/) found a second workaround.  All this has been bundled into the latest version linked below.

1. Download the fake package [here](https://github.com/Skyedra/UnspamifyUbuntu/blob/master/fake-ubuntu-advantage-tools/fake-ubuntu-advantage-tools.deb?raw=true).
2. (Optional)  Verify package with `dpkg -I fake-ubuntu-advantage-tools.deb` to check the metadata to see how it works:
```
 new Debian package, version 2.0.
 size 658 bytes: control archive=387 bytes.
     550 bytes,     9 lines      control              
 Package: fake-ubuntu-advantage-tools 
 Version: 0.3
 Architecture: all
 Conflicts: ubuntu-advantage-tools, ubuntu-advantage-desktop-daemon
 Breaks: ubuntu-advantage-tools, ubuntu-advantage-desktop-daemon
 Provides: ubuntu-advantage-tools (= 65535:65535), ubuntu-advantage-desktop-daemon (= 65535:65535)
 Description: Ban ubuntu-advantage-tools while satisfying ubuntu-minimal dependency
 Maintainer: Originally by Vitaly _Vi Shukela <vi0oss@gmail.com>, this one updated by Skye with fix idea by gamemanj
 Homepage: https://github.com/Skyedra/UnspamifyUbuntu
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
5. No more ads!

### Prevent APT trying to start spammy uninstalled services

You may start to get these warnings:

```
root@lab:~# apt update
Failed to start apt-news.service: Unit apt-news.service is masked.
Failed to start esm-cache.service: Unit esm-cache.service not found.
```

You can resolve this by disabling the spam hooks in APT:

```
sudo mv /etc/apt/apt.conf.d/20apt-esm-hook.conf /etc/apt/apt.conf.d/20apt-esm-hook.conf.disabled
```

### Patch Update Manager (for Ubuntu 23.04+ Desktop only)
UpdateManager in Ubuntu 23.04 now hooks into ubuntu advantage.  Chabala submitted a patch to make update manager function independently again.

First, test the patch can be applied cleanly:

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/updateManager2304.patch" | patch /usr/lib/python3/dist-packages/UpdateManager/UpdateManager.py --dry-run`

If that doesn't cause any errors, remove the --dry-run option to actually apply it:

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/updateManager2304.patch" | patch /usr/lib/python3/dist-packages/UpdateManager/UpdateManager.py`

### Patch Software Properties GTK (for Ubuntu 22.04 Desktop only, not later)
`software-properties-gtk` now hooks into ubuntu advantage and will cause a crash.  Muggenhor and reneas submitted patches to make it function independently again.

First, test the patch can be applied cleanly:

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/software-properties-2204.patch" | patch -d/ -p0 --dry-run`

If that doesn't cause any errors, remove the --dry-run option to actually apply it:

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/software-properties-2204.patch" | patch -d/ -p0`

## Removal Instructions -- Option 2: Set Flag

If you need to keep Ubuntu Advantage installed (for instance, because you are using Ubuntu Pro extended support), you can use this somewhat secret command to hide the ads:

```
sudo pro config set apt_news=false
```

If you don't need pro features, I recommend Option 1 instead as the flag isn't well documented and may change in future (or I personally think it likely ubuntu advantage may add more types of spam with different flags in future requiring more undocumented flags be set.  Removing the source of the spam as in Option 1 seems more likely to fully nip the problem in the bud).

# Remove ESM Apps MOTD Spam 

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


# Remove MOTD ESM Announce Spam

## Spam Example

On login, messages like this:

>  * Introducing Expanded Security Maintenance for Applications.
>   Receive updates to over 25,000 software packages with your
>   Ubuntu Pro subscription. Free for personal use.
>
>     https://ubuntu.com/pro

## Removal Instructions

### Option 1:  Remove UA + Cache

This method is best if you don't use ubuntu ESM / don't need ubuntu pro.

1. Follow [previous instructions](https://github.com/Skyedra/UnspamifyUbuntu#removal-instructions----option-1-remove-ubuntu-advantage) to remove ubuntu advantage and instead use the fake ubuntu advantage package.  

2. Remove previously downloaded/cached MOTD ads:
```
rm /var/lib/ubuntu-advantage/messages/motd-esm-announce
```

### Option 2:  Modify motd hooks
If you need ubuntu advantage installed for some reason, you might try modifying `/etc/update-motd.d/88-esm-annouce` so it does not return anything.  For instance, making the top of the file like:
```
#!/bin/sh
exit 0
```
should remove the spam.  Using this method, you may get update conflicts to resolve when/if ubuntu changes this file.  (Unfortunately, they don't appear to have made this type of spam configurable, like they did the update-motd spam.)
