"""Test control device query commands."""

import pytest
from click.testing import CliRunner
from dali.DALI.system.constants import DaliMax
from dali.dali_cli import cli


@pytest.mark.parametrize(
    "command, opcode",
    [
        ("capabilities", 0x46),
        ("dtr0", 0x36),
        ("dtr1", 0x37),
        ("dtr2", 0x38),
        ("quiescent", 0x40),
        ("status", 0x30),
        ("version", 0x34),
    ],
)
def test_query_device_command(command, opcode):
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "device", "query", command])
    expect = 0xFFFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "device", "query", command, "--adr", "BCU"])
    expect = 0xFDFE00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test short address
    for short in range(DaliMax.ADR):
        result = runner.invoke(cli, ["--mock", "device", "query", command, "--adr", str(short)])
        expect = 0x01FE00 + (short * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test group address
    for group in range(DaliMax.DEVICE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", "query", command, "--adr", f"G{group}"])
        expect = 0x81FE00 + (group * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"


@pytest.mark.parametrize(
    "command,opcode",
    [
        ("enabled", 0x86),
        ("error", 0x82),
        ("istatus", 0x83),
        ("primary", 0x88),
        ("resolution", 0x81),
        ("scheme", 0x8B),
    ],
)
def test_query_device_instance_command(command, opcode):
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "device", "query", command])
    expect = 0xFFFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "device", "query", command, "--adr", "BCU"])
    expect = 0xFDFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test short address
    for short in range(DaliMax.ADR):
        result = runner.invoke(cli, ["--mock", "device", "query", command, "--adr", str(short)])
        expect = 0x01FF00 + (short * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test group address
    for group in range(DaliMax.DEVICE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", "query", command, "--adr", f"G{group}"])
        expect = 0x81FF00 + (group * 0x20000) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test instance broadcast
    result = runner.invoke(cli, ["--mock", "device", "query", command, "--instance", "BC"])
    instance_byte = 0xFF << 8
    expect = 0xFF0000 + instance_byte + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test instance device
    result = runner.invoke(cli, ["--mock", "device", "query", command, "--instance", "DEVICE"])
    instance_byte = 0xFE << 8
    expect = 0xFF0000 + instance_byte + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test instance number
    for instance in range(DaliMax.INSTANCE_NUMBER):
        result = runner.invoke(
            cli,
            ["--mock", "device", "query", command, "--instance", str(instance)],
        )
        instance_byte = instance << 8
        expect = 0xFF0000 + instance_byte + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test instance groups
    for group in range(DaliMax.INSTANCE_GROUP):
        result = runner.invoke(cli, ["--mock", "device", "query", command, "--instance", f"G{group}"])
        instance_byte = (group + 0x80) << 8
        expect = 0xFF0000 + instance_byte + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
    # test instance types
    for typ in range(DaliMax.INSTANCE_TYPES):
        result = runner.invoke(cli, ["--mock", "device", "query", command, "--instance", f"T{typ}"])
        instance_byte = (typ + 0xC0) << 8
        expect = 0xFF0000 + instance_byte + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 18 {expect:X}\ntimeout - NO\n"
