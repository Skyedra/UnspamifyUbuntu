This page illustrates a number of steps to remove unwanted spam from Ubuntu.

# Remove Ubuntu APT Spam

## Spam Example

When running APT:

> Try Ubuntu Pro beta with a free personal subscription on up to 5 machines.
> Learn more at https://ubuntu.com/pro

## Removal Instructions -- Option 1: Install fake-ubuntu-advantage-tools (Recommended)

To get rid of the spam, replace the program generating the spam with a stub package.

The package that generates this spam is `ubuntu-advantage-tools`. Unfortunately removing it is tricky since Ubuntu devs have decided to make this a required system package so they can make more money ([yes, that is their official justification](https://bugs.launchpad.net/ubuntu/+source/ubuntu-meta/+bug/1930914/comments/11)).

A clever person named vi0oss [came up with a workaround](https://old.reddit.com/r/assholedesign/comments/yg97tk/ubuntu_includes_ads_in_system_update_theyre/iuj7hug/): replace the spammy package with an additional package which `Provides`, `Breaks` and `Conflicts` with `ubuntu-advantage-tools`. When this fix broke due to Ubuntu devs requiring a later version, [gamemanj](https://old.reddit.com/r/assholedesign/comments/yg97tk/ubuntu_includes_ads_in_system_update_theyre/jbxyq01/) found a second workaround.

The package includes minimal Python stubs that prevent crashes in Ubuntu system tools (UpdateManager, software-properties-gtk) that try to import ubuntu-advantage-tools modules. **No patches needed anymore!**

1. Download the fake package [here](https://github.com/Skyedra/UnspamifyUbuntu/blob/master/fake-ubuntu-advantage-tools/fake-ubuntu-advantage-tools.deb?raw=true).
2. (Optional) Verify package with `dpkg -I fake-ubuntu-advantage-tools.deb` to check the metadata:
```
 new Debian package, version 2.0.
 size 1998 bytes: control archive=592 bytes.
     989 bytes,    14 lines      control
 Package: fake-ubuntu-advantage-tools
 Version: 1.0
 Architecture: all
 Conflicts: ubuntu-advantage-tools, ubuntu-advantage-desktop-daemon, ubuntu-pro-client
 Breaks: ubuntu-advantage-tools, ubuntu-advantage-desktop-daemon, ubuntu-pro-client
 Provides: ubuntu-advantage-tools (= 65535:65535), ubuntu-advantage-desktop-daemon (= 65535:65535), ubuntu-pro-client (= 65535:65535)
 Description: Stub replacement for ubuntu-advantage-tools that prevents advertisements
  This package provides minimal Python stubs for the uaclient module to prevent
  crashes in Ubuntu system tools (UpdateManager, software-properties-gtk) when
  ubuntu-advantage-tools is not installed. No patches needed - just install this
  package to remove Ubuntu Pro advertisements while keeping system tools working.
 Maintainer: Originally by Vitaly _Vi Shukela <vi0oss@gmail.com>, this one updated by Skye with fix idea by gamemanj
 Homepage: https://github.com/Skyedra/UnspamifyUbuntu
```
3. (Optional) Verify package contents with `dpkg -c fake-ubuntu-advantage-tools.deb` to see the Python stubs it installs:
```
./usr/lib/python3/dist-packages/uaclient/__init__.py
./usr/lib/python3/dist-packages/uaclient/api/...
./usr/lib/python3/dist-packages/uaclient/api/u/pro/packages/updates/v1.py
(and other stub files)
```
4. Install the package: `apt install ./fake-ubuntu-advantage-tools.deb`
```
The following packages will be REMOVED:
  ubuntu-advantage-tools
The following NEW packages will be installed:
  fake-ubuntu-advantage-tools
0 upgraded, 1 newly installed, 1 to remove and 1 not upgraded.
```
5. **That's it!** No more ads and no patches needed! The Python stubs in the package ensure that UpdateManager and other system tools continue to work without modifications.

Optional:  The real `ubuntu-advantage-tools` seems to be the only package that depends on `distro-info`.  It does not appear to
be necessary to keep this tool, but if you want it, you can explicitly keep it installed via `apt install distro-info`.
If you do not, your system may prompt you to automatically remove it later on.

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

## Removal Instructions -- Option 2: Set Flag

If you need to keep Ubuntu Advantage installed (for instance, because you are using Ubuntu Pro extended support), you can use this somewhat secret command to hide the ads:

```
sudo pro config set apt_news=false
```

If you don't need pro features, I recommend Option 1 instead as the flag isn't well documented and may change in future (or I personally think it likely ubuntu advantage may add more types of spam with different flags in future requiring more undocumented flags be set.  Removing the source of the spam as in Option 1 seems more likely to fully nip the problem in the bud).

## Removal Instructions -- Option 3: Non-stub package (deprecated)

Similar to option #1, we also provide [instructions](fake-ubuntu-advantage-tools-legacy-nonstub) on how to swap ubuntu-advantage-tools out with a fake package that
contains no code.  However, this requires making modifications to software properties & update manager so it is no
longer recommended.

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
