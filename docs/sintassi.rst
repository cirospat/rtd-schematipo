
.. _h4f561e675749113322e7d7c7813b36:

Sintassi del formato RST per Docs Italia
########################################

.. _h2c1d74277104e41780968148427e:




| `Link utili <#h3c421475615eaf30273e2d7c114534>`_
| `Struttura del documento <#h77637252685a785b3b3954452f2a7166>`_
| `Formattazione e markup di base <#h6b2b4d486a6d4d7d1b475d521c6a6d7d>`_
| `Link <#h69193759306e5406a28415467f3475>`_
| `Titoli <#h5e503015621ec352b4937d1d2a5640>`_
| `Sezioni <#h4648177646504f6e1329505566c3226>`_
| `Indice <#h3f424c937355b747362a1542582064>`_
| `Riassunto <#h70753d28321024f5383ff32b3e>`_
| `Figure <#h666dec742f6f38212c93967247969>`_
| `Tabelle <#h4a878152f4d5c62225d753ce77d33>`_
| `Glossario <#h31187c4f803f4c429114a765677a48>`_
| `Citazioni <#h2b2d5112501a7340214d7c64921e21>`_
| `Riferimenti <#h2957346c201b5367b31462f715956>`_
| `Note <#h3b6493926503d135d5733733356414>`_
| `Box <#h3c41a511a67557b486d2c2a7f7b776>`_
| `Componente “In consultazione” <#h146e5425387676217358407d636a6a39>`_
| `Componente “Procedura” <#h4c452325372a3530b5d7c87a1b49>`_
| `Componente “Documenti utili” <#h751d47c341445e7522211b4cb2b2b>`_
| `Componente “Tono di voce” <#h34333e6c1b2c48351f35a2e4f6a2575>`_

.. _h2c1d74277104e41780968148427e:




.. _h3c421475615eaf30273e2d7c114534:

Link utili
**********

* \ |LINK1|\ 

* \ |LINK2|\ 

* \ |LINK3|\ 

* \ |LINK4|\ 

* \ |LINK5|\ 

.. _h77637252685a785b3b3954452f2a7166:

Struttura del documento
***********************

I documenti pubblicati su Docs Italia devono essere suddivisi in file differenti. Il file index.rst contiene il titolo del documento, un breve riassunto, e l’indice dei contenuti. Il resto del documento è diviso in capitoli (sezioni di primo livello) che corrispondono ad altrettanti file.

Esempio di file index.rst:

Titolo del documento

====================

.. highlights:

   Breve testo che riassume il contenuto del documento. Lorem ipsum 

   dolor sit amet, consectetur adipiscing elit.

.. toctree::

   :numbered:

   titolo-primo-capitolo

   titolo-secondo-capitolo

I file che contengono le diverse sezioni di primo livello devono essere nominati con il titolo del capitolo, sostituendo tutti gli spazi con il trattino e omettendo le particelle grammaticali.

Poiché la strutturazione del repository impatta sugli URL generati, tutti i file devono essere collocati nella radice del repository.

Per documenti particolarmente complessi, che rendono necessaria una ulteriore suddivisione in file, è possibile creare una directory per ogni sezione (usando il titolo della sezione) e replicare la struttura di un documento semplice all’interno di ogni directory.

Esempio di strutturazione di un documento complesso:

├── index.rst

├── titolo-primo-capitolo

│   ├── index.rst

│   ├── primo-paragrafo.rst

│   ├── titolo-interessante.rst

│   └── titolo-sezione.rst

├── titolo-secondo-capitolo

│   ├── index.rst

│   ├── nuova-sezione.rst

│   └── titolo-molto-molto-lungo.rst

└── titolo-terzo-capitolo

    ├── index.rst

    ├── paragrafo-rivoluzionario.rst

    ├── paragrafo-tecnologico.rst

    └── paragrafo-tradizionale.rst

.. _h6b2b4d486a6d4d7d1b475d521c6a6d7d:

Formattazione e markup di base
******************************

[inserire qui tutte le informazioni relative alla formattazione inline, la creazione di elenchi, etc.]

.. _h69193759306e5406a28415467f3475:

Link
****

[istruzioni per la generazione di link]

.. _h5e503015621ec352b4937d1d2a5640:

Titoli
******

I titoli che identificano le sezioni del 

