Titolo del Read the Docs
*********************

.. raw:: html

    <img class="imageLeft" style="width: 360px;" src="https://raw.githubusercontent.com/cirospat/rtd-schematipo/master/static/robin_batman.PNG">

``cultura della documentazione`` 

Questo progetto è solo una dimostrazione dell'esposizione di contenuti su **Read the Docs**.



.. raw:: html

    <img class="imageLeft" style="width: 360px;" src="https://raw.githubusercontent.com/cirospat/rtd-schematipo/master/static/rtd.png">
    <p></p>




.. raw:: html

    <strong><span style="background-color: #49634e; color: #ffffff; display: inline-block; padding: 1px 3px; border-radius: 7px;">Questa è solo una bozza</span></strong>
    <p></p>



.. raw:: html

    <img src="https://raw.githubusercontent.com/cirospat/rtd-schematipo/master/static/help.jpg">
    

Il repository dello **schema tipo RTD** si trova a questo  `link <https://github.com/cirospat/rtd-schematipo>`_, da potere clonare per progetti di documentazione online.

    

Questo **Read the Docs** è uno schema tipo ottimizzato (per design e setting vari) per la pubblicazione di documenti. Settaggi quali colore della colonna sinistra e colori del testo dei paragrafi, titoli, ecc., possono essere cambiati nel file ``theme_override.css``.

Altre impostazioni di visualizzazione grafica del documento su Read the Docs possono essere effettuate sui seguenti file, all'interno della cartella ``_templates``:

- ``breadcrumbs.html``
- ``footer.html``
- ``layout.html``
- ``searchbox.html``
- ``versions.html``


..  Important:: 
    
    Le impostazioni dentro il repository Github di questo progetto permettono di usare sia file in formato `.rST` (reStructuredText), che in formato `.MD` (Markdown). Le istruzioni da inserire nel file ``conf.py`` sono dettagliate in questa `ricetta di Tansignari <http://tansignari.opendatasicilia.it/it/latest/ricette/ReadtheDocs/come_fare_leggere_un_file_MD_a_ReadtheDocs.html>`_.


   

.. toctree::
  :maxdepth: 2

  Home <https://schema-tipo.readthedocs.io> 



.. toctree::  
    :maxdepth: 4
    :caption: index (max 30 caratteri)

    1.rst
    2.rst
    messaggi_colorati.md
    tabella.md
    GGeditor-script-per-Google-Doc.rst
    


.. toctree::  
    :maxdepth: 4
    :caption: Risorse

    MD_per_RTD.md
    iframe.md
    

.. toctree::  
    :maxdepth: 2
    :caption: Altre risorse

    external_link.md


.. toctree::  
    :maxdepth: 2
    :caption: External contribution

    build_fail.md


.. toctree::  
    :maxdepth: 3
    :caption: Informativa Privacy

    privacy.md
