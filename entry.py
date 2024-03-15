import logging
import subprocess
import sys

def compile_typst_file(filename: str, options: list[str]) -> bool:
    """Compiles a Typst file with the specified global options.

    Args:
        filename: The name of the Typst file to compile.
        options: A list of global options for the Typst compiler.

    Returns:
        True if the compilation was successful, False otherwise.
    """
    command = ["typst"] + options + ["compile", filename]
    logging.debug("Running: %s", " ".join(command))

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Compiling %s failed with stderr:\n%s", filename, e.stderr)
        return False
    except Exception as e:
        logging.error("An error occurred while compiling %s: %s", filename, str(e))
        return False

def main():
    logging.basicConfig(level=logging.INFO)

    files = sys.argv[1].splitlines()
    options = sys.argv[2].splitlines()

    try:
        version = subprocess.run(["typst", "--version"], capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Failed to get Typst version with stderr:\n%s", e.stderr)
        sys.exit(1)

    logging.info("Using Typst version: %s", version)

    success = {}

    for filename in files:
        filename = filename.strip()
        if not filename:
            continue
        logging.info("Compiling %s…", filename)
        success[filename] = compile_typst_file(filename, options)

    for filename, was_successful in success.items():
        logging.info("%s: %s", filename, '✔' if was_successful else '❌')

    if not all(success.values()):
        logging.error("Some files failed to compile.")
        sys.exit(1)

if __name__ == "__main__":
    main()
