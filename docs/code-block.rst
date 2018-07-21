
.. _h3c5c394db521d25642014a2cd143a:

html code e code blocks
#######################

servizi di opendatasicilia

|REPLACE1|

.. _h2c1d74277104e41780968148427e:




|

.. _h436b5279535ab39574d944c194c5b:

buttons colorati con testo
**************************

|

.. raw:: html

   <p>questo è un colore &nbsp;&nbsp;<button class="btn btn-pill btn-success" type="button"><b>verde</b></button>&nbsp;&nbsp; per un tasto verde</p>

.. raw:: html

   <p>questo è un colore &nbsp;&nbsp;<button class="btn btn-pill btn-info"type="button"><strong>blu</strong></button>&nbsp;&nbsp; per un tasto blu</p>

.. raw:: html

   <p>questo è un colore &nbsp;&nbsp;<span class="btn btn-danger btn-xs">rosso</span>&nbsp;&nbsp; per un tasto rosso</p>

.. raw:: html

   <p>questo è un colore &nbsp;&nbsp;<button type="button" class="btn btn-xs btn-pill btn-warning"><b>marrone</b></button>&nbsp;&nbsp; per un tasto marrone</p>

|

.. _h17143c773422746f363a7e5505727:

html emdedding
**************


.. code:: 

    <iframe width="100%" height="600px" frameBorder="0" src="https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vRlMpRdyCdLZy6c2UNFk-KJ3dEHq5vyeyMkB4XDUrEBcmUZLJd9NDgjCfeEONqVcnO-Z588ms8g_tOl/pubhtml"></iframe>


|REPLACE2|

.. _h357a422a66b3f2d7360165d78226031:

embeddare video youtube
***********************


.. code:: 

    <iframe width="100%" height="380" src="https://www.youtube.com/embed/FeUayR8t8oM" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>


|REPLACE3|

.. _h6049143d7324d802e5b1d80343a34:

embeddare powerpoint
********************


.. code:: 

    <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTutfK7O5PJb41zPl-97_-j3pQai64hyRRTosVbd2rl5uZ5DwUJ1klOrMrCJlH4DGf4tFG6yZFV4gVQ/embed?start=false&loop=false&delayms=5000" frameborder="0" width="800" height="554" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>


|REPLACE4|

.. _h1617e81323d3739152241496067:

script in HTML per freccia back to the top
******************************************


.. code:: 

    <!-- script Back To Top
    -->
    <a id='backTop'>Back To Top</a>
    <script src="top/jquery.backTop.min.js"></script>
    <script>
               $(document).ready( function() 
                   $('#backTop').backTop({
                       'position' : 500,
                       'speed' : 500,
                       'color' : 'red',
    
                                                });
                });
    </script>

--------

.. _h4d4f60106b6a7cd791a7b252e51487f:

code block
**********

https://docs.readthedocs.io

------

http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html

------

\*\*code-block gherkin\*\*

scrivi ``.. code-block:: gherkin``

.. code-block:: gherkin

   blabla \*\*aaallll\*\* aallaalall aalal al  http://bla.it ggggggggg ggg gggggggjjj jjj hhhhhh
   documentation-style-guide-sphinx/   jjjjj jj jjjj
   tuudududu duuu dduuud u
  
------

\*\*code-block rst\*\*

scrivi ``.. code-block:: rst``

.. code-block:: rst

  #############
  Some document
  #############

  Some text which includes links to `Example website`_ and many other links.

  `Example website`_ can be referenced multiple times.

  (... document content...)

  And at the end of the document...

  \*\*\*\*\*\*\*\*\*\*
  References
  \*\*\*\*\*\*\*\*\*\*

  .. target-notes::

  .. _`Example website`: http://www.example.com/
  

------
------

