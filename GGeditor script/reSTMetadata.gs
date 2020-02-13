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
