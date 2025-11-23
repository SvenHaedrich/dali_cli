"""Test control gear special commands."""

import pytest
from click.testing import CliRunner

from dali.dali_cli import cli


@pytest.mark.parametrize(
    "command,address_byte,twice",
    [
        ("term", 0xA1, " "),
        ("rand", 0xA7, "+"),
        ("withdraw", 0xAB, " "),
        ("ping", 0xAD, " "),
    ],
)
def test_simple_special_command(command, address_byte, twice):
    runner = CliRunner()
    result = runner.invoke(cli, ["--mock", "gear", command])
    expect = address_byte << 8
    assert result.exit_code == 0
    assert result.output == f"S2 10{twice}{expect:X}\n"


@pytest.mark.parametrize(
    "command,address_byte",
    [
        ("dtr0", 0xA3),
        ("dt", 0xC1),
        ("dtr1", 0xC3),
        ("dtr2", 0xC5),
        ("noreply", 0xC9),
    ],
)
def test_special_command_with_parameter(command, address_byte):
    runner = CliRunner()
    for data in range(0x100):
        result = runner.invoke(cli, ["--mock", "gear", command, str(data)])
        expect = (address_byte << 8) + data
        assert result.exit_code == 0
        assert result.output == f"S2 10 {expect:X}\n"
