import argparse as ap
import os

from src.tasks.stages import Stage

"""
Define the Command Line Interface of the module
"""

def cli_set_up() -> ap.ArgumentParser:
    """
    Parse the CLI.

    Args:
        - `-d`, `--scenario`, path of the input scenario, `default=None`,
        - `-n`, `--name`, name of the scenario scenario, `default=None`
        - `-s`, `--final-stage`, final stage of the run, `default=Stage.PREDICTION_BACKTESTED`

    :return: Parser object
    """

    parser = ap.ArgumentParser(description="Demand Forecast Package")

    parser.add_argument("-d", "--scenario",
                        help='path of the input scenario (Optional)', default=None)
    parser.add_argument("-n", "--name",
                        help='Name of the prediction', default="demand_prediction")
    parser.add_argument(
        "-s", "--final-stage", default=Stage.PREDICTION_BACKTESTED,
        choices=Stage.STAGES,
        help='final stage of the pipeline')
    return parser


def cli_read(parser: ap.ArgumentParser):
    """
    Check if the cli arguments are valid then return their value.

    :param parser: Parser of the cli set up.
    :return: scenario path and final_stage
    """

    args = parser.parse_args()

    if args.scenario is not None:
        if not os.path.isdir(args.scenario):
            raise FileNotFoundError(f'{args.scenario} was not found')

    if args.final_stage is None:
        final_stage = None
    else:
        final_stage = args.final_stage.upper()
        if not Stage.is_valid_stage(final_stage):
            raise AttributeError(f'{final_stage} is not a valid stage .\
             Stages : {list(map(lambda _: _.lower(), Stage.STAGES))}')

    return args.scenario, args.name, final_stage
