#!/usr/bin/python3

import click
import re

@click.command()
@click.option(
    "-l", "--language", default="pa",
    help="Language definition, 'papaština' used by default.")
@click.argument("filename")
def translate(language, filename):
    """
    The syllable language translator.

    It is possible to use arbitrary syllable to construct new languages.
    For example the following syllables make a very nice sound :-)

    \b
    pa ... papaština
    ng ... ngština
    rg ... rgština
    """

    # Remove any syllable-forming suffix from the language
    lang = re.sub("[aeiouylr]*$", "", language)

    for line in open(filename):
        # Use lower case and short vowels
        line = line.strip().lower()
        line = line.translate(str.maketrans("áéíóúůý", "aeiouuy"))

        # Syllable-forming "l" and "r" with no vowels around
        # petr --> pepetrpr, ale per --> peper
        line = re.sub("(?<![aeiouy])([lr])(?![aeiouy])", f"\\1{lang}\\1", line)

        # All vowels except when preceeded by another vowel
        # už --> upuž, ale kouzlo --> kopouzlopo
        line = re.sub("(?<![aeiouy])([aeiouy])", f"\\1{lang}\\1", line)

        # The "ě" transforms into "e"
        # dělo --> děpelopo
        line = re.sub("([ě])", f"\\1{lang}e", line)

        # And we're done!
        print(line)

if __name__ == "__main__":
    translate()
