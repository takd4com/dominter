// Copyright (c) 2017-2018 Tamini Bean
// License: MIT
"use strict";

(function() {
  var excepts = ['_in_init_', 'tagName', 'document', 'parent',
    '_id', '_objid_', '_classList', '_eventlisteners',
    '_childList', '_onclick', 'onclick', '_onchange', 'onchange',
    '_setAttributes', '_removeAttributes', '_delattr',
    '_clearChild', '_reverseChild', '_sortorder',
    '_addClass', '_removeClass', '_clearClass',
    '_setStyle', '_deleteStyle', '_clearStyle',
    '_removeChild', '_appendChild', '_insertBefore', '_replaceChild',
    '_sortChild', '_createElement',
    '_addEventListener', '_removeEventListener',
  ];
  var headId, bodyId;

  var handlerDic = {};

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
      else if (('keypress' == type_)||
                ('keyup' == type_)||
                ('keydown' == type_)) {
        dic['value'] = ev.target.value;
      }
      var js = JSON.stringify(dic);
      ws.send(js);
      return true;
    };
    handlerDic[id_] = handler;
    return handler;
  };

  var removeEventHandler = function(elm, type_, id_) {
    if (handlerDic[id_]) {
      var handler = handlerDic[id_];
      elm.removeEventListener(type_, handler);
      return true;
    }
    return false;
  }

  var newElement = function(ws, dat) {
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
    val = dat['_eventlisteners']
    if (val) {
      for (var tpl of val) {
        var typ = tpl[0];
        var fnc = tpl[1];
        elm.addEventListener(typ, createEventHandler(ws, typ, fnc), false);
      }
    }
    return elm;
  };

  var newWindow = function(ws, dat) {
    var elm = window;
    for (var pr in dat) {
      if (0 > excepts.indexOf(pr)) {
        elm[pr] = dat[pr];
      }
    }
    var val = dat['_eventlisteners']
    if (val) {
      for (var tpl of val) {
        var typ = tpl[0];
        var fnc = tpl[1];
        elm.addEventListener(typ, createEventHandler(ws, typ, fnc), false);
      }
    }
  }

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
        elm = newElement(ws, dat)
      }
      if (dat._childList) {
        appendElements(ws, elm, dat._childList);
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
    var dic = {'type': 'open', 'id': 'window', 'location': window.location};
    var js = JSON.stringify(dic);
    ws.send(js);
  };

  var findElm = function(dic, eid) {
    var res;
    if (eid in dic) {
      res = dic[eid];
    }
    return res;
  };

  var diffproc = function(ws, dic, name) {
    var newdic = {};
    for (var dat of dic[name]) {
      var objid = dat['_objid_'];
      if (objid == '_window_handler') {
        if ('_addEventListener' in dat) {
          var lst = dat['_addEventListener'];
          var typ = lst[0];
          var fnc = lst[1];
          window.addEventListener(typ, createEventHandler(ws, typ, fnc), false);
        }
        if ('_removeEventListener' in dat) {
          var lst = dat['_removeEventListener'];
          var typ = lst[0];
          var fnc = lst[1];
          removeEventHandler(window, typ, fnc);
        }
        continue;
      }
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
        if ('_setAttributes' in dat) {
          var atrs = dat['_setAttributes'];
          for (var key of Object.keys(atrs)) {
            elm.setAttribute(key, atrs[key]);
          }
        }
        if ('_removeAttributes' in dat) {
          var atrs = dat['_removeAttributes'];
          for (var key of atrs) {
            elm.removeAttribute(key);
          }
        }
        if ('_delattr' in dat) {
          var atrs = dat['_delattr'];
          for (var key of atrs) {
            elm.removeAttribute(key);
          }
        }
        if ('_clearChild' in dat) {
          while (elm.firstChild) {
            elm.removeChild(elm.firstChild);
          }
        }
        if ('_reverseChild' in dat) {
          var cnt = elm.children.length;
          for (var j = 0; j < cnt/2; j++) {
            elm.insertBefore(elm.children[j], elm.children[cnt-1-j]);
            elm.insertBefore(elm.children[cnt-1-j], elm.children[j]);
          }
        }
        if ('_sortChild' in dat) {
          var lst = dat['_sortChild'];
          var pre = [];
          for (var chd of elm.children) {
            pre.push(chd);
          }
          while (elm.firstChild) {
            elm.removeChild(elm.firstChild);
          }
          for (var od of lst) {
            elm.appendChild(pre[od])
          }
        }
        if ('_addClass' in dat) {
          var lst = dat['_addClass'];
          for (var cls of lst) {
            elm.classList.add(cls);
          }
        }
        if ('_removeClass' in dat) {
          var lst = dat['_removeClass'];
          for (var cls of lst) {
            elm.classList.remove(cls);
          }
        }
        if ('_clearClass' in dat) {
          elm.className = '';
        }
        if ('_setStyle' in dat) {
          var dic = dat['_setStyle'];
          for (var k of Object.keys(dic)) {
            elm.style[k] = dic[k];
          }
        }
        if ('_deleteStyle' in dat) {
          var lst = dat['_deleteStyle'];
          for (var k of lst) {
            elm.style.removeProperty(k);
          }
        }
        if ('_clearStyle' in dat) {
          elm.style.cssText = '';
        }
        if ('_removeChild' in dat) {
          var chd = document.getElementById(dat['_removeChild']);
          if (chd) {
            elm.removeChild(chd);
          }
        }
        if ('_appendChild' in dat) {
          var aid = dat['_appendChild'];
          var chd = document.getElementById(aid);
          if (!chd) {
            chd = findElm(newdic, aid);
          }
          if (chd) {
            elm.appendChild(chd);
          }
        }
        if ('_insertBefore' in dat) {
          var lst = dat['_insertBefore'];
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
              elm.insertBefore(newelm, refelm);
            }
            else {
              elm.appendChild(newelm);
            }
          }
        }
        if ('_replaceChild' in dat) {
          var lst = dat['_replaceChild'];
          var newid = lst[0];
          var oldid = lst[1];
          var newelm = document.getElementById(newid);
          if (!newelm) {
            newelm = findElm(newdic, newid);
          }
          if (newelm) {
            var oldelm = document.getElementById(olcid);
            if (!oldelm) {
              oldelm = findElm(newdic, oldid);
            }
            if (oldelm) {
              elm.replaceChild(newelm, oldelm);
            }
            else {
              elm.appendChild(newelm);
            }
          }
        }
        if ('_addEventListener' in dat) {
          var lst = dat['_addEventListener'];
          var typ = lst[0];
          var fnc = lst[1];
          elm.addEventListener(typ, createEventHandler(ws, typ, fnc), false);
        }
        if ('_removeEventListener' in dat) {
          var lst = dat['_removeEventListener'];
          var typ = lst[0];
          var fnc = lst[1];
          removeEventHandler(elm, typ, fnc);
        }
        if ('_focus' in dat) {
          elm.focus();
        }
        if ('_blur' in dat) {
          elm.blur();
        }
      }
      if ('_createElement' in dat) {
        var d = dat['_createElement'];
        if (d) {
          var newdat = JSON.parse(d);
          var newid = newdat['_id'];
          var newelm = newElement(ws, newdat);
          newdic[newid] = newelm;
        }
      }
    }
  };

  var typeproc = function(ws, dic) {
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
      if (head['_childList']) {
        appendElements(ws, document.head, head['_childList']);
      }
      headId = head._id;
    }
    if ('body' in dic) {
      var body = dic['body'];
      if (body['_childList']) {
        appendElements(ws, document.body, body['_childList']);
      }
      bodyId = body._id;
    }
    if ('_window_element' in dic) {
      var dat = dic['_window_element'];
      newWindow(ws, dat);
    }
    if ('diff' in dic) {
      diffproc(ws, dic, 'diff');
    }
    if ('type' in dic) {
      typeproc(ws, dic);
    }
  };
})();
