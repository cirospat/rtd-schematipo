
.. _h6c3e1d1d695c775e697f3f1a706e19:

GGeditor-script-per-Google-Doc
##############################

2017/01/10 - PM 01:11:42

.. admonition:: Cosa è questo documento?

    Questo documento contiene uno script con il codice sorgente che permette di trasmettere (in maniera automatica) su Github i contenuti editati in questo foglio, trasformandoli in sintassi del formato ``.RST``.
    Creando una copia di questo documento sul proprio Google Drive si copierà anche lo script che si trova su:
    \ |STYLE0|\ 


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

This is a "special" paragraph.


.. class:: da fare 

    

    questo testo  è stato editato nella direttiva generica codificata come ``.. class:: speciale``

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
    


.. bottom of content


.. |STYLE0| replace:: **Strumenti / <> Editor di script GGeditor**


.. |LINK1| raw:: html

    <a href="https://docs.google.com/document/d/14soShDfb2IoM5wSOHCSl6XwYmGJ2CK18jEwHXaWqWho/edit?usp=sharing" target="_blank">https://docs.google.com/document/d/14soShDfb2IoM5wSOHCSl6XwYmGJ2CK18jEwHXaWqWho/edit?usp=sharing</a>

