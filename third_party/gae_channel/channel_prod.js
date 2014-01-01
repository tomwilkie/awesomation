(function() {
    function h(a) {
        throw a;
    }

    var i = void 0,m = null,n,o = this,aa = function(a) {
        for (var a = a.split("."),b = o,c; c = a.shift();)if (b[c] != m)b = b[c]; else return m;
        return b
    },ba = function() {
    },ca = function(a) {
        var b = typeof a;
        if (b == "object")if (a) {
            if (a instanceof Array)return"array"; else if (a instanceof Object)return b;
            var c = Object.prototype.toString.call(a);
            if (c == "[object Window]")return"object";
            if (c == "[object Array]" || typeof a.length == "number" && typeof a.splice != "undefined" && typeof a.propertyIsEnumerable != "undefined" && !a.propertyIsEnumerable("splice"))return"array";
            if (c ==
                    "[object Function]" || typeof a.call != "undefined" && typeof a.propertyIsEnumerable != "undefined" && !a.propertyIsEnumerable("call"))return"function"
        } else return"null"; else if (b == "function" && typeof a.call == "undefined")return"object";
        return b
    },q = function(a) {
        return ca(a) == "array"
    },r = function(a) {
        var b = ca(a);
        return b == "array" || b == "object" && typeof a.length == "number"
    },s = function(a) {
        return typeof a == "string"
    },da = function(a) {
        return ca(a) == "function"
    },ea = function(a) {
        a = ca(a);
        return a == "object" || a == "array" || a == "function"
    },
            ha = function(a) {
                return a[fa] || (a[fa] = ++ga)
            },fa = "closure_uid_" + Math.floor(Math.random() * 2147483648).toString(36),ga = 0,ia = function(a) {
        return a.call.apply(a.bind, arguments)
    },ja = function(a, b) {
        var c = b || o;
        if (arguments.length > 2) {
            var d = Array.prototype.slice.call(arguments, 2);
            return function() {
                var b = Array.prototype.slice.call(arguments);
                Array.prototype.unshift.apply(b, d);
                return a.apply(c, b)
            }
        } else return function() {
            return a.apply(c, arguments)
        }
    },t = function() {
        t = Function.prototype.bind && Function.prototype.bind.toString().indexOf("native code") !=
                -1 ? ia : ja;
        return t.apply(m, arguments)
    },ka = function(a) {
        var b = Array.prototype.slice.call(arguments, 1);
        return function() {
            var c = Array.prototype.slice.call(arguments);
            c.unshift.apply(c, b);
            return a.apply(this, c)
        }
    },la = Date.now || function() {
        return+new Date
    },v = function(a, b) {
        var c = a.split("."),d = o;
        !(c[0]in d) && d.execScript && d.execScript("var " + c[0]);
        for (var e; c.length && (e = c.shift());)!c.length && b !== i ? d[e] = b : d = d[e] ? d[e] : d[e] = {}
    },w = function(a, b) {
        function c() {
        }

        c.prototype = b.prototype;
        a.A = b.prototype;
        a.prototype =
                new c;
        a.prototype.constructor = a
    };
    Function.prototype.bind = Function.prototype.bind || function(a) {
        if (arguments.length > 1) {
            var b = Array.prototype.slice.call(arguments, 1);
            b.unshift(this, a);
            return t.apply(m, b)
        } else return t(this, a)
    };
    var x = function() {
    };
    x.prototype.ia = !1;
    x.prototype.H = function() {
        if (!this.ia)this.ia = !0,this.i()
    };
    x.prototype.i = function() {
    };
    var ma = function(a) {
        this.stack = Error().stack || "";
        if (a)this.message = String(a)
    };
    w(ma, Error);
    ma.prototype.name = "CustomError";
    var na = function(a) {
        for (var b = 1; b < arguments.length; b++)var c = String(arguments[b]).replace(/\$/g, "$$$$"),a = a.replace(/\%s/, c);
        return a
    },oa = /^[a-zA-Z0-9\-_.!~*'()]*$/,pa = function(a) {
        a = String(a);
        if (!oa.test(a))return encodeURIComponent(a);
        return a
    },va = function(a) {
        if (!qa.test(a))return a;
        a.indexOf("&") != -1 && (a = a.replace(ra, "&amp;"));
        a.indexOf("<") != -1 && (a = a.replace(sa, "&lt;"));
        a.indexOf(">") != -1 && (a = a.replace(ta, "&gt;"));
        a.indexOf('"') != -1 && (a = a.replace(ua, "&quot;"));
        return a
    },ra = /&/g,sa = /</g,ta = />/g,
            ua = /\"/g,qa = /[&<>\"]/,xa = function(a, b) {
        for (var c = 0,d = String(a).replace(/^[\s\xa0]+|[\s\xa0]+$/g, "").split("."),e = String(b).replace(/^[\s\xa0]+|[\s\xa0]+$/g, "").split("."),f = Math.max(d.length, e.length),g = 0; c == 0 && g < f; g++) {
            var j = d[g] || "",k = e[g] || "",l = RegExp("(\\d*)(\\D*)", "g"),u = RegExp("(\\d*)(\\D*)", "g");
            do{
                var p = l.exec(j) || ["","",""],D = u.exec(k) || ["","",""];
                if (p[0].length == 0 && D[0].length == 0)break;
                c = wa(p[1].length == 0 ? 0 : parseInt(p[1], 10), D[1].length == 0 ? 0 : parseInt(D[1], 10)) || wa(p[2].length == 0, D[2].length ==
                        0) || wa(p[2], D[2])
            } while (c == 0)
        }
        return c
    },wa = function(a, b) {
        if (a < b)return-1; else if (a > b)return 1;
        return 0
    };
    var ya = function(a, b) {
        b.unshift(a);
        ma.call(this, na.apply(m, b));
        b.shift();
        this.sc = a
    };
    w(ya, ma);
    ya.prototype.name = "AssertionError";
    var za = function(a, b) {
        if (!a) {
            var c = Array.prototype.slice.call(arguments, 2),d = "Assertion failed";
            if (b) {
                d += ": " + b;
                var e = c
            }
            h(new ya("" + d, e || []))
        }
    },Aa = function(a) {
        h(new ya("Failure" + (a ? ": " + a : ""), Array.prototype.slice.call(arguments, 1)))
    };
    var y = Array.prototype,Ba = y.indexOf ? function(a, b, c) {
        za(a.length != m);
        return y.indexOf.call(a, b, c)
    } : function(a, b, c) {
        c = c == m ? 0 : c < 0 ? Math.max(0, a.length + c) : c;
        if (s(a)) {
            if (!s(b) || b.length != 1)return-1;
            return a.indexOf(b, c)
        }
        for (; c < a.length; c++)if (c in a && a[c] === b)return c;
        return-1
    },Ca = y.forEach ? function(a, b, c) {
        za(a.length != m);
        y.forEach.call(a, b, c)
    } : function(a, b, c) {
        for (var d = a.length,e = s(a) ? a.split("") : a,f = 0; f < d; f++)f in e && b.call(c, e[f], f, a)
    },Da = function(a, b) {
        var c = Ba(a, b);
        c >= 0 && (za(a.length != m),y.splice.call(a,
                c, 1))
    },Ea = function() {
        return y.concat.apply(y, arguments)
    },Fa = function(a) {
        if (q(a))return Ea(a); else {
            for (var b = [],c = 0,d = a.length; c < d; c++)b[c] = a[c];
            return b
        }
    },Ga = function(a) {
        for (var b = 1; b < arguments.length; b++) {
            var c = arguments[b],d;
            if (q(c) || (d = r(c)) && c.hasOwnProperty("callee"))a.push.apply(a, c); else if (d)for (var e = a.length,f = c.length,g = 0; g < f; g++)a[e + g] = c[g]; else a.push(c)
        }
    },Ha = function(a, b, c) {
        za(a.length != m);
        return arguments.length <= 2 ? y.slice.call(a, b) : y.slice.call(a, b, c)
    };
    var Ia = function(a, b) {
        for (var c in a)b.call(i, a[c], c, a)
    },Ja = function(a) {
        var b = [],c = 0,d;
        for (d in a)b[c++] = a[d];
        return b
    },Ka = function(a) {
        var b = [],c = 0,d;
        for (d in a)b[c++] = d;
        return b
    },La = ["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"],Ma = function(a) {
        for (var b,c,d = 1; d < arguments.length; d++) {
            c = arguments[d];
            for (b in c)a[b] = c[b];
            for (var e = 0; e < La.length; e++)b = La[e],Object.prototype.hasOwnProperty.call(c, b) && (a[b] = c[b])
        }
    };
    var Na,Oa,Pa,Qa,Ra = function() {
        return o.navigator ? o.navigator.userAgent : m
    };
    Qa = Pa = Oa = Na = !1;
    var Sa;
    if (Sa = Ra()) {
        var Ta = o.navigator;
        Na = Sa.indexOf("Opera") == 0;
        Oa = !Na && Sa.indexOf("MSIE") != -1;
        Pa = !Na && Sa.indexOf("WebKit") != -1;
        Qa = !Na && !Pa && Ta.product == "Gecko"
    }
    var z = Oa,Ua = Qa,A = Pa,Va = o.navigator,Wa = (Va && Va.platform || "").indexOf("Mac") != -1,Xa;
    a:{
        var Ya = "",Za;
        if (Na && o.opera)var $a = o.opera.version,Ya = typeof $a == "function" ? $a() : $a; else if (Ua ? Za = /rv\:([^\);]+)(\)|;)/ : z ? Za = /MSIE\s+([^\);]+)(\)|;)/ : A && (Za = /WebKit\/(\S+)/),Za)var ab = Za.exec(Ra()),Ya = ab ? ab[1] : "";
        if (z) {
            var bb,cb = o.document;
            bb = cb ? cb.documentMode : i;
            if (bb > parseFloat(Ya)) {
                Xa = String(bb);
                break a
            }
        }
        Xa = Ya
    }
    var db = Xa,eb = {},B = function(a) {
        return eb[a] || (eb[a] = xa(db, a) >= 0)
    };
    var fb,gb = !z || B("9");
    !Ua && !z || z && B("9") || Ua && B("1.9.1");
    z && B("9");
    var hb = function(a) {
        var b;
        b = (b = a.className) && typeof b.split == "function" ? b.split(/\s+/) : [];
        var c = Ha(arguments, 1),d;
        d = b;
        for (var e = 0,f = 0; f < c.length; f++)Ba(d, c[f]) >= 0 || (d.push(c[f]),e++);
        d = e == c.length;
        a.className = b.join(" ");
        return d
    };
    var C = function(a) {
        return a ? new ib(a.nodeType == 9 ? a : a.ownerDocument || a.document) : fb || (fb = new ib)
    },jb = function(a, b) {
        var c = b && b != "*" ? b.toUpperCase() : "";
        if (a.querySelectorAll && a.querySelector && (!A || document.compatMode == "CSS1Compat" || B("528")) && c)return a.querySelectorAll(c + "");
        return a.getElementsByTagName(c || "*")
    },lb = function(a, b) {
        Ia(b, function(b, d) {
            d == "style" ? a.style.cssText = b : d == "class" ? a.className = b : d == "for" ? a.htmlFor = b : d in kb ? a.setAttribute(kb[d], b) : a[d] = b
        })
    },kb = {cellpadding:"cellPadding",cellspacing:"cellSpacing",
        colspan:"colSpan",rowspan:"rowSpan",valign:"vAlign",height:"height",width:"width",usemap:"useMap",frameborder:"frameBorder",maxlength:"maxLength",type:"type"},nb = function(a, b, c) {
        function d(c) {
            c && b.appendChild(s(c) ? a.createTextNode(c) : c)
        }

        for (var e = 2; e < c.length; e++) {
            var f = c[e];
            r(f) && !(ea(f) && f.nodeType > 0) ? Ca(mb(f) ? Fa(f) : f, d) : d(f)
        }
    },ob = function(a) {
        return a && a.parentNode ? a.parentNode.removeChild(a) : m
    },mb = function(a) {
        if (a && typeof a.length == "number")if (ea(a))return typeof a.item == "function" || typeof a.item ==
                "string"; else if (da(a))return typeof a.item == "function";
        return!1
    },ib = function(a) {
        this.u = a || o.document || document
    };
    n = ib.prototype;
    n.rb = function() {
        var a = this.u,b = arguments,c = b[0],d = b[1];
        if (!gb && d && (d.name || d.type)) {
            c = ["<",c];
            d.name && c.push(' name="', va(d.name), '"');
            if (d.type) {
                c.push(' type="', va(d.type), '"');
                var e = {};
                Ma(e, d);
                d = e;
                delete d.type
            }
            c.push(">");
            c = c.join("")
        }
        c = a.createElement(c);
        if (d)s(d) ? c.className = d : q(d) ? hb.apply(m, [c].concat(d)) : lb(c, d);
        b.length > 2 && nb(a, c, b);
        return c
    };
    n.createElement = function(a) {
        return this.u.createElement(a)
    };
    n.createTextNode = function(a) {
        return this.u.createTextNode(a)
    };
    n.e = function() {
        return this.u.parentWindow || this.u.defaultView
    };
    n.appendChild = function(a, b) {
        a.appendChild(b)
    };
    n.removeNode = ob;
    var pb = new Function("a", "return a"),qb = function(a, b) {
        try {
            return pb(a[b]),!0
        } catch(c) {
        }
        return!1
    };
    var rb;
    !z || B("9");
    z && B("8");
    var sb = function(a, b) {
        this.type = a;
        this.currentTarget = this.target = b
    };
    w(sb, x);
    sb.prototype.i = function() {
        delete this.type;
        delete this.target;
        delete this.currentTarget
    };
    sb.prototype.Na = !1;
    sb.prototype.hc = !0;
    var tb = function(a, b) {
        a && this.oa(a, b)
    };
    w(tb, sb);
    n = tb.prototype;
    n.target = m;
    n.relatedTarget = m;
    n.offsetX = 0;
    n.offsetY = 0;
    n.clientX = 0;
    n.clientY = 0;
    n.screenX = 0;
    n.screenY = 0;
    n.button = 0;
    n.keyCode = 0;
    n.charCode = 0;
    n.ctrlKey = !1;
    n.altKey = !1;
    n.shiftKey = !1;
    n.metaKey = !1;
    n.gc = !1;
    n.qa = m;
    n.oa = function(a, b) {
        var c = this.type = a.type;
        sb.call(this, c);
        this.target = a.target || a.srcElement;
        this.currentTarget = b;
        var d = a.relatedTarget;
        if (d)Ua && (qb(d, "nodeName") || (d = m)); else if (c == "mouseover")d = a.fromElement; else if (c == "mouseout")d = a.toElement;
        this.relatedTarget = d;
        this.offsetX = a.offsetX !== i ? a.offsetX : a.layerX;
        this.offsetY = a.offsetY !== i ? a.offsetY : a.layerY;
        this.clientX = a.clientX !== i ? a.clientX : a.pageX;
        this.clientY = a.clientY !== i ? a.clientY : a.pageY;
        this.screenX = a.screenX || 0;
        this.screenY = a.screenY || 0;
        this.button = a.button;
        this.keyCode = a.keyCode || 0;
        this.charCode = a.charCode || (c == "keypress" ? a.keyCode : 0);
        this.ctrlKey = a.ctrlKey;
        this.altKey = a.altKey;
        this.shiftKey = a.shiftKey;
        this.metaKey = a.metaKey;
        this.gc = Wa ? a.metaKey : a.ctrlKey;
        this.state = a.state;
        this.qa = a;
        delete this.hc;
        delete this.Na
    };
    n.i = function() {
        tb.A.i.call(this);
        this.relatedTarget = this.currentTarget = this.target = this.qa = m
    };
    var E = function(a, b) {
        this.Bb = b;
        this.O = [];
        a > this.Bb && h(Error("[goog.structs.SimplePool] Initial cannot be greater than max"));
        for (var c = 0; c < a; c++)this.O.push(this.D ? this.D() : {})
    };
    w(E, x);
    E.prototype.D = m;
    E.prototype.Eb = m;
    E.prototype.getObject = function() {
        if (this.O.length)return this.O.pop();
        return this.D ? this.D() : {}
    };
    var vb = function(a, b) {
        a.O.length < a.Bb ? a.O.push(b) : ub(a, b)
    },ub = function(a, b) {
        if (a.Eb)a.Eb(b); else if (ea(b))if (da(b.H))b.H(); else for (var c in b)delete b[c]
    };
    E.prototype.i = function() {
        E.A.i.call(this);
        for (var a = this.O; a.length;)ub(this, a.pop());
        delete this.O
    };
    var wb,xb = (wb = "ScriptEngine"in o && o.ScriptEngine() == "JScript") ? o.ScriptEngineMajorVersion() + "." + o.ScriptEngineMinorVersion() + "." + o.ScriptEngineBuildVersion() : "0";
    var yb = function() {
    },zb = 0;
    n = yb.prototype;
    n.key = 0;
    n.Y = !1;
    n.zb = !1;
    n.oa = function(a, b, c, d, e, f) {
        da(a) ? this.yb = !0 : a && a.handleEvent && da(a.handleEvent) ? this.yb = !1 : h(Error("Invalid listener argument"));
        this.ga = a;
        this.pb = b;
        this.src = c;
        this.type = d;
        this.capture = !!e;
        this.Ka = f;
        this.zb = !1;
        this.key = ++zb;
        this.Y = !1
    };
    n.handleEvent = function(a) {
        if (this.yb)return this.ga.call(this.Ka || this.src, a);
        return this.ga.handleEvent.call(this.ga, a)
    };
    var Ab,Bb,Cb,Db,Eb,Fb,Gb,Hb,Ib,Jb,Kb;
    (function() {
        function a() {
            return{g:0,W:0}
        }

        function b() {
            return[]
        }

        function c() {
            var a = function(b) {
                return g.call(a.src, a.key, b)
            };
            return a
        }

        function d() {
            return new yb
        }

        function e() {
            return new tb
        }

        var f = wb && !(xa(xb, "5.7") >= 0),g;
        Fb = function(a) {
            g = a
        };
        if (f) {
            Ab = function() {
                return j.getObject()
            };
            Bb = function(a) {
                vb(j, a)
            };
            Cb = function() {
                return k.getObject()
            };
            Db = function(a) {
                vb(k, a)
            };
            Eb = function() {
                return l.getObject()
            };
            Gb = function() {
                vb(l, c())
            };
            Hb = function() {
                return u.getObject()
            };
            Ib = function(a) {
                vb(u, a)
            };
            Jb = function() {
                return p.getObject()
            };
            Kb = function(a) {
                vb(p, a)
            };
            var j = new E(0, 600);
            j.D = a;
            var k = new E(0, 600);
            k.D = b;
            var l = new E(0, 600);
            l.D = c;
            var u = new E(0, 600);
            u.D = d;
            var p = new E(0, 600);
            p.D = e
        } else Ab = a,Bb = ba,Cb = b,Db = ba,Eb = c,Gb = ba,Hb = d,Ib = ba,Jb = e,Kb = ba
    })();
    var Lb = {},G = {},Mb = {},Nb = {},Ob = function(a, b, c, d, e) {
        if (b)if (q(b))for (var f = 0; f < b.length; f++)Ob(a, b[f], c, d, e); else {
            var d = !!d,g = G;
            b in g || (g[b] = Ab());
            g = g[b];
            d in g || (g[d] = Ab(),g.g++);
            var g = g[d],j = ha(a),k;
            g.W++;
            if (g[j]) {
                k = g[j];
                for (f = 0; f < k.length; f++)if (g = k[f],g.ga == c && g.Ka == e) {
                    if (g.Y)break;
                    return
                }
            } else k = g[j] = Cb(),g.g++;
            f = Eb();
            f.src = a;
            g = Hb();
            g.oa(c, f, a, b, d, e);
            c = g.key;
            f.key = c;
            k.push(g);
            Lb[c] = g;
            Mb[j] || (Mb[j] = Cb());
            Mb[j].push(g);
            a.addEventListener ? (a == o || !a.Yb) && a.addEventListener(b, f, d) : a.attachEvent(Pb(b),
                    f)
        } else h(Error("Invalid event type"))
    },Qb = function(a, b, c, d, e) {
        if (q(b))for (var f = 0; f < b.length; f++)Qb(a, b[f], c, d, e); else {
            d = !!d;
            a:{
                f = G;
                if (b in f && (f = f[b],d in f && (f = f[d],a = ha(a),f[a]))) {
                    a = f[a];
                    break a
                }
                a = m
            }
            if (a)for (f = 0; f < a.length; f++)if (a[f].ga == c && a[f].capture == d && a[f].Ka == e) {
                Rb(a[f].key);
                break
            }
        }
    },Rb = function(a) {
        if (Lb[a]) {
            var b = Lb[a];
            if (!b.Y) {
                var c = b.src,d = b.type,e = b.pb,f = b.capture;
                c.removeEventListener ? (c == o || !c.Yb) && c.removeEventListener(d, e, f) : c.detachEvent && c.detachEvent(Pb(d), e);
                c = ha(c);
                e = G[d][f][c];
                if (Mb[c]) {
                    var g = Mb[c];
                    Da(g, b);
                    g.length == 0 && delete Mb[c]
                }
                b.Y = !0;
                e.sb = !0;
                Sb(d, f, c, e);
                delete Lb[a]
            }
        }
    },Sb = function(a, b, c, d) {
        if (!d.va && d.sb) {
            for (var e = 0,f = 0; e < d.length; e++)if (d[e].Y) {
                var g = d[e].pb;
                g.src = m;
                Gb(g);
                Ib(d[e])
            } else e != f && (d[f] = d[e]),f++;
            d.length = f;
            d.sb = !1;
            f == 0 && (Db(d),delete G[a][b][c],G[a][b].g--,G[a][b].g == 0 && (Bb(G[a][b]),delete G[a][b],G[a].g--),G[a].g == 0 && (Bb(G[a]),delete G[a]))
        }
    },Pb = function(a) {
        if (a in Nb)return Nb[a];
        return Nb[a] = "on" + a
    },Ub = function(a, b, c, d, e) {
        var f = 1,b = ha(b);
        if (a[b]) {
            a.W--;
            a = a[b];
            a.va ? a.va++ : a.va = 1;
            try {
                for (var g = a.length,j = 0; j < g; j++) {
                    var k = a[j];
                    k && !k.Y && (f &= Tb(k, e) !== !1)
                }
            } finally {
                a.va--,Sb(c, d, b, a)
            }
        }
        return Boolean(f)
    },Tb = function(a, b) {
        var c = a.handleEvent(b);
        a.zb && Rb(a.key);
        return c
    };
    Fb(function(a, b) {
        if (!Lb[a])return!0;
        var c = Lb[a],d = c.type,e = G;
        if (!(d in e))return!0;
        var e = e[d],f,g;
        rb === i && (rb = z && !o.addEventListener);
        if (rb) {
            f = b || aa("window.event");
            var j = !0 in e,k = !1 in e;
            if (j) {
                if (f.keyCode < 0 || f.returnValue != i)return!0;
                a:{
                    var l = !1;
                    if (f.keyCode == 0)try {
                        f.keyCode = -1;
                        break a
                    } catch(u) {
                        l = !0
                    }
                    if (l || f.returnValue == i)f.returnValue = !0
                }
            }
            l = Jb();
            l.oa(f, this);
            f = !0;
            try {
                if (j) {
                    for (var p = Cb(),D = l.currentTarget; D; D = D.parentNode)p.push(D);
                    g = e[!0];
                    g.W = g.g;
                    for (var F = p.length - 1; !l.Na && F >= 0 && g.W; F--)l.currentTarget =
                            p[F],f &= Ub(g, p[F], d, !0, l);
                    if (k) {
                        g = e[!1];
                        g.W = g.g;
                        for (F = 0; !l.Na && F < p.length && g.W; F++)l.currentTarget = p[F],f &= Ub(g, p[F], d, !1, l)
                    }
                } else f = Tb(c, l)
            } finally {
                if (p)p.length = 0,Db(p);
                l.H();
                Kb(l)
            }
            return f
        }
        d = new tb(b, this);
        try {
            f = Tb(c, d)
        } finally {
            d.H()
        }
        return f
    });
    var Vb = function(a) {
        var a = String(a),b;
        b = /^\s*$/.test(a) ? !1 : /^[\],:{}\s\u2028\u2029]*$/.test(a.replace(/\\["\\\/bfnrtu]/g, "@").replace(/"[^"\\\n\r\u2028\u2029\x00-\x08\x10-\x1f\x80-\x9f]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:[\s\u2028\u2029]*\[)+/g, ""));
        if (b)try {
            return eval("(" + a + ")")
        } catch(c) {
        }
        h(Error("Invalid JSON string: " + a))
    },Wb = function() {
    },Yb = function(a) {
        var b = [];
        Xb(new Wb, a, b);
        return b.join("")
    },Xb = function(a, b, c) {
        switch (typeof b) {
            case "string":
                Zb(b,
                        c);
                break;
            case "number":
                c.push(isFinite(b) && !isNaN(b) ? b : "null");
                break;
            case "boolean":
                c.push(b);
                break;
            case "undefined":
                c.push("null");
                break;
            case "object":
                if (b == m) {
                    c.push("null");
                    break
                }
                if (q(b)) {
                    var d = b.length;
                    c.push("[");
                    for (var e = "",f = 0; f < d; f++)c.push(e),Xb(a, b[f], c),e = ",";
                    c.push("]");
                    break
                }
                c.push("{");
                d = "";
                for (e in b)Object.prototype.hasOwnProperty.call(b, e) && (f = b[e],typeof f != "function" && (c.push(d),Zb(e, c),c.push(":"),Xb(a, f, c),d = ","));
                c.push("}");
                break;
            case "function":
                break;
            default:
                h(Error("Unknown type: " +
                        typeof b))
        }
    },$b = {'"':'\\"',"\\":"\\\\","/":"\\/","\u0008":"\\b","\u000c":"\\f","\n":"\\n","\r":"\\r","\t":"\\t","\u000b":"\\u000b"},ac = /\uffff/.test("\uffff") ? /[\\\"\x00-\x1f\x7f-\uffff]/g : /[\\\"\x00-\x1f\x7f-\xff]/g,Zb = function(a, b) {
        b.push('"', a.replace(ac, function(a) {
            if (a in $b)return $b[a];
            var b = a.charCodeAt(0),e = "\\u";
            b < 16 ? e += "000" : b < 256 ? e += "00" : b < 4096 && (e += "0");
            return $b[a] = e + b.toString(16)
        }), '"')
    };
    var bc = "StopIteration"in o ? o.StopIteration : Error("StopIteration"),cc = function() {
    };
    cc.prototype.next = function() {
        h(bc)
    };
    cc.prototype.kc = function() {
        return this
    };
    var dc = function(a) {
        if (typeof a.L == "function")return a.L();
        if (s(a))return a.split("");
        if (r(a)) {
            for (var b = [],c = a.length,d = 0; d < c; d++)b.push(a[d]);
            return b
        }
        return Ja(a)
    },ec = function(a, b, c) {
        if (typeof a.forEach == "function")a.forEach(b, c); else if (r(a) || s(a))Ca(a, b, c); else {
            var d;
            if (typeof a.Z == "function")d = a.Z(); else if (typeof a.L != "function")if (r(a) || s(a)) {
                d = [];
                for (var e = a.length,f = 0; f < e; f++)d.push(f)
            } else d = Ka(a); else d = i;
            for (var e = dc(a),f = e.length,g = 0; g < f; g++)b.call(c, e[g], d && d[g], a)
        }
    };
    var H = function(a) {
        this.z = {};
        this.j = [];
        var b = arguments.length;
        if (b > 1) {
            b % 2 && h(Error("Uneven number of arguments"));
            for (var c = 0; c < b; c += 2)this.set(arguments[c], arguments[c + 1])
        } else if (a) {
            a instanceof H ? (b = a.Z(),c = a.L()) : (b = Ka(a),c = Ja(a));
            for (var d = 0; d < b.length; d++)this.set(b[d], c[d])
        }
    };
    n = H.prototype;
    n.g = 0;
    n.pa = 0;
    n.L = function() {
        fc(this);
        for (var a = [],b = 0; b < this.j.length; b++)a.push(this.z[this.j[b]]);
        return a
    };
    n.Z = function() {
        fc(this);
        return this.j.concat()
    };
    n.M = function(a) {
        return gc(this.z, a)
    };
    n.remove = function(a) {
        if (gc(this.z, a))return delete this.z[a],this.g--,this.pa++,this.j.length > 2 * this.g && fc(this),!0;
        return!1
    };
    var fc = function(a) {
        if (a.g != a.j.length) {
            for (var b = 0,c = 0; b < a.j.length;) {
                var d = a.j[b];
                gc(a.z, d) && (a.j[c++] = d);
                b++
            }
            a.j.length = c
        }
        if (a.g != a.j.length) {
            for (var e = {},c = b = 0; b < a.j.length;)d = a.j[b],gc(e, d) || (a.j[c++] = d,e[d] = 1),b++;
            a.j.length = c
        }
    };
    H.prototype.get = function(a, b) {
        if (gc(this.z, a))return this.z[a];
        return b
    };
    H.prototype.set = function(a, b) {
        gc(this.z, a) || (this.g++,this.j.push(a),this.pa++);
        this.z[a] = b
    };
    H.prototype.ca = function() {
        return new H(this)
    };
    H.prototype.kc = function(a) {
        fc(this);
        var b = 0,c = this.j,d = this.z,e = this.pa,f = this,g = new cc;
        g.next = function() {
            for (; ;) {
                e != f.pa && h(Error("The map has changed since the iterator was created"));
                b >= c.length && h(bc);
                var g = c[b++];
                return a ? g : d[g]
            }
        };
        return g
    };
    var gc = function(a, b) {
        return Object.prototype.hasOwnProperty.call(a, b)
    };
    var ic = function(a) {
        return hc(a || arguments.callee.caller, [])
    },hc = function(a, b) {
        var c = [];
        if (Ba(b, a) >= 0)c.push("[...circular reference...]"); else if (a && b.length < 50) {
            c.push(jc(a) + "(");
            for (var d = a.arguments,e = 0; e < d.length; e++) {
                e > 0 && c.push(", ");
                var f;
                f = d[e];
                switch (typeof f) {
                    case "object":
                        f = f ? "object" : "null";
                        break;
                    case "string":
                        break;
                    case "number":
                        f = String(f);
                        break;
                    case "boolean":
                        f = f ? "true" : "false";
                        break;
                    case "function":
                        f = (f = jc(f)) ? f : "[fn]";
                        break;
                    default:
                        f = typeof f
                }
                f.length > 40 && (f = f.substr(0, 40) + "...");
                c.push(f)
            }
            b.push(a);
            c.push(")\n");
            try {
                c.push(hc(a.caller, b))
            } catch(g) {
                c.push("[exception trying to get caller]\n")
            }
        } else a ? c.push("[...long stack...]") : c.push("[end]");
        return c.join("")
    },jc = function(a) {
        a = String(a);
        if (!kc[a]) {
            var b = /function ([^\(]+)/.exec(a);
            kc[a] = b ? b[1] : "[Anonymous]"
        }
        return kc[a]
    },kc = {};
    var lc = function(a, b, c, d, e) {
        this.reset(a, b, c, d, e)
    };
    lc.prototype.sa = 0;
    lc.prototype.xb = m;
    lc.prototype.wb = m;
    var mc = 0;
    lc.prototype.reset = function(a, b, c, d, e) {
        this.sa = typeof e == "number" ? e : mc++;
        this.pc = d || la();
        this.ha = a;
        this.fc = b;
        this.oc = c;
        delete this.xb;
        delete this.wb
    };
    lc.prototype.Db = function(a) {
        this.ha = a
    };
    var I = function(a) {
        this.Fb = a
    };
    I.prototype.ya = m;
    I.prototype.ha = m;
    I.prototype.Ra = m;
    I.prototype.Jb = m;
    var nc = function(a, b) {
        this.name = a;
        this.value = b
    };
    nc.prototype.toString = function() {
        return this.name
    };
    var oc = new nc("SEVERE", 1E3),pc = new nc("WARNING", 900),qc = new nc("INFO", 800),rc = new nc("CONFIG", 700),sc = new nc("FINE", 500),tc = new nc("FINEST", 300);
    I.prototype.getName = function() {
        return this.Fb
    };
    I.prototype.getParent = function() {
        return this.ya
    };
    I.prototype.Db = function(a) {
        this.ha = a
    };
    var uc = function(a) {
        if (a.ha)return a.ha;
        if (a.ya)return uc(a.ya);
        Aa("Root logger has no level set.");
        return m
    };
    I.prototype.log = function(a, b, c) {
        if (a.value >= uc(this).value) {
            a = this.jc(a, b, c);
            o.console && o.console.markTimeline && o.console.markTimeline("log:" + a.fc);
            for (b = this; b;) {
                var c = b,d = a;
                if (c.Jb)for (var e = 0,f = i; f = c.Jb[e]; e++)f(d);
                b = b.getParent()
            }
        }
    };
    I.prototype.jc = function(a, b, c) {
        var d = new lc(a, String(b), this.Fb);
        if (c) {
            d.xb = c;
            var e;
            var f = arguments.callee.caller;
            try {
                var g;
                var j = aa("window.location.href");
                if (s(c))g = {message:c,name:"Unknown error",lineNumber:"Not available",fileName:j,stack:"Not available"}; else {
                    var k,l,u = !1;
                    try {
                        k = c.lineNumber || c.qc || "Not available"
                    } catch(p) {
                        k = "Not available",u = !0
                    }
                    try {
                        l = c.fileName || c.filename || c.sourceURL || j
                    } catch(D) {
                        l = "Not available",u = !0
                    }
                    g = u || !c.lineNumber || !c.fileName || !c.stack ? {message:c.message,name:c.name,
                        lineNumber:k,fileName:l,stack:c.stack || "Not available"} : c
                }
                e = "Message: " + va(g.message) + '\nUrl: <a href="view-source:' + g.fileName + '" target="_new">' + g.fileName + "</a>\nLine: " + g.lineNumber + "\n\nBrowser stack:\n" + va(g.stack + "-> ") + "[end]\n\nJS stack traversal:\n" + va(ic(f) + "-> ")
            } catch(F) {
                e = "Exception trying to expose exception! You win, we lose. " + F
            }
            d.wb = e
        }
        return d
    };
    var K = function(a, b) {
        J.log(oc, a, b)
    },L = function(a, b) {
        a.log(pc, b, i)
    };
    I.prototype.info = function(a, b) {
        this.log(qc, a, b)
    };
    var M = function(a) {
        J.log(sc, a, i)
    },N = function(a) {
        J.log(tc, a, i)
    },vc = {},wc = m,xc = function(a) {
        wc || (wc = new I(""),vc[""] = wc,wc.Db(rc));
        var b;
        if (!(b = vc[a])) {
            b = new I(a);
            var c = a.lastIndexOf("."),d = a.substr(c + 1),c = xc(a.substr(0, c));
            if (!c.Ra)c.Ra = {};
            c.Ra[d] = b;
            b.ya = c;
            vc[a] = b
        }
        return b
    };
    var yc = function() {
        this.ja = {}
    };
    w(yc, x);
    yc.prototype.la = xc("goog.messaging.AbstractChannel");
    yc.prototype.t = function(a) {
        a && a()
    };
    yc.prototype.q = function() {
        return!0
    };
    var zc = function(a, b, c) {
        a.ja[b] = {kb:c,lb:!1}
    };
    yc.prototype.i = function() {
        yc.A.i.call(this);
        var a = this.la;
        a && typeof a.H == "function" && a.H();
        delete this.la;
        delete this.ja;
        delete this.Ya
    };
    var Ac = RegExp("^(?:([^:/?#.]+):)?(?://(?:([^/?#]*)@)?([\\w\\d\\-\\u0100-\\uffff.%]*)(?::([0-9]+))?)?([^?#]+)?(?:\\?([^#]*))?(?:#(.*))?$"),Bc = function(a) {
        var b = a.match(Ac),a = b[1],c = b[2],d = b[3],b = b[4],e = [];
        a && e.push(a, ":");
        d && (e.push("//"),c && e.push(c, "@"),e.push(d),b && e.push(":", b));
        return e.join("")
    };
    var O = function(a, b) {
        var c;
        a instanceof O ? (this.V(b == m ? a.v : b),P(this, a.n),Cc(this, a.fa),Dc(this, a.J),Ec(this, a.G),Fc(this, a.K),Gc(this, a.w.ca()),Hc(this, a.ea)) : a && (c = String(a).match(Ac)) ? (this.V(!!b),P(this, c[1] || "", !0),Cc(this, c[2] || "", !0),Dc(this, c[3] || "", !0),Ec(this, c[4]),Fc(this, c[5] || "", !0),Gc(this, c[6] || "", !0),Hc(this, c[7] || "", !0)) : (this.V(!!b),this.w = new Ic(m, this, this.v))
    };
    n = O.prototype;
    n.n = "";
    n.fa = "";
    n.J = "";
    n.G = m;
    n.K = "";
    n.ea = "";
    n.lc = !1;
    n.v = !1;
    n.toString = function() {
        if (this.r)return this.r;
        var a = [];
        this.n && a.push(Jc(this.n, Kc), ":");
        if (this.J) {
            a.push("//");
            this.fa && a.push(Jc(this.fa, Kc), "@");
            var b;
            b = this.J;
            b = s(b) ? encodeURIComponent(b) : m;
            a.push(b);
            this.G != m && a.push(":", String(this.G))
        }
        this.K && (this.J && this.K.charAt(0) != "/" && a.push("/"),a.push(Jc(this.K, this.K.charAt(0) == "/" ? Lc : Mc)));
        (b = String(this.w)) && a.push("?", b);
        this.ea && a.push("#", Jc(this.ea, Nc));
        return this.r = a.join("")
    };
    n.ca = function() {
        var a = this.n,b = this.fa,c = this.J,d = this.G,e = this.K,f = this.w.ca(),g = this.ea,j = new O(m, this.v);
        a && P(j, a);
        b && Cc(j, b);
        c && Dc(j, c);
        d && Ec(j, d);
        e && Fc(j, e);
        f && Gc(j, f);
        g && Hc(j, g);
        return j
    };
    var P = function(a, b, c) {
        Q(a);
        delete a.r;
        a.n = c ? b ? decodeURIComponent(b) : "" : b;
        if (a.n)a.n = a.n.replace(/:$/, "")
    },Cc = function(a, b, c) {
        Q(a);
        delete a.r;
        a.fa = c ? b ? decodeURIComponent(b) : "" : b
    },Dc = function(a, b, c) {
        Q(a);
        delete a.r;
        a.J = c ? b ? decodeURIComponent(b) : "" : b
    },Ec = function(a, b) {
        Q(a);
        delete a.r;
        b ? (b = Number(b),(isNaN(b) || b < 0) && h(Error("Bad port number " + b)),a.G = b) : a.G = m
    },Fc = function(a, b, c) {
        Q(a);
        delete a.r;
        a.K = c ? b ? decodeURIComponent(b) : "" : b
    },Gc = function(a, b, c) {
        Q(a);
        delete a.r;
        b instanceof Ic ? (a.w = b,a.w.La = a,a.w.V(a.v)) :
                (c || (b = Jc(b, Oc)),a.w = new Ic(b, a, a.v))
    },Pc = function(a, b, c) {
        Q(a);
        delete a.r;
        a.w.set(b, c)
    },Hc = function(a, b, c) {
        Q(a);
        delete a.r;
        a.ea = c ? b ? decodeURIComponent(b) : "" : b
    },Q = function(a) {
        a.lc && h(Error("Tried to modify a read-only Uri"))
    };
    O.prototype.V = function(a) {
        this.v = a;
        this.w && this.w.V(a);
        return this
    };
    var Qc = /^[a-zA-Z0-9\-_.!~*'():\/;?]*$/,Jc = function(a, b) {
        var c = m;
        s(a) && (c = a,Qc.test(c) || (c = encodeURI(a)),c.search(b) >= 0 && (c = c.replace(b, Rc)));
        return c
    },Rc = function(a) {
        a = a.charCodeAt(0);
        return"%" + (a >> 4 & 15).toString(16) + (a & 15).toString(16)
    },Kc = /[#\/\?@]/g,Mc = /[\#\?:]/g,Lc = /[\#\?]/g,Oc = /[\#\?@]/g,Nc = /#/g,Ic = function(a, b, c) {
        this.C = a || m;
        this.La = b || m;
        this.v = !!c
    },R = function(a) {
        if (!a.f && (a.f = new H,a.C))for (var b = a.C.split("&"),c = 0; c < b.length; c++) {
            var d = b[c].indexOf("="),e = m,f = m;
            d >= 0 ? (e = b[c].substring(0, d),
                    f = b[c].substring(d + 1)) : e = b[c];
            e = decodeURIComponent(e.replace(/\+/g, " "));
            e = Sc(a, e);
            a.add(e, f ? decodeURIComponent(f.replace(/\+/g, " ")) : "")
        }
    };
    n = Ic.prototype;
    n.f = m;
    n.g = m;
    n.add = function(a, b) {
        R(this);
        Tc(this);
        a = Sc(this, a);
        if (this.M(a)) {
            var c = this.f.get(a);
            q(c) ? c.push(b) : this.f.set(a, [c,b])
        } else this.f.set(a, b);
        this.g++;
        return this
    };
    n.remove = function(a) {
        R(this);
        a = Sc(this, a);
        if (this.f.M(a)) {
            Tc(this);
            var b = this.f.get(a);
            q(b) ? this.g -= b.length : this.g--;
            return this.f.remove(a)
        }
        return!1
    };
    n.M = function(a) {
        R(this);
        a = Sc(this, a);
        return this.f.M(a)
    };
    n.Z = function() {
        R(this);
        for (var a = this.f.L(),b = this.f.Z(),c = [],d = 0; d < b.length; d++) {
            var e = a[d];
            if (q(e))for (var f = 0; f < e.length; f++)c.push(b[d]); else c.push(b[d])
        }
        return c
    };
    n.L = function(a) {
        R(this);
        if (a)if (a = Sc(this, a),this.M(a)) {
            var b = this.f.get(a);
            if (q(b))return b; else a = [],a.push(b)
        } else a = []; else for (var b = this.f.L(),a = [],c = 0; c < b.length; c++) {
            var d = b[c];
            q(d) ? Ga(a, d) : a.push(d)
        }
        return a
    };
    n.set = function(a, b) {
        R(this);
        Tc(this);
        a = Sc(this, a);
        if (this.M(a)) {
            var c = this.f.get(a);
            q(c) ? this.g -= c.length : this.g--
        }
        this.f.set(a, b);
        this.g++;
        return this
    };
    n.get = function(a, b) {
        R(this);
        a = Sc(this, a);
        if (this.M(a)) {
            var c = this.f.get(a);
            return q(c) ? c[0] : c
        } else return b
    };
    n.toString = function() {
        if (this.C)return this.C;
        if (!this.f)return"";
        for (var a = [],b = 0,c = this.f.Z(),d = 0; d < c.length; d++) {
            var e = c[d],f = pa(e),e = this.f.get(e);
            if (q(e))for (var g = 0; g < e.length; g++)b > 0 && a.push("&"),a.push(f),e[g] !== "" && a.push("=", pa(e[g])),b++; else b > 0 && a.push("&"),a.push(f),e !== "" && a.push("=", pa(e)),b++
        }
        return this.C = a.join("")
    };
    var Tc = function(a) {
        delete a.Ma;
        delete a.C;
        a.La && delete a.La.r
    };
    Ic.prototype.ca = function() {
        var a = new Ic;
        if (this.Ma)a.Ma = this.Ma;
        if (this.C)a.C = this.C;
        if (this.f)a.f = this.f.ca();
        return a
    };
    var Sc = function(a, b) {
        var c = String(b);
        a.v && (c = c.toLowerCase());
        return c
    };
    Ic.prototype.V = function(a) {
        a && !this.v && (R(this),Tc(this),ec(this.f, function(a, c) {
            var d = c.toLowerCase();
            c != d && (this.remove(c),this.add(d, a))
        }, this));
        this.v = a
    };
    var Uc = {1:"NativeMessagingTransport",2:"FrameElementMethodTransport",3:"IframeRelayTransport",4:"IframePollingTransport",5:"FlashTransport",6:"NixTransport"},Vc = ["pu","lru","pru","lpu","ppu"],S = {},Xc = function(a) {
        for (var b = Wc,c = b.length,d = ""; a-- > 0;)d += b.charAt(Math.floor(Math.random() * c));
        return d
    },Wc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",J = xc("goog.net.xpc");
    var T = function(a) {
        this.l = a || C()
    };
    w(T, x);
    T.prototype.aa = 0;
    T.prototype.e = function() {
        return this.l.e()
    };
    T.prototype.getName = function() {
        return Uc[this.aa] || ""
    };
    var Yc = function(a, b) {
        this.l = b || C();
        this.a = a;
        this.da = [];
        this.Pb = t(this.Xb, this)
    };
    w(Yc, T);
    n = Yc.prototype;
    n.aa = 2;
    n.Ga = !1;
    n.Tb = 0;
    n.t = function() {
        Zc(this.a) == 0 ? (this.B = this.a.Q,this.B.XPC_toOuter = t(this.eb, this)) : this.cb()
    };
    n.cb = function() {
        var a = !0;
        try {
            if (!this.B)this.B = this.e().frameElement;
            if (this.B && this.B.XPC_toOuter)this.Da = this.B.XPC_toOuter,this.B.XPC_toOuter.XPC_toInner = t(this.eb, this),a = !1,this.send("tp", "SETUP_ACK"),U(this.a)
        } catch(b) {
            K("exception caught while attempting setup: " + b)
        }
        if (a) {
            if (!this.ib)this.ib = t(this.cb, this);
            this.e().setTimeout(this.ib, 100)
        }
    };
    n.Ia = function(a) {
        Zc(this.a) == 0 && !this.a.q() && a == "SETUP_ACK" ? (this.Da = this.B.XPC_toOuter.XPC_toInner,U(this.a)) : h(Error("Got unexpected transport message."))
    };
    n.eb = function(a, b) {
        if (!this.Ga && this.da.length == 0)V(this.a, a, b); else if (this.da.push({Sb:a,Ea:b}),this.da.length == 1)this.Tb = this.e().setTimeout(this.Pb, 1)
    };
    n.Xb = function() {
        for (; this.da.length;) {
            var a = this.da.shift();
            V(this.a, a.Sb, a.Ea)
        }
    };
    n.send = function(a, b) {
        this.Ga = !0;
        this.Da(a, b);
        this.Ga = !1
    };
    n.i = function() {
        Yc.A.i.call(this);
        this.B = this.Da = m
    };
    var W = function(a, b) {
        this.l = b || C();
        this.a = a;
        this.ba = this.a.b.ppu;
        this.Ob = this.a.b.lpu;
        this.ma = []
    },$c,ad;
    w(W, T);
    W.prototype.aa = 4;
    W.prototype.na = 0;
    W.prototype.T = !1;
    W.prototype.I = !1;
    var bd = function(a) {
        return"googlexpc_" + a.a.name + "_msg"
    },cd = function(a) {
        return"googlexpc_" + a.a.name + "_ack"
    };
    W.prototype.t = function() {
        M("transport connect called");
        if (!this.I) {
            M("initializing...");
            var a = bd(this);
            this.S = dd(this, a);
            this.Ca = this.e().frames[a];
            a = cd(this);
            this.R = dd(this, a);
            this.Ba = this.e().frames[a];
            this.I = !0
        }
        if (!ed(this, bd(this)) || !ed(this, cd(this))) {
            N("foreign frames not (yet) present");
            if (Zc(this.a) == 1 && !this.Mb)N("innerPeerReconnect called"),this.a.name = Xc(10),N("switching channels: " + this.a.name),fd(this),this.I = !1,this.Mb = dd(this, "googlexpc_reconnect_" + this.a.name); else if (Zc(this.a) ==
                    0) {
                N("outerPeerReconnect called");
                for (var a = this.a.o.frames,b = a.length,c = 0; c < b; c++) {
                    var d;
                    try {
                        if (a[c] && a[c].name)d = a[c].name
                    } catch(e) {
                    }
                    if (d) {
                        var f = d.split("_");
                        if (f.length == 3 && f[0] == "googlexpc" && f[1] == "reconnect") {
                            this.a.name = f[2];
                            fd(this);
                            this.I = !1;
                            break
                        }
                    }
                }
            }
            this.e().setTimeout(t(this.t, this), 100)
        } else M("foreign frames present"),this.Ta = new gd(this, this.a.o.frames[bd(this)], t(this.Lb, this)),this.Sa = new gd(this, this.a.o.frames[cd(this)], t(this.Kb, this)),this.Ua()
    };
    var dd = function(a, b) {
        N("constructing sender frame: " + b);
        var c = document.createElement("iframe"),d = c.style;
        d.position = "absolute";
        d.top = "-10px";
        d.left = "10px";
        d.width = "1px";
        d.height = "1px";
        c.id = c.name = b;
        c.src = a.ba + "#INITIAL";
        a.e().document.body.appendChild(c);
        return c
    },fd = function(a) {
        N("deconstructSenderFrames called");
        if (a.S)a.S.parentNode.removeChild(a.S),a.S = m,a.Ca = m;
        if (a.R)a.R.parentNode.removeChild(a.R),a.R = m,a.Ba = m
    },ed = function(a, b) {
        N("checking for receive frame: " + b);
        try {
            var c = a.a.o.frames[b];
            if (!c ||
                    c.location.href.indexOf(a.Ob) != 0)return!1
        } catch(d) {
            return!1
        }
        return!0
    };
    W.prototype.Ua = function() {
        var a = this.a.o.frames;
        if (!a[cd(this)] || !a[bd(this)]) {
            if (!this.Za)this.Za = t(this.Ua, this);
            this.e().setTimeout(this.Za, 100);
            M("local frames not (yet) present")
        } else this.Va = new hd(this.ba, this.Ca),this.ka = new hd(this.ba, this.Ba),M("local frames ready"),this.e().setTimeout(t(function() {
            this.Va.send("SETUP");
            this.T = this.nc = !0;
            M("SETUP sent")
        }, this), 100)
    };
    var id = function(a) {
        if (a.Ha && a.jb) {
            if (U(a.a),a.X) {
                M("delivering queued messages (" + a.X.length + ")");
                for (var b = 0,c; b < a.X.length; b++)c = a.X[b],V(a.a, c.Ub, c.Ea);
                delete a.X
            }
        } else N("checking if connected: ack sent:" + a.Ha + ", ack rcvd: " + a.jb)
    };
    W.prototype.Lb = function(a) {
        N("msg received: " + a);
        if (a == "SETUP") {
            if (this.ka)this.ka.send("SETUP_ACK"),N("SETUP_ACK sent"),this.Ha = !0,id(this)
        } else if (this.a.q() || this.Ha) {
            var b = a.indexOf("|"),c = a.substring(0, b),a = a.substring(b + 1),b = c.indexOf(",");
            if (b == -1) {
                var d;
                this.ka.send("ACK:" + c);
                jd(this, a)
            } else {
                d = c.substring(0, b);
                this.ka.send("ACK:" + d);
                c = c.substring(b + 1).split("/");
                b = parseInt(c[0], 10);
                c = parseInt(c[1], 10);
                if (b == 1)this.Ja = [];
                this.Ja.push(a);
                b == c && (jd(this, this.Ja.join("")),delete this.Ja)
            }
        } else L(J,
                "received msg, but channel is not connected")
    };
    W.prototype.Kb = function(a) {
        N("ack received: " + a);
        a == "SETUP_ACK" ? (this.T = !1,this.jb = !0,id(this)) : this.a.q() ? this.T ? parseInt(a.split(":")[1], 10) == this.na ? (this.T = !1,kd(this)) : L(J, "got ack with wrong sequence") : L(J, "got unexpected ack") : L(J, "received ack, but channel not connected")
    };
    var kd = function(a) {
        if (!a.T && a.ma.length) {
            var b = a.ma.shift();
            ++a.na;
            a.Va.send(a.na + b);
            N("msg sent: " + a.na + b);
            a.T = !0
        }
    },jd = function(a, b) {
        var c = b.indexOf(":"),d = b.substr(0, c),c = b.substring(c + 1);
        a.a.q() ? V(a.a, d, c) : ((a.X || (a.X = [])).push({Ub:d,Ea:c}),N("queued delivery"))
    };
    W.prototype.Aa = 3800;
    W.prototype.send = function(a, b) {
        var c = a + ":" + b;
        if (!z || b.length <= this.Aa)this.ma.push("|" + c); else for (var d = b.length,e = Math.ceil(d / this.Aa),f = 0,g = 1; f < d;)this.ma.push("," + g + "/" + e + "|" + c.substr(f, this.Aa)),g++,f += this.Aa;
        kd(this)
    };
    W.prototype.i = function() {
        W.A.i.call(this);
        var a = ld;
        Da(a, this.Ta);
        Da(a, this.Sa);
        this.Ta = this.Sa = m;
        ob(this.S);
        ob(this.R);
        this.Ca = this.Ba = this.S = this.R = m
    };
    var ld = [],md = t(function() {
        var a = !1;
        try {
            for (var b = 0,c = ld.length; b < c; b++) {
                var d;
                if (!(d = a)) {
                    var e = ld[b],f = e.ob.location.href;
                    if (f != e.nb) {
                        e.nb = f;
                        var g = f.split("#")[1];
                        g && (g = g.substr(1),e.Wb(decodeURIComponent(g)));
                        d = !0
                    } else d = !1
                }
                a = d
            }
        } catch(j) {
            if (J.info("receive_() failed: " + j),b = ld[b].k.a,J.info("Transport Error"),b.close(),!ld.length)return
        }
        b = la();
        a && ($c = b);
        ad = window.setTimeout(md, b - $c < 1E3 ? 10 : 100)
    }, W),nd = function() {
        M("starting receive-timer");
        $c = la();
        ad && window.clearTimeout(ad);
        ad = window.setTimeout(md,
                10)
    },hd = function(a, b) {
        this.ba = a;
        this.Cb = b;
        this.Qa = 0
    };
    hd.prototype.send = function(a) {
        this.Qa = ++this.Qa % 2;
        a = this.ba + "#" + this.Qa + encodeURIComponent(a);
        try {
            A ? this.Cb.location.href = a : this.Cb.location.replace(a)
        } catch(b) {
            K("sending failed", b)
        }
        nd()
    };
    var gd = function(a, b, c) {
        this.k = a;
        this.ob = b;
        this.Wb = c;
        this.nb = this.ob.location.href.split("#")[0] + "#INITIAL";
        ld.push(this);
        nd()
    };
    var X = function(a, b) {
        this.l = b || C();
        this.a = a;
        this.Nb = this.a.b.pru;
        this.$a = this.a.b.ifrid;
        A && od()
    };
    w(X, T);
    if (A)var pd = [],qd = 0,od = function() {
        qd || (qd = window.setTimeout(function() {
            rd()
        }, 1E3))
    },rd = function(a) {
        for (var b = la(),a = a || 3E3; pd.length && b - pd[0].timestamp >= a;) {
            var c = pd.shift().Vb;
            ob(c);
            N("iframe removed")
        }
        qd = window.setTimeout(sd, 1E3)
    },sd = function() {
        rd()
    };
    var td = {};
    X.prototype.aa = 3;
    X.prototype.t = function() {
        this.e().xpcRelay || (this.e().xpcRelay = ud);
        this.send("tp", "SETUP")
    };
    var ud = function(a, b) {
        var c = b.indexOf(":"),d = b.substr(0, c),e = b.substr(c + 1);
        if (!z || (c = d.indexOf("|")) == -1)var f = d; else {
            var f = d.substr(0, c),d = d.substr(c + 1),c = d.indexOf("+"),g = d.substr(0, c),c = parseInt(d.substr(c + 1), 10),j = td[g];
            j || (j = td[g] = {Hb:[],Ib:0,Gb:0});
            if (d.indexOf("++") != -1)j.Gb = c + 1;
            j.Hb[c] = e;
            j.Ib++;
            if (j.Ib != j.Gb)return;
            e = j.Hb.join("");
            delete td[g]
        }
        V(S[a], f, decodeURIComponent(e))
    };
    X.prototype.Ia = function(a) {
        a == "SETUP" ? (this.send("tp", "SETUP_ACK"),U(this.a)) : a == "SETUP_ACK" && U(this.a)
    };
    X.prototype.send = function(a, b) {
        var c = encodeURIComponent(b),d = c.length;
        if (z && d > 1800)for (var e = Math.floor(Math.random() * 2147483648).toString(36) + Math.abs(Math.floor(Math.random() * 2147483648) ^ la()).toString(36),f = 0,g = 0; f < d; g++) {
            var j = c.substr(f, 1800);
            f += 1800;
            vd(this, a, j, e + (f >= d ? "++" : "+") + g)
        } else vd(this, a, c)
    };
    var vd = function(a, b, c, d) {
        if (z) {
            var e = a.e().document.createElement("div");
            e.innerHTML = '<iframe onload="this.xpcOnload()"></iframe>';
            e = e.childNodes[0];
            e.xpcOnload = wd
        } else e = a.e().document.createElement("iframe"),A ? pd.push({timestamp:la(),Vb:e}) : Ob(e, "load", wd);
        var f = e.style;
        f.visibility = "hidden";
        f.width = e.style.height = "0px";
        f.position = "absolute";
        f = a.Nb;
        f += "#" + a.a.name;
        a.$a && (f += "," + a.$a);
        f += "|" + b;
        d && (f += "|" + d);
        f += ":" + c;
        e.src = f;
        a.e().document.body.appendChild(e);
        N("msg sent: " + f)
    },wd = function() {
        N("iframe-load");
        ob(this);
        this.tc = m
    };
    X.prototype.i = function() {
        X.A.i.call(this);
        A && rd(0)
    };
    var Y = function(a, b, c) {
        this.l = c || C();
        this.a = a;
        this.mb = b || "*"
    };
    w(Y, T);
    Y.prototype.I = !1;
    Y.prototype.aa = 1;
    var xd = {},yd = function(a) {
        var b = a.qa.data,c = b.indexOf("|"),d = b.indexOf(":");
        if (c == -1 || d == -1)return!1;
        var e = b.substring(0, c),c = b.substring(c + 1, d),b = b.substring(d + 1);
        M("messageReceived: channel=" + e + ", service=" + c + ", payload=" + b);
        if (d = S[e])return V(d, c, b, a.qa.origin),!0;
        for (var f in S)if (a = S[f],Zc(a) == 1 && !a.q() && c == "tp" && b == "SETUP")return M("changing channel name to " + e),a.name = e,delete S[f],S[e] = a,V(a, c, b),!0;
        J.info('channel name mismatch; message ignored"');
        return!1
    };
    n = Y.prototype;
    n.Ia = function(a) {
        switch (a) {
            case "SETUP":
                this.send("tp", "SETUP_ACK");
                break;
            case "SETUP_ACK":
                U(this.a)
        }
    };
    n.t = function() {
        var a = this.e(),b = ha(a),c = xd[b];
        typeof c == "number" || (c = 0);
        c == 0 && Ob(a.postMessage ? a : a.document, "message", yd, !1, Y);
        xd[b] = c + 1;
        this.I = !0;
        this.gb()
    };
    n.gb = function() {
        !this.a.q() && !this.ia && (this.send("tp", "SETUP"),this.e().setTimeout(t(this.gb, this), 100))
    };
    n.send = function(a, b) {
        var c = this.a.o;
        if (c) {
            var d = c.postMessage ? c : c.document;
            this.send = function(a, b) {
                M("send(): payload=" + b + " to hostname=" + this.mb);
                d.postMessage(this.a.name + "|" + a + ":" + b, this.mb)
            };
            this.send(a, b)
        } else M("send(): window not ready")
    };
    n.i = function() {
        Y.A.i.call(this);
        if (this.I) {
            var a = this.e(),b = ha(a),c = xd[b];
            xd[b] = c - 1;
            c == 1 && Qb(a.postMessage ? a : a.document, "message", yd, !1, Y)
        }
    };
    var zd = function(a, b) {
        this.l = b || C();
        this.a = a;
        this.Wa = a.at || "";
        this.ab = a.rat || "";
        var c = this.e();
        if (!c.nix_setup_complete)try {
            c.execScript("Class GCXPC____NIXVBS_wrapper\n Private m_Transport\nPrivate m_Auth\nPublic Sub SetTransport(transport)\nIf isEmpty(m_Transport) Then\nSet m_Transport = transport\nEnd If\nEnd Sub\nPublic Sub SetAuth(auth)\nIf isEmpty(m_Auth) Then\nm_Auth = auth\nEnd If\nEnd Sub\nPublic Function GetAuthToken()\n GetAuthToken = m_Auth\nEnd Function\nPublic Sub SendMessage(service, payload)\n Call m_Transport.GCXPC____NIXJS_handle_message(service, payload)\nEnd Sub\nPublic Sub CreateChannel(channel)\n Call m_Transport.GCXPC____NIXJS_create_channel(channel)\nEnd Sub\nPublic Sub GCXPC____NIXVBS_container()\n End Sub\nEnd Class\n Function GCXPC____NIXVBS_get_wrapper(transport, auth)\nDim wrap\nSet wrap = New GCXPC____NIXVBS_wrapper\nwrap.SetTransport transport\nwrap.SetAuth auth\nSet GCXPC____NIXVBS_get_wrapper = wrap\nEnd Function",
                    "vbscript"),c.nix_setup_complete = !0
        } catch(d) {
            K("exception caught while attempting global setup: " + d)
        }
        this.GCXPC____NIXJS_handle_message = this.Rb;
        this.GCXPC____NIXJS_create_channel = this.Qb
    };
    w(zd, T);
    n = zd.prototype;
    n.aa = 6;
    n.U = !1;
    n.initbind = m;
    n.t = function() {
        Zc(this.a) == 0 ? this.hb() : this.fb()
    };
    n.hb = function() {
        if (!this.U) {
            var a = this.a.Q;
            try {
                a.contentWindow.opener = this.e().GCXPC____NIXVBS_get_wrapper(this, this.Wa),this.U = !0
            } catch(b) {
                K("exception caught while attempting setup: " + b)
            }
            this.U || this.e().setTimeout(t(this.hb, this), 100)
        }
    };
    n.fb = function() {
        if (!this.U) {
            try {
                var a = this.e().opener;
                if (a && "GCXPC____NIXVBS_container"in a) {
                    this.initbind = a;
                    if (this.initbind.GetAuthToken() != this.ab) {
                        K("Invalid auth token from other party");
                        return
                    }
                    this.initbind.CreateChannel(this.e().GCXPC____NIXVBS_get_wrapper(this, this.Wa));
                    this.U = !0;
                    U(this.a)
                }
            } catch(b) {
                K("exception caught while attempting setup: " + b);
                return
            }
            this.U || this.e().setTimeout(t(this.fb, this), 100)
        }
    };
    n.Qb = function(a) {
        (typeof a != "unknown" || !("GCXPC____NIXVBS_container"in a)) && K("Invalid NIX channel given to createChannel_");
        this.initbind = a;
        this.initbind.GetAuthToken() != this.ab ? K("Invalid auth token from other party") : U(this.a)
    };
    n.Rb = function(a, b) {
        this.e().setTimeout(t(function() {
            V(this.a, a, b)
        }, this), 1)
    };
    n.send = function(a, b) {
        typeof this.initbind !== "unknown" && K("NIX channel not connected");
        this.initbind.SendMessage(a, b)
    };
    n.i = function() {
        zd.A.i.call(this);
        this.initbind = m
    };
    var Z = function(a, b) {
        this.ja = {};
        for (var c = 0,d; d = Vc[c]; c++)d in a && !/^https?:\/\//.test(a[d]) && h(Error("URI " + a[d] + " is invalid for field " + d));
        this.b = a;
        this.name = this.b.cn || Xc(10);
        this.l = b || C();
        a.lpu = a.lpu || Bc(this.l.e().location.href) + "/robots.txt";
        a.ppu = a.ppu || Bc(a.pu || "") + "/robots.txt";
        S[this.name] = this;
        Ob(window, "unload", Ad);
        J.info("CrossPageChannel created: " + this.name)
    };
    w(Z, yc);
    var Bd = /^%*tp$/,Cd = /^%+tp$/;
    n = Z.prototype;
    n.k = m;
    n.Pa = 1;
    n.q = function() {
        return this.Pa == 2
    };
    n.o = m;
    n.Q = m;
    var Dd = function(a) {
        var b = {};
        b.cn = a.name;
        b.tp = a.b.tp;
        a.b.lru && (b.pru = a.b.lru);
        a.b.lpu && (b.ppu = a.b.lpu);
        a.b.ppu && (b.lpu = a.b.ppu);
        return b
    },Ed = function(a) {
        var b = document.body,c = a.b.ifrid;
        c || (c = a.b.ifrid = "xpcpeer" + Xc(4));
        var d = document.createElement("IFRAME");
        d.id = d.name = c;
        d.style.width = d.style.height = "100%";
        var e = a.b.pu;
        s(e) && (e = a.b.pu = new O(e));
        Pc(e, "xpc", Yb(Dd(a)));
        Ua || A ? (a.Fa = !0,window.setTimeout(t(function() {
            this.Fa = !1;
            b.appendChild(d);
            d.src = e.toString();
            J.info("peer iframe created (" + c + ")");
            this.bb &&
            this.t(this.Xa)
        }, a), 1)) : (d.src = e.toString(),b.appendChild(d),J.info("peer iframe created (" + c + ")"))
    };
    Z.prototype.Fa = !1;
    Z.prototype.bb = !1;
    Z.prototype.t = function(a) {
        this.Xa = a || ba;
        if (this.Fa)J.info("connect() deferred"),this.bb = !0; else {
            J.info("connect()");
            if (this.b.ifrid)this.Q = s(this.b.ifrid) ? this.l.u.getElementById(this.b.ifrid) : this.b.ifrid;
            if (this.Q)(a = this.Q.contentWindow) || (a = window.frames[this.b.ifrid]),this.o = a;
            if (!this.o)window == top ? h(Error("CrossPageChannel: Can't connect, peer window-object not set.")) : this.o = window.parent;
            if (!this.k) {
                if (!this.b.tp) {
                    var a = this.b,b;
                    if (da(document.postMessage) || da(window.postMessage) || z && window.postMessage)b =
                            1; else if (Ua)b = 2; else if (z && this.b.pru)b = 3; else {
                        var c;
                        if (c = z) {
                            c = !1;
                            try {
                                b = window.opener,window.opener = {},c = qb(window, "opener"),window.opener = b
                            } catch(d) {
                            }
                        }
                        b = c ? 6 : 4
                    }
                    a.tp = b
                }
                switch (this.b.tp) {
                    case 1:
                        this.k = new Y(this, this.b.ph, this.l);
                        break;
                    case 6:
                        this.k = new zd(this, this.l);
                        break;
                    case 2:
                        this.k = new Yc(this, this.l);
                        break;
                    case 3:
                        this.k = new X(this, this.l);
                        break;
                    case 4:
                        this.k = new W(this, this.l)
                }
                this.k ? J.info("Transport created: " + this.k.getName()) : h(Error("CrossPageChannel: No suitable transport found!"))
            }
            this.k.t()
        }
    };
    Z.prototype.close = function() {
        if (this.q())this.Pa = 3,this.k.H(),this.k = m,J.info('Channel "' + this.name + '" closed')
    };
    var U = function(a) {
        if (!a.q())a.Pa = 2,J.info('Channel "' + a.name + '" connected'),a.Xa()
    };
    Z.prototype.send = function(a, b) {
        this.q() ? this.o.closed ? (K("Peer has disappeared."),this.close()) : (ea(b) && (b = Yb(b)),this.k.send(Fd(a), b)) : K("Can't send. Channel not connected.")
    };
    var V = function(a, b, c, d) {
        var e = a.b.ph;
        if (/^[\s\xa0]*$/.test(d == m ? "" : String(d)) || /^[\s\xa0]*$/.test(e == m ? "" : String(e)) || d == a.b.ph)if (a.ia)L(J, "CrossPageChannel::deliver_(): Disposed."); else if (!b || b == "tp")a.k.Ia(c); else if (a.q()) {
            if (b = b.replace(/%[0-9a-f]{2}/gi, decodeURIComponent),b = Cd.test(b) ? b.substring(1) : b,d = a.ja[b],d || (a.Ya ? (d = ka(a.Ya, b),e = ea(c),d = {kb:d,lb:e}) : (L(a.la, 'Unknown service name "' + b + '"'),d = m)),d) {
                var f;
                a:{
                    if ((e = d.lb) && s(c))try {
                        f = Vb(c);
                        break a
                    } catch(g) {
                        L(a.la, "Expected JSON payload for " +
                                b + ', was "' + c + '"');
                        f = m;
                        break a
                    } else if (!e && !s(c)) {
                        f = Yb(c);
                        break a
                    }
                    f = c
                }
                f != m && d.kb(f)
            }
        } else J.info("CrossPageChannel::deliver_(): Not connected."); else L(J, 'Message received from unapproved origin "' + d + '" - rejected.')
    },Fd = function(a) {
        Bd.test(a) && (a = "%" + a);
        return a.replace(/[%:|]/g, encodeURIComponent)
    },Zc = function(a) {
        return window.parent == a.o ? 1 : 0
    };
    Z.prototype.i = function() {
        Z.A.i.call(this);
        this.close();
        this.Q = this.o = m;
        delete S[this.name]
    };
    var Ad = function() {
        for (var a in S) {
            var b = S[a];
            b && b.H()
        }
    };
    var Gd = function(a, b) {
        z ? a.cssText = b : a[A ? "innerText" : "innerHTML"] = b
    };
    var XhrClient = function(a, b, c, d, e, f) {
        var d = new O(d || window.location.href),g = new O;
        Dc(g, e || "talkgadget.google.com");
        Fc(g, "/talkgadget/d");
        Pc(g, "token", a);
        f && Ec(g, f);
        var a = c || "wcs-iframe",c = "#" + a + " { display: none; }",j = C(i),k = m;
        if (z)k = j.u.createStyleSheet(),Gd(k, c); else {
            var l = jb(j.u, "head")[0];
            l || (k = jb(j.u, "body")[0],l = j.rb("head"),k.parentNode.insertBefore(l, k));
            k = j.rb("style");
            Gd(k, c);
            j.appendChild(l, k)
        }
        c = {};
        j = new O;
        Dc(j, e || "talkgadget.google.com");
        f && Ec(j, f);
        Fc(j, "/talkgadget/xpc_blank");
        d.n == "http" || d.n ==
                "https" ? (P(g, d.n),P(j, d.n),e = new O,P(e, d.n),Dc(e, d.J),d.G != 80 && Ec(e, d.G),Fc(e, b)) : (P(g, "http"),P(j, "http"),e = new O("http://www.google.com/xpc_blank"));
        c.lpu = e.toString();
        c.ppu = j.toString();
        c.ifrid = a;
        c.pu = g.toString();
        Z.call(this, c)
    };
    w(XhrClient, Z);
    v("chat.WcsCrossPageChannel", XhrClient);
    var Id = m,Jd = m,Kd = m;
    var Socket = function(a, b, c, d, e) {
        this.readyState = 0;
        this.Oa = [];
        this.onopen = b.onopen;
        this.onmessage = b.onmessage;
        this.onerror = b.onerror;
        this.onclose = b.onclose;
        this.N = c || new XhrClient(a, "/_ah/channel/xpc_blank");
        this.ra = c ? d : "wcs-iframe";
        this.qb = e || new Ld(a);
        document.body || h("document.body is not defined -- do not create socket from script in <head>.");
        Ed(this.N);
        zc(this.N, "opened", t(this.ac, this));
        zc(this.N, "onMessage", t(this.$b, this));
        zc(this.N, "onError", t(this.Zb, this));
        zc(this.N, "onClosed", t(this.close, this));
        this.N.t(t(function() {
        },
                this))
    };
    Socket.prototype.send = function() {
        return!1
    };
    Socket.prototype.close = function() {
        this.close()
    };
    Socket.prototype.ic = function() {
        for (var a = 0,b; b = this.Oa[a]; a++)switch (b.type) {
            case 0:
                this.onopen(b.za);
                break;
            case 1:
                this.onmessage(b.za);
                break;
            case 2:
                this.onerror(b.za);
                break;
            case 3:
                this.onclose(b.za)
        }
        this.Oa = []
    };
    var Md = function(a, b, c) {
        a.Oa.push({type:b,za:c});
        window.setTimeout(t(a.ic, a), 1)
    };
    Socket.prototype.$b = function(a) {
        for (var a = Vb(a),b = a.m,a = a.s,c = this.qb,d = [],e = 0,f = 0; f < b.length; f++) {
            for (var g = b.charCodeAt(f); g > 255;)d[e++] = g & 255,g >>= 8;
            d[e++] = g
        }
        d.push(c.sa);
        c = c.dc;
        c.reset();
        c.update(d);
        a:if (d = c.$(),!r(d) || !r(a) || d.length != a.length)a = !1; else {
            c = d.length;
            for (e = 0; e < c; e++)if (d[e] !== a[e]) {
                a = !1;
                break a
            }
            a = !0
        }
        a && Md(this, 1, {data:b});
        this.qb.sa++
    };
    Socket.prototype.Zb = function(a) {
        a = Vb(a);
        Md(this, 2, {description:a.d,code:a.c})
    };
    Socket.prototype.ac = function() {
        this.readyState = 1;
        Md(this, 0, {})
    };
    Socket.prototype.close = function() {
        this.N.close();
        this.readyState = 3;
        Md(this, 3, {});
        if (this.ra) {
            var a = new ib,b = s(this.ra) ? a.u.getElementById(this.ra) : this.ra;
            b && a.removeNode(b)
        }
    };
    var Ld = function(a) {
        for (; a.length % 4 != 0;)a += ".";
        this.sa = 0;
        try {
            if (!Id) {
                Id = {};
                Jd = {};
                Kd = {};
                for (var b = 0; b < 65; b++)Id[b] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(b),Jd[b] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.".charAt(b),Kd[Jd[b]] = b
            }
            for (var b = Kd,c = [],d = 0; d < a.length;) {
                var e = b[a.charAt(d++)],f = d < a.length ? b[a.charAt(d)] : 0;
                ++d;
                var g = d < a.length ? b[a.charAt(d)] : 0;
                ++d;
                var j = d < a.length ? b[a.charAt(d)] : 0;
                ++d;
                (e == m || f == m || g == m || j == m) && h(Error());
                c.push(e <<
                        2 | f >> 4);
                g != 64 && (c.push(f << 4 & 240 | g >> 2),j != 64 && c.push(g << 6 & 192 | j))
            }
            this.Ab = c
        } catch(k) {
            k.message ? h(Error("The provided token is invalid (" + k.name + ": " + k.message + ")")) : h(Error("The provided token is invalid."))
        }
        this.p = new SHA1;
        this.dc = new G_HMAC(this.p, this.Ab, this.Ab.length)
    };
    v("goog.appengine.Socket", Socket);
    v("goog.appengine.Socket.ReadyState", {CONNECTING:0,OPEN:1,rc:2,CLOSED:3});
    v("goog.appengine.Socket.ReadyState.CONNECTING", 0);
    v("goog.appengine.Socket.ReadyState.OPEN", 1);
    v("goog.appengine.Socket.ReadyState.CLOSING", 2);
    v("goog.appengine.Socket.ReadyState.CLOSED", 3);
    v("goog.appengine.Socket.prototype.send", Socket.prototype.send);
    v("goog.appengine.Socket.prototype.close", Socket.prototype.close);
    var Nd = function(a) {
        this.mc = a
    },Od = {onopen:function() {
    },onclose:function() {
    },onerror:function() {
    },onmessage:function() {
    }};
    Nd.prototype.open = function(a) {
        a = a || Od;
        return new Socket(this.mc, a)
    };
    v("goog.appengine.Channel", Nd);
    v("goog.appengine.Channel.prototype.open", Nd.prototype.open);
    SHA1 = function() {
        this.h = Array(5);
        this.ta = Array(64);
        this.ec = Array(80);
        this.ua = Array(64);
        this.ua[0] = 128;
        for (var a = 1; a < 64; ++a)this.ua[a] = 0;
        this.reset()
    };
    SHA1.prototype.reset = function() {
        this.h[0] = 1732584193;
        this.h[1] = 4023233417;
        this.h[2] = 2562383102;
        this.h[3] = 271733878;
        this.h[4] = 3285377520;
        this.wa = this.P = 0
    };
    var Pd = function(a, b) {
        return(a << b | a >>> 32 - b) & 4294967295
    },Qd = function(a, b) {
        for (var c = a.ec,d = 0; d < 64; d += 4)c[d / 4] = b[d] << 24 | b[d + 1] << 16 | b[d + 2] << 8 | b[d + 3];
        for (d = 16; d < 80; ++d)c[d] = Pd(c[d - 3] ^ c[d - 8] ^ c[d - 14] ^ c[d - 16], 1);
        for (var e = a.h[0],f = a.h[1],g = a.h[2],j = a.h[3],k = a.h[4],l,u,d = 0; d < 80; ++d)d < 40 ? d < 20 ? (l = j ^ f & (g ^ j),u = 1518500249) : (l = f ^ g ^ j,u = 1859775393) : d < 60 ? (l = f & g | j & (f | g),u = 2400959708) : (l = f ^ g ^ j,u = 3395469782),l = Pd(e, 5) + l + k + u + c[d] & 4294967295,k = j,j = g,g = Pd(f, 30),f = e,e = l;
        a.h[0] = a.h[0] + e & 4294967295;
        a.h[1] = a.h[1] + f & 4294967295;
        a.h[2] = a.h[2] + g & 4294967295;
        a.h[3] = a.h[3] + j & 4294967295;
        a.h[4] = a.h[4] + k & 4294967295
    };
    SHA1.prototype.update = function(a, b) {
        if (!b)b = a.length;
        var c = 0;
        if (this.P == 0)for (; c + 64 < b;)Qd(this, a.slice(c, c + 64)),c += 64,this.wa += 64;
        for (; c < b;)if (this.ta[this.P++] = a[c++],++this.wa,this.P == 64) {
            this.P = 0;
            for (Qd(this, this.ta); c + 64 < b;)Qd(this, a.slice(c, c + 64)),c += 64,this.wa += 64
        }
    };
    SHA1.prototype.$ = function() {
        var a = Array(20),b = this.wa * 8;
        this.P < 56 ? this.update(this.ua, 56 - this.P) : this.update(this.ua, 64 - (this.P - 56));
        for (var c = 63; c >= 56; --c)this.ta[c] = b & 255,b >>>= 8;
        Qd(this, this.ta);
        for (c = b = 0; c < 5; ++c)for (var d = 24; d >= 0; d -= 8)a[b++] = this.h[c] >> d & 255;
        return a
    };
    G_HMAC = function(a, b, c) {
        (!a || typeof a != "object" || !a.reset || !a.update || !a.$) && h(Error("Invalid hasher object. Hasher unspecified or does not implement expected interface."));
        b.constructor != Array && h(Error("Invalid key."));
        c && typeof c != "number" && h(Error("Invalid block size."));
        this.p = a;
        this.xa = c || 16;
        this.ub = Array(this.xa);
        this.vb = Array(this.xa);
        b.length > this.xa && (this.p.update(b),b = this.p.$());
        for (c = 0; c < this.xa; c++)a = c < b.length ? b[c] : 0,this.ub[c] = a ^ G_HMAC.cc,this.vb[c] = a ^ G_HMAC.bc
    };
    G_HMAC.cc = 92;
    G_HMAC.bc = 54;
    G_HMAC.prototype.reset = function() {
        this.p.reset();
        this.p.update(this.vb)
    };
    G_HMAC.prototype.update = function(a) {
        a.constructor != Array && h(Error("Invalid data. Data must be an array."));
        this.p.update(a)
    };
    G_HMAC.prototype.$ = function() {
        var a = this.p.$();
        this.p.reset();
        this.p.update(this.ub);
        this.p.update(a);
        return this.p.$()
    };
})()