.. code:: html

   <style>
    .data-table {
        border-collapse: collapse;
    }
    .border-top {
        border-top: 1px solid #000;
    }
    .border-bottom {
        border-bottom: 1px solid #000;
    }
    .border-left {
        border-left: 1px solid #000;
    }
    .border-right {
        border-right: 1px solid #000;
    }
   </style>

   <table class="data-table">
    <tr>
        <th class="border-top border-bottom border-left border-right">da Google Doc &rarr;</th>
        <th class="border-top border-bottom border-right">&rarr;&nbsp;a&nbsp;GGeditor</th>
        <th class="border-top border-bottom border-right">&rarr; a Github</th>
        <th class="border-top border-bottom">&rarr; a Read the Docs</th>
    </tr>
    <tr>
        <td class="border-bottom border-left border-right">Scrivi facilmente testo in un documento senza conoscere il linguaggio RST</td>
        <td class="border-bottom border-right">GG editor &egrave; un plug-in di Google Docs che automatizza il lavoro di compilazione sul repository di Github</td>
        <td class="border-bottom border-right">Il progetto sul repository di Github &egrave; fondamentale per esporre il documento da pubblicare su Read the Docs</td>
        <td class="border-bottom">Read the Docs &egrave; la piattaforma che espone documenti con un efficace architettura dei contenuti, in un formato usabile da tutte le dimensioni di display e che permette una facile ricerca di parole nel testo</td>
    </tr>
    <tr>
        <td class="border-bottom border-left border-right">.. figure::&nbsp;http://googledocs.readthedocs.io/it/latest/_images/index_3.png</td>
        <td class="border-bottom border-right">.. figure::&nbsp;http://googledocs.readthedocs.io/it/latest/_images/index_4.png</td>
        <td class="border-bottom border-right">.. figure::&nbsp;http://googledocs.readthedocs.io/it/latest/_images/index_5.png</td>
        <td class="border-bottom">.. figure::&nbsp;http://googledocs.readthedocs.io/it/latest/_images/index_6.png</td>
    </tr>
   </table>

--------

.. _h54520d7d56655242621495d2e757:

Tabella con http://truben.no/table
**********************************

+---------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| Reti di impegno                                                     | Link                                                                                                   |
+=====================================================================+========================================================================================================+
| Comune di Palermo (Ufficio Innovazione, UO transizione al digitale) | https://opendata.comune.palermo.it                                                                     |
+---------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| OpendataSicilia (community civica sulla cultura dei dati)           | http://opendatasicilia.it + https://www.comune.palermo.it/unita.php?apt=4&uo=1770&serv=394&sett=138    |
+---------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| “Developers Italia" Forum nazionale sui servizi pubblici digitali   | https://forum.italia.it                                                                                |
+---------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+


.. sidebar:: **questo report è stato scritto**
    :subtitle: \*\*dopo aver fatto fare il ruttino alla piccola di 3 mesi, alle 3 del mattino\*\*

    bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla v bla bla bla bla bla bla bla bla bla bla bla blabla bla bla blabla bla bla blabla bla bla blabla bla bla blabla bla bla blabla bla bla bla


|REPLACE5|


.. bottom of content


