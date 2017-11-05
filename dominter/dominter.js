"use strict";

(function() {
  var excepts = ['_in_init_', 'tagName', 'document', 'parent',
    '_id', '_classList', 'eventlisteners',
    'attributes', 'elements', '_onclick', '_onchange',
    'appendChild', 'removeChild',
  ];
  var headId, bodyId;

  var createEventHandler = function(ws, type_, id_) {
    var handler = function(ev) {
      var dic = {'id': id_};
      var ids = ['currentTarget', 'explicitOriginalTarget', 'fromElement',
        'originalTarget', 'relatedNode', 'relatedTarget', 'srcElement',
        'toElement', 'target'];
      var ignores = ['path', 'sourceCapabilities', 'view'];
      for (var p in ev) {
        if (0 <= ids.indexOf(p)) {
          dic[p + 'Id'] = ev[p] ? ev[p].id : null;
        }
        else if (0 <= ignores.indexOf(p)) {
          // ignore
        }
        else if ('function' == typeof(ev[p])) {
          // ignore
        }
        else {
          dic[p] = ev[p];
        }
      }
      if ('change' == type_) {
        dic['value'] = ev.target.value;
        if (ev.target.checked !== undefined) {
          dic['checked'] = ev.target.checked;
        }
        if (ev.target.selectedIndex !== undefined) {
          dic['selectedIndex'] = ev.target.selectedIndex;
        }
      }
      var js = JSON.stringify(dic);
      ws.send(js);
      return true;
    };
    return handler;
  };

  var newElement = function(dat) {
    var tagname = dat['tagName'];
    var elm = document.createElement(tagname);
    if (dat['_id'] !== undefined) {
      elm.id = dat['_id'];
    }
    for (var pr in dat) {
      if (0 > excepts.indexOf(pr)) {
        elm[pr] = dat[pr];
      }
    }
    var cl = dat['_classList'];
    if (cl) {
      var cn = cl.join(' ');
      elm['className'] = cn;
    }
    var styl = dat['_style'];
    if (styl) {
      var s = '';
      for (var key of Object.keys(styl)) {
        s += key + ':' + styl[key] + ';';
      }
      elm.setAttribute('style', s)
    }
    var val = dat['attributes'];
    if (val) {
      for (var key of Object.keys(val)) {
        elm.setAttribute(key, val[key]);
      }
    }
    // add onchange to input/select/textarea
    if ('input' == tagname) {
      elm.addEventListener('change', createEventHandler(ws, 'change', dat['_id']), false);
    }
    else if ('select' == tagname) {
      elm.addEventListener('change', createEventHandler(ws, 'change', dat['_id']), false);
    }
    else if ('textarea' == tagname) {
      elm.addEventListener('change', createEventHandler(ws, 'change', dat['_id']), false);
    }

    // add user handler after system handler to avoid to refer old value
    val = dat['_onclick'];
    if (val) {
      elm.onclick = createEventHandler(ws, 'click', val)
    }
    val = dat['_onchange']
    if (val) {
      elm.onchange = createEventHandler(ws, 'change', val)
    }
    val = dat['eventlisteners']
    if (val) {
      for (var tpl of val) {
        var typ = tpl[0];
        var fnc = tpl[1];
        elm.addEventListener(typ, createEventHandler(ws, typ, fnc), false);
      }
    }
    return elm;
  };

  var appendElements = function(ws, parent, lst) {
    for (var dat of lst) {
      var tagname = dat['tagName'];
      var isnew = true;
      var elm;
      //var notnew = parent[tagname];  // don't work on style of head
      var notnew = false;  // so force new
      if (notnew) {
        isnew = false;
        elm = parent[tagname];
      }
      else {
        //elm = document.createElement(tagname);
        elm = newElement(dat)
      }
      if (dat.elements) {
        appendElements(ws, elm, dat.elements);
      }
      if (isnew) {
        parent.appendChild(elm);
      }
    }
  };

  var getWsPath = function() {
    var scr = document.getElementById('dominter-js');
    return scr.getAttribute('data-ws');
  };

  var wspath = getWsPath();
  if (!wspath) {
    return;
  }
  var url = (location.protocol == 'https:' ? 'wss' : 'ws:') +
    location.host + wspath;
  var ws = new WebSocket(url);

  ws.onopen = function(ev) {
  };

  var findElm = function(dic, eid) {
    var res;
    if (eid in dic) {
      res = dic[eid];
    }
    return res;
  };

  var diffproc = function(dic, name) {
    var newdic = {};
    for (var dat of dic[name]) {
      var objid = dat['_objid_'];
      var elm = document.getElementById(objid);
      if (!elm) {
        if (objid == headId) {
          elm = document.head;
        }
        else if (objid == bodyId) {
          elm = document.body;
        }
        else if (objid in newdic) {
          elm = newdic[objid];
        }
        else {
          //for create//return;
        }
      }
      if (elm) {
        if (dat['id'] !== undefined) {
          elm.id = dat['id'];
        }
        for (var pr in dat) {
          if (0 > excepts.indexOf(pr)) {
            elm[pr] = dat[pr];
          }
        }
        if (dat['onclick']) {
          elm.onclick = createEventHandler(ws, 'click', dat['onclick'])
        }
        if (dat['onchange']) {
          elm.onchange = createEventHandler(ws, 'change', dat['onchange'])
        }
        if ('setAttributes' in dat) {
          var atrs = dat['setAttributes'];
          for (var key of Object.keys(atrs)) {
            elm.setAttribute(key, atrs[key]);
          }
        }
        if ('removeAttributes' in dat) {
          var atrs = dat['removeAttributes'];
          for (var key of atrs) {
            elm.removeAttribute(key);
          }
        }
        if ('addClass' in dat) {
          var lst = dat['addClass'];
          for (var cls of lst) {
            elm.classList.add(cls);
          }
        }
        if ('removeClass' in dat) {
          var lst = dat['removeClass'];
          for (var cls of lst) {
            elm.classList.remove(cls);
          }
        }
        if ('clearClass' in dat) {
          elm.className = '';
        }
        if ('setStyle' in dat) {
          var dic = dat['setStyle'];
          for (var k of Object.keys(dic)) {
            elm.style[k] = dic[k];
          }
        }
        if ('deleteStyle' in dat) {
          var lst = dat['deleteStyle'];
          for (var k of lst) {
            elm.style.removeProperty(k);
          }
        }
        if ('clearStyle' in dat) {
          elm.style.cssText = '';
        }
        if ('removeChild' in dat) {
          var child = document.getElementById(dat['removeChild']);
          if (child) {
            elm.removeChild(child);
          }
        }
        if ('appendChild' in dat) {
          var aid = dat['appendChild'];
          var child = document.getElementById(aid);
          if (!child) {
            child = findElm(newdic, aid);
          }
          if (child) {
            elm.appendChild(child);
          }
        }
        if ('insertBefor' in dat) {
          var lst = dat['insertBefor'];
          var newid = lst[0];
          var refid = lst[1];
          var newelm = document.getElementById(newid);
          if (!newelm) {
            newelm = findElm(newdic, newid);
          }
          if (newelm) {
            var refelm = document.getElementById(refid);
            if (!refelm) {
              refelm = findElm(newdic, refid);
            }
            if (refelm) {
              elm.insertBefor(newelm, refelm);
            }
            else {
              elm.appendChild(newelm);
            }
          }
        }
      }
      if ('createElement' in dat) {
        var d = dat['createElement'];
        if (d) {
          var newdat = JSON.parse(d);
          var newid = newdat['_id'];
          var newelm = newElement(newdat);
          newdic[newid] = newelm;
        }
      }
    }
  };

  var typeproc = function(dic) {
    var id = dic['id'];
    var elm = document.getElementById(id);
    if (!elm) {
      return;
    }
    var type_ = dic['type'];
    if ('click' == type_) {
    }
    else if ('change' == type_) {
      if ('value' in dic) {
        elm.value = dic['value'];
      }
      if ('checked' in dic) {
        elm.checked = dic['checked'];
      }
      if ('selectedIndex' in dic) {
        elm.selectedIndex = dic['selectedIndex'];
      }
    }
  };

  ws.onmessage = function(ev) {
    var dic = JSON.parse(ev.data);
    if ('head' in dic) {
      var head = dic['head'];
      if (head['elements']) {
        appendElements(ws, document.head, head['elements']);
      }
      headId = head._id;
    }
    if ('body' in dic) {
      var body = dic['body'];
      if (body['elements']) {
        appendElements(ws, document.body, body['elements']);
      }
      bodyId = body._id;
    }
    if ('diff' in dic) {
      diffproc(dic, 'diff');
    }
    if ('type' in dic) {
      typeproc(dic);
    }
  };
})();
