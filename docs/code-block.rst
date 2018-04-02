
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

scrivi ``.. topic::`` titolo

.. topic:: titolo

   Subsequent indented lines comprise the body of the topic, and are interpreted as body elements.

------
------

+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| da Google Doc →                                                              | → a GGeditor                                                                                             | → a Github                                                                                                  | → a Read the Docs                                                                                                                                                                                             |
+==============================================================================+==========================================================================================================+=============================================================================================================+===============================================================================================================================================================================================================+
| Scrivi facilmente testo in un documento senza conoscere il linguaggio RST    | GG editor è un plug-in di Google Docs che automatizza il lavoro di compilazione sul repository di Github | Il progetto sul repository di Github è fondamentale per esporre il documento da pubblicare su Read the Docs | Read the Docs è la piattaforma che espone documenti con un efficace architettura dei contenuti, in un formato usabile da tutte le dimensioni di display e che permette una facile ricerca di parole nel testo |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| .. figure:: http://googledocs.readthedocs.io/it/latest/_images/index_3.png   | .. figure:: http://googledocs.readthedocs.io/it/latest/_images/index_4.png                               | .. figure:: http://googledocs.readthedocs.io/it/latest/_images/index_5.png                                  | .. figure:: http://googledocs.readthedocs.io/it/latest/_images/index_6.png                                                                                                                                    |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+



