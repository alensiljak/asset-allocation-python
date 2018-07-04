""" Test runners for debugging """

# import click
# from click.testing import CliRunner
from asset_allocation import AppAggregate, AsciiFormatter


def test_text_output():
    """ Test the generation of asset allocation cli output """
    # runner = CliRunner()
    # result = runner.invoke(cli.show, ["ascii", False])
    # assert (result.exit_code == 0)
    # assert result.output
    app = AppAggregate()
    model = app.get_asset_allocation()

    formatter = AsciiFormatter()
    output = formatter.format(model, False)

    assert output
