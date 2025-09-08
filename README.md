# rule-based-honorific-Russian-second-person-pronouns
Rule-based defining of the honorific of Russian second-person pronouns

This project was an experiment to create a tokenizer, normalizer, and pos-tagger based on rules for the Russian language without using third-party libraries. Initially, this processing and analysis were intended to determine the honorific of the pronoun for further correct translation of the second-person pronoun into other foreign languages, where this system is not identical to the Russian grammar.

class_objects contains .csv with data for each class group, including auxiliary ones, taken from open sources or listed and analyzed independently. Data on various features of parts of speech are presented in the form of short designations - designations of Russian names in Latin alphabet.

The main module contains the main code for starting a full cycle of text data processing, giving out information about the location of the second person's pronoun and important features for its translation.

The pos_classes module contains all classes for pos tagging, as well as a function that initializes all standard objects for closed classes (that is, rarely or never replenished, for example, numerals).

The text_processing module contains functions that perform all processing and analysis of text data. They contain large blocks of conditions.

In this project, I wanted to introduce a linguistic approach to the definition and analysis of Russian words, and despite the fact that tagging is not always accurate, this project can serve as a basis for further development and quality improvement using a linguistic framework.
