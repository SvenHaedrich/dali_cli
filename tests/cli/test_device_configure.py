"""Test control device configure commands."""

import pytest
from click.testing import CliRunner

from dali.DALI.system.constants import DaliMax
from dali.dali_cli import cli


def test_set_short_command():
    runner = CliRunner()
    opcode = 0x14
    # test broadcast
    result = runner.invoke(cli, ["--mock", "device", "short", "0"])
    expect = 0xFFFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 C13000\nS2 18+{expect:X}\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "device", "short", "0", "--adr", "BCU"])
    expect = 0xFDFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 C13000\nS2 18+{expect:X}\n"
    # test short address
    for short in range(DaliMax.ADR):
        result = runner.invoke(cli, ["--mock", "device", "short", "0", "--adr", str(short)])
        expect = 0x01FE00 + (short * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 C13000\nS2 18+{expect:X}\n"
    # test group address
    for group in range(DaliMax.DEVICE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", "short", "0", "--adr", f"G{group}"])
        expect = 0x81FE00 + (group * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 C13000\nS2 18+{expect:X}\n"


@pytest.mark.parametrize(
    "command,opcode",
    [
        ("start", 0x1D),
        ("stop", 0x1E),
        ("reset", 0x10),
    ],
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
    "command,opcode,argument",
    [("primary", 0x64, 0), ("scheme", 0x67, 0)],
)
def test_instance_device_configure_command(command, opcode, argument):
    runner = CliRunner()
    # test address broadcast
    result = runner.invoke(cli, ["--mock", "device", command, str(argument)])
    expect = 0xFFFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test address broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "device", command, str(argument), "--adr", "BCU"])
    expect = 0xFDFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test address short address
    for short in range(DaliMax.ADR):
        result = runner.invoke(cli, ["--mock", "device", command, str(argument), "--adr", str(short)])
        expect = 0x01FF00 + (short * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test address group address
    for group in range(DaliMax.DEVICE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", command, str(argument), "--adr", f"G{group}"])
        expect = 0x81FF00 + (group * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test instance broadcast
    result = runner.invoke(cli, ["--mock", "device", command, str(argument), "--instance", "BC"])
    instance_byte = 0xFF << 8
    expect = 0xFF0000 + instance_byte + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test instance device
    result = runner.invoke(cli, ["--mock", "device", command, str(argument), "--instance", "DEVICE"])
    instance_byte = 0xFE << 8
    expect = 0xFF0000 + instance_byte + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test instance number
    for instance in range(DaliMax.INSTANCE_NUMBER):
        result = runner.invoke(
            cli,
            ["--mock", "device", command, str(argument), "--instance", str(instance)],
        )
        instance_byte = instance << 8
        expect = 0xFF0000 + instance_byte + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test instance groups
    for group in range(DaliMax.INSTANCE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", command, str(argument), "--instance", f"G{group}"])
        instance_byte = (group + 0x80) << 8
        expect = 0xFF0000 + instance_byte + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"
    # test instance types
    for typ in range(DaliMax.INSTANCE_TYPES):
        result = runner.invoke(cli, ["--mock", "device", command, str(argument), "--instance", f"T{typ}"])
        instance_byte = (typ + 0xC0) << 8
        expect = 0xFF0000 + instance_byte + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {(argument + 0xC13000):X}\nS2 18+{expect:X}\n"


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
        result = runner.invoke(cli, ["--mock", "device", command, str(group), "--adr", "BCU"])
        assert result.exit_code == 0
        data_set = 0xC90000 + (1 << (group - low))
        data_cmd = 0xFDFE00 + opcode
        assert result.output == f"S2 18 {data_set:X}\nS2 18+{data_cmd:X}\n"
    # test short address
    for short in range(DaliMax.ADR):
        for group in range(low, high):
            result = runner.invoke(cli, ["--mock", "device", command, str(group), "--adr", str(short)])
            assert result.exit_code == 0
            data_set = 0xC90000 + (1 << (group - low))
            data_cmd = 0x01FE00 + (short * 0x20000) + opcode
            assert result.output == f"S2 18 {data_set:X}\nS2 18+{data_cmd:X}\n"
    # test group address
    for short in range(DaliMax.DEVICE_GROUP):
        for group in range(low, high):
            result = runner.invoke(cli, ["--mock", "device", command, str(group), "--adr", f"G{group}"])
            assert result.exit_code == 0
            data_set = 0xC90000 + (1 << (group - low))
            data_cmd = 0x81FE00 + (group * 0x20000) + opcode
            assert result.output == f"S2 18 {data_set:X}\nS2 18+{data_cmd:X}\n"


@pytest.mark.parametrize(
    "command,argument,opcode",
    [
        ("application", "true", 0x16),
        ("application", "false", 0x17),
        ("cycle", "true", 0x1F),
        ("cycle", "false", 0x20),
    ],
)
def test_device_configure_command_w_argument(command, argument, opcode):
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "device", command, argument])
    expect = 0xFFFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18+{expect:X}\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "device", command, argument, "--adr", "BCU"])
    expect = 0xFDFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18+{expect:X}\n"
    # test short address
    for short in range(DaliMax.ADR):
        result = runner.invoke(cli, ["--mock", "device", command, argument, "--adr", str(short)])
        expect = 0x01FE00 + (short * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18+{expect:X}\n"
    # test group address
    for group in range(DaliMax.DEVICE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", command, argument, "--adr", f"G{group}"])
        expect = 0x81FE00 + (group * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18+{expect:X}\n"
