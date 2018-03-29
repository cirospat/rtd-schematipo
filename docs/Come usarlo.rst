
.. _h85b6993fe7e11412b481a47264959:

Come usarlo
***********

\ |IMG1|\ 

.. _h177537546887b67276822514c66016:

How to Use
==========

\ |LINK1|\ 

.. _h84e3b4616757118376d336e2e5d5d23:

For reStructuredText Beginners
==============================

If you are a beginner of the reStructuredText and you feel a little bit of confusing about how to put your documents onto the RTD website. I wrote two quick guides to help your task to be quickly completed with the GGeditor. 

\ |LINK2|\ 

    This guide for you to make the 1st copy of your product documents get online.

\ |LINK3|\ 

    This guide for you to make the 1st copy of your module documents get online.

I was struggling on writing reStructuredText for a long time . Now, with the GGeditor and these two tutorials, I hope them can help you to get jobs done quicker and easier.


|REPLACE1|

|

.. _h447662145f7692285c35327713294c:

Code block with line number
===========================


+--+--------------------------------------------------------------------------------------------------------------+
| 1|#!/usr/bin/env python                                                                                         |
| 2|                                                                                                              |
| 3|"""                                                                                                           |
| 4|Twisted moved the C{twisted} hierarchy to the C{src} hierarchy, but C{git}                                    |
| 5|doesn't know how to track moves of directories, only files.  Therefore any                                    |
| 6|files added in branches after this move will be added into ./twisted/ and need                                |
| 7|to be moved over into                                                                                         |
| 8|"""                                                                                                           |
| 9|                                                                                                              |
|10|\ |STYLE0|\  os                                                                                               |
|11|\ |STYLE1|\  twisted.python.filepath \ |STYLE2|\  FilePath                                                    |
|12|                                                                                                              |
|13|here \ |STYLE3|\  FilePath(__file__)\ |STYLE4|\ parent()\ |STYLE5|\ parent()                                  |
|14|fromPath \ |STYLE6|\  here\ |STYLE7|\ child("twisted")                                                        |
|15|toPath \ |STYLE8|\  here\ |STYLE9|\ child("src")                                                              |
|16|                                                                                                              |
|17|\ |STYLE10|\  fn \ |STYLE11|\  fromPath\ |STYLE12|\ walk():                                                   |
|18|    \ |STYLE13|\  fn\ |STYLE14|\ isfile():                                                                    |
|19|        os\ |STYLE15|\ system("git mv {it} src/{it}"                                                          |
|20|                  \ |STYLE16|\ format(it\ |STYLE17|\ "/"\ |STYLE18|\ join(fn\ |STYLE19|\ segmentsFrom(here))))|
|21|                                                                                                              |
|22|os\ |STYLE20|\ system('git clean -fd')                                                                        |
|23|                                                                                                              |
|24|\ |STYLE21|\  \ |STYLE22|\ (x):                                                                               |
|25|\ |STYLE23|\  \ |STYLE24|\ (x):                                                                               |
|26|    go start start                                                                                            |
|27|    go start end                                                                                              |
|28|                                                                                                              |
|29|\ |STYLE25|\  \ |STYLE26|\ (y):                                                                               |
|30|    go end start                                                                                              |
|31|    go end end                                                                                                |
+--+--------------------------------------------------------------------------------------------------------------+

.. _h2c1d74277104e41780968148427e:





.. code:: 

    #!/usr/bin/env python
    
    """
    Twisted moved the C{twisted} hierarchy to the C{src} hierarchy, but C{git}
    doesn't know how to track moves of directories, only files.  Therefore any
    files added in branches after this move will be added into ./twisted/ and need
    to be moved over into
    """
    
    import os
    from twisted.python.filepath import FilePath
    
    here = FilePath(__file__).parent().parent()
    fromPath = here.child("twisted")
    toPath = here.child("src")
    
    for fn in fromPath.walk():
        if fn.isfile():
            os.system("git mv {it} src/{it}"
                      .format(it="/".join(fn.segmentsFrom(here))))
    
    os.system('git clean -fd')
    
    def outer(x):
    def indent_start(x):
        go start start
        go start end
    
    def end(y):
        go end start
        go end end


