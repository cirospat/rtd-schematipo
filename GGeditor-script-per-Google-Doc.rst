
.. _h6c3e1d1d695c775e697f3f1a706e19:

GGeditor-script-per-Google-Doc
##############################

{2017/01/10 - PM 01:11:42}

.. admonition:: Cosa è questo documento?

    Questo documento contiene uno script con il codice sorgente che permette di trasmettere (in maniera automatica) su Github i contenuti editati in questo foglio, trasformandoli in sintassi del formato ``.RST``.
    Creando una copia di questo documento sul proprio Google Drive si copierà anche lo script che si trova su:
    
    \ |STYLE0|\ 

.. _bookmark-kix-wrnrl54anjqk:


.. admonition:: I file contenuti nello script

    * conversion.html
    
    * explicitMarkup.html
    
    * generator.gs
    
    * github.html
    
    * properties.gs
    
    * reSTMetadata.gs
    
    * settings.html
    
    * sidebar.html
    
    * 程式碼.gs


.. toctree::  
    :maxdepth: 3
    :caption: file script GGeditor 

    GGeditor-script-per-Google-Doc

|

.. admonition:: Release Note

    New:
    
    #. Convert table in HTML tags for preserving background color, column-span, row-span and column width.
    
    #. Multiple github accounts.
    
    Improved:
    
    #. New "Settings" panel for accounts and document options.
    
    #. In partial conversion, markups of table will keep the same as it is in whole document conversion.
    
    (Release note dal creatore dello script di GGeditor)

|

..  Important:: 

    Questo documento si trova al link: 
    \ |LINK1|\  

.. class:: speciale

This is a "special" chapter.

--------

.. _h5a6b1f4b7c464a7e2373674c59d3f34:

程式碼.gs
*********


.. code-block:: python
    :linenos:

    function onInstall(e){
      onOpen(e);
      try{
      }
      catch(e){
      }
    }
    function onOpen(e) {
      var menu = DocumentApp.getUi().createAddonMenu();
      if (e && e.authMode == ScriptApp.AuthMode.NONE) {
         // installed but not enabled
         menu.addItem('Show Markup Panel', 'showSidebar')         
         menu.addItem('Conversion', 'showConversion')         
         menu.addItem('Commit to Github', 'showGithub')
         menu.addSeparator()
         menu.addItem('Settings', 'showSettings')
      } else {
        // installed and enabled
         menu.addItem('Show Markup Panel', 'showSidebar')
         menu.addItem('Conversion', 'showConversion')
         menu.addItem('Commit to Github', 'showGithub')
         menu.addSeparator()
         menu.addItem('Settings', 'showSettings')
      }
      menu.addToUi();
    }
    
    function showSidebar() {
      DocumentApp.getUi().showSidebar(
          HtmlService
              .createHtmlOutputFromFile('sidebar.html')
              .setSandboxMode(HtmlService.SandboxMode.IFRAME)
              .setTitle('GGEditor Markup Panel')
              .setWidth(150)); /* pixels */
    }
    function showGithub() {
      DocumentApp.getUi().showModalDialog(
          HtmlService
              .createHtmlOutputFromFile('github.html')
              .setSandboxMode(HtmlService.SandboxMode.IFRAME)
              .setHeight(450)
              .setWidth(800),
          'Commit to Github')
    }
    function showConversion(){
      DocumentApp.getUi().showModalDialog(
          HtmlService
              .createHtmlOutputFromFile('conversion.html')
              .setSandboxMode(HtmlService.SandboxMode.IFRAME)
              .setWidth(650) 
              .setHeight(450),
          'Conversion')  
    }
    function showSettings(){
      var htmlService = HtmlService
              .createHtmlOutputFromFile('settings.html')
              .setSandboxMode(HtmlService.SandboxMode.IFRAME)
              .setWidth(650) 
              .setHeight(450)
      DocumentApp.getUi().showModalDialog(htmlService,'Settings')
    }
    /* 
     * utilities 
    */
    function i18n(s){
      return s
    }
    function setSelection(element){
      var rangeBuilder = DocumentApp.getActiveDocument().newRange();
      rangeBuilder.addElement(element)
      DocumentApp.getActiveDocument().setSelection(rangeBuilder.build());
    }
    function getSelection(warnning){
      if (typeof(warnning)==='undefined') warnning = true;
      var selection = DocumentApp.getActiveDocument().getSelection();
      if (selection) {
        return selection;
      }
      else{
        if (warnning) DocumentApp.getUi().alert(i18n('Please select text to format.'));
        return;
      }
    }
    function copyDocumentAttributes(src,dest){
    
      //handle things like: style[DocumentApp.Attribute.HORIZONTAL_ALIGNMENT] = DocumentApp.HorizontalAlignment.RIGHT;
      var equivents = {
        RIGHT:DocumentApp.HorizontalAlignment.RIGHT,
        LEFT:DocumentApp.HorizontalAlignment.LEFT,
      }
      for (var key in src){
        var value = src[key]
        if (typeof(equivents[value]) != 'undefined') value = equivents[value]
        dest[DocumentApp.Attribute[key]] = value
      }
    }
    function closestType(ele,typesToFind){
      /*
       * find a type in the parents of given ele
       * typesToFind: a DocumentApp.ElementType or an array of it
       */
    
      if (!typesToFind.some) typesToFind = [typesToFind]
      var found = null
      var j = 0 // prevent infinit loop
      while (ele && j < 20){
        var tp = ele.getType()
        typesToFind.some(function(t){
          if (tp==t){
            found = ele
            return true
          }
        })
        if (found) break
        j+=1
        ele = ele.getParent()
      }
      return found
    }
    function encloseSelectionWith(prefix,surfix){
      var selection = getSelection(false);
      if (!selection) {
        var cursor = DocumentApp.getActiveDocument().getCursor();
        if (cursor) {
          cursor.insertText(prefix+surfix);
        }
        return;
      }
      var selectedElements = selection.getSelectedElements();
      var rangeBuilder = DocumentApp.getActiveDocument().newRange();
      for (var i = 0; i < selectedElements.length; ++i) {
        var selectedElement = selectedElements[i];
    
        // Only modify elements that can be edited as text; skip images and other
        // non-text elements.
        var text = selectedElement.getElement().editAsText();
        if (selectedElement.isPartial()) {
          var ss=-1, se = -1;
          if (prefix.length>0){
            text.insertText(selectedElement.getStartOffset(),prefix);
            ss = selectedElement.getStartOffset();
            se = selectedElement.getEndOffsetInclusive() + prefix.length + 1;
          }
          if (surfix.length>0){
            var surfixLen = surfix.length + 1
            ss = (ss==-1) ? selectedElement.getEndOffsetInclusive()+prefix.length+1 : ss;
            se = (se==-1) ? (ss+surfix.length) : (selectedElement.getEndOffsetInclusive()+prefix.length+1)+surfix.length
            text.insertText(selectedElement.getEndOffsetInclusive()+prefix.length+1,surfix);
          }
          rangeBuilder.addElement(text,ss,se-1);
        } else {
          if (prefix.length>0) text.insertText(0,prefix);
          if (surfix.length>0) text.appendText(surfix);
          rangeBuilder.addElement(selectedElement.getElement());
        }
      }
      DocumentApp.getActiveDocument().setSelection(rangeBuilder.build());
    }
    function applyStyleToElement(ele,param,offset){
      if (param.style){
        var style = {};
        copyDocumentAttributes(param.style,style)
        if (offset){
          ele.editAsText().setAttributes(offset.start,offset.end,style)
        }
        else{
          ele.setAttributes(style);
        }
      }
      if (param.heading){
        var pEle = closestType(ele,DocumentApp.ElementType.PARAGRAPH)
        if (pEle){
          pEle.setHeading(DocumentApp.ParagraphHeading[param.heading]);
        }
        else{
          //Logger.log('No pEle')
        }
      }
      if (param.paragraph_style){
        var style = {};
        copyDocumentAttributes(param.paragraph_style,style)
        var selectedElement = selectedElements[i];
        var ele = selectedElement.getElement()
        var pEle = closestType(ele,DocumentApp.ElementType.PARAGRAPH)
        if (pEle) pEle.setAttributes(style);
      }
    }
    function applyStyleToSelected(param){
      /*
       param:{
         style:{
           RIGHT:
           FONT_FAMILY:
           FONT_SIZE:
           BOLD:
         },
         heading:(string) NORMAL, HEADING1,...6, TITLE, Empty string to remove heading
       }
      */
      var selection = getSelection(false);
      if (!selection) return false;  
      var selectedElements = selection.getSelectedElements();
      for (var i = 0; i < selectedElements.length; ++i) {
        var selectedElement = selectedElements[i];
        // Only modify elements that can be edited as text; skip images and other
        // non-text elements.
        var ele = selectedElement.getElement()
        if (selectedElement.isPartial()){
          applyStyleToElement(ele,param,{start:selectedElement.getStartOffset(),end:selectedElement.getEndOffsetInclusive()})
        }
        else{
          applyStyleToElement(ele,param)
        }
      }
    
      return true
    }
    function insertAtCursor(txt,silent){
      var doc = DocumentApp.getActiveDocument();
      var cursor = doc.getCursor();
      if (cursor) {
        // Attempt to insert text at the cursor position. If insertion returns null,
        // then the cursor's containing element doesn't allow text insertions.
        var element = cursor.insertText(txt);
        var rangeBuilder = doc.newRange();
        rangeBuilder.addElement(element);
        if (element) {
            try{
              doc.setCursor(doc.newPosition(element.getNextSibling(),0));
            }
            catch(e){
              doc.setCursor(doc.newPosition(element,txt.length));
            }
            var r = rangeBuilder.build()
            doc.setSelection(r);
            return r
        } else {
          if (silent) return //no warning
          DocumentApp.getUi().alert(i18n('Cannot insert text at this cursor location.'));
          return;
        }
      } else {
        var selection =  getSelection(false);
        if (selection){
            //replace the selection
            var selectedElements = selection.getSelectedElements();
            var rangeBuilder = doc.newRange();
            for (var i = 0; i < selectedElements.length; ++i) {
              var selectedElement = selectedElements[i];      
              // Only modify elements that can be edited as text; skip images and other
              // non-text elements.
              var ele = selectedElement.getElement();
              var text = ele.editAsText();          
              if (selectedElement.isPartial()) {
                var t = text.getText();
                var txt2add;
                if (i==selectedElements.length-1){
                  txt2add = txt;
                }
                else{
                  txt2add = '';
                }
                var newt = t.substr(0,selectedElement.getStartOffset())+txt2add+t.substr(selectedElement.getEndOffsetInclusive()+1);
                text.setText(newt);
                if (txt2add.length){
                  var pos = selectedElement.getStartOffset()+txt2add.length;
                  doc.setCursor(doc.newPosition(ele,pos));
                  rangeBuilder.addElement(text, selectedElement.getStartOffset(), pos-1)
                }
              } else {
                var t = ele.getType();
                if (t == DocumentApp.ElementType.TABLE_CELL || i==selectedElements.length-1){
                  text.setText(txt);
                  rangeBuilder.addElement(ele)
                  if (i==selectedElements.length-1) doc.setCursor(doc.newPosition(ele,txt.length-1));
                }
                else{
                  if (t == DocumentApp.ElementType.TEXT || t == DocumentApp.ElementType.PARAGRAPH) text.removeFromParent();
                  else rangeBuilder.addElement(ele)
                }            
              }
            }
            var r = rangeBuilder.build()
            doc.setSelection(rangeBuilder.build());
            return r
        }
    
        if (silent) return //no warning
        DocumentApp.getUi().alert(i18n('Cannot find a cursor in the document.'));
      }
    }
    function removeSelection(){
      var selection =  getSelection(false);
      if (!selection) return null;
      //replace the selection
      var rangeElements = selection.getSelectedElements();
      var body = DocumentApp.getActiveDocument().getBody();
      var eles = []
      var previousSibling, nextSibling;
      rangeElements.forEach(function(rangeEle,i){
        //eles.push(ele) //var pEle = closestType(ele,DocumentApp.ElementType.PARAGRAPH)
        var p;
        if (rangeEle.isPartial()){
          //slip partial selection
          p = closestType(rangeEle.getElement(),DocumentApp.ElementType.PARAGRAPH)
          p.removeChild(rangeEle.getElement())
        }
        else{    
          var ele = rangeEle.getElement()
          if (ele.getType()==DocumentApp.ElementType.PARAGRAPH) {
            if (!previousSibling) previousSibling =ele.getPreviousSibling()
            nextSibling = ele.getNextSibling()
            body.removeChild(ele)
          }
        }
      })
      return {previousSibling:previousSibling,nextSibling:nextSibling};
    }
    function replaceSelectionWithElement(ele){
      removeSelection()
      var rangeBuilder = doc.newRange();
    }
    
    function changeElementHeadning(rootEle,upgrade,depth){
      if (depth > 1) return 
      var childEle = rootEle.getChild(0)
      while(childEle){
        if (childEle.getType()==DocumentApp.ElementType.BODY_SECTION){
          changeElementHeadning(childEle,upgrade,depth+1)
        }
        else if (childEle.getType()==DocumentApp.ElementType.PARAGRAPH){
          var level = getHeadingLevel(childEle)
          if (level){
            var newlevel
            if (upgrade){
              newlevel = level-2
            }
            else{
              newlevel = level
            }
            if (newlevel<0 || newlevel >6){
              //do nothing
            }
            else if (newlevel==0){
              childEle.setHeading(DocumentApp.ParagraphHeading.TITLE)
            }
            else{
    
              childEle.setHeading(DocumentApp.ParagraphHeading['HEADING'+newlevel])
            }
          }
        }
        childEle = childEle.getNextSibling()
      }      
    }
    
    function makeRelativePath(src,dst){
      /*
       * support both src and dst are *.html files with or without path
       *
       */
      var myPaths = src.split('/')
      var myName = myPaths.pop()
      var targetPaths = dst.split('/')
      var targetName = targetPaths.pop()
      var sameCount = 0
      myPaths.some(function(p,i){
        if (targetPaths[i] != p) return true
        sameCount += 1
      })
      var relativeLink
      if (sameCount == myPaths.length && myPaths.length==targetPaths.length){
        relativeLink = targetName
      }
      else {
        var upperLevels = []
        for (var x=0;x < (myPaths.length-sameCount);x++){
          upperLevels.push('..')
        }
        if (targetPaths.length > sameCount){
          targetPaths.splice(0,sameCount)
          if (targetPaths.length) {
            targetPaths.push(targetName)
            targetName = targetPaths.join('/')
          }
        }
        upperLevels.push(targetName)
        relativeLink = upperLevels.join('/')
      }
      return relativeLink
    }
    
    /*
     * application implementation starts
     *
     * services for sidebar.html
     *
     */
    
    function markup(name,options){
      var applyStyle = function(param){
        var doc = DocumentApp.getActiveDocument();
        var cursor = doc.getCursor();
        if (cursor) applyStyleToElement(cursor.getElement(),param)
      }
      switch (name){
        case 'part':
          var param = {
            heading:'TITLE',
          }
          applyStyle(param)
          break
        case 'chapter':
          var param = {
            heading:'HEADING1',
          }
          applyStyle(param)
          break
        case 'section':
          var param = {
            heading:'HEADING2',
          }
          applyStyle(param)
          break
        case 'subsection':
          var param = {
            heading:'HEADING3',
          }
          applyStyle(param)
          break
        case 'subsubsection':
          var param = {
            heading:'HEADING4',
          }
          applyStyle(param)
          break
        case 'subsubsubsection':
          var param = {
            heading:'HEADING5',
          }
          applyStyle(param)
          break
        case 'paragraph':
          var param = {
            heading:'NORMAL',
          }
          applyStyle(param)
          break
        case 'hyperlink':
    
          var url
          if (/^.+:\/\//.test(options.link)) url = options.link //link to bookmark or footnotes
          else {
            url = 'http://cross.document/'+options.link //cross-document link
          }
    
          var selection = DocumentApp.getActiveDocument().getSelection();
           if (selection) {
             // make the selected text with link
             var elements = selection.getRangeElements();
             for (var i = 0; i < elements.length; i++) {
               var element = elements[i];      
               // Only modify elements that can be edited as text; skip images and other non-text elements.
               if (element.getElement().editAsText) {
                 var text = element.getElement().editAsText();
    
                 // Bold the selected part of the element, or the full element if it's completely selected.
                 if (element.isPartial()) {
                   text.setLinkUrl(element.getStartOffset(), element.getEndOffsetInclusive(), url);
                 } else {
                   text.setLinkUrl(url);
                 }
               }           
             }
           }
           else{
            // insert a link with text and link
            var range = insertAtCursor(options.text,true)
            if (range){
              var text = range.getRangeElements()[0].getElement().editAsText();
              text.setLinkUrl(url)
             }
           }
          break
        case 'downgradeheadings':
          var body = DocumentApp.getActiveDocument().getBody()
          changeElementHeadning(body,false,0)
          break
        case 'upgradeheadings':
          var body = DocumentApp.getActiveDocument().getBody()
          changeElementHeadning(body,true,0)
          break
      }
    }
    
    function inlineMarkup(domain,name){
      var cursor = DocumentApp.getActiveDocument().getCursor();
      if (!cursor) return
      var ele = cursor.getElement()
      var keyname = name.split('::')[0]
      var meta = reSTMetadata[domain](keyname,name)
      var body = DocumentApp.getActiveDocument().getBody();
      var childIndex = body.getChildIndex(ele)
      var table = body.insertTable(childIndex, meta.cells)
      var style = {
        FONT_FAMILY:'Courier New',
        //FONT_SIZE:14,
        LINE_SPACING:1,
        BOLD:false,
        ITALIC:false        
      }
      table.setAttributes(style)
    
      /* disabled because the issue #3321, TableCell.merge() crashes
      // merge cells
      if (meta.merge.length){
        meta.merge.forEach(function(item){
          var row = table.getRow(item.row)
          for (var i=item.cols.length-1;i>0;--i){
            row.getCell(parseInt(item.cols[i])).merge()
          }
        })
      }
      */
      // set the indent of the 1st cell in rows except 1st row
      var paragraph_style = {
        INDENT_START:20,
        INDENT_FIRST_LINE:20
      }
      for (var i=1;i<meta.cells.length;i++){
        var p = closestType(table.getRow(i).getCell(0).getChild(0) ,DocumentApp.ElementType.PARAGRAPH)
        p.setAttributes(paragraph_style)
        if (i==1) setSelection(p)
      }
    }
    
    function createTableInPlace(options){
      /*
       * helper for insertDirective()
       *
       *
       */
      //var ele = cursor.getElement()
    
      // figure where to insert and what to be the content of last row
      var content = ''
      var ele
      var selection = getSelection(false)
      if (selection){
          var selectedElements = selection.getSelectedElements();
          for (var i = 0; i < selectedElements.length; ++i) {
              var selectedElement = selectedElements[i]; 
              ele = selectedElement.getElement();
              content = ele.getText();
              break
          }
      }
      else{
        var cursor = DocumentApp.getActiveDocument().getCursor();
        if (!cursor) return
        ele = cursor.getElement()
      }
    
      var meta = options.meta
      //replace the content of last row column 1
      if (content) meta.cells[meta.cells.length-1] = [content]
    
      var body = DocumentApp.getActiveDocument().getBody();
      var childIndex
      try {
        childIndex = body.getChildIndex(ele)
      }
      catch(e){
        var p = closestType(ele,DocumentApp.ElementType.TABLE)
        if (!p) p = closestType(ele,DocumentApp.ElementType.LIST_ITEM)
        if (!p) p = closestType(ele,DocumentApp.ElementType.PARAGRAPH)
        var nextSibling = p.getNextSibling()
        if (!nextSibling) nextSibling = body.appendParagraph('')
        childIndex = body.getChildIndex(nextSibling)
      }
      var focusRow = options.focusRow == -1 ? (meta.cells.length-1) : options.focusRow
      var table_style = options.table_style
      var table = body.insertTable(childIndex, meta.cells)
      // format 1st col of each row
      if (table_style) table.setAttributes(table_style)
      for (var i=0;i<meta.cells.length;i++){
        var col0 = table.getRow(i).getCell(0)
        if (meta.styles && meta.styles[i]) {
          var style = meta.styles[i][0]
          col0.setAttributes(style) // set to cell
          // set to paragraph (cell content)
          col0.getChild(0).setAttributes(style)
          //col0.getChild(0).setBackgroundColor(null)
        }
        if (i==focusRow) {
          setSelection(col0.getChild(0))
        }
      }
      // remove ele if it is a slection
      if (selection) ele.removeFromParent()
    }
    
    function insertDirective(kind,name){
      if (kind=='admonition'){
        var meta, table_style, focusRow = -1
        switch(name){
          case 'Attention':
          case 'Caution':
          case 'Custom':
          case 'Danger':
          case 'Error':
          case 'Hint':
          case 'Important':
          case 'Note':
          case 'See also':
          case 'Tip':
          case 'Warning':      
            var headerBgColor = {
              'Attention':'#f0b37e',
              'Caution':'#f0b37e',
              'Custom':'#6ab0de',
              'Danger':'#f29f97',
              'Error':'#f29f97',
              'Hint':'#1abc9c',
              'Important':'#1abc9c',
              'Note':'#6ab0de',
              'See also':'#6ab0de',
              'Tip':'#1abc9c',
              'Warning':'#f0b37e',
            }
            var bgColor = {
              'Attention':'#ffedcc',
              'Caution':'#ffedcc',
              'Custom':'#e7f2fa',
              'Danger':'#fdf3f2',
              'Error':'#fdf3f2',
              'Hint':'#dbfaf4',
              'Important':'#dbfaf4',
              'Note':'#e7f2fa',
              'See also':'#e7f2fa',
              'Tip':'#dbfaf4',
              'Warning':'#ffedcc',
            }
            var admonitionName = name=='Custom' ? 'Change-me' : name
            meta = { cells:[
                ['ⓘ '+admonitionName], //row1
                ['(content of '+admonitionName+')']  //row2
              ],
              styles:[
                [{BACKGROUND_COLOR:headerBgColor[name],FOREGROUND_COLOR:'#ffffff'}],
                [{BACKGROUND_COLOR:bgColor[name],SPACING_AFTER:0}]            
              ],
              focusRow:focusRow
            }
            break
          default:
            meta = { cells : [
                ['.. '+name+'::'],
                ['(content of '+name+')']
              ],
              styles:[
                [{BACKGROUND_COLOR:'#ffffff',FOREGROUND_COLOR:'#000000'}],
                [{BACKGROUND_COLOR:'#ffffff',SPACING_AFTER:0}]
              ]
            }
        }
        if (!table_style) table_style = {
              FONT_FAMILY:'Courier New',
              //FONT_SIZE:14,
              LINE_SPACING:1.1,
              BORDER_COLOR:'#000000',
              BORDER_WIDTH: 0.25,
              BOLD:false,
              ITALIC:false   
         }
         // set the indent of the 1st cell in rows except 1st row
         /*
         if (!content_style) content_style = {
              INDENT_START:20,
              INDENT_FIRST_LINE:20
         }
         */
         //createTableAtCursor(cursor,{meta:meta,table_style:table_style})
         createTableInPlace({meta:meta,table_style:table_style,focusRow:focusRow})
      }
      else if (kind=='specialDirective'){
        var meta, table_style
        name = name.toLowerCase()
        meta = { cells : [
            ['.. '+name+'::'],
            ['(content of '+name+')'],
          ],
          styles:[
            [{BACKGROUND_COLOR:'#ffffff',FOREGROUND_COLOR:'#000000'}],
            [{BACKGROUND_COLOR:'#ffffff',SPACING_AFTER:0}]
          ]
        }
        var lowerName = name.toLowerCase()
        switch (lowerName){
          case 'generic':
            meta.cells =  [
              ['.. name:: argument'],
              [':option: value\n:option: value'],
              ['content'],
            ]
            break
          case 'codelineno':
          case 'code':
            if (lowerName=='code'){
              meta.cells =  [
                ['.. code::'],
                ['(content of code)'],
              ]
            }
            else{
              meta.cells =  [
                ['.. code-block:: python'],
                [':linenos:'],
                ['(content of code)'],
              ]
            }
            meta.styles = [
              [{BACKGROUND_COLOR:'#6ab0de',FOREGROUND_COLOR:'#ffffff',PADDING_TOP:1,PADDING_BOTTOM:1, BORDER_WIDTH:0}],
              [{BACKGROUND_COLOR:'#ffffff',FOREGROUND_COLOR:'#000000',SPACING_AFTER:0}]
            ]
            break
          case 'rawhtml':
            meta.cells =  [
              ['ϕ HTML'],
              ['(html tags to embed)'],
            ]
            meta.styles = [
              [{BACKGROUND_COLOR:'#6ab0de',FOREGROUND_COLOR:'#ffffff',PADDING_TOP:1,PADDING_BOTTOM:1, BORDER_WIDTH:0}],
              [{BACKGROUND_COLOR:'#ffffff',FOREGROUND_COLOR:'#000000',SPACING_AFTER:0}]
            ]
            break
          case 'toctree':
            var docName = DocumentApp.getActiveDocument().getName().replace(/\.(rst|md)$/,'')
            meta.styles = [
              [{BACKGROUND_COLOR:'#6ab0de',FOREGROUND_COLOR:'#ffffff',PADDING_TOP:1,PADDING_BOTTOM:1, BORDER_WIDTH:0}],
              [{BACKGROUND_COLOR:'#6ab0de',FOREGROUND_COLOR:'#ffffff',PADDING_TOP:1,PADDING_BOTTOM:1, BORDER_WIDTH:0}],
            ]
            meta.cells = [
              ['.. '+name+'::'],
              [':maxdepth: 2\n:hidden:'],
            ]
            var row3 = []
    
            /* .rst or .md in the same folder with this document */
            var bindings = PropertiesService.getUserProperties().getProperty('githubBindings')
            if (bindings) bindings = JSON.parse(bindings)
    
            var parents = DriveApp.getFileById(DocumentApp.getActiveDocument().getId()).getParents()
            var parent = parents.next()
            var files = parent.getFiles()
            var pat = /\.(rst|md)$/
            while (files.hasNext()){
              var file = files.next()
              var binding = bindings[file.getId()]
              var name
              if (binding){
                name = binding.name.replace(pat,'')
              }
              else{
                name = file.getName()
                if (pat.test(name.toLowerCase())){
                  name = name.replace(pat,'')
                }
              }
              // don't put something like "index" in the toctree, 
              // that would case infinite loop while building
              if (name != docName) row3.push(name)
            }
            if (row3.length==0) row3.push('')
            else row3.sort(function(a,b){
              var s0 = a.toLowerCase()
              var s1 = b.toLowerCase()
              return s0 > s1 ? 1 : (s0 < s1 ? -1 : 0)
            })
            meta.cells.push([row3.join('\n')])
            //meta.cells.push([''])
            break
        }
        if (!table_style) table_style = {
              FONT_FAMILY:'Courier New',
              //FONT_SIZE:14,
              LINE_SPACING:1.1,
              BORDER_COLOR:'#c0c0c0',
              BORDER_WIDTH: 0.5,
              BOLD:false,
              ITALIC:false,
              BACKGROUND_COLOR:null
         }
        //createTableAtCursor(cursor,{meta:meta,table_style:table_style})    
        createTableInPlace({meta:meta,table_style:table_style})    
      }
    }
    function reformatDirectiveStyle(){
      var selection = getSelection(false)
      var eles = []
      if (selection){
          var selectedElements = selection.getSelectedElements();
          for (var i = 0; i < selectedElements.length; ++i) {
              var selectedElement = selectedElements[i]; 
              eles.push(selectedElement.getElement())
          }
      }
      else{
        var cursor = DocumentApp.getActiveDocument().getCursor();
        if (!cursor) return
        eles.push(cursor.getElement())
      }
      var table_style = {
          FONT_FAMILY:'Courier New',
          //FONT_SIZE:14,
          LINE_SPACING:1.1,
          BOLD:false,
          ITALIC:false,
          BACKGROUND_COLOR:null
        }
      var normal = {}
      normal[DocumentApp.Attribute.HEADING] = DocumentApp.ParagraphHeading.NORMAL
      eles.forEach(function(ele){
        ele.setAttributes(normal)
        ele.setAttributes(table_style)
      })
    }
    /*
    function explicitMarkup(){
      DocumentApp.getUi().showModelessDialog(
          HtmlService
              .createHtmlOutputFromFile('explicitMarkup.html')
              .setSandboxMode(HtmlService.SandboxMode.IFRAME)
              .setWidth(400)
              .setHeight(500)
              ,'Explicit Markup'); / * pixels * /  
    }
    */
    function generate(inBase64,includeImages,wholeDocument) {
      var imgInBase64 = true
      if (typeof(wholeDocument)=='undefined') wholeDocument = true
      return JSON.stringify(generateReST(inBase64,includeImages,imgInBase64,wholeDocument))
    }
    function download(includeImages,wholeDocument){
      var inBase64 = false
      var imgInBase64 = false
      if (typeof(wholeDocument)=='undefined') wholeDocument = true
      var resp = generateReST(inBase64,includeImages,imgInBase64,wholeDocument)
      var name = resp.namespace.replace(/\.(rst|md)$/,'')
      var blobs = [Utilities.newBlob(resp.content, 'text/plain', resp.namespace+'/'+name+'.rst')]
      if (includeImages){
        resp.files.forEach(function(img){
          blobs.push(Utilities.newBlob(img.content, img.mimetype, resp.namespace+'/static/'+img.name))
        })
      }
      var zip = Utilities.zip(blobs, name+'.zip');
      return zip.getBytes()
    }
    
    function getLinkableDocuments(){
       var bindings = PropertiesService.getUserProperties().getProperty('githubBindings')        
       var targetFiles = []
       if (bindings){
         bindings = JSON.parse(bindings)
         var myBinding = bindings[DocumentApp.getActiveDocument().getId()]
         var myPath;
         if (!myBinding) return {ok:false,errmsg:'this document has not binding yet'}
         myPath = myBinding.path+(myBinding.path ? '/' : '') + myBinding.name.replace(/(.rst|.md)$/,'')
         for (var fileId in bindings){
           var binding = bindings[fileId]
           if (binding.repo != myBinding.repo) continue
           var name = binding.name.replace(/(.rst|.md)$/,'')
           var docname = DriveApp.getFileById(fileId).getName()
           var linkText = binding.path +(binding.path ? '/' : '') + name
           var targetPath = binding.path +(binding.path ? '/' : '') + name
           if (targetPath != myPath){
             targetFiles.push([docname+'@'+linkText, makeRelativePath(myPath,targetPath)])
           }
         }
       }
       return {ok:true, names:targetFiles}
    }
    
    function showCommitDialog(){
      showGithub()
      return 1
    }
    
    function showSettingsDialog(){
     showSettings()
     return 1 
    }
    

|

.. _h2e63a53b627f2f2f7385c2353281c:

sidebar.html
************


.. code-block:: python
    :linenos:

    <!DOCTYPE html>
    <html>
      <head>
        <link rel="stylesheet" href="https://ssl.gstatic.com/docs/script/css/add-ons.css">
        <base target="_top">
    <style>
    .tab {
      position:relative;
      left:0;
      top:0;
      display:none;
      padding:5px 2px 0px 10px;
    }
    .tab.active{
      display:block;
    }
    .tab-title{
      border:solid 1px #c0c0c0;
      display:inline-block;
      position:relative;
      padding:5px 8px;
      border-bottom:none;
      -webkit-border-top-left-radius: 2px;
      -webkit-border-top-right-radius: 2px;
      -moz-border-radius-topleft: 2px;
      -moz-border-radius-topright: 2px;
      border-top-left-radius: 2px;
      border-top-right-radius: 2px;
      cursor:pointer;
      text-align:center;
      width:24%;
      font-size:0.95em;
      white-space: nowrap;
      overflow-x: hidden;
      text-overflow: ellipsis;
      margin-bottom:-5px;
    }
    .tab-title.active,.tab-title.active:hover{
      top:1px;
      background-color:white;
      -webkit-box-shadow: none;
      -moz-box-shadow:    none;
      box-shadow:         none;
    }
    .tab-title:hover{
      background-color:#f0f0f0;  
      -webkit-box-shadow: 0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      -moz-box-shadow:    0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      box-shadow:         0px 0px 1px 0px rgba(50, 50, 50, 0.25);
    }
    .tab-title-bar {
      border-bottom:solid 1px #c0c0c0;
      margin-bottom:10px;
      padding:0px 10px;
    }
    .tab > .block{
        margin-top:30px  !important;
    }
    .tab > .block:first-child{
        margin-top:12px  !important;
    }
    .tab > .block > label:first-child {
      margin-bottom:5px;
      display:block;
    }
    
    button.small{
        min-width:35px;
        height:25px;
        margin-left:3px;
        margin-top:3px;
    }
    select option{
      text-align:left;
    }
    
    /* start of help */
    .help:hover{
      cursor:help;
    }
    select.help:hover,button.help:hover{
      outline:none;
      box-shadow:none;
      cursor:inherit;
    }
    .helpframe{
      display:none;
      border-radius: 5px; 
      -moz-border-radius: 5px; 
      -webkit-border-radius: 5px; 
      border: 1px solid #c0c0c0;
      color:black;
      padding:5px;
      width:95%;
      margin-top:2px;
      overflow: hidden;
    }
    .helpframe{ /* temporary disable */
      border:none;
      width:100%;
      padding:0px;
    }
    .helpframetitle{
      margin:-5px -5px 2px -5px;
      padding:2px 0px;
      background-color:#f0f0f0;
      text-align:right;
      display:none;/* temporary disable */
    }
    .helpframetitle .closebtn{
      color:#000000;
      margin-right:4px;
      padding: 0px 2px;
      font-weight:bold;
      text-decoration:none;
    }
    .helpframetitle .closebtn:hover{
      color:#f0f0f0;
      background-color:#0c0c0c;
      margin-right:4px;
      padding: 1px 3px;
      font-weight:bold;
      text-decoration:none;
    }
    .helppos{
      display:none;
      position:absolute;
      z-index:99;
      background-color:black;
      color:white;
      padding:5px;
      margin-right:10px;
      overflow: hidden;
      opacity:0;
    }
    .helpcontent{
      overflow:hidden;
    }
    #helps{
      position:absolute;
      left:-500px;
      top:-10000px;
      padding:5px;
      visibility:hidden;
      width:80%;
      overflow:hidden;
    }
    #helps table td,.helpcontent table td{
      padding:2px 10px;
    }
    #helps table th,.helpcontent table th{
      vertical-align:top;
      padding:2px;
      border-bottom:solid 1px #ebebeb;
    }
    #helps p,.helpcontent p{
      margin-top:1px;
    }
    /* end of help */
    
    /* make option be easier to click */
    option{
      padding:2px;
      border-bottom:solid 1px white;
    }
    option.option-label+option{
      border-bottom:solid 1px #d0d0d0;
    }
    option.option-label+option:last-child{
      border-bottom:solid 1px white;
    }
    .flat-btn-box{
      height:90px;
      width:255px;
    }
    .flat-btn{
      outline:#c0c0c0 solid thin;
      display:inline-block;
      float:left;
      width:25px;
      height:25px;
      line-height:25px;
      margin:2px;
      cursor:pointer;
      text-align:center;
    }
    .flat-btn-zoomin{
      display:none;
      position:absolute;
      border:solid 3px #4d90fe;
      height:45px;
      width:60px;
      z-index:99;
      background-color:white;
      font-size:1.75em;
      text-align:center;
      line-height:45px;
    }
    /*loading */
    #loading{
      display:none;
      position:absolute;
      height:100px;
      min-height: 100px;
      top:40%;
      left:5%;
      right:5%;
      width:60%;
      margin:auto;
      text-align:center;
      background-color:rgba(255,255,255,0.85);
      z-index:99;
    }
    #loading div{
      padding: 0px 0px 30px 0px;
      background-image: url('data:image/gif;base64,R0lGODlhEAALAPQAAP///wAAANra2tDQ0Orq6gYGBgAAAC4uLoKCgmBgYLq6uiIiIkpKSoqKimRkZL6+viYmJgQEBE5OTubm5tjY2PT09Dg4ONzc3PLy8ra2tqCgoMrKyu7u7gAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCwAAACwAAAAAEAALAAAFLSAgjmRpnqSgCuLKAq5AEIM4zDVw03ve27ifDgfkEYe04kDIDC5zrtYKRa2WQgAh+QQJCwAAACwAAAAAEAALAAAFJGBhGAVgnqhpHIeRvsDawqns0qeN5+y967tYLyicBYE7EYkYAgAh+QQJCwAAACwAAAAAEAALAAAFNiAgjothLOOIJAkiGgxjpGKiKMkbz7SN6zIawJcDwIK9W/HISxGBzdHTuBNOmcJVCyoUlk7CEAAh+QQJCwAAACwAAAAAEAALAAAFNSAgjqQIRRFUAo3jNGIkSdHqPI8Tz3V55zuaDacDyIQ+YrBH+hWPzJFzOQQaeavWi7oqnVIhACH5BAkLAAAALAAAAAAQAAsAAAUyICCOZGme1rJY5kRRk7hI0mJSVUXJtF3iOl7tltsBZsNfUegjAY3I5sgFY55KqdX1GgIAIfkECQsAAAAsAAAAABAACwAABTcgII5kaZ4kcV2EqLJipmnZhWGXaOOitm2aXQ4g7P2Ct2ER4AMul00kj5g0Al8tADY2y6C+4FIIACH5BAkLAAAALAAAAAAQAAsAAAUvICCOZGme5ERRk6iy7qpyHCVStA3gNa/7txxwlwv2isSacYUc+l4tADQGQ1mvpBAAIfkECQsAAAAsAAAAABAACwAABS8gII5kaZ7kRFGTqLLuqnIcJVK0DeA1r/u3HHCXC/aKxJpxhRz6Xi0ANAZDWa+kEAA7AAAAAAAAAAAA');
      background-repeat:no-repeat;
      background-position:center;
    }
    #loading-text{
      font-size:16px;
    }
    
    .modal-dialog{
      display:none;
      position:absolute;
      top:40%;
      left:5%;
      right:5%;
      width:70%;
      margin:auto;
      min-height:200px;
      z-index:99;
      box-shadow: 0 4px 16px rgba(0,0,0,.2);
      background: #fff;
      background-clip: padding-box;
      border: 1px solid #acacac;
      border: 1px solid rgba(0,0,0,.333);
      outline: 0;
      position: absolute;
      color: #000;
      padding: 15px 21px;
      font-size:14px;
    }
    .modal-dialog button{
      -webkit-border-radius: 2px;
      -moz-border-radius: 2px;
      border-radius: 2px;
      background-color: #f5f5f5;
      background-image: -webkit-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -moz-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -ms-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -o-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: linear-gradient(top,#f5f5f5,#f1f1f1);
      border: 1px solid #dcdcdc;
      border: 1px solid rgba(0,0,0,0.1);
      color: #333;
      cursor: default;
      font-family: inherit;
      font-size: 11px;
      font-weight: bold;
      height: 29px;
      line-height: 27px;
      margin:0;
      min-width: 72px;
      outline: 0;
      padding: 0 8px;  
    }
    .modal-dialog .title{
      font-weight:bold;
    }
    .modal-dialog .buttons{
        position: absolute;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
    }
    .modal-dialog button+button{
      margin-left:20px;
    }
    .modal-dialog .x{
      font-weight: bold;
      text-align: right;
      margin-top: -5px;
      margin-right: -5px;
      color: #a0a0a0;
      cursor:pointer;
    }
    
    .modal-dialog ul.options {
      height:200px;
      overflow-y:auto;
      padding-left:0px;
    }
    .modal-dialog ul.options li{
      list-style: none;
      padding:5px 0px;
      white-space:nowrap;
      outline:#f5f7f7 thin solid;
    }
    .modal-dialog ul.options li:hover{
      background-color:rgba(0,0,0,0.2);
    }
    
    /* end of loading */
    .gray {
      background-color:rgba(230, 230, 230, 0.1);
    }
    /* application specific */
    #reST{
        white-space: pre;
        overflow-y: auto;
        font-family: monospace;
        font-size: 12px;
        width: 100%;
        overflow-x: auto;
        outline: thin solid rgba(0,0,0,0.2);
        margin-top: 10px !important;   
    }
    #reSTFiles {
        width: 99%;
        padding-left:0;
    }
    #reSTFiles div {
        outline: thin solid rgba(0,0,0,0.2);
    }
    #reSTFiles div .title {
        background-color: rgba(152, 152, 152, 0.2);
        padding: 2px;
        font-size: 12px;
        font-family: monospace;
    }
    #reSTFiles div img {
        width:100%;
    }
    
    
    .hierarchy-style tr td{
      padding: 5px 20px 0px 0px;
    
    }
    .hierarchy-style tr td.part{
      font-size:18px;
    }
    .hierarchy-style tr td.chapter{
      font-size:16px;
    }
    .hierarchy-style tr td.section{
      font-size:14px;
    }
    .hierarchy-style tr td.subsection,.hierarchy-style tr td.subsubsection, .hierarchy-style tr td.subsubsubsection, .hierarchy-style tr td.paragraph{
      font-size:12px;
    }
    .hierarchy-style tr td.note{
      font-size:10px;
      padding:0px;
      color: #9c9c9c;
      border:none;
    }
    .admonition-panel td{
      padding:2px 5px;
    }
    .admonition-panel .small-table td{
      border:solid 1px rgba(199,199,199,0.5);
      min-width:50px;
    }
    .admonition-panel .small-table td.header{
      line-height:8px;
      height:8px;
    }
    .admonition-panel .small-table td.content{
    }
    .admonition-panel .small-table.attention td.header{
      background-color:#f0b37e;
    }
    .admonition-panel .small-table.attention td.content{
      background-color:#ffedcc;
    }
    .admonition-panel .small-table.danger td.header{
      background-color:#f29f97;
    }
    .admonition-panel .small-table.danger td.content{
      background-color:#fdf3f2;
    }
    .admonition-panel .small-table.hint td.header{
      background-color:#1abc9c;
    }
    .admonition-panel .small-table.hint td.content{
      background-color:#dbfaf4;
    }
    .admonition-panel .small-table.note td.header{
      background-color:#6ab0de;
    }
    .admonition-panel .small-table.note td.content{
      background-color:#e7f2fa;
    }
    
    
    .directive-panel td{
      padding:2px 5px;
    }
    .directive-panel .small-table{
      border:solid 1px rgba(199,199,199,0.5);
    }
    .directive-panel .small-table td.header{
      min-width:50px;
      line-height:8px;
      height:8px;
    }
    .directive-panel .small-table td.content{
      text-align:center;
      color: rgba(199,199,199,1);
    }
    .directive-panel .small-table td.header{
      background-color:#f0f0f0f;
    }
    .directive-panel .small-table td.content{
      background-color:#ffffff;
    }
    
    td.btn:hover {
      cursor:pointer;
      color:blue;
    }
    
    ul.options li:nth-child(even){
      background-color:#f0f0f0;
    }
    ul.options li:hover{
      background-color:#c0c0c0;
    }
    
    </style>
      </head>
      <body>
    <div class="sidebar" style="padding:5px 0px;margin:-8px">
      <div class="tab-title-bar">
        <div class="tab-title active" tab="t1" onclick="setActiveTab('t1')"><span class="i18n">Directive</span></div>
        <div class="tab-title" tab="t2" onclick="setActiveTab('t2')"><span class="i18n">Structure</span></div>
        <div class="tab-title" tab="t3" onclick="setActiveTab('t3')"><span class="i18n">Link</span></div>
        <!--
        <div class="tab-title" tab="t2" onclick="setActiveTab('t2')"><span class="i18n">Style</span></div>
        <div class="tab-title" tab="t3" onclick="setActiveTab('t3')"><span class="i18n">Conversion</span></div>
        -->
      </div>
      <div class="markup tab active" tab="t1">
          <div class="block form-group">
            <label class="help" helpname="adm" helptype="hover"><span class="i18n">Admonitions</span>:</label>
            <table class="admonition-panel">
              <tr><td><table class="small-table attention"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">&nbsp;</td></tr></table></td>
                  <td class="btn">Attention</td><td class="btn">Caution</td><td class="btn">Warning</td></tr>
              <tr><td><table class="small-table danger"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">&nbsp;</td></tr></table></td>
                  <td class="btn">Danger</td><td class="btn">Error</td></tr>
              <tr><td><table class="small-table hint"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">&nbsp;</td></tr></table></td>
                  <td class="btn">Hint</td><td class="btn">Important</td><td class="btn">Tip</td></tr>
              <tr><td><table class="small-table note"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">&nbsp;</td></tr></table></td>
                  <td class="btn">Note</td><td class="btn">See also</td><td valut="admonition" class="btn">Custom</td>
                  </tr>
            </table>        
          </div>
          <div class="block form-group">        
            <label class="help" helpname="dir" helptype="hover"><span class="i18n">Directives</span>:</label>
    
            <table class="directive-panel">
              <tr><td><table class="small-table generic"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">Generic</td></tr></table></td>
                  <td class="btn" value="generic">Generic directive</td></tr>
              <tr><td><table class="small-table code"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">Code</td></tr></table></td>
                  <td class="btn">Code</td></tr>
              <tr><td><table class="small-table code"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">#Code</td></tr></table></td>
                  <td class="btn" value="codelineno">Code with line number</td></tr>
              <tr><td><table class="small-table toctree"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">TOC</td></tr></table></td>
                  <td class="btn help" value="toctree" helptype="hover" helpname="toc">Table of Contents(index)</td></tr>
              <tr><td><table class="small-table rawhtml"><tr><td class="header">&nbsp;</td></tr><tr><td class="content">HTML</td></tr></table></td>
                  <td class="btn help" value="rawhtml" helptype="hover" helpname="rah">Embed HTML(tag,js,...)</td></tr>
            </table>
          </div>
       </div>
       <div class="structure tab" tab="t2">
          <div class="block form-group">
            <label class="help" helpname="hea" helptype="hover"><span class="i18n">Headings</span>:</label>
            <table class="hierarchy-style" style="margin-left:5px">
              <tr><td class="part btn">Part</td>      <td class="chapter btn">Chapter</td><td class="section btn">Section</td></tr>
              <tr><td class="note btn" value="part">Title</td><td class="note btn" value="chapter">H1</td>     <td class="note btn" value="section">H2</td></tr>
              <tr><td class="subsection btn" value="subsection">Sub-section</td><td class="subsubsection btn" value="subsubsection">Subsub-s.</td><td value="subsubsubsection" class="subsubsubsection btn">Subsubsub-s.</td></tr>
              <tr><td class="note btn" value="subsection">H3</td><td class="note btn" value="subsubsection">H4</td>     <td class="note btn" value="subsubsubsection">H5</td></tr>
            </table>
          </div>
          <div class="block form-group">
            <label class="help" helpname="par" helptype="hover"><span class="i18n">Text Style</span>:</label>
            <table class="hierarchy-style" style="margin-left:5px">
              <tr><td class="paragraph btn" value="paragraph">Paragraph Content</td><td class="paragraph btn" onclick="reformatDirectiveStyle()">Directive Content</td></tr>
              <tr><td class="note btn" value="paragraph">Normal text</td><td class="note" onclick="reformatDirectiveStyle()">Code style</td></tr>
            </table>
          </div>
          <div class="block form-group">
            <label><span class="i18n">Utilities</span>:</label>
            <table class="markup-panel" style="margin-left:5px">
              <tr><td class="btn" value="upgradeHeadings"><span class="help" helpname="ugh" helptype="hover">Upgrade all headings</a></td></tr>
              <tr><td class="btn" value="downgradeHeadings"><span class="help" helpname="dgh" helptype="hover">Downgrade all headings</a></td></tr>
            </table>        
          </div>
       </div>
       <div class="link tab" tab="t3">      
          <div class="block form-group">
            <label><span class="i18n">Utilities</span>:</label>
            <table class="markup-panel" style="margin-left:5px">
              <tr><td class="btn" value="hyperlink"><span class="help" helpname="hyp" helptype="hover">Add link to another document</a></td></tr>
            </table>        
          </div>
          <!--
    
          temporary disabled
    
          <div class="block form-group">
            <label class="help" helpname="pip" helptype="hover"><span class="i18n">Inline Markup</span>:</label>
            <select id="markupDomainSelection" onchange="renderMarkupOptions()">
              <option value="python" selected>Python</option>
              <option value="javascript">Javascript</option>
            </select>
            <select id="inlineMarkupSelection" onchange="inlineMarkup(this.options[this.selectedIndex].value);this.selectedIndex=0">
              <option value="">Choose an inline markup</option>
            </select>
          </div>
          <div class="block form-group">
            <label class="help" helpname="pip" helptype="hover"><span class="i18n">Directives</span>:</label>
            <select id="directiveSelection" onchange="insertDirective('directive',this.options[this.selectedIndex].value);this.selectedIndex=0">
              <option value="">Choose a directive</option>
            </select>
          </div>
          <div class="block form-group" style="min-heigth:50px">
            < !-- place hodler -- >
          </div>
          -->
      </div>
    
      <!--end of tab-->
    </div>
    <div class="masterhelpframe helpframe">
      <div class="helpframetitle">
        <a class="closebtn" onclick="closeHelp(this)">×</a>
      </div>
      <div class="helpcontent"></div>
    </div>
    
    <div id="loading" class="modal-dialog">
      <div>
        <h1><label class="i18n" id="loading-text"></label></h1>
      </div>
    </div>
    <div id="dialog" class="modal-dialog">
      <div style="width:100%">
        <div class="x">x</div>
        <p class="title"></p>
        <p class="content"></p>
        <div class="buttons">
          <button class="yes i18n blue">Delete</button><button class="cancel i18n">Cancel</button>
        </div>
      </div>
    </div>
    <span class="helppos" id="helppostmpl" style="display:none"></span>
    <span id="helppostmplpt" style="display:none;position:absolute">▲</span>
    <div style="display:none">
      <div id="helps">
        <div name="adm">Insert admonition block</div>
        <div name="dir">Insert directive block</div>
        <div name="cii">Generate images</div>
        <!--
        <div name="dow">Download generated restructuredtext file</div>
        <div name="gen">Generate restructuredtext</div>
        -->
        <div name="dgh">Downgrade 1 level of all headings in documents</div>
        <div name="hea">Set the heading level of paragraph</div>
        <div name="hyp">Add hyperlink of another document to selection</div>
        <div name="par">Set the text style of paragraph</div>
        <div name="rah">Embed html tags</div>
        <div name="toc">Insert cross-document table of contents.</div>    
        <div name="ugh">Upgrade 1 level of all headings in documents</div>
      </div>
    </div>
    <script>
    document.addEventListener( "DOMContentLoaded", initialization , false );
    var serverValues={locale:'en'};
    function localI18n(s){
      return s
    }
    function setActiveTab(name){
      var tabs = document.querySelectorAll('.tab')
      for (var i=0;i<tabs.length;i++){
        tabs[i].className = tabs[i].className.replace(/ active/,''); 
        if (tabs[i].getAttribute('tab')==name){tabs[i].className+=' active'}
      }
      var titles = document.querySelectorAll('.tab-title')
      for (var i=0;i<titles.length;i++){
        if (titles[i].getAttribute('tab')==name){titles[i].className='tab-title active'}
        else titles[i].className='tab-title';
      }
    }
    
    function moveElementToViewportCenter(ele) {
        var size = getViewportSize()
        var rect = ele.getBoundingClientRect()
        ele.style.top = window.pageYOffset + Math.round(size.height/2 - rect.height/2)+'px'
        ele.style.marginLeft = 'auto'
    }
    
    var loadingCount=0;
    function loading(yes,label){
      var title = localI18n('Please be waiting...');
    
      if (yes && typeof(yes)=='string') title = yes
    
      if ((loadingCount<0 && !yes) || (loadingCount>0 && yes)) {
        if (title) {
          document.getElementById('loading-text').innerHTML = title;
        }
        loadingCount += yes ? 1 : -1;
        return;
      }
      loadingCount += yes ? 1 : -1;
      var loadingDiv = document.getElementById('loading')
      if (loadingCount==1){
        // start loading
        loadingDiv.style.display='flex';
        document.getElementById('loading-text').innerHTML = title;
        document.querySelector('.sidebar').style.opacity = 0.5;
        moveElementToViewportCenter(loadingDiv)
      }
      else{
        // stop loading
        loadingDiv.style.display='none';
        document.querySelector('.sidebar').style.opacity = 1;
      }
    }
    function stopLoading(label){loading(false,label)}
    
    function myConfirm(title,callback){
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'  
      dialog.style.display='block';
      document.querySelector('.sidebar').style.opacity = 0.5;
      moveElementToViewportCenter(dialog)
      var cleanup = function(yes){
        callback(yes)
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.cancel').onclick = null;
        document.querySelector('.sidebar').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        dialog.style.top = '0px';
        document.querySelector('.sidebar').style.opacity = 1; 
      }
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.cancel').onclick = function(){
        cleanup(false);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      setTimeout(function(){
        document.querySelector('.sidebar').onclick = function(){
          cleanup(false);
        } 
      },100)
    }
    function myAlert(title,callback){
      if (!callback) callback = function(){}
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'
      dialog.style.display='block';
      document.querySelector('.sidebar').style.opacity = 0.5;
      var yesHTML = dialog.querySelector('.yes').innerHTML
      var cleanup = function(yes){
        callback(yes)
        document.querySelector('.sidebar').onclick = null
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.cancel').style.display = ''
        dialog.querySelector('.yes').innerHTML = yesHTML
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        document.querySelector('.sidebar').style.opacity = 1; 
      }
      dialog.querySelector('.cancel').style.display = 'none'
      dialog.querySelector('.yes').innerHTML = 'OK'
    
      moveElementToViewportCenter(dialog)
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      // click outside dialog also close the dialog
      setTimeout(function(){
        document.querySelector('.sidebar').onclick = function(){
          cleanup(false);
        } 
      },100)
    }
    
    function myPrompt(title,options,callback){
        /*
         * options = {
         *     value*:(string) value of the input element
         *     placeholder*:(string) default null
         *     content*:(string) default "<input style="width:100%;height:40px;font-size:1.5em">"
         *     button:*(dict){ok:{className:<class name>},cancel:{className:<class name>}}, default null
         * }
         */
        var dialog = document.getElementById('dialog')
        dialog.querySelector('.title').innerHTML = title;
        dialog.querySelector('.content').innerHTML = (options.content || '<input style="width:100%;height:40px;font-size:1.5em">')
        dialog.querySelector('.content').style = 'block'
        dialog.querySelector('.buttons').style = 'block'
        var input = dialog.querySelector('.content input')
        if (options.placeholder) input.setAttribute('placeholder',options.placeholder)
        if (options.value) input.value = options.value
        var buttons = [
            '<button class="ok'+((options.button && options.button.ok && options.button.ok.className) ? ' '+options.button.ok.className : '' )+'">OK</button>',
            '<button class="cancel'+((options.button && options.button.cancel && options.button.cancel.className) ? ' '+options.button.cancel.className : '' )+'">Cancel</button>',
            ]
        dialog.querySelector('.buttons').innerHTML = buttons.join('')
    
        var cleanup = function(value){
          document.querySelector('.sidebar').style.opacity = 1; 
          document.querySelector('.sidebar').onclick = null
          dialog.querySelector('.cancel').onclick = null;
          dialog.querySelector('.x').onclick = null;
          dialog.querySelector('.ok').onclick = null;
          dialog.querySelector('.buttons').innerHTML = ''
          dialog.querySelector('.content').innerHTML = ''
          dialog.querySelector('.title').innerHTML = ''
          dialog.style.display='none';
          callback(value)
        }
        setTimeout(function(){
          dialog.querySelector('.x').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.cancel').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.ok').onclick = function(){
              var text = dialog.querySelector('input').value || (options.defaultText || '')
              cleanup(text)
          }
        },500)
        document.querySelector('.sidebar').style.opacity = 0.5;     
        dialog.style.display = 'block'
        dialog.style.height = '200px'
        moveElementToViewportCenter(dialog)
        // click outside dialog also close the dialog
        setTimeout(function(){
          document.querySelector('.sidebar').onclick = function(){
            cleanup(false);
          } 
        },100)
        return {dom:dialog,callback:callback}
    }
    
    /* general */
    
    /* start of help system */
    function enableHelp(){
      var helps =  document.querySelectorAll('.help');
      var timer = 0,delay = 1000,hoverDelay=1000;
      for (var i=0,l=helps.length;i<l;i++){
        var hoverType = helps[i].getAttribute('helptype')=='hover';
        helps[i].onmouseover = function(evt){
          var target = evt.currentTarget
          var helpname = target.getAttribute('hoverhelpname') || target.getAttribute('helpname')
          // check if the same help is openning
          if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) {
            return;
          }
          if (timer>0) clearTimeout(timer);
          timer = setTimeout(function(){
            timer = 0;
            showHelp(helpname,target.getAttribute('helpCloseByBtn'),target.getAttribute('helptype'))
          },(hoverType ? hoverDelay : delay))
        }
        if (hoverType){
          helps[i].onmouseout = function(evt){
            if (timer){
              //give up to show it
              clearTimeout(timer);timer = 0;
            }
            else{
              closeHoverHelp();
            }
          }
        }
        else{
          // cancel the help showup
          helps[i].onmouseout = function(evt){
            if (timer){
              clearTimeout(timer);timer = 0;
            }
          }
        }
      }
    }
    
    function getOffset( el ) {
        var _x = 0;
        var _y = 0;
        while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
            _x += el.offsetLeft //- el.scrollLeft;
            _y += el.offsetTop //- el.scrollTop;
            el = el.offsetParent;
        }
        return { top: _y, left: _x };
    }
    function showHelp(helpname,helpCloseByBtn,helpType){
    
      /* simply deal with hover help */
      if (helpType=='hover'){
          var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
          var tmpl = document.getElementById('helppostmpl')
          var c = document.querySelector('#helps div[name="'+helpname+'"]');
          // make it visible
          var sidebarRect = document.querySelector('.sidebar').getBoundingClientRect()
          var sidebarWidth = sidebarRect.right - sidebarRect.left;
          tmpl.style.display='inline-block';
          tmpl.style.position = 'absolute';
          tmpl.style.zIndex = 99;
          var target = document.querySelector('.help[hoverhelpname="'+helpname+'"][helptype="hover"]');
          if (!target) target = document.querySelector('.help[helpname="'+helpname+'"][helptype="hover"]');
          var targetRect = target.getBoundingClientRect()
          var targetHeight = targetRect.bottom - targetRect.top;
          var targetWidth = targetRect.right - targetRect.left;
          var rect = getOffset(target)
          tmpl.style.top = (rect.top + targetHeight+4)+'px'
          tmpl.style.opacity = 0;
          tmpl.innerHTML= c.innerHTML;
          tmpl.style.maxWidth = Math.floor(sidebarWidth * 0.8)+'px'
          var tmplRect = tmpl.getBoundingClientRect()
          var tmplWidth = tmplRect.right - tmplRect.left
          var p0 = Math.floor(sidebarWidth * 0.1);
          var p1 = Math.floor(sidebarWidth * 0.9);
          var tmplpt = document.getElementById('helppostmplpt')
          tmplpt.style.top = (parseInt(tmpl.style.top)-10)+'px';
          if (rect.left < p0){
            tmpl.style.left = rect.left+'px'
            tmplpt.style.left = tmpl.style.left;
          }
          else if (rect.left+targetWidth > p1) {
            tmpl.style.left = Math.floor((rect.left+targetWidth - tmplWidth))+'px'
            tmplpt.style.left = Math.floor(parseInt(tmpl.style.left)+tmplWidth-18)+'px';
          }
          else {
            tmpl.style.left = Math.max(0,Math.floor(rect.left+targetWidth/2-tmplWidth/2))+'px'
            tmplpt.style.left = Math.max(0,Math.floor(parseInt(tmpl.style.left)+tmplWidth/2-6))+'px'
          }
          tmpl.setAttribute('active',1);
          setTimeout(function(){
            //starts animation
            tmpl.style.opacity=1;
            tmplpt.style.display='';
          },1)
        return;
      }
    
      /* need to check again for some help is triggered manually */
      if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) return;//already opened
      /* one help only, unless the existing help is a modal help */
      closeHelp()
      // create a new helpframe  
      /* prepare for animation */
      // clone the masterhelpframe  
      var helpframe = document.querySelector('.masterhelpframe.helpframe').cloneNode(true);
      helpframe.className = 'helpframe';
    
      helpframe.style.display = 'block';
      helpframe.setAttribute('helpname',helpname)
      var trigger = function(){    
        //var helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpname = this._helpname; 
        if (helpCloseByBtn) helpframe.setAttribute('modal',1)
        helpframe.querySelector('.closebtn').setAttribute('helpname',helpname)
        var cele = helpframe.querySelector('.helpcontent')
        /* find the insert position */
        var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
        helppos.parentNode.insertBefore(helpframe, helppos.nextSibling);
        /* find the help content to insert */
        var c = document.querySelector('#helps div[name="'+helpname+'"]');
        /* insert the help content */
        cele.appendChild(c);//move it
        /* starts the animation to show up*/
        var titleheight = helpframe.querySelector('.helpframetitle').clientHeight;
        /* make the helpframe visible, delay to wait the DOM been refreshed */
        setTimeout(function(){
          // scroll to make it visible
          var y = getOffset( helpframe ).top; 
          var offset = y-window.scrollY;
          if (offset<0 || offset > window.innerHeight)  window.scrollTo(0,Math.max(0,y-50));      
    
          //trigger event
          var e = document.createEvent('Event');
          e.initEvent('help-open-'+helpname,false,true);
          document.dispatchEvent(e);
    
        },100);
      }
      setTimeout(function(){trigger.apply({_helpname:helpname})},1)
    }
    
    function closeHoverHelp(){
      /* find the insert position */
      var helppos = document.querySelector('.helppos[active]');
      if (helppos===null) return;
      helppos.innerHTML='';
      // make it invisible
      helppos.style.display='none';
      helppos.style.opacity=0;
      helppos.removeAttribute('active');
      var tmplpt = document.getElementById('helppostmplpt')
      tmplpt.style.display='none';
    }
    function closeHelp(btn){
      /* release the body click */
      document.body.onclick = null;
    
      var helpname = null,helpframe=null;
      if (btn) {
        helpname = btn.getAttribute('helpname');
        helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpframe.removeAttribute('modal')//enforce to close by btn
        //fire event if closed by button
        var e = document.createEvent('Event');
        e.initEvent('help-close-'+helpname,false,true);
        document.dispatchEvent(e);
      }
      else {
        helpframe = document.querySelector('.helpframe[helpname]');
        if (!helpframe) return true;//no helpframe is showing    
        helpname = helpframe.getAttribute('helpname');
      }
      if (helpframe.getAttribute('modal')) return false
      var cele = helpframe.querySelector('.helpcontent')
      if (cele.firstChild != null){
        /*cele.removeChild(cele.firstChild);*/
        //move back to helps
        document.getElementById('helps').appendChild(cele.firstChild);    
      }
      helpframe.style.display = 'none';
      helpframe.parentNode.removeChild(helpframe);
      return true;
    }
    /* end of help system */
    
    /*
     *
     * application specific implementation starts below 
     *
     */
    function downloadContentAs(content,filename,isBinary){
      var requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
      if (!requestFileSystem){
        myAlert('Not Supported, Downloading in your browser is not supported.')
        return;
      }
      var fsErrorHandler = function(e) {
          var msg = '';
          switch (e.name) {
            case FileError.QUOTA_EXCEEDED_ERR:
              msg = 'QUOTA_EXCEEDED_ERR';
              break;
            case FileError.NOT_FOUND_ERR:
              msg = 'NOT_FOUND_ERR';
              break;
            case FileError.SECURITY_ERR:
              msg = 'SECURITY_ERR';
              break;
            case FileError.INVALID_MODIFICATION_ERR:
              msg = 'INVALID_MODIFICATION_ERR';
              break;
            case FileError.INVALID_STATE_ERR:
              msg = 'INVALID_STATE_ERR';
              break;
            default:
              msg = 'Error:'+e.name+';'+e.message;
              break;
          };
          console.log('Error: ' + msg);
      }
      requestFileSystem(window.TEMPORARY, 1024*1024, function(fs) {
        fs.root.getFile(filename, {create: true}, function(fileEntry) {
            fileEntry.createWriter(function(fileWriter) {
                var blob;
                if (isBinary){
                  var byteArray = new Uint8Array(content);
                  blob = new Blob([byteArray],{type: "application/octet-binary"});
                }
                else{
                  blob = new Blob([content],{type: "text/plain"});
                }
                fileWriter.onwriteend = function() {
                  var a = document.createElement('a')
                  a.href = fileEntry.toURL()
                  a.setAttribute('download',filename)
                  a.setAttribute('target','_blank')
                  a.click()
                };
              fileWriter.write(blob);
            }, fsErrorHandler);
        }, fsErrorHandler);
      }, fsErrorHandler);
    }
    
    function enableAdmonitions(){
      var handler = function(evt){
        var target = evt.currentTarget
        var value = target.getAttribute('value') || target.innerText
        insertDirective('admonition',value)
      }
      document.querySelectorAll('.admonition-panel .btn').forEach(function(btn){
        btn.onclick = handler
      })
    }
    
    
    function enableDirectives(){
      var handler = function(evt){
        var target = evt.currentTarget
        var value = target.getAttribute('value') || target.innerText
        insertDirective('specialDirective',value)
      }
      document.querySelectorAll('.directive-panel .btn').forEach(function(btn){
        btn.onclick = handler
      })
    }
    
    function enableHierarchyStyle(){  
      var handler = function(evt){
        var target = evt.currentTarget
        var value = (target.getAttribute('value') || target.innerText).toLowerCase()
        if (value=='hyperlink'){ 
          loading(true)
          google.script.run.withSuccessHandler(function(ret){
            loading(false)
            if (!ret.ok){
              myAlert(ret.errmsg)
              return
            }
            var names = ret.names        
            var tags = ['<ul class="options">']
            names.reverse()
            names.forEach(function(item){
              tags.push('<li path="'+item[1]+'">'+item[0]+'</li>')
            })
            tags.push('</ul>')
            myPrompt('Select document to link',{content:tags.join(''),buttons:[]},function(){
            })
            var handler = function (evt){
              dialog.querySelector('.x').click()
              var path = evt.currentTarget.getAttribute('path')
              var name = evt.currentTarget.innerText
              markup(value,{link:path+'.html',text:name})
            }
            var dialog = document.querySelector('#dialog')
            dialog.querySelectorAll('.modal-dialog ul.options li').forEach(function(li){
              li.onclick = handler
            })
            dialog.querySelector('.modal-dialog .buttons').style.display = 'none'
            var height = dialog.getBoundingClientRect().bottom
            var titleHeight =dialog.querySelector('.modal-dialog .title').getBoundingClientRect().bottom
            dialog.querySelector('.modal-dialog ul.options').style.height = (height - titleHeight - 10)+'px'
            dialog.querySelector('.modal-dialog ul.options').style.marginTop = '-10px'
          }).withFailureHandler(stopLoading).getLinkableDocuments();      
        }
        else {
          markup({link:value,text:value})
        }
      }
      document.querySelectorAll('.hierarchy-style .btn, .markup-panel .btn').forEach(function(btn){
        if (btn.getAttribute('onclick')) return // skip if btn has custom onclick
        btn.onclick = handler
      })  
    }
    function getTimestamp(){
      var now = new Date()
      return now.getFullYear()+'-'+(now.getMonth()+1)+'-'+now.getDate()+' '+now.getHours()+':'+now.getMinutes()+':'+now.getSeconds()
    }
    function getViewportSize(){
      var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
      var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
      return {width:w,height:h}
    }
    function getOuterSize(ele){
      var style = ele.currentStyle || window.getComputedStyle(ele),
        width = ele.offsetWidth, // or use style.width
        margin = parseFloat(style.marginLeft) + parseFloat(style.marginRight),
        padding = parseFloat(style.paddingLeft) + parseFloat(style.paddingRight),
        border = parseFloat(style.borderLeftWidth) + parseFloat(style.borderRightWidth),
        height = ele.offsetHeight,
        vMargin = parseFloat(style.marginTop) + parseFloat(style.marginBottom),
        vPadding = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom),
        vBorder = parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth)
        return {
          width:width + margin - padding + border,
          height:height + vMargin - vPadding + vBorder,
          vBorder:vBorder,
          vMargin:vMargin,
          vPadding:vPadding
        }
    }
    
    /*
     * properties is persistent in server. it is:
     * {
     *    githubBindings: {
     *          docID:{
     *                repo:
     *                path
     *               name:
     *                repoUrl:
     *                }
     *           }
     *     githubCredential:{
     *          username:
     *          password:
     *     }
     *  }
     *
     */
    var properties = null
    function initialization(){
      //setup markup options
      enableAdmonitions()
      enableDirectives()
      enableHierarchyStyle()
      enableHelp()
    
      /* assign initial values from persistent data */
      loading(true)
      google.script.run.withSuccessHandler(function(response){
        loading(false)
        properties = response
        githubCredentials = properties.githubCredentials
      }).withFailureHandler(stopLoading).getUserProperties();
    }
    
    /*
     *
     * Editing routines
     *
     */
    
    function markup(name,options){
      if (!name) return
      loading(true)
      google.script.run.withSuccessHandler(stopLoading).withFailureHandler(stopLoading).markup(name,options);
    }
    
    function inlineMarkup(name){
      if (!name) return
      loading(true)
      var markupDomainSelection = document.getElementById('markupDomainSelection')
      var domain = markupDomainSelection.options[markupDomainSelection.selectedIndex].value
      google.script.run.withSuccessHandler(stopLoading).withFailureHandler(stopLoading).inlineMarkup(domain,name);
    }
    function reformatDirectiveStyle(){
      loading(true)
      google.script.run.withSuccessHandler(stopLoading).withFailureHandler(stopLoading).reformatDirectiveStyle()
    }
    
    function insertDirective(kind,name){
      if (!name) return
      loading(true)
      google.script.run.withSuccessHandler(stopLoading).withFailureHandler(stopLoading).insertDirective(kind,name);
    }
    
    </script>
      </body>
    </html>
    
    
    

.. _h782b4d2b477f7f3d5b7a6f6616322027:

reSTMetadata.gs
***************


.. code-block:: python
    :linenos:

    var reSTMetadata = {
      python: function(keyname,fullname){
        var cells = [
          ['.. '+keyname+'::'+(fullname.split('::')[1])],
          ['content of '+keyname]
        ]
        var merge = []
        var styles = []
        switch(keyname){
          case 'py:function':
            cells = [
              ['.. '+keyname+':: send_message(sender, [priority=1])'],
              ['Send a message to a recipient'],
              [':param str sender: The person sending the message'],
              [':param priority: The priority of the message, can be a number 1-5'],
              [':type priority: integer or None'],
              [':return: the message id'],
              [':rtype: int'],
              [':raises ValueError: if the message_body exceeds 160 characters'],
            ]
            merge.push({row:0,cols:[2,3]})
            merge.push({row:1,cols:[1,2]})
            break      
        }
        var meta = {
          cells:cells,
          merge:merge,
          styles:styles
        }
        return meta
      },
      javascript:function(keyname,fullname){
        var cells = [
          ['.. '+keyname+'::'+(fullname.split('::')[1])],
          ['content of '+keyname]
        ]
        var merge = []
        var styles = []
        switch (keyname){
          case 'js:function':
            cells = [
              ['.. '+keyname+':: $.getJSON(href, callback[, errback])'],
              [':param string href: An URI to the location of the resource.'],
              [':param callback: Gets called with the object.'],
              [':param errback: Gets called in case the request fails. And a lot of other text so we need multiple lines.'],
              [':throws SomeError: For whatever reason in that case.'],
              [':returns: Something.'],
            ]
            break
          case 'js:class':
            cells = [
             ['.. '+keyname+':: MyAnimal(name[, age]'], 
             [':param string name: The name of the animal'],
             [':param number age: an optional age for the animal'],
            ]
            break
        }
        var meta = {
          cells:cells,
          merge:merge,
          styles:styles
        }
        return meta
      }
    }
    

|

.. _h2e2c5a17b6c914967196639535670:

generator.gs
************


.. code-block:: python
    :linenos:

    /*
     * test reST tags in http://rst.ninjs.org/
     * FAQ: http://docutils.sourceforge.net/FAQ.html
     * reST spec: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
     * reST directives: http://docutils.sourceforge.net/docs/ref/rst/directives.html#rubric
     * Sphinx: http://www.sphinx-doc.org/en/stable/rest.html
     */
    // got bytes for utf8 string
    function lengthInUtf8Bytes(str) {
      // Matches only the 10.. bytes that are non-initial characters in a multi-byte sequence.
      var m = encodeURIComponent(str).match(/%[89ABab]/g);
      return str.length + (m ? m.length : 0);
    }
    
    //see http://www.unicode.org/charts/
    // \u1100-\u11FF //korean
    // \u3000-\u303F full-width CJK Symbols and Punctuation
    // \u3041-\u309F Hiragana
    // \u30A0-\u30FF Katakana
    // \u3130-\u318F korean
    // \u3200-\u32FF korean
    //see https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
    // \u3400-\u9FFF CKJ basic \u4E00–\u9FFF, extension A \u3400–\u4DBF 1
    //see http://www.unicode.org/charts/PDF/UFF00.pdf
    // \uAC00-\uD7AF korean
    // \uFF01-\uFF60 ascii full-width
    // \uFFE0-\uFFE6 full-width, 
    var fullWidthPat=/[\u1100-\u11FF\u3000-\u30FF\u3130-\u318F\u3200-\u32FF\u3400-\u9FFF\uAC00-\uD7AF\uFF01-\uFF60\uFFE0-\uFFE6]/
    function countFullWidth(s){
        var c = 0
        for (var x=0;x<s.length;x++){
          c +=  fullWidthPat.test(s.charAt(x)) ? 1 : 0 
          //range U+AC00–U+D7AF
          //c +=  /[]/.test(s.charAt(x)) ? 1 : 0 
        }
        return c
    }
    
    function getIndentPrefix(ele,levelWidth){
      /*
       * levelWidth:(in pixel; int) how many pixel of indentation is a level
       */
      if (typeof(levelWidth)=='undefined') levelWidth = 36
      var indentLevel 
      if (ele.getType()==DocumentApp.ElementType.LIST_ITEM){
        indentLevel = ele.getAttributes()[DocumentApp.Attribute.NESTING_LEVEL]
      }
      else{
        var indent = Math.max(ele.getIndentStart(),ele.getIndentEnd(),ele.getIndentFirstLine())
         indentLevel = Math.ceil(indent / levelWidth)
      } 
      var indentLength = 4 // 4 spaces
      return duplicateChar(' ',indentLevel*indentLength)
    }
    function duplicateChar(char,size){
      // '*' -> '*****'
      var text = []
      for (var i=0;i<size;i++){
        text.push(char)
      }
      return text.join('')
    }
    function cellTextAlignment(text,width,align){
      // align: -1 :left, 0: center, 1:right
      // '123' -> '    123'
      var len = lengthInUtf8Bytes(text)
      if (align == 1) return duplicateChar(' ',width - len)+text
      else if (align == 0) {
        var size = (width - len)    
        var leftPadding = size%2==0 ? size/2 : (size+1)/2
        var rightPadding = size%2==0 ? size/2 : (size-1)/2
        return duplicateChar(' ',leftPadding)+text+duplicateChar(' ',rightPadding)
      }
      return text+duplicateChar(' ',width - len)
    }
    
    //usage:
    //text.replace(escapePat,escapeFun)
    
    // caution: |, : was not escaped intentionally
    // if escape *, it will destroy javascript
    var escapePat = /[`\*]/g 
    function escapeFun(m){
        return '\\'+m
    }
    
    var directivePats = [/`{1,2}.+?`{1,2}/g, /^\.\. \|.+?\| replace\:\:.*$/g]
    function escapeText(s){
      //preserve `some` and ``some``
      var directives = []
      var s1 = s
      directivePats.forEach(function(directivePat){
        s1 = s1.replace(directivePat,function(m){
          directives.push(m)
          return '__m__'
        })
      })
      directives.reverse()
      var s2 = s1.replace(escapePat,escapeFun)
      var s3 = s2.replace(/__m__/g,function(){
        return directives.pop()
      })
      return s3
    }
    
    function splitByWidth(nomarkupText,lineWidth,textchunks){
      /*
       * split a long text (without \n) to a specific width of several lines
       * please note:
       *   1. the heading spaces in line content will be removed
       *   2. the sepical character resulted line content will be escaped
       *
       * nomarkupText: string, should not contain markups
       * lineWidth: int, line width to cut, the cutpoint is roughly around this number
       * textchunks: array to save the splited lines content
       * 
       */
        var nomarkupTextLines = nomarkupText.replace(/\r/g,'\n').split('\n')
        var deltaOffset = 5
        var lines = []
        var pat = /[a-zA-Z]/
        nomarkupTextLines.forEach(function(line){
          var len = line.length + countFullWidth(line)
          if (lineWidth && len > lineWidth){
            var curPos = lineWidth - deltaOffset
            var maxPos = line.length
            var startPos = 0
            while (curPos < maxPos){
              var c = line.charAt(curPos)
              if (!pat.test(c)){
                var newline = line.substring(startPos,curPos+1)
                lines.push(escapeText(newline.replace(/^\s+/,''))+'\n')
                startPos = curPos+1
                curPos += lineWidth - deltaOffset
              }
              else{
                curPos +=1
              }
            }
            if (startPos <maxPos){
                var lastline = line.substr(startPos)
                lines.push(escapeText(lastline.replace(/^\s+/,'')))
            }
          }
          else{
            lines.push(escapeText(line))
          }
        })
       lines.forEach(function(line){
         textchunks.push(line)
       })
     }
    
    
    function getHeadingLevel(ele){  
      var t = ele.getHeading()
      var level = 0
      if (t==DocumentApp.ParagraphHeading.TITLE) level = 1
      else if (t==DocumentApp.ParagraphHeading.HEADING1) level = 2
      else if (t==DocumentApp.ParagraphHeading.HEADING2) level = 3
      else if (t==DocumentApp.ParagraphHeading.HEADING3) level = 4
      else if (t==DocumentApp.ParagraphHeading.HEADING4) level = 5
      else if (t==DocumentApp.ParagraphHeading.HEADING5) level = 6
      return level
    }
    
    function mergeInlineMarkup(cellLines,pat){
          var lineIndexToDel = []
          var linesLength = cellLines.length
          for (var k=0;k<linesLength;k++){
              if (pat.test(cellLines[k])){
                if (k==0){
                  //at first line and next line is not empty, merge the next line to this first line
                  if (cellLines[k+1]){
                    cellLines[k] += cellLines[k+1]
                    lineIndexToDel.push(k+1)
                    k += 1
                  }
                }
                else if (k==linesLength-1){
                  //at last line and previous line is not empty, merge this last line to the previous line
                  if (cellLines[k-1]){
                    cellLines[k-1] += cellLines[k]
                    lineIndexToDel.push(k)
                  }
                }
                else if (cellLines[k-1]=='' && cellLines[k+1]==''){
                  //keep this, do nothing
                }
                else if (cellLines[k-1]==''){
                  //merge the next line to this line
                  cellLines[k] += cellLines[k+1]
                  lineIndexToDel.push(k+1)
                  k += 1
                }
                else if (cellLines[k+1]==''){
                  //merge this line to the previous line
                  cellLines[k-1] += cellLines[k]
                  lineIndexToDel.push(k)
                }
                else{
                  //merge this line and next line to previous line
                  cellLines[k-1] += cellLines[k] + cellLines[k+1]
                  lineIndexToDel.push(k)            
                  lineIndexToDel.push(k+1)
                  k += 1
                }
              }
          }
          lineIndexToDel.reverse()
          lineIndexToDel.forEach(function(k){
            cellLines.splice(k,1)
          })
    }
    
    
    function getNormalizedUrl(url){
      var a = 'http://cross.document/'          
      if (url.indexOf('#bookmark=')==0){
        // internal link, is something like "#bookmark=id.5s63cugwc4nd"
        return url.replace(/[=\.]/g,'-')
      }
      else if (url.indexOf(a)==0){
        return url.substring(a.length)
      }
      else{
        return url
      }        
    }
    
    function markupInlineStyles(ele,attachments,options){
      /*
       * helper for generate inline links, styles
       *
       * return a string (might contains "\n") with markups of
       * links, bold, italic, subscript, superscript
       * and special-character escaping
       *
       * ele: element of Google Docs
       * links: == attachements.links
       * options: {
       *   exclusive:(obj){
       *     url:(boolean)
       *     bold:(boolean), if true, not to markup bold and italic
       *     sub:(boolean), if true, not ot markup sub and sup
       *   },
       *   lineWidth:int, if 0, do not split by width
       *   inlineStyle:boolean, if true, generate inline links, bold markups,
       *   html: boolean, if true, generate html
       *}
       */
    
      if (!ele.editAsText) return ''
    
      var links = attachments.links
      var styles = attachments.styles
    
      var exclusive = options && options.exclusive ? options.exclusive : {}
    
      /* do not support, too complex
      if (options.html){
        exclusive.fontsize = false
        exclusive.color = false
      }
      else{
        exclusive.fontsize = true
        exclusive.color = true
      }
      */
    
      var lineWidth = options && options.lineWidth ? options.lineWidth : 0
    
      var textObj = ele.editAsText();
      var text = ele.getText();
      var chunks = []
      var types = ['url','sub','sup','bold','italic','fontsize']
      var curType = -1 // initial no type
      var curItem = null
      var attrBoldKey = DocumentApp.Attribute.BOLD
      var attrItalicKey = DocumentApp.Attribute.ITALIC
      var subKey = DocumentApp.TextAlignment.SUBSCRIPT
      var supKey = DocumentApp.TextAlignment.SUPERSCRIPT
      var fontsizeKey = DocumentApp.Attribute.FONT_SIZE
    
      for (var ch=0; ch < text.length; ch++) {
        // firstly, checks the link
        var url = exclusive.url ? null : textObj.getLinkUrl(ch);    
        if (url != null) {
            if (curType === 0) {
              curItem.endOffsetInclusive = ch;
            }
            else{
              // We are now!
              curType = 0;
              curItem = {
                type:curType,
                url:String( url ), // grab a copy
                startOffset: ch,
                endOffsetInclusive:ch
              };
              chunks.push(curItem)
            }
        }
        else {
    
            if (curType === 0) {
              // Not any more, we're not.
              curType = -1
              curItem = null
            }
    
            var textAlign = exclusive.sub ? null : (textObj.setTextAlignment ? textObj.getTextAlignment(ch) : null)
            var attr = exclusive.bold ? null : (textObj.getAttributes(ch));
            var chType = -1
            var data = null
            var subType = false //if true, chType is not changed, but a new chunk is required. ex font-size changed
            if (textAlign===subKey){
              chType = types.indexOf('sub') 
            }
            else if (textAlign===supKey){
              chType = types.indexOf('sup')
            }
            else if (attr && attr[attrBoldKey]) {
              chType = types.indexOf('bold')
            }
            else if (attr && attr[attrItalicKey]) {
              chType = types.indexOf('italic')          
            }
            /* do not support, too much complext
            else if (attr && attr[fontsizeKey]){
              chType = types.indexOf('fontsize')
              if (curItem && curItem.data && curItem.data.fontsize && curItem.data.fontsize==attr[fontsizeKey]){
              }
              else{
                subType = true
                data = {fontsize:attr[fontsizeKey]}
              }
            }
            */
            else{
              // do nothing
            }
    
            if (curType>=0 && curType===chType){
              // continue the current type
              curItem.endOffsetInclusive = ch
            }
            else if (curType>=0 && chType>=0 && (curType!==chType || subType)){
              // endup current type , start another type
              curItem = {
                  startOffset : ch,
                  type:chType,
                  endOffsetInclusive:ch
              }
              if (data) curItem.data = data
              chunks.push(curItem)
            }
            else if (chType === -1 && curType >= 0){
              // end up current chunk item
              curItem = null
            }
            else if (chType >=0 && curType === -1){
              // starts a new type
              curItem = {
                  startOffset : ch,
                  type:chType,
                  endOffsetInclusive:ch
              }
              if (data) curItem.data = data
              chunks.push(curItem)
            }
            else{
              // normal text
            }
            curType = chType
        }
      }
      // with links
      var textchunks = []
      if (chunks.length==0) {
        // no links, so do char escaping and new line replacement only
        /*
        if (lineWidth) {
          splitByWidth(text,lineWidth,textchunks)
          return textchunks.join('\n')
        }
        else{
          return escapeText(text)
        }
        */
        if (options.html) return text
        else return escapeText(text).replace(/\r/g,'\n')
      }
      var pos = 0
      // don't trim the chunk text, otherwize texts will crash to each other
      var countSpace = function(s){
        var trimed = s.trim()
        if (trimed=='') return null
        var scount=''
        for (var i=0,end=s.length;i<end;i++){
          if (s.charAt(i)==' ') scount += ' '
          else break
        }
        var ecount = ''
        for (var i=s.length-1;i>=0;--i){
          if (s.charAt(i)==' ') ecount += ' '
          else break
        }
        return [scount,trimed,ecount]
      }
      chunks.forEach(function(chunk){
        // do escaping for not-in-link text, allow line break and spaces in this text chunk
        var nomarkupText = text.substring(pos,chunk.startOffset)
        /*
        if (lineWidth) {
          var tempChunks = []
          splitByWidth(nomarkupText,lineWidth,tempChunks)
          tempChunks.forEach(function(line,i){
            if (i>0) textchunks.push('\n')
            textchunks.push(line)
          })
          textchunks.push(escapeText(nomarkupText).replace(/\r/g,'\n'))
        }
        else{
          //textchunks.push(nomarkupText.replace(escapePat,escapeFun).replace(/\r/g,'\n'))
          textchunks.push(escapeText(nomarkupText).replace(/\r/g,'\n'))
        }
        */
        if (options.html){
          textchunks.push(nomarkupText)
        }
        else{
          textchunks.push(escapeText(nomarkupText).replace(/\r/g,'\n'))
        }
    
        pos = chunk.endOffsetInclusive+1
        var chunktext = text.substring(chunk.startOffset,pos).replace(/[\n\r]/g,' ')
        switch (chunk.type){
          case 0: //link
            // don't allow multiple lines in link text, for prevent mis-leading in next converting processes.
            // also do escaping for link text
            pos = chunk.endOffsetInclusive+1 
            if (options.html){
              //var linkText = text.substring(chunk.startOffset,pos).replace(/[\n\r]/g,' ')
              var url = getNormalizedUrl(chunk.url)
              var p = url.indexOf('://')
              var blank = (p>0 && p < 10) ? ' target="_blank"' : ''         
              textchunks.push('<a href="'+url+'"'+blank+'>'+chunktext+'</a>')
            }
            else{        
              //var linkText = escapeText(text.substring(chunk.startOffset,pos)).replace(/[\n\r]/g,' ')
              chunktext = escapeText(chunktext)
              var spaces = countSpace(chunktext)
              if (spaces){
                textchunks.push(spaces[0])
                if (options.inlineStyle){
                  textchunks.push(' `'+spaces[1]+' <'+chunk.url+'>`__ ')
                }
                else{
                  // use replace style
                  if (textchunks.length) textchunks.push('\\ ')
                  textchunks.push('|LINK'+(links.length+1)+'|\\ ')
                  links.push([getNormalizedUrl(chunk.url),spaces[1]])
                }
                textchunks.push(spaces[2])
              }
              else{
                textchunks.push(chunktext)
              }
            }
            break
          case 1: //sub      
    
            if (chunktext) {
              if (options.html){
                textchunks.push('<sub>'+chunktext+'</sub>')
              }
              else{
                chunktext = escapeText(chunktext)
                var spaces = countSpace(chunktext)
                if (spaces){
                  textchunks.push(spaces[0])
                  if (options.inlineStyle){
                    textchunks.push('\\ :sub:`'+spaces[1]+'`\\ ')
                  }
                  else{
                    var replaceMark = '\\ |STYLE'+styles.length+'|\\ '
                    textchunks.push(replaceMark)
                    styles.push(['|STYLE'+styles.length+'|',':sub:`'+spaces[1]+'`'])
                  }
                  textchunks.push(spaces[2])
                }
                else{
                  textchunks.push(chunktext)
                }
              }
            }
            break
          case 2: //sup
            //var chunktext = text.substring(chunk.startOffset,pos).replace(/[\n\r]/g,' ')
            if (chunktext) {
              if (options.html){
                textchunks.push('<sup>'+chunktext+'</sup>')
              }
              else{
                chunktext = escapeText(chunktext)
                var spaces = countSpace(chunktext)
                if (spaces){
                  textchunks.push(spaces[0])
                  if (options.inlineStyle){
                    textchunks.push('\\ :sup:`'+spaces[1]+'`\\ ')
                  }
                  else{
                    var replaceMark = '\\ |STYLE'+styles.length+'|\\ '
                    textchunks.push(replaceMark)
                    styles.push(['|STYLE'+styles.length+'|',':sup:`'+spaces[1]+'`'])
                  }
                  textchunks.push(spaces[2])
                }
                else{
                  textchunks.push(chunktext)
                }
              }
            }        
            break
          case 3: //bold
            // var chunktext = text.substring(chunk.startOffset,pos).replace(/[\n\r]/g,' ')
            if (chunktext) {
              if (options.html){
                textchunks.push('<span style="font-weight:bold">'+chunktext+'</span>')
              }
              else{
                chunktext = escapeText(chunktext)
                var spaces = countSpace(chunktext)
                if (spaces){
                  textchunks.push(spaces[0])
                  if (options.inlineStyle){
                    if (textchunks.length)  textchunks.push('\\ ')
                    textchunks.push('**'+spaces[1]+'**\\ ')
                  }
                  else{
                    var replaceMark = '\\ |STYLE'+styles.length+'|\\ '
                    textchunks.push(replaceMark)
                    styles.push(['|STYLE'+styles.length+'|','**'+spaces[1]+'**'])
                  }
                  textchunks.push(spaces[2])
                }
                else{
                  textchunks.push(chunktext)
                }
              }
            }
    
            break
          case 4: //italic
            // var chunktext = text.substring(chunk.startOffset,pos).replace(/[\n\r]/g,' ')
            if (chunktext) {
              if (options.html){
                textchunks.push('<span style="font-style:italic">'+chunktext+'</span>')
              }
              else{
                chunktext = escapeText(chunktext)
                var spaces = countSpace(chunktext)
                if (spaces){          
                  textchunks.push(spaces[0])
                  if (options.inlineStyle){
                    if (textchunks.length) textchunks.push('\\ ')
                    textchunks.push('*'+spaces[1]+'*\\ ')
                  }
                  else{
                    var replaceMark = '\\ |STYLE'+styles.length+'|\\ '
                    textchunks.push(replaceMark)
                    styles.push(['|STYLE'+styles.length+'|','*'+spaces[1]+'*'])
                  }
                  textchunks.push(spaces[2])
                }
                else{
                  textchunks.push(chunktext)
                }
              }
            }        
            break
          /* do not support, too much complext
          case 5: //fontsize
            if (chunktext) {
              if (options.html){
                Logger.log(chunk)
                textchunks.push('<span style="font-size:'+chunk.data.fontsize+'">'+chunktext+'</span>')
              }
              else{
                textchunks.push(chunktext)
              }
            }        
            break
          */
        }
      })
      // pickup the last chunk text and do escaping, allow line break and spaces in this text chunk
      var lastText = text.substring(pos)
      if (options.html){
        textchunks.push(lastText)
      }
      else{
        textchunks.push(escapeText(lastText).replace(/\r/g,'\n'))
      }
      return textchunks.join('')
    }
    
    function markupLineBlock(lines,indent){
       var markedLines = []
       var lastPrefix;
       var prefix;
       lines.forEach(function(line,i){
    
         // do not add | if the previous line is empty
         prefix = lines.length == 1 ? '' : (i==0 ? (lines[1]=='' ? '' :'| ') : (lines[i-1]=='' ? '': '| ') )
    
         //prefix = '| '
    
         // append an extra line in front of a line block
         if (i==0 && (prefix)) markedLines.push('')
    
         // append an extra line at the end of a line block
         if (lastPrefix && (prefix=='')) markedLines.push('')
    
         markedLines.push(prefix+indent+line)
    
         lastPrefix = prefix
       })
    
       // append an extra line at the end of a line block
       if (prefix) markedLines.push('')
    
       return markedLines
    }
    
    function addInternalLink(bookmarkElements,rootEle,lines){
      /*
       * lookup the given rootEle in cached bookmarks and add label for internal link if it is found
       */
      var idx = -1
      bookmarkElements.some(function(item,i){
        // footnote has not item[0].getText
        if (!rootEle.getText) {return}
        else if (rootEle.getText()==item[0].getText()){
          // item[1] is something like "id.5s63cugwc4nd", we only need the value
          if (lines[lines.length-1]) lines.push('')
          lines.push('.. _bookmark-'+item[1].replace('.','-')+':')
          lines.push('')
          idx = i
          return true
        }
      })
      // remove a matched bookmark item
      if (idx>=0) bookmarkElements.splice(idx,1)
    }
    
    function ImageBag(){
      this.images = {}
      this.imgCount = 0
      this.keys = []
      this.imgType = 'png'
    }
    ImageBag.prototype = {
      put:function(namespace,files,ele){
        //var blob =ele.getAs('image/'+this.imgType)
        var blob = ele.getBlob()
        Logger.log(blob.getContentType())
        var mimetype = blob.getContentType()
        var suffix = mimetype.split('/')[1]
        var sno = files.length+1
        var imgNo = this.getImgNo(blob,mimetype,suffix)
        var basename = namespace.split('/').pop()
        files.push({
          name:basename+'_'+imgNo+'.'+suffix,
          sno:sno,
          imgNo:imgNo,
          width:ele.getWidth(),
          height:ele.getHeight(),
          title:ele.getAltTitle(),
          url:ele.getLinkUrl()
        })
        var markup = '\\ |IMG'+sno+'|\\ '
        return markup
      },
      putHTML:function(namespace,files,ele){
        //var blob = ele.getAs('image/'+this.imgType)
        var blob = ele.getBlob()
        Logger.log(blob.getContentType())
        var sno = files.length+1
        var basename = namespace.split('/').pop()
        var mimetype = blob.getContentType()
        var suffix = mimetype.split('/')[1]
        var imgNo = this.getImgNo(blob,mimetype,suffix)
        var meta = {
          name:basename+'_'+imgNo+'.'+suffix,
          sno:sno,
          imgNo:imgNo,
          width:ele.getWidth(),
          height:ele.getHeight(),
          title:ele.getAltTitle(),
          url:ele.getLinkUrl()
        }
        //vertical-align: baseline; is google docs' default mode
        var html = ['<img src="_images/'+meta.name+'" style="width:'+meta.width+'px;height:'+meta.height+'px;vertical-align: baseline;">']
        if (meta.url) {
          var url = getNormalizedUrl(meta.url)
          var p = url.indexOf('://')
          var blank = (p>0 && p < 10) ? ' target="_blank"' : ''    
          html.splice(0,0,'<a href="'+url+'"'+blank+'>')
          html.push('</a>')
        }
        files.push(meta)
        return html.join('')
      },
      getImgNo:function(blob,mimetype,suffix){
        var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, blob.getBytes());
        var key = '';
        digest.forEach(function(byte){
          key += byte.toString(16)
        })
        if (this.images[key]) return this.images[key].imgNo
        else{
          this.keys.push(key)
          this.imgCount += 1
          this.images[key] = {
            imgNo:this.imgCount,
            blob: blob,
            mimetype:mimetype,
            suffix:suffix
          }
          return this.imgCount
        }
      },
      full:function(basename,imgFiles,includeImages,imgInBase64){
        var self = this
        this.keys.forEach(function(key){
          var imgItem = self.images[key]
          var blob = imgItem.blob
          var content
          if (includeImages){
            if (imgInBase64){
              content = Utilities.base64Encode(blob.getBytes())
            }
            else{
              content = blob.getBytes()
            }
          }
          else{
            content = ''
          }
          Logger.log('le='+content.length+';')
          var imgname = basename+'_'+imgItem.imgNo+'.'+imgItem.suffix
          imgFiles.push({name:imgname,content:content,mimetype:imgItem.mimetype})
        })  
      }
    }
    var imageBag = new ImageBag()
    /*
     *  element generating starts
     */
    
    function generateHeadingParagraph(namespace, rootEle, lines, attachements, options){
      /*
       * if the given paragraph element has heading, generate it, otherwise do nothing
       */
      var headingLevel = getHeadingLevel(rootEle)  
      if (headingLevel==0) return false
    
      var hLines = []
    
      // donot markup bold/italic, because the content will be in <H1>, the font-style is useless
      var exclusive = options.exclusive
      options.exclusive = {
        bold:true,
      }
      var complete = generateElementTextOnly(namespace, rootEle, hLines, attachements, options)
      //restore exclusive
      options.exclusive = exclusive
    
      // deal with images
      var imgPat = /^\\ \|IMG\d+\|\\ $/
      mergeInlineMarkup(hLines,imgPat)  
      // deal with footnotes
      var pat = /^\\ \[\#F\d+\]_\\ $/
      mergeInlineMarkup(hLines,pat)
    
      var txt = hLines.join('\n')
    
      // ensure there is an empty line above
      if (lines[lines.length-1] != '') lines.push('')
    
      // add an internal link target
      var digest = 'h'+getMD5(txt) //return value of getMD5() might starts with '-', so prefix with 'H'
      lines.push('.. _'+digest+':')
      lines.push('')
    
      lines.push(txt)
    
      var headingMarkup = [null,'#','*','=','-','~','^']  
      var marker = headingMarkup[headingLevel]
      lines.push(duplicateChar(marker,txt.length+countFullWidth(txt)))
    
      lines.push('')//empty line below
      return true
    }
    function generateText(ele,lines,attachments,options){
      /*
       * For text emelment, we do:
       * 1. markup hyper links, also, handles the escaping special characters 
       * 2. handle indent for mulple lines
       * 3. searching for directives and handle it correctly
       */
      var text = markupInlineStyles(ele,attachments,{lineWidth:options.lineWidth,exclusive:options.exclusive,inlineStyle:options.inlineStyle})
      var multilines = text.split('\n')
      multilines.forEach(function(line){
        lines.push(options.indent+line)
      })  
      return true
    }
    
    function generateTable(namespace,ele,lines, attachements, options){
    
      var files = attachements.files
      var footnotes = attachements.footnotes
    
      var maxRows = ele.getNumRows()
      var maxCols = 0
      var rowsData = []
      var maxColLength = []
      var maxRowHeight = []
      var numHeaderRow = 0
      var findHeaderRows = true
    
      if (options.htmlTable){
        var getStyle = function(value,style,styleName,suffix){
          if (typeof(value) != 'undefined' && value !==null ) style.push(styleName+':'+value+(suffix || ''))
        }
        var tableWidth = 0
        var row = ele.getRow(0)
        var cols = row.getNumCells()
    
        for (var j=0;j<cols;j++){
          tableWidth += row.getCell(j).getWidth()
        }
    
        var tableWidthPercent = tableWidth ? Math.round(100*tableWidth/options.bodyWidth) : 100;
        var tableStyle = ['width:'+tableWidthPercent+'%']
        var tableAttr = ele.getAttributes()
        getStyle(tableAttr[DocumentApp.Attribute.BACKGROUND_COLOR],tableStyle,'background-color')
    
        // api dose not return these value
        //var halign = tableAttr[DocumentApp.Attribute.HORIZONTAL_ALIGNMENT]
        //Logger.log([tableAttr[DocumentApp.Attribute.MARGIN_LEFT],tableAttr[DocumentApp.Attribute.MARGIN_RIGHT]])
    
        var cellDefaultBorder = ''
        if (tableAttr[DocumentApp.Attribute.BORDER_WIDTH]){
          cellDefaultBorder= ';border:solid '+tableAttr[DocumentApp.Attribute.BORDER_WIDTH]+'px '+tableAttr[DocumentApp.Attribute.BORDER_COLOR]
        }
      }
    
      var rowSpans = []
      for (var i=0;i<maxRows;i++){
        var row = ele.getRow(i)
        var cols = row.getNumCells()
        if (cols > maxCols) maxCols = cols
        var rowdata = []
        var isHeader = findHeaderRows
    
        //retrieve row-span array
        var rowSpan = null
        if (rowSpans.length){
          rowSpan = rowSpans.splice(0,1)[0]
        }  
        for (var j=0;j<cols;j++){
          if (rowSpan && rowSpan[j]) {
            //column in row-span
            continue
          }
          var cell = row.getCell(j)
          var attr = cell.getAttributes()
          var firstChild = cell.getChild(0)
          if (isHeader){
            var isBold = firstChild.getAttributes()[DocumentApp.Attribute.BOLD]
            if (!isBold) isHeader = false
          }
    
          if (options.htmlTable){
    
            // collect cell style
            var style=[]
    
            var align = cell.getChild(0).getAttributes()[DocumentApp.Attribute.HORIZONTAL_ALIGNMENT]
            // -1:left, 0: center, 1:right
            var cellAlign =  (align == DocumentApp.HorizontalAlignment.CENTER) ? 0 : ((align == DocumentApp.HorizontalAlignment.RIGHT) ? 1 : -1 )
            if (cellAlign > -1) style.push('text-align:'+(cellAlign==0 ? 'center' : 'right'))
    
            // assign column width
            if (i==0 && tableWidth){
              var tdWidth = Math.round(100*cell.getWidth()/tableWidth) 
              style.push('width:'+tdWidth+'%')
            }
    
            // assign cell background and foreground color
            getStyle(attr[DocumentApp.Attribute.BACKGROUND_COLOR]||null,style,'background-color')
            getStyle(attr[DocumentApp.Attribute.FOREGROUND_COLOR],style,'color')
            // now way to get height (2017/01/12)
            //getStyle(attr[DocumentApp.Attribute.HEIGHT],style,'height')
            getStyle(attr[DocumentApp.Attribute.VERTICAL_ALIGNMENT],style,'vertical-align')
            getStyle(cell.getPaddingTop() ,style,'padding-top','px')
            getStyle(cell.getPaddingBottom() ,style,'padding-bottom','px')
            getStyle(cell.getPaddingLeft() ,style,'padding-left','px')
            getStyle(cell.getPaddingRight() ,style,'padding-right','px')
    
            var cellBorder        
            if (attr[DocumentApp.Attribute.BORDER_WIDTH]){
              // seems api does not report this value
              cellBorder=';border:solid '+Math.round(attr[DocumentApp.Attribute.BORDER_WIDTH]/2)+'px '+attr[DocumentApp.Attribute.BORDER_COLOR]
            }
            else{
              cellBorder = cellDefaultBorder
            }
    
            // update row-span table
            var colspan = cell.getColSpan()
            var rowspan = cell.getRowSpan()
            if (rowspan>1) {
              for (var x=0;x<rowspan-1;x++){
                if (rowSpans.length > x) {
                  for (var z=0;z<colspan;z++){
                    rowSpans[x][j+z] += 1
                  }
                }
                else {
                  //create a new row for registing span
                  var spans = []
                  for (var y=0;y<cols;y++){
                    spans.push((y>=j && y<(j+colspan)) ? 1 : 0)
                  }
                  rowSpans.push(spans)
                }
              }
            }
            //jump to next non-span column
            if (colspan>1) j+= (colspan-1)
    
            var cellLines = ['<t'+(isHeader ? 'h' : 'd')+(rowspan>1 ? ' rowspan="'+rowspan+'"' : '')+(colspan>1 ? ' colspan="'+colspan+'"' : '')+(style.length ? ' style="'+style.join(';')+cellBorder+'"' : (cellBorder ? ' style="'+cellBorder+'"' : ''))+'>']
    
            var charWidth = 6.0
            var lineWidth =  Math.floor((cell.getWidth() ? cell.getWidth() :(options.bodyWidth)/cols)/charWidth)
            var myoptions = {
              exclusive:{
                bold: isHeader ? true : false
              },
            }        
            var numChildren = cell.getNumChildren()
            for (var k=0;k<numChildren;k++){
              var cellChild = cell.getChild(k)
              generateElementInHTML(namespace,cellChild,cellLines, attachements,myoptions)
            }
    
            cellLines.push('</t'+(isHeader ? 'h' : 'd')+'>')
            rowdata.push([cellLines.join('')])
          }
          else{
            // cell content in lines
            var cellLines = []
            var charWidth = 6.0
            var lineWidth =  Math.floor((cell.getWidth() ? cell.getWidth() :(options.bodyWidth)/cols)/charWidth)
            var myoptions = {
              indent:'',
              level: 0,
              pureText: isHeader ? true : false,
              lineWidth:lineWidth,
              bodyWidth:options.bodyWidth,
              inlineStyle:options.inlineStyle,
              exclusive:options.exclusive,
              htmlTable:false
            }
    
            var numChildren = cell.getNumChildren()
            for (var k=0;k<numChildren;k++){
              var cellChild = cell.getChild(k)
              generateElementTextOnly(namespace,cellChild,cellLines, attachements,myoptions)
            }
    
            // deal with images
            var imgPat = /^\\ \|IMG\d+\|\\ $/
            mergeInlineMarkup(cellLines,imgPat)
    
            // deal with footnotes
            var pat = /^\\ \[\#F\d+\]_\\ $/
            mergeInlineMarkup(cellLines,pat)
    
    
            if (cellLines.length==0) cellLines.push('')
    
            rowdata.push(cellLines)
    
            cellLines.forEach(function(line){
              // calculate max width of this column 
              var lineLength
              if (line){
                lineLength = line.length+countFullWidth(line)
              }
              else{
                lineLength = 3  // at least 3
              }
    
              if (!maxColLength[j]){
                maxColLength[j] = lineLength
              }
              else if (maxColLength[j]<lineLength){
                maxColLength[j] = lineLength
              }
            })
            // calculate max heigth of this row
            var lineHeight = cellLines.length
            if (!maxRowHeight[i]) maxRowHeight[i] = lineHeight
            else if (maxRowHeight[i]<lineHeight) maxRowHeight[i] = lineHeight
    
          }
        }
        if (isHeader) numHeaderRow += 1
        else findHeaderRows = false
    
        rowsData.push(rowdata)
      }
    
      /*
      * start to generate reST table
      */
    
      lines.push('') // to seperate from previous content
    
      if (options.htmlTable){
        var html =['<table cellspacing="0" cellpadding="0" style="'+tableStyle.join(';')+'">']
        // iterate every row
        if (numHeaderRow) html.push('<thead>')
        else html.push('<tbody>')
        for (var i=0;i<rowsData.length;i++){      
          if (numHeaderRow && i==numHeaderRow){
            html.push('</thead><tbody>')
          }
          // iterate every line of this row
          var row = ele.getRow(i)
          var style=[]
          var attr = row.getAttributes()
          if (attr[DocumentApp.Attribute.BACKGROUND_COLOR]) style.push('background-color:'+attr[DocumentApp.Attribute.BACKGROUND_COLOR])
          if (attr[DocumentApp.Attribute.FOREGROUND_COLOR]) style.push('color:'+attr[DocumentApp.Attribute.FOREGROUND_COLOR])
          if (attr[DocumentApp.Attribute.FONT_SIZE]) style.push('font-size:'+attr[DocumentApp.Attribute.FONT_SIZE]+'px')
          if (attr[DocumentApp.Attribute.FONT_FAMILY]) style.push('font-family:'+attr[DocumentApp.Attribute.FONT_FAMILY])
          var tr = ['<tr'+(style.length ? ' style="'+style.join(';')+'"' : '')+'>']
    
          var rowData = rowsData[i]
          tr.push('</tr>')
          html.push('<tr>'+rowData.join('')+'</tr>')
        }
        html.push('</tbody></table>')
    
        var no = 1+(attachements.replacements.length)    
        lines.push('|REPLACE'+no+'|')
        lines.push('')
    
        var replacementContent = ['.. |REPLACE'+no+'| raw:: html']
        replacementContent.push('')
        html.forEach(function(row){
          replacementContent.push(options.indent+'    '+row)
        })
        replacementContent.push('')
        attachements.replacements.push(replacementContent)
    
      }
      else{
    
        // header line
        var rowLine = []
        for (var i=0;i<maxColLength.length;i++){
          rowLine.push('+')
          rowLine.push(duplicateChar('-',maxColLength[i]))
        }
        rowLine.push('+')
        var hLine = rowLine.join('')
    
        // iterate every row
        for (var i=0;i<rowsData.length;i++){
    
          if (numHeaderRow && i==numHeaderRow){
            var rowLine = []
            for (var j=0;j<maxColLength.length;j++){
              rowLine.push('+')    
              rowLine.push(duplicateChar('=',maxColLength[j]))
            }
            rowLine.push('+')
            lines.push(rowLine.join(''))
          }
          else{
            lines.push(hLine)
          }
    
          // iterate every line of this row
          for (var h=0;h<maxRowHeight[i];h++){
            var line = ['']
            var rowData = rowsData[i]
            // iterate every column of this line in this row
            for (var j=0;j<rowData.length;j++){
              line.push('|')
              var cellLines = rowData[j]
              var colLineData = cellLines[h]
              if (colLineData){
                var paddingLength = maxColLength[j] - (colLineData.length+countFullWidth(colLineData))
                line.push(colLineData+duplicateChar(' ',paddingLength))
              }
              else{
                line.push(duplicateChar(' ',maxColLength[j]))
              }
            }
            line.push('|')
            lines.push(line.join(''))
          }
        }
        // bottom line
        lines.push(hLine)
      }
      return true
    }
    
    function generateDirectiveTable(namespace,ele,lines, attachements, options){
    
      var files = attachements.files
      var footnotes = attachements.footnotes
    
      var maxRows = ele.getNumRows()
      var maxCols = 0
      var tableData = []
      var contentStarted = false
      var directiveName;
      var lines2append = lines
      for (var i=0;i<maxRows;i++){
        var row = ele.getRow(i)
        var cols = row.getNumCells()
        if (cols > maxCols) maxCols = cols
        var rowdata = []
        for (var j=0;j<cols;j++){
          var cell = row.getCell(j)
          var firstChild = cell.getChild(0)
    
          // first row
          if (i==0){
            // directive name
            var firstLine = cell.getText().split(':')
            var firstChunk = firstLine[0].trim()
            if (firstChunk.substr(0,1)=='ⓘ' && (!/^ⓘ\s*(attention|caution|danger|error|hint|important|note|see\s+also|tip|warning)\s*$/i.test(firstLine[0]))){
              // custom admonition
              firstLine[0]='.. admonition:: '+firstLine[0].trim().replace(/(^ⓘ\s*)/g,'')
              rowdata.push([firstLine[0]])
              directiveName = 'admonition'
            }
            if (firstChunk.substr(0,1)=='ϕ'){
              var name = firstChunk.substr(1).trim().toLowerCase()
              switch (name){
                case 'html':
                  directiveName = 'raw'
                  var no = 1+(attachements.replacements.length)
                  //Logger.log('no='+no)
                  rowdata.push(null)
                  lines.push('')
                  lines.push('|REPLACE'+no+'|')
                  lines2append = ['.. |REPLACE'+no+'| raw:: html']
                  attachements.replacements.push(lines2append)
                  break
              }
            }
            else{
              // admonition or others, not custom admonition
              // should starts with .. or ⓘ
    
              firstLine[0] = firstChunk.replace(/ⓘ\s*?/,'.. ').replace(/see also/i,'seealso')
              // insert : if necessary
              if (firstLine[1] !== '') firstLine.splice(1,0,'')
              // ensure there must be '::' at the end
              if (firstLine.length<3) firstLine.push(' ')
              // ensure a space after '::'
              if (firstLine[2].substr(0,1) != ' ') firstLine[2] = ' '+firstLine[2]
    
              // for code-block, there must has an language          
              if (firstLine[0]=='.. code-block' && firstLine[firstLine.length-1].trim()==''){
                 firstLine[firstLine.length-1] = ' python'
              }
    
              rowdata.push([firstLine.join(':')])
              directiveName = firstLine[0]
            }
            break
          }
    
          // second row and below
          var cellLines = []
          var charWidth = 6.0
          var lineWidth =  Math.floor((options.bodyWidth/cols)/charWidth)
          var myoptions = {
            indent:'',
            level: 0,
            pureText: false,
            lineWidth:lineWidth,
            bodyWidth:options.bodyWidth,
            lineByLine:true,
            inlineStyle:options.inlineStyle,
            exclusive:{},
            htmlTable:options.htmlTable
          }
    
          var numChildren = cell.getNumChildren()
          var pureTextPat = /(code-block|code|raw)$/i
          for (var k=0;k<numChildren;k++){
            var cellChild = cell.getChild(k)
            // keep empty line          
            if (cellChild.getType()==DocumentApp.ElementType.PARAGRAPH && ((cellChild.getNumChildren()==0)||(
                cellChild.getNumChildren()==1 && 
                cellChild.getChild(0).getType()==DocumentApp.ElementType.TEXT && 
                cellChild.getChild(0).getText().trim()==''))) {
              cellLines.push('')
            }
            else{
              // generate this element's content
              try{
                myoptions.indent =  getIndentPrefix(cellChild)
              }
              catch(e){
              }
              // use puretext in code block
              if (pureTextPat.test(directiveName)){
                /* disabled, because code been escaped though pureText is true
                myoptions.pureText =  true            
                myoptions.exclusive = {url:true,bold:true,sub:true} 
                generateElementTextOnly(namespace,cellChild,cellLines, attachements,myoptions)
                */
                cellChild.getText().split('\n').forEach(function(line){
                  cellLines.push(line)
                })
    
              }
              else{
                // for note, caution,... do nothing but reset
                myoptions.pureText =  false
                myoptions.exclusive = {}
                generateElementTextOnly(namespace,cellChild,cellLines, attachements,myoptions)
              }
    
            }
          }
    
          // deal with images
          var imgPat = /^\\ \|IMG\d+\|\\ $/
          mergeInlineMarkup(cellLines,imgPat)
    
          // deal with footnotes
          var pat = /^\\ \[\#F\d+\]_\\ $/
          mergeInlineMarkup(cellLines,pat)
    
          var cellLines2 = []
          cellLines.forEach(function(line){
            line.split('\r').forEach(function(l){
              cellLines2.push(l);
            })
          })
          rowdata.push(cellLines2)  
        }
    
        // if the 2nd row does not contains arguments
        // put an empty line to signle the content starts
        if (i==0){
          if (rowdata[0]) tableData.push(rowdata[0].join('\n'))
          continue
        }
        else if (!contentStarted){
          if (rowdata[0][0].trim().indexOf(':') != 0){
            // put an empty line to signle the content starts
            if (tableData[tableData.length-1]) tableData.push('')
            contentStarted = true
          }
        }
        // suppose there is 1 column only
        // add indent 4 spaces
        rowdata[0].forEach(function(cellLine){
          tableData.push('    '+cellLine)
        })
        // if contentStarted, seperate content rows with an empty line
        if (contentStarted && i<maxRows-1 && tableData[tableData.length-1]) tableData.push('')
      }
    
      // generating starts
      lines2append.push('') // to seperate from previous content
      tableData.forEach(function(line){
        lines2append.push(line)
      })
      return true
    }
    
    function generateListItem(namespace, ele, lines, attachements, options){
      var files = attachements.files
      var footnotes = attachements.footnotes
      /*
       *
       * files: (array or null), if null, then skip image (ex. list item in table cell)
       */
      var type = ele.getGlyphType()
      var prefix = ((type == DocumentApp.GlyphType.BULLET) || (type == DocumentApp.GlyphType.HOLLOW_BULLET) || (type == DocumentApp.GlyphType.SQUARE_BULLET)) ?  '* ' : '#. '
      var indent = options.indent;
    
      // figure if we have to append an extra empty line
      // 1. if the previous sibling is also a list item of the same type, not append
      // 2. if this is first item but within a tablecell, not append
      // otherwise, do append
      var prevSibling = ele.getPreviousSibling()
      var parentIsContainer = ele.getParent().getType()==DocumentApp.ElementType.TABLE_CELL ? true : false
      var isLeadningItem = prevSibling ? (prevSibling.getType()==DocumentApp.ElementType.LIST_ITEM ? (prevSibling.getGlyphType()==ele.getGlyphType() ? false : true) : true) : (parentIsContainer ? false : true)
    
      //insert leading empty line for leading item
      if (isLeadningItem && lines[lines.length-1] != '') lines.push('')
    
      // generate item content
      var cellLines = []
      var myoptions = options
      myoptions.indent = '' //indentation is handled in this function 
      myoptions.lineWidth = 0 //don't split line by width for list item
      var numChildren = ele.getNumChildren()
      for (var k=0;k<numChildren;k++){
        var childEle = ele.getChild(k)
        generateElementTextOnly(namespace,childEle,cellLines, attachements,myoptions)
      }
    
      // deal with images
      var imgPat = /^\\ \|IMG\d+\|\\ $/
      mergeInlineMarkup(cellLines,imgPat)
    
      // deal with footnotes
      var pat = /^\\ \[\#F\d+\]_\\ $/
      mergeInlineMarkup(cellLines,pat)
    
      if (lines[lines.length-1]) lines.push('')
    
      cellLines.forEach(function(line){
        lines.push(indent+prefix+line)
      })
      return true
    }
    
    function generateListItemInHTML(namespace, ele, lines, attachements, options){
      var files = attachements.files
      var footnotes = attachements.footnotes
      /*
       *
       * files: (array or null), if null, then skip image (ex. list item in table cell)
       */
      var type = ele.getGlyphType()
    
      if ((!ele.getPreviousSibling())||(ele.getPreviousSibling().getType() != DocumentApp.ElementType.LIST_ITEM)){
        var numberic = !((type == DocumentApp.GlyphType.BULLET) || (type == DocumentApp.GlyphType.HOLLOW_BULLET) || (type == DocumentApp.GlyphType.SQUARE_BULLET))
        // readthedocs std_theme_css set these properties to "none", so we have to restore it
        var style=['list-style:'+(numberic ? 'decimal':'disc'),'list-style-image:inherit','padding:0px 40px','margin:initial']
        lines.push(numberic ? '<ol style="'+style.join(';')+'">' : '<ul style="'+style.join(';')+'">')
      }
    
      // generate item content
      var cellLines = []
      var numChildren = ele.getNumChildren()
      var myoptions = options
      var style=['list-style:inherit','list-style-image:inherit']
      cellLines.push('<li style="'+style.join(';')+'">')
      for (var k=0;k<numChildren;k++){
        var childEle = ele.getChild(k)
        generateElementInHTML(namespace,childEle,cellLines, attachements,myoptions)
      }
      cellLines.push('</li>')
      cellLines.forEach(function(line){
        lines.push(line)
      })
      if ((!ele.getNextSibling()) || (ele.getNextSibling().getType() != DocumentApp.ElementType.LIST_ITEM)){
        var numberic = !((type == DocumentApp.GlyphType.BULLET) || (type == DocumentApp.GlyphType.HOLLOW_BULLET) || (type == DocumentApp.GlyphType.SQUARE_BULLET))
        lines.push(numberic ? '</ol>' : '</ul>')
      }
      return true
    }
    /*
    function generateInlineImage(namespace, ele,lines,files,options){
      //ref: http://docutils.sourceforge.net/docs/ref/rst/directives.html#image
      lines.push(imageBag.put(namespace,files,ele))  
      return true
    }
    */
    function generateImageMarkup(folderName,fileItem,lines){
    
      lines.push('.. |IMG'+fileItem.sno+'| image:: '+folderName+(folderName ? '/' : '')+fileItem.name)
      lines.push('   :height: '+fileItem.height+' px')
      lines.push('   :width: '+fileItem.width+' px')  
      // figure the alignment in parent paragraph
    
      /*
    
      temporary disable, becasue reST parser has problem to parse :align:
    
      var parentParagraph = closestType(ele,[DocumentApp.ElementType.PARAGRAPH,DocumentApp.ElementType.LIST_ITEM,DocumentApp.ElementType.TABLE_CELL])
      if (parentParagraph){
        var attr = parentParagraph.getAttributes()  
        var hAlign; 
    
        switch (attr[DocumentApp.Attribute.HORIZONTAL_ALIGNMENT]){
          case DocumentApp.HorizontalAlignment.CENTER:
            hAlign = 'center'
            break
          case DocumentApp.HorizontalAlignment.RIGHT:
            hAlign = 'right'
            break
         }
         if (hAlign) lines.push('   :align: '+hAlign)
      }
      */
    
    
      var title = fileItem.title // ele.getAltTitle()
      if (title) lines.push('   :alt: '+title)
    
      var url = fileItem.url //ele.getLinkUrl()
      if (url) lines.push('   :target: '+url)
    
      lines.push('')
    
    }
    function getMD5(text){
      var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, text);
      var result = '';
      digest.forEach(function(byte){
        result += byte.toString(16)//String.fromCharCode(byte)
      })
      return result.replace(/-/g,'').toLowerCase();
    }
    function generateTOC(namespace, rootEle, lines, attachements, options){
        var numChildren = rootEle.getNumChildren()
        if (numChildren==0) return
    
        // iterate over children
        var childEle = rootEle.getChild(0)
        var myoptions = {
          indent : options.indent,
          level : options.level + 1,
          lineWidth:options.lineWidth,
          bodyWidth:options.bodyWidth,
          lineByLine:options.lineByLine,
          inlineStyle:options.inlineStyle,
          htmlTable:options.htmlTable,
        }
        if (lines[lines.length-1]) lines.push('')
        while(childEle){
          var indent = getIndentPrefix(childEle,18)
          var text = childEle.getText().replace(/\s+\d+$/,'')
          var digest = 'h'+getMD5(text) //return value of getMD5() might starts with '-', so prefix with 'H'
          lines.push('| '+indent+'`'+text+' <#'+digest+'>`_')
          //lines.push('')
          childEle = childEle.getNextSibling()
        }
        lines.push('')
        return true
    }
    
    function generateElementInHTML(namespace, rootEle, lines, attachements, options){
      /* 
       * for generating a table cell by navigation all children
       *
       * options = {
       *       exclusive:{
       *           //passed to markupInlineStyles() 
       *       }
       * }
       *
       * return (boolean) complete
      */
    
      addInternalLink(attachements.bookmarkElements,rootEle,lines)
    
      var files = attachements.files
      var footnotes = attachements.footnotes
    
      var complete = false
      var suffixLines = []
      switch(rootEle.getType()){
          case DocumentApp.ElementType.PARAGRAPH:
            // a new paragraph should has an empty line to seperate it from others
            var style=[]
            var attr = rootEle.getAttributes()
            if (attr[DocumentApp.Attribute.BACKGROUND_COLOR]) style.push('background-color:'+attr[DocumentApp.Attribute.BACKGROUND_COLOR])
            if (attr[DocumentApp.Attribute.FOREGROUND_COLOR]) style.push('color:'+attr[DocumentApp.Attribute.FOREGROUND_COLOR])
            if (attr[DocumentApp.Attribute.FONT_SIZE]) style.push('font-size:'+attr[DocumentApp.Attribute.FONT_SIZE]+'px')
            if (attr[DocumentApp.Attribute.FONT_FAMILY]) style.push('font-family:'+attr[DocumentApp.Attribute.FONT_FAMILY])
            if (rootEle.getSpacingAfter()) style.push('margin-bottom:'+rootEle.getSpacingAfter())
            if (rootEle.getSpacingBefore()) style.push('margin-top:'+rootEle.getSpacingBefore())
            //style.push('line-space:'+Math.round(attr[DocumentApp.Attribute.FONT_SIZE]*rootEle.getLineSpacing())+'px')
            lines.push('<p'+(style.length ? ' style="'+style.join(';')+'"' : '')+'>')
            suffixLines.push('</p>')
            break
          case DocumentApp.ElementType.LIST_ITEM:
            generateListItemInHTML(namespace, rootEle, lines, attachements, options)
            complete = true
            break
          case DocumentApp.ElementType.INLINE_IMAGE:
            lines.push(imageBag.putHTML(namespace,files,rootEle))
            complete = true;
            break
          case DocumentApp.ElementType.FOOTNOTE:
          case DocumentApp.ElementType.INLINE_DRAWING:
          case DocumentApp.ElementType.EQUATION:
          case DocumentApp.ElementType.EQUATION_FUNCTION:
          case DocumentApp.ElementType.HEADER_SECTION:
          case DocumentApp.ElementType.FOOTER_SECTION:
            lines.push('')
            lines.push('<!-- Skipped, unable to convert element of type '+rootEle.getType()+' -->')
            lines.push('')
            complete = true
            break
          default:
            var style=[]
            var attr = rootEle.getAttributes()
            if (attr[DocumentApp.Attribute.BACKGROUND_COLOR]) style.push('background-color:'+attr[DocumentApp.Attribute.BACKGROUND_COLOR])
            if (attr[DocumentApp.Attribute.FOREGROUND_COLOR]) style.push('color:'+attr[DocumentApp.Attribute.FOREGROUND_COLOR])
            if (attr[DocumentApp.Attribute.FONT_SIZE]) style.push('font-size:'+attr[DocumentApp.Attribute.FONT_SIZE]+'px')
            if (attr[DocumentApp.Attribute.FONT_FAMILY]) style.push('font-family:'+attr[DocumentApp.Attribute.FONT_FAMILY])
            if (style.length){
              lines.push('<span '+(style.length ? ' style="'+style.join(';')+'"' : '')+'>')
              suffixLines.push('</span>')
            }
            var eleLines = markupInlineStyles(rootEle,attachements,{exclusive:options.exclusive,html:true}).split('\n')
            eleLines.forEach(function(line,i){
              lines.push(line.replace(/[\r\n]/g,'<br/>'))
            })
            complete = true
      }  
      if (complete){
      }
      else{
        // do a depth-first walk on rootEle's child
        var numChildren = rootEle.getNumChildren ? rootEle.getNumChildren() : 0
        if (numChildren==0) return
        // iterate over children
        var childEle = rootEle.getChild(0)
        var myoptions = options
        while(childEle){
          try{
            //unless the child element has its own indent
            myoptions.indent = getIndentPrefix(childEle)
          }
          catch(e){
            // this type of element has no indent property (ex, Text)
          }
          generateElementInHTML(namespace,childEle, lines, attachements, myoptions)
          childEle = childEle.getNextSibling()
        }
      }
      suffixLines.reverse()
      suffixLines.forEach(function(line){
        lines.push(line)
      })
      return true
    }
    
    function generateElementTextOnly(namespace, rootEle, lines, attachements, options){
      /* 
       * for generating a table cell by navigation all children
       *
       * options = {
       *       indent : '',
       *       level: 0,
       *       // if true, do not generate link, neither bold and italic markups 
       *       // used for generating cells in header row
       *       pureText: (boolean false )
       *       // if true, no empty line between paragraphs
       *       lineByLine: (boolean false ),
       *       exclusive:{
       *           //passed to markupInlineStyles() 
       *       }
       * }
       *
       * return (boolean) complete
      */
    
      addInternalLink(attachements.bookmarkElements,rootEle,lines)
    
      var files = attachements.files
      var footnotes = attachements.footnotes
    
      var lineWidth = options.lineWidth
    
      if (options.pureText){
        var exclusive  = options.exclusive  ? options.exclusive  : {bold:true,sub:true,url:true}
        var headerLines = markupInlineStyles(rootEle,attachements,{lineWidth:lineWidth,exclusive:exclusive,inlineStyle:options.inlineStyle}).split('\n')
        headerLines.forEach(function(line){
          lines.push(options.indent+line)
        })
        return true
      }
    
      var complete = false
      switch(rootEle.getType()){
          case DocumentApp.ElementType.PARAGRAPH:
            // a new paragraph should has an empty line to seperate it from others        
            if ((!options.lineByLine) && lines[lines.length-1]) lines.push('')
            break
          case DocumentApp.ElementType.LIST_ITEM:
            options.indent = getIndentPrefix(rootEle)
            generateListItem(namespace, rootEle, lines, attachements, options)
            complete = true
            break
          case DocumentApp.ElementType.FOOTNOTE:
            footnotes.push(rootEle)
            lines.push('\\ [#F'+footnotes.length+']_\\ ')
            complete = true
            break
          case DocumentApp.ElementType.INLINE_IMAGE:
            lines.push(imageBag.put(namespace,files,rootEle))
            complete = true;
            break
          case DocumentApp.ElementType.INLINE_DRAWING:
          case DocumentApp.ElementType.EQUATION:
          case DocumentApp.ElementType.EQUATION_FUNCTION:
          case DocumentApp.ElementType.HEADER_SECTION:
          case DocumentApp.ElementType.FOOTER_SECTION:
            lines.push('')
            lines.push('.. Skipped, unable to convert element of type '+rootEle.getType())
            lines.push('')
            complete = true
            break
          default:
            var eleLines = markupInlineStyles(rootEle,attachements,{lineWidth:lineWidth,exclusive:options.exclusive,inlineStyle:options.inlineStyle}).split('\n')
            eleLines.forEach(function(line,i){
              lines.push(options.indent+line)
            })
            complete = true
      }  
      if (complete) return true
      // do a depth-first walk on rootEle's child
      var numChildren = rootEle.getNumChildren ? rootEle.getNumChildren() : 0
      if (numChildren==0) return
      // iterate over children
      var childEle = rootEle.getChild(0)
      var myoptions = {
        //use same indent
        indent : options.indent,
        level : options.level + 1,
        lineWidth:lineWidth,
        bodyWidth:options.bodyWidth,
        lineByLine:options.lineByLine,
        inlineStyle:options.inlineStyle,
        pureText:options.pureText,
        exclusive:options.exclusive,
        htmlTable:options.htmlTable
      }
      while(childEle){
        try{
          //unless the child element has its own indent
          myoptions.indent = getIndentPrefix(childEle)
        }
        catch(e){
          // this type of element has no indent property (ex, Text)
        }
        generateElementTextOnly(namespace,childEle, lines, attachements, myoptions)
        childEle = childEle.getNextSibling()
      }
      return true
    }
    
    function generateElement(namespace, rootEle, lines, attachements, options){
      var files = attachements.files
      var footnotes = attachements.footnotes
    
      var complete = false
      switch (rootEle.getType()){
        case DocumentApp.ElementType.BODY_SECTION:
          //pass
          break
        case DocumentApp.ElementType.TEXT:
          options.indent = getIndentPrefix(rootEle)
          generateElementTextOnly(namespace, rootEle, lines, attachements, options)
          complete = true
          break;
        case DocumentApp.ElementType.PARAGRAPH:
          addInternalLink(attachements.bookmarkElements,rootEle,lines)
          // ensure has an empty line in front of a paragraph
          if (lines[lines.length-1]) lines.push('')
    
          complete = generateHeadingParagraph(namespace, rootEle, lines, attachements, options)
    
          if (!complete){
            // find the last non-empty line, to see if it is ended with ::
            // if it is, increase the indent level for next paragraph
            if (rootEle.getNumChildren()==1 && rootEle.getChild(0).getType()==DocumentApp.ElementType.HORIZONTAL_RULE){
              if (lines[lines.length-1]) lines.push('')//ensure there is an empty line
              lines.push('--------')
              lines.push('')
            }
            else{
              options.indent = getIndentPrefix(rootEle)
              generateElementTextOnly(namespace, rootEle, lines, attachements, options)
            }
            complete = true
          }
    
          break     
        case DocumentApp.ElementType.TABLE:
          // check if this is 
          var pat = /^\s*?[ⓘϕ]\s*|^\.\.\s/
          var cell0content = rootEle.getRow(0).getCell(0).getText().trim()
          if (pat.test(cell0content)){
            generateDirectiveTable(namespace, rootEle, lines, attachements, options)
            complete = true
          }
          else{
            complete = generateTable(namespace, rootEle, lines, attachements, options)
          }
          break
        case DocumentApp.ElementType.LIST_ITEM:
          options.indent = getIndentPrefix(rootEle)
          complete = generateListItem(namespace, rootEle, lines, attachements, options)
          break
        case DocumentApp.ElementType.INLINE_DRAWING:
          lines.push('')
          lines.push('.. Skipped, drawing is not supported, please use image instead')
          lines.push('')
          complete = true
          break
        case DocumentApp.ElementType.INLINE_IMAGE:
          lines.push(imageBag.put(namespace,files,rootEle))
          complete = true;
          break
        case DocumentApp.ElementType.HORIZONTAL_RULE:
          if (lines[lines.length-1]) lines.push('')//ensure there is an empty line
          lines.push('--------')
          lines.push('')
          complete = true
          break
        case DocumentApp.ElementType.FOOTNOTE:
          footnotes.push(rootEle)
          lines.push('\\ [#f'+footnotes.length+']_\\ ')
          complete = true
          break
        case DocumentApp.ElementType.TABLE_OF_CONTENTS:
          generateTOC(namespace, rootEle, lines, attachements, options)
          complete = true
          break
        default:
          lines.push('')
          lines.push('.. Skipped: unable to convert element of type '+rootEle.getType())
          lines.push('')
          complete = true
          return
      }
      if (!complete) {
        var numChildren = rootEle.getNumChildren()
        if (numChildren==0) return
    
        // iterate over children
        var childEle = rootEle.getChild(0)
        var myoptions = {
          indent : options.indent,
          level : options.level + 1,
          lineWidth:options.lineWidth,
          bodyWidth:options.bodyWidth,
          lineByLine:options.lineByLine,
          inlineStyle:options.inlineStyle,
          pureText:options.pureText,
          exclusive:options.exclusive,
          htmlTable:options.htmlTable
        }
        while(childEle){
          try{
            //unless the child element has its own indent
            myoptions.indent = getIndentPrefix(childEle)
          }
          catch(e){
            // this type of element has no indent property (ex, Text)
            //use same indent
          }
          generateElement(namespace, childEle, lines, attachements, myoptions)
          childEle = childEle.getNextSibling()
        }
      }
    }
    
    // interface for sidebar.html
    function generateReST(inBase64,includeImages,imgInBase64,wholeDocument) {
      /*
       * 
       */
      var doc = DocumentApp.getActiveDocument()
      var name = doc.getName()
      /*
       * docPreferences.htmlTable, if true, generate table with html tags
       */
      var docPreferences = PropertiesService.getUserProperties().getProperty('docPreferences')
      var preferences = docPreferences ? JSON.parse(docPreferences)[doc.getId()]||{} : {}
    
      //figure the lineWidth
      var charWidth = 6
      var body = doc.getBody()
      var bodyWidth = body.getPageWidth() - body.getMarginLeft() - body.getMarginRight()
      var lineWidth = Math.floor(bodyWidth/charWidth )
    
      // find a safe namespace to prevent confliction in Github
      // not to create folder and file with the same name
      // namespace is used for create image name
      var namespace = name
    
      /*
       * get better namespace
       */
    
      // use binding name for namespace if it is available
      var githubBindings = PropertiesService.getUserProperties().getProperty('githubBindings')
      if (githubBindings) githubBindings = JSON.parse(githubBindings)
      var githubBinding = githubBindings ? githubBindings[DocumentApp.getActiveDocument().getId()] : null
      var bindingName;
      if (githubBinding){
        bindingName = githubBinding.name
        namespace = bindingName
      }
    
      // omit file extension from namespace (last .ext was remove, so a.b.c ==> a.b  )
      var namespaceParts = namespace.split('.')
      if (namespaceParts.length>1){
        namespaceParts.pop()
        namespace = namespaceParts.join('.')
      }
      /* image will not in imageFolder
      else if (bindingName==namespace){
        namespace += '_files'
      }
      */
      // remove illigal characters from namespace
      namespace = namespace.replace(/[\s\.\*]/g,'_')
    
      //bookmarks
      var bookmarks = doc.getBookmarks()
      var bookmarkElements = []
      bookmarks.forEach(function(bookmark){
        bookmarkElements.push([bookmark.getPosition().getElement(), bookmark.getId()])
      })
    
      /*
       * figure the target element to be generated (partial or full document)
       */
    
      var getTopExportableEle = function(ele,forSelection){
        /*
         * return the top table, or element which contains the list, or the top paragraph
         */
        var j = 0 // prevent infinit loop
        var parents = []
        while (ele && j < 20){
          parents.push(ele)
          ele = ele.getParent()
          j += 1
        }
        parents.reverse()
        var firstFav = [],secondFav
        parents.some(function(ele,i){
          if (ele.getType()==DocumentApp.ElementType.TABLE){
            firstFav.push(ele)
            return true
          }
          else if (ele.getType()==DocumentApp.ElementType.TABLE_OF_CONTENTS){
            firstFav.push(ele)
            return true
          }
          else if (ele.getType()==DocumentApp.ElementType.LIST_ITEM){
            if (forSelection){
               firstFav.push(ele)
               return true
            }
            else{
              // for cursor 
              // search for all list items 
              /*
              var item = ele
              while (1){
                if (! item.getPreviousSibling()) break
                if (item.getPreviousSibling().getType() != DocumentApp.ElementType.LIST_ITEM) break
                item = item.getPreviousSibling()
              }
              while (1){
                firstFav.push(item)
                item = item.getNextSibling()
                if (!item) break
                else if (item.getType() != DocumentApp.ElementType.LIST_ITEM) break
              }
              return true
              */
            }
    
          }      
          else if ((!secondFav) && ele.getType()==DocumentApp.ElementType.PARAGRAPH){
            secondFav = ele
          }
        })
        return firstFav.length ? firstFav : ( forSelection ? [secondFav] : [])
      }
      var body = doc.getBody()
    
      var rootElements = []  
      var addToRootElements = function(ele){
        // ele might be duplicated because selected elements share same parent
        var existed = false
        /* disabled, seem check last is good enough
        rootElements.some(function(e){
          // this is not effecient, but there is no API to get element ID
          if (e.getText()==ele.getText()) {existed = true ;return true}
        })
        */
        if (rootElements.length && rootElements[rootElements.length-1].getText()==ele.getText()) existed = true
        if (!existed) rootElements.push(ele)
      }
      var tableGenerated = false
      if (!wholeDocument){
        var selection = getSelection(false)
        if (selection){
          selection.getSelectedElements().forEach(function(item){
            var eles = getTopExportableEle(item.getElement(),true)
            eles.forEach(function(ele){
              if (typeof(ele) == 'undefined')  return
              addToRootElements(ele)
            })
          })
        }
        else{
          var cursor = DocumentApp.getActiveDocument().getCursor();
          if (cursor) {
            var eles = getTopExportableEle(cursor.getElement(),false)
            eles.forEach(function(ele){
              addToRootElements(ele)
              if (ele.getType()==DocumentApp.ElementType.TABLE) tableGenerated = true
            })
          }
          else{
            // EOF selected
            //DocumentApp.getUi().alert('No selection and cursor not found')
          }
        }
      }
    
      if (rootElements.length==0){
        wholeDocument = true
        rootElements.push(body)
      }
    
      /*
       * start to generate all exportable elements
       */
      var lines = []
      var attachements = {
        links:[],
        files:[],
        styles:[],//bold,sub,sup,italic
        footnotes:[],
        replacements:[],
        bookmarkElements:bookmarkElements
      }
    
      var options = {
          indent : '',
          level: 0,
          lineWidth:lineWidth,
          bodyWidth:bodyWidth,
          inlineStyle:wholeDocument ? false : true,
          htmlTable: preferences.htmlTable
      }
    
      rootElements.forEach(function(rootEle){
        //Logger.log(rootEle.getType())
        generateElement(namespace,rootEle,lines,attachements,options)
      })
    
    
      /*
       * add an empty line to separate the content from markups of links, images, footnotes.
       */
      lines.push('')
    
      // put flag to signal content chunk has rendered
      // so the inline style knows not to break lines for long line (in conversion.html)
      lines.push('.. bottom of content')
      lines.push('')
    
      //generate styles
      if (attachements.styles.length){
        lines.push('')
    
        attachements.styles.forEach(function(item,i){
          lines.push('.. '+item[0]+' replace:: '+item[1])
          lines.push('')
        })
    
      }
    
      //generate replacements
      if (attachements.replacements.length){
        lines.push('')
    
        attachements.replacements.forEach(function(lineChunks,i){
          lineChunks.forEach(function(line){
            lines.push(line)
          })
        })
    
      }
    
    
      //generate links  
      if (attachements.links.length){
        lines.push('')
    
        attachements.links.forEach(function(item,i){
          //item[0] is the url been normalized
          var p = item[0].indexOf('://')
          var blank = (p>0 && p < 10) ? ' target="_blank"' : ''
          lines.push('.. |LINK'+(i+1)+'| raw:: html')
          lines.push('')
          lines.push('    <a href="'+item[0]+'"'+blank+'>'+item[1]+'</a>')
          lines.push('')
        })
    
        lines.push('')    
      }
    
      // generate footnotes
      if (attachements.footnotes.length){
        // connect markup to original lines
    
        var pat = /^\\ \[\#f\d+\]_\\ $/i
        mergeInlineMarkup(lines,pat)
    
        // create footnote contents at the end
        lines.push('')
        lines.push('.. rubric:: Footnotes')
        lines.push('')
        attachements.footnotes.forEach(function(footnote,i){
             var section = footnote.getFootnoteContents()
    
             // var content = escapeText(section.getChild(0).getText()).replace(/[\r\n]/g,';')
             // allow hyper links in footnotes
             var myattachments = {links:[],styles:[]}
             var content = markupInlineStyles(section.getChild(0),myattachments,{inlineStyle:true})
    
             lines.push('.. [#f'+(i+1)+'] '+(content||' (empty)'))
        })
        lines.push('')
      }
    
      // generate image replacement
      // imageFolder is used for putting image files
      var imageFolder = 'static'
      var imgFiles = []
      if (attachements.files.length){
        // deal with images
    
        // merge the outest isolation image
        var imgPat = /^\\ \|IMG\d+\|\\ $/
        mergeInlineMarkup(lines,imgPat)
    
        var basename = namespace.split('/').pop()
    
        attachements.files.forEach(function(fileItem,i){
          generateImageMarkup(imageFolder,fileItem,lines)
        })
        imageBag.full(basename,imgFiles,includeImages,imgInBase64)
      }
    
      // replace footnote markup in table cell
    
      var content = lines.join('\n')
    
      var resp = {
        name: name,
        namespace:namespace,
        content:(inBase64 ? Utilities.base64Encode(content,Utilities.Charset.UTF_8) : content),
        files:imgFiles,
        imageFolder:imageFolder,
        namespace:namespace,
        wholeDocument:wholeDocument,
        tableGenerated:tableGenerated
      }
      return resp
    }
    
    

|

.. _h374e1e52778544f7c42346a1b597143:

properties.gs
*************


.. code-block:: python
    :linenos:

    /* persistent data */
    function getUserProperties(){
      //Caution: user properties always key = JSON encoded object
      // before 2017/1/4
      //   var keys = ['githubBindings','githubCredentials']
      // after 2017/1/4
      //   var keys = ['githubBindings','credentialsArray']
      //   resetProperties()
      // after 2018/1/23
      //   githubBindings no more used, will use document property to store githubBinding
      //   because githubBindings too big to save in user property
      //
      var properties = PropertiesService.getUserProperties().getProperties()
      var doc = DocumentApp.getActiveDocument()
      var obj = {
        doc:{
          id: doc.getId(),
          name: doc.getName()
        }
      }
      for (var key in properties){
        obj[key] = JSON.parse(properties[key]) 
      }
      //setup initial value
    
      /* handle githubBinding starts */
      var githubBinding
      if (obj['githubBindings']) {
        githubBinding = obj['githubBindings'][obj.doc.id]
        delete obj['githubBindings']
      }
    
      docProp = PropertiesService.getDocumentProperties()
      var key = 'githubBinding'
      if (githubBinding){
        // save githubBinding from user-property to doc-property
        docProp.setProperty(key,JSON.stringify(githubBinding))
        setUserProperty('githubBindings',null,obj.doc.id)
      }
      else{
        docProp = PropertiesService.getDocumentProperties()
        githubBinding = docProp.getProperty(key)
        if (githubBinding) {
          githubBinding = JSON.parse(githubBinding)
        }
        else {
          githubBinding = {}
        }
      }
    
      obj[key] = githubBinding
      /* handle githubBinding ended */
    
      // convert single credential to multiple credentials
      if (obj['credentialsArray']){
        //already upgraded
      }
      else{
        obj['credentialsArray'] = []
        if (obj['githubCredentials']) {
          if (obj['githubCredentials'].username){
            obj['credentialsArray'].push(obj['githubCredentials'])
          }
        }
      }
      /*
      else{
        // productive mode
        obj['credentialsArray'] = []
        if (obj['githubCredentials']) {
          if (obj['githubCredentials'].username){
            obj['credentialsArray'].push(obj['githubCredentials'])
          }
          setUserProperty('githubCredentials',null)
        }
        setCredentialsArray(obj['credentialsArray'])
      }
      */
      var docPreferences
      if (obj['docPreferences']){
        docPreferences = obj['docPreferences'][obj.doc.id]
        delete obj['docPreferences']
      }
      if (!docPreferences){
        docPreferences = {
          htmlTable: false
        }
      }
      obj.doc.preferences = docPreferences
    
      return obj
    }
    function dumpUserProperty(){
       var userProp = PropertiesService.getUserProperties()
       Logger.log(userProp.getProperties())
    }
    function setUserProperty(key,obj,subkey){
       var userProp = PropertiesService.getUserProperties()
       var deleteAllOthers = false
       if (subkey){
         var value = userProp.getProperty(key)
         value = value ? JSON.parse(value) : null;
         // case of bindings
         if (obj){
           if (!value) value = {}
           value[subkey] = obj
         }
         else{
           if (value) delete value[subkey]
         }
         userProp.setProperty(key,JSON.stringify(value))
       }
       else{
         // case of credential
         if (obj){
           userProp.setProperty(key, JSON.stringify(obj))
         }
         else{
           userProp.deleteProperty(key)
         }
       }
    }
    function setGithubCredentials(githubCredentials){
      if (githubCredentials && githubCredentials.username){
        setUserProperty('githubCredentials',githubCredentials)
      }
      else {
        setUserProperty('githubCredentials',null)
      }
    }
    function setCredentialsArray(credentialsArray){
      setUserProperty('credentialsArray',credentialsArray)
    }
    function setDocPreferences(docPreferences){
      return setUserProperty('docPreferences',docPreferences,DocumentApp.getActiveDocument().getId())
    }
    function resetGithubBinding(){
      var docId = DocumentApp.getActiveDocument().getId()
      setUserProperty('docPreferences',null,docId)
      setUserProperty('githubBindings',null,docId)
      var key = 'githubBinding'
      PropertiesService.getDocumentProperties().deleteProperty(key)
      return true
    }
    function resetProperties(){
      PropertiesService.getDocumentProperties().deleteAllProperties()
      PropertiesService.getUserProperties().deleteAllProperties()
    }
    function setGithubBinding(githubBinding){
      var obj = githubBinding
      var key = 'githubBinding'
      var docProp = PropertiesService.getDocumentProperties()
      docProp.setProperty(key, JSON.stringify(obj))
    }
    
    
    /* obsoleted
    function setGithubBinding(githubBinding){
      return setUserProperty('githubBindings',githubBinding,DocumentApp.getActiveDocument().getId())
    }
    function testSetProperties(){
      var githubBinding = {
        name:"DocStructure.rst",
        path:"docs",
        repo:"GGeditor",
        repoUrl:"https://api.github.com/repos/iapyeh/GGeditor"  
      }
      setGithubBinding(githubBinding)
    }
    */
    

|

.. _h603b59267213c503a2f3b493e401276:

explicitMarkup.html
*******************


.. code-block:: python
    :linenos:

    <!DOCTYPE html>
    <html>
      <head>
        <base target="_top">
      <style>
    #markup-table{
      border:solid 1px gray;
      height:200px;
      width:100%;
    }
    #markup-table th{
    
    }
    #markup-table th.token{
      width:24px;
      vertical-align:middle;
    }
    #markup-name{
      width:100px;
    }
    #markup-arguments{
      width:100px;
    }
    #markup-name input{
      width:90%;
      border:solid 1px rgba(0,0,0,0.1);
      padding:5px;
    }
    #markup-arguments input{
      width:90%;
      border:solid 1px rgba(0,0,0,0.1);
      padding:5px;
    }
    #options, #contents{
      padding-left:35px;
    }
    #options textarea, #contents textarea{
      width:98%;
      height:100%;
      border:solid 1px rgba(0,0,0,0.1);
    }
      </style>
      </head>
      <body>
        <table id="markup-table">
          <tr style="height:30px;">
            <th class="token">..</th>
            <td id="markup-name"><input placeholder="name"></td>
            <th class="token">::</th>
            <td id="markup-arguments"><input placeholder="arguments"></td>
          </tr>
          <tr><td id="options" colspan="4"><textarea placeholder="options"></textarea></td></tr>
          <tr><td id="contents" colspan="4"><textarea placeholder="content"></textarea></td></tr>
        </table>
      </body>
    </html>
    
    
    

|

.. _h6c122521437f5b59572c1c7b248025d:

github.html
***********


.. code-block:: python
    :linenos:

    <!DOCTYPE html>
    <html>
      <head>
        <base target="_top">
        <link rel="stylesheet" href="https://ssl.gstatic.com/docs/script/css/add-ons.css">
    <style>
    .tab {
      position:relative;
      left:0;
      top:0;
      display:none;
      padding:5px 2px 0px 10px;
    }
    .tab.active{
      display:block;
    }
    .tab-title{
      border:solid 1px #c0c0c0;
      display:inline-block;
      position:relative;
      padding:5px 8px;
      border-bottom:none;
      -webkit-border-top-left-radius: 2px;
      -webkit-border-top-right-radius: 2px;
      -moz-border-radius-topleft: 2px;
      -moz-border-radius-topright: 2px;
      border-top-left-radius: 2px;
      border-top-right-radius: 2px;
      cursor:pointer;
      text-align:center;
      width:24%;
      font-size:0.95em;
      white-space: nowrap;
      overflow-x: hidden;
      text-overflow: ellipsis;
      margin-bottom:-5px;
    }
    .tab-title.active,.tab-title.active:hover{
      top:1px;
      background-color:white;
      -webkit-box-shadow: none;
      -moz-box-shadow:    none;
      box-shadow:         none;
    }
    .tab-title:hover{
      background-color:#f0f0f0;  
      -webkit-box-shadow: 0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      -moz-box-shadow:    0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      box-shadow:         0px 0px 1px 0px rgba(50, 50, 50, 0.25);
    }
    .tab-title-bar {
      border-bottom:solid 1px #c0c0c0;
      margin-bottom:10px;
      padding:0px 10px;
    }
    .tab > .block{
    }
    .tab > .block:first-child{
        margin-top:12px  !important;
    }
    .tab > .block > label:first-child {
      margin-bottom:5px;
      display:block;
    }
    
    button.small{
        min-width:35px;
        height:25px;
        margin-left:3px;
        margin-top:3px;
    }
    select option{
      text-align:left;
    }
    
    /* start of help */
    .help:hover{
      cursor:help;
    }
    select.help:hover,button.help:hover{
      outline:none;
      box-shadow:none;
      cursor:inherit;
    }
    .helpframe{
      display:none;
      border-radius: 5px; 
      -moz-border-radius: 5px; 
      -webkit-border-radius: 5px; 
      border: 1px solid #c0c0c0;
      color:black;
      padding:5px;
      width:95%;
      margin-top:2px;
      overflow: hidden;
    }
    .helpframe{ /* temporary disable */
      border:none;
      width:100%;
      padding:0px;
    }
    .helpframetitle{
      margin:-5px -5px 2px -5px;
      padding:2px 0px;
      background-color:#f0f0f0;
      text-align:right;
      display:none;/* temporary disable */
    }
    .helpframetitle .closebtn{
      color:#000000;
      margin-right:4px;
      padding: 0px 2px;
      font-weight:bold;
      text-decoration:none;
    }
    .helpframetitle .closebtn:hover{
      color:#f0f0f0;
      background-color:#0c0c0c;
      margin-right:4px;
      padding: 1px 3px;
      font-weight:bold;
      text-decoration:none;
    }
    .helppos{
      display:none;
      position:absolute;
      z-index:99;
      background-color:black;
      color:white;
      padding:5px;
      margin-right:10px;
      overflow: hidden;
      opacity:0;
    }
    .helpcontent{
      overflow:hidden;
    }
    #helps{
      position:absolute;
      left:-500px;
      top:-10000px;
      padding:5px;
      visibility:hidden;
      width:80%;
      overflow:hidden;
    }
    #helps table td,.helpcontent table td{
      padding:2px 10px;
    }
    #helps table th,.helpcontent table th{
      vertical-align:top;
      padding:2px;
      border-bottom:solid 1px #ebebeb;
    }
    #helps p,.helpcontent p{
      margin-top:1px;
    }
    /* end of help */
    
    /* make option be easier to click */
    option{
      padding:2px;
      border-bottom:solid 1px white;
    }
    option.option-label+option{
      border-bottom:solid 1px #d0d0d0;
    }
    option.option-label+option:last-child{
      border-bottom:solid 1px white;
    }
    .flat-btn-box{
      height:90px;
      width:255px;
    }
    .flat-btn{
      outline:#c0c0c0 solid thin;
      display:inline-block;
      float:left;
      width:25px;
      height:25px;
      line-height:25px;
      margin:2px;
      cursor:pointer;
      text-align:center;
    }
    .flat-btn-zoomin{
      display:none;
      position:absolute;
      border:solid 3px #4d90fe;
      height:45px;
      width:60px;
      z-index:99;
      background-color:white;
      font-size:1.75em;
      text-align:center;
      line-height:45px;
    }
    /*loading */
    #loading{
      display:none;
      position:absolute;
      height:100px;
      min-height: 100px;
      top:40%;
      left:5%;
      right:5%;
      width:60%;
      margin:auto;
      text-align:center;
      background-color:rgba(255,255,255,0.85);
      z-index:99;
    }
    #loading div{
      padding: 0px 0px 30px 0px;
      background-image: url('data:image/gif;base64,R0lGODlhEAALAPQAAP///wAAANra2tDQ0Orq6gYGBgAAAC4uLoKCgmBgYLq6uiIiIkpKSoqKimRkZL6+viYmJgQEBE5OTubm5tjY2PT09Dg4ONzc3PLy8ra2tqCgoMrKyu7u7gAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCwAAACwAAAAAEAALAAAFLSAgjmRpnqSgCuLKAq5AEIM4zDVw03ve27ifDgfkEYe04kDIDC5zrtYKRa2WQgAh+QQJCwAAACwAAAAAEAALAAAFJGBhGAVgnqhpHIeRvsDawqns0qeN5+y967tYLyicBYE7EYkYAgAh+QQJCwAAACwAAAAAEAALAAAFNiAgjothLOOIJAkiGgxjpGKiKMkbz7SN6zIawJcDwIK9W/HISxGBzdHTuBNOmcJVCyoUlk7CEAAh+QQJCwAAACwAAAAAEAALAAAFNSAgjqQIRRFUAo3jNGIkSdHqPI8Tz3V55zuaDacDyIQ+YrBH+hWPzJFzOQQaeavWi7oqnVIhACH5BAkLAAAALAAAAAAQAAsAAAUyICCOZGme1rJY5kRRk7hI0mJSVUXJtF3iOl7tltsBZsNfUegjAY3I5sgFY55KqdX1GgIAIfkECQsAAAAsAAAAABAACwAABTcgII5kaZ4kcV2EqLJipmnZhWGXaOOitm2aXQ4g7P2Ct2ER4AMul00kj5g0Al8tADY2y6C+4FIIACH5BAkLAAAALAAAAAAQAAsAAAUvICCOZGme5ERRk6iy7qpyHCVStA3gNa/7txxwlwv2isSacYUc+l4tADQGQ1mvpBAAIfkECQsAAAAsAAAAABAACwAABS8gII5kaZ7kRFGTqLLuqnIcJVK0DeA1r/u3HHCXC/aKxJpxhRz6Xi0ANAZDWa+kEAA7AAAAAAAAAAAA');
      background-repeat:no-repeat;
      background-position:center;
    }
    #loading-text{
      font-size:16px;
    }
    
    .modal-dialog{
      display:none;
      position:absolute;
      top:40%;
      left:5%;
      right:5%;
      width:70%;
      margin:auto;
      min-height:200px;
      z-index:99;
      box-shadow: 0 4px 16px rgba(0,0,0,.2);
      background: #fff;
      background-clip: padding-box;
      border: 1px solid #acacac;
      border: 1px solid rgba(0,0,0,.333);
      outline: 0;
      position: absolute;
      color: #000;
      padding: 15px 21px;
      font-size:14px;
    }
    .modal-dialog button{
      -webkit-border-radius: 2px;
      -moz-border-radius: 2px;
      border-radius: 2px;
      background-color: #f5f5f5;
      background-image: -webkit-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -moz-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -ms-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -o-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: linear-gradient(top,#f5f5f5,#f1f1f1);
      border: 1px solid #dcdcdc;
      border: 1px solid rgba(0,0,0,0.1);
      color: #333;
      cursor: default;
      font-family: inherit;
      font-size: 11px;
      font-weight: bold;
      height: 29px;
      line-height: 27px;
      margin:0;
      min-width: 72px;
      outline: 0;
      padding: 0 8px;  
    }
    .modal-dialog .title{
      font-weight:bold;
    }
    .modal-dialog .buttons{
        position: absolute;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
    }
    .modal-dialog button+button{
      margin-left:20px;
    }
    .modal-dialog .x{
      font-weight: bold;
      text-align: right;
      margin-top: -5px;
      margin-right: -5px;
      color: #a0a0a0;
      cursor:pointer;
    }
    /* end of loading */
    .gray {
      background-color:rgba(230, 230, 230, 0.1);
    }
    
    #github-repository-list{
      font-size: 14px;
      overflow-x:auto;
      overflow-y:hidden;
      height:100%;
      width:1000px;
    }
    #github-repository-list div{
      overflow:hidden;
      float:left;
      height:430px;
      margin-left: 2px;
      border:none;
    }
    #github-repository-list div:hover select{
      outline:rgba(0,0,255,0.4) thin solid;
    }
    #github-repository-list div select{
      width: 200px;
      height:100%;
    }
    #github-repository-list div select option{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
      padding:5px;
      color:blue;
      border-bottom:solid 1px rgba(0,0,0,0.1);
    }
    #github-url{
        background-color: #ffc;
        border: solid 1px rgba(0,0,0,0.2);
        width: 90%;
        margin-left: 0;
        padding: 10px 5px;
    }
    </style>
      </head>
      <body>
    <div class="sidebar" style="padding:0px 0px;margin:-8px;height:100%">
      <div class="tab-title-bar" style="display:none">
        <div class="tab-title" tab="t1" onclick="setActiveTab('t1')"><span class="i18n">Github</span></div>
        <div class="tab-title" tab="t2" onclick="setActiveTab('t2')"><span class="i18n">Repositories</span></div>
      </div>
      <div class="github tab active" tab="t1">
        <div class="block form-group"  id="github-has-binding">
          <label for="github-url"><span class="i18n">Binding File</span>:</label>  
          <div id="github-url"></div>
        </div>
        <div class="block form-group">
          <label for="github-credentials"><span class="i18n">Account</span>:</label>  
          <div id="github-account"></div>
          <div id="github-account-once" style="display:none">
            <div class="block form-group">
              <label class="help" helpname="pip" helptype="hover" for="github-username"><span class="i18n">Username</span>:</label>
              <input class="gray" type="text" id="github-username" value="">
            </div>
            <div class="block form-group">
              <label class="help" helpname="pip" helptype="hover" for="github-password"><span class="i18n">Password</span>:</label>      
              <input class="gray" id="github-password" type="password" value="">
            </div>
            <!--
            <div class="block form-group">
              <input type="checkbox" id="github-remember" onclick="githubRemember()">
              <label class="help" helpname="pip" helptype="hover" for="github-remember"><span class="i18n">Remember Github Credentials</span></label> 
            </div>
            -->
          </div>
        </div>
        <div class="block form-group">
          <input type="checkbox" id="commit-include-images" checked>
          <label class="help" helpname="cii" helptype="hover" for="commit-include-images"><span class="i18n">Commit images</span></label> 
        </div>
        <div class="block form-group">
          <p id="html-table-1" style="display:none">
          Tables are converted to HTML &lt;TABLE&gt; ( <a href="#" class="open-settiongs">Settings</a> )
          </p>
          <p id="html-table-0" style="display:none">
          Tables are converted to reStructuredText table markups. ( <a href="#" class="open-settiongs">Settings</a> )
          </p>
        </div>
        <div class="block form-group">
          <button onclick="githubLogin()" id="github-login-btn" class="blue" style="display:none">Login</button>
          <button onclick="githubCommit()" id="github-commit-btn" class="blue" style="display:none;margin-left:0;">Commit</button>
          <button onclick="githubResetPath()" id="github-resetPath-btn" style="display:none">Reset Binding</button>
          <!--
          <button onclick="githubResetCredentials()" id="github-resetCredentials-btn" style="display:none">Reset Account</button>
          -->
        </div>
      </div>
      <div class="github-repository tab" tab="t2">
        <div id="github-repository-list"></div>
      </div>
      <!--end of tab-->
    </div>
    <div class="masterhelpframe helpframe">
      <div class="helpframetitle">
        <a class="closebtn" onclick="closeHelp(this)">×</a>
      </div>
      <div class="helpcontent"></div>
    </div>
    
    <div id="loading" class="modal-dialog">
      <div>
        <h1><label class="i18n" id="loading-text"></label></h1>
      </div>
    </div>
    <div id="dialog" class="modal-dialog">
      <div style="width:100%">
        <div class="x">x</div>
        <p class="title"></p>
        <p class="content"></p>
        <div class="buttons">
          <button class="yes i18n blue">Delete</button><button class="cancel i18n">Cancel</button>
        </div>
      </div>
    </div>
    <span class="helppos" id="helppostmpl" style="display:none"></span>
    <span id="helppostmplpt" style="display:none;position:absolute">▲</span>
    <div style="display:none">
      <div id="helps">
        <div name="cii">If checked, images in document will be committed too</div>
      </div>
    </div>
    <script language="javascript">
    document.addEventListener( "DOMContentLoaded", initialization , false );
    
    var userCredentials;
    function Credentials(username,password){
      this.username = username
      this.password = password
      this.key = username.toUpperCase()
      if (this.password) this.encrypt()
    }
    Credentials.prototype = {
      encrypt:function(){
        this.encrypted = JSON.stringify(sjcl.encrypt(this.key,this.password))
      },
      decrypt:function(encrypted){
        try{
          this.password = sjcl.decrypt(this.key,JSON.parse(encrypted))
          this.encrypted = encrypted
          return true
        }
        catch(e){
          this.password = ''
          this.encrypted = ''
          return false
        }
      }
    }
    
    function initialization(){
      enableHelp()
    
      /* assign initial values from persistent data */  
      loading(true)
      google.script.run.withSuccessHandler(function(response){
        loading(false)
        properties = response
        renderGithubButtons()
      }).withFailureHandler(stopLoading).getUserProperties();
    
      var showSettingsDialog = function(evt){
        evt.preventDefault()
        loading(true)
        google.script.run.withSuccessHandler(function(){
          stopLoading()
          google.script.host.close()
        }).withFailureHandler(stopLoading).showSettingsDialog();
      }
    
      document.querySelectorAll('a.open-settiongs').forEach(function(a){
        a.onclick = showSettingsDialog
      })
    }
    
    
    /*
     * lib functions starts below
     * 
     */
    var serverValues={locale:'en'};
    function localI18n(s){
      return s
    }
    function setActiveTab(name){
      var tabs = document.querySelectorAll('.tab')
      for (var i=0;i<tabs.length;i++){
        if (tabs[i].getAttribute('tab')==name){tabs[i].className+=' active'}
        else {      
          tabs[i].className = tabs[i].className.replace(/ active/,'');
        }
      }
      var titles = document.querySelectorAll('.tab-title')
      for (var i=0;i<titles.length;i++){
        if (titles[i].getAttribute('tab')==name){titles[i].className='tab-title active'}
        else titles[i].className='tab-title';
      }
    }
    
    function getTimestamp(){
      var now = new Date()
      return now.getFullYear()+'-'+(now.getMonth()+1)+'-'+now.getDate()+' '+now.getHours()+':'+now.getMinutes()+':'+now.getSeconds()
    }
    function getViewportSize(){
      var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
      var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
      return {width:w,height:h}
    }
    function moveElementToViewportCenter(ele) {
        var size = getViewportSize()
        var rect = ele.getBoundingClientRect()
        ele.style.top =  Math.round(size.height/2 - rect.height/2)+'px'
        ele.style.marginLeft = Math.round(size.width/2  - rect.width/2)+'px'
    }
    
    var loadingCount=0;
    function loading(yes,label){
      var title = localI18n('Please be waiting...');
    
      if (yes && typeof(yes)=='string') title = yes
    
      if ((loadingCount<0 && !yes) || (loadingCount>0 && yes)) {
        if (title) {
          document.getElementById('loading-text').innerHTML = title;
        }
        loadingCount += yes ? 1 : -1;
        return;
      }
      loadingCount += yes ? 1 : -1;
      var loadingDiv = document.getElementById('loading')
      if (loadingCount==1){
        // start loading
        loadingDiv.style.display='flex';
        document.getElementById('loading-text').innerHTML = title;
        document.querySelector('.sidebar').style.opacity = 0.5;
        moveElementToViewportCenter(loadingDiv)
      }
      else{
        // stop loading
        loadingDiv.style.display='none';
        document.querySelector('.sidebar').style.opacity = 1;
      }
    }
    function stopLoading(label){loading(false,label)}
    function setLoadingTitle(title){document.getElementById('loading-text').innerHTML = title;}
    
    function myConfirm(title,callback){
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'  
      dialog.style.display='block';
      //dialog.style.top = (window.pageYOffset+150)+'px'
      document.querySelector('.sidebar').style.opacity = 0.5;
      moveElementToViewportCenter(dialog)
      var cleanup = function(yes){
        callback(yes)
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.cancel').onclick = null;
        document.querySelector('.sidebar').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        dialog.style.top = '0px';
        document.querySelector('.sidebar').style.opacity = 1; 
      }
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.cancel').onclick = function(){
        cleanup(false);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      setTimeout(function(){
        document.querySelector('.sidebar').onclick = function(){
          cleanup(false);
        } 
      },100)
    }
    function myAlert(title,callback){
      if (!callback) callback = function(){}
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'
      dialog.style.display='block';
      //dialog.style.top = (window.pageYOffset+150)+'px'
      document.querySelector('.sidebar').style.opacity = 0.5;
      var yesHTML = dialog.querySelector('.yes').innerHTML
      var cleanup = function(yes){
        callback(yes)
        document.querySelector('.sidebar').onclick = null
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.cancel').style.display = ''
        dialog.querySelector('.yes').innerHTML = yesHTML
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        document.querySelector('.sidebar').style.opacity = 1; 
      }
      dialog.querySelector('.cancel').style.display = 'none'
      dialog.querySelector('.yes').innerHTML = 'OK'
    
      moveElementToViewportCenter(dialog)
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      // click outside dialog also close the dialog
      setTimeout(function(){
        document.querySelector('.sidebar').onclick = function(){
          cleanup(false);
        } 
      },100)
    }
    
    function myPrompt(title,options,callback){
        /*
         * options = {
         *     value*:(string) value of the input element
         *     placeholder*:(string) default null
         *     content*:(string) default "<input style="width:100%;height:40px;font-size:1.5em">"
         *     button:*(dict){ok:{className:<class name>},cancel:{className:<class name>}}, default null
         * }
         */
        var dialog = document.getElementById('dialog')
        dialog.querySelector('.title').innerHTML = title;
        dialog.querySelector('.content').innerHTML = (options.content || '<input style="width:100%;height:40px;font-size:1.5em">')
        dialog.querySelector('.content').style = 'block'
        dialog.querySelector('.buttons').style = 'block'
        var input = dialog.querySelector('.content input')
        if (options.placeholder) input.setAttribute('placeholder',options.placeholder)
        if (options.value) input.value = options.value
        var buttons = [
            '<button class="ok'+((options.button && options.button.ok && options.button.ok.className) ? ' '+options.button.ok.className : '' )+'">OK</button>',
            '<button class="cancel'+((options.button && options.button.cancel && options.button.cancel.className) ? ' '+options.button.cancel.className : '' )+'">Cancel</button>',
            ]
        dialog.querySelector('.buttons').innerHTML = buttons.join('')
    
        var cleanup = function(value){
          document.querySelector('.sidebar').style.opacity = 1; 
          document.querySelector('.sidebar').onclick = null
          dialog.querySelector('.cancel').onclick = null;
          dialog.querySelector('.x').onclick = null;
          dialog.querySelector('.ok').onclick = null;
          dialog.querySelector('.buttons').innerHTML = ''
          dialog.querySelector('.content').innerHTML = ''
          dialog.querySelector('.title').innerHTML = ''
          dialog.style.display='none';
          callback(value)
        }
        setTimeout(function(){
          dialog.querySelector('.x').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.cancel').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.ok').onclick = function(){
              var text = dialog.querySelector('input').value || (options.defaultText || '')
              cleanup(text)
          }
        },500)
        document.querySelector('.sidebar').style.opacity = 0.5;     
        dialog.style.display = 'block'
        dialog.style.height = '200px'
        moveElementToViewportCenter(dialog)
        // click outside dialog also close the dialog
        setTimeout(function(){
          document.querySelector('.sidebar').onclick = function(){
            cleanup(false);
          } 
        },100)
        return {dom:dialog,callback:callback}
    }
    
    /* start of help system */
    function enableHelp(){
      var helps =  document.querySelectorAll('.help');
      var timer = 0,delay = 1000,hoverDelay=1000;
      for (var i=0,l=helps.length;i<l;i++){
        var hoverType = helps[i].getAttribute('helptype')=='hover';
        helps[i].onmouseover = function(evt){
          var target = evt.currentTarget
          var helpname = target.getAttribute('hoverhelpname') || target.getAttribute('helpname')
          // check if the same help is openning
          if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) {
            return;
          }
          if (timer>0) clearTimeout(timer);
          timer = setTimeout(function(){
            timer = 0;
            showHelp(helpname,target.getAttribute('helpCloseByBtn'),target.getAttribute('helptype'))
          },(hoverType ? hoverDelay : delay))
        }
        if (hoverType){
          helps[i].onmouseout = function(evt){
            if (timer){
              //give up to show it
              clearTimeout(timer);timer = 0;
            }
            else{
              closeHoverHelp();
            }
          }
        }
        else{
          // cancel the help showup
          helps[i].onmouseout = function(evt){
            if (timer){
              clearTimeout(timer);timer = 0;
            }
          }
        }
      }
    }
    
    function getOffset( el ) {
        var _x = 0;
        var _y = 0;
        while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
            _x += el.offsetLeft //- el.scrollLeft;
            _y += el.offsetTop //- el.scrollTop;
            el = el.offsetParent;
        }
        return { top: _y, left: _x };
    }
    function showHelp(helpname,helpCloseByBtn,helpType){
    
      /* simply deal with hover help */
      if (helpType=='hover'){
          var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
          var tmpl = document.getElementById('helppostmpl')
          var c = document.querySelector('#helps div[name="'+helpname+'"]');
          // make it visible
          var sidebarRect = document.querySelector('.sidebar').getBoundingClientRect()
          var sidebarWidth = sidebarRect.right - sidebarRect.left;
          tmpl.style.display='inline-block';
          tmpl.style.position = 'absolute';
          tmpl.style.zIndex = 99;
          var target = document.querySelector('.help[hoverhelpname="'+helpname+'"][helptype="hover"]');
          if (!target) target = document.querySelector('.help[helpname="'+helpname+'"][helptype="hover"]');
          var targetRect = target.getBoundingClientRect()
          var targetHeight = targetRect.bottom - targetRect.top;
          var targetWidth = targetRect.right - targetRect.left;
          var rect = getOffset(target)
          tmpl.style.top = (rect.top + targetHeight+4)+'px'
          tmpl.style.opacity = 0;
          tmpl.innerHTML= c.innerHTML;
          tmpl.style.maxWidth = Math.floor(sidebarWidth * 0.8)+'px'
          var tmplRect = tmpl.getBoundingClientRect()
          var tmplWidth = tmplRect.right - tmplRect.left
          var p0 = Math.floor(sidebarWidth * 0.1);
          var p1 = Math.floor(sidebarWidth * 0.9);
          var tmplpt = document.getElementById('helppostmplpt')
          tmplpt.style.top = (parseInt(tmpl.style.top)-10)+'px';
          if (rect.left < p0){
            tmpl.style.left = rect.left+'px'
            tmplpt.style.left = tmpl.style.left;
          }
          else if (rect.left+targetWidth > p1) {
            tmpl.style.left = Math.floor((rect.left+targetWidth - tmplWidth))+'px'
            tmplpt.style.left = Math.floor(parseInt(tmpl.style.left)+tmplWidth-18)+'px';
          }
          else {
            tmpl.style.left = Math.max(0,Math.floor(rect.left+targetWidth/2-tmplWidth/2))+'px'
            tmplpt.style.left = Math.max(0,Math.floor(parseInt(tmpl.style.left)+tmplWidth/2-6))+'px'
          }
          tmpl.setAttribute('active',1);
          setTimeout(function(){
            //starts animation
            tmpl.style.opacity=1;
            tmplpt.style.display='';
          },1)
        return;
      }
    
      /* need to check again for some help is triggered manually */
      if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) return;//already opened
      /* one help only, unless the existing help is a modal help */
      closeHelp()
      // create a new helpframe  
      /* prepare for animation */
      // clone the masterhelpframe  
      var helpframe = document.querySelector('.masterhelpframe.helpframe').cloneNode(true);
      helpframe.className = 'helpframe';
    
      helpframe.style.display = 'block';
      helpframe.setAttribute('helpname',helpname)
      var trigger = function(){    
        //var helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpname = this._helpname; 
        if (helpCloseByBtn) helpframe.setAttribute('modal',1)
        helpframe.querySelector('.closebtn').setAttribute('helpname',helpname)
        var cele = helpframe.querySelector('.helpcontent')
        /* find the insert position */
        var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
        helppos.parentNode.insertBefore(helpframe, helppos.nextSibling);
        /* find the help content to insert */
        var c = document.querySelector('#helps div[name="'+helpname+'"]');
        /* insert the help content */
        cele.appendChild(c);//move it
        /* starts the animation to show up*/
        var titleheight = helpframe.querySelector('.helpframetitle').clientHeight;
        /* make the helpframe visible, delay to wait the DOM been refreshed */
        setTimeout(function(){
          // scroll to make it visible
          var y = getOffset( helpframe ).top; 
          var offset = y-window.scrollY;
          if (offset<0 || offset > window.innerHeight)  window.scrollTo(0,Math.max(0,y-50));      
    
          //trigger event
          var e = document.createEvent('Event');
          e.initEvent('help-open-'+helpname,false,true);
          document.dispatchEvent(e);
    
        },100);
      }
      setTimeout(function(){trigger.apply({_helpname:helpname})},1)
    }
    
    function closeHoverHelp(){
      /* find the insert position */
      var helppos = document.querySelector('.helppos[active]');
      if (helppos===null) return;
      helppos.innerHTML='';
      // make it invisible
      helppos.style.display='none';
      helppos.style.opacity=0;
      helppos.removeAttribute('active');
      var tmplpt = document.getElementById('helppostmplpt')
      tmplpt.style.display='none';
    }
    function closeHelp(btn){
      /* release the body click */
      document.body.onclick = null;
    
      var helpname = null,helpframe=null;
      if (btn) {
        helpname = btn.getAttribute('helpname');
        helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpframe.removeAttribute('modal')//enforce to close by btn
        //fire event if closed by button
        var e = document.createEvent('Event');
        e.initEvent('help-close-'+helpname,false,true);
        document.dispatchEvent(e);
      }
      else {
        helpframe = document.querySelector('.helpframe[helpname]');
        if (!helpframe) return true;//no helpframe is showing    
        helpname = helpframe.getAttribute('helpname');
      }
      if (helpframe.getAttribute('modal')) return false
      var cele = helpframe.querySelector('.helpcontent')
      if (cele.firstChild != null){
        /*cele.removeChild(cele.firstChild);*/
        //move back to helps
        document.getElementById('helps').appendChild(cele.firstChild);    
      }
      helpframe.style.display = 'none';
      helpframe.parentNode.removeChild(helpframe);
      return true;
    }
    /* end of help system */
    
    
    /* 
     github related implementation
     */
    function renderGithubButtons(){
      var githubBinding = properties.githubBinding //properties.githubBindings[properties.doc.id]
      //githubCredentials = properties.githubCredentials
    
      if (githubBinding.name){
          // store a local copy for handy
          //properties.githubBinding = githubBinding
          document.getElementById('github-has-binding').style.display = ''      
          document.getElementById('github-url').innerHTML = githubBinding.repo + '/' + githubBinding.path + ( githubBinding.path ? '/' : '') + githubBinding.name
          document.getElementById('github-login-btn').style.display = 'none'
          document.getElementById('github-commit-btn').style.display = ''
          document.getElementById('github-resetPath-btn').style.display = ''
          document.getElementById('github-username').value = githubBinding.username || ''
          if (properties.doc.preferences.htmlTable){
            document.getElementById('html-table-0').style.display = 'none'
            document.getElementById('html-table-1').style.display = ''
          }
          else{
            document.getElementById('html-table-0').style.display = ''
            document.getElementById('html-table-1').style.display = 'none'
          }
      }
      else{
          document.getElementById('github-has-binding').style.display = 'none'      
          document.getElementById('github-url').innerHTML = ''
          document.getElementById('github-login-btn').style.display = ''
          document.getElementById('github-commit-btn').style.display = 'none'
          document.getElementById('github-resetPath-btn').style.display = 'none'
          document.getElementById('github-username').value = ''
      }
      var credentialsArray = properties.credentialsArray
      var options = ['<select>']
      var username =  githubBinding ? githubBinding.username : ''
      credentialsArray.forEach(function(item,i){
        var select='';
        if (username && item.username==username){
          //githubCredentials = item
          select = ' selected'
        }
        else if (i==0){
          select = ' selected'
        }
        options.push('<option value="'+item.username+'"'+select+'>'+item.username+'</option>')
      })
      options.push('<option value="-once-">Manual Input</option>')
      options.push('</select>')
      document.getElementById('github-account').innerHTML = options.join('')
      var setAccount = function (selEle){
          var username = selEle.options[selEle.selectedIndex].value
          if (username=='-once-'){
            document.getElementById('github-account').style.display = 'none'
            document.getElementById('github-account-once').style.display = 'block'
            userCredentials = null
          }
          else{
            userCredentials = new Credentials(username,'')
            properties.credentialsArray.some(function(item){
              if (item.username==username){
                if (!userCredentials.decrypt(item.password)){
                  userCredentials = null
                  myAlert('Invalid credentials, please reset it')
                }
                return true
              }
            })
          }
      }
      document.querySelector('#github-account select').onchange = function(evt){
        setAccount(evt.currentTarget)
      }
      setAccount(document.querySelector('#github-account select'))
    }
    
    function githubLogin(){
      var afterLogin = function(success){
          //render a repository navigation interface for selecting the associated file
          if (success){ 
            setActiveTab('t2')
            gitHubController.renderRepositoryList()
          }
          else{
          }
      }
      if (gitHubController && gitHubController.hasLogin) {
        //has been committed, this is 2nd time to commit    
        afterLogin(true)
      }
      else{
        //sidebar.html just been loaded
        if (!gitHubController) gitHubController = new GitHubController()
        gitHubController.login(afterLogin)
      } 
    }
    /*
    function githubRemember(){
      // save to server
      if (document.getElementById('github-remember').checked){
          var username = document.getElementById('github-username').value
          var password = document.getElementById('github-password').value      
          userCredentials = new Credentials(username,password)
          properties.githubCredentials = {
            username:userCredentials.username,
            password:userCredentials.encrypted
          }
      }  
      else{
        properties.githubCredentials = {}
      }
    
      loading(true)
      google.script.run.withSuccessHandler(function(){
        stopLoading()
      }).withFailureHandler(function(err){
        stopLoading()
        myAlert(err)
      }).setGithubCredentials(properties.githubCredentials)      
    
    }
    function githubResetCredentials(){
      myConfirm('Reset Credentials?',function(yes){
        if (!yes) return
        userCredentials = new Credentials(githubCredentials.username,'')
        githubCredentials.password = ''
        document.getElementById('github-username').value = userCredentials.username
        document.getElementById('github-password').value = ''
        document.getElementById('github-remember').checked = false
        githubRemember()
        renderGithubButtons()
     })
    }
    */
    
    function githubResetPath(){
      myConfirm('Reset binding ?',function(yes){
        if (!yes) return
    
        document.getElementById('github-url').value = '' 
        document.getElementById('github-has-binding').style.display = 'none'
        document.getElementById('github-commit-btn').style.display = 'none'
    
        delete properties.githubBinding
        //delete properties.githubBindings[properties.doc.id]
        //delete properties.githubBinding
    
        loading(true)
        google.script.run.withSuccessHandler(function(){
          stopLoading()
          if (userCredentials && userCredentials.username && userCredentials.password){
            // do  auto login
            githubLogin()
          }
          else{
            document.getElementById('github-login-btn').style.display = ''
            document.getElementById('github-resetPath-btn').style.display = 'none'
          }
    
        }).withFailureHandler(function(err){
          stopLoading()
          myAlert(err)
        }).resetGithubBinding()
      })
    }
    
    /*
     * GitHubController related functions start
     */
    var attrRegExp = new RegExp('([\'"<>])','g') //escape attribute value in html tag
    var gitHubController;//global singleton
    
    function githubCommit(){
      var hasConnected = function(){
          if (properties.githubBinding){
            gitHubController.addByUrl(function(success){
              if (success) {
                // upgrade githubBindings if not manual input
                if (userCredentials && userCredentials.username && userCredentials.password){
                  if (!properties.githubBinding.username){
                    properties.githubBinding.username = userCredentials.username
                    google.script.run.setGithubBinding(properties.githubBinding)
                  }             
                }
                myAlert('Commit completed')
              }
              else {
                // maybe bad credentials
                console.log(gitHubController.lastError)
                //login failure
                if (gitHubController.lastError && gitHubController.lastError.message.indexOf('credentials')>=0){
                  if (userCredentials){
                    userCredentials = new Credentials(userCredentials.username,'')
                  }
                  else{
                    // githubCredentials.password = ''
                    document.getElementById('github-password').value = ''
                  }
                  renderGithubButtons()            
                }
              }
            })
          }
      }
      if (!gitHubController) {
        gitHubController = new GitHubController()
      }
      hasConnected()
    }
    
    function GitHubController(){
      this.username='';
      this.password='';
      this.octo;
      this.repositories = []
      this.renderingTree = [] // list of [tree]
      this.renderingStack = [] // content of item which is in the list of renderingTree
      this.defaultCommitMessage = 'Google Docs reST Editor'
      this.hasLogin = false
    }
    GitHubController.prototype = {
      setCredentials:function(){
        if (userCredentials && userCredentials.username && userCredentials.password){
          this.username = userCredentials.username
          this.password = userCredentials.password
        }    
        else{
          this.username = document.getElementById('github-username').value
          this.password = document.getElementById('github-password').value
        }
        return this.username.length && this.password.length
      },
      alertError:function(err){
        this.lastError = err
        try{
          myAlert(JSON.parse(err.message).message)
        }
        catch(e){
          myAlert(err.message)
        }
      },  
      login:function(callback){
        var self = this
        if (!this.setCredentials()){
          self.hasLogin = false
          myAlert('No credentials to login')
          return
        }
        this.octo = new Octokat({username:this.username,password:this.password})
        loading('Doing login')
        self.octo.user.repos.fetchAll(function(err,val){
          stopLoading()
          if (err) {
            self.octo = null
            self.hasLogin = false
    
            //login failure
            if (err.message.indexOf('credentials')>=0){
              if (userCredentials){
                userCredentials = null
              }
              else{
    
                document.getElementById('github-password').value = ''
              }
              renderGithubButtons()            
            }
    
            callback(false)
            self.alertError(err)
            return
          }
          // login success
          /* .fetch() returns an object val(has val.items), .fetchAll() returns an array val (actually, is items) */
          self.hasLogin = true
          self.repositories = val
          callback(true)
        })
      },
      renderRepositoryList:function(){
        var box = document.querySelector('#github-repository-list')
        var html = ['<div><select class="repository-options" multi size=5 onclick="gitHubController.naviRepository(this)">']
    
        this.repositories.forEach(function(item,idx){
          var title = item.name.replace(attrRegExp,'\\$1')
          html.push('<option title="'+title+'" value="'+idx+'">🀫 '+item.name+'</option>')
        })
        html.push('</select></div>')
        box.innerHTML = html.join('')
        box.style.width = (200)+'px'
      },
      naviRepository:function(selEle){
        if (selEle.options.selectedIndex==-1) return
        var idx = selEle.options[selEle.options.selectedIndex].value
        // remove existing tree options
        var box = document.querySelector('#github-repository-list')
        for (var i = 0;i<this.renderingStack.length;i++){
          var div = box.querySelector('select[stack-idx="'+i+'"]').parentNode
          div.parentNode.removeChild(div)
        }
        this.activeRepository =  this.repositories[parseInt(idx)]
    
        var self = this
        loading(true)
        this.activeRepository.commits.fetch().then(function(response){
          var last_commit = response.items[0]
          self.activeRepository.trees({sha:last_commit.sha}).fetch().then(function(response){
            self.renderingStack = [[self.activeRepository,response.tree]]
            self.renderTree(response.tree,idx)
            loading(false)
          })
        }).catch(function(err,val){
          console.log(err)
          stopLoading();
          if (err.message.indexOf('Repository')>=0 && err.message.indexOf('empty')>=0){
            self.renderingStack = [[self.activeRepository,[]]]
            self.renderTree([],idx)
          }      
          else{
            self.alertError(err)
          }
        })
        return
      },
      renderTree:function(treeArray,treeIdx){
        /*
         * treeArray: [treeItem]
         * treeIdx: the index of this node in its parent treeArray
         */
        var stack_idx = (this.renderingStack.length-1)
        var html = ['<select multi size="5" tree-idx="'+treeIdx+'" stack-idx="'+stack_idx+'" onclick="gitHubController.naviTree(this)">']
        html.push('<option value="_new_file_">New File</option>')
        var htmlUnsorted = [[],[]]
        treeArray.forEach(function(tree,idx){
          var title = tree.path.replace(attrRegExp,'\\$1')
          if (tree.type=='tree'){
            htmlUnsorted[0].push([tree.path.toLowerCase(),'<option title="'+title+'" value="'+idx+'">🗂 &nbsp;'+tree.path+'</option>'])
          }
          else{
            htmlUnsorted[1].push([tree.path.toLowerCase(),'<option title="'+title+'" value="'+idx+'">📄 &nbsp;'+tree.path+'</option>'])
          }
        })
        htmlUnsorted[0].sort(function(a,b){
          return a[0]>b[0] ? 1 : (a[0]<b[0] ? -1 : 0)
        })
        htmlUnsorted[1].sort(function(a,b){
          return a[0]>b[0] ? 1 : (a[0]<b[0] ? -1 : 0)
        })
        html = html.concat(htmlUnsorted[0]).concat(htmlUnsorted[1])
        html.push('</select>')
        var box = document.querySelector('#github-repository-list')
    
        box.style.width = (200+this.renderingStack.length*(200+4))+'px'
    
        // if user double-click on an item, this code block will prevent from two select block was generated
        var existingEle = box.querySelector('select[stack-idx="'+stack_idx+'"]')
        if (existingEle) existingEle.parentNode.removeChild(existingEle)
    
        var div = document.createElement('div')
        div.innerHTML = html.join('')
        box.appendChild(div)
        //
        //div.scrollIntoView()
        var rect = div.getBoundingClientRect()
        //console.log(rect)
        //console.log(box.getBoundingClientRect())
        if (stack_idx>1){
          document.querySelector('.sidebar').scrollLeft = 200 * stack_idx - 100
        }
        else{
          document.querySelector('.sidebar').scrollLeft =  0
        }
      },
      naviTree:function(selEle){
        if (selEle.options.selectedIndex==-1) return
        var stackIdx = selEle.getAttribute('stack-idx')
        var treeIdx = selEle.options[selEle.options.selectedIndex].value
        if (treeIdx=='_new_folder_'){
          return this.createNewFolder(stackIdx,parseInt(selEle.getAttribute('tree-idx')))
        }
        else if (treeIdx == '_new_file_'){
          return this.createNewFile(stackIdx,parseInt(selEle.getAttribute('tree-idx')))
        }
    
        stackIdx = parseInt(stackIdx)
        treeIdx = parseInt(treeIdx)
    
        //if user click on upper folder, remove other branch rendering
        if (stackIdx < this.renderingStack.length-1){
          var box = document.querySelector('#github-repository-list')
          for (var i = stackIdx+1;i<this.renderingStack.length;i++){
            var div = box.querySelector('select[stack-idx="'+i+'"]').parentNode
            div.parentNode.removeChild(div)
          }
          var howMany = this.renderingStack.length - stackIdx - 1
          this.renderingStack.splice(stackIdx+1, howMany)
        }
    
        var treeItem =  this.renderingStack[stackIdx][1][treeIdx]
        var self = this
        if (treeItem.type=='blob'){
          myPrompt('Commit to '+treeItem.path,{button:{ok:{className:'blue'}},defaultText:this.defaultCommitMessage,placeholder:'message of commit'},function(message){
            if (!message) return
            var paths = []
            self.renderingStack.forEach(function(stackItem,idx){
              if (idx==0) return //skip 1st repository
              else if (idx > stackIdx) return
              paths.push(stackItem[0].path)
            })
            var folderPath = paths.join('/')
            paths.push(treeItem.path)
            var path = paths.join('/')
            var githubBinding = {
                  'repoUrl':self.activeRepository.url,
                  'path':folderPath,
                  'name':treeItem.path,
                  'repo':self.activeRepository.name,
                  'username': gitHubController.username
             }
             //save a local copy
             properties.githubBinding = githubBinding
             //properties.githubBindings[properties.doc.id] = githubBinding
    
             loading(true)
             var save_binding_error = function(err){
               stopLoading()
               console.log('binding error:',err)
               console.log('githubBinding=',githubBinding)
             }
             google.script.run.withSuccessHandler(stopLoading).withFailureHandler(save_binding_error).setGithubBinding(githubBinding)
    
             self.commit(message,function(success){
                // update the buttons state
                renderGithubButtons() 
    
                // clean up the select options
                var box = document.querySelector('#github-repository-list')
                box.innerHTML = ''
                self.renderingStack = []
    
                if (success) myAlert('commit completed') 
                else {
                  // something wrong, but suppose self.commit has informed user
                  // so do nothing here.
                }
             })
          })
        }
        else if (treeItem.type=='tree'){
          loading(true)
          this.activeRepository.trees({sha:treeItem.sha}).fetch().then(function(response){
            self.renderingStack.push([treeItem,response.tree])
            self.renderTree(response.tree,treeIdx)
            loading(false)
          })
        }
        return
      },
      createNewFile:function(stackIdx,treeIdxInParent){
        var self = this
        var done = function(resp){
          stopLoading()
          var generatedResult = JSON.parse(resp)
    
          //figure the folder for the new file
          var paths = []
          self.renderingStack.forEach(function(stackItem,idx){
            if (idx==0) return //skip 1st repository
            else if (idx > stackIdx) return
            paths.push(stackItem[0].path)
          })
          var folderPath = paths.join('/')
    
          var defaultName = properties.doc.name
          if (!/\.(md|rst)$/.test(defaultName)) defaultName += '.rst'      
          myPrompt('New in '+folderPath+'/',{button:{ok:{className:'blue'}},placeholder:'.rst',value:defaultName},function(name){
            if (!name) return
    
            // ensure name is end with .rst
            if (name.substring(name.length-4).toUpperCase()=='.RST'){
              name = name.substr(0,name.length-4) + '.rst'
            }
            else{
              name += '.rst'
            }
    
            stackIdx = parseInt(stackIdx)
            var treeItem =  self.renderingStack[stackIdx][0]
    
            // check name existence
            //pending
    
            // check if we have path in the given name
            var foldersInName = name.split('/')
            if (foldersInName.length>1){
              name = foldersInName.pop().trim()
              foldersInName.forEach(function(n){
                if (n.trim()) paths.push(n.trim())
              })
              folderPath = paths.join('/')
            }
    
             //create the created path
             paths.push(name)
             var path = paths.join('/')
    
             var githubBinding = {
               'repoUrl':self.activeRepository.url,
               'path':folderPath,
               'name':name,
               'repo':self.activeRepository.name,
               'username':gitHubController.username
             }
    
             //save a local copy in browser
             properties.githubBinding = githubBinding
             //properties.githubBindings[properties.doc.id] = githubBinding
    
             // save github Binding info to server
             google.script.run.setGithubBinding(githubBinding)
    
    
             var finalCommit = function(){
               var message = 'add file '+name
               var config = {"message":message,"content":generatedResult.content,sha:treeItem.sha}
               loading('creating new file: '+name)
               self.activeRepository.contents(path).add(config).then(function(response){
                 stopLoading()
                 // miso
                 self.commit(message,function(success){
                    // update the buttons state
                    renderGithubButtons() 
    
                    // clean up the select options
                    var box = document.querySelector('#github-repository-list')
                    box.innerHTML = ''
                    self.renderingStack = []
    
                    if (success){
                      myAlert('commit completed') 
                    }
                    else {
                      // something wrong, but suppose self.commit has informed user
                      // so do nothing here.
                    }
                 })
               }).catch(function(err,val){
                 stopLoading()
                 self.alertError(err)
               })
             }
             if (foldersInName.length>1){
               //create folders in middle
               var checkFolder = function(idx,parentTreeItem){
                 if (idx==foldersInName.length-1) {
                   // reach the last one
                   stopLoading()
                   finalCommit()
                 }
                 else{
                   var foldername = foldersInName[idx]
                   var message = 'add folder '+foldername
                   var config = {"message":message,"content":'',sha:parentTreeItem.sha}
                   setLoadingTitle('checking '+foldername)
                   var lastIdx = (paths.length - (foldersInName.length+1)) + idx +1
                   var folderPath = ''
                   for (var x=0;x<lastIdx;x++){
                     folderPath += (x > 0 ? '/' : '') +paths[x]
                   }
                   self.activeRepository.contents(folderPath).fetch().then(function(response){
                      // this folder existed
                      checkFolder(idx+1,response)
                   }).catch(function(err,val){
                      var mesgObj = JSON.parse(err.message)
                      if (mesgObj.message.toLowerCase().indexOf('not found')>=0){
                         // this folder is not existed, lets create one
                         self.activeRepository.contents(folderPath+'/index.rst').add(config).then(function(response){               
                           setLoadingTitle('creating '+folderPath)
                           checkFolder(idx+1,response)
                         })
                      }
                      else{
                        // there is other error
                        stopLoading();
                        self.alertError(err)
                      }
                   })
                 }
               }
               loading(true)
               checkFolder(0,treeItem)
             }
             else{
               finalCommit()
             }
           })
         }
         loading(true)
         var inBase64 = true
         google.script.run.withSuccessHandler(done).withFailureHandler(function(err){
           console.log(['generating failure',err])
           stopLoading();
           self.alertError(err)
         }).generate(inBase64);      
      },  
      addByUrl:function(callback){
        /* 
         * update document content to given githubURL 
         */
        var self = this
        if (!this.setCredentials()){
          self.hasLogin = false
          myAlert('Please give credentials to commit')
          return
        }
        this.octo = new Octokat({username:this.username,password:this.password})
        var ts = getTimestamp()
        myPrompt('Message for Committing',{button:{ok:{className:'blue'}},defaultText:this.defaultCommitMessage+'@'+ts,placeholder:''},function(message){
            if (!message) return
            self.commit(message,function(success){
              callback(success)
            })
        })
      },
      commit:function(message, callback){
        /*
         * callback:function(success){}
         */
        var self = this
    
        var githubBinding = properties.githubBinding
        // check if user create new file with new folder, such as "docs/index.rst"
        // images have to upload to docs/static instead of static
        var imagePrefixFolder = githubBinding.imagePrefixFolder
        if (imagePrefixFolder) delete githubBinding.imagePrefixFolder
    
        var githubRepoUrl = githubBinding.repoUrl
    
        var doCommit = function(){
            var done = function(resp){
              stopLoading();
              generatedResult = JSON.parse(resp)
              var path = githubBinding.path+(githubBinding.path ? '/' : '')+githubBinding.name
              loading('Committing','Committing')
              self.activeRepository.contents(path).fetch().then(function(response){
                var config = {"message":message,"content":generatedResult.content,sha:response.sha} 
                response.add(config).then(function(response){
                    stopLoading('Committing');
                    var folderpath = githubBinding.path
                    var subfoldername = generatedResult.imageFolder
                    if (imagePrefixFolder){
                      folderpath += (folderpath ? '/' : '') +imagePrefixFolder
                    }
                    self.uploadFiles(generatedResult.namespace,folderpath,subfoldername,generatedResult.files,function(success){
                      callback(success)
    
                      myAlert('Commit completed',function(){
                        // clse the dialog
                        google.script.host.close()
                      })
                    })
                }).catch(function(err,val){
                    stopLoading('committing error on add()');
                    self.alertError(err)
                    callback(false)
                })
              }).catch(function(err,val){
                  stopLoading('committing error on contents()');
                  self.alertError(err)
                  callback(false)
              })
    
            } // end of done()  
            var inBase64 = true
            var includeImages = document.getElementById('commit-include-images').checked
            loading('Generating')
            google.script.run.withSuccessHandler(done).withFailureHandler(function(err){
                console.log(['generating failure',err])
                stopLoading();
                self.alertError('Sorry bug:'+err.message)
                callback(false)
            }).generate(inBase64,includeImages);    
        }    
        if (self.activeRepository) {
          doCommit()
        }
        else{
          loading(true)
          self.octo.fromUrl(githubRepoUrl).fetch().then(function(repo){
            stopLoading();
            self.activeRepository = repo
            doCommit()
          }).catch(function(err,val){
            stopLoading();
            self.alertError(err)
            callback(false)
          })
        }
      },
      uploadFiles:function(namespace,folderpath,subfoldername,files,callback){
        /*
         *
         * subfoldername: folder to put the image files
         *
         */
        if (!document.getElementById('commit-include-images').checked){
          callback(true)
          return
        }
    
        /* 
         * called by commit to help it to update images
         * callback:function(success){}
         */
        var sortByObjname = function (a,b){
          var f1,f2
          if (a.some){
            f1 = a[0]
            f2 = b[0]
          }
          else{
            f1 = a
            f2 = b
          }
          var name1 = parseInt(f1.name.match(/_(\d+)\.png/)[1])
          var name2 = parseInt(f2.name.match(/_(\d+)\.png/)[1])
          return name1 > name2 ? 1 : (name1 < name2 ? -1 : 0)
        }
    
        loading('Uploading files')
    
        var self = this
        this.activeRepository.contents(folderpath).fetch().then(function(treeItem){
          var subfolderItem = null
          treeItem.items.some(function(item){
            if (item.name == subfoldername){
              subfolderItem = item
              return true
            }
          })
          var ts = getTimestamp()
          var subfolderPath = folderpath+(folderpath ? '/' : '')+(subfolderItem ? subfolderItem.name : subfoldername )
          if (subfolderItem){
            self.activeRepository.contents(subfolderPath).fetch().then(function(treeItem){
              //do file maintenance
              var itemsToRemove = []
              var itemsToAdd = []
              var itemsToUpdate = []
              if (files.length==0){
                // remove all items
                treeItem.items.forEach(function(item){
                  // only remove item which starts with the same name with the file in question.
                  if (item.name.indexOf(namespace+'_')==0){
                    itemsToRemove.push(item)
                  }
                })
              }
              else{
                treeItem.items.forEach(function(item){
                  var updated = false
                  files.some(function(file){
                    if (file.name == item.name){
                       itemsToUpdate.push([item,file])
                       updated = true
                       return true
                    }
                  })
                  if (!updated){
                    if (item.name.indexOf(namespace+'_')==0){
                      itemsToRemove.push(item)
                    }
                  }
                })
                files.forEach(function(file){
                  var found = false
                  treeItem.items.forEach(function(item){
                    if (item.name==file.name){
                      found = true
                      return true
                    }
                  })
                  if (!found) itemsToAdd.push(file)
                })          
              }
    
              if (itemsToUpdate.length+itemsToRemove.length+itemsToAdd.length==0){
                //nothing to do
                callback(true)
                return
              }
    
              // do updating
              var removeItem = function (idx,complete_callback){
                if (idx >= itemsToRemove.length){
                  complete_callback(3)
                  return
                }
                var item = itemsToRemove[idx]
                setLoadingTitle('Removing '+item.name)
                var config = {"message":'remove '+item.name+'@'+ts,"sha":item.sha}
                self.activeRepository.contents(subfolderPath+'/'+item.name).remove(config).then(function(response){
                  //move to next update
                  removeItem(idx+1,complete_callback)
                }).catch(function(err,val){
                    var mesgObj = JSON.parse(err.message)
                    if (mesgObj.message.indexOf('refs/heads/master is at')==0){
                      setLoadingTitle('restart removing file')
                      self.uploadFiles(namespace,folderpath,subfoldername,files,callback)
                    }
                    else{
                      complete_callback(3,err)
                    }            
                })              
              }         
              var addItem = function (idx,complete_callback){
                if (idx >= itemsToAdd.length){
                  complete_callback(2)
                  return
                }
                var file = itemsToAdd[idx]
                if (file._done_) {
                  setLoadingTitle('skip adding '+file.name)
                  addItem(idx+1,complete_callback)
                  return
                }
                var config = {"message":'add '+file.name+'@'+ts,"content":file.content}
                setLoadingTitle('Adding '+file.name)
                self.activeRepository.contents(subfolderPath+'/'+file.name).add(config).then(function(response){
                  //move to next update
                  file._done_ = 1
                  addItem(idx+1,complete_callback)
                }).catch(function(err,val){
                    var mesgObj = JSON.parse(err.message)
                    if (mesgObj.message.indexOf('refs/heads/master is at')==0){
                      stopLoading()
                      self.uploadFiles(namespace,folderpath,subfoldername,files,callback)
                    }
                    else{
                      complete_callback(2,err)
                    }
                })            
              }          
              if (itemsToUpdate.length) itemsToUpdate.sort(sortByObjname)
              if (itemsToAdd.length) itemsToAdd.sort(sortByObjname)
              if (itemsToRemove.length) itemsToRemove.sort(sortByObjname)
    
              var updateItem = function(idx,complete_callback){
                if (idx >= itemsToUpdate.length){
                  complete_callback(1)
                  return
                }
                var item = itemsToUpdate[idx]
                var file = item[1]
                if (file._done_) {
                  setLoadingTitle('skip update '+file.name)
                  updateItem(idx+1,complete_callback)
                  return
                }
                var config = {"message":'update '+file.name+'@'+ts,"content":file.content,sha:item[0].sha}
                setLoadingTitle('Updating '+file.name)
                self.activeRepository.contents(subfolderPath+'/'+file.name).add(config).then(function(response){
                  //move to next update
                  file._done_ = 1
                  updateItem(idx+1,complete_callback)
                }).catch(function(err,val){
                    var mesgObj = JSON.parse(err.message)
                    if (mesgObj.message.indexOf('refs/heads/master is at')==0){
                      stopLoading()
                      self.uploadFiles(namespace,folderpath,subfoldername,files,callback)
                    }
                    else{
                      complete_callback(1,err)
                    }
                })  
              }
              var complete = function(flag,err){
                if (err){
                  setTimeout(function(){
                    self.alertError(err)
                  },1000)
                  stopLoading()
                  callback(false)
                }
                else if (flag==1){ // updating complete
                  addItem(0,complete)
                }
                else if (flag==2){ //adding complete
                  removeItem(0,complete)
                }
                else if (flag==3){ //removing complete
                  stopLoading()
                  callback(true)
                }
              }
              updateItem(0,complete)
            })
          }
          else{
            // folder does not existed, all files should be added
            itemsToAdd = files
            var complete = function(flag,err){
              if (err){
                 self.alertError(err)
              }
              stopLoading()
              callback((err ? false : true))
            }
            var addItem = function (idx,complete_callback){
                if (idx >= itemsToAdd.length){
                  complete_callback()
                  return
                }
                var file = itemsToAdd[idx]
                var config = {"message":'add '+file.name+'@'+ts,"content":file.content}
                self.activeRepository.contents(subfolderPath+'/'+file.name).add(config).then(function(response){
                  //move to next update
                  addItem(idx+1,complete_callback)
                }).catch(function(err,val){
                    complete_callback(1,err)
                })            
            }
            addItem(0,complete)
          }
        })
      }
    }
    </script>
    
    <script language="javascript">
    /*
     * https://github.com/philschatz/octokat.js/
     */
    
    (function webpackUniversalModuleDefinition(root, factory) {
    	if(typeof exports === 'object' && typeof module === 'object')
    		module.exports = factory();
    	else if(typeof define === 'function' && define.amd)
    		define([], factory);
    	else if(typeof exports === 'object')
    		exports["Octokat"] = factory();
    	else
    		root["Octokat"] = factory();
    })(this, function() {
    return /******/ (function(modules) { // webpackBootstrap
    /******/ 	// The module cache
    /******/ 	var installedModules = {};
    
    /******/ 	// The require function
    /******/ 	function __webpack_require__(moduleId) {
    
    /******/ 		// Check if module is in cache
    /******/ 		if(installedModules[moduleId])
    /******/ 			return installedModules[moduleId].exports;
    
    /******/ 		// Create a new module (and put it into the cache)
    /******/ 		var module = installedModules[moduleId] = {
    /******/ 			exports: {},
    /******/ 			id: moduleId,
    /******/ 			loaded: false
    /******/ 		};
    
    /******/ 		// Execute the module function
    /******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
    
    /******/ 		// Flag the module as loaded
    /******/ 		module.loaded = true;
    
    /******/ 		// Return the exports of the module
    /******/ 		return module.exports;
    /******/ 	}
    
    
    /******/ 	// expose the modules object (__webpack_modules__)
    /******/ 	__webpack_require__.m = modules;
    
    /******/ 	// expose the module cache
    /******/ 	__webpack_require__.c = installedModules;
    
    /******/ 	// __webpack_public_path__
    /******/ 	__webpack_require__.p = "";
    
    /******/ 	// Load entry module and return exports
    /******/ 	return __webpack_require__(0);
    /******/ })
    /************************************************************************/
    /******/ ([
    /* 0 */
    /***/ function(module, exports, __webpack_require__) {
    
    	module.exports = __webpack_require__(1);
    
    
    /***/ },
    /* 1 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var ALL_PLUGINS, HypermediaPlugin, Octokat, OctokatBase, deprecate;
    
    	deprecate = __webpack_require__(2);
    
    	OctokatBase = __webpack_require__(3);
    
    	HypermediaPlugin = __webpack_require__(18);
    
    	ALL_PLUGINS = [__webpack_require__(19), __webpack_require__(21), __webpack_require__(25), __webpack_require__(27), __webpack_require__(29), __webpack_require__(31), __webpack_require__(12), __webpack_require__(32), __webpack_require__(33), __webpack_require__(34), __webpack_require__(35), HypermediaPlugin, __webpack_require__(36)];
    
    	Octokat = function(clientOptions) {
    	  var instance;
    	  if (clientOptions == null) {
    	    clientOptions = {};
    	  }
    	  if (clientOptions.plugins == null) {
    	    clientOptions.plugins = ALL_PLUGINS;
    	  }
    	  if (clientOptions.disableHypermedia) {
    	    deprecate('Please use the clientOptions.plugins array and just do not include the hypermedia plugin');
    	    clientOptions.plugins = clientOptions.plugins.filter(function(plugin) {
    	      return plugin !== HypermediaPlugin;
    	    });
    	  }
    	  instance = new OctokatBase(clientOptions);
    	  return instance;
    	};
    
    	module.exports = Octokat;
    
    
    /***/ },
    /* 2 */
    /***/ function(module, exports) {
    
    	module.exports = function(message) {
    	  return typeof console !== "undefined" && console !== null ? typeof console.warn === "function" ? console.warn("Octokat Deprecation: " + message) : void 0 : void 0;
    	};
    
    
    /***/ },
    /* 3 */
    /***/ function(module, exports, __webpack_require__) {
    
    	/* WEBPACK VAR INJECTION */(function(global) {var Chainer, NativePromiseOnlyPlugin, OctokatBase, Requester, SimpleVerbsPlugin, TREE_OPTIONS, VerbMethods, applyHypermedia, deprecate, plus, ref, toPromise, uncamelizeObj,
    	  slice = [].slice;
    
    	plus = __webpack_require__(4);
    
    	deprecate = __webpack_require__(2);
    
    	TREE_OPTIONS = __webpack_require__(8);
    
    	Chainer = __webpack_require__(9);
    
    	ref = __webpack_require__(10), VerbMethods = ref.VerbMethods, toPromise = ref.toPromise;
    
    	SimpleVerbsPlugin = __webpack_require__(12);
    
    	NativePromiseOnlyPlugin = __webpack_require__(13);
    
    	Requester = __webpack_require__(15);
    
    	applyHypermedia = __webpack_require__(17);
    
    	uncamelizeObj = function(obj) {
    	  var i, j, key, len, o, ref1, value;
    	  if (Array.isArray(obj)) {
    	    return (function() {
    	      var j, len, results;
    	      results = [];
    	      for (j = 0, len = obj.length; j < len; j++) {
    	        i = obj[j];
    	        results.push(uncamelizeObj(i));
    	      }
    	      return results;
    	    })();
    	  } else if (obj === Object(obj)) {
    	    o = {};
    	    ref1 = Object.keys(obj);
    	    for (j = 0, len = ref1.length; j < len; j++) {
    	      key = ref1[j];
    	      value = obj[key];
    	      o[plus.uncamelize(key)] = uncamelizeObj(value);
    	    }
    	    return o;
    	  } else {
    	    return obj;
    	  }
    	};
    
    	OctokatBase = function(clientOptions) {
    	  var disableHypermedia, instance, newPromise, plugins, request, verbMethods;
    	  if (clientOptions == null) {
    	    clientOptions = {};
    	  }
    	  plugins = clientOptions.plugins || [SimpleVerbsPlugin, NativePromiseOnlyPlugin];
    	  disableHypermedia = clientOptions.disableHypermedia;
    	  if (disableHypermedia == null) {
    	    disableHypermedia = false;
    	  }
    	  instance = {};
    	  request = function(method, path, data, options, cb) {
    	    var ref1, requester;
    	    if (options == null) {
    	      options = {
    	        raw: false,
    	        isBase64: false,
    	        isBoolean: false
    	      };
    	    }
    	    if (data && !(typeof global !== "undefined" && global !== null ? (ref1 = global['Buffer']) != null ? ref1.isBuffer(data) : void 0 : void 0)) {
    	      data = uncamelizeObj(data);
    	    }
    	    requester = new Requester(instance, clientOptions, plugins);
    	    return requester.request(method, path, data, options, function(err, val) {
    	      var context;
    	      if (err) {
    	        return cb(err);
    	      }
    	      if (options.raw) {
    	        return cb(null, val);
    	      }
    	      if (!disableHypermedia) {
    	        context = {
    	          data: val,
    	          plugins: plugins,
    	          requester: requester,
    	          instance: instance,
    	          clientOptions: clientOptions
    	        };
    	        return instance._parseWithContext(path, context, cb);
    	      } else {
    	        return cb(null, val);
    	      }
    	    });
    	  };
    	  verbMethods = new VerbMethods(plugins, {
    	    request: request
    	  });
    	  (new Chainer(verbMethods)).chain('', null, TREE_OPTIONS, instance);
    	  instance.me = instance.user;
    	  instance.parse = function(cb, data) {
    	    var context;
    	    context = {
    	      requester: {
    	        request: request
    	      },
    	      plugins: plugins,
    	      data: data,
    	      instance: instance,
    	      clientOptions: clientOptions
    	    };
    	    return instance._parseWithContext('', context, cb);
    	  };
    	  newPromise = plugins.filter(function(arg) {
    	    var promiseCreator;
    	    promiseCreator = arg.promiseCreator;
    	    return promiseCreator;
    	  })[0].promiseCreator.newPromise;
    	  instance.parse = toPromise(instance.parse, newPromise);
    	  instance._parseWithContext = function(path, context, cb) {
    	    var data, requester, responseMiddlewareAsyncs;
    	    if (typeof cb !== 'function') {
    	      throw new Error('Callback is required');
    	    }
    	    data = context.data, requester = context.requester;
    	    context.url = (data != null ? data.url : void 0) || path;
    	    responseMiddlewareAsyncs = plus.map(plus.filter(plugins, function(arg) {
    	      var responseMiddlewareAsync;
    	      responseMiddlewareAsync = arg.responseMiddlewareAsync;
    	      return responseMiddlewareAsync;
    	    }), function(plugin) {
    	      return plugin.responseMiddlewareAsync.bind(plugin);
    	    });
    	    responseMiddlewareAsyncs.unshift(function(cb) {
    	      return cb(null, context);
    	    });
    	    return plus.waterfall(responseMiddlewareAsyncs, function(err, val) {
    	      if (err) {
    	        return cb(err, val);
    	      }
    	      data = val.data;
    	      return cb(err, data);
    	    });
    	  };
    	  instance._fromUrlWithDefault = function() {
    	    var args, defaultFn, path;
    	    path = arguments[0], defaultFn = arguments[1], args = 3 <= arguments.length ? slice.call(arguments, 2) : [];
    	    path = applyHypermedia.apply(null, [path].concat(slice.call(args)));
    	    verbMethods.injectVerbMethods(path, defaultFn);
    	    return defaultFn;
    	  };
    	  instance.fromUrl = function() {
    	    var args, defaultFn, path;
    	    path = arguments[0], args = 2 <= arguments.length ? slice.call(arguments, 1) : [];
    	    defaultFn = function() {
    	      var args;
    	      args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	      deprecate('call ....fetch() explicitly instead of ...()');
    	      return defaultFn.fetch.apply(defaultFn, args);
    	    };
    	    return instance._fromUrlWithDefault.apply(instance, [path, defaultFn].concat(slice.call(args)));
    	  };
    	  instance._fromUrlCurried = function(path, defaultFn) {
    	    var fn;
    	    fn = function() {
    	      var templateArgs;
    	      templateArgs = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	      if (defaultFn && templateArgs.length === 0) {
    	        return defaultFn.apply(fn);
    	      } else {
    	        return instance.fromUrl.apply(instance, [path].concat(slice.call(templateArgs)));
    	      }
    	    };
    	    if (!/\{/.test(path)) {
    	      verbMethods.injectVerbMethods(path, fn);
    	    }
    	    return fn;
    	  };
    	  instance.status = instance.fromUrl('https://status.github.com/api/status.json');
    	  instance.status.api = instance.fromUrl('https://status.github.com/api.json');
    	  instance.status.lastMessage = instance.fromUrl('https://status.github.com/api/last-message.json');
    	  instance.status.messages = instance.fromUrl('https://status.github.com/api/messages.json');
    	  return instance;
    	};
    
    	module.exports = OctokatBase;
    
    	/* WEBPACK VAR INJECTION */}.call(exports, (function() { return this; }())))
    
    /***/ },
    /* 4 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var filter, forEach, map, onlyOnce, plus;
    
    	filter = __webpack_require__(5);
    
    	forEach = __webpack_require__(6);
    
    	map = __webpack_require__(7);
    
    	onlyOnce = function(fn) {
    	  return function() {
    	    var callFn;
    	    if (fn === null) {
    	      throw new Error("Callback was already called.");
    	    }
    	    callFn = fn;
    	    fn = null;
    	    return callFn.apply(this, arguments);
    	  };
    	};
    
    	plus = {
    	  camelize: function(string) {
    	    if (string) {
    	      return string.replace(/[_-]+(\w)/g, function(m) {
    	        return m[1].toUpperCase();
    	      });
    	    } else {
    	      return '';
    	    }
    	  },
    	  uncamelize: function(string) {
    	    if (!string) {
    	      return '';
    	    }
    	    return string.replace(/([A-Z])+/g, function(match, letter) {
    	      if (letter == null) {
    	        letter = '';
    	      }
    	      return "_" + (letter.toLowerCase());
    	    });
    	  },
    	  dasherize: function(string) {
    	    if (!string) {
    	      return '';
    	    }
    	    string = string[0].toLowerCase() + string.slice(1);
    	    return string.replace(/([A-Z])|(_)/g, function(m, letter) {
    	      if (letter) {
    	        return '-' + letter.toLowerCase();
    	      } else {
    	        return '-';
    	      }
    	    });
    	  },
    	  waterfall: function(tasks, cb) {
    	    var nextTask, taskIndex;
    	    taskIndex = 0;
    	    nextTask = function(val) {
    	      var task, taskCallback;
    	      if (taskIndex === tasks.length) {
    	        return cb(null, val);
    	      }
    	      taskCallback = onlyOnce(function(err, val) {
    	        if (err) {
    	          return cb(err, val);
    	        }
    	        return nextTask(val);
    	      });
    	      task = tasks[taskIndex++];
    	      if (val) {
    	        return task(val, taskCallback);
    	      } else {
    	        return task(taskCallback);
    	      }
    	    };
    	    return nextTask(null);
    	  },
    	  extend: function(target, source) {
    	    var i, key, len, ref, results;
    	    if (source) {
    	      ref = Object.keys(source);
    	      results = [];
    	      for (i = 0, len = ref.length; i < len; i++) {
    	        key = ref[i];
    	        results.push(target[key] = source[key]);
    	      }
    	      return results;
    	    }
    	  },
    	  forOwn: function(obj, iterator) {
    	    var i, key, len, ref, results;
    	    ref = Object.keys(obj);
    	    results = [];
    	    for (i = 0, len = ref.length; i < len; i++) {
    	      key = ref[i];
    	      results.push(iterator(obj[key], key));
    	    }
    	    return results;
    	  },
    	  filter: filter,
    	  forEach: forEach,
    	  map: map
    	};
    
    	module.exports = plus;
    
    
    /***/ },
    /* 5 */
    /***/ function(module, exports) {
    
    	/**
    	 * A specialized version of `_.filter` for arrays without support for callback
    	 * shorthands and `this` binding.
    	 *
    	 * @private
    	 * @param {Array} array The array to iterate over.
    	 * @param {Function} predicate The function invoked per iteration.
    	 * @returns {Array} Returns the new filtered array.
    	 */
    	function arrayFilter(array, predicate) {
    	  var index = -1,
    	      length = array.length,
    	      resIndex = -1,
    	      result = [];
    
    	  while (++index < length) {
    	    var value = array[index];
    	    if (predicate(value, index, array)) {
    	      result[++resIndex] = value;
    	    }
    	  }
    	  return result;
    	}
    
    	module.exports = arrayFilter;
    
    
    /***/ },
    /* 6 */
    /***/ function(module, exports) {
    
    	/**
    	 * A specialized version of `_.forEach` for arrays without support for callback
    	 * shorthands and `this` binding.
    	 *
    	 * @private
    	 * @param {Array} array The array to iterate over.
    	 * @param {Function} iteratee The function invoked per iteration.
    	 * @returns {Array} Returns `array`.
    	 */
    	function arrayEach(array, iteratee) {
    	  var index = -1,
    	      length = array.length;
    
    	  while (++index < length) {
    	    if (iteratee(array[index], index, array) === false) {
    	      break;
    	    }
    	  }
    	  return array;
    	}
    
    	module.exports = arrayEach;
    
    
    /***/ },
    /* 7 */
    /***/ function(module, exports) {
    
    	/**
    	 * A specialized version of `_.map` for arrays without support for callback
    	 * shorthands and `this` binding.
    	 *
    	 * @private
    	 * @param {Array} array The array to iterate over.
    	 * @param {Function} iteratee The function invoked per iteration.
    	 * @returns {Array} Returns the new mapped array.
    	 */
    	function arrayMap(array, iteratee) {
    	  var index = -1,
    	      length = array.length,
    	      result = Array(length);
    
    	  while (++index < length) {
    	    result[index] = iteratee(array[index], index, array);
    	  }
    	  return result;
    	}
    
    	module.exports = arrayMap;
    
    
    /***/ },
    /* 8 */
    /***/ function(module, exports) {
    
    	module.exports = {
    	  'zen': false,
    	  'octocat': false,
    	  'organizations': false,
    	  'issues': false,
    	  'emojis': false,
    	  'markdown': false,
    	  'meta': false,
    	  'rate_limit': false,
    	  'feeds': false,
    	  'events': false,
    	  'notifications': {
    	    'threads': {
    	      'subscription': false
    	    }
    	  },
    	  'gitignore': {
    	    'templates': false
    	  },
    	  'user': {
    	    'repos': false,
    	    'orgs': false,
    	    'followers': false,
    	    'following': false,
    	    'emails': false,
    	    'issues': false,
    	    'starred': false,
    	    'teams': false
    	  },
    	  'orgs': {
    	    'repos': false,
    	    'issues': false,
    	    'members': false,
    	    'events': false,
    	    'teams': false
    	  },
    	  'teams': {
    	    'members': false,
    	    'memberships': false,
    	    'repos': false
    	  },
    	  'users': {
    	    'repos': false,
    	    'orgs': false,
    	    'gists': false,
    	    'followers': false,
    	    'following': false,
    	    'keys': false,
    	    'starred': false,
    	    'received_events': {
    	      'public': false
    	    },
    	    'events': {
    	      'public': false,
    	      'orgs': false
    	    },
    	    'site_admin': false,
    	    'suspended': false
    	  },
    	  'search': {
    	    'repositories': false,
    	    'issues': false,
    	    'users': false,
    	    'code': false
    	  },
    	  'gists': {
    	    'public': false,
    	    'starred': false,
    	    'star': false,
    	    'comments': false,
    	    'forks': false
    	  },
    	  'repos': {
    	    'readme': false,
    	    'tarball': false,
    	    'zipball': false,
    	    'compare': false,
    	    'deployments': {
    	      'statuses': false
    	    },
    	    'hooks': {
    	      'tests': false
    	    },
    	    'assignees': false,
    	    'languages': false,
    	    'teams': false,
    	    'tags': false,
    	    'branches': false,
    	    'contributors': false,
    	    'subscribers': false,
    	    'subscription': false,
    	    'stargazers': false,
    	    'comments': false,
    	    'downloads': false,
    	    'forks': false,
    	    'milestones': {
    	      'labels': false
    	    },
    	    'labels': false,
    	    'releases': {
    	      'assets': false,
    	      'latest': false,
    	      'tags': false
    	    },
    	    'events': false,
    	    'notifications': false,
    	    'merges': false,
    	    'statuses': false,
    	    'pulls': {
    	      'merge': false,
    	      'comments': false,
    	      'commits': false,
    	      'files': false,
    	      'events': false,
    	      'labels': false
    	    },
    	    'pages': {
    	      'builds': {
    	        'latest': false
    	      }
    	    },
    	    'commits': {
    	      'comments': false,
    	      'status': false,
    	      'statuses': false
    	    },
    	    'contents': false,
    	    'collaborators': false,
    	    'issues': {
    	      'events': false,
    	      'comments': false,
    	      'labels': false
    	    },
    	    'git': {
    	      'refs': {
    	        'heads': false,
    	        'tags': false
    	      },
    	      'trees': false,
    	      'blobs': false,
    	      'commits': false
    	    },
    	    'stats': {
    	      'contributors': false,
    	      'commit_activity': false,
    	      'code_frequency': false,
    	      'participation': false,
    	      'punch_card': false
    	    }
    	  },
    	  'licenses': false,
    	  'authorizations': {
    	    'clients': false
    	  },
    	  'applications': {
    	    'tokens': false
    	  },
    	  'enterprise': {
    	    'settings': {
    	      'license': false
    	    },
    	    'stats': {
    	      'issues': false,
    	      'hooks': false,
    	      'milestones': false,
    	      'orgs': false,
    	      'comments': false,
    	      'pages': false,
    	      'users': false,
    	      'gists': false,
    	      'pulls': false,
    	      'repos': false,
    	      'all': false
    	    }
    	  },
    	  'staff': {
    	    'indexing_jobs': false
    	  },
    	  'setup': {
    	    'api': {
    	      'start': false,
    	      'upgrade': false,
    	      'configcheck': false,
    	      'configure': false,
    	      'settings': {
    	        'authorized-keys': false
    	      },
    	      'maintenance': false
    	    }
    	  }
    	};
    
    
    /***/ },
    /* 9 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var Chainer, plus,
    	  slice = [].slice;
    
    	plus = __webpack_require__(4);
    
    	module.exports = Chainer = (function() {
    	  function Chainer(_verbMethods) {
    	    this._verbMethods = _verbMethods;
    	  }
    
    	  Chainer.prototype.chain = function(path, name, contextTree, fn) {
    	    var fn1;
    	    if (fn == null) {
    	      fn = (function(_this) {
    	        return function() {
    	          var args, separator;
    	          args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	          if (!args.length) {
    	            throw new Error('BUG! must be called with at least one argument');
    	          }
    	          if (name === 'compare') {
    	            separator = '...';
    	          } else {
    	            separator = '/';
    	          }
    	          return _this.chain(path + "/" + (args.join(separator)), name, contextTree);
    	        };
    	      })(this);
    	    }
    	    this._verbMethods.injectVerbMethods(path, fn);
    	    if (typeof fn === 'function' || typeof fn === 'object') {
    	      fn1 = (function(_this) {
    	        return function(name) {
    	          delete fn[plus.camelize(name)];
    	          return Object.defineProperty(fn, plus.camelize(name), {
    	            configurable: true,
    	            enumerable: true,
    	            get: function() {
    	              return _this.chain(path + "/" + name, name, contextTree[name]);
    	            }
    	          });
    	        };
    	      })(this);
    	      for (name in contextTree || {}) {
    	        fn1(name);
    	      }
    	    }
    	    return fn;
    	  };
    
    	  return Chainer;
    
    	})();
    
    	module.exports = Chainer;
    
    
    /***/ },
    /* 10 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var VerbMethods, extend, filter, forOwn, ref, toPromise, toQueryString,
    	  slice = [].slice;
    
    	ref = __webpack_require__(4), filter = ref.filter, forOwn = ref.forOwn, extend = ref.extend;
    
    	toQueryString = __webpack_require__(11);
    
    	toPromise = function(orig, newPromise) {
    	  return function() {
    	    var args, last;
    	    args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	    last = args[args.length - 1];
    	    if (typeof last === 'function') {
    	      args.pop();
    	      return orig.apply(null, [last].concat(slice.call(args)));
    	    } else if (newPromise) {
    	      return newPromise(function(resolve, reject) {
    	        var cb;
    	        cb = function(err, val) {
    	          if (err) {
    	            return reject(err);
    	          }
    	          return resolve(val);
    	        };
    	        return orig.apply(null, [cb].concat(slice.call(args)));
    	      });
    	    } else {
    	      throw new Error('You must specify a callback or have a promise library loaded');
    	    }
    	  };
    	};
    
    	VerbMethods = (function() {
    	  function VerbMethods(plugins, _requester) {
    	    var i, j, len, len1, plugin, promisePlugins, ref1, ref2;
    	    this._requester = _requester;
    	    if (!this._requester) {
    	      throw new Error('Octokat BUG: request is required');
    	    }
    	    promisePlugins = filter(plugins, function(arg) {
    	      var promiseCreator;
    	      promiseCreator = arg.promiseCreator;
    	      return promiseCreator;
    	    });
    	    if (promisePlugins) {
    	      this._promisePlugin = promisePlugins[0];
    	    }
    	    this._syncVerbs = {};
    	    ref1 = filter(plugins, function(arg) {
    	      var verbs;
    	      verbs = arg.verbs;
    	      return verbs;
    	    });
    	    for (i = 0, len = ref1.length; i < len; i++) {
    	      plugin = ref1[i];
    	      extend(this._syncVerbs, plugin.verbs);
    	    }
    	    this._asyncVerbs = {};
    	    ref2 = filter(plugins, function(arg) {
    	      var asyncVerbs;
    	      asyncVerbs = arg.asyncVerbs;
    	      return asyncVerbs;
    	    });
    	    for (j = 0, len1 = ref2.length; j < len1; j++) {
    	      plugin = ref2[j];
    	      extend(this._asyncVerbs, plugin.asyncVerbs);
    	    }
    	  }
    
    	  VerbMethods.prototype.injectVerbMethods = function(path, obj) {
    	    var allPromises, newPromise, ref1;
    	    if (this._promisePlugin) {
    	      ref1 = this._promisePlugin.promiseCreator, newPromise = ref1.newPromise, allPromises = ref1.allPromises;
    	    }
    	    obj.url = path;
    	    forOwn(this._syncVerbs, (function(_this) {
    	      return function(verbFunc, verbName) {
    	        return obj[verbName] = function() {
    	          var args, makeRequest;
    	          args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	          makeRequest = function() {
    	            var cb, data, method, options, originalArgs, ref2;
    	            cb = arguments[0], originalArgs = 2 <= arguments.length ? slice.call(arguments, 1) : [];
    	            ref2 = verbFunc.apply(null, [path].concat(slice.call(originalArgs))), method = ref2.method, path = ref2.path, data = ref2.data, options = ref2.options;
    	            return _this._requester.request(method, path, data, options, cb);
    	          };
    	          return toPromise(makeRequest, newPromise).apply(null, args);
    	        };
    	      };
    	    })(this));
    	    return forOwn(this._asyncVerbs, (function(_this) {
    	      return function(verbFunc, verbName) {
    	        return obj[verbName] = function() {
    	          var args, makeRequest;
    	          args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	          makeRequest = verbFunc(_this._requester, path);
    	          return toPromise(makeRequest, newPromise).apply(null, args);
    	        };
    	      };
    	    })(this));
    	  };
    
    	  return VerbMethods;
    
    	})();
    
    	module.exports = {
    	  VerbMethods: VerbMethods,
    	  toPromise: toPromise
    	};
    
    
    /***/ },
    /* 11 */
    /***/ function(module, exports) {
    
    	var toQueryString;
    
    	toQueryString = function(options, omitQuestionMark) {
    	  var key, params, ref, value;
    	  if (!options || options === {}) {
    	    return '';
    	  }
    	  params = [];
    	  ref = options || {};
    	  for (key in ref) {
    	    value = ref[key];
    	    if (value) {
    	      params.push(key + "=" + (encodeURIComponent(value)));
    	    }
    	  }
    	  if (params.length) {
    	    if (omitQuestionMark) {
    	      return "&" + (params.join('&'));
    	    } else {
    	      return "?" + (params.join('&'));
    	    }
    	  } else {
    	    return '';
    	  }
    	};
    
    	module.exports = toQueryString;
    
    
    /***/ },
    /* 12 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var SimpleVerbs, toQueryString,
    	  slice = [].slice;
    
    	toQueryString = __webpack_require__(11);
    
    	module.exports = new (SimpleVerbs = (function() {
    	  function SimpleVerbs() {}
    
    	  SimpleVerbs.prototype.verbs = {
    	    fetch: function(path, query) {
    	      return {
    	        method: 'GET',
    	        path: "" + path + (toQueryString(query))
    	      };
    	    },
    	    read: function(path, query) {
    	      return {
    	        method: 'GET',
    	        path: "" + path + (toQueryString(query)),
    	        options: {
    	          isRaw: true
    	        }
    	      };
    	    },
    	    remove: function(path, data) {
    	      return {
    	        method: 'DELETE',
    	        path: path,
    	        data: data,
    	        options: {
    	          isBoolean: true
    	        }
    	      };
    	    },
    	    create: function(path, data, contentType) {
    	      if (contentType) {
    	        return {
    	          method: 'POST',
    	          path: path,
    	          data: data,
    	          options: {
    	            isRaw: true,
    	            contentType: contentType
    	          }
    	        };
    	      } else {
    	        return {
    	          method: 'POST',
    	          path: path,
    	          data: data
    	        };
    	      }
    	    },
    	    update: function(path, data) {
    	      return {
    	        method: 'PATCH',
    	        path: path,
    	        data: data
    	      };
    	    },
    	    add: function(path, data) {
    	      return {
    	        method: 'PUT',
    	        path: path,
    	        data: data,
    	        options: {
    	          isBoolean: true
    	        }
    	      };
    	    },
    	    contains: function() {
    	      var args, path;
    	      path = arguments[0], args = 2 <= arguments.length ? slice.call(arguments, 1) : [];
    	      return {
    	        method: 'GET',
    	        path: path + "/" + (args.join('/')),
    	        options: {
    	          isBoolean: true
    	        }
    	      };
    	    }
    	  };
    
    	  return SimpleVerbs;
    
    	})());
    
    
    /***/ },
    /* 13 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var UseNativePromises;
    
    	module.exports = new (UseNativePromises = (function() {
    	  function UseNativePromises() {}
    
    	  UseNativePromises.prototype.promiseCreator = __webpack_require__(14);
    
    	  return UseNativePromises;
    
    	})());
    
    
    /***/ },
    /* 14 */
    /***/ function(module, exports) {
    
    	var allPromises, newPromise;
    
    	if (typeof Promise !== "undefined" && Promise !== null) {
    	  newPromise = (function(_this) {
    	    return function(fn) {
    	      return new Promise(function(resolve, reject) {
    	        if (resolve.fulfill) {
    	          return fn(resolve.resolve.bind(resolve), resolve.reject.bind(resolve));
    	        } else {
    	          return fn.apply(null, arguments);
    	        }
    	      });
    	    };
    	  })(this);
    	  allPromises = (function(_this) {
    	    return function(promises) {
    	      return Promise.all(promises);
    	    };
    	  })(this);
    	}
    
    	module.exports = {
    	  newPromise: newPromise,
    	  allPromises: allPromises
    	};
    
    
    /***/ },
    /* 15 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var require;var Requester, ajax, eventId, extend, filter, forEach, map, ref, waterfall;
    
    	ref = __webpack_require__(4), filter = ref.filter, forEach = ref.forEach, extend = ref.extend, map = ref.map, waterfall = ref.waterfall;
    
    	ajax = function(options, cb) {
    	  var XMLHttpRequest, name, ref1, req, value, xhr;
    	  if (typeof window !== "undefined" && window !== null) {
    	    XMLHttpRequest = window.XMLHttpRequest;
    	  } else {
    	    req = require;
    	    XMLHttpRequest = __webpack_require__(16).XMLHttpRequest;
    	  }
    	  xhr = new XMLHttpRequest();
    	  xhr.dataType = options.dataType;
    	  if (typeof xhr.overrideMimeType === "function") {
    	    xhr.overrideMimeType(options.mimeType);
    	  }
    	  xhr.open(options.type, options.url);
    	  if (options.data && options.type !== 'GET') {
    	    xhr.setRequestHeader('Content-Type', options.contentType);
    	  }
    	  ref1 = options.headers;
    	  for (name in ref1) {
    	    value = ref1[name];
    	    xhr.setRequestHeader(name, value);
    	  }
    	  xhr.onreadystatechange = function() {
    	    var name1, ref2;
    	    if (4 === xhr.readyState) {
    	      if ((ref2 = options.statusCode) != null) {
    	        if (typeof ref2[name1 = xhr.status] === "function") {
    	          ref2[name1]();
    	        }
    	      }
    	      if (xhr.status >= 200 && xhr.status < 300 || xhr.status === 304 || xhr.status === 302 || xhr.status === 0) {
    	        return cb(null, xhr);
    	      } else {
    	        return cb(xhr);
    	      }
    	    }
    	  };
    	  return xhr.send(options.data);
    	};
    
    	eventId = 0;
    
    	module.exports = Requester = (function() {
    	  function Requester(_instance, _clientOptions, plugins) {
    	    var base, base1, base2;
    	    this._instance = _instance;
    	    this._clientOptions = _clientOptions != null ? _clientOptions : {};
    	    if ((base = this._clientOptions).rootURL == null) {
    	      base.rootURL = 'https://api.github.com';
    	    }
    	    if ((base1 = this._clientOptions).useETags == null) {
    	      base1.useETags = true;
    	    }
    	    if ((base2 = this._clientOptions).usePostInsteadOfPatch == null) {
    	      base2.usePostInsteadOfPatch = false;
    	    }
    	    if (typeof this._clientOptions.emitter === 'function') {
    	      this._emit = this._clientOptions.emitter;
    	    }
    	    this._pluginMiddlewareAsync = map(filter(plugins, function(arg) {
    	      var requestMiddlewareAsync;
    	      requestMiddlewareAsync = arg.requestMiddlewareAsync;
    	      return requestMiddlewareAsync;
    	    }), function(plugin) {
    	      return plugin.requestMiddlewareAsync.bind(plugin);
    	    });
    	    this._plugins = plugins;
    	  }
    
    	  Requester.prototype.request = function(method, path, data, options, cb) {
    	    var acc, headers, initial, pluginsPlusInitial;
    	    if (options == null) {
    	      options = {
    	        isRaw: false,
    	        isBase64: false,
    	        isBoolean: false,
    	        contentType: 'application/json'
    	      };
    	    }
    	    if (options == null) {
    	      options = {};
    	    }
    	    if (options.isRaw == null) {
    	      options.isRaw = false;
    	    }
    	    if (options.isBase64 == null) {
    	      options.isBase64 = false;
    	    }
    	    if (options.isBoolean == null) {
    	      options.isBoolean = false;
    	    }
    	    if (options.contentType == null) {
    	      options.contentType = 'application/json';
    	    }
    	    if (!/^http/.test(path)) {
    	      path = "" + this._clientOptions.rootURL + path;
    	    }
    	    headers = {
    	      'Accept': this._clientOptions.acceptHeader || 'application/json'
    	    };
    	    if (typeof window === "undefined" || window === null) {
    	      headers['User-Agent'] = 'octokat.js';
    	    }
    	    acc = {
    	      method: method,
    	      path: path,
    	      headers: headers,
    	      options: options,
    	      clientOptions: this._clientOptions
    	    };
    	    initial = function(cb) {
    	      return cb(null, acc);
    	    };
    	    pluginsPlusInitial = [initial].concat(this._pluginMiddlewareAsync);
    	    return waterfall(pluginsPlusInitial, (function(_this) {
    	      return function(err, acc) {
    	        var ajaxConfig, mimeType;
    	        if (err) {
    	          return cb(err, acc);
    	        }
    	        method = acc.method, headers = acc.headers, mimeType = acc.mimeType;
    	        if (options.isRaw) {
    	          headers['Accept'] = 'application/vnd.github.raw';
    	        }
    	        ajaxConfig = {
    	          url: path,
    	          type: method,
    	          contentType: options.contentType,
    	          mimeType: mimeType,
    	          headers: headers,
    	          processData: false,
    	          data: !options.isRaw && data && JSON.stringify(data) || data,
    	          dataType: !options.isRaw ? 'json' : void 0
    	        };
    	        if (options.isBoolean) {
    	          ajaxConfig.statusCode = {
    	            204: function() {
    	              return cb(null, true);
    	            },
    	            404: function() {
    	              return cb(null, false);
    	            }
    	          };
    	        }
    	        eventId++;
    	        if (typeof _this._emit === "function") {
    	          _this._emit('start', eventId, {
    	            method: method,
    	            path: path,
    	            data: data,
    	            options: options
    	          });
    	        }
    	        return ajax(ajaxConfig, function(err, val) {
    	          var emitterRate, jqXHR, json, rateLimit, rateLimitRemaining, rateLimitReset;
    	          jqXHR = err || val;
    	          if (_this._emit) {
    	            if (jqXHR.getResponseHeader('X-RateLimit-Limit')) {
    	              rateLimit = parseFloat(jqXHR.getResponseHeader('X-RateLimit-Limit'));
    	              rateLimitRemaining = parseFloat(jqXHR.getResponseHeader('X-RateLimit-Remaining'));
    	              rateLimitReset = parseFloat(jqXHR.getResponseHeader('X-RateLimit-Reset'));
    	              emitterRate = {
    	                remaining: rateLimitRemaining,
    	                limit: rateLimit,
    	                reset: rateLimitReset
    	              };
    	              if (jqXHR.getResponseHeader('X-OAuth-Scopes')) {
    	                emitterRate.scopes = jqXHR.getResponseHeader('X-OAuth-Scopes').split(', ');
    	              }
    	            }
    	            _this._emit('end', eventId, {
    	              method: method,
    	              path: path,
    	              data: data,
    	              options: options
    	            }, jqXHR.status, emitterRate);
    	          }
    	          if (!err) {
    	            if (jqXHR.status === 302) {
    	              return cb(null, jqXHR.getResponseHeader('Location'));
    	            } else if (!(jqXHR.status === 204 && options.isBoolean)) {
    	              if (jqXHR.responseText && ajaxConfig.dataType === 'json') {
    	                data = JSON.parse(jqXHR.responseText);
    	              } else {
    	                data = jqXHR.responseText;
    	              }
    	              acc = {
    	                clientOptions: _this._clientOptions,
    	                plugins: _this._plugins,
    	                data: data,
    	                options: options,
    	                jqXHR: jqXHR,
    	                status: jqXHR.status,
    	                request: acc,
    	                requester: _this,
    	                instance: _this._instance
    	              };
    	              return _this._instance._parseWithContext('', acc, function(err, val) {
    	                if (err) {
    	                  return cb(err, val);
    	                }
    	                return cb(null, val, jqXHR.status, jqXHR);
    	              });
    	            }
    	          } else {
    	            if (options.isBoolean && jqXHR.status === 404) {
    
    	            } else {
    	              err = new Error(jqXHR.responseText);
    	              err.status = jqXHR.status;
    	              if (jqXHR.getResponseHeader('Content-Type') === 'application/json; charset=utf-8') {
    	                if (jqXHR.responseText) {
    	                  try {
    	                    json = JSON.parse(jqXHR.responseText);
    	                  } catch (error) {
    	                    cb({
    	                      message: 'Error Parsing Response'
    	                    });
    	                  }
    	                } else {
    	                  json = '';
    	                }
    	                err.json = json;
    	              }
    	              return cb(err);
    	            }
    	          }
    	        });
    	      };
    	    })(this));
    	  };
    
    	  return Requester;
    
    	})();
    
    
    /***/ },
    /* 16 */
    /***/ function(module, exports) {
    
    	module.exports = window.XMLHTTPRequest;
    
    
    /***/ },
    /* 17 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var deprecate, toQueryString,
    	  slice = [].slice;
    
    	toQueryString = __webpack_require__(11);
    
    	deprecate = __webpack_require__(2);
    
    	module.exports = function() {
    	  var args, fieldName, fieldValue, i, j, k, len, len1, m, match, optionalNames, optionalParams, param, templateParams, url;
    	  url = arguments[0], args = 2 <= arguments.length ? slice.call(arguments, 1) : [];
    	  if (args.length === 0) {
    	    templateParams = {};
    	  } else {
    	    if (args.length > 1) {
    	      deprecate('When filling in a template URL pass all the field to fill in 1 object instead of comma-separated args');
    	    }
    	    templateParams = args[0];
    	  }
    	  i = 0;
    	  while (m = /(\{[^\}]+\})/.exec(url)) {
    	    match = m[1];
    	    param = '';
    	    switch (match[1]) {
    	      case '/':
    	        fieldName = match.slice(2, match.length - 1);
    	        fieldValue = templateParams[fieldName];
    	        if (fieldValue) {
    	          if (/\//.test(fieldValue)) {
    	            throw new Error("Octokat Error: this field must not contain slashes: " + fieldName);
    	          }
    	          param = "/" + fieldValue;
    	        }
    	        break;
    	      case '+':
    	        fieldName = match.slice(2, match.length - 1);
    	        fieldValue = templateParams[fieldName];
    	        if (fieldValue) {
    	          param = fieldValue;
    	        }
    	        break;
    	      case '?':
    	        optionalNames = match.slice(2, -1).split(',');
    	        optionalParams = {};
    	        for (j = 0, len = optionalNames.length; j < len; j++) {
    	          fieldName = optionalNames[j];
    	          optionalParams[fieldName] = templateParams[fieldName];
    	        }
    	        param = toQueryString(optionalParams);
    	        break;
    	      case '&':
    	        optionalNames = match.slice(2, -1).split(',');
    	        optionalParams = {};
    	        for (k = 0, len1 = optionalNames.length; k < len1; k++) {
    	          fieldName = optionalNames[k];
    	          optionalParams[fieldName] = templateParams[fieldName];
    	        }
    	        param = toQueryString(optionalParams, true);
    	        break;
    	      default:
    	        fieldName = match.slice(1, match.length - 1);
    	        if (templateParams[fieldName]) {
    	          param = templateParams[fieldName];
    	        } else {
    	          throw new Error("Octokat Error: Required parameter is missing: " + fieldName);
    	        }
    	    }
    	    url = url.replace(match, param);
    	    i++;
    	  }
    	  return url;
    	};
    
    
    /***/ },
    /* 18 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var HyperMedia, deprecate,
    	  slice = [].slice;
    
    	deprecate = __webpack_require__(2);
    
    	module.exports = new (HyperMedia = (function() {
    	  function HyperMedia() {}
    
    	  HyperMedia.prototype.replace = function(instance, data) {
    	    if (Array.isArray(data)) {
    	      return this._replaceArray(instance, data);
    	    } else if (typeof data === 'function') {
    	      return data;
    	    } else if (data instanceof Date) {
    	      return data;
    	    } else if (data === Object(data)) {
    	      return this._replaceObject(instance, data);
    	    } else {
    	      return data;
    	    }
    	  };
    
    	  HyperMedia.prototype._replaceObject = function(instance, orig) {
    	    var acc, i, key, len, ref, value;
    	    acc = {};
    	    ref = Object.keys(orig);
    	    for (i = 0, len = ref.length; i < len; i++) {
    	      key = ref[i];
    	      value = orig[key];
    	      this._replaceKeyValue(instance, acc, key, value);
    	    }
    	    return acc;
    	  };
    
    	  HyperMedia.prototype._replaceArray = function(instance, orig) {
    	    var arr, i, item, key, len, ref, value;
    	    arr = (function() {
    	      var i, len, results;
    	      results = [];
    	      for (i = 0, len = orig.length; i < len; i++) {
    	        item = orig[i];
    	        results.push(this.replace(instance, item));
    	      }
    	      return results;
    	    }).call(this);
    	    ref = Object.keys(orig);
    	    for (i = 0, len = ref.length; i < len; i++) {
    	      key = ref[i];
    	      value = orig[key];
    	      this._replaceKeyValue(instance, arr, key, value);
    	    }
    	    return arr;
    	  };
    
    	  HyperMedia.prototype._replaceKeyValue = function(instance, acc, key, value) {
    	    var defaultFn, fn, newKey;
    	    if (/_url$/.test(key)) {
    	      if (/^upload_url$/.test(key)) {
    	        defaultFn = function() {
    	          var args;
    	          args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	          deprecate('call .upload({name, label}).create(data, contentType)' + ' instead of .upload(name, data, contentType)');
    	          return defaultFn.create.apply(defaultFn, args);
    	        };
    	        fn = function() {
    	          var args;
    	          args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	          return instance._fromUrlWithDefault.apply(instance, [value, defaultFn].concat(slice.call(args)))();
    	        };
    	      } else {
    	        defaultFn = function() {
    	          deprecate('instead of directly calling methods like .nextPage(), use .nextPage.fetch()');
    	          return this.fetch();
    	        };
    	        fn = instance._fromUrlCurried(value, defaultFn);
    	      }
    	      newKey = key.substring(0, key.length - '_url'.length);
    	      acc[newKey] = fn;
    	      if (!/\{/.test(value)) {
    	        return acc[key] = value;
    	      }
    	    } else if (/_at$/.test(key)) {
    	      return acc[key] = value ? new Date(value) : null;
    	    } else {
    	      return acc[key] = this.replace(instance, value);
    	    }
    	  };
    
    	  HyperMedia.prototype.responseMiddlewareAsync = function(input, cb) {
    	    var data, instance;
    	    instance = input.instance, data = input.data;
    	    data = this.replace(instance, data);
    	    input.data = data;
    	    return cb(null, input);
    	  };
    
    	  return HyperMedia;
    
    	})());
    
    
    /***/ },
    /* 19 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var Chainer, OBJECT_MATCHER, ObjectChainer, TREE_OPTIONS, VerbMethods;
    
    	OBJECT_MATCHER = __webpack_require__(20);
    
    	TREE_OPTIONS = __webpack_require__(8);
    
    	VerbMethods = __webpack_require__(10).VerbMethods;
    
    	Chainer = __webpack_require__(9);
    
    	module.exports = new (ObjectChainer = (function() {
    	  function ObjectChainer() {}
    
    	  ObjectChainer.prototype.chainChildren = function(chainer, url, obj) {
    	    var context, i, k, key, len, re, ref, results;
    	    results = [];
    	    for (key in OBJECT_MATCHER) {
    	      re = OBJECT_MATCHER[key];
    	      if (re.test(obj.url)) {
    	        context = TREE_OPTIONS;
    	        ref = key.split('.');
    	        for (i = 0, len = ref.length; i < len; i++) {
    	          k = ref[i];
    	          context = context[k];
    	        }
    	        results.push(chainer.chain(url, k, context, obj));
    	      } else {
    	        results.push(void 0);
    	      }
    	    }
    	    return results;
    	  };
    
    	  ObjectChainer.prototype.responseMiddlewareAsync = function(input, cb) {
    	    var chainer, data, datum, i, len, plugins, requester, url, verbMethods;
    	    plugins = input.plugins, requester = input.requester, data = input.data, url = input.url;
    	    verbMethods = new VerbMethods(plugins, requester);
    	    chainer = new Chainer(verbMethods);
    	    if (url) {
    	      chainer.chain(url, true, {}, data);
    	      this.chainChildren(chainer, url, data);
    	    } else {
    	      chainer.chain('', null, {}, data);
    	      if (Array.isArray(data)) {
    	        for (i = 0, len = data.length; i < len; i++) {
    	          datum = data[i];
    	          this.chainChildren(chainer, datum.url, datum);
    	        }
    	      }
    	    }
    	    return cb(null, input);
    	  };
    
    	  return ObjectChainer;
    
    	})());
    
    
    /***/ },
    /* 20 */
    /***/ function(module, exports) {
    
    	module.exports = {
    	  'repos': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/repos\/[^\/]+\/[^\/]+$/,
    	  'gists': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/gists\/[^\/]+$/,
    	  'issues': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/repos\/[^\/]+\/[^\/]+\/(issues|pulls)\/[^\/]+$/,
    	  'users': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/users\/[^\/]+$/,
    	  'orgs': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/orgs\/[^\/]+$/,
    	  'teams': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/teams\/[^\/]+$/,
    	  'repos.comments': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/repos\/[^\/]+\/[^\/]+\/comments\/[^\/]+$/
    	};
    
    
    /***/ },
    /* 21 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var PreferLibraryOverNativePromises, allPromises, newPromise, ref, ref1, ref2;
    
    	ref = __webpack_require__(22), newPromise = ref.newPromise, allPromises = ref.allPromises;
    
    	if (!(newPromise && allPromises)) {
    	  ref1 = __webpack_require__(14), newPromise = ref1.newPromise, allPromises = ref1.allPromises;
    	}
    
    	if (!((typeof window !== "undefined" && window !== null) || newPromise)) {
    	  ref2 = __webpack_require__(23), newPromise = ref2.newPromise, allPromises = ref2.allPromises;
    	}
    
    	if ((typeof window !== "undefined" && window !== null) && !newPromise) {
    	  if (typeof console !== "undefined" && console !== null) {
    	    if (typeof console.warn === "function") {
    	      console.warn('Octokat: A Promise API was not found. Supported libraries that have Promises are jQuery, angularjs, and es6-promise');
    	    }
    	  }
    	} else if ((typeof window === "undefined" || window === null) && !newPromise) {
    	  throw new Error('Could not find a promise lib for node. Seems like a bug');
    	}
    
    	module.exports = new (PreferLibraryOverNativePromises = (function() {
    	  function PreferLibraryOverNativePromises() {}
    
    	  PreferLibraryOverNativePromises.prototype.promiseCreator = {
    	    newPromise: newPromise,
    	    allPromises: allPromises
    	  };
    
    	  return PreferLibraryOverNativePromises;
    
    	})());
    
    
    /***/ },
    /* 22 */
    /***/ function(module, exports) {
    
    	var allPromises, injector, newPromise, ref,
    	  slice = [].slice;
    
    	if (typeof window !== "undefined" && window !== null) {
    	  if (window.Q) {
    	    newPromise = (function(_this) {
    	      return function(fn) {
    	        var deferred, reject, resolve;
    	        deferred = window.Q.defer();
    	        resolve = function(val) {
    	          return deferred.resolve(val);
    	        };
    	        reject = function(err) {
    	          return deferred.reject(err);
    	        };
    	        fn(resolve, reject);
    	        return deferred.promise;
    	      };
    	    })(this);
    	    allPromises = function(promises) {
    	      return window.Q.all(promises);
    	    };
    	  } else if (window.angular) {
    	    newPromise = null;
    	    allPromises = null;
    	    injector = angular.injector(['ng']);
    	    injector.invoke(function($q) {
    	      newPromise = function(fn) {
    	        var deferred, reject, resolve;
    	        deferred = $q.defer();
    	        resolve = function(val) {
    	          return deferred.resolve(val);
    	        };
    	        reject = function(err) {
    	          return deferred.reject(err);
    	        };
    	        fn(resolve, reject);
    	        return deferred.promise;
    	      };
    	      return allPromises = function(promises) {
    	        return $q.all(promises);
    	      };
    	    });
    	  } else if ((ref = window.jQuery) != null ? ref.Deferred : void 0) {
    	    newPromise = (function(_this) {
    	      return function(fn) {
    	        var promise, reject, resolve;
    	        promise = window.jQuery.Deferred();
    	        resolve = function(val) {
    	          return promise.resolve(val);
    	        };
    	        reject = function(val) {
    	          return promise.reject(val);
    	        };
    	        fn(resolve, reject);
    	        return promise.promise();
    	      };
    	    })(this);
    	    allPromises = (function(_this) {
    	      return function(promises) {
    	        var ref1;
    	        return (ref1 = window.jQuery).when.apply(ref1, promises).then(function() {
    	          var promises;
    	          promises = 1 <= arguments.length ? slice.call(arguments, 0) : [];
    	          return promises;
    	        });
    	      };
    	    })(this);
    	  }
    	}
    
    	module.exports = {
    	  newPromise: newPromise,
    	  allPromises: allPromises
    	};
    
    
    /***/ },
    /* 23 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var require;var Promise, allPromises, newPromise, req;
    
    	req = require;
    
    	Promise = this.Promise || __webpack_require__(24).Promise;
    
    	newPromise = function(fn) {
    	  return new Promise(fn);
    	};
    
    	allPromises = function(promises) {
    	  return Promise.all(promises);
    	};
    
    	module.exports = {
    	  newPromise: newPromise,
    	  allPromises: allPromises
    	};
    
    
    /***/ },
    /* 24 */
    /***/ function(module, exports) {
    
    	module.exports = window.Promise;
    
    
    /***/ },
    /* 25 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var PathValidator, URL_VALIDATOR;
    
    	URL_VALIDATOR = __webpack_require__(26);
    
    	module.exports = new (PathValidator = (function() {
    	  function PathValidator() {}
    
    	  PathValidator.prototype.requestMiddlewareAsync = function(input, cb) {
    	    var err, path;
    	    path = input.path;
    	    if (!URL_VALIDATOR.test(path)) {
    	      err = "Octokat BUG: Invalid Path. If this is actually a valid path then please update the URL_VALIDATOR. path=" + path;
    	      console.warn(err);
    	    }
    	    return cb(null, input);
    	  };
    
    	  return PathValidator;
    
    	})());
    
    
    /***/ },
    /* 26 */
    /***/ function(module, exports) {
    
    	module.exports = /^(https:\/\/status.github.com\/api\/(status.json|last-message.json|messages.json)$)|(https?:\/\/[^\/]+)?(\/api\/v3)?\/(zen|octocat|users|organizations|issues|gists|emojis|markdown|meta|rate_limit|feeds|events|notifications|notifications\/threads(\/[^\/]+)|notifications\/threads(\/[^\/]+)\/subscription|gitignore\/templates(\/[^\/]+)?|user(\/\d+)?|user(\/\d+)?\/(|repos|orgs|followers|following(\/[^\/]+)?|emails(\/[^\/]+)?|issues|starred|starred(\/[^\/]+){2}|teams)|orgs\/[^\/]+|orgs\/[^\/]+\/(repos|issues|members|events|teams)|teams\/[^\/]+|teams\/[^\/]+\/(members(\/[^\/]+)?|memberships\/[^\/]+|repos|repos(\/[^\/]+){2})|users\/[^\/]+|users\/[^\/]+\/(repos|orgs|gists|followers|following(\/[^\/]+){0,2}|keys|starred|received_events(\/public)?|events(\/public)?|events\/orgs\/[^\/]+)|search\/(repositories|issues|users|code)|gists\/(public|starred|([a-f0-9]{20}|[0-9]+)|([a-f0-9]{20}|[0-9]+)\/forks|([a-f0-9]{20}|[0-9]+)\/comments(\/[0-9]+)?|([a-f0-9]{20}|[0-9]+)\/star)|repos(\/[^\/]+){2}|repos(\/[^\/]+){2}\/(readme|tarball(\/[^\/]+)?|zipball(\/[^\/]+)?|compare\/([^\.{3}]+)\.{3}([^\.{3}]+)|deployments(\/[0-9]+)?|deployments\/[0-9]+\/statuses(\/[0-9]+)?|hooks|hooks\/[^\/]+|hooks\/[^\/]+\/tests|assignees|languages|teams|tags|branches(\/[^\/]+){0,2}|contributors|subscribers|subscription|stargazers|comments(\/[0-9]+)?|downloads(\/[0-9]+)?|forks|milestones|milestones\/[0-9]+|milestones\/[0-9]+\/labels|labels(\/[^\/]+)?|releases|releases\/([0-9]+)|releases\/([0-9]+)\/assets|releases\/latest|releases\/tags\/([^\/]+)|releases\/assets\/([0-9]+)|events|notifications|merges|statuses\/[a-f0-9]{40}|pages|pages\/builds|pages\/builds\/latest|commits|commits\/[a-f0-9]{40}|commits\/[a-f0-9]{40}\/(comments|status|statuses)?|contents\/|contents(\/[^\/]+)*|collaborators(\/[^\/]+)?|(issues|pulls)|(issues|pulls)\/(events|events\/[0-9]+|comments(\/[0-9]+)?|[0-9]+|[0-9]+\/events|[0-9]+\/comments|[0-9]+\/labels(\/[^\/]+)?)|pulls\/[0-9]+\/(files|commits|merge)|git\/(refs|refs\/(.+|heads(\/[^\/]+)?|tags(\/[^\/]+)?)|trees(\/[^\/]+)?|blobs(\/[a-f0-9]{40}$)?|commits(\/[a-f0-9]{40}$)?)|stats\/(contributors|commit_activity|code_frequency|participation|punch_card))|licenses|licenses\/([^\/]+)|authorizations|authorizations\/((\d+)|clients\/([^\/]{20})|clients\/([^\/]{20})\/([^\/]+))|applications\/([^\/]{20})\/tokens|applications\/([^\/]{20})\/tokens\/([^\/]+)|enterprise\/(settings\/license|stats\/(issues|hooks|milestones|orgs|comments|pages|users|gists|pulls|repos|all))|staff\/indexing_jobs|users\/[^\/]+\/(site_admin|suspended)|setup\/api\/(start|upgrade|configcheck|configure|settings(authorized-keys)?|maintenance))(\?.*)?$/;
    
    
    /***/ },
    /* 27 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var Authorization, base64encode;
    
    	base64encode = __webpack_require__(28);
    
    	module.exports = new (Authorization = (function() {
    	  function Authorization() {}
    
    	  Authorization.prototype.requestMiddlewareAsync = function(input, cb) {
    	    var auth, headers, password, ref, token, username;
    	    if (input.headers == null) {
    	      input.headers = {};
    	    }
    	    headers = input.headers, (ref = input.clientOptions, token = ref.token, username = ref.username, password = ref.password);
    	    if (token || (username && password)) {
    	      if (token) {
    	        auth = "token " + token;
    	      } else {
    	        auth = 'Basic ' + base64encode(username + ":" + password);
    	      }
    	      input.headers['Authorization'] = auth;
    	    }
    	    return cb(null, input);
    	  };
    
    	  return Authorization;
    
    	})());
    
    
    /***/ },
    /* 28 */
    /***/ function(module, exports) {
    
    	/* WEBPACK VAR INJECTION */(function(global) {var base64encode;
    
    	if (typeof window !== "undefined" && window !== null) {
    	  base64encode = window.btoa;
    	} else if (typeof global !== "undefined" && global !== null ? global['Buffer'] : void 0) {
    	  base64encode = function(str) {
    	    var buffer;
    	    buffer = new global['Buffer'](str, 'binary');
    	    return buffer.toString('base64');
    	  };
    	} else {
    	  throw new Error('Native btoa function or Buffer is missing');
    	}
    
    	module.exports = base64encode;
    
    	/* WEBPACK VAR INJECTION */}.call(exports, (function() { return this; }())))
    
    /***/ },
    /* 29 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var DEFAULT_HEADER, PREVIEW_HEADERS, PreviewApis;
    
    	PREVIEW_HEADERS = __webpack_require__(30);
    
    	DEFAULT_HEADER = function(url) {
    	  var key, val;
    	  for (key in PREVIEW_HEADERS) {
    	    val = PREVIEW_HEADERS[key];
    	    if (val.test(url)) {
    	      return key;
    	    }
    	  }
    	};
    
    	module.exports = new (PreviewApis = (function() {
    	  function PreviewApis() {}
    
    	  PreviewApis.prototype.requestMiddlewareAsync = function(input, cb) {
    	    var acceptHeader, path;
    	    path = input.path;
    	    acceptHeader = DEFAULT_HEADER(path);
    	    if (acceptHeader) {
    	      input.headers['Accept'] = acceptHeader;
    	    }
    	    return cb(null, input);
    	  };
    
    	  return PreviewApis;
    
    	})());
    
    
    /***/ },
    /* 30 */
    /***/ function(module, exports) {
    
    	module.exports = {
    	  'application/vnd.github.drax-preview+json': /^(https?:\/\/[^\/]+)?(\/api\/v3)?(\/licenses|\/licenses\/([^\/]+)|\/repos\/([^\/]+)\/([^\/]+))$/,
    	  'application/vnd.github.v3.star+json': /^(https?:\/\/[^\/]+)?(\/api\/v3)?\/users\/([^\/]+)\/starred$/
    	};
    
    
    /***/ },
    /* 31 */
    /***/ function(module, exports) {
    
    	var UsePostInsteadOfPatch;
    
    	module.exports = new (UsePostInsteadOfPatch = (function() {
    	  function UsePostInsteadOfPatch() {}
    
    	  UsePostInsteadOfPatch.prototype.requestMiddlewareAsync = function(input, cb) {
    	    var method, ref, usePostInsteadOfPatch;
    	    (ref = input.clientOptions, usePostInsteadOfPatch = ref.usePostInsteadOfPatch), method = input.method;
    	    if (usePostInsteadOfPatch && method === 'PATCH') {
    	      input.method = 'POST';
    	    }
    	    return cb(null, input);
    	  };
    
    	  return UsePostInsteadOfPatch;
    
    	})());
    
    
    /***/ },
    /* 32 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var FetchAll, fetchNextPage, getMore, pushAll, toQueryString;
    
    	toQueryString = __webpack_require__(11);
    
    	pushAll = function(target, source) {
    	  if (!Array.isArray(source)) {
    	    throw new Error('Octokat Error: Calling fetchAll on a request that does not yield an array');
    	  }
    	  return target.push.apply(target, source);
    	};
    
    	getMore = function(fetchable, requester, acc, cb) {
    	  var doStuff;
    	  doStuff = function(err, results) {
    	    if (err) {
    	      return cb(err);
    	    }
    	    pushAll(acc, results.items);
    	    return getMore(results, requester, acc, cb);
    	  };
    	  if (!fetchNextPage(fetchable, requester, doStuff)) {
    	    return cb(null, acc);
    	  }
    	};
    
    	fetchNextPage = function(obj, requester, cb) {
    	  if (typeof obj.next_page_url === 'string') {
    	    requester.request('GET', obj.next_page, null, null, cb);
    	    return true;
    	  } else if (obj.next_page) {
    	    obj.next_page.fetch(cb);
    	    return true;
    	  } else if (typeof obj.nextPageUrl === 'string') {
    	    requester.request('GET', obj.nextPageUrl, null, null, cb);
    	    return true;
    	  } else if (obj.nextPage) {
    	    obj.nextPage.fetch(cb);
    	    return true;
    	  } else {
    	    return false;
    	  }
    	};
    
    	module.exports = new (FetchAll = (function() {
    	  function FetchAll() {}
    
    	  FetchAll.prototype.asyncVerbs = {
    	    fetchAll: function(requester, path) {
    	      return function(cb, query) {
    	        return requester.request('GET', "" + path + (toQueryString(query)), null, null, function(err, results) {
    	          var acc;
    	          if (err) {
    	            return cb(err);
    	          }
    	          acc = [];
    	          pushAll(acc, results.items);
    	          return getMore(results, requester, acc, cb);
    	        });
    	      };
    	    }
    	  };
    
    	  return FetchAll;
    
    	})());
    
    
    /***/ },
    /* 33 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var ReadBinary, toQueryString;
    
    	toQueryString = __webpack_require__(11);
    
    	module.exports = new (ReadBinary = (function() {
    	  function ReadBinary() {}
    
    	  ReadBinary.prototype.verbs = {
    	    readBinary: function(path, query) {
    	      return {
    	        method: 'GET',
    	        path: "" + path + (toQueryString(query)),
    	        options: {
    	          isRaw: true,
    	          isBase64: true
    	        }
    	      };
    	    }
    	  };
    
    	  ReadBinary.prototype.requestMiddlewareAsync = function(input, cb) {
    	    var isBase64, options;
    	    options = input.options;
    	    if (options) {
    	      isBase64 = options.isBase64;
    	      if (isBase64) {
    	        input.headers['Accept'] = 'application/vnd.github.raw';
    	        input.mimeType = 'text/plain; charset=x-user-defined';
    	      }
    	    }
    	    return cb(null, input);
    	  };
    
    	  ReadBinary.prototype.responseMiddlewareAsync = function(input, cb) {
    	    var converted, data, i, isBase64, j, options, ref;
    	    options = input.options, data = input.data;
    	    if (options) {
    	      isBase64 = options.isBase64;
    	      if (isBase64) {
    	        converted = '';
    	        for (i = j = 0, ref = data.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
    	          converted += String.fromCharCode(data.charCodeAt(i) & 0xff);
    	        }
    	        input.data = converted;
    	      }
    	    }
    	    return cb(null, input);
    	  };
    
    	  return ReadBinary;
    
    	})());
    
    
    /***/ },
    /* 34 */
    /***/ function(module, exports) {
    
    	var Pagination;
    
    	module.exports = new (Pagination = (function() {
    	  function Pagination() {}
    
    	  Pagination.prototype.responseMiddlewareAsync = function(input, cb) {
    	    var data, discard, href, i, jqXHR, len, links, part, ref, ref1, rel;
    	    jqXHR = input.jqXHR, data = input.data;
    	    if (!jqXHR) {
    	      return cb(null, input);
    	    }
    	    if (Array.isArray(data)) {
    	      data = {
    	        items: data.slice(0)
    	      };
    	      links = jqXHR.getResponseHeader('Link');
    	      ref = (links != null ? links.split(',') : void 0) || [];
    	      for (i = 0, len = ref.length; i < len; i++) {
    	        part = ref[i];
    	        ref1 = part.match(/<([^>]+)>;\ rel="([^"]+)"/), discard = ref1[0], href = ref1[1], rel = ref1[2];
    	        data[rel + "_page_url"] = href;
    	      }
    	      input.data = data;
    	    }
    	    return cb(null, input);
    	  };
    
    	  return Pagination;
    
    	})());
    
    
    /***/ },
    /* 35 */
    /***/ function(module, exports) {
    
    	var CacheHandler;
    
    	module.exports = new (CacheHandler = (function() {
    	  function CacheHandler() {
    	    this._cachedETags = {};
    	  }
    
    	  CacheHandler.prototype.get = function(method, path) {
    	    return this._cachedETags[method + " " + path];
    	  };
    
    	  CacheHandler.prototype.add = function(method, path, eTag, data, status) {
    	    return this._cachedETags[method + " " + path] = {
    	      eTag: eTag,
    	      data: data,
    	      status: status
    	    };
    	  };
    
    	  CacheHandler.prototype.requestMiddlewareAsync = function(input, cb) {
    	    var cacheHandler, clientOptions, method, path;
    	    clientOptions = input.clientOptions, method = input.method, path = input.path;
    	    if (input.headers == null) {
    	      input.headers = {};
    	    }
    	    cacheHandler = clientOptions.cacheHandler || this;
    	    if (cacheHandler.get(method, path)) {
    	      input.headers['If-None-Match'] = cacheHandler.get(method, path).eTag;
    	    } else {
              /* disabled by iap 
    	      input.headers['If-Modified-Since'] = 'Thu, 01 Jan 1970 00:00:00 GMT';
              */
    	    }
    	    return cb(null, input);
    	  };
    
    	  CacheHandler.prototype.responseMiddlewareAsync = function(input, cb) {
    	    var cacheHandler, clientOptions, data, eTag, jqXHR, method, path, ref, request, status;
    	    clientOptions = input.clientOptions, request = input.request, status = input.status, jqXHR = input.jqXHR, data = input.data;
    	    if (!jqXHR) {
    	      return cb(null, input);
    	    }
    	    if (jqXHR) {
    	      method = request.method, path = request.path;
    	      cacheHandler = clientOptions.cacheHandler || this;
    	      if (status === 304 || status === 0) {
    	        ref = cacheHandler.get(method, path);
    	        if (ref) {
    	          data = ref.data, status = ref.status, eTag = ref.eTag;
    	          data.__IS_CACHED = eTag || true;
    	        } else {
    	          throw new Error('ERROR: Bug in Octokat cacheHandler. It had an eTag but not the cached response');
    	        }
    	      } else {
    	        if (method === 'GET' && jqXHR.getResponseHeader('ETag')) {
    	          eTag = jqXHR.getResponseHeader('ETag');
    	          cacheHandler.add(method, path, eTag, data, jqXHR.status);
    	        }
    	      }
    	      input.data = data;
    	      input.status = status;
    	      return cb(null, input);
    	    }
    	  };
    
    	  return CacheHandler;
    
    	})());
    
    
    /***/ },
    /* 36 */
    /***/ function(module, exports, __webpack_require__) {
    
    	var CamelCase, plus;
    
    	plus = __webpack_require__(4);
    
    	module.exports = new (CamelCase = (function() {
    	  function CamelCase() {}
    
    	  CamelCase.prototype.responseMiddlewareAsync = function(input, cb) {
    	    var data;
    	    data = input.data;
    	    data = this.replace(data);
    	    input.data = data;
    	    return cb(null, input);
    	  };
    
    	  CamelCase.prototype.replace = function(data) {
    	    if (Array.isArray(data)) {
    	      return this._replaceArray(data);
    	    } else if (typeof data === 'function') {
    	      return data;
    	    } else if (data instanceof Date) {
    	      return data;
    	    } else if (data === Object(data)) {
    	      return this._replaceObject(data);
    	    } else {
    	      return data;
    	    }
    	  };
    
    	  CamelCase.prototype._replaceObject = function(orig) {
    	    var acc, i, key, len, ref, value;
    	    acc = {};
    	    ref = Object.keys(orig);
    	    for (i = 0, len = ref.length; i < len; i++) {
    	      key = ref[i];
    	      value = orig[key];
    	      this._replaceKeyValue(acc, key, value);
    	    }
    	    return acc;
    	  };
    
    	  CamelCase.prototype._replaceArray = function(orig) {
    	    var arr, i, item, key, len, ref, value;
    	    arr = (function() {
    	      var i, len, results;
    	      results = [];
    	      for (i = 0, len = orig.length; i < len; i++) {
    	        item = orig[i];
    	        results.push(this.replace(item));
    	      }
    	      return results;
    	    }).call(this);
    	    ref = Object.keys(orig);
    	    for (i = 0, len = ref.length; i < len; i++) {
    	      key = ref[i];
    	      value = orig[key];
    	      this._replaceKeyValue(arr, key, value);
    	    }
    	    return arr;
    	  };
    
    	  CamelCase.prototype._replaceKeyValue = function(acc, key, value) {
    	    return acc[plus.camelize(key)] = this.replace(value);
    	  };
    
    	  return CamelCase;
    
    	})());
    
    
    /***/ }
    /******/ ])
    });
    ;
    </script>
    <script language="javascript">
    "use strict";var sjcl={cipher:{},hash:{},mode:{},misc:{},codec:{},exception:{corrupt:function(a){this.toString=function(){return"CORRUPT: "+this.message};this.message=a},invalid:function(a){this.toString=function(){return"INVALID: "+this.message};this.message=a},bug:function(a){this.toString=function(){return"BUG: "+this.message};this.message=a},notReady:function(a){this.toString=function(){return"NOT READY: "+this.message};this.message=a}}};
    sjcl.cipher.aes=function(a){this.h[0][0][0]||this.z();var b,c,d,e,f=this.h[0][4],g=this.h[1];b=a.length;var h=1;if(b!==4&&b!==6&&b!==8)throw new sjcl.exception.invalid("invalid aes key size");this.a=[d=a.slice(0),e=[]];for(a=b;a<4*b+28;a++){c=d[a-1];if(a%b===0||b===8&&a%b===4){c=f[c>>>24]<<24^f[c>>16&255]<<16^f[c>>8&255]<<8^f[c&255];if(a%b===0){c=c<<8^c>>>24^h<<24;h=h<<1^(h>>7)*283}}d[a]=d[a-b]^c}for(b=0;a;b++,a--){c=d[b&3?a:a-4];e[b]=a<=4||b<4?c:g[0][f[c>>>24]]^g[1][f[c>>16&255]]^g[2][f[c>>8&255]]^
    g[3][f[c&255]]}};
    sjcl.cipher.aes.prototype={encrypt:function(a){return this.I(a,0)},decrypt:function(a){return this.I(a,1)},h:[[[],[],[],[],[]],[[],[],[],[],[]]],z:function(){var a=this.h[0],b=this.h[1],c=a[4],d=b[4],e,f,g,h=[],i=[],k,j,l,m;for(e=0;e<0x100;e++)i[(h[e]=e<<1^(e>>7)*283)^e]=e;for(f=g=0;!c[f];f^=k||1,g=i[g]||1){l=g^g<<1^g<<2^g<<3^g<<4;l=l>>8^l&255^99;c[f]=l;d[l]=f;j=h[e=h[k=h[f]]];m=j*0x1010101^e*0x10001^k*0x101^f*0x1010100;j=h[l]*0x101^l*0x1010100;for(e=0;e<4;e++){a[e][f]=j=j<<24^j>>>8;b[e][l]=m=m<<24^m>>>8}}for(e=
    0;e<5;e++){a[e]=a[e].slice(0);b[e]=b[e].slice(0)}},I:function(a,b){if(a.length!==4)throw new sjcl.exception.invalid("invalid aes block size");var c=this.a[b],d=a[0]^c[0],e=a[b?3:1]^c[1],f=a[2]^c[2];a=a[b?1:3]^c[3];var g,h,i,k=c.length/4-2,j,l=4,m=[0,0,0,0];g=this.h[b];var n=g[0],o=g[1],p=g[2],q=g[3],r=g[4];for(j=0;j<k;j++){g=n[d>>>24]^o[e>>16&255]^p[f>>8&255]^q[a&255]^c[l];h=n[e>>>24]^o[f>>16&255]^p[a>>8&255]^q[d&255]^c[l+1];i=n[f>>>24]^o[a>>16&255]^p[d>>8&255]^q[e&255]^c[l+2];a=n[a>>>24]^o[d>>16&
    255]^p[e>>8&255]^q[f&255]^c[l+3];l+=4;d=g;e=h;f=i}for(j=0;j<4;j++){m[b?3&-j:j]=r[d>>>24]<<24^r[e>>16&255]<<16^r[f>>8&255]<<8^r[a&255]^c[l++];g=d;d=e;e=f;f=a;a=g}return m}};
    sjcl.bitArray={bitSlice:function(a,b,c){a=sjcl.bitArray.P(a.slice(b/32),32-(b&31)).slice(1);return c===undefined?a:sjcl.bitArray.clamp(a,c-b)},concat:function(a,b){if(a.length===0||b.length===0)return a.concat(b);var c=a[a.length-1],d=sjcl.bitArray.getPartial(c);return d===32?a.concat(b):sjcl.bitArray.P(b,d,c|0,a.slice(0,a.length-1))},bitLength:function(a){var b=a.length;if(b===0)return 0;return(b-1)*32+sjcl.bitArray.getPartial(a[b-1])},clamp:function(a,b){if(a.length*32<b)return a;a=a.slice(0,Math.ceil(b/
    32));var c=a.length;b&=31;if(c>0&&b)a[c-1]=sjcl.bitArray.partial(b,a[c-1]&2147483648>>b-1,1);return a},partial:function(a,b,c){if(a===32)return b;return(c?b|0:b<<32-a)+a*0x10000000000},getPartial:function(a){return Math.round(a/0x10000000000)||32},equal:function(a,b){if(sjcl.bitArray.bitLength(a)!==sjcl.bitArray.bitLength(b))return false;var c=0,d;for(d=0;d<a.length;d++)c|=a[d]^b[d];return c===0},P:function(a,b,c,d){var e;e=0;if(d===undefined)d=[];for(;b>=32;b-=32){d.push(c);c=0}if(b===0)return d.concat(a);
    for(e=0;e<a.length;e++){d.push(c|a[e]>>>b);c=a[e]<<32-b}e=a.length?a[a.length-1]:0;a=sjcl.bitArray.getPartial(e);d.push(sjcl.bitArray.partial(b+a&31,b+a>32?c:d.pop(),1));return d},k:function(a,b){return[a[0]^b[0],a[1]^b[1],a[2]^b[2],a[3]^b[3]]}};
    sjcl.codec.utf8String={fromBits:function(a){var b="",c=sjcl.bitArray.bitLength(a),d,e;for(d=0;d<c/8;d++){if((d&3)===0)e=a[d/4];b+=String.fromCharCode(e>>>24);e<<=8}return decodeURIComponent(escape(b))},toBits:function(a){a=unescape(encodeURIComponent(a));var b=[],c,d=0;for(c=0;c<a.length;c++){d=d<<8|a.charCodeAt(c);if((c&3)===3){b.push(d);d=0}}c&3&&b.push(sjcl.bitArray.partial(8*(c&3),d));return b}};
    sjcl.codec.hex={fromBits:function(a){var b="",c;for(c=0;c<a.length;c++)b+=((a[c]|0)+0xf00000000000).toString(16).substr(4);return b.substr(0,sjcl.bitArray.bitLength(a)/4)},toBits:function(a){var b,c=[],d;a=a.replace(/\s|0x/g,"");d=a.length;a+="00000000";for(b=0;b<a.length;b+=8)c.push(parseInt(a.substr(b,8),16)^0);return sjcl.bitArray.clamp(c,d*4)}};
    sjcl.codec.base64={F:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",fromBits:function(a,b){var c="",d,e=0,f=sjcl.codec.base64.F,g=0,h=sjcl.bitArray.bitLength(a);for(d=0;c.length*6<h;){c+=f.charAt((g^a[d]>>>e)>>>26);if(e<6){g=a[d]<<6-e;e+=26;d++}else{g<<=6;e-=6}}for(;c.length&3&&!b;)c+="=";return c},toBits:function(a){a=a.replace(/\s|=/g,"");var b=[],c,d=0,e=sjcl.codec.base64.F,f=0,g;for(c=0;c<a.length;c++){g=e.indexOf(a.charAt(c));if(g<0)throw new sjcl.exception.invalid("this isn't base64!");
    if(d>26){d-=26;b.push(f^g>>>d);f=g<<32-d}else{d+=6;f^=g<<32-d}}d&56&&b.push(sjcl.bitArray.partial(d&56,f,1));return b}};sjcl.hash.sha256=function(a){this.a[0]||this.z();if(a){this.n=a.n.slice(0);this.i=a.i.slice(0);this.e=a.e}else this.reset()};sjcl.hash.sha256.hash=function(a){return(new sjcl.hash.sha256).update(a).finalize()};
    sjcl.hash.sha256.prototype={blockSize:512,reset:function(){this.n=this.N.slice(0);this.i=[];this.e=0;return this},update:function(a){if(typeof a==="string")a=sjcl.codec.utf8String.toBits(a);var b,c=this.i=sjcl.bitArray.concat(this.i,a);b=this.e;a=this.e=b+sjcl.bitArray.bitLength(a);for(b=512+b&-512;b<=a;b+=512)this.D(c.splice(0,16));return this},finalize:function(){var a,b=this.i,c=this.n;b=sjcl.bitArray.concat(b,[sjcl.bitArray.partial(1,1)]);for(a=b.length+2;a&15;a++)b.push(0);b.push(Math.floor(this.e/
    4294967296));for(b.push(this.e|0);b.length;)this.D(b.splice(0,16));this.reset();return c},N:[],a:[],z:function(){function a(e){return(e-Math.floor(e))*0x100000000|0}var b=0,c=2,d;a:for(;b<64;c++){for(d=2;d*d<=c;d++)if(c%d===0)continue a;if(b<8)this.N[b]=a(Math.pow(c,0.5));this.a[b]=a(Math.pow(c,1/3));b++}},D:function(a){var b,c,d=a.slice(0),e=this.n,f=this.a,g=e[0],h=e[1],i=e[2],k=e[3],j=e[4],l=e[5],m=e[6],n=e[7];for(a=0;a<64;a++){if(a<16)b=d[a];else{b=d[a+1&15];c=d[a+14&15];b=d[a&15]=(b>>>7^b>>>18^
    b>>>3^b<<25^b<<14)+(c>>>17^c>>>19^c>>>10^c<<15^c<<13)+d[a&15]+d[a+9&15]|0}b=b+n+(j>>>6^j>>>11^j>>>25^j<<26^j<<21^j<<7)+(m^j&(l^m))+f[a];n=m;m=l;l=j;j=k+b|0;k=i;i=h;h=g;g=b+(h&i^k&(h^i))+(h>>>2^h>>>13^h>>>22^h<<30^h<<19^h<<10)|0}e[0]=e[0]+g|0;e[1]=e[1]+h|0;e[2]=e[2]+i|0;e[3]=e[3]+k|0;e[4]=e[4]+j|0;e[5]=e[5]+l|0;e[6]=e[6]+m|0;e[7]=e[7]+n|0}};
    sjcl.mode.ccm={name:"ccm",encrypt:function(a,b,c,d,e){var f,g=b.slice(0),h=sjcl.bitArray,i=h.bitLength(c)/8,k=h.bitLength(g)/8;e=e||64;d=d||[];if(i<7)throw new sjcl.exception.invalid("ccm: iv must be at least 7 bytes");for(f=2;f<4&&k>>>8*f;f++);if(f<15-i)f=15-i;c=h.clamp(c,8*(15-f));b=sjcl.mode.ccm.H(a,b,c,d,e,f);g=sjcl.mode.ccm.J(a,g,c,b,e,f);return h.concat(g.data,g.tag)},decrypt:function(a,b,c,d,e){e=e||64;d=d||[];var f=sjcl.bitArray,g=f.bitLength(c)/8,h=f.bitLength(b),i=f.clamp(b,h-e),k=f.bitSlice(b,
    h-e);h=(h-e)/8;if(g<7)throw new sjcl.exception.invalid("ccm: iv must be at least 7 bytes");for(b=2;b<4&&h>>>8*b;b++);if(b<15-g)b=15-g;c=f.clamp(c,8*(15-b));i=sjcl.mode.ccm.J(a,i,c,k,e,b);a=sjcl.mode.ccm.H(a,i.data,c,d,e,b);if(!f.equal(i.tag,a))throw new sjcl.exception.corrupt("ccm: tag doesn't match");return i.data},H:function(a,b,c,d,e,f){var g=[],h=sjcl.bitArray,i=h.k;e/=8;if(e%2||e<4||e>16)throw new sjcl.exception.invalid("ccm: invalid tag length");if(d.length>0xffffffff||b.length>0xffffffff)throw new sjcl.exception.bug("ccm: can't deal with 4GiB or more data");
    f=[h.partial(8,(d.length?64:0)|e-2<<2|f-1)];f=h.concat(f,c);f[3]|=h.bitLength(b)/8;f=a.encrypt(f);if(d.length){c=h.bitLength(d)/8;if(c<=65279)g=[h.partial(16,c)];else if(c<=0xffffffff)g=h.concat([h.partial(16,65534)],[c]);g=h.concat(g,d);for(d=0;d<g.length;d+=4)f=a.encrypt(i(f,g.slice(d,d+4).concat([0,0,0])))}for(d=0;d<b.length;d+=4)f=a.encrypt(i(f,b.slice(d,d+4).concat([0,0,0])));return h.clamp(f,e*8)},J:function(a,b,c,d,e,f){var g,h=sjcl.bitArray;g=h.k;var i=b.length,k=h.bitLength(b);c=h.concat([h.partial(8,
    f-1)],c).concat([0,0,0]).slice(0,4);d=h.bitSlice(g(d,a.encrypt(c)),0,e);if(!i)return{tag:d,data:[]};for(g=0;g<i;g+=4){c[3]++;e=a.encrypt(c);b[g]^=e[0];b[g+1]^=e[1];b[g+2]^=e[2];b[g+3]^=e[3]}return{tag:d,data:h.clamp(b,k)}}};
    sjcl.mode.ocb2={name:"ocb2",encrypt:function(a,b,c,d,e,f){if(sjcl.bitArray.bitLength(c)!==128)throw new sjcl.exception.invalid("ocb iv must be 128 bits");var g,h=sjcl.mode.ocb2.B,i=sjcl.bitArray,k=i.k,j=[0,0,0,0];c=h(a.encrypt(c));var l,m=[];d=d||[];e=e||64;for(g=0;g+4<b.length;g+=4){l=b.slice(g,g+4);j=k(j,l);m=m.concat(k(c,a.encrypt(k(c,l))));c=h(c)}l=b.slice(g);b=i.bitLength(l);g=a.encrypt(k(c,[0,0,0,b]));l=i.clamp(k(l.concat([0,0,0]),g),b);j=k(j,k(l.concat([0,0,0]),g));j=a.encrypt(k(j,k(c,h(c))));
    if(d.length)j=k(j,f?d:sjcl.mode.ocb2.pmac(a,d));return m.concat(i.concat(l,i.clamp(j,e)))},decrypt:function(a,b,c,d,e,f){if(sjcl.bitArray.bitLength(c)!==128)throw new sjcl.exception.invalid("ocb iv must be 128 bits");e=e||64;var g=sjcl.mode.ocb2.B,h=sjcl.bitArray,i=h.k,k=[0,0,0,0],j=g(a.encrypt(c)),l,m,n=sjcl.bitArray.bitLength(b)-e,o=[];d=d||[];for(c=0;c+4<n/32;c+=4){l=i(j,a.decrypt(i(j,b.slice(c,c+4))));k=i(k,l);o=o.concat(l);j=g(j)}m=n-c*32;l=a.encrypt(i(j,[0,0,0,m]));l=i(l,h.clamp(b.slice(c),
    m).concat([0,0,0]));k=i(k,l);k=a.encrypt(i(k,i(j,g(j))));if(d.length)k=i(k,f?d:sjcl.mode.ocb2.pmac(a,d));if(!h.equal(h.clamp(k,e),h.bitSlice(b,n)))throw new sjcl.exception.corrupt("ocb: tag doesn't match");return o.concat(h.clamp(l,m))},pmac:function(a,b){var c,d=sjcl.mode.ocb2.B,e=sjcl.bitArray,f=e.k,g=[0,0,0,0],h=a.encrypt([0,0,0,0]);h=f(h,d(d(h)));for(c=0;c+4<b.length;c+=4){h=d(h);g=f(g,a.encrypt(f(h,b.slice(c,c+4))))}b=b.slice(c);if(e.bitLength(b)<128){h=f(h,d(h));b=e.concat(b,[2147483648|0,0,
    0,0])}g=f(g,b);return a.encrypt(f(d(f(h,d(h))),g))},B:function(a){return[a[0]<<1^a[1]>>>31,a[1]<<1^a[2]>>>31,a[2]<<1^a[3]>>>31,a[3]<<1^(a[0]>>>31)*135]}};sjcl.misc.hmac=function(a,b){this.M=b=b||sjcl.hash.sha256;var c=[[],[]],d=b.prototype.blockSize/32;this.l=[new b,new b];if(a.length>d)a=b.hash(a);for(b=0;b<d;b++){c[0][b]=a[b]^909522486;c[1][b]=a[b]^1549556828}this.l[0].update(c[0]);this.l[1].update(c[1])};
    sjcl.misc.hmac.prototype.encrypt=sjcl.misc.hmac.prototype.mac=function(a){a=(new this.M(this.l[0])).update(a).finalize();return(new this.M(this.l[1])).update(a).finalize()};
    sjcl.misc.pbkdf2=function(a,b,c,d,e){c=c||1E3;if(d<0||c<0)throw sjcl.exception.invalid("invalid params to pbkdf2");if(typeof a==="string")a=sjcl.codec.utf8String.toBits(a);e=e||sjcl.misc.hmac;a=new e(a);var f,g,h,i,k=[],j=sjcl.bitArray;for(i=1;32*k.length<(d||1);i++){e=f=a.encrypt(j.concat(b,[i]));for(g=1;g<c;g++){f=a.encrypt(f);for(h=0;h<f.length;h++)e[h]^=f[h]}k=k.concat(e)}if(d)k=j.clamp(k,d);return k};
    sjcl.random={randomWords:function(a,b){var c=[];b=this.isReady(b);var d;if(b===0)throw new sjcl.exception.notReady("generator isn't seeded");else b&2&&this.U(!(b&1));for(b=0;b<a;b+=4){(b+1)%0x10000===0&&this.L();d=this.w();c.push(d[0],d[1],d[2],d[3])}this.L();return c.slice(0,a)},setDefaultParanoia:function(a){this.t=a},addEntropy:function(a,b,c){c=c||"user";var d,e,f=(new Date).valueOf(),g=this.q[c],h=this.isReady(),i=0;d=this.G[c];if(d===undefined)d=this.G[c]=this.R++;if(g===undefined)g=this.q[c]=
    0;this.q[c]=(this.q[c]+1)%this.b.length;switch(typeof a){case "number":if(b===undefined)b=1;this.b[g].update([d,this.u++,1,b,f,1,a|0]);break;case "object":c=Object.prototype.toString.call(a);if(c==="[object Uint32Array]"){e=[];for(c=0;c<a.length;c++)e.push(a[c]);a=e}else{if(c!=="[object Array]")i=1;for(c=0;c<a.length&&!i;c++)if(typeof a[c]!="number")i=1}if(!i){if(b===undefined)for(c=b=0;c<a.length;c++)for(e=a[c];e>0;){b++;e>>>=1}this.b[g].update([d,this.u++,2,b,f,a.length].concat(a))}break;case "string":if(b===
    undefined)b=a.length;this.b[g].update([d,this.u++,3,b,f,a.length]);this.b[g].update(a);break;default:i=1}if(i)throw new sjcl.exception.bug("random: addEntropy only supports number, array of numbers or string");this.j[g]+=b;this.f+=b;if(h===0){this.isReady()!==0&&this.K("seeded",Math.max(this.g,this.f));this.K("progress",this.getProgress())}},isReady:function(a){a=this.C[a!==undefined?a:this.t];return this.g&&this.g>=a?this.j[0]>80&&(new Date).valueOf()>this.O?3:1:this.f>=a?2:0},getProgress:function(a){a=
    this.C[a?a:this.t];return this.g>=a?1:this.f>a?1:this.f/a},startCollectors:function(){if(!this.m){if(window.addEventListener){window.addEventListener("load",this.o,false);window.addEventListener("mousemove",this.p,false)}else if(document.attachEvent){document.attachEvent("onload",this.o);document.attachEvent("onmousemove",this.p)}else throw new sjcl.exception.bug("can't attach event");this.m=true}},stopCollectors:function(){if(this.m){if(window.removeEventListener){window.removeEventListener("load",
    this.o,false);window.removeEventListener("mousemove",this.p,false)}else if(window.detachEvent){window.detachEvent("onload",this.o);window.detachEvent("onmousemove",this.p)}this.m=false}},addEventListener:function(a,b){this.r[a][this.Q++]=b},removeEventListener:function(a,b){var c;a=this.r[a];var d=[];for(c in a)a.hasOwnProperty(c)&&a[c]===b&&d.push(c);for(b=0;b<d.length;b++){c=d[b];delete a[c]}},b:[new sjcl.hash.sha256],j:[0],A:0,q:{},u:0,G:{},R:0,g:0,f:0,O:0,a:[0,0,0,0,0,0,0,0],d:[0,0,0,0],s:undefined,
    t:6,m:false,r:{progress:{},seeded:{}},Q:0,C:[0,48,64,96,128,192,0x100,384,512,768,1024],w:function(){for(var a=0;a<4;a++){this.d[a]=this.d[a]+1|0;if(this.d[a])break}return this.s.encrypt(this.d)},L:function(){this.a=this.w().concat(this.w());this.s=new sjcl.cipher.aes(this.a)},T:function(a){this.a=sjcl.hash.sha256.hash(this.a.concat(a));this.s=new sjcl.cipher.aes(this.a);for(a=0;a<4;a++){this.d[a]=this.d[a]+1|0;if(this.d[a])break}},U:function(a){var b=[],c=0,d;this.O=b[0]=(new Date).valueOf()+3E4;for(d=
    0;d<16;d++)b.push(Math.random()*0x100000000|0);for(d=0;d<this.b.length;d++){b=b.concat(this.b[d].finalize());c+=this.j[d];this.j[d]=0;if(!a&&this.A&1<<d)break}if(this.A>=1<<this.b.length){this.b.push(new sjcl.hash.sha256);this.j.push(0)}this.f-=c;if(c>this.g)this.g=c;this.A++;this.T(b)},p:function(a){sjcl.random.addEntropy([a.x||a.clientX||a.offsetX||0,a.y||a.clientY||a.offsetY||0],2,"mouse")},o:function(){sjcl.random.addEntropy((new Date).valueOf(),2,"loadtime")},K:function(a,b){var c;a=sjcl.random.r[a];
    var d=[];for(c in a)a.hasOwnProperty(c)&&d.push(a[c]);for(c=0;c<d.length;c++)d[c](b)}};try{var s=new Uint32Array(32);crypto.getRandomValues(s);sjcl.random.addEntropy(s,1024,"crypto['getRandomValues']")}catch(t){}
    sjcl.json={defaults:{v:1,iter:1E3,ks:128,ts:64,mode:"ccm",adata:"",cipher:"aes"},encrypt:function(a,b,c,d){c=c||{};d=d||{};var e=sjcl.json,f=e.c({iv:sjcl.random.randomWords(4,0)},e.defaults),g;e.c(f,c);c=f.adata;if(typeof f.salt==="string")f.salt=sjcl.codec.base64.toBits(f.salt);if(typeof f.iv==="string")f.iv=sjcl.codec.base64.toBits(f.iv);if(!sjcl.mode[f.mode]||!sjcl.cipher[f.cipher]||typeof a==="string"&&f.iter<=100||f.ts!==64&&f.ts!==96&&f.ts!==128||f.ks!==128&&f.ks!==192&&f.ks!==0x100||f.iv.length<
    2||f.iv.length>4)throw new sjcl.exception.invalid("json encrypt: invalid parameters");if(typeof a==="string"){g=sjcl.misc.cachedPbkdf2(a,f);a=g.key.slice(0,f.ks/32);f.salt=g.salt}if(typeof b==="string")b=sjcl.codec.utf8String.toBits(b);if(typeof c==="string")c=sjcl.codec.utf8String.toBits(c);g=new sjcl.cipher[f.cipher](a);e.c(d,f);d.key=a;f.ct=sjcl.mode[f.mode].encrypt(g,b,f.iv,c,f.ts);return e.encode(f)},decrypt:function(a,b,c,d){c=c||{};d=d||{};var e=sjcl.json;b=e.c(e.c(e.c({},e.defaults),e.decode(b)),
    c,true);var f;c=b.adata;if(typeof b.salt==="string")b.salt=sjcl.codec.base64.toBits(b.salt);if(typeof b.iv==="string")b.iv=sjcl.codec.base64.toBits(b.iv);if(!sjcl.mode[b.mode]||!sjcl.cipher[b.cipher]||typeof a==="string"&&b.iter<=100||b.ts!==64&&b.ts!==96&&b.ts!==128||b.ks!==128&&b.ks!==192&&b.ks!==0x100||!b.iv||b.iv.length<2||b.iv.length>4)throw new sjcl.exception.invalid("json decrypt: invalid parameters");if(typeof a==="string"){f=sjcl.misc.cachedPbkdf2(a,b);a=f.key.slice(0,b.ks/32);b.salt=f.salt}if(typeof c===
    "string")c=sjcl.codec.utf8String.toBits(c);f=new sjcl.cipher[b.cipher](a);c=sjcl.mode[b.mode].decrypt(f,b.ct,b.iv,c,b.ts);e.c(d,b);d.key=a;return sjcl.codec.utf8String.fromBits(c)},encode:function(a){var b,c="{",d="";for(b in a)if(a.hasOwnProperty(b)){if(!b.match(/^[a-z0-9]+$/i))throw new sjcl.exception.invalid("json encode: invalid property name");c+=d+'"'+b+'":';d=",";switch(typeof a[b]){case "number":case "boolean":c+=a[b];break;case "string":c+='"'+escape(a[b])+'"';break;case "object":c+='"'+
    sjcl.codec.base64.fromBits(a[b],1)+'"';break;default:throw new sjcl.exception.bug("json encode: unsupported type");}}return c+"}"},decode:function(a){a=a.replace(/\s/g,"");if(!a.match(/^\{.*\}$/))throw new sjcl.exception.invalid("json decode: this isn't json!");a=a.replace(/^\{|\}$/g,"").split(/,/);var b={},c,d;for(c=0;c<a.length;c++){if(!(d=a[c].match(/^(?:(["']?)([a-z][a-z0-9]*)\1):(?:(\d+)|"([a-z0-9+\/%*_.@=\-]*)")$/i)))throw new sjcl.exception.invalid("json decode: this isn't json!");b[d[2]]=
    d[3]?parseInt(d[3],10):d[2].match(/^(ct|salt|iv)$/)?sjcl.codec.base64.toBits(d[4]):unescape(d[4])}return b},c:function(a,b,c){if(a===undefined)a={};if(b===undefined)return a;var d;for(d in b)if(b.hasOwnProperty(d)){if(c&&a[d]!==undefined&&a[d]!==b[d])throw new sjcl.exception.invalid("required parameter overridden");a[d]=b[d]}return a},V:function(a,b){var c={},d;for(d=0;d<b.length;d++)if(a[b[d]]!==undefined)c[b[d]]=a[b[d]];return c}};sjcl.encrypt=sjcl.json.encrypt;sjcl.decrypt=sjcl.json.decrypt;
    sjcl.misc.S={};sjcl.misc.cachedPbkdf2=function(a,b){var c=sjcl.misc.S,d;b=b||{};d=b.iter||1E3;c=c[a]=c[a]||{};d=c[d]=c[d]||{firstSalt:b.salt&&b.salt.length?b.salt.slice(0):sjcl.random.randomWords(2,0)};c=b.salt===undefined?d.firstSalt:b.salt;d[c]=d[c]||sjcl.misc.pbkdf2(a,c,b.iter);return{key:d[c].slice(0),salt:c.slice(0)}};
    </script>
      </body>
    </html>
    
    
    

|

.. _h4f135c7124c273f414779321e1f5ff:

conversion.html
***************


.. code-block:: python
    :linenos:

    <!DOCTYPE html>
    <html>
      <head>
        <base target="_top">
        <link rel="stylesheet" href="https://ssl.gstatic.com/docs/script/css/add-ons.css">
    <style>
    .tab {
      position:relative;
      left:0;
      top:0;
      display:none;
     /* padding:5px 2px 0px 10px; */
    }
    .tab.active{
      display:block;
    }
    .tab-title{
      border:solid 1px #c0c0c0;
      display:inline-block;
      position:relative;
      padding:5px 8px;
      border-bottom:none;
      -webkit-border-top-left-radius: 2px;
      -webkit-border-top-right-radius: 2px;
      -moz-border-radius-topleft: 2px;
      -moz-border-radius-topright: 2px;
      border-top-left-radius: 2px;
      border-top-right-radius: 2px;
      cursor:pointer;
      text-align:center;
      width:24%;
      font-size:0.95em;
      white-space: nowrap;
      overflow-x: hidden;
      text-overflow: ellipsis;
      margin-bottom:-5px;
    }
    .tab-title.active,.tab-title.active:hover{
      top:1px;
      background-color:white;
      -webkit-box-shadow: none;
      -moz-box-shadow:    none;
      box-shadow:         none;
    }
    .tab-title:hover{
      background-color:#f0f0f0;  
      -webkit-box-shadow: 0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      -moz-box-shadow:    0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      box-shadow:         0px 0px 1px 0px rgba(50, 50, 50, 0.25);
    }
    .tab-title-bar {
      border-bottom:solid 1px #c0c0c0;
      margin-bottom:10px;
      padding:0px 10px;
    }
    .tab > .block{
        margin-top:30px  !important;
    }
    .tab > .block:first-child{
        margin-top:12px  !important;
    }
    .tab > .block > label:first-child {
      margin-bottom:5px;
      display:block;
    }
    
    button.small{
        min-width:35px;
        height:25px;
        margin-left:3px;
        margin-top:3px;
    }
    select option{
      text-align:left;
    }
    
    /* start of help */
    .help:hover{
      cursor:help;
    }
    select.help:hover,button.help:hover{
      outline:none;
      box-shadow:none;
      cursor:inherit;
    }
    .helpframe{
      display:none;
      border-radius: 5px; 
      -moz-border-radius: 5px; 
      -webkit-border-radius: 5px; 
      border: 1px solid #c0c0c0;
      color:black;
      padding:5px;
      width:95%;
      margin-top:2px;
      overflow: hidden;
    }
    .helpframe{ /* temporary disable */
      border:none;
      width:100%;
      padding:0px;
    }
    .helpframetitle{
      margin:-5px -5px 2px -5px;
      padding:2px 0px;
      background-color:#f0f0f0;
      text-align:right;
      display:none;/* temporary disable */
    }
    .helpframetitle .closebtn{
      color:#000000;
      margin-right:4px;
      padding: 0px 2px;
      font-weight:bold;
      text-decoration:none;
    }
    .helpframetitle .closebtn:hover{
      color:#f0f0f0;
      background-color:#0c0c0c;
      margin-right:4px;
      padding: 1px 3px;
      font-weight:bold;
      text-decoration:none;
    }
    .helppos{
      display:none;
      position:absolute;
      z-index:99;
      background-color:black;
      color:white;
      padding:5px;
      margin-right:10px;
      overflow: hidden;
      opacity:0;
    }
    .helpcontent{
      overflow:hidden;
    }
    #helps{
      position:absolute;
      left:-500px;
      top:-10000px;
      padding:5px;
      visibility:hidden;
      width:80%;
      overflow:hidden;
    }
    #helps table td,.helpcontent table td{
      padding:2px 10px;
    }
    #helps table th,.helpcontent table th{
      vertical-align:top;
      padding:2px;
      border-bottom:solid 1px #ebebeb;
    }
    #helps p,.helpcontent p{
      margin-top:1px;
    }
    /* end of help */
    
    /* make option be easier to click */
    option{
      padding:2px;
      border-bottom:solid 1px white;
    }
    option.option-label+option{
      border-bottom:solid 1px #d0d0d0;
    }
    option.option-label+option:last-child{
      border-bottom:solid 1px white;
    }
    .flat-btn-box{
      height:90px;
      width:255px;
    }
    .flat-btn{
      outline:#c0c0c0 solid thin;
      display:inline-block;
      float:left;
      width:25px;
      height:25px;
      line-height:25px;
      margin:2px;
      cursor:pointer;
      text-align:center;
    }
    .flat-btn-zoomin{
      display:none;
      position:absolute;
      border:solid 3px #4d90fe;
      height:45px;
      width:60px;
      z-index:99;
      background-color:white;
      font-size:1.75em;
      text-align:center;
      line-height:45px;
    }
    /*loading */
    #loading{
      display:none;
      position:absolute;
      height:100px;
      min-height: 100px;
      top:40%;
      left:5%;
      right:5%;
      width:60%;
      margin:auto;
      text-align:center;
      background-color:rgba(255,255,255,0.85);
      z-index:99;
    }
    #loading div{
      padding: 0px 0px 30px 0px;
      background-image: url('data:image/gif;base64,R0lGODlhEAALAPQAAP///wAAANra2tDQ0Orq6gYGBgAAAC4uLoKCgmBgYLq6uiIiIkpKSoqKimRkZL6+viYmJgQEBE5OTubm5tjY2PT09Dg4ONzc3PLy8ra2tqCgoMrKyu7u7gAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCwAAACwAAAAAEAALAAAFLSAgjmRpnqSgCuLKAq5AEIM4zDVw03ve27ifDgfkEYe04kDIDC5zrtYKRa2WQgAh+QQJCwAAACwAAAAAEAALAAAFJGBhGAVgnqhpHIeRvsDawqns0qeN5+y967tYLyicBYE7EYkYAgAh+QQJCwAAACwAAAAAEAALAAAFNiAgjothLOOIJAkiGgxjpGKiKMkbz7SN6zIawJcDwIK9W/HISxGBzdHTuBNOmcJVCyoUlk7CEAAh+QQJCwAAACwAAAAAEAALAAAFNSAgjqQIRRFUAo3jNGIkSdHqPI8Tz3V55zuaDacDyIQ+YrBH+hWPzJFzOQQaeavWi7oqnVIhACH5BAkLAAAALAAAAAAQAAsAAAUyICCOZGme1rJY5kRRk7hI0mJSVUXJtF3iOl7tltsBZsNfUegjAY3I5sgFY55KqdX1GgIAIfkECQsAAAAsAAAAABAACwAABTcgII5kaZ4kcV2EqLJipmnZhWGXaOOitm2aXQ4g7P2Ct2ER4AMul00kj5g0Al8tADY2y6C+4FIIACH5BAkLAAAALAAAAAAQAAsAAAUvICCOZGme5ERRk6iy7qpyHCVStA3gNa/7txxwlwv2isSacYUc+l4tADQGQ1mvpBAAIfkECQsAAAAsAAAAABAACwAABS8gII5kaZ7kRFGTqLLuqnIcJVK0DeA1r/u3HHCXC/aKxJpxhRz6Xi0ANAZDWa+kEAA7AAAAAAAAAAAA');
      background-repeat:no-repeat;
      background-position:center;
    }
    #loading-text{
      font-size:16px;
    }
    
    .modal-dialog{
      display:none;
      position:absolute;
      top:40%;
      left:5%;
      right:5%;
      width:70%;
      margin:auto;
      min-height:200px;
      z-index:99;
      box-shadow: 0 4px 16px rgba(0,0,0,.2);
      background: #fff;
      background-clip: padding-box;
      border: 1px solid #acacac;
      border: 1px solid rgba(0,0,0,.333);
      outline: 0;
      position: absolute;
      color: #000;
      padding: 15px 21px;
      font-size:14px;
    }
    .modal-dialog button{
      -webkit-border-radius: 2px;
      -moz-border-radius: 2px;
      border-radius: 2px;
      background-color: #f5f5f5;
      background-image: -webkit-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -moz-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -ms-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -o-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: linear-gradient(top,#f5f5f5,#f1f1f1);
      border: 1px solid #dcdcdc;
      border: 1px solid rgba(0,0,0,0.1);
      color: #333;
      cursor: default;
      font-family: inherit;
      font-size: 11px;
      font-weight: bold;
      height: 29px;
      line-height: 27px;
      margin:0;
      min-width: 72px;
      outline: 0;
      padding: 0 8px;  
    }
    .modal-dialog .title{
      font-weight:bold;
    }
    .modal-dialog .buttons{
        position: absolute;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
    }
    .modal-dialog button+button{
      margin-left:20px;
    }
    .modal-dialog .x{
      font-weight: bold;
      text-align: right;
      margin-top: -5px;
      margin-right: -5px;
      color: #a0a0a0;
      cursor:pointer;
    }
    /* end of loading */
    #reST{
        white-space: pre;
        overflow-y: auto;
        font-family: monospace;
        font-size: 12px;
        width: 100%;
        overflow-x: auto;
        outline: thin solid rgba(0,0,0,0.2);
        margin-top: 10px !important;   
    }
    #reSTFilesBox {
        width: 99%;
        padding-left:0;
    }
    #reSTFiles {
        width: 100%;
    }
    #reSTFiles div{
      width: 20%;
      float:left;
      margin-left:4%;
    }
    #reSTFiles div .title {
        padding: 2px;
        font-size: 12px;
        font-family: monospace;
    }
    #reSTFiles div img {
        outline: thin solid rgba(0,0,0,0.2);
        width:100%;
    }
    #convertion-message{
      display:inline-block;
      outline:thin solid #c0c0c0;
      padding:5px 10px;
      float:right;
      background-color:#e5ec7c;
    }
    </style>
      </head>
      <body>
    <div class="sidebar" style="padding:5px 1px;margin:-8px;height:100%;overflow:hidden">
      <div class="tab-title-bar" style="">
        <div class="tab-title" tab="t1" onclick="setActiveTab('t1')"><span class="i18n">Conversion</span></div>
        <div class="tab-title" tab="t2" onclick="setActiveTab('t2')"><span class="i18n">Rules</span></div>
        <div class="tab-title" tab="t3" onclick="setActiveTab('t3')"><span class="i18n">Convenience</span></div>
      </div>
      <div class="restructure-text tab active" tab="t1" style="">
        <div class="block form-group fixed" style="">
           <button onclick="generateDocument()" id="generateDocument-btn" style="display:none"><span class="help" helpname="gen" helptype="hover">Generate Document</span></button>
           <span id="copygroup" style="margin-left:15px">
             <button onclick="copyToClipboard()" class="blue"><span class="help" helpname="ctc" helptype="hover">Copy to Clipboard</span></button>
             <select onchange="onPrefixChanged()" id="copy-prefix" class="help" helpname="cpf" helptype="hover">
               <option value="">No prefix &nbsp;</option>
               <option value="# ">#</option>
               <option value="* ">*</option>
               <option value="// ">//</option>
               <option value="_ask_">Ask</option>
             </select>
           </span>
           <button onclick="download()" id="download-btn" style="margin-left:16px;display:none" class="blue"><span class="help" helpname="dow" helptype="hover">Download</span></button>
           <span id="convertion-message"></span>
        </div>
        <div class="block form-group" style="margin-top:5px !important;display:none">
          <input type="checkbox" id="commit-include-images">
          <label class="help" helpname="cii" helptype="hover" for="commit-include-images"><span class="i18n">Include images</span></label> 
        </div>    
        <div class="block" id="reST"></div>
        <div class="block" id="reSTFilesBox"><div id="reSTFiles"></div></div>
      </div>
      <div class="rules tab" tab="t2">
        <label for="conversion-rules">For Conversion</label>
        <ol style="line-height:24px" id="conversion-rules">
          <li>If there are selections, the top elements of every selected one are converted. Which means if a paragraph is partially selected, whole the paragraph is converted.</li>
          <li>If there is no selection and the cursor is in a table, that table is converted</li>
          <li>Otherwise, the whole document is converted</li>
        </ol>
        <label for="download-rules">For Dowload</label>
        <ol style="line-height:24px" id="download-rules">
          <li>When partially converted, a selection.zip will be created with the partial reStructedText and images (if any).</li>
          <li>If whole document is converted, a &lt;document-name&gt;.zip will be created with all generated reStructedText and images (if any).</li>
        </ol>
      </div>
      <div class="convenience tab" tab="t3">
        <div class="block form-group">
          <label for="convenience-links">Links</label>
          <ul style="line-height:24px" id="convenience-links">
            <li><a href="#" id="commit-to-github">Commit to Github</a></li>
            <li><a href="https://ggeditor.readthedocs.io/en/latest/User%20Guide.html" target="_blank">GGeditor User Guide</a></li>
            <li><a href="https://github.com" target="_blank">Github</a></li>
            <li><a href="https://readthedocs.org" target="_blank">Readthedocs.org</a></li>
            <li><a href="http://rst.ninjs.org" target="_blank">Online reStructuredText Editor</a></li>
            <li><a href="http://www.sphinx-doc.org/en/1.4.9/contents.html" target="_blank">Sphinx Documentation</a></li>
          </ul>
        </div>
        <div class="block form-group" style="border-top:dashed 1px #c0c0c0;padding-top:10px">
          <label for="ratestart">Appreciation for You</label>
          <div id="ratestart" style="padding-left:25px">
          It would really help us if you had a second to
          <ul>
            <li><a href="https://chrome.google.com/webstore/detail/ggeditor/piedgdbcihbejidgkpabjhppneghbcnp" target="_blank">Leave a Google Docs store rating</a></li>
            <li>Or <a href="https://github.com/iapyeh/GGeditor" target="_blank">star GGeditor on Github</a></li>
          </ul>
          that helps us keep momentun on GGeditor.
          </div>
        </div>
      </div>
      <!--end of tab-->
    </div>
    <div class="masterhelpframe helpframe">
      <div class="helpframetitle">
        <a class="closebtn" onclick="closeHelp(this)">×</a>
      </div>
      <div class="helpcontent"></div>
    </div>
    
    <div id="loading" class="modal-dialog">
      <div>
        <h1><label class="i18n" id="loading-text"></label></h1>
      </div>
    </div>
    <div id="dialog" class="modal-dialog">
      <div style="width:100%">
        <div class="x">x</div>
        <p class="title"></p>
        <p class="content"></p>
        <div class="buttons">
          <button class="yes i18n blue">Delete</button><button class="cancel i18n">Cancel</button>
        </div>
      </div>
    </div>
    <span class="helppos" id="helppostmpl" style="display:none"></span>
    <span id="helppostmplpt" style="display:none;position:absolute">▲</span>
    <div style="display:none">
      <div id="helps">
        <div name="gen">Generate reStructuredText of whole document</div>
        <div name="dow">Download generated reStructuredText file and images</div>
        <div name="ctc">Copy generated reStructuredText content to clipboard</div>
        <div name="cpf">Line-prefix when copying to clipboard</div>
      </div>
    </div>
    <script language="javascript">
    document.addEventListener( "DOMContentLoaded", initialization , false );
    
    function initialization(){
      document.getElementById('commit-to-github').onclick = showCommitDialog
      enableHelp()
      setupElementsStyle()
      /* assign initial values from persistent data */  
      setTimeout(function(){
        generate()
      })
    }
    
    
    /*
     * lib functions starts below
     * 
     */
    var serverValues={locale:'en'};
    function localI18n(s){
      return s
    }
    function setActiveTab(name){
      var tabs = document.querySelectorAll('.tab')
      for (var i=0;i<tabs.length;i++){
        tabs[i].className = tabs[i].className.replace(/ active/,'');
        if (tabs[i].getAttribute('tab')==name){
          tabs[i].className+=' active'
        }
      }
      var titles = document.querySelectorAll('.tab-title')
      for (var i=0;i<titles.length;i++){
        if (titles[i].getAttribute('tab')==name){titles[i].className='tab-title active'}
        else titles[i].className='tab-title';
      }
    }
    
    function getTimestamp(){
      var now = new Date()
      return now.getFullYear()+'-'+(now.getMonth()+1)+'-'+now.getDate()+' '+now.getHours()+':'+now.getMinutes()+':'+now.getSeconds()
    }
    function getViewportSize(){
      var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
      var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
      return {width:w,height:h}
    }
    function moveElementToViewportCenter(ele) {
        var size = getViewportSize()
        var rect = ele.getBoundingClientRect()
        ele.style.top =  Math.round(size.height/2 - rect.height/2)+'px'
        ele.style.marginLeft = Math.round(size.width/2  - rect.width/2)+'px'
    }
    
    var loadingCount=0;
    function loading(yes,label){
      var title = localI18n('Please be waiting...');
    
      if (yes && typeof(yes)=='string') title = yes
    
      if ((loadingCount<0 && !yes) || (loadingCount>0 && yes)) {
        if (title) {
          document.getElementById('loading-text').innerHTML = title;
        }
        loadingCount += yes ? 1 : -1;
        return;
      }
      loadingCount += yes ? 1 : -1;
      var loadingDiv = document.getElementById('loading')
      if (loadingCount==1){
        // start loading
        loadingDiv.style.display='flex';
        document.getElementById('loading-text').innerHTML = title;
        document.querySelector('.sidebar').style.opacity = 0.5;
        moveElementToViewportCenter(loadingDiv)
      }
      else{
        // stop loading
        loadingDiv.style.display='none';
        document.querySelector('.sidebar').style.opacity = 1;
      }
    }
    function stopLoading(label){loading(false,label)}
    function setLoadingTitle(title){document.getElementById('loading-text').innerHTML = title;}
    
    function myConfirm(title,callback){
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'  
      dialog.style.display='block';
      //dialog.style.top = (window.pageYOffset+150)+'px'
      document.querySelector('.sidebar').style.opacity = 0.5;
      moveElementToViewportCenter(dialog)
      var cleanup = function(yes){
        callback(yes)
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.cancel').onclick = null;
        document.querySelector('.sidebar').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        dialog.style.top = '0px';
        document.querySelector('.sidebar').style.opacity = 1; 
      }
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.cancel').onclick = function(){
        cleanup(false);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      setTimeout(function(){
        document.querySelector('.sidebar').onclick = function(){
          cleanup(false);
        } 
      },100)
    }
    function myAlert(title,callback,autoCloseInterval){
      if (!callback) callback = function(){}
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'
      dialog.style.display='block';
      //dialog.style.top = (window.pageYOffset+150)+'px'
      document.querySelector('.sidebar').style.opacity = 0.5;
      var yesHTML = dialog.querySelector('.yes').innerHTML
      var autoCloseTimer = 0
      var cleanup = function(yes){
        callback(yes)
        if (autoCloseTimer) clearTimeout(autoCloseTimer)
        document.querySelector('.sidebar').onclick = null
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.cancel').style.display = ''
        dialog.querySelector('.yes').innerHTML = yesHTML
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        document.querySelector('.sidebar').style.opacity = 1; 
      }
      dialog.querySelector('.cancel').style.display = 'none'
      dialog.querySelector('.yes').innerHTML = 'OK'
    
      moveElementToViewportCenter(dialog)
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      // click outside dialog also close the dialog
      setTimeout(function(){
        document.querySelector('.sidebar').onclick = function(){
          cleanup(false);
        } 
      },100)
      // auto close dialog
      if (autoCloseInterval){
        autoCloseTimer = setTimeout(function(){
          autoCloseTimer = 0
          cleanup(false)
        },autoCloseInterval)
      }
    }
    
    function myPrompt(title,options,callback){
        /*
         * options = {
         *     value*:(string) value of the input element
         *     placeholder*:(string) default null
         *     content*:(string) default "<input style="width:100%;height:40px;font-size:1.5em">"
         *     button:*(dict){ok:{className:<class name>},cancel:{className:<class name>}}, default null
         * }
         */
        var dialog = document.getElementById('dialog')
        dialog.querySelector('.title').innerHTML = title;
        dialog.querySelector('.content').innerHTML = (options.content || '<input style="width:100%;height:40px;font-size:1.5em">')
        dialog.querySelector('.content').style = 'block'
        dialog.querySelector('.buttons').style = 'block'
        var input = dialog.querySelector('.content input')
        if (options.placeholder) input.setAttribute('placeholder',options.placeholder)
        if (options.value) input.value = options.value
        var buttons = [
            '<button class="ok'+((options.button && options.button.ok && options.button.ok.className) ? ' '+options.button.ok.className : '' )+'">OK</button>',
            '<button class="cancel'+((options.button && options.button.cancel && options.button.cancel.className) ? ' '+options.button.cancel.className : '' )+'">Cancel</button>',
            ]
        dialog.querySelector('.buttons').innerHTML = buttons.join('')
    
        var cleanup = function(value){
          document.querySelector('.sidebar').style.opacity = 1; 
          document.querySelector('.sidebar').onclick = null
          dialog.querySelector('.cancel').onclick = null;
          dialog.querySelector('.x').onclick = null;
          dialog.querySelector('.ok').onclick = null;
          dialog.querySelector('.buttons').innerHTML = ''
          dialog.querySelector('.content').innerHTML = ''
          dialog.querySelector('.title').innerHTML = ''
          dialog.style.display='none';
          callback(value)
        }
        setTimeout(function(){
          dialog.querySelector('.x').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.cancel').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.ok').onclick = function(){
              var text = dialog.querySelector('input').value || (options.defaultText || '')
              cleanup(text)
          }
        },500)
        document.querySelector('.sidebar').style.opacity = 0.5;     
        dialog.style.display = 'block'
        dialog.style.height = '200px'
        moveElementToViewportCenter(dialog)
        // click outside dialog also close the dialog
        setTimeout(function(){
          document.querySelector('.sidebar').onclick = function(){
            cleanup(false);
          } 
        },100)
        return {dom:dialog,callback:callback}
    }
    
    /* start of help system */
    function enableHelp(){
      var helps =  document.querySelectorAll('.help');
      var timer = 0,delay = 1000,hoverDelay=1000;
      for (var i=0,l=helps.length;i<l;i++){
        var hoverType = helps[i].getAttribute('helptype')=='hover';
        helps[i].onmouseover = function(evt){
          var target = evt.currentTarget
          var helpname = target.getAttribute('hoverhelpname') || target.getAttribute('helpname')
          // check if the same help is openning
          if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) {
            return;
          }
          if (timer>0) clearTimeout(timer);
          timer = setTimeout(function(){
            timer = 0;
            showHelp(helpname,target.getAttribute('helpCloseByBtn'),target.getAttribute('helptype'))
          },(hoverType ? hoverDelay : delay))
        }
        if (hoverType){
          helps[i].onmouseout = function(evt){
            if (timer){
              //give up to show it
              clearTimeout(timer);timer = 0;
            }
            else{
              closeHoverHelp();
            }
          }
        }
        else{
          // cancel the help showup
          helps[i].onmouseout = function(evt){
            if (timer){
              clearTimeout(timer);timer = 0;
            }
          }
        }
      }
    }
    
    function getOffset( el ) {
        var _x = 0;
        var _y = 0;
        while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
            _x += el.offsetLeft //- el.scrollLeft;
            _y += el.offsetTop //- el.scrollTop;
            el = el.offsetParent;
        }
        return { top: _y, left: _x };
    }
    function showHelp(helpname,helpCloseByBtn,helpType){
    
      /* simply deal with hover help */
      if (helpType=='hover'){
          var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
          var tmpl = document.getElementById('helppostmpl')
          var c = document.querySelector('#helps div[name="'+helpname+'"]');
          // make it visible
          var sidebarRect = document.querySelector('.sidebar').getBoundingClientRect()
          var sidebarWidth = sidebarRect.right - sidebarRect.left;
          tmpl.style.display='inline-block';
          tmpl.style.position = 'absolute';
          tmpl.style.zIndex = 99;
          var target = document.querySelector('.help[hoverhelpname="'+helpname+'"][helptype="hover"]');
          if (!target) target = document.querySelector('.help[helpname="'+helpname+'"][helptype="hover"]');
          var targetRect = target.getBoundingClientRect()
          var targetHeight = targetRect.bottom - targetRect.top;
          var targetWidth = targetRect.right - targetRect.left;
          var rect = getOffset(target)
          tmpl.style.top = (rect.top + targetHeight+4)+'px'
          tmpl.style.opacity = 0;
          tmpl.innerHTML= c.innerHTML;
          tmpl.style.maxWidth = Math.floor(sidebarWidth * 0.8)+'px'
          var tmplRect = tmpl.getBoundingClientRect()
          var tmplWidth = tmplRect.right - tmplRect.left
          var p0 = Math.floor(sidebarWidth * 0.1);
          var p1 = Math.floor(sidebarWidth * 0.9);
          var tmplpt = document.getElementById('helppostmplpt')
          tmplpt.style.top = (parseInt(tmpl.style.top)-10)+'px';
          if (rect.left < p0){
            tmpl.style.left = rect.left+'px'
            tmplpt.style.left = tmpl.style.left;
          }
          else if (rect.left+targetWidth > p1) {
            tmpl.style.left = Math.floor((rect.left+targetWidth - tmplWidth))+'px'
            tmplpt.style.left = Math.floor(parseInt(tmpl.style.left)+tmplWidth-18)+'px';
          }
          else {
            tmpl.style.left = Math.max(0,Math.floor(rect.left+targetWidth/2-tmplWidth/2))+'px'
            tmplpt.style.left = Math.max(0,Math.floor(parseInt(tmpl.style.left)+tmplWidth/2-6))+'px'
          }
          tmpl.setAttribute('active',1);
          setTimeout(function(){
            //starts animation
            tmpl.style.opacity=1;
            tmplpt.style.display='';
          },1)
        return;
      }
    
      /* need to check again for some help is triggered manually */
      if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) return;//already opened
      /* one help only, unless the existing help is a modal help */
      closeHelp()
      // create a new helpframe  
      /* prepare for animation */
      // clone the masterhelpframe  
      var helpframe = document.querySelector('.masterhelpframe.helpframe').cloneNode(true);
      helpframe.className = 'helpframe';
    
      helpframe.style.display = 'block';
      helpframe.setAttribute('helpname',helpname)
      var trigger = function(){    
        //var helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpname = this._helpname; 
        if (helpCloseByBtn) helpframe.setAttribute('modal',1)
        helpframe.querySelector('.closebtn').setAttribute('helpname',helpname)
        var cele = helpframe.querySelector('.helpcontent')
        /* find the insert position */
        var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
        helppos.parentNode.insertBefore(helpframe, helppos.nextSibling);
        /* find the help content to insert */
        var c = document.querySelector('#helps div[name="'+helpname+'"]');
        /* insert the help content */
        cele.appendChild(c);//move it
        /* starts the animation to show up*/
        var titleheight = helpframe.querySelector('.helpframetitle').clientHeight;
        /* make the helpframe visible, delay to wait the DOM been refreshed */
        setTimeout(function(){
          // scroll to make it visible
          var y = getOffset( helpframe ).top; 
          var offset = y-window.scrollY;
          if (offset<0 || offset > window.innerHeight)  window.scrollTo(0,Math.max(0,y-50));      
    
          //trigger event
          var e = document.createEvent('Event');
          e.initEvent('help-open-'+helpname,false,true);
          document.dispatchEvent(e);
    
        },100);
      }
      setTimeout(function(){trigger.apply({_helpname:helpname})},1)
    }
    
    function closeHoverHelp(){
      /* find the insert position */
      var helppos = document.querySelector('.helppos[active]');
      if (helppos===null) return;
      helppos.innerHTML='';
      // make it invisible
      helppos.style.display='none';
      helppos.style.opacity=0;
      helppos.removeAttribute('active');
      var tmplpt = document.getElementById('helppostmplpt')
      tmplpt.style.display='none';
    }
    function closeHelp(btn){
      /* release the body click */
      document.body.onclick = null;
    
      var helpname = null,helpframe=null;
      if (btn) {
        helpname = btn.getAttribute('helpname');
        helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpframe.removeAttribute('modal')//enforce to close by btn
        //fire event if closed by button
        var e = document.createEvent('Event');
        e.initEvent('help-close-'+helpname,false,true);
        document.dispatchEvent(e);
      }
      else {
        helpframe = document.querySelector('.helpframe[helpname]');
        if (!helpframe) return true;//no helpframe is showing    
        helpname = helpframe.getAttribute('helpname');
      }
      if (helpframe.getAttribute('modal')) return false
      var cele = helpframe.querySelector('.helpcontent')
      if (cele.firstChild != null){
        /*cele.removeChild(cele.firstChild);*/
        //move back to helps
        document.getElementById('helps').appendChild(cele.firstChild);    
      }
      helpframe.style.display = 'none';
      helpframe.parentNode.removeChild(helpframe);
      return true;
    }
    /* end of help system */
    
    function setupElementsStyle(){
      var viewport = getViewportSize()
      var reSTEle = document.getElementById('reST')
      var reSTTab = document.querySelector('.restructure-text.tab')
      setActiveTab(reSTTab.getAttribute('tab'))
      var marginSpace = 15;
      reSTEle.style.maxHeight =   reSTEle.style.minHeight = (viewport.height - marginSpace - document.querySelector('.restructure-text.tab div:first-child').getBoundingClientRect().bottom)+'px'
      setActiveTab('t1')
    }
    var generatedResult;
    function generate(wholeDocument){
      document.getElementById('reST').innerHTML = 'waiting...'
      document.getElementById('reSTFiles').innerHTML = ''  
      loading(true)
      document.getElementById('convertion-message').innerText = ''
      var includeImages = document.getElementById('commit-include-images').checked
      var done = function(resp){
        stopLoading()
    
        //document.getElementById('download-btn').removeAttribute('disabled')
    
    
        generatedResult = JSON.parse(resp)
        document.getElementById('reST').innerText = generatedResult.content
        // some message to indicate what been generated
        var mesg;
        if (generatedResult.wholeDocument){
          mesg = 'Document is converted'
          // show generate document button if partially generated
          document.getElementById('generateDocument-btn').style.display = 'none'
          document.getElementById('copygroup').style.display = 'none'
          document.getElementById('download-btn').style.display = ''
        }
        /*
        else if (/\+\-\-\-\-/.test(generatedResult.content)){
        */
        else if (generatedResult.tableGenerated){
          mesg = 'Table is converted only'
          // show generate document button if partially generated
          document.getElementById('generateDocument-btn').style.display = ''
          document.getElementById('copygroup').style.display = ''
          document.getElementById('download-btn').style.display = 'none'      
        }
        else{
          mesg = 'Selection is converted only'
          // show generate document button if partially generated
          document.getElementById('generateDocument-btn').style.display = ''
          document.getElementById('copygroup').style.display = ''
          document.getElementById('download-btn').style.display = 'none'      
        }
        document.getElementById('convertion-message').innerText = mesg
    
    
        //show images
        if (includeImages && generatedResult.files.length){
          document.querySelector('.sidebar').style.overflowY = 'auto'
          var reSTFiles = document.getElementById('reSTFiles')
          reSTFiles.innerHTML = ''
          generatedResult.files.forEach(function(file){
            var div = document.createElement('div')
            //div.innerHTML = '<div class="title">'+generatedResult.imageFolder+'/'+file.name+'</div>'
            div.innerHTML = '<div class="title">'+file.name+'</div>'
            reSTFiles.appendChild(div)
            var img = new Image()
            img.style.width = "100%"
            div.appendChild(img)
            img.src = 'data:image/jpeg;base64,'+file.content
          })
        }
        else if (generatedResult.files.length){
          // ensure the download-button appears, if there are images in generated markup
          // even in partial conversion
          document.getElementById('download-btn').style.display = ''
        }
        else{
          document.querySelector('.sidebar').style.overflowY = 'hidden'
        }
        // release memory pressure
        if (generatedResult.wholeDocument){
          delete generatedResult.content
        }
        else{
          // test if code, code-block or raw html geen generated
          // if it is, don't do escape
          if (generatedResult.tableGenerated){
            var no_escape = /\.\. code\-?/i.test(generatedResult.content) || /\.\. .+? raw:: html/i.test(generatedResult.content)
            if (no_escape){
              escapePat = null
              generatedResult.rawContentGenerated = true
            }
          }
          updatePrefix()
        }
      }
      var inBase64 = false
      if (typeof(wholeDocument)=='undefined') wholeDocument = false
      google.script.run.withSuccessHandler(done).withFailureHandler(stopLoading).generate(inBase64,includeImages,wholeDocument);
    }
    
    function generateDocument(){
      generate(true)
    }
    
    function downloadContentAs(content,filename,isBinary){
      var requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
      if (!requestFileSystem){
        myAlert('Not Supported','Downloading in your browser is not supported.')
        return;
      }
      var fsErrorHandler = function(e) {
          var msg = '';
          switch (e.name) {
            case FileError.QUOTA_EXCEEDED_ERR:
              msg = 'QUOTA_EXCEEDED_ERR';
              break;
            case FileError.NOT_FOUND_ERR:
              msg = 'NOT_FOUND_ERR';
              break;
            case FileError.SECURITY_ERR:
              msg = 'SECURITY_ERR';
              break;
            case FileError.INVALID_MODIFICATION_ERR:
              msg = 'INVALID_MODIFICATION_ERR';
              break;
            case FileError.INVALID_STATE_ERR:
              msg = 'INVALID_STATE_ERR';
              break;
            default:
              msg = 'Error:'+e.name+';'+e.message;
              break;
          };
          console.log('Error: ' + msg);
      }
      requestFileSystem(window.TEMPORARY, 1024*1024, function(fs) {
        fs.root.getFile(filename, {create: true}, function(fileEntry) {
            fileEntry.createWriter(function(fileWriter) {
                var blob;
                if (isBinary){
                  var byteArray = new Uint8Array(content);
                  blob = new Blob([byteArray],{type: "application/octet-binary"});
                }
                else{
                  blob = new Blob([content],{type: "text/plain"});
                }
                fileWriter.onwriteend = function() {
                  var a = document.createElement('a')
                  a.href = fileEntry.toURL()
                  a.setAttribute('download',filename)
                  a.setAttribute('target','_blank')
                  a.click()
                };
              fileWriter.write(blob);
            }, fsErrorHandler);
        }, fsErrorHandler);
      }, fsErrorHandler);
    }
    
    function download(){
      loading(true)
      var next = function(zipbytes){
        stopLoading()
        zipname = generatedResult.wholeDocument ? generatedResult.namespace+'.zip' : generatedResult.namespace+'_'+(generatedResult.tableGenerated ? 'table.zip' : 'selection.zip')
        downloadContentAs(zipbytes,zipname,true)
      }
      //var includeImages = document.getElementById('commit-include-images').checked
      var includeImages = true
      var wholeDocument = false
      google.script.run.withSuccessHandler(next).withFailureHandler(stopLoading).download(includeImages,wholeDocument);
    }
    
    /*
     * countFullWidth() and splitByWidth are copied from generator.gs, should keep synced with its original copy
     */
    // caution: |, : was not escaped intentionally
    function duplicateChar(char,size){
      // '*' -> '*****'
      var text = []
      for (var i=0;i<size;i++){
        text.push(char)
      }
      return text.join('')
    }
    
    var escapePat = /[`\*]/g
    function escapeFun(m){
        return '\\'+m
    }
    
    // /`.+?`__/g was added for inline links [/^\s+(\*\s)/g,
    // this would preserve directives lines
    var directivePats = [/`.+?`__/g,/`{1,2}.+?`{1,2}/g, /^\.\. \|.+?\| replace\:\:.*$/g]
    // this would preserve list items
    directivePats = directivePats.concat([/^\*\s.*$/g])
    function escapeText(s){
      //preserve `some` and ``some``
      var directives = []
      var s1 = s
      directivePats.forEach(function(directivePat){
        s1 = s1.replace(directivePat,function(m,g1){
          directives.push(m)
          return '♞'
        })
      })
      directives.reverse()
      var s2
      if (escapePat){
        s2 = s1.replace(escapePat,escapeFun) 
      }
      else{
        s2 = s1
      }
      var s3 = s2.replace(/♞/g,function(){
        return directives.pop()
      })
      return s3
    }
    function escapeTextWithWidth(s,lineWidth,lines,indent,secondaryLinePrefix){
      //preserve `some` and ``some``
      var directives = []
      var s1 = s
      directivePats.forEach(function(directivePat){
        s1 = s1.replace(directivePat,function(m){
          directives.push(m)
          return '☢'
        })
      })
      directives.reverse()
      //var s2 = s1.replace(escapePat,escapeFun)
      var rawlines = s1.split('\n')
      var splitedLines = []
      rawlines.forEach(function(line){
        splitByWidthUnescaped(line,lineWidth,splitedLines,indent)
      })
      splitedLines.forEach(function(line,i){
        // for list item, prefix more indentation for secondary lines
        if (i>0) line = secondaryLinePrefix+line
        lines.push(line.replace(/☢/g,function(){
          return directives.pop()
        }))
      })
    }
    
    var fullWidthPat=/[\u1100-\u11FF\u3000-\u30FF\u3130-\u318F\u3200-\u32FF\u3400-\u9FFF\uAC00-\uD7AF\uFF01-\uFF60\uFFE0-\uFFE6]/
    function countFullWidth(s){
        var c = 0
        for (var x=0;x<s.length;x++){
          c +=  fullWidthPat.test(s.charAt(x)) ? 1 : 0 
          //range U+AC00–U+D7AF
          c +=  /[]/.test(s.charAt(x)) ? 1 : 0 
        }
        return c
    }
    function splitByWidthUnescaped(nomarkupText,lineWidth,textchunks,prefix){
    
      // !! this copy is original from splitByWidth, but don't do escapeText, because this is used for inline display
    
      /*
       * split a long text (without \n) to a specific width of several lines      
       * please note:
       *   1. the heading spaces in line content will be removed
       *   2. the sepical character resulted line content will be escaped
       *
       * nomarkupText: string, should not contain markups
       * lineWidth: int, line width to cut, the cutpoint is roughly around this number
       * textchunks: array to save the splited lines content
       * 
       */
        var nomarkupTextLines = nomarkupText.replace(/\r/g,'\n').split('\n')
        var deltaOffset = 5
        var lines = []
        var pat = /[a-zA-Z]/
        nomarkupTextLines.forEach(function(line){
          var len = line.length + countFullWidth(line)
          if (lineWidth && len > lineWidth){
            var curPos = lineWidth - deltaOffset
            var maxPos = line.length
            var startPos = 0
            // find a suitable break point
            while (curPos < maxPos){
              var c = line.charAt(curPos)
              if (!pat.test(c)){
                var newline = line.substring(startPos,curPos+1)
                // disabled, don't know why to +"\n" ?
                //lines.push(escapeText(newline.replace(/^\s+/,''))+'\n')
                lines.push(newline.replace(/^\s+/,''))
                startPos = curPos+1
                curPos += lineWidth - deltaOffset
              }
              else{
                curPos +=1
              }
            }
            if (startPos <maxPos){
                var lastline = line.substr(startPos)
                lines.push(escapeText(lastline.replace(/^\s+/,'')))
            }
          }
          else{
            lines.push(escapeText(line))
          }
        })
       lines.forEach(function(line){
         textchunks.push(prefix+line)
       })
    }
    
    function copyToClipboard(){
      justCopyToClipboard()
      /*
      var prefixSle = document.getElementById('copy-prefix')
      var prefix = prefixSle.options[prefixSle.selectedIndex].value
      if (prefix=='_ask_'){
        myPrompt('Prefix every copied line with:',{},function(text){
          if (!text) return
          copyToClipboardWithPrefix(text)
        })
      }
      else{
        copyToClipboardWithPrefix(prefix)
      }
      */
    }
    function onPrefixChanged(){
      var prefixSle = document.getElementById('copy-prefix')
      var prefix = prefixSle.options[prefixSle.selectedIndex].value
      if (prefix=='_ask_'){
        myPrompt('Prefix every copied line with:',{},function(text){
          if (!text) return
          updatePrefix(text)
        })
      }
      else{
        updatePrefix(prefix)
      }  
    }
    function updatePrefix(prefix){
      var lineWidth = 60
      var lines = []
      var rawLines =  generatedResult.content.split('\n')
    
      // find out list item with indentition
      var patListItem0 = /^\s+\*\s/
      var patListItem1 = /^\s+#\.\s/
      if (lineWidth){
        for (var i=0,end=rawLines.length;i<end;i++){
          if (rawLines[i]=='.. bottom of content') {
            for (var ii=i+1;ii<end;ii++){
              lines.push(rawLines[ii])
            }
            break
          }
          if (generatedResult.rawContentGenerated || generatedResult.tableGenerated){
            // do not break line by width
            lines.push(rawLines[i])
          }
          else{
            var spaces
            var secondaryLinePrefix = ''
            if (patListItem0.test(rawLines[i])){
              spaces = (rawLines[i].match(/^\s+/)||[''])[0]
              secondaryLinePrefix = '  ' // 2 spaces
            }
            if (patListItem1.test(rawLines[i])){
              spaces = (rawLines[i].match(/^\s+/)||[''])[0]
              secondaryLinePrefix = '   ' // 3 spaces
            }
            else{
              spaces = (rawLines[i].match(/^\s+/)||[''])[0]
            }
            escapeTextWithWidth(rawLines[i].substring(spaces.length),lineWidth,lines,spaces,secondaryLinePrefix) 
          }
        }
      }
      else{
        lines = rawLines
      }
      if (prefix){
        for (var i=0,end=lines.length;i<end;i++){
          lines[i] = prefix + lines[i]
        }
      }
      document.getElementById('reST').innerText = lines.join('\n')
      // document.body.removeChild(copyTextarea);
    }
    function justCopyToClipboard(){
      var copyTextarea = document.createElement('textarea')
      document.body.appendChild(copyTextarea);
      copyTextarea.value = document.getElementById('reST').innerText
      copyTextarea.style.position = 'absolute'
      copyTextarea.style.width = '10px'
      copyTextarea.style.left = '-200px'
      try {
        copyTextarea.select();
        var successful = document.execCommand('copy');
        if (successful){
          var msg = 'Copied to clipboard'
          myAlert(msg,null,1000);
        }
        else{
          myAlert('Copy not supported on this browser')
        }
      } catch (err) {
        myAlert('Failed, '+err.message);
      }
      document.body.removeChild(copyTextarea);
    }
    /*
    function copyToClipboardWithPrefix(prefix){
      var copyTextarea = document.createElement('textarea')
      document.body.appendChild(copyTextarea);
      var lines =  document.getElementById('reST').innerText.split('\n')
      if (prefix){
        for (var i=0,end=lines.length;i<end;i++){
          lines[i] = prefix + lines[i]
        }
      }
      copyTextarea.value = lines.join('\n')
    
      var copyTextarea = document.createElement('textarea')
      document.body.appendChild(copyTextarea);
      copyTextarea.value = document.getElementById('reST').innerText
      copyTextarea.style.position = 'absolute'
      copyTextarea.style.width = '10px'
      copyTextarea.style.left = '-200px'
      try {
        copyTextarea.select();
        var successful = document.execCommand('copy');
        if (successful){
          var msg = 'Copied to clipboard'
          if (prefix) msg += ' with prefix "'+prefix+'"'
          myAlert(msg);
        }
        else{
          myAlert('Copy not supported on this browser')
        }
      } catch (err) {
        myAlert('Failed, '+err.message);
      }
      document.body.removeChild(copyTextarea);
    }
    */
    
    function showCommitDialog(evt){
      evt.preventDefault()
      loading(true)
      google.script.run.withSuccessHandler(function(){
        stopLoading()
        google.script.host.close()
      }).withFailureHandler(stopLoading).showCommitDialog();
    }
    </script>
    </body>
    </html>
    
    

|

.. _h665a1e3a382d3964444f29261a426b7e:

settings.html
*************


.. code-block:: python
    :linenos:

    <!DOCTYPE html>
    <html>
      <head>
        <base target="_top">
        <link rel="stylesheet" href="https://ssl.gstatic.com/docs/script/css/add-ons.css">
    <style>
    .tab {
      position:relative;
      left:0;
      top:0;
      display:none;
     /* padding:5px 2px 0px 10px; */
    }
    .tab.active{
      display:block;
    }
    .tab-title{
      border:solid 1px #c0c0c0;
      display:inline-block;
      position:relative;
      padding:5px 8px;
      border-bottom:none;
      -webkit-border-top-left-radius: 2px;
      -webkit-border-top-right-radius: 2px;
      -moz-border-radius-topleft: 2px;
      -moz-border-radius-topright: 2px;
      border-top-left-radius: 2px;
      border-top-right-radius: 2px;
      cursor:pointer;
      text-align:center;
      width:24%;
      font-size:0.95em;
      white-space: nowrap;
      overflow-x: hidden;
      text-overflow: ellipsis;
      margin-bottom:-5px;
    }
    .tab-title.active,.tab-title.active:hover{
      top:1px;
      background-color:white;
      -webkit-box-shadow: none;
      -moz-box-shadow:    none;
      box-shadow:         none;
    }
    .tab-title:hover{
      background-color:#f0f0f0;  
      -webkit-box-shadow: 0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      -moz-box-shadow:    0px 0px 1px 0px rgba(50, 50, 50, 0.25);
      box-shadow:         0px 0px 1px 0px rgba(50, 50, 50, 0.25);
    }
    .tab-title-bar {
      border-bottom:solid 1px #c0c0c0;
      margin-bottom:10px;
      padding:0px 10px;
    }
    .tab > .block{
        margin-top:30px  !important;
    }
    .tab > .block:first-child{
        margin-top:12px  !important;
    }
    .tab > .block > label:first-child {
      margin-bottom:5px;
      display:block;
    }
    
    button.small{
        min-width:35px;
        height:25px;
        margin-left:3px;
        margin-top:3px;
    }
    select option{
      text-align:left;
    }
    
    /* start of help */
    .help:hover{
      cursor:help;
    }
    select.help:hover,button.help:hover{
      outline:none;
      box-shadow:none;
      cursor:inherit;
    }
    .helpframe{
      display:none;
      border-radius: 5px; 
      -moz-border-radius: 5px; 
      -webkit-border-radius: 5px; 
      border: 1px solid #c0c0c0;
      color:black;
      padding:5px;
      width:95%;
      margin-top:2px;
      overflow: hidden;
    }
    .helpframe{ /* temporary disable */
      border:none;
      width:100%;
      padding:0px;
    }
    .helpframetitle{
      margin:-5px -5px 2px -5px;
      padding:2px 0px;
      background-color:#f0f0f0;
      text-align:right;
      display:none;/* temporary disable */
    }
    .helpframetitle .closebtn{
      color:#000000;
      margin-right:4px;
      padding: 0px 2px;
      font-weight:bold;
      text-decoration:none;
    }
    .helpframetitle .closebtn:hover{
      color:#f0f0f0;
      background-color:#0c0c0c;
      margin-right:4px;
      padding: 1px 3px;
      font-weight:bold;
      text-decoration:none;
    }
    .helppos{
      display:none;
      position:absolute;
      z-index:99;
      background-color:black;
      color:white;
      padding:5px;
      margin-right:10px;
      overflow: hidden;
      opacity:0;
    }
    .helpcontent{
      overflow:hidden;
    }
    #helps{
      position:absolute;
      left:-500px;
      top:-10000px;
      padding:5px;
      visibility:hidden;
      width:80%;
      overflow:hidden;
    }
    #helps table td,.helpcontent table td{
      padding:2px 10px;
    }
    #helps table th,.helpcontent table th{
      vertical-align:top;
      padding:2px;
      border-bottom:solid 1px #ebebeb;
    }
    #helps p,.helpcontent p{
      margin-top:1px;
    }
    /* end of help */
    
    /* make option be easier to click */
    option{
      padding:2px;
      border-bottom:solid 1px white;
    }
    option.option-label+option{
      border-bottom:solid 1px #d0d0d0;
    }
    option.option-label+option:last-child{
      border-bottom:solid 1px white;
    }
    .flat-btn-box{
      height:90px;
      width:255px;
    }
    .flat-btn{
      outline:#c0c0c0 solid thin;
      display:inline-block;
      float:left;
      width:25px;
      height:25px;
      line-height:25px;
      margin:2px;
      cursor:pointer;
      text-align:center;
    }
    .flat-btn-zoomin{
      display:none;
      position:absolute;
      border:solid 3px #4d90fe;
      height:45px;
      width:60px;
      z-index:99;
      background-color:white;
      font-size:1.75em;
      text-align:center;
      line-height:45px;
    }
    /*loading */
    #loading{
      display:none;
      position:absolute;
      height:100px;
      min-height: 100px;
      top:40%;
      left:5%;
      right:5%;
      width:60%;
      margin:auto;
      text-align:center;
      background-color:rgba(255,255,255,0.85);
      z-index:99;
    }
    #loading div{
      padding: 0px 0px 30px 0px;
      background-image: url('data:image/gif;base64,R0lGODlhEAALAPQAAP///wAAANra2tDQ0Orq6gYGBgAAAC4uLoKCgmBgYLq6uiIiIkpKSoqKimRkZL6+viYmJgQEBE5OTubm5tjY2PT09Dg4ONzc3PLy8ra2tqCgoMrKyu7u7gAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCwAAACwAAAAAEAALAAAFLSAgjmRpnqSgCuLKAq5AEIM4zDVw03ve27ifDgfkEYe04kDIDC5zrtYKRa2WQgAh+QQJCwAAACwAAAAAEAALAAAFJGBhGAVgnqhpHIeRvsDawqns0qeN5+y967tYLyicBYE7EYkYAgAh+QQJCwAAACwAAAAAEAALAAAFNiAgjothLOOIJAkiGgxjpGKiKMkbz7SN6zIawJcDwIK9W/HISxGBzdHTuBNOmcJVCyoUlk7CEAAh+QQJCwAAACwAAAAAEAALAAAFNSAgjqQIRRFUAo3jNGIkSdHqPI8Tz3V55zuaDacDyIQ+YrBH+hWPzJFzOQQaeavWi7oqnVIhACH5BAkLAAAALAAAAAAQAAsAAAUyICCOZGme1rJY5kRRk7hI0mJSVUXJtF3iOl7tltsBZsNfUegjAY3I5sgFY55KqdX1GgIAIfkECQsAAAAsAAAAABAACwAABTcgII5kaZ4kcV2EqLJipmnZhWGXaOOitm2aXQ4g7P2Ct2ER4AMul00kj5g0Al8tADY2y6C+4FIIACH5BAkLAAAALAAAAAAQAAsAAAUvICCOZGme5ERRk6iy7qpyHCVStA3gNa/7txxwlwv2isSacYUc+l4tADQGQ1mvpBAAIfkECQsAAAAsAAAAABAACwAABS8gII5kaZ7kRFGTqLLuqnIcJVK0DeA1r/u3HHCXC/aKxJpxhRz6Xi0ANAZDWa+kEAA7AAAAAAAAAAAA');
      background-repeat:no-repeat;
      background-position:center;
    }
    #loading-text{
      font-size:16px;
    }
    
    .modal-dialog{
      display:none;
      position:absolute;
      top:40%;
      left:5%;
      right:5%;
      width:70%;
      margin:auto;
      min-height:200px;
      z-index:99;
      box-shadow: 0 4px 16px rgba(0,0,0,.2);
      background: #fff;
      background-clip: padding-box;
      border: 1px solid #acacac;
      border: 1px solid rgba(0,0,0,.333);
      outline: 0;
      position: absolute;
      color: #000;
      padding: 15px 21px;
      font-size:14px;
    }
    .modal-dialog button{
      -webkit-border-radius: 2px;
      -moz-border-radius: 2px;
      border-radius: 2px;
      background-color: #f5f5f5;
      /*
      background-image: -webkit-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -moz-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -ms-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: -o-linear-gradient(top,#f5f5f5,#f1f1f1);
      background-image: linear-gradient(top,#f5f5f5,#f1f1f1);
      color: #333;
      */
      border: 1px solid #dcdcdc;
      border: 1px solid rgba(0,0,0,0.1);
      cursor: default;
      font-family: inherit;
      font-size: 11px;
      font-weight: bold;
      height: 29px;
      line-height: 27px;
      margin:0;
      min-width: 72px;
      outline: 0;
      padding: 0 8px;  
    }
    .modal-dialog .title{
      font-weight:bold;
    }
    .modal-dialog .buttons{
        position: absolute;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
    }
    .modal-dialog button+button{
      margin-left:20px;
    }
    .modal-dialog .x{
      font-weight: bold;
      text-align: right;
      margin-top: -5px;
      margin-right: -5px;
      color: #a0a0a0;
      cursor:pointer;
    }
    /* end of loading */
    .tab.accounts .content table{
      border: solid 1px #c0c0c0;
      width:100%;
      margin-bottom:10px;
      margin-top: 30px;
    }
    .tab.accounts .content table tr:nth-child(odd){
      background-color:#f0f0f0;
    }
    .tab.accounts .content table tr:first-child{
      background-color:white;
    }
    .tab.accounts .content table tr td{
      padding-left: 10px;
    }
    .tab.accounts .content table tr th{
      padding-left: 10px;
      padding-top: 10px;
    }
    </style>
      </head>
      <body>
    <div class="sidebar" style="padding:5px 1px;margin:-8px;height:100%;overflow:hidden">
      <div class="tab-title-bar" style="">
        <div class="tab-title active" tab="t1" onclick="setActiveTab('t1')"><span class="i18n">Accounts</span></div>
        <div class="tab-title" tab="t2" onclick="setActiveTab('t2')"><span class="i18n">Document</span></div>
        <div class="tab-title" tab="t3" onclick="setActiveTab('t3')"><span class="i18n">About</span></div>
      </div>
      <div class="tab accounts active" tab="t1" style=""><div class="content"></div></div>
      <div class="tab" tab="t2">
          <div class="block form-group" style="padding-top:20px;height:400px;position:relative">
            <h3>When converting tables in this document "<span class="doc-name"></span>"</h3>
            <div>
              <input type="radio" name="html-table" id="html-table-0" value="0" checked>
              <label class="help" helpname="tbl" helptype="hover" for="html-table-0">with pure reStructuredText markups</label>
            </div>
            <div style="margin-top:10px">
              <input type="radio" name="html-table" id="html-table-1" value="1">
              <label class="help" helpname="tbl" helptype="hover" for="html-table-1">
              with HTML tags
              </label>
              <p style="padding-left:25px;margin-top:5px">
              This option would generate table with HTML &lt;TABLE&gt;. Useful for those who utilizes the readthedocs.org as a blog system.
              <a href="http://ggeditor.readthedocs.io/en/latest/table_in_html.html" target="_blank">Details ...</a>
              </p>
            </div>
          </div>
      </div>
      <div class="tab" tab="t3">
        <div style="padding-top:20px;height:400px;position:relative">
          <p>
             The "Reset" button will clean up all your stored information of accounts and bindings.
             <br/><button class="red" onclick="reset_all()" style="margin-top:20px;clear:both">Reset</button>
          </p>
          <p style="position:absolute;bottom:0">Version: 2018-04-01</p>
        </div>
      </div>
      <!--end of tab-->
    </div>
    <div class="masterhelpframe helpframe">
      <div class="helpframetitle">
        <a class="closebtn" onclick="closeHelp(this)">×</a>
      </div>
      <div class="helpcontent"></div>
    </div>
    
    <div id="loading" class="modal-dialog">
      <div>
        <h1><label class="i18n" id="loading-text"></label></h1>
      </div>
    </div>
    <div id="dialog" class="modal-dialog">
      <div style="width:100%">
        <div class="x">x</div>
        <p class="title"></p>
        <p class="content"></p>
        <div class="buttons">
          <button class="yes i18n blue">Delete</button><button class="cancel i18n">Cancel</button>
        </div>
      </div>
    </div>
    <span class="helppos" id="helppostmpl" style="display:none"></span>
    <span id="helppostmplpt" style="display:none;position:absolute">▲</span>
    <div style="display:none">
      <div id="helps">
        <div name="gen"></div>
      </div>
    </div>
    <script language="javascript">
    document.addEventListener( "DOMContentLoaded", initialization , false );
    
    function initialization(){
      enableHelp()
      renderPage()
    }
    
    
    /*
     * lib functions starts below
     * 
     */
    var serverValues={locale:'en'};
    function localI18n(s){
      return s
    }
    function setActiveTab(name){
      var tabs = document.querySelectorAll('.tab')
      for (var i=0;i<tabs.length;i++){
        tabs[i].className = tabs[i].className.replace(/ active/,'');
        if (tabs[i].getAttribute('tab')==name){
          tabs[i].className+=' active'
        }
      }
      var titles = document.querySelectorAll('.tab-title')
      for (var i=0;i<titles.length;i++){
        if (titles[i].getAttribute('tab')==name){titles[i].className='tab-title active'}
        else titles[i].className='tab-title';
      }
    }
    
    function getTimestamp(){
      var now = new Date()
      return now.getFullYear()+'-'+(now.getMonth()+1)+'-'+now.getDate()+' '+now.getHours()+':'+now.getMinutes()+':'+now.getSeconds()
    }
    function getViewportSize(){
      var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
      var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
      return {width:w,height:h}
    }
    function moveElementToViewportCenter(ele) {
        var size = getViewportSize()
        var rect = ele.getBoundingClientRect()
        ele.style.top =  Math.round(size.height/2 - rect.height/2)+'px'
        ele.style.marginLeft = Math.round(size.width/2  - rect.width/2)+'px'
    }
    
    var loadingCount=0;
    function loading(yes,label){
      var title = localI18n('Please be waiting...');
    
      if (yes && typeof(yes)=='string') title = yes
    
      if ((loadingCount<0 && !yes) || (loadingCount>0 && yes)) {
        if (title) {
          document.getElementById('loading-text').innerHTML = title;
        }
        loadingCount += yes ? 1 : -1;
        return;
      }
      loadingCount += yes ? 1 : -1;
      var loadingDiv = document.getElementById('loading')
      if (loadingCount==1){
        // start loading
        loadingDiv.style.display='flex';
        document.getElementById('loading-text').innerHTML = title;
        document.querySelector('.sidebar').style.opacity = 0.5;
        moveElementToViewportCenter(loadingDiv)
      }
      else{
        // stop loading
        loadingDiv.style.display='none';
        document.querySelector('.sidebar').style.opacity = 1;
      }
    }
    function stopLoading(label){loading(false,label)}
    function setLoadingTitle(title){document.getElementById('loading-text').innerHTML = title;}
    
    function myConfirm(title,options,callback){
      /*
       * options {
       *     button:{
       *            yes:{
       *                className:'red'
       *                }
       *            }
       *     }
       * }
       */
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'  
      dialog.style.display='block';
      //dialog.style.top = (window.pageYOffset+150)+'px'
      document.querySelector('.sidebar').style.opacity = 0.5;
      moveElementToViewportCenter(dialog)
      if (options && options.button && options.button.yes && options.button.yes.className) dialog.querySelector('.yes').className += ' '+options.button.yes.className
      var cleanup = function(yes){
        callback(yes)
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.cancel').onclick = null;
        document.querySelector('.sidebar').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        dialog.style.top = '0px';
        document.querySelector('.sidebar').style.opacity = 1; 
      }
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.cancel').onclick = function(){
        cleanup(false);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      setTimeout(function(){
        document.querySelector('.sidebar').onclick = function(){
          cleanup(false);
        } 
      },100)
    }
    function myAlert(title,callback,autoCloseInterval){
      if (!callback) callback = function(){}
      var dialog = document.getElementById('dialog')
      dialog.querySelector('.title').innerHTML = title;
      dialog.querySelector('.content').style.display = 'none'
      dialog.querySelector('.buttons').innerHTML = '<button class="yes i18n">YES</button><button class="cancel i18n">Cancel</button>'
      dialog.style.display='block';
      //dialog.style.top = (window.pageYOffset+150)+'px'
      var sidebar = document.querySelector('.sidebar')
      if (sidebar) sidebar.style.opacity = 0.5;
      var yesHTML = dialog.querySelector('.yes').innerHTML
      var autoCloseTimer = 0
      var cleanup = function(yes){
        callback(yes)
        if (autoCloseTimer) clearTimeout(autoCloseTimer)
        if (sidebar) sidebar.onclick = null
        dialog.querySelector('.yes').onclick = null;
        dialog.querySelector('.x').onclick = null;
        dialog.querySelector('.cancel').style.display = ''
        dialog.querySelector('.yes').innerHTML = yesHTML
        dialog.querySelector('.title').innerHTML = '';
        dialog.style.display='none';
        if (sidebar) sidebar.style.opacity = 1; 
      }
      dialog.querySelector('.cancel').style.display = 'none'
      dialog.querySelector('.yes').innerHTML = 'OK'
    
      moveElementToViewportCenter(dialog)
      dialog.querySelector('.yes').onclick = function(){
        cleanup(true);
      }
      dialog.querySelector('.x').onclick = function(){
        cleanup(false);
      }
      // click outside dialog also close the dialog
      setTimeout(function(){
        if (sidebar) sidebar.onclick = function(){
          cleanup(false);
        } 
      },100)
      // auto close dialog
      if (autoCloseInterval){
        autoCloseTimer = setTimeout(function(){
          autoCloseTimer = 0
          cleanup(false)
        },autoCloseInterval)
      }
    }
    
    function myPrompt(title,options,callback){
        /*
         * options = {
         *     value*:(string) value of the input element
         *     placeholder*:(string) default null
         *     content*:(string) default "<input style="width:100%;height:40px;font-size:1.5em">"
         *     button:*(dict){ok:{className:<class name>},cancel:{className:<class name>}}, default null     
         * }
         */
        var dialog = document.getElementById('dialog')
        dialog.querySelector('.title').innerHTML = title;
        dialog.querySelector('.content').innerHTML = (options.content || '<input style="width:100%;height:40px;font-size:1.5em">')
        dialog.querySelector('.content').style = 'block'
        dialog.querySelector('.buttons').style = 'block'
        var input = dialog.querySelector('.content input')
        if (options.placeholder) input.setAttribute('placeholder',options.placeholder)
        if (options.value) input.value = options.value
        var buttons = [
            '<button class="ok'+((options.button && options.button.ok && options.button.ok.className) ? ' '+options.button.ok.className : '' )+'">OK</button>',
            '<button class="cancel'+((options.button && options.button.cancel && options.button.cancel.className) ? ' '+options.button.cancel.className : '' )+'">Cancel</button>',
            ]
        dialog.querySelector('.buttons').innerHTML = buttons.join('') //#195
        var sidebar = document.querySelector('.sidebar')
        var cleanup = function(value){
          if (sidebar) sidebar.style.opacity = 1; 
          if (sidebar) sidebar.onclick = null
          if (dialog.querySelector('.cancel')) dialog.querySelector('.cancel').onclick = null;
          if (dialog.querySelector('.x'))dialog.querySelector('.x').onclick = null;
          if (dialog.querySelector('.ok')) dialog.querySelector('.ok').onclick = null;
          dialog.querySelector('.buttons').innerHTML = ''
          dialog.querySelector('.content').innerHTML = ''
          dialog.querySelector('.title').innerHTML = ''
          dialog.style.display='none';
          callback(value)
        }
        setTimeout(function(){
          dialog.querySelector('.x').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.cancel').onclick = function(){
                  cleanup(null)
          }
          dialog.querySelector('.ok').onclick = function(){
              var text = dialog.querySelector('input').value || (options.defaultText || '')
              cleanup(text)
          }
        },500)
        if (sidebar) sidebar.style.opacity = 0.5;
        dialog.style.display = 'block'
        dialog.style.height = '200px'
        moveElementToViewportCenter(dialog)
        // click outside dialog also close the dialog
        setTimeout(function(){
          document.querySelector('.sidebar').onclick = function(){
            cleanup(false);
          } 
        },100)
        return {dom:dialog,callback:callback}
    }
    
    /* start of help system */
    function enableHelp(){
      var helps =  document.querySelectorAll('.help');
      var timer = 0,delay = 1000,hoverDelay=1000;
      for (var i=0,l=helps.length;i<l;i++){
        var hoverType = helps[i].getAttribute('helptype')=='hover';
        helps[i].onmouseover = function(evt){
          var target = evt.currentTarget
          var helpname = target.getAttribute('hoverhelpname') || target.getAttribute('helpname')
          // check if the same help is openning
          if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) {
            return;
          }
          if (timer>0) clearTimeout(timer);
          timer = setTimeout(function(){
            timer = 0;
            showHelp(helpname,target.getAttribute('helpCloseByBtn'),target.getAttribute('helptype'))
          },(hoverType ? hoverDelay : delay))
        }
        if (hoverType){
          helps[i].onmouseout = function(evt){
            if (timer){
              //give up to show it
              clearTimeout(timer);timer = 0;
            }
            else{
              closeHoverHelp();
            }
          }
        }
        else{
          // cancel the help showup
          helps[i].onmouseout = function(evt){
            if (timer){
              clearTimeout(timer);timer = 0;
            }
          }
        }
      }
    }
    
    function getOffset( el ) {
        var _x = 0;
        var _y = 0;
        while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
            _x += el.offsetLeft //- el.scrollLeft;
            _y += el.offsetTop //- el.scrollTop;
            el = el.offsetParent;
        }
        return { top: _y, left: _x };
    }
    function showHelp(helpname,helpCloseByBtn,helpType){
    
      /* simply deal with hover help */
      if (helpType=='hover'){
          var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
          var tmpl = document.getElementById('helppostmpl')
          var c = document.querySelector('#helps div[name="'+helpname+'"]');
          // make it visible
          var sidebarRect = document.querySelector('.sidebar').getBoundingClientRect()
          var sidebarWidth = sidebarRect.right - sidebarRect.left;
          tmpl.style.display='inline-block';
          tmpl.style.position = 'absolute';
          tmpl.style.zIndex = 99;
          var target = document.querySelector('.help[hoverhelpname="'+helpname+'"][helptype="hover"]');
          if (!target) target = document.querySelector('.help[helpname="'+helpname+'"][helptype="hover"]');
          var targetRect = target.getBoundingClientRect()
          var targetHeight = targetRect.bottom - targetRect.top;
          var targetWidth = targetRect.right - targetRect.left;
          var rect = getOffset(target)
          tmpl.style.top = (rect.top + targetHeight+4)+'px'
          tmpl.style.opacity = 0;
          tmpl.innerHTML= c.innerHTML;
          tmpl.style.maxWidth = Math.floor(sidebarWidth * 0.8)+'px'
          var tmplRect = tmpl.getBoundingClientRect()
          var tmplWidth = tmplRect.right - tmplRect.left
          var p0 = Math.floor(sidebarWidth * 0.1);
          var p1 = Math.floor(sidebarWidth * 0.9);
          var tmplpt = document.getElementById('helppostmplpt')
          tmplpt.style.top = (parseInt(tmpl.style.top)-10)+'px';
          if (rect.left < p0){
            tmpl.style.left = rect.left+'px'
            tmplpt.style.left = tmpl.style.left;
          }
          else if (rect.left+targetWidth > p1) {
            tmpl.style.left = Math.floor((rect.left+targetWidth - tmplWidth))+'px'
            tmplpt.style.left = Math.floor(parseInt(tmpl.style.left)+tmplWidth-18)+'px';
          }
          else {
            tmpl.style.left = Math.max(0,Math.floor(rect.left+targetWidth/2-tmplWidth/2))+'px'
            tmplpt.style.left = Math.max(0,Math.floor(parseInt(tmpl.style.left)+tmplWidth/2-6))+'px'
          }
          tmpl.setAttribute('active',1);
          setTimeout(function(){
            //starts animation
            tmpl.style.opacity=1;
            tmplpt.style.display='';
          },1)
        return;
      }
    
      /* need to check again for some help is triggered manually */
      if (document.querySelector('.helpframe[helpname="'+helpname+'"]')) return;//already opened
      /* one help only, unless the existing help is a modal help */
      closeHelp()
      // create a new helpframe  
      /* prepare for animation */
      // clone the masterhelpframe  
      var helpframe = document.querySelector('.masterhelpframe.helpframe').cloneNode(true);
      helpframe.className = 'helpframe';
    
      helpframe.style.display = 'block';
      helpframe.setAttribute('helpname',helpname)
      var trigger = function(){    
        //var helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpname = this._helpname; 
        if (helpCloseByBtn) helpframe.setAttribute('modal',1)
        helpframe.querySelector('.closebtn').setAttribute('helpname',helpname)
        var cele = helpframe.querySelector('.helpcontent')
        /* find the insert position */
        var helppos = document.querySelector('.helppos[helpname="'+helpname+'"]');
        helppos.parentNode.insertBefore(helpframe, helppos.nextSibling);
        /* find the help content to insert */
        var c = document.querySelector('#helps div[name="'+helpname+'"]');
        /* insert the help content */
        cele.appendChild(c);//move it
        /* starts the animation to show up*/
        var titleheight = helpframe.querySelector('.helpframetitle').clientHeight;
        /* make the helpframe visible, delay to wait the DOM been refreshed */
        setTimeout(function(){
          // scroll to make it visible
          var y = getOffset( helpframe ).top; 
          var offset = y-window.scrollY;
          if (offset<0 || offset > window.innerHeight)  window.scrollTo(0,Math.max(0,y-50));      
    
          //trigger event
          var e = document.createEvent('Event');
          e.initEvent('help-open-'+helpname,false,true);
          document.dispatchEvent(e);
    
        },100);
      }
      setTimeout(function(){trigger.apply({_helpname:helpname})},1)
    }
    
    function closeHoverHelp(){
      /* find the insert position */
      var helppos = document.querySelector('.helppos[active]');
      if (helppos===null) return;
      helppos.innerHTML='';
      // make it invisible
      helppos.style.display='none';
      helppos.style.opacity=0;
      helppos.removeAttribute('active');
      var tmplpt = document.getElementById('helppostmplpt')
      tmplpt.style.display='none';
    }
    function closeHelp(btn){
      /* release the body click */
      document.body.onclick = null;
    
      var helpname = null,helpframe=null;
      if (btn) {
        helpname = btn.getAttribute('helpname');
        helpframe = document.querySelector('.helpframe[helpname="'+helpname+'"]');
        helpframe.removeAttribute('modal')//enforce to close by btn
        //fire event if closed by button
        var e = document.createEvent('Event');
        e.initEvent('help-close-'+helpname,false,true);
        document.dispatchEvent(e);
      }
      else {
        helpframe = document.querySelector('.helpframe[helpname]');
        if (!helpframe) return true;//no helpframe is showing    
        helpname = helpframe.getAttribute('helpname');
      }
      if (helpframe.getAttribute('modal')) return false
      var cele = helpframe.querySelector('.helpcontent')
      if (cele.firstChild != null){
        /*cele.removeChild(cele.firstChild);*/
        //move back to helps
        document.getElementById('helps').appendChild(cele.firstChild);    
      }
      helpframe.style.display = 'none';
      helpframe.parentNode.removeChild(helpframe);
      return true;
    }
    /* end of help system */
    
    /* application starts */
    var userCredentials;
    function Credentials(username,password){
      this.username = username
      this.password = password
      this.key = username.toUpperCase()
      if (this.password) this.encrypt()
    }
    Credentials.prototype = {
      encrypt:function(){
        this.encrypted = JSON.stringify(sjcl.encrypt(this.key,this.password))
      },
      decrypt:function(encrypted){
        try{
          this.password = sjcl.decrypt(this.key,JSON.parse(encrypted))
          this.encrypted = encrypted
          return true
        }
        catch(e){
          this.password = ''
          this.encrypted = ''
          return false
        }
      }
    }
    
    var userProperties = null
    function renderPage(){
      var done = function(obj){
        stopLoading()
        userProperties = obj
    
        document.querySelectorAll('.doc-name').forEach(function(ele){
          ele.innerText = userProperties.doc.name
        })
    
        // render doc preferences
        if (userProperties.doc.preferences){
          document.getElementById('html-table-1').checked = userProperties.doc.preferences.htmlTable ? true : false
          document.getElementById('html-table-0').checked = !document.getElementById('html-table-1').checked
        }
        var toggle_html_table = function(evt){
          var value = document.getElementById('html-table-1').checked
          userProperties.doc.preferences.htmlTable = value
          loading(true)
          google.script.run.withSuccessHandler(stopLoading).withFailureHandler(stopLoading).setDocPreferences(userProperties.doc.preferences);  
        }
        document.querySelectorAll('input[name="html-table"]').forEach(function(ele){
          ele.onclick = toggle_html_table
        })
    
        if (userProperties.credentialsArray){
          // upgraded user
        }
        else if (typeof(userProperties.githubCredentials.forEach)=='undefined'){
          //single-account settings
          userProperties.credentialsArray = [userProperties.githubCredentials]
          delete userProperties.githubCredentials
        }
        else{
          // new users
          userProperties.credentialsArray = []    
        }
        var credentialsArray = []
        userProperties.credentialsArray.forEach(function(item){
          var userCredentials = new Credentials(item.username,'')
          if (item.password){
            if (!userCredentials.decrypt(item.password)){
              userCredentials.password = ''
            }
          }
          credentialsArray.push(userCredentials)
        })
        userProperties.credentialsArray = credentialsArray
        renderAccountPanel()
      }
      loading(true)
      google.script.run.withSuccessHandler(done).withFailureHandler(stopLoading).getUserProperties();  
    }
    function updateAccountToServer(callback){
      //update to server
      var credentialsArray = []
      userProperties.credentialsArray.forEach(function(item){
        credentialsArray.push({type:'Github',username:item.username, password:item.encrypted})
      })
      loading(true)
      google.script.run.withSuccessHandler(function(){
        stopLoading()
        callback(true)
      }).withFailureHandler(function(err){
      stopLoading()
        myAlert(err)
        callback(false)
      }).setCredentialsArray(credentialsArray)        
    }
    
    
    function reset_all(){
      myConfirm('Are you sure to reset?',{button:{yes:{className:'red'}}},function(yes){
        if (!yes) return
        loading(true)
        google.script.run.withSuccessHandler(function(){
          stopLoading()
          myAlert('Reset success',function(){
            google.script.host.close() 
          })
    
        }).withFailureHandler(function(err){
        stopLoading()
          myAlert(err)
        }).resetProperties()  
      })
    }
    function renderAccountPanel(){
      //get initial state
      var state = document.querySelector('.tab.accounts .content table #toggle-password-btn') ? document.querySelector('.tab.accounts .content table #toggle-password-btn').getAttribute('state') : '0'
    
      var html = []
      html.push('<table><tr><th>Type</th><th>Username</th><th>Password</th><th colspan="2"><a href="#" id="toggle-password-btn" state="'+state+'">'+(state=='0' ? 'Show' : 'Hide')+' password</a></th></tr>')
      userProperties.credentialsArray.forEach(function(userCredentials,idx){
        html.push('<tr><td>Github</td><td>'+userCredentials.username+'</td><td class="password-cell" value="'+userCredentials.password+'"><a href="#" class="chgpwd" value="'+idx+'">'+(state=='0' ? '********' : userCredentials.password)+'</td><td><a href="#" class="delete" value="'+idx+'">Delete</a></td>')
        html.push('</tr>')
      })
      html.push('</table>')
      html.push('<div><a href="#" class="add">+ Add Account</a></div>')
      document.querySelector('.tab.accounts .content').innerHTML = html.join('')
      // assign callbacks
      var chgpwd = function(evt){
        evt.preventDefault()
        var credentials = userProperties.credentialsArray[parseInt(evt.currentTarget.getAttribute('value'))]
        myPrompt('New Password for '+credentials.username,{button:{ok:{className:'blue'}}},function(newPassword){
          if (!newPassword) return;
          credentials.password = newPassword
          credentials.encrypt()
          updateAccountToServer(function(success){
            if (success) renderAccountPanel()
          })
        })
      }
      document.querySelectorAll('.tab.accounts .content table a.chgpwd').forEach(function(ele){
        ele.onclick = chgpwd
      })
      // assign callbacks
      var delAccount = function(evt){
        evt.preventDefault()
        var idx = parseInt(evt.currentTarget.getAttribute('value'))
        var credentials = userProperties.credentialsArray[idx]
        myConfirm('Delete '+credentials.username+'?',{button:{yes:{className:'red'}}},function(yes){
          if (!yes) return;
          //credentials.password = newPassword
          //update to server
          userProperties.credentialsArray.splice(idx,1)
          updateAccountToServer(function(){
            setTimeout(function(){myAlert(credentials.username+' has eleted')},100)
            renderAccountPanel()
          })
        })
      }
      document.querySelector('.tab.accounts .content table #toggle-password-btn').onclick = function(evt){
        evt.preventDefault()
        var state = evt.currentTarget.getAttribute('state')
        state = state=='0' ? '1' : '0'
        evt.currentTarget.setAttribute('state',state)
        evt.currentTarget.innerText = state=='0' ? 'Show password' : 'Hide password'
        document.querySelectorAll('.tab.accounts .content table .password-cell a').forEach(function(a){
          a.innerText = state=='0' ? '********' : a.parentNode.getAttribute('value')
        })
      }
      document.querySelectorAll('.tab.accounts .content table a.delete').forEach(function(ele){
        ele.onclick = delAccount
      })
      document.querySelectorAll('.tab.accounts .content a.add').forEach(function(ele){
        ele.onclick = function(evt){
          evt.preventDefault()
          var form = '<table style="width:100%"><tr><td>Username</td><td><input style="width:100%" id="add-account-username"></td></tr><tr><td>Password</td><td><input type="password" id="add-account-password1"></td></tr><tr><td>Password again</td><td><input type="password" id="add-account-password2"></td></tr></table>'
          var ret = myPrompt('Add Account',{content:form,button:{ok:{className:'blue'}}},function(){
          })
          ret.dom.style.height = '300px'
          setTimeout(function(){
            var origin_ok = ret.dom.querySelector('.ok').onclick
            ret.dom.querySelector('.ok').onclick = function(evt){
              evt.preventDefault()
              var username = ret.dom.querySelector('#add-account-username').value
              if (!username) {
                myAlert('No username')
                origin_ok()
                return
              }
              var pwd1=ret.dom.querySelector('#add-account-password1').value
              var pwd2=ret.dom.querySelector('#add-account-password2').value        
              if (pwd1 && pwd1!=pwd2){
                alert('Two passwords dismatch!')
                return
              }
              // ok
              var credentials = new Credentials(username, pwd1)
              userProperties.credentialsArray.push(credentials)
              origin_ok()
              // update to server
              updateAccountToServer(function(success){
                 renderAccountPanel()
              })
            }
          },750)
        }
      })
    }
    </script>
    <script language="javascript">
    "use strict";var sjcl={cipher:{},hash:{},mode:{},misc:{},codec:{},exception:{corrupt:function(a){this.toString=function(){return"CORRUPT: "+this.message};this.message=a},invalid:function(a){this.toString=function(){return"INVALID: "+this.message};this.message=a},bug:function(a){this.toString=function(){return"BUG: "+this.message};this.message=a},notReady:function(a){this.toString=function(){return"NOT READY: "+this.message};this.message=a}}};
    sjcl.cipher.aes=function(a){this.h[0][0][0]||this.z();var b,c,d,e,f=this.h[0][4],g=this.h[1];b=a.length;var h=1;if(b!==4&&b!==6&&b!==8)throw new sjcl.exception.invalid("invalid aes key size");this.a=[d=a.slice(0),e=[]];for(a=b;a<4*b+28;a++){c=d[a-1];if(a%b===0||b===8&&a%b===4){c=f[c>>>24]<<24^f[c>>16&255]<<16^f[c>>8&255]<<8^f[c&255];if(a%b===0){c=c<<8^c>>>24^h<<24;h=h<<1^(h>>7)*283}}d[a]=d[a-b]^c}for(b=0;a;b++,a--){c=d[b&3?a:a-4];e[b]=a<=4||b<4?c:g[0][f[c>>>24]]^g[1][f[c>>16&255]]^g[2][f[c>>8&255]]^
    g[3][f[c&255]]}};
    sjcl.cipher.aes.prototype={encrypt:function(a){return this.I(a,0)},decrypt:function(a){return this.I(a,1)},h:[[[],[],[],[],[]],[[],[],[],[],[]]],z:function(){var a=this.h[0],b=this.h[1],c=a[4],d=b[4],e,f,g,h=[],i=[],k,j,l,m;for(e=0;e<0x100;e++)i[(h[e]=e<<1^(e>>7)*283)^e]=e;for(f=g=0;!c[f];f^=k||1,g=i[g]||1){l=g^g<<1^g<<2^g<<3^g<<4;l=l>>8^l&255^99;c[f]=l;d[l]=f;j=h[e=h[k=h[f]]];m=j*0x1010101^e*0x10001^k*0x101^f*0x1010100;j=h[l]*0x101^l*0x1010100;for(e=0;e<4;e++){a[e][f]=j=j<<24^j>>>8;b[e][l]=m=m<<24^m>>>8}}for(e=
    0;e<5;e++){a[e]=a[e].slice(0);b[e]=b[e].slice(0)}},I:function(a,b){if(a.length!==4)throw new sjcl.exception.invalid("invalid aes block size");var c=this.a[b],d=a[0]^c[0],e=a[b?3:1]^c[1],f=a[2]^c[2];a=a[b?1:3]^c[3];var g,h,i,k=c.length/4-2,j,l=4,m=[0,0,0,0];g=this.h[b];var n=g[0],o=g[1],p=g[2],q=g[3],r=g[4];for(j=0;j<k;j++){g=n[d>>>24]^o[e>>16&255]^p[f>>8&255]^q[a&255]^c[l];h=n[e>>>24]^o[f>>16&255]^p[a>>8&255]^q[d&255]^c[l+1];i=n[f>>>24]^o[a>>16&255]^p[d>>8&255]^q[e&255]^c[l+2];a=n[a>>>24]^o[d>>16&
    255]^p[e>>8&255]^q[f&255]^c[l+3];l+=4;d=g;e=h;f=i}for(j=0;j<4;j++){m[b?3&-j:j]=r[d>>>24]<<24^r[e>>16&255]<<16^r[f>>8&255]<<8^r[a&255]^c[l++];g=d;d=e;e=f;f=a;a=g}return m}};
    sjcl.bitArray={bitSlice:function(a,b,c){a=sjcl.bitArray.P(a.slice(b/32),32-(b&31)).slice(1);return c===undefined?a:sjcl.bitArray.clamp(a,c-b)},concat:function(a,b){if(a.length===0||b.length===0)return a.concat(b);var c=a[a.length-1],d=sjcl.bitArray.getPartial(c);return d===32?a.concat(b):sjcl.bitArray.P(b,d,c|0,a.slice(0,a.length-1))},bitLength:function(a){var b=a.length;if(b===0)return 0;return(b-1)*32+sjcl.bitArray.getPartial(a[b-1])},clamp:function(a,b){if(a.length*32<b)return a;a=a.slice(0,Math.ceil(b/
    32));var c=a.length;b&=31;if(c>0&&b)a[c-1]=sjcl.bitArray.partial(b,a[c-1]&2147483648>>b-1,1);return a},partial:function(a,b,c){if(a===32)return b;return(c?b|0:b<<32-a)+a*0x10000000000},getPartial:function(a){return Math.round(a/0x10000000000)||32},equal:function(a,b){if(sjcl.bitArray.bitLength(a)!==sjcl.bitArray.bitLength(b))return false;var c=0,d;for(d=0;d<a.length;d++)c|=a[d]^b[d];return c===0},P:function(a,b,c,d){var e;e=0;if(d===undefined)d=[];for(;b>=32;b-=32){d.push(c);c=0}if(b===0)return d.concat(a);
    for(e=0;e<a.length;e++){d.push(c|a[e]>>>b);c=a[e]<<32-b}e=a.length?a[a.length-1]:0;a=sjcl.bitArray.getPartial(e);d.push(sjcl.bitArray.partial(b+a&31,b+a>32?c:d.pop(),1));return d},k:function(a,b){return[a[0]^b[0],a[1]^b[1],a[2]^b[2],a[3]^b[3]]}};
    sjcl.codec.utf8String={fromBits:function(a){var b="",c=sjcl.bitArray.bitLength(a),d,e;for(d=0;d<c/8;d++){if((d&3)===0)e=a[d/4];b+=String.fromCharCode(e>>>24);e<<=8}return decodeURIComponent(escape(b))},toBits:function(a){a=unescape(encodeURIComponent(a));var b=[],c,d=0;for(c=0;c<a.length;c++){d=d<<8|a.charCodeAt(c);if((c&3)===3){b.push(d);d=0}}c&3&&b.push(sjcl.bitArray.partial(8*(c&3),d));return b}};
    sjcl.codec.hex={fromBits:function(a){var b="",c;for(c=0;c<a.length;c++)b+=((a[c]|0)+0xf00000000000).toString(16).substr(4);return b.substr(0,sjcl.bitArray.bitLength(a)/4)},toBits:function(a){var b,c=[],d;a=a.replace(/\s|0x/g,"");d=a.length;a+="00000000";for(b=0;b<a.length;b+=8)c.push(parseInt(a.substr(b,8),16)^0);return sjcl.bitArray.clamp(c,d*4)}};
    sjcl.codec.base64={F:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",fromBits:function(a,b){var c="",d,e=0,f=sjcl.codec.base64.F,g=0,h=sjcl.bitArray.bitLength(a);for(d=0;c.length*6<h;){c+=f.charAt((g^a[d]>>>e)>>>26);if(e<6){g=a[d]<<6-e;e+=26;d++}else{g<<=6;e-=6}}for(;c.length&3&&!b;)c+="=";return c},toBits:function(a){a=a.replace(/\s|=/g,"");var b=[],c,d=0,e=sjcl.codec.base64.F,f=0,g;for(c=0;c<a.length;c++){g=e.indexOf(a.charAt(c));if(g<0)throw new sjcl.exception.invalid("this isn't base64!");
    if(d>26){d-=26;b.push(f^g>>>d);f=g<<32-d}else{d+=6;f^=g<<32-d}}d&56&&b.push(sjcl.bitArray.partial(d&56,f,1));return b}};sjcl.hash.sha256=function(a){this.a[0]||this.z();if(a){this.n=a.n.slice(0);this.i=a.i.slice(0);this.e=a.e}else this.reset()};sjcl.hash.sha256.hash=function(a){return(new sjcl.hash.sha256).update(a).finalize()};
    sjcl.hash.sha256.prototype={blockSize:512,reset:function(){this.n=this.N.slice(0);this.i=[];this.e=0;return this},update:function(a){if(typeof a==="string")a=sjcl.codec.utf8String.toBits(a);var b,c=this.i=sjcl.bitArray.concat(this.i,a);b=this.e;a=this.e=b+sjcl.bitArray.bitLength(a);for(b=512+b&-512;b<=a;b+=512)this.D(c.splice(0,16));return this},finalize:function(){var a,b=this.i,c=this.n;b=sjcl.bitArray.concat(b,[sjcl.bitArray.partial(1,1)]);for(a=b.length+2;a&15;a++)b.push(0);b.push(Math.floor(this.e/
    4294967296));for(b.push(this.e|0);b.length;)this.D(b.splice(0,16));this.reset();return c},N:[],a:[],z:function(){function a(e){return(e-Math.floor(e))*0x100000000|0}var b=0,c=2,d;a:for(;b<64;c++){for(d=2;d*d<=c;d++)if(c%d===0)continue a;if(b<8)this.N[b]=a(Math.pow(c,0.5));this.a[b]=a(Math.pow(c,1/3));b++}},D:function(a){var b,c,d=a.slice(0),e=this.n,f=this.a,g=e[0],h=e[1],i=e[2],k=e[3],j=e[4],l=e[5],m=e[6],n=e[7];for(a=0;a<64;a++){if(a<16)b=d[a];else{b=d[a+1&15];c=d[a+14&15];b=d[a&15]=(b>>>7^b>>>18^
    b>>>3^b<<25^b<<14)+(c>>>17^c>>>19^c>>>10^c<<15^c<<13)+d[a&15]+d[a+9&15]|0}b=b+n+(j>>>6^j>>>11^j>>>25^j<<26^j<<21^j<<7)+(m^j&(l^m))+f[a];n=m;m=l;l=j;j=k+b|0;k=i;i=h;h=g;g=b+(h&i^k&(h^i))+(h>>>2^h>>>13^h>>>22^h<<30^h<<19^h<<10)|0}e[0]=e[0]+g|0;e[1]=e[1]+h|0;e[2]=e[2]+i|0;e[3]=e[3]+k|0;e[4]=e[4]+j|0;e[5]=e[5]+l|0;e[6]=e[6]+m|0;e[7]=e[7]+n|0}};
    sjcl.mode.ccm={name:"ccm",encrypt:function(a,b,c,d,e){var f,g=b.slice(0),h=sjcl.bitArray,i=h.bitLength(c)/8,k=h.bitLength(g)/8;e=e||64;d=d||[];if(i<7)throw new sjcl.exception.invalid("ccm: iv must be at least 7 bytes");for(f=2;f<4&&k>>>8*f;f++);if(f<15-i)f=15-i;c=h.clamp(c,8*(15-f));b=sjcl.mode.ccm.H(a,b,c,d,e,f);g=sjcl.mode.ccm.J(a,g,c,b,e,f);return h.concat(g.data,g.tag)},decrypt:function(a,b,c,d,e){e=e||64;d=d||[];var f=sjcl.bitArray,g=f.bitLength(c)/8,h=f.bitLength(b),i=f.clamp(b,h-e),k=f.bitSlice(b,
    h-e);h=(h-e)/8;if(g<7)throw new sjcl.exception.invalid("ccm: iv must be at least 7 bytes");for(b=2;b<4&&h>>>8*b;b++);if(b<15-g)b=15-g;c=f.clamp(c,8*(15-b));i=sjcl.mode.ccm.J(a,i,c,k,e,b);a=sjcl.mode.ccm.H(a,i.data,c,d,e,b);if(!f.equal(i.tag,a))throw new sjcl.exception.corrupt("ccm: tag doesn't match");return i.data},H:function(a,b,c,d,e,f){var g=[],h=sjcl.bitArray,i=h.k;e/=8;if(e%2||e<4||e>16)throw new sjcl.exception.invalid("ccm: invalid tag length");if(d.length>0xffffffff||b.length>0xffffffff)throw new sjcl.exception.bug("ccm: can't deal with 4GiB or more data");
    f=[h.partial(8,(d.length?64:0)|e-2<<2|f-1)];f=h.concat(f,c);f[3]|=h.bitLength(b)/8;f=a.encrypt(f);if(d.length){c=h.bitLength(d)/8;if(c<=65279)g=[h.partial(16,c)];else if(c<=0xffffffff)g=h.concat([h.partial(16,65534)],[c]);g=h.concat(g,d);for(d=0;d<g.length;d+=4)f=a.encrypt(i(f,g.slice(d,d+4).concat([0,0,0])))}for(d=0;d<b.length;d+=4)f=a.encrypt(i(f,b.slice(d,d+4).concat([0,0,0])));return h.clamp(f,e*8)},J:function(a,b,c,d,e,f){var g,h=sjcl.bitArray;g=h.k;var i=b.length,k=h.bitLength(b);c=h.concat([h.partial(8,
    f-1)],c).concat([0,0,0]).slice(0,4);d=h.bitSlice(g(d,a.encrypt(c)),0,e);if(!i)return{tag:d,data:[]};for(g=0;g<i;g+=4){c[3]++;e=a.encrypt(c);b[g]^=e[0];b[g+1]^=e[1];b[g+2]^=e[2];b[g+3]^=e[3]}return{tag:d,data:h.clamp(b,k)}}};
    sjcl.mode.ocb2={name:"ocb2",encrypt:function(a,b,c,d,e,f){if(sjcl.bitArray.bitLength(c)!==128)throw new sjcl.exception.invalid("ocb iv must be 128 bits");var g,h=sjcl.mode.ocb2.B,i=sjcl.bitArray,k=i.k,j=[0,0,0,0];c=h(a.encrypt(c));var l,m=[];d=d||[];e=e||64;for(g=0;g+4<b.length;g+=4){l=b.slice(g,g+4);j=k(j,l);m=m.concat(k(c,a.encrypt(k(c,l))));c=h(c)}l=b.slice(g);b=i.bitLength(l);g=a.encrypt(k(c,[0,0,0,b]));l=i.clamp(k(l.concat([0,0,0]),g),b);j=k(j,k(l.concat([0,0,0]),g));j=a.encrypt(k(j,k(c,h(c))));
    if(d.length)j=k(j,f?d:sjcl.mode.ocb2.pmac(a,d));return m.concat(i.concat(l,i.clamp(j,e)))},decrypt:function(a,b,c,d,e,f){if(sjcl.bitArray.bitLength(c)!==128)throw new sjcl.exception.invalid("ocb iv must be 128 bits");e=e||64;var g=sjcl.mode.ocb2.B,h=sjcl.bitArray,i=h.k,k=[0,0,0,0],j=g(a.encrypt(c)),l,m,n=sjcl.bitArray.bitLength(b)-e,o=[];d=d||[];for(c=0;c+4<n/32;c+=4){l=i(j,a.decrypt(i(j,b.slice(c,c+4))));k=i(k,l);o=o.concat(l);j=g(j)}m=n-c*32;l=a.encrypt(i(j,[0,0,0,m]));l=i(l,h.clamp(b.slice(c),
    m).concat([0,0,0]));k=i(k,l);k=a.encrypt(i(k,i(j,g(j))));if(d.length)k=i(k,f?d:sjcl.mode.ocb2.pmac(a,d));if(!h.equal(h.clamp(k,e),h.bitSlice(b,n)))throw new sjcl.exception.corrupt("ocb: tag doesn't match");return o.concat(h.clamp(l,m))},pmac:function(a,b){var c,d=sjcl.mode.ocb2.B,e=sjcl.bitArray,f=e.k,g=[0,0,0,0],h=a.encrypt([0,0,0,0]);h=f(h,d(d(h)));for(c=0;c+4<b.length;c+=4){h=d(h);g=f(g,a.encrypt(f(h,b.slice(c,c+4))))}b=b.slice(c);if(e.bitLength(b)<128){h=f(h,d(h));b=e.concat(b,[2147483648|0,0,
    0,0])}g=f(g,b);return a.encrypt(f(d(f(h,d(h))),g))},B:function(a){return[a[0]<<1^a[1]>>>31,a[1]<<1^a[2]>>>31,a[2]<<1^a[3]>>>31,a[3]<<1^(a[0]>>>31)*135]}};sjcl.misc.hmac=function(a,b){this.M=b=b||sjcl.hash.sha256;var c=[[],[]],d=b.prototype.blockSize/32;this.l=[new b,new b];if(a.length>d)a=b.hash(a);for(b=0;b<d;b++){c[0][b]=a[b]^909522486;c[1][b]=a[b]^1549556828}this.l[0].update(c[0]);this.l[1].update(c[1])};
    sjcl.misc.hmac.prototype.encrypt=sjcl.misc.hmac.prototype.mac=function(a){a=(new this.M(this.l[0])).update(a).finalize();return(new this.M(this.l[1])).update(a).finalize()};
    sjcl.misc.pbkdf2=function(a,b,c,d,e){c=c||1E3;if(d<0||c<0)throw sjcl.exception.invalid("invalid params to pbkdf2");if(typeof a==="string")a=sjcl.codec.utf8String.toBits(a);e=e||sjcl.misc.hmac;a=new e(a);var f,g,h,i,k=[],j=sjcl.bitArray;for(i=1;32*k.length<(d||1);i++){e=f=a.encrypt(j.concat(b,[i]));for(g=1;g<c;g++){f=a.encrypt(f);for(h=0;h<f.length;h++)e[h]^=f[h]}k=k.concat(e)}if(d)k=j.clamp(k,d);return k};
    sjcl.random={randomWords:function(a,b){var c=[];b=this.isReady(b);var d;if(b===0)throw new sjcl.exception.notReady("generator isn't seeded");else b&2&&this.U(!(b&1));for(b=0;b<a;b+=4){(b+1)%0x10000===0&&this.L();d=this.w();c.push(d[0],d[1],d[2],d[3])}this.L();return c.slice(0,a)},setDefaultParanoia:function(a){this.t=a},addEntropy:function(a,b,c){c=c||"user";var d,e,f=(new Date).valueOf(),g=this.q[c],h=this.isReady(),i=0;d=this.G[c];if(d===undefined)d=this.G[c]=this.R++;if(g===undefined)g=this.q[c]=
    0;this.q[c]=(this.q[c]+1)%this.b.length;switch(typeof a){case "number":if(b===undefined)b=1;this.b[g].update([d,this.u++,1,b,f,1,a|0]);break;case "object":c=Object.prototype.toString.call(a);if(c==="[object Uint32Array]"){e=[];for(c=0;c<a.length;c++)e.push(a[c]);a=e}else{if(c!=="[object Array]")i=1;for(c=0;c<a.length&&!i;c++)if(typeof a[c]!="number")i=1}if(!i){if(b===undefined)for(c=b=0;c<a.length;c++)for(e=a[c];e>0;){b++;e>>>=1}this.b[g].update([d,this.u++,2,b,f,a.length].concat(a))}break;case "string":if(b===
    undefined)b=a.length;this.b[g].update([d,this.u++,3,b,f,a.length]);this.b[g].update(a);break;default:i=1}if(i)throw new sjcl.exception.bug("random: addEntropy only supports number, array of numbers or string");this.j[g]+=b;this.f+=b;if(h===0){this.isReady()!==0&&this.K("seeded",Math.max(this.g,this.f));this.K("progress",this.getProgress())}},isReady:function(a){a=this.C[a!==undefined?a:this.t];return this.g&&this.g>=a?this.j[0]>80&&(new Date).valueOf()>this.O?3:1:this.f>=a?2:0},getProgress:function(a){a=
    this.C[a?a:this.t];return this.g>=a?1:this.f>a?1:this.f/a},startCollectors:function(){if(!this.m){if(window.addEventListener){window.addEventListener("load",this.o,false);window.addEventListener("mousemove",this.p,false)}else if(document.attachEvent){document.attachEvent("onload",this.o);document.attachEvent("onmousemove",this.p)}else throw new sjcl.exception.bug("can't attach event");this.m=true}},stopCollectors:function(){if(this.m){if(window.removeEventListener){window.removeEventListener("load",
    this.o,false);window.removeEventListener("mousemove",this.p,false)}else if(window.detachEvent){window.detachEvent("onload",this.o);window.detachEvent("onmousemove",this.p)}this.m=false}},addEventListener:function(a,b){this.r[a][this.Q++]=b},removeEventListener:function(a,b){var c;a=this.r[a];var d=[];for(c in a)a.hasOwnProperty(c)&&a[c]===b&&d.push(c);for(b=0;b<d.length;b++){c=d[b];delete a[c]}},b:[new sjcl.hash.sha256],j:[0],A:0,q:{},u:0,G:{},R:0,g:0,f:0,O:0,a:[0,0,0,0,0,0,0,0],d:[0,0,0,0],s:undefined,
    t:6,m:false,r:{progress:{},seeded:{}},Q:0,C:[0,48,64,96,128,192,0x100,384,512,768,1024],w:function(){for(var a=0;a<4;a++){this.d[a]=this.d[a]+1|0;if(this.d[a])break}return this.s.encrypt(this.d)},L:function(){this.a=this.w().concat(this.w());this.s=new sjcl.cipher.aes(this.a)},T:function(a){this.a=sjcl.hash.sha256.hash(this.a.concat(a));this.s=new sjcl.cipher.aes(this.a);for(a=0;a<4;a++){this.d[a]=this.d[a]+1|0;if(this.d[a])break}},U:function(a){var b=[],c=0,d;this.O=b[0]=(new Date).valueOf()+3E4;for(d=
    0;d<16;d++)b.push(Math.random()*0x100000000|0);for(d=0;d<this.b.length;d++){b=b.concat(this.b[d].finalize());c+=this.j[d];this.j[d]=0;if(!a&&this.A&1<<d)break}if(this.A>=1<<this.b.length){this.b.push(new sjcl.hash.sha256);this.j.push(0)}this.f-=c;if(c>this.g)this.g=c;this.A++;this.T(b)},p:function(a){sjcl.random.addEntropy([a.x||a.clientX||a.offsetX||0,a.y||a.clientY||a.offsetY||0],2,"mouse")},o:function(){sjcl.random.addEntropy((new Date).valueOf(),2,"loadtime")},K:function(a,b){var c;a=sjcl.random.r[a];
    var d=[];for(c in a)a.hasOwnProperty(c)&&d.push(a[c]);for(c=0;c<d.length;c++)d[c](b)}};try{var s=new Uint32Array(32);crypto.getRandomValues(s);sjcl.random.addEntropy(s,1024,"crypto['getRandomValues']")}catch(t){}
    sjcl.json={defaults:{v:1,iter:1E3,ks:128,ts:64,mode:"ccm",adata:"",cipher:"aes"},encrypt:function(a,b,c,d){c=c||{};d=d||{};var e=sjcl.json,f=e.c({iv:sjcl.random.randomWords(4,0)},e.defaults),g;e.c(f,c);c=f.adata;if(typeof f.salt==="string")f.salt=sjcl.codec.base64.toBits(f.salt);if(typeof f.iv==="string")f.iv=sjcl.codec.base64.toBits(f.iv);if(!sjcl.mode[f.mode]||!sjcl.cipher[f.cipher]||typeof a==="string"&&f.iter<=100||f.ts!==64&&f.ts!==96&&f.ts!==128||f.ks!==128&&f.ks!==192&&f.ks!==0x100||f.iv.length<
    2||f.iv.length>4)throw new sjcl.exception.invalid("json encrypt: invalid parameters");if(typeof a==="string"){g=sjcl.misc.cachedPbkdf2(a,f);a=g.key.slice(0,f.ks/32);f.salt=g.salt}if(typeof b==="string")b=sjcl.codec.utf8String.toBits(b);if(typeof c==="string")c=sjcl.codec.utf8String.toBits(c);g=new sjcl.cipher[f.cipher](a);e.c(d,f);d.key=a;f.ct=sjcl.mode[f.mode].encrypt(g,b,f.iv,c,f.ts);return e.encode(f)},decrypt:function(a,b,c,d){c=c||{};d=d||{};var e=sjcl.json;b=e.c(e.c(e.c({},e.defaults),e.decode(b)),
    c,true);var f;c=b.adata;if(typeof b.salt==="string")b.salt=sjcl.codec.base64.toBits(b.salt);if(typeof b.iv==="string")b.iv=sjcl.codec.base64.toBits(b.iv);if(!sjcl.mode[b.mode]||!sjcl.cipher[b.cipher]||typeof a==="string"&&b.iter<=100||b.ts!==64&&b.ts!==96&&b.ts!==128||b.ks!==128&&b.ks!==192&&b.ks!==0x100||!b.iv||b.iv.length<2||b.iv.length>4)throw new sjcl.exception.invalid("json decrypt: invalid parameters");if(typeof a==="string"){f=sjcl.misc.cachedPbkdf2(a,b);a=f.key.slice(0,b.ks/32);b.salt=f.salt}if(typeof c===
    "string")c=sjcl.codec.utf8String.toBits(c);f=new sjcl.cipher[b.cipher](a);c=sjcl.mode[b.mode].decrypt(f,b.ct,b.iv,c,b.ts);e.c(d,b);d.key=a;return sjcl.codec.utf8String.fromBits(c)},encode:function(a){var b,c="{",d="";for(b in a)if(a.hasOwnProperty(b)){if(!b.match(/^[a-z0-9]+$/i))throw new sjcl.exception.invalid("json encode: invalid property name");c+=d+'"'+b+'":';d=",";switch(typeof a[b]){case "number":case "boolean":c+=a[b];break;case "string":c+='"'+escape(a[b])+'"';break;case "object":c+='"'+
    sjcl.codec.base64.fromBits(a[b],1)+'"';break;default:throw new sjcl.exception.bug("json encode: unsupported type");}}return c+"}"},decode:function(a){a=a.replace(/\s/g,"");if(!a.match(/^\{.*\}$/))throw new sjcl.exception.invalid("json decode: this isn't json!");a=a.replace(/^\{|\}$/g,"").split(/,/);var b={},c,d;for(c=0;c<a.length;c++){if(!(d=a[c].match(/^(?:(["']?)([a-z][a-z0-9]*)\1):(?:(\d+)|"([a-z0-9+\/%*_.@=\-]*)")$/i)))throw new sjcl.exception.invalid("json decode: this isn't json!");b[d[2]]=
    d[3]?parseInt(d[3],10):d[2].match(/^(ct|salt|iv)$/)?sjcl.codec.base64.toBits(d[4]):unescape(d[4])}return b},c:function(a,b,c){if(a===undefined)a={};if(b===undefined)return a;var d;for(d in b)if(b.hasOwnProperty(d)){if(c&&a[d]!==undefined&&a[d]!==b[d])throw new sjcl.exception.invalid("required parameter overridden");a[d]=b[d]}return a},V:function(a,b){var c={},d;for(d=0;d<b.length;d++)if(a[b[d]]!==undefined)c[b[d]]=a[b[d]];return c}};sjcl.encrypt=sjcl.json.encrypt;sjcl.decrypt=sjcl.json.decrypt;
    sjcl.misc.S={};sjcl.misc.cachedPbkdf2=function(a,b){var c=sjcl.misc.S,d;b=b||{};d=b.iter||1E3;c=c[a]=c[a]||{};d=c[d]=c[d]||{firstSalt:b.salt&&b.salt.length?b.salt.slice(0):sjcl.random.randomWords(2,0)};c=b.salt===undefined?d.firstSalt:b.salt;d[c]=d[c]||sjcl.misc.pbkdf2(a,c,b.iter);return{key:d[c].slice(0),salt:c.slice(0)}};
    </script>
    </body>
    </html>
    
    
    
    


.. bottom of content


.. |STYLE0| replace:: **Strumenti / <> Editor di script GGeditor**


.. |LINK1| raw:: html

    <a href="https://docs.google.com/document/d/14soShDfb2IoM5wSOHCSl6XwYmGJ2CK18jEwHXaWqWho/edit?usp=sharing" target="_blank">https://docs.google.com/document/d/14soShDfb2IoM5wSOHCSl6XwYmGJ2CK18jEwHXaWqWho/edit?usp=sharing</a>

