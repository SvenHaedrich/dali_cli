# DALI cli

Command line interface to control a DALI system.

DALI is the digital addressable lighting interface as described [here](https://www.dali-alliance.org).

## Usage

To transmit a gear OFF command to the DALI bus you enter the following.

```shell
dali --serial-port /dev/ttyUSB0 off
```

This will transmit the control gear command OFF, using broadcast
addressing, via an adapter connected to the serial port.
Alternatively, you can use a Lunatone or BEGA adapter.

```shell
dali --hid off
```

Usually,
you will operate with a single bus interface. You can use an
environment variable to set it once.

```shell
export DALI_SERIAL_PORT=/dev/ttyUSB0
dali max
dali min
dali off
```

Use optional addressing to direct DALI commands to single controllers
attached to the bus.

```shell
dali dapc 100 --adr G0
```

Use the `--help` option to learn more about available commands.

```shell
dali --help
```

Some commands support further parameters. Again, the help option let
you explore the available commands and their usage. Note that most commands for DALI control gears are grouped under the `gear` command,
while control device commands are grouped under the `device` command.

```shell
dali gear --help
```

The commands are structured like a tree. For instance the following
command queries a control gear's status.

```shell
dali gear query status
status: 4 = 0x04 = 00000100b
bit : description
  0 : controlGearFailure
  0 : lampFailure
  1 : lampOn
  0 : limitError
  0 : fadeRunning
  0 : resetState
  0 : shortAddress is MASK
  0 : powerCycleSeen
```

## Supported Hardware

* Lunatone 241 389 23DO
* BEGA 71024
* [Serial based SevenLab Hardware](https://github.com/SvenHaedrich/dali_usb_lpc1114)

## Tests

This script:
```bash
./test_dali_cli.sh
```
prepares a vritual environment, and then runs the tests. Optionally you can
add `--log-level=debug` for more detailled logging.


## Install from github

```shell
git clone git@github.com:SvenHaedrich/dali_cli.git
cd dali_cli
git submodule update --init
python3 -m venv --prompt dali .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools
python3 -m build
python3 -m pip install --editable .
```

