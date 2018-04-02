
:Whatever: 

   this is handy to create new field
   
------

http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html

.. note::

  Usage of ``.rst`` extension is not recommended because:

  * RST files are human-readable text files. Most systems natively recognize
    the ``.txt`` extension and open these files with a text editor. This is
    a good choice.

  * Some programs parse ``.rst`` with `rst2html`_, which cannot interpret some
    Sphinx's directives such as ``code-block``. So readers using such programs
    actually lose some content.

    As an example, well known `Github`_ platform uses rst2html
    to render ``.rst`` files in its repository browser. Not only you lose
    content, you also lose features like links to lines.

  * When you need to read HTML builds of the documentation, best practice is to
    export documentation as static builds with ``sphinx-build`` command, then
    host and serve these builds as static files. For public projects, you may
    have a look at services like `Read the docs`_.

------

**code-block gherkin**

``.. code-block:: gherkin``

.. code-block:: gherkin

   bla bla a  aallll aalla alall aalal al allllll allllllllllllll alllllllll http://bla.it
   documentation-style-guide-sphinx/
   tuudududu duuu dduuud u
  
------

**code-block rst**

``.. code-block:: rst``

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

run tests with ``make tests``

------

.. note::  This is a **note** box.


------

.. hlist::
   :columns: 3

   * 1 item
   
   * 2 item
   
   * 3 item
   
   * 4 item
   
   * 5 item
 
  
------

.. topic:: titolo

   Subsequent indented lines comprise the body of the topic, and are interpreted as body elements.

------

.. role:: pyth(code)
  :language: python

Then we can do, :pyth:`print("Hello World!")`
examples in-line, :pyth:`for i in range(10)`

------

.. highlight:: rst

.. role:: python(code)
    :language: python

.. role:: latex(code)
    :language: latex

Now here are latex command :latex:`\\setlength` and python command
:python:`import`, created by ``:python:`import```.  Here is a
:literal:`literal`, which stays a literal, and
:code:`.. highlight:: rst` makes code role look as it looks.

------

.. confval:: inline_highlight_respect_highlight

    This (boolean) setting triggers, if language, which is set by 
    :code:`highlight` directive, shall be used in :code:`code` role, if no 
    language is set by a customization.  Then instead of::

       .. role:: python(code)
           :language: py

       this can :python:`trigger("python", "syntax highlight")`

    Wich is rendered:

       this can :python:`trigger("python", "syntax highlight")`

    You can also write::

       .. highlight:: py

       this can :code:`trigger("python", "syntax highlight")`
       
------



