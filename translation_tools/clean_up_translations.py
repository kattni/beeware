import shutil
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


def remove_temporary_translation_files(language_code):
    shutil.rmtree(SOURCE_DIR / "_tmp" / f"{language_code}")


if __name__ == "__main__":
    args = parse_args()

    for language in args.language_code:
        remove_temporary_translation_files(language)