+-----------------------------------------------------+------------------------+---------------------+
|Titolo                                               |Carattere sottolineatura|Esempio              |
+=====================================================+========================+=====================+
|Documento (solo index.rst)                           |= (uguale)              |Titolo del documento |
|                                                     |                        |                     |
|                                                     |                        |==================== |
+-----------------------------------------------------+------------------------+---------------------+
|Titolo di capitolo (sezione di primo livello)        |* (trattino)            |Titolo del capitolo  |
|                                                     |                        |                     |
|                                                     |                        |-------------------  |
+-----------------------------------------------------+------------------------+---------------------+
|Titolo del paragrafo (sezione di secondo livello)    |~ (tilde)               |Titolo del paragrafo |
|                                                     |                        |                     |
|                                                     |                        |~~~~~~~~~~~~~~~~~~~~ |
+-----------------------------------------------------+------------------------+---------------------+
|Titolo del sotto-paragrafo (sezione di terzo livello)|^ (cappelletto - caret) |Titolo terzo livello |
|                                                     |                        |                     |
|                                                     |                        |^^^^^^^^^^^^^^^^^^^^ |
+-----------------------------------------------------+------------------------+---------------------+
|Titolo della sezione di quarto livello               |‘ (apice singolo)       |Titolo quarto livello|
|                                                     |                        |                     |
|                                                     |                        |‘’’’’’’’’’’’’’’’’’’’’|
+-----------------------------------------------------+------------------------+---------------------+

.. _h4648177646504f6e1329505566c3226:

Sezioni
*******

Ciascuna sezione di primo livello (capitolo) corrispondente ad un diverso file deve contenere un breve \ |LINK6|\  subito dopo il titolo.

Il documento non dovrebbe contenere sezioni oltre il quarto livello.

.. _h3f424c937355b747362a1542582064:

Indice
******

L’indice del documento va inserito nel file index.rst per mezzo della direttiva di Sphinx \ |LINK7|\ . Per generare la numerazione delle \ |LINK8|\ , delle \ |LINK9|\  e delle \ |LINK10|\ , è necessario usare l’opzione :numbered:. Il contenuto della direttiva è costituito da un elenco di tutti i file da includere. I file corrispondono alle sezioni di primo livello.

Il glossario, se presente, non va inserito nella toctree insieme ai file delle sezioni, ma in una toctree dedicata che non deve avere l’opzione :numbered: (perché il glossario non va numerato) e deve invece riportare le opzioni :hidden: e :name: glossary_toc. Queste opzioni sono necessarie per fare in modo che Sphinx identifichi e gestisca correttamente la sezione glossario.

Esempio di toctree (nel caso di glossario presente):

.. toctree::

   :numbered:

   titolo-primo-capitolo

   titolo-secondo-capitolo

.. toctree::

   :name: glossary_toc

   :hidden:

   glossario

.. _h70753d28321024f5383ff32b3e:

Riassunto
*********

Il riassunto (summary) del documento e di ogni sezione va inserito usando la direttiva di RST \ |LINK11|\ .

Esempio:

.. highlights:

   Breve testo che riassume il contenuto del documento. Lorem ipsum 

   dolor sit amet, consectetur adipiscing elit.

.. _h666dec742f6f38212c93967247969:

Figure
******

Le immagini dovrebbero essere inserite all’interno di una figura (includendo quindi almeno una didascalia). Le figure vanno inserite usando la direttiva RST \ |LINK12|\ .

È obbligatorio inserire l’opzione :name: per avere la possibilità di creare \ |LINK13|\  alla figura nel corpo del testo.

È obbligatorio inserire nella direttiva l’opzione :alt: contenente il testo alternativo della figura e una didascalia. Il testo alternativo è visualizzato anche nell’indice delle figure.

Il testo alternativo dovrebbe essere usato per nominare il file dell’immagine (trattini al posto degli spazi e omissione delle particelle grammaticali).

Esempio:

    .. figure:: mappa-modello-strategico.png
       :alt: Mappa del modello strategico
    
       Mappa del modello strategico di evoluzione del sistema

       informativo della PA

.. _h4a878152f4d5c62225d753ce77d33:

Tabelle
*******

Le tabelle vanno inserite mediante la direttiva RST \ |LINK14|\ .

È obbligatorio inserire l’opzione :name: per avere la possibilità di creare \ |LINK15|\  alla tabella nel corpo del testo. È obbligatorio inserire una didascalia. La didascalia è visualizzata anche nell’indice delle tabelle.

