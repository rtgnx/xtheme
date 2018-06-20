# XTHEME
Theme manager for people who are tired of writing tons of config files.
Inspired by [budRich/mondo](https://github.com/budRich/mondo).


### Install

```Bash

git clone https://github.com/rtnx/xtheme
cd xtheme
pip install --user .

```

### Themes

Theme files are in `toml` format. There's no requirements for them,
they are there for you to set variable that will be used later in generators.

### Generators

Generators include:

+ template.jinja2 - template for config file using variables from theme.
+ config.toml     - configuration file.
+ pre-apply.sh    - script executed before applying theme
+ post-apply.sh   - script executed after applying theme.

config.toml:

```Toml

[config]

  name = 'i3'
  target = '/home/rtgnx/.i3/config' # target file to which template is rendered

```
