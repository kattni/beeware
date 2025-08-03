import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path

SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    args = parser.parse_args()
    for language_code in args.language_code:
        if not (SOURCE_DIR / "locales" / f"{language_code}").is_dir():
            raise RuntimeError(
                f'Language code "{language_code}" does not match an existing translation'
            )

    return args


def build_docs(config_file: Path, build_dir: Path) -> None:
    subprocess.run(
        [
            "python",
            "-m",
            "mkdocs",
            "build",
            "--clean",
            "--config-file",
            f"{config_file}",
            "--site-dir",
            f"{build_dir}",
        ],
        check=True,
    )


if __name__ == "__main__":
    args = parse_args()

    for language in args.language_code:

        build_docs(
            config_file=SOURCE_DIR / "docs" / "config" / f"mkdocs.{language}.yml",
            build_dir=SOURCE_DIR / "_build" / "html" / f"{language}",
        )