Sono disponibili alcune classi (da inserire nell’opzione class) per stilizzare la tabella [TDB].

Esempio:

.. table:: Didascalia testo tabella. Enim ad minim veniam neste.

   :name: attivita-previste

   +-----------+-----------+-----------+

   | Lorem     | Vivamus   | Phasellus |

   | ipsum sit | elementum | viverra   |

   | dolor est | semper    | nulla ut  |

   | quantu    | nisi      | metus     |

   | ieres     | aenean    | arius     |

   | numer     | vusere    | laoreet   |

   |           |           | quisque   |

   |           |           | rutrum    |

   +-----------+-----------+-----------+

   | Maecenas  | Cursus    | Fusce     |

   | nec odio  | nunc,     | vulputate |

   | et ante   | quis      | eleifend  |

   | tincidunt | gravida   | sapie ves |

   | tempus    | magna mi  | tibulum   |

   |           | a libero  | purus     |

   |           |           | quam      |

   +-----------+-----------+-----------+

.. _h31187c4f803f4c429114a765677a48:

Glossario
*********

Il glossario va inserito in unico file che poi è incluso in una \ |LINK16|\ . Per generare correttamente i riferimenti ai termini di glossario è obbligatorio usare la direttiva \ |LINK17|\  di Sphinx e la seguente struttura.

Glossario

=========

A

-

.. glossary::

   atermine

      Definizione del termine. Neque porro quisquam est, qui dolorem 

      ipsum quia dolor sit consectetur, adipisci velit, sed quia non 

      incidunt ut labore et dolore magnam aliquam quaerat.

      Duis aute irure dolor in reprehenderit in voluptate velit esse 

      cillum dolore eu fugiat nulla pariatur.

   antiopam

      Neque porro quisquam est, qui dolorem ipsum quia dolor sit 

      consectetur, adipisci velit, sed quia non numquam eius modi 

      incidunt ut labore et dolore magnam aliquam quaerat.

B

-

.. glossary::

   btimeam

      Neque porro quisquam est, qui dolorem ipsum quia dolor sit

      consectetur, adipisci velit, sed quia non numquam eius modi

      incidunt ut labore et dolore magnam aliquam quaerat.

Per inserire nel testo un riferimento ad un termine di glossario è necessario usare la sintassi: :term:`antiopam`. È possibile anche fare riferimento ad un termine di glossario senza usare esattamente la stessa parola presente nel glossario. In questo caso la sintassi è: :term:`laudem<antiopam>`.

.. _h2b2d5112501a7340214d7c64921e21:

Citazioni
*********

Per inserire nel testo delle citazioni da mettere in evidenza è possibile usare la direttiva di RST \ |LINK18|\ . La direttiva va usata usando la struttura nell’esempio.

.. epigraph::

   Quote nel testo. Lorem ipsum dolor sit amet, adipisici elit, sed 

   aiusmod tempo soiu incidunt labore et aliqua sumen fortes.

   -- Autore della citazione

.. _h2957346c201b5367b31462f715956:

Riferimenti
***********

Per creare riferimenti a figure e tabelle è possibile usare la sintassi:

:ref:`testo che riferisce <attivita-previste>`

Per creare nel corpo del testo delle ancore referenziabili è possibile usare la sintassi:

.. _`qui inani vivendo`:

Queste ancora possono essere referenziate con

:ref:`corrumpit mel <qui inani vivendo>`

In generale è possibile usare la sintassi \ |LINK19|\  per creare riferimenti ipertestuali a tutte le direttive che includono un’opzione :name:.

I riferimenti sono generati correttamente anche se puntano a file diversi da quello corrente.

.. _h3b6493926503d135d5733733356414:

Note
****

Le note nel testo possono essere inserite usando la \ |LINK20|\  dallo standard RST. Anziché usare la convenzione, derivata dalla carta stampata, di inserire il testo delle note alla fine della pagina, in Docs Italia il testo delle note deve essere inserito alla fine del paragrafo che contiene la nota.

I numeri delle note vanno indicati esplicitamente per evitare che possano variare a seguito di una rigenerazione della documentazione.

Esempio:

Civibus facilisis vulputate ex mea, summo dicunt sed et.

Iriure graecis ei vis. Facilis petentium laboramus ad eam, id alii 

