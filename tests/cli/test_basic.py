import pytest
from click.testing import CliRunner
from dali import cli


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == "dali, version 0.0.9\n"


def test_dapc_bc_command():
    runner = CliRunner()
    for level in range(0x100):
        result = runner.invoke(cli, ["--mock", "dapc", str(level)])
        assert result.exit_code == 0
        assert result.output == f"S2 10 FE{level:02X}\n"
    result = runner.invoke(cli, ["mock", "dapc", "256"])
    assert result.exit_code == 2


def test_dapc_for_short_addresses():
    runner = CliRunner()
    for short in range(64):
        for level in range(0x100):
            result = runner.invoke(
                cli, ["--mock", "dapc", str(level), "--adr", str(short)]
            )
            code = level + short * 0x200
            assert result.exit_code == 0
            assert result.output == f"S2 10 {code:X}\n"


@pytest.mark.parametrize(
    "command,opcode",
    [
        ("off", 0x00),
        ("up", 0x01),
        ("down", 0x02),
        ("max", 0x05),
        ("min", 0x06),
    ],
)
def test_top_commands(command, opcode):
    runner = CliRunner()
    result = runner.invoke(cli, ["--mock", command])
    expect = 0xFF00 + opcode
    assert result.exit_code == 0
    assert result.output == f"S2 10 {expect:X}\n"


def test_goto_scene():
    runner = CliRunner()
    for scene in range(16):
        result = runner.invoke(cli, ["--mock", "goto", str(scene)])
        code = 0xFF10 + scene
        assert result.exit_code == 0
        assert result.output == f"S2 10 {code:X}\n"
