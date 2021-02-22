# EquitEase
Access up-to-date price data for any of your favorite stocks from the command line

## Who is this Project For?
This project is for those who enjoy following day-to-day movements in the market, want to stay up-to-date on the latest price trends, and spend a majority of your time working in the terminal or with their terminal open.

## Getting Started
### Installation
Currently, you can install the CLI with `brew` or `pip`.
### With Brew
Initial Installation:
```shell
>>> brew tap danmurphy1217/equit-ease
>>> brew install danmurphy1217/equit-ease/equit-ease
```
Installing Updates:
```shell
>>> brew tap danmurphy1217/equit-ease
>>> brew upgrade danmurphy1217/equit-ease/equit-ease
```
### With Pip
Initial Installation:
```shell
>>> python3 -m venv venv # setup virtual env...
>>> source venv/bin/activate 
(venv) >>> pip install EquitEase
```
Installing Updates:
```shell
(venv) >>> pip install --upgrade EquitEase
```
### Verifying Installation
```shell
>>> equity --version # or equity -v
```
## Exploring the EquitEase CLI
### Getting Help
When in doubt, the `--help` / `-h` flag will return docs for each argument that is supported by the EquitEase CLI.
```shell
>>> equity --help
positional arguments:
  config
optional arguments:
  -h, --help
    [...]

  --force FORCE, -f FORCE
    [...]

  --name NAME, -n NAME
    [...]

  --list [LIST], -l [LIST]
    [...]

  --update [UPDATE], -u [UPDATE]
    [...]

  --version [VERSION], -v [VERSION]
    [...] 
```
### --name [-n]
...
### --force [-f]
...
### --list [-l]
...
### --update [-u]
...
### --version [-v]
...