function trackEmbedEvent(event) {
    try {
        event.type = 'embed'
        return $.post("api/e/stat/gen", event)
            .then(function(response){
                console.info("Successfully recorded embed event:", event.type, event.tuid)
                return response;
            }, function(response){
                console.info("Failed to record embed event:", event.type, event.tuid)
            });
    } catch(err) {
        debugger
    }
}

function awaitDocumentBodyAnchorClick(callback) {
    document.body.onclick = function(e){
        e = e || event;
        var from = findParentElemByTagName('a', e.target || e.srcElement);
        if (from && from.href && from.href.trim().length){ try { callback(from) }catch(err) {} }
    }
}

//find first parent with tagName [tagname]
function findParentElemByTagName(tagname, el){
  if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
    return el;
  }
  while (el = el.parentNode){
    if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
      return el;
    }
  }
  return null;
}