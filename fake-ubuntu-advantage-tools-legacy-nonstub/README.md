 
# Non-stub version (legacy)

This is the older version of fake-ubuntu-advantage-tools which does not provide stubs.  This is an internally simpler 
version of the workaround (no code), but comes at the cost of you having to manually apply patchfiles to other utilities 
that rely on the package, namely software-properties & update manager.

⚠️ **This method is no longer recommended for use since the [newer](https://github.com/Skyedra/UnspamifyUbuntu) stub 
version provides a cleaner installation method.**  (If you use the newer method, you will not have to apply patchfiles
to software-properties & update manager.)

# Remove Ubuntu APT Spam

## Spam Example

When running APT:

> Try Ubuntu Pro beta with a free personal subscription on up to 5 machines.
> Learn more at https://ubuntu.com/pro

## Removal Instructions -- Legacy Non-stub Option: Remove Ubuntu Advantage

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

### Patch Update Manager

Known supported versions:
- 20.04 Desktop (`updateManager2004.patch`)
- 22.04 Desktop (`updateManager2204.patch`)
- 23.04 Desktop (`updateManager2304.patch`)

UpdateManager in Ubuntu 23.04 now hooks into ubuntu advantage.  Chabala submitted a patch to make update manager function independently again.

First, test the patch can be applied cleanly (replace `updateManager2304.patch` with the patch for your version):

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/fake-ubuntu-advantage-tools-legacy-nonstub/updateManager2304.patch" | patch /usr/lib/python3/dist-packages/UpdateManager/UpdateManager.py --dry-run`

If that doesn't cause any errors, remove the `--dry-run` option to actually apply it:

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/fake-ubuntu-advantage-tools-legacy-nonstub/updateManager2304.patch" | patch /usr/lib/python3/dist-packages/UpdateManager/UpdateManager.py`

### Patch Software Properties GTK (for Ubuntu 22.04 Desktop only, not later)
`software-properties-gtk` now hooks into ubuntu advantage and crashes itself on start without it.  Muggenhor and reneas submitted patches to make it function independently again.

First, test the patch can be applied cleanly:

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/fake-ubuntu-advantage-tools-legacy-nonstub/software-properties-2204.patch" | patch -d/ -p0 --dry-run`

If that doesn't cause any errors, remove the --dry-run option to actually apply it:

`wget -O - "https://raw.githubusercontent.com/Skyedra/UnspamifyUbuntu/master/fake-ubuntu-advantage-tools-legacy-nonstub/software-properties-2204.patch" | patch -d/ -p0`


