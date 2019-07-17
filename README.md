
# Prelude

The experiment is legacy from a long time ago in a galaxy far away...
What do I mean about that?
Well, it uses the window system "WX", to comply with legacy code, but was later abandoned in favour of "Qt" only to adhere to the system most used in the group.

# Install

## Dependencies

```
sudo apt install python-{setuptools,matplotlib}
sudo pip install minimalmodubs, wxPython, wxmplot
```


## Modules

The module is located on GitHub.
It is recomended to keep the git repository in the "HOME" folder such that changes can be reported to the master.
The following commands stores the repository as "HOME/Git/<REPOSITORY>" and installs the module in the system "root".

```
git clone "https://github.com/sigveka/RTD.git" "${HOME}/Git/RTD"
cd "${HOME}/Git/RTD"
python setup.py build
sudo python setup.py install
```

the experiment can now be run as a module:

```
python -m RTD
```

This is the current setup, but the "setuptools" option "entry_point" should probably be used in the future.

