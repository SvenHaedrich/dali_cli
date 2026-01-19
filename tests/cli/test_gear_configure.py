"""Test control gear configure commands."""

import pytest
from click.testing import CliRunner
from dali.dali_cli import cli


@pytest.mark.parametrize(
    "command,opcode",
    [
        ("reset", 0x20),
        ("actual", 0x21),
        ("id", 0x25),
        ("enable", 0x81),
    ],
)
def test_simple_gear_configure_command(command, opcode):
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "gear", command])
    expect = 0xFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 10+{expect:X}\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "gear", command, "--adr", "BCU"])
    expect = 0xFD00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 10+{expect:X}\n"
    # test short address
    for short in range(64):
        result = runner.invoke(cli, ["--mock", "gear", command, "--adr", str(short)])
        expect = 0x0100 + (short * 0x200) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 10+{expect:X}\n"
    # test group address
    for group in range(16):
        result = runner.invoke(cli, ["--mock", "gear", command, "--adr", f"G{group}"])
        expect = 0x8100 + (group * 0x200) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 10+{expect:X}\n"


@pytest.mark.parametrize(
    "command,opcode",
    [
        ("op", 0x23),
        ("reset_mem", 0x24),
        ("max", 0x2A),
        ("min", 0x2B),
        ("fail", 0x2C),
        ("on", 0x2D),
        ("time", 0x2E),
        ("rate", 0x2F),
        ("ext", 0x30),
    ],
)
def test_set_dtr_to_configure(command, opcode):
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "gear", command, "0"])
    expect = 0xFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 10 A300\nS2 10+{expect:X}\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "gear", command, "0", "--adr", "BCU"])
    expect = 0xFD00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 10 A300\nS2 10+{expect:X}\n"
    # test short address
    for short in range(64):
        result = runner.invoke(
            cli, ["--mock", "gear", command, "0", "--adr", str(short)]
        )
        expect = 0x0100 + (short * 0x200) + opcode
        assert result.exit_code == 0
        assert result.output == f"S2 10 A300\nS2 10+{expect:X}\n"
    # test group address
    for group in range(16):
        result = runner.invoke(
            cli, ["--mock", "gear", command, "0", "--adr", f"G{group}"]
        )
        expect = 0x8100 + (group * 0x200) + opcode
        assert result.exit_code == 0

        assert result.output == f"S2 10 A300\nS2 10+{expect:X}\n"


def test_set_short_address():
    runner = CliRunner()
    # test broadcast
    result = runner.invoke(cli, ["--mock", "gear", "short", "0"])
    expect = 0xFF80
    assert result.exit_code == 0
    assert result.output == f"S2 10 A301\nS2 10+{expect:X}\n"
    # test broadcast unaddressed
    result = runner.invoke(cli, ["--mock", "gear", "short", "0", "--adr", "BCU"])
    expect = 0xFD80
    assert result.exit_code == 0
    assert result.output == f"S2 10 A301\nS2 10+{expect:X}\n"
    # test short address
    for short in range(64):
        result = runner.invoke(
            cli, ["--mock", "gear", "short", "0", "--adr", str(short)]
        )
        expect = 0x0180 + (short * 0x200)
        assert result.exit_code == 0
        assert result.output == f"S2 10 A301\nS2 10+{expect:X}\n"
    # test group address
    for group in range(16):
        result = runner.invoke(
            cli, ["--mock", "gear", "short", "0", "--adr", f"G{group}"]
        )
        expect = 0x8180 + (group * 0x200)
        assert result.exit_code == 0
        assert result.output == f"S2 10 A301\nS2 10+{expect:X}\n"
