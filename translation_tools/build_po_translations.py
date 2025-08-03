import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from translate.convert import pot2po

SOURCE_DIR = Path.cwd() / "locales"


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    args = parser.parse_args()

    for language_code in args.language_code:
        if not (SOURCE_DIR / f"{language_code}").is_dir():
            raise RuntimeError(
                f'Language code "{language_code}" does not match an existing translation'
            )

    return args


def merge_translation_files(
    source_dir: Path, template_dir: Path, destination_dir: Path
) -> None:
    pot2po.main(
        [
            f"--template={source_dir}",
            f"--input={template_dir}",
            f"--output={destination_dir}",
        ]
    )


def main():
    args = parse_args()

    with TemporaryDirectory() as in_progress_dir:
        with TemporaryDirectory() as final_dir:
            in_progress_dir = Path(in_progress_dir)
            final_dir = Path(final_dir)

            shutil.copytree(
                SOURCE_DIR / "templates", final_dir / "templates", dirs_exist_ok=True
            )

            for language in args.language_code:
                shutil.copytree(
                    SOURCE_DIR / language,
                    in_progress_dir / language,
                    dirs_exist_ok=True,
                )
                output_directory = final_dir / language / "LC_MESSAGES"
                output_directory.mkdir(parents=True)

                merge_translation_files(
                    source_dir=in_progress_dir / language / "LC_MESSAGES",
                    template_dir=final_dir / "templates",
                    destination_dir=final_dir / language / "LC_MESSAGES",
                )

            shutil.rmtree(SOURCE_DIR)
            shutil.copytree(final_dir, SOURCE_DIR)


if __name__ == "__main__":
    main()
