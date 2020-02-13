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