.. code-block:: python
    :linenos:

    #!/usr/bin/env python
    
    """
    Twisted moved the C{twisted} hierarchy to the C{src} hierarchy, but C{git}
    doesn't know how to track moves of directories, only files.  Therefore any
    files added in branches after this move will be added into ./twisted/ and need
    to be moved over into
    """
    
    import os
    from twisted.python.filepath import FilePath
    
    here = FilePath(__file__).parent().parent()
    fromPath = here.child("twisted")
    toPath = here.child("src")
    
    for fn in fromPath.walk():
        if fn.isfile():
            os.system("git mv {it} src/{it}"
                      .format(it="/".join(fn.segmentsFrom(here))))
    
    os.system('git clean -fd')
    
    def outer(x):
    def indent_start(x):
        go start start
        go start end
    
    def end(y):
        go end start
        go end end


.. name:: direttiva generica
    :option: value
    :option: value

    prova di contenuto in una direttiva generica


..  Attention:: 

    (content of Attention)


..  Caution:: 

    (content of Caution)


..  Warning:: 

    (content of Warning)


..  Danger:: 

    (content of Danger)


..  Error:: 

    (content of Error)


..  Hint:: 

    (content of Hint)


..  Important:: 

    (content of Important)


..  Tip:: 

    (content of Tip)


..  Note:: 

    (content of Note)


..  seealso:: 

    (content of See also)


.. admonition:: Change-me

    (content of Change-me)


.. bottom of content


.. |STYLE0| replace:: **import**

.. |STYLE1| replace:: **from**

.. |STYLE2| replace:: **import**

.. |STYLE3| replace:: **=**

.. |STYLE4| replace:: **.**

.. |STYLE5| replace:: **.**

.. |STYLE6| replace:: **=**

.. |STYLE7| replace:: **.**

.. |STYLE8| replace:: **=**

.. |STYLE9| replace:: **.**

.. |STYLE10| replace:: **for**

.. |STYLE11| replace:: **in**

.. |STYLE12| replace:: **.**

.. |STYLE13| replace:: **if**

.. |STYLE14| replace:: **.**

.. |STYLE15| replace:: **.**

.. |STYLE16| replace:: **.**

.. |STYLE17| replace:: **=**

.. |STYLE18| replace:: **.**

.. |STYLE19| replace:: **.**

.. |STYLE20| replace:: **.**

.. |STYLE21| replace:: **def**

.. |STYLE22| replace:: **outer**

.. |STYLE23| replace:: **def**

.. |STYLE24| replace:: **indent_start**

.. |STYLE25| replace:: **def**

.. |STYLE26| replace:: **end**


.. |REPLACE1| raw:: html

    <iframe width="100%" height="500px" frameBorder="0" src="http://umap.openstreetmap.fr/it/map/avvisi-della-polizia-municipale-sulla-mobilita-a-p_135416?scaleControl=false&miniMap=false&scrollWheelZoom=false&zoomControl=true&allowEdit=false&moreControl=true&searchControl=null&tilelayersControl=null&embedControl=null&datalayersControl=true&onLoadPanel=none&captionBar=false"></iframe><p><a href="http://umap.openstreetmap.fr/it/map/avvisi-della-polizia-municipale-sulla-mobilita-a-p_135416">Visualizza a schermo intero la mappa degli avvisi della Polizia Municipale</a></p>

.. |LINK1| raw:: html

    <a href="User%20Guide.html">How to Use</a>

.. |LINK2| raw:: html

    <a href="how2Readthedocs.html">How to create a generic website of documentation on the RTD</a>

.. |LINK3| raw:: html

    <a href="ApiDoc.html">How to create API document for python modules</a>


.. |IMG1| image:: static/Come_usarlo_1.png
   :height: 136 px
   :width: 601 px