.. |REPLACE1| raw:: html

    <p><strong><span style="background-color: #ffffff;">Servizi di <a href="http://opendatasicilia.it/" target="_blank" rel="noopener">opendatasicilia</a></span></strong></p>
    <p><a title="accuss&igrave; tutorial catalogue" href="http://accussi.opendatasicilia.it/index.html" target="_blank" rel="noopener"><img src="https://camo.githubusercontent.com/24bc1b1450d155db547405fa90d92b6b34f4a132/68747470733a2f2f6369726f737061742e6769746875622e696f2f6d6170732f696d672f616363757373695f66617669636f6e2e706e67" alt="accussi" width="41" height="41" /></a>&nbsp;accuss&igrave;&nbsp; &nbsp; &nbsp;<a title="petrusino" href="http://petrusino.opendatasicilia.it/index.html" target="_blank" rel="noopener"><img src="https://camo.githubusercontent.com/acae135c1a21da78bfd3423518810cd5465a8642/68747470733a2f2f6369726f737061742e6769746875622e696f2f6d6170732f696d672f706574727573696e6f5f66617669636f6e2e706e67" alt="petrusino" width="41" height="41" /></a>&nbsp;petrusino</p>
    <p><a title="non portale open data regione sicilia" href="http://nonportale.opendatasicilia.it/index.html" target="_blank" rel="nofollow noopener"><img src="https://camo.githubusercontent.com/7ad90a32a27ec7b68b3f5d1c9aec83d0bf5e4120/68747470733a2f2f6369726f737061742e6769746875622e696f2f6d6170732f696d672f6e6f6e706f7274616c655f66617669636f6e2e706e67" alt="non portale" width="41" height="41" data-canonical-src="https://cirospat.github.io/maps/img/nonportale_favicon.png" /></a>&nbsp;non portale&nbsp;&nbsp;<a title="albopo" href="http://albopop.it/" target="_blank" rel="noopener"><img src="http://albopop.it/images/logo.png" width="41" height="41" /></a>&nbsp;albopop&nbsp;&nbsp;</p>
    <p><a title="foia pop" href="http://foiapop.it/" target="_blank" rel="noopener"><img src="https://lh3.googleusercontent.com/5mPgjmfRCJ6mgv0-OjTNj8i_CiYEaMnXZ3LHs48QCQG7X2AiG9L87f8LgCKw2l2hMuHZmoBRIhuybiHWJgBEixT6mjL8YrEV9_4SpR0fPsVPPptqqc_fW16cA9th5jxVTuExQXQWAzu5kqYBDgtWpCVeTPw4OX2Fml6AVBMfmzO3gNL2H5jvRdGrqAV67P3Nrl-bJDvqlwXna3gAWikjxZRJzk925fBbth-h0Vs577x1fVD69y_Q7DWMBTjUgR9Y5YuKpoMGO6RfSY1zkcCEXdncFGf7uIk6EB2zvQvLeVDt4pqJFlf0JRbK4WLR7SsAvfKCz0cmlYkiRi4K9KalWnK1RhO08k2xsfZGsKf9aIVqL_K-r8SlW9HJ0cFkwcTRRD8lDPqurdxkIUKsYMY9Fx8MspczsPijqlJeu_AgsMPMwJjppfmgP951LS6fVgu99Csso2JaGk9BN0BWYpLk8e7pqBrvF0fR0jIBfiIAnzVj1loh4bER3n1W9FG0nvrh67fsngfMozKzDSBHvFoXchJoG2e83-r1CwWoEQK3tDazIhkpZkxzLCLJYi4fASURZPsi2a0XEsGxn7h70K4s6AWuQo8R6hMLenbpeG0=s53-no" alt="" width="44" height="44" /></a>&nbsp;foiapop&nbsp; &nbsp;&nbsp;<a title="visual cad" href="http://www.visualcad.it/" target="_blank" rel="noopener"><img src="https://lh3.googleusercontent.com/zMrMz72sJ1JjKagZKoq-1gbg8TTLWIggKZ67vBsNRTUaUcd2Pm7dKGQXTVrl_bEQFbzG2DMYx06bmW-oN8VndQ2vqOHiibkKEMLjnS0AneovCNx58hyoaH3PqzxCt__5MKqYjepqzVbC7pNbQ1SEUaWtDGmcCReqV6bYaKLHCi6VIN5R18DjmIuVTh3nbUJYjbVsd2upIBITuJGKuErtFYzNk_f-nZ88I3W4KDbgHWBDVWf5Wx5My_b40QacDemr4YhVgSsJMQ9Si6inPNnJF9N9d2BcxW__sy8FSNll87wzH_Sk0Pw0a7e7oDjq0y4VNw0LJzXLl0KDBc-c3HX7GWrb2xY9VnUl2-hkaGID9g1nyvNMmSMreynpyn5Az9iqQ5KlcVJT7GehDHODDEeH25ktD3Nb3a2mmOv12SXh1ULuwIBWoqXFcRdFMSKG42XpR2Qs3tzj7RaE9kPKsCdmrr6AvbfNeELgQNBIJLKmPenJib5rgt-ddEhJr518SM2Ma5OGmW4uBQdooTAgxESB6Ir71qTBaXv9XcL_1_wBLbYC06PvKb3YoXnAl0Opx_zCR1bNMl5-yCpO58d7FEddNhmxKzcVQOOc-QWtEek=w192-h132-no" alt="" width="60" height="41" /></a>&nbsp;visualcad</p>
    <p><a class="twitter-follow-button" href="https://twitter.com/opendatasicilia?ref_src=twsrc%5Etfw" data-show-count="false">Follow @opendatasicilia</a></p>
.. |REPLACE2| raw:: html

    <iframe width="100%" height="600px" frameBorder="0" src="https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vRlMpRdyCdLZy6c2UNFk-KJ3dEHq5vyeyMkB4XDUrEBcmUZLJd9NDgjCfeEONqVcnO-Z588ms8g_tOl/pubhtml"></iframe>
.. |REPLACE3| raw:: html

    <iframe width="100%" height="380" src="https://www.youtube.com/embed/FeUayR8t8oM" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
.. |REPLACE4| raw:: html

    <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTutfK7O5PJb41zPl-97_-j3pQai64hyRRTosVbd2rl5uZ5DwUJ1klOrMrCJlH4DGf4tFG6yZFV4gVQ/embed?start=false&loop=false&delayms=5000" frameborder="0" width="800" height="554" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
.. |REPLACE5| raw:: html

    <iframe width="100%" height="500px" frameBorder="0" src="http://umap.openstreetmap.fr/it/map/hotspot-wifi-del-comune-di-palermo_211092?scaleControl=false&miniMap=false&scrollWheelZoom=false&zoomControl=true&allowEdit=false&moreControl=true&searchControl=null&tilelayersControl=null&embedControl=null&datalayersControl=true&onLoadPanel=undefined&captionBar=false"></iframe>