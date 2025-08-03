from argparse import ArgumentParser, Namespace
from pathlib import Path

from translate.convert import po2md

SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    args = parser.parse_args()

    return args


def generate_translated_md(
    input_dir: Path, template_dir: Path, output_dir: Path
) -> None:
    po2md.main(
        [
            f"--input={input_dir}",
            f"--template={template_dir}",
            f"--output={output_dir}",
            "--fuzzy",
        ]
    )


if __name__ == "__main__":
    args = parse_args()

    for language in args.language_code:
        output_directory = SOURCE_DIR / language
        output_directory.mkdir(parents=True, exist_ok=True)

        generate_translated_md(
            input_dir=SOURCE_DIR / "locales" / language / "LC_MESSAGES",
            template_dir=SOURCE_DIR / "docs",
            output_dir=output_directory,
        )
        print(output_directory)
