
https://docs.readthedocs.io

------

http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html

------

**code-block gherkin**

scrivi ``.. code-block:: gherkin``

.. code-block:: gherkin

   blabla **aaallll** aallaalall aalal al  http://bla.it ggggggggg ggg gggggggjjj jjj hhhhhh
   documentation-style-guide-sphinx/   jjjjj jj jjjj
   tuudududu duuu dduuud u
  
------

**code-block rst**

scrivi ``.. code-block:: rst``

.. code-block:: rst

  #############
  Some document
  #############

  Some text which includes links to `Example website`_ and many other links.

  `Example website`_ can be referenced multiple times.

  (... document content...)

  And at the end of the document...

  **********
  References
  **********

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
