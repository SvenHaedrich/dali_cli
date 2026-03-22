"""Test control gear query commands."""

import pytest
from click.testing import CliRunner
from dali.DALI.system.constants import DaliMax
from dali.dali_cli import cli


@pytest.mark.parametrize(
    "command, opcode",
    [
        ("status", 0x90),
        ("missing", 0x96),
    ],
)
def test_query_device_command(command, opcode):
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "gear", "query", command])
    expect = 0xFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 10 {expect:X}\ntimeout - NO\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "gear", "query", command, "--adr", "BCU"])
    expect = 0xFD00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 10 {expect:X}\ntimeout - NO\n"
    # test short address
    for short in range(DaliMax.ADR):
        result = runner.invoke(cli, ["--mock", "gear", "query", command, "--adr", str(short)])
        expect = 0x0100 + (short * 0x200) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 10 {expect:X}\ntimeout - NO\n"
    # test group address
    for group in range(DaliMax.GEAR_GROUP):
        result = runner.invoke(cli, ["--mock", "gear", "query", command, "--adr", f"G{group}"])
        expect = 0x8100 + (group * 0x200) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 10 {expect:X}\ntimeout - NO\n"