qui ex dolores vulputate scribentur [1]_. Nam no esse eleifend, vis 

dignissim. Vim ad augue vidisse, adhuc everti eos te, sea blandit adversarium ne.

.. [1] Cfr. art. 101 del Codice degli appalti d.lgs. 18 aprile 2016

   n. 50.

.. _h3c41a511a67557b486d2c2a7f7b776:

Box
***

Nel corpo dei documenti è possibile inserire i seguenti tipi di box:


+---------------------------------------------------------------------------------+-------------------------------------------------------+
|Box                                                                              |Sintassi                                               |
+=================================================================================+=======================================================+
|Nota                                                                             |.. note::                                              |
+---------------------------------------------------------------------------------+-------------------------------------------------------+
|Errore                                                                           |.. error::                                             |
+---------------------------------------------------------------------------------+-------------------------------------------------------+
|Suggerimento                                                                     |.. hint::                                              |
+---------------------------------------------------------------------------------+-------------------------------------------------------+
|Attenzione                                                                       |.. attention::                                         |
+---------------------------------------------------------------------------------+-------------------------------------------------------+
|Importante                                                                       |.. important::                                         |
+---------------------------------------------------------------------------------+-------------------------------------------------------+
|Approfondimento (il box, che può essere espanso, mostra solo una parte del testo)|.. admonition:: deepening                              |
|                                                                                 |                                                       |
|                                                                                 |   :class: admonition-deepening admonition-display-page|
+---------------------------------------------------------------------------------+-------------------------------------------------------+
|Esempio                                                                          |.. admonition:: example                                |
|                                                                                 |                                                       |
|                                                                                 |   :class: admonition-example admonition-display-page  |
|                                                                                 |                                                       |
|                                                                                 |                                                       |
|                                                                                 |                                                       |
|                                                                                 |   .. role:: admonition-internal-title                 |
|                                                                                 |                                                       |
|                                                                                 |      :class: admonition-internal-title                |
|                                                                                 |                                                       |
|                                                                                 |   `Titolo interno al box`:admonition-internal-title:  |
|                                                                                 |                                                       |
+---------------------------------------------------------------------------------+-------------------------------------------------------+

.. _h146e5425387676217358407d636a6a39:

Componente “In consultazione”
*****************************

Codice:

.. admonition:: Consultazione

   :class: admonition-consultazione

   Questo documento è in consultazione pubblica dal 3 aprile al 4 

   maggio 2018, come previsto dall'\`art. 71 comma 1 del decreto 

   legislativo 7 marzo 2005, n. 82. Ogni commento verrà preso in 

   considerazione per la stesura finale.

.. _h4c452325372a3530b5d7c87a1b49:

Componente “Procedura”
**********************

Codice:

