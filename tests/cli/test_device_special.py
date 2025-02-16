"""Test control device speical commands."""

import pytest
from click.testing import CliRunner
from dali import cli
from DALI.system.constants import DaliMax


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
