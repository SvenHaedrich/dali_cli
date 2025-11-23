"""Test control device special commands."""

import pytest
from click.testing import CliRunner

from dali.DALI.system.constants import DaliMax
from dali.dali_cli import cli


@pytest.mark.parametrize(
    "command,opcode",
    [("dtr0", 0x30), ("dtr1", 0x31), ("dtr2", 0x32)],
)
def test_command_with_data(command, opcode):
    runner = CliRunner()
    # test broadcast
    for data in range(0x100):
        result = runner.invoke(cli, ["--mock", "device", command, str(data)])
        expect = 0xC10000 + (opcode << 8) + data
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\n"


@pytest.mark.parametrize(
    "command,opcode,send_twice",
    [("rand", 0x02, True)],
)
def test_simple_command(command, opcode, send_twice):
    runner = CliRunner()
    result = runner.invoke(cli, ["--mock", "device", command])
    if send_twice:
        expect = f"S2 18+{(0xC10000 + (opcode << 8)):06X}\n"
    else:
        expect = f"S2 18 {(0xC10000 + (opcode << 8)):06X}\n"
    assert result.exit_code == 0
    assert result.output == expect


def test_initialise():
    runner = CliRunner()
    # all
    result = runner.invoke(cli, ["--mock", "device", "init", "ALL"])
    assert result.exit_code == 0
    assert result.output == "S2 18+C101FF\n"
    # unaddressed
    result = runner.invoke(cli, ["--mock", "device", "init", "UN"])
    assert result.exit_code == 0
    assert result.output == "S2 18+C1017F\n"
    # address
    for address in range(0x40):
        result = runner.invoke(cli, ["--mock", "device", "init", str(address)])
        assert result.exit_code == 0
        assert result.output == f"S2 18+C101{address:02X}\n"


def test_command_testframe():
    runner = CliRunner()
    # default values
    result = runner.invoke(cli, ["--mock", "device", "testframe"])
    assert result.exit_code == 0
    assert result.output == "S2 18 C13305\n"
    # priorities
    for priority in range(1, 6):
        result = runner.invoke(cli, ["--mock", "device", "testframe", str(priority)])
        expect = 0xC13300 + priority
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\n"
    # test bad parameters
    result = runner.invoke(cli, ["--mock", "device", "testframe", "0"])
    assert result.exit_code == 2
