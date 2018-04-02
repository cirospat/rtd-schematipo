
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

scrivi ``.. code-block:: gherkin``

.. code-block:: gherkin

   blabla **aaallll** aallaalall aalal al  http://bla.it ggggggggg ggg gggggggjjj jjj
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

.. hlist::
   :columns: 2

   - 1 item
   
   - 2 item
   
   - 3 item
   
   - 4 item
   
   - 5 item
 
  
------

.. topic:: titolo

   Subsequent indented lines comprise the body of the topic, and are interpreted as body elements.

------


------