.. topic:: Procedura

   :class: procedure

   1. Assicurati di avere tutti i file necessari elencati nella 

      sezione precedente e visita la pagina del repository su 

      GitHub;

   2. Clicca sul pulsante \*Clone or download\*;

   3. Clicca sul pulsante \*Copy to clipboard\* accanto all’URL del 

      repo;

   .. image:: images/github_example.png

   .. role:: procedure-internal-title

      :class: procedure-internal-title

   :procedure-internal-title:`Da linea di comando, esegui`

   1. :code:`cd` alla cartella con i file della documentazione

   2. :code:`git clone <URL>`, dove <URL> è l’URL del repo. Puoi 

      ottenerlo facendo semplicemente incolla (CTRL+V oppure CMD+V)

   3. :code:`git add *`

   4. :code:`git commit`

   5. All’apertura dell’editor di testo, scrivi il messaggio di 

      commit, secondo le modalità descritte nella sezione \`Messaggi 

      di commit\`_

   6. :code:`git push origin master`

.. _h751d47c341445e7522211b4cb2b2b:

Componente “Documenti utili”
****************************

Codice:

.. topic:: Documenti utili

   :class: useful-docs

   - :mimetype:`application/pdf` \`Predisposizione e invio del file 

      di pre-subentro [204kb] <https://www.example.com>\`_ 

   - :mimetype:`application/pdf` \`Guida rapida per il censimento 

     degli utenti e delle postazioni per i Comuni [82kb]

     <https://www.example.com>\`_

   - :mimetype:`text/html` \`Piano dei test di integrazione (Apertura 

     nuova finestra) <https://www.example.com>\`_

.. _h34333e6c1b2c48351f35a2e4f6a2575:

Componente “Tono di voce”
*************************

Codice:

.. topic:: Titolo del Q&A fra utente e amministrazione

   :class: question-and-answers

   Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit 

   sed quia consequuntur magni dolores eos qui ratione voluptatem

   nesciunt.

   .. pull-quote:: utente

      Quote di domanda dell’utente. Lorem ipsum dolor sit amet,

      sed aiusmod tempo soiu incidunt labore et aliqua sumen fortes.

     - :term:`Keyword 1`

     - :term:`Keyword 2`

     - :term:`Keyword 3`

     - :term:`Keyword 4`

   .. pull-quote:: amministrazione

      Quote di risposta dall’Amministrazione. Quod sale ius, id 

      conclusionemque mea, vis no ipsum quaeque minimum tritani.

     - :term:`Keyword 1`

     - :term:`Keyword 2`

     - :term:`Keyword 3`

   .. glossary::

      Keyword 1

         Neque porro quisquam est, qui dolorem ipsum quia dolor sit

         consectetur, adipisci velit, sed quia non numquam eius modi

         incidunt ut labore et dolore magnam aliquam quaerat.

      Keyword 2

         Neque porro quisquam est, qui dolorem ipsum quia dolor sit

         consectetur, adipisci velit, sed quia non numquam eius modi

         incidunt ut labore et dolore magnam aliquam quaerat.

      Keyword 3

         Neque porro quisquam est, qui dolorem ipsum quia dolor sit

         consectetur, adipisci velit, sed quia non numquam eius modi 

         incidunt ut labore et dolore magnam aliquam quaerat.

      Keyword 4

         Neque porro quisquam est, qui dolorem ipsum quia dolor sit

         consectetur, adipisci velit, sed quia non numquam eius modi

         incidunt ut labore et dolore magnam aliquam quaerat.


.. bottom of content


.. |LINK1| raw:: html

    <a href="http://docutils.sourceforge.net/rst.html" target="_blank">Homepage di reStructuredText</a>

.. |LINK2| raw:: html

    <a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">Quickreference di RST</a>

.. |LINK3| raw:: html

    <a href="http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html" target="_blank">Markup specification di RST</a>

.. |LINK4| raw:: html

    <a href="http://docutils.sourceforge.net/docs/ref/rst/directives.html" target="_blank">Direttive di RST</a>

.. |LINK5| raw:: html

    <a href="http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html" target="_blank">Direttive di Sphinx</a>

.. |LINK6| raw:: html

    <a href="#heading=h.lyddn8nqu2f6">riassunto</a>

.. |LINK7| raw:: html

    <a href="http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree" target="_blank">toctree</a>

.. |LINK8| raw:: html

    <a href="#heading=h.c42j1yu8h0p3">sezioni</a>

.. |LINK9| raw:: html

    <a href="#heading=h.edd07z6eb6r6">tabelle</a>

.. |LINK10| raw:: html

    <a href="#heading=h.hnrwq07xwzad">figure</a>

.. |LINK11| raw:: html

    <a href="http://docutils.sourceforge.net/docs/ref/rst/directives.html#highlights" target="_blank">highlights</a>

.. |LINK12| raw:: html

    <a href="http://docutils.sourceforge.net/docs/ref/rst/directives.html#figure" target="_blank">figure</a>

.. |LINK13| raw:: html

    <a href="#heading=h.in9l4ac6g3jw">riferimenti</a>

.. |LINK14| raw:: html

    <a href="http://docutils.sourceforge.net/docs/ref/rst/directives.html#table" target="_blank">table</a>

.. |LINK15| raw:: html

    <a href="#heading=h.in9l4ac6g3jw">riferimenti</a>

.. |LINK16| raw:: html

    <a href="#heading=h.phb8obpdvu1w">toctree dedicata</a>

.. |LINK17| raw:: html

    <a href="http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-glossary" target="_blank">glossary</a>

.. |LINK18| raw:: html

    <a href="http://docutils.sourceforge.net/docs/ref/rst/directives.html#epigraph" target="_blank">epigraph</a>

.. |LINK19| raw:: html

    <a href="http://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-ref" target="_blank">ref</a>

.. |LINK20| raw:: html

    <a href="http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#footnotes" target="_blank">sintassi prevista</a>

