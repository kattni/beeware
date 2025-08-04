import shutil
import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from translate.convert import po2md

SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language-code", nargs="*")
    parser.add_argument("--output", default=SOURCE_DIR / "_build" / "html")
    args = parser.parse_args()
    for language_code in args.language_code:
        if not (SOURCE_DIR / "locales" / f"{language_code}").is_dir():
            raise RuntimeError(
                f'Language code "{language_code}" does not match an existing translation'
            )

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

    with TemporaryDirectory() as temp_md_directory:
        temp_md_directory = Path(temp_md_directory)

        for language in args.language_code:
            output_directory = temp_md_directory / language
            output_directory.mkdir(parents=True, exist_ok=True)

            # Copy config files to temp directory. docs_dir and INHERIT paths are
            # relative, so to build translations successfully while allowing English
            # to build on its own, files must be available relative to the build.
            shutil.copy(
                SOURCE_DIR / "docs" / f"mkdocs.{language}.yml",
                temp_md_directory,
            )
            shutil.copy(SOURCE_DIR / "docs" / "config.yml", temp_md_directory)
            shutil.copy(
                SOURCE_DIR / "docs" / "spelling_wordlist.txt", temp_md_directory
            )

            generate_translated_md(
                input_dir=SOURCE_DIR / "locales" / language / "LC_MESSAGES",
                template_dir=SOURCE_DIR / "docs",
                output_dir=output_directory,
            )

            build_docs(
                config_file=temp_md_directory / f"mkdocs.{language}.yml",
                build_dir=Path(args.output) / f"{language}",
            )
