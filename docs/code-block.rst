
.. _h3c5c394db521d25642014a2cd143a:

html code e code blocks
#######################

.. _h436b5279535ab39574d944c194c5b:

buttons colorati con testo
**************************

.. raw:: html

   <p>questo è un colore <span style="color: #0000ff;">&nbsp;&nbsp;<button class="btn btn-pill btn-success" type="button"><b>verde</b></button>&nbsp;&nbsp;</span><span style="color: #0000ff;"></span>per un tasto verde</p>

.. raw:: html

   <p>questo è un colore<button class="btn btn-pill btn-info"type="button"><strong>blu</strong></button>per un tasto blu</p>

.. raw:: html

   <p>questo è un colore<span class="btn btn-danger btn-xs">rosso</span>per un tasto rosso</p>

.. raw:: html

   <p>questo è un colore<button type="button" class="btn btn-xs btn-pill btn-warning"><b>marrone</b></button>per un tasto marrone</p>

|

.. _h17143c773422746f363a7e5505727:

html emdedding
**************


.. code:: 

    <iframe width="100%" height="600px" frameBorder="0" src="https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vRlMpRdyCdLZy6c2UNFk-KJ3dEHq5vyeyMkB4XDUrEBcmUZLJd9NDgjCfeEONqVcnO-Z588ms8g_tOl/pubhtml"></iframe>


|REPLACE1|

.. _h357a422a66b3f2d7360165d78226031:

embeddare video youtube
***********************


.. code:: 

    <iframe width="100%" height="380" src="https://www.youtube.com/embed/FeUayR8t8oM" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>


|REPLACE2|

.. _h6049143d7324d802e5b1d80343a34:

embeddare powerpoint
********************


.. code:: 

    <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTutfK7O5PJb41zPl-97_-j3pQai64hyRRTosVbd2rl5uZ5DwUJ1klOrMrCJlH4DGf4tFG6yZFV4gVQ/embed?start=false&loop=false&delayms=5000" frameborder="0" width="700" height="554" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>


|REPLACE3|

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


+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+
|   |       |
+---+-------+


.. bottom of content


.. |REPLACE1| raw:: html

    <iframe width="100%" height="600px" frameBorder="0" src="https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vRlMpRdyCdLZy6c2UNFk-KJ3dEHq5vyeyMkB4XDUrEBcmUZLJd9NDgjCfeEONqVcnO-Z588ms8g_tOl/pubhtml"></iframe>
.. |REPLACE2| raw:: html

    <iframe width="100%" height="380" src="https://www.youtube.com/embed/FeUayR8t8oM" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
.. |REPLACE3| raw:: html

    <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTutfK7O5PJb41zPl-97_-j3pQai64hyRRTosVbd2rl5uZ5DwUJ1klOrMrCJlH4DGf4tFG6yZFV4gVQ/embed?start=false&loop=false&delayms=5000" frameborder="0" width="700" height="554" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>