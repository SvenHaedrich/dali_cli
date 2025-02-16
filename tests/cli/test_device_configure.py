"""Test control device configure commands."""

import pytest
from click.testing import CliRunner
from dali import cli
from DALI.system.constants import DaliMax


@pytest.mark.parametrize(
    "command,opcode",
    [("start", 0x1D), ("stop", 0x1E)],
)
def test_simple_device_configure_command(command, opcode):
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "device", command])
    expect = 0xFFFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18+{expect:X}\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "device", command, "--adr", "BCU"])
    expect = 0xFDFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18+{expect:X}\n"
    # test short address
    for short in range(DaliMax.ADR):
        result = runner.invoke(cli, ["--mock", "device", command, "--adr", str(short)])
        expect = 0x01FE00 + (short * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18+{expect:X}\n"
    # test group address
    for group in range(DaliMax.DEVICE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", command, "--adr", f"G{group}"])
        expect = 0x81FE00 + (group * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18+{expect:X}\n"


@pytest.mark.parametrize(
    "command,opcode,low,high",
    [
        ("add", 0x19, 0, 16),
        ("add", 0x1A, 16, 32),
        ("ungroup", 0x1B, 0, 16),
        ("ungroup", 0x1C, 16, 32),
    ],
)
def test_device_group_command(command, opcode, low, high):
    runner = CliRunner()
    # test broadcast
    for group in range(low, high):
        result = runner.invoke(cli, ["--mock", "device", command, str(group)])
        assert result.exit_code == 0
        data_set = 0xC90000 + (1 << (group - low))
        data_cmd = 0xFFFE00 + opcode
        assert result.output == f"S2 18 {data_set:X}\nS2 18+{data_cmd:X}\n"
    # test broadcast unaddressed
    for group in range(low, high):
        result = runner.invoke(
            cli, ["--mock", "device", command, str(group), "--adr", "BCU"]
        )
        assert result.exit_code == 0
        data_set = 0xC90000 + (1 << (group - low))
        data_cmd = 0xFDFE00 + opcode
        assert result.output == f"S2 18 {data_set:X}\nS2 18+{data_cmd:X}\n"
    # test short address
    for short in range(DaliMax.ADR):
        for group in range(low, high):
            result = runner.invoke(
                cli, ["--mock", "device", command, str(group), "--adr", str(short)]
            )
            assert result.exit_code == 0
            data_set = 0xC90000 + (1 << (group - low))
            data_cmd = 0x01FE00 + (short * 0x20000) + opcode
            assert result.output == f"S2 18 {data_set:X}\nS2 18+{data_cmd:X}\n"
    # test group address
    for short in range(DaliMax.DEVICE_GROUP):
        for group in range(low, high):
            result = runner.invoke(
                cli, ["--mock", "device", command, str(group), "--adr", f"G{group}"]
            )
            assert result.exit_code == 0
            data_set = 0xC90000 + (1 << (group - low))
            data_cmd = 0x81FE00 + (group * 0x20000) + opcode
            assert result.output == f"S2 18 {data_set:X}\nS2 18+{data_cmd:X}\n"
