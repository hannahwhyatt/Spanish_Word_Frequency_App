# Word Frequency in Spanish
**TL;DR: Spanish vocabulary is often regional. Can we get some insight into this by measuring the frequency of lemma by region, using web corpus data?**

In Spain, the word for 'potato' is _patata_, and in Latin America it is usually _papa_. In Spain, _papa_ means Pope. Good dictionaries will indicate country of origin for certain translations, but as a learner of the language, sometimes this doesn't feel like enough. Speaking to native speakers from various Spanish-speaking countries, I've found:​​​

- Some words are regional, but universally understood, e.g. _órale güey_, from Mexico; _guay_ or _vale_ from Spain.
- Some words (often slang terms) are unheard of outside certain countries or regions, e.g. _zarpado_ from Argentina, or _tuani_ from Nicaragua, El Salvador.
- Some words change meaning depending on country or region, e.g. _papa_; _torta_. 

The aim of this project is to explore Spanish word frequency by region, and therefore get some measure of which vocabularies are most likely to be understood by location. Changes in meaning are set aside for now. I've use data from a corpus of Spanish language web pages (about 2 billion words) found at [corpusdata.org](https://www.corpusdata.org/spanish.asp) [(download page)](https://www.corpusdata.org/formats.asp), which is labelled with the country origin of each webpage source. The authors of the data have published a couple of [insights](https://www.corpusdelespanol.org/web-dial/) into this topic, but here I'll explore further. I've used the sample (~1/100 of the original dataset) to carry out some analysis and practice using SQL, python, visualisation tools, etc. The full text corpus would grant a more reliable analysis, but I'm about $795 short.  

## Data
**TL;DR: SQL to manage the corpus data.**

The repo containing the data for this project can be found [here](https://github.com/hannahwhyatt/Spanish_Corpus_Database), alongside my python script for transforming the text files into a PostgreSQL database using the psycopg2 library. In short, the raw corpus data is stored by individual word instance, and each word is stored by word ID, alongside a text source ID. The lexical information for each word ID is found in a separate .txt file, as are the source texts. Given the size and organisation of this data, it seemed like a nice opportunity to learn how to use SQL, and practice creating some relations. Below is the Entity-Relationship diagram showing relations between the raw data (main table) and lexicon reference and text source tables in the database.  

![image](https://github.com/hannahwhyatt/corpusapp/assets/103440636/31d31ddf-9d7e-4e0a-ad7e-db8f8adb537e)

## Map App
The app connects to the corpus database to visualise relative frequency of lemma by country. It's written in python using Dash and hosted on Render at https://corpus-app-pmt8.onrender.com. 

![Screenshot](https://github.com/hannahwhyatt/corpusapp/assets/103440636/86595b78-cd4c-43b0-a200-4a3662284629)
A screenshot of the app.

## Limitations
Checking the results of the app against ground-truths, we get mixed results. For example, the pronoun _vos_, which is used to varying degrees across Latin America (mostly in the Southern Cone) but not Spain, indeed appears most frequently in the Americas, particularly Argentina and Uruguay, and infrequently in Spain. However, Chile, where vos is commonly used, displays the lowest frequency. Some things to note:

- **Possibly incorrect labelling**: even if we consider the labels for origin of each webpage generally accurate, there's no guarantee that each webpage was written by a native speaker of the country it is labelled with.
- **Bias**: it's unlikely the sample selected from the corpus contains a comparable distribution of domains (in media, news, blogs, books, etc.) for each country. Over representation of certain domains is likely to bias the frequency of certain terms. This could be mitigated in pre-processing, but would reduce the size of the useable data.
- **Missing vocabulary**: many not uncommon terms are missing from the list of lemma available in the sample.

The second two points are likely to be well addressed with more data, but this is of course pretty costly and/or time consuming. In the meantime, this analysis is also very basic. I'll work on adding some more statistics to the app and further options for analysis, so watch this space. 👀
