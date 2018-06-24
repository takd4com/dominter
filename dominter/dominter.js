// Copyright (c) 2017-2018 Tamini Bean
// License: MIT
"use strict";

(function() {
  // logger
  var logger = {};
  logger.DEBUG = 1;
  logger.INFO = 2;
  logger.logLevel = logger.DEBUG;
  //logger.logLevel = logger.INFO;
  var nowstr = function() {
    var date = new Date();
    var ms = date.getMilliseconds();
    return date.toLocaleString() + ',' + ms;
  }
  logger.debug = function(msg) {
    var disp = 'DEBUG';
    if (logger.DEBUG < logger.logLevel) {
      return;
    }
    console.debug(nowstr() + ' ' + disp + ' ' + msg);
  }
  logger.info = function(msg) {
    var disp = 'INFO';
    if (logger.INFO < logger.logLevel) {
      return;
    }
    console.info(nowstr() + ' ' + disp + ' ' + msg);
  }
  logger.error = function(msg) {
    var disp = 'ERROR';
    if (logger.ERROR < logger.logLevel) {
      return;
    }
    console.error(nowstr() + ' ' + disp + ' ' + msg);
  }

  // dominter
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
  var renderingMethod2D = {
    'addHitRegion': [0, false],
    'arc': [5, false],
    'arcTo': [5, false],
    'beginPath': [0, false],
    'bezierCurveTo': [6, false],
    'clearRect': [4, false],
    'clearHitRegions': [0, false],
    'clearRect': [4, false],
    'clip': [0, false],
    'closePath': [0, false],
    //'createImageData': [1, true],
    'createLinearGradient': [4, true],
    'createPattern': [2, true],
    'createRadialGradient': [6, true],
    'drawFocusIfNeeded': [1, false],
    'drawImage': [3, true],
    'ellipse': [7, false],
    'fill': [0, false],
    'fillRect': [4, false],
    'fillText': [3, false],
    //'getImageData': [4, true],
    //'getLineDash': [0, true],
    //'isPointInPath': [2, true],
    //'isPointInStroke': [2, true],
    'lineTo': [2, false],
    //'measureText': [1, true],
    'moveTo': [2, false],
    //'putImageData': [3, true],
    'quadraticCurveTo': [4, false],
    'rect': [4, false],
    'removeHitRegion': [1, false],
    'resetTransform': [0, false],
    'restore': [0, false],
    'rotate': [1, false],
    'save': [0, false],
    'scale': [2, false],
    'scrollPathIntoView': [0, false],
    'setLineDash': [1, false],
    'setTransform': [6, false],
    'stroke': [0, false],
    'strokeRect': [4, false],
    'strokeText': [3, false],
    'transform': [6, false],
    'translate': [2, false],
    //
    'addColorStop': [2, false],
  };
  var headId, bodyId;

  var handlerDic = {};

  var windowDic = {};

  var objectDic = {};

  var modalCallback = function(ws, type_, id_, value) {
      var dic = {'id': id_, 'type': type_, 'value': value};
      var js = JSON.stringify(dic);
      ws.send(js);
  };

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

  var appendElements = function(ws, parent, lst, istop=true) {
    var tgt = istop ? document.createDocumentFragment() : parent;
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
        appendElements(ws, elm, dat._childList, false);
      }
      if (isnew) {
        tgt.appendChild(elm);
      }
    }
    if (istop) {
      parent.appendChild(tgt);
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

  var parseStorage = function(dic) {
    // storage is dict, key is string, value is JSON.stringified.
    var res = {};
    var keys = Object.keys(dic);
    for (var key of keys) {
      res[key] = JSON.parse(dic[key]);
    }
    return res;
  }

  var findElm = function(dic, eid) {
    var res;
    if (eid in dic) {
      res = dic[eid];
    }
    return res;
  };

  var getArgs = function(lst) {
    var args = [];
    for (var arg of lst) {
      if (('object' == (typeof arg))&& arg['_id']) {
        var objid = arg['_id'];
        var obj = objectDic[objid];
        if (!obj) {
          obj = document.getElementById(objid);
        }
        args.push(obj);
      }
      else {
        args.push(arg);
      }
    }
    return args;
  }

  var diffproc = function(ws, dic, name) {
    var newdic = {};
    for (var dat of dic[name]) {
      var objid = dat['_objid_'];
      var winmethod = dat['_win_method'];
      if (winmethod) {
        if (winmethod == '_alert') {
          var msg = dat['message'];
          window.alert(msg);
          modalCallback(ws, 'alert', '_alert', true);
          continue;
        }
        else if (winmethod == '_confirm') {
          var msg = dat['message'];
          var res = window.confirm(msg);
          modalCallback(ws, 'confirm', '_confirm', res);
          continue;
        }
        else if (winmethod == '_prompt') {
          var msg = dat['message'];
          var val = dat['value'];
          var res = window.prompt(msg, val);
          modalCallback(ws, 'prompt', '_prompt', res);
          continue;
        }
        else if (winmethod == '_open') {
          var url = dat['url'];
          var name = dat['name'];
          var features = dat['features'];
          var winid = dat['winid'];
          var hdl;
          if (features) {
            hdl = window.open(url, name, features);
          }
          else {
            hdl = window.open(url, name);
          }
          windowDic[winid] = hdl;
        }
        else if (winmethod == '_close') {
          var hdl = windowDic[winid];
          if (hdl) {
            hdl.close();
            delete windowDic[winid];
          }
          else {
            window.close();
          }
        }
        else if (winmethod == '_blur') {
          var hdl = windowDic[winid];
          if (hdl) {
            hdl.blur();
          }
          else {
            window.blur();
          }
        }
        else if (winmethod == '_focus') {
          var hdl = windowDic[winid];
          if (hdl) {
            hdl.focus();
          }
          else {
            window.focus();
          }
        }
        else if (winmethod == '_print') {
          var hdl = windowDic[winid];
          if (hdl) {
            hdl.print();
          }
          else {
            window.print();
          }
        }
        else if (winmethod == '_moveBy') {
          var hdl = windowDic[winid];
          var x = dat['x'];
          var y = dat['y'];
          if (hdl) {
            hdl.moveBy(x, y);
          }
          else {
            window.moveBy(x, y);
          }
        }
        else if (winmethod == '_moveTo') {
          var hdl = windowDic[winid];
          var x = dat['x'];
          var y = dat['y'];
          if (hdl) {
            hdl.moveTo(x, y);
          }
          else {
            window.moveTo(x, y);
          }
        }
        else if (winmethod == '_resizeBy') {
          var hdl = windowDic[winid];
          var x = dat['x'];
          var y = dat['y'];
          if (hdl) {
            hdl.resizeBy(x, y);
          }
          else {
            window.resizeBy(x, y);
          }
        }
        else if (winmethod == '_resizeTo') {
          var hdl = windowDic[winid];
          var x = dat['x'];
          var y = dat['y'];
          if (hdl) {
            hdl.resizeTo(x, y);
          }
          else {
            window.resizeTo(x, y);
          }
        }
        else if (winmethod == '_scroll') {
          var hdl = windowDic[winid];
          var x = dat['x'];
          var y = dat['y'];
          if (hdl) {
            hdl.scroll(x, y);
          }
          else {
            window.scroll(x, y);
          }
        }
        else if (winmethod == '_scrollBy') {
          var hdl = windowDic[winid];
          var x = dat['x'];
          var y = dat['y'];
          if (hdl) {
            hdl.scrollBy(x, y);
          }
          else {
            window.scrollBy(x, y);
          }
        }
        else if (winmethod == '_scrollTo') {
          var hdl = windowDic[winid];
          var x = dat['x'];
          var y = dat['y'];
          if (hdl) {
            hdl.scrollTo(x, y);
          }
          else {
            window.scrollTo(x, y);
          }
        }
        /*
        else if (winmethod == '_minimize') {
          var hdl = windowDic[winid];
          if (hdl) {
            hdl.minimize();
          }
          else {
            window.minimize();
          }
        }*/
        else if (winmethod == '_create') {
          var typ = dat['_objType'];
          var args = getArgs(dat['args']);
          var newid = dat['_id'];
          var newobj;
          if (typ == 'Image') {
            if (2 == args.length) {
              newobj = new Image(args[0], args[1]);
            }
            else {
              newobj = new Image();
            }
          }
          else {
            var obj = objectDic[objid];
            var method = dat['_method'];
            if (obj && method) {
              if (method in renderingMethod2D) {
                var mp = renderingMethod2D[method];
                var an = mp[0];
                if (args.length >= an) {
                  var res = obj[method].apply(obj, args);
                  if (mp[1]||(dat['_register'])) {
                    newobj = res;
                  }
                }
                else {
                  logger.error('bad arg count. method=' + method + ' args=' + args);
                  // need to return error
                }
              }
            }
            else {
              logger.error('obj or method is null');
            }
          }
          if (newobj) {
            objectDic[newid] = newobj;
          }
          else {
            logger.error('bad params');
          }
        }

        continue;
      } else
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
      else if ((objid == '_sessionStorage') || (objid == '_localStorage')) {
        var storage = (objid == '_sessionStorage') ? sessionStorage : localStorage;
        if ('setitem' in dat) {
          var kv = dat['setitem'];
          storage.setItem(kv[0], JSON.stringify(kv[1]));
        }
        else if ('delitem' in dat) {
          var key = dat['delitem'];
          storage.removeItem(key);
        }
        else if ('update' in dat) {
          var dic = dat['update'];
          for (var key in dic) {
            storage.setItem(key, dic[key]);
          }
        }
        else if ('clear' in dat) {
          storage.clear();
        }
        continue;
      }
      var obj = objectDic[objid];
      if (obj) {
        var objtype = dat['_objType'];
        if ('RenderingContext' == objtype) {
          var method = dat['_method'];
          var args = dat['args'];
          if ('setattr' == method) {
            var key = dat['key'];
            if (key) {
              var value = dat['value'];
              if (dat['_valueType'] == 'DomObject') {
                value = objectDic[value];
              }
              obj[key] = value;
            }
          }
          else if ('__del__' == method) {
            logger.info('delete from objectDic: ' + objid);  //tmp
            delete objectDic[objid];
          }
          else if (method in renderingMethod2D) {
            var mp = renderingMethod2D[method];
            var an = mp[0];
            if (args.length >= an) {
              var ca = getArgs(args);
              var res = obj[method].apply(obj, ca);
              if (mp[1]||(dat['_register'])) {
                var _id = dat['_id'];
                objectDic[_id] = res;
                logger.info('add DomObject to objectDic: ' + _id);  //tmp
              }
            }
            else {
              logger.error('bad arg count. method=' + method + ' args=' + args);
              // need to return error
            }
          }
          else {
            logger.error('unknown method. method=' + method + ' args=' + args);
          }
        }
        else {  // Image,...
          var method = dat['_method'];
          if ('setattr' == method) {
            var key = dat['key'];
            var value = dat['value'];
            var vt = dat['_valueType'];
            if (vt == 'DomObject') {
              value = objectDic[value];
              if (!value) {
                logger.error('setattr: dom object not found. key=' + key + ' value=' + dat['value']);
              }
            }
            obj[key] = value;
          }
          else if ('addEventListener' == method) {
            var lst = dat['args'];
            var typ = lst[0];
            var fnc = lst[1];
            var hdr = createEventHandler(ws, typ, fnc);
            var res = obj[method].apply(obj, [typ, hdr, false]);
          }
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
        if ('_method' in dat) {
          var fnc = dat['_method'];
          if ('focus' == fnc) {
            elm.focus();
          }
          else if ('blur' == fnc) {
            elm.blur();
          }
          else if ('scrollIntoView' == fnc) {
            var alignToTop = dat['alignToTop'];
            var behavior = dat['behavior'];
            var block = dat['block'];
            var inline = dat['inline'];
            if (alignToTop === null) {
              if (behavior || block || inline) {
                var opt = {};
                if (behavior) {
                  opt['behavior'] = behavior;
                }
                if (block) {
                  opt['block'] = block;
                }
                if (inline) {
                  opt['inline'] = inline;
                }
                elm.scrollIntoView(opt);
              }
              else {
                elm.scrollIntoView();
              }
            }
            else {
              elm.scrollIntoView(alignToTop);
            }
          }
          else if ('getContext' == fnc) {
            var contentType = dat['contentType'];
            var contextAttributes = dat['contextAttributes'];
            var objid = dat['_id'];
            var obj;
            if (contextAttributes) {
              obj = elm.getContext(contentType, contextAttributes);
            }
            else {
              obj = elm.getContext(contentType);
            }
            objectDic[objid] = obj;
            logger.info('add RenderingContext to objectDic: ' + objid);  //tmp
          }
          continue;
        }
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

  // websocket class
  var DominterWs = function(url) {
    this.url = url;
    this.websocket = null;
    this.waitque = [];
    this.init();
  };

  DominterWs.prototype.send = function(dat) {
    var st = this.websocket.readyState;
    if (WebSocket.OPEN == st) {
      this.websocket.send(dat);
    } else {
      /*
      // auto reconnect
      this.waitque.push(dat);
      if (WebSocket.CLOSING <= st) {
        this.init();
      }
      */
      var res = window.confirm('Connection terminated. OK to reload.')
      if (res) {
        location.reload();
      }
    }
  };

  DominterWs.prototype.init = function() {
    var ws = this;
    var se = document.getElementById('_ws_status');
    if (se) {
      se.textContent = 'connecting';
    }
    var websocket = new WebSocket(this.url);
    this.websocket = websocket;
    websocket.onopen = function(ev) {
      logger.info('onopen');
      var se = document.getElementById('_ws_status');
      if (se) {
        se.textContent = 'open';
      }
      var localst = parseStorage(window.localStorage);
      var sessionst = parseStorage(window.sessionStorage);
      var dic = {'type': 'open', 'id': 'window', 'location': window.location,
        'localStorage': localst, 'sessionStorage': sessionst};
      var js = JSON.stringify(dic);
      websocket.send(js);
    };

    websocket.onclose = function(ev) {
      logger.info('onclose');
      var se = document.getElementById('_ws_status');
      if (se) {
        se.textContent = 'close';
      }
    };

    websocket.onerror = function(ev) {
      logger.info('onerror');
      var se = document.getElementById('_ws_status');
      if (se) {
        se.textContent = 'error';
      }
    };

    var parentinit = function(parent, exceptid) {
      var ofs = 0;
      var lst = parent.children;
      while (lst.length - ofs) {
        var elm = lst[ofs];
        if (elm.id == exceptid) {
          ofs = 1;
        } else {
          parent.removeChild(elm);
        }
      }
    };

    websocket.onmessage = function(ev) {
      logger.debug('onmessage: len=' + ev.data.length)
      var dic = JSON.parse(ev.data);
      if ('head' in dic) {
        parentinit(document.head, 'dominter-js');
        var head = dic['head'];
        if (head['_childList']) {
          appendElements(ws, document.head, head['_childList']);
        }
        headId = head._id;
        logger.debug('rcv head')
      }
      if ('body' in dic) {
        document.body.innerHTML = '';
        var body = dic['body'];
        if (body['_childList']) {
          appendElements(ws, document.body, body['_childList']);
        }
        bodyId = body._id;
        logger.debug('rcv body')
        while (0 < ws.waitque.length) {
          var dat = ws.waitque.shift();
          ws.websocket.send(dat);
        }
      }
      if ('_window_element' in dic) {
        var dat = dic['_window_element'];
        newWindow(ws, dat);
        logger.debug('rcv _window_element')
      }
      if ('diff' in dic) {
        diffproc(ws, dic, 'diff');
        logger.debug('rcv diff')
      }
      if ('type' in dic) {
        typeproc(ws, dic);
        logger.debug('rcv type')
      }
    };
  };
  var url = (location.protocol == 'https:' ? 'wss:' : 'ws:') +
    location.host + wspath;

  var ws = new DominterWs(url);
})();
