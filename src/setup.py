from typing import Optional

import click


@click.command()
@click.option("--shout", help="what do you mad about")
def hello(shout: Optional[str]) -> None:
    print(shout or "Hello, World!")


if __name__ == "__main__":
    hello()
