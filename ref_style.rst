bla bla bla :ref:`Markdown <ref_style:1>` bla bla bla

si trova qui: https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html

lo stile è:

<a class="hoverxref tooltip reference internal tooltipstered" data-doc="intro/getting-started-with-sphinx" data-docpath="/intro/getting-started-with-sphinx.html" data-project="docs" data-section="using-markdown-with-sphinx" data-version="stable" href="#using-markdown-with-sphinx"><span class="std std-ref">Markdown</span></a>

può darsi che serva questo:

https://github.com/readthedocs/readthedocs.org/blob/b53ebff433f6907adde529561aeb383d8809a9c6/docs/_static/js/expand_tabs.js
cioè:
/*
 * Expands a specific tab of sphinx-tabs.
 * Usage:
 * - docs.readthedocs.io/?tab=Name
 * - docs.readthedocs.io/?tab=Name#section
 * Where 'Name' is the title of the tab (case sensitive).
*/
$( document ).ready(function() {
  const urlParams = new URLSearchParams(window.location.search);
  const tabName = urlParams.get('tab');
  if (tabName !== null) {
    const tab = $('a.item > div:contains("' + tabName + '")');
    if (tab.length > 0) {
      tab.click();
    }
  }
});
