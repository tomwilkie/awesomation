(function() {
    function f(a) {
        throw a;
    }

    var h = void 0,m = null,n,aa = aa || {},p = this,ba = function(a) {
        for (var a = a.split("."),b = p,c; c = a.shift();)if (b[c] != m)b = b[c]; else return m;
        return b
    },ca = function() {
    },da = function(a) {
        var b = typeof a;
        if (b == "object")if (a) {
            if (a instanceof Array)return"array"; else if (a instanceof Object)return b;
            var c = Object.prototype.toString.call(a);
            if (c == "[object Window]")return"object";
            if (c == "[object Array]" || typeof a.length == "number" && typeof a.splice != "undefined" && typeof a.propertyIsEnumerable != "undefined" && !a.propertyIsEnumerable("splice"))return"array";
            if (c == "[object Function]" || typeof a.call != "undefined" && typeof a.propertyIsEnumerable != "undefined" && !a.propertyIsEnumerable("call"))return"function"
        } else return"null"; else if (b == "function" && typeof a.call == "undefined")return"object";
        return b
    },q = function(a) {
        return da(a) == "array"
    },ea = function(a) {
        var b = da(a);
        return b == "array" || b == "object" && typeof a.length == "number"
    },r = function(a) {
        return typeof a == "string"
    },fa = function(a) {
        return da(a) == "function"
    },ga = function(a) {
        a = da(a);
        return a == "object" || a == "array" ||
                a == "function"
    },s = function(a) {
        return a[ha] || (a[ha] = ++ia)
    },ha = "closure_uid_" + Math.floor(Math.random() * 2147483648).toString(36),ia = 0,ja = function(a) {
        return a.call.apply(a.bind, arguments)
    },ka = function(a, b) {
        var c = b || p;
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
                -1 ? ja : ka;
        return t.apply(m, arguments)
    },la = function(a) {
        var b = Array.prototype.slice.call(arguments, 1);
        return function() {
            var c = Array.prototype.slice.call(arguments);
            c.unshift.apply(c, b);
            return a.apply(this, c)
        }
    },do_something = Date.now || function() {
        return+new Date
    },w = function(a, b) {
        var c = a.split("."),d = p;
        !(c[0]in d) && d.execScript && d.execScript("var " + c[0]);
        for (var e; c.length && (e = c.shift());)!c.length && b !== h ? d[e] = b : d = d[e] ? d[e] : d[e] = {}
    },x = function(a, b) {
        function c() {
        }

        c.prototype = b.prototype;
        a.H = b.prototype;
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
    var ma = function(a) {
        this.stack = Error().stack || "";
        if (a)this.message = String(a)
    };
    x(ma, Error);
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
            ua = /\"/g,qa = /[&<>\"]/,wa = function(a) {
        a.length > 1024 && (a = a.substring(0, 1021) + "...");
        return a
    },xalculate_zx = function() {
        return Math.floor(Math.random() * 2147483648).toString(36) + Math.abs(Math.floor(Math.random() * 2147483648) ^ do_something()).toString(36)
    },za = function(a, b) {
        for (var c = 0,d = String(a).replace(/^[\s\xa0]+|[\s\xa0]+$/g, "").split("."),e = String(b).replace(/^[\s\xa0]+|[\s\xa0]+$/g, "").split("."),g = Math.max(d.length, e.length),i = 0; c == 0 && i < g; i++) {
            var j = d[i] || "",k = e[i] || "",l = RegExp("(\\d*)(\\D*)", "g"),o = RegExp("(\\d*)(\\D*)",
                    "g");
            do{
                var v = l.exec(j) || ["","",""],H = o.exec(k) || ["","",""];
                if (v[0].length == 0 && H[0].length == 0)break;
                c = ya(v[1].length == 0 ? 0 : parseInt(v[1], 10), H[1].length == 0 ? 0 : parseInt(H[1], 10)) || ya(v[2].length == 0, H[2].length == 0) || ya(v[2], H[2])
            } while (c == 0)
        }
        return c
    },ya = function(a, b) {
        if (a < b)return-1; else if (a > b)return 1;
        return 0
    };
    var Aa = function(a, b) {
        b.unshift(a);
        ma.call(this, na.apply(m, b));
        b.shift();
        this.Vh = a
    };
    x(Aa, ma);
    Aa.prototype.name = "AssertionError";
    var Ba = function(a, b) {
        if (!a) {
            var c = Array.prototype.slice.call(arguments, 2),d = "Assertion failed";
            if (b) {
                d += ": " + b;
                var e = c
            }
            f(new Aa("" + d, e || []))
        }
    },Ca = function(a) {
        f(new Aa("Failure" + (a ? ": " + a : ""), Array.prototype.slice.call(arguments, 1)))
    };
    var y = Array.prototype,Da = y.indexOf ? function(a, b, c) {
        Ba(a.length != m);
        return y.indexOf.call(a, b, c)
    } : function(a, b, c) {
        c = c == m ? 0 : c < 0 ? Math.max(0, a.length + c) : c;
        if (r(a)) {
            if (!r(b) || b.length != 1)return-1;
            return a.indexOf(b, c)
        }
        for (; c < a.length; c++)if (c in a && a[c] === b)return c;
        return-1
    },Ea = y.forEach ? function(a, b, c) {
        Ba(a.length != m);
        y.forEach.call(a, b, c)
    } : function(a, b, c) {
        for (var d = a.length,e = r(a) ? a.split("") : a,g = 0; g < d; g++)g in e && b.call(c, e[g], g, a)
    },Fa = function(a, b) {
        var c = Da(a, b);
        c >= 0 && (Ba(a.length != m),y.splice.call(a,
                c, 1))
    },Ga = function() {
        return y.concat.apply(y, arguments)
    },Ha = function(a) {
        if (q(a))return Ga(a); else {
            for (var b = [],c = 0,d = a.length; c < d; c++)b[c] = a[c];
            return b
        }
    },Ia = function(a) {
        for (var b = 1; b < arguments.length; b++) {
            var c = arguments[b],d;
            if (q(c) || (d = ea(c)) && c.hasOwnProperty("callee"))a.push.apply(a, c); else if (d)for (var e = a.length,g = c.length,i = 0; i < g; i++)a[e + i] = c[i]; else a.push(c)
        }
    },Ja = function(a, b, c) {
        Ba(a.length != m);
        return arguments.length <= 2 ? y.slice.call(a, b) : y.slice.call(a, b, c)
    };
    var Ka,La,Ma,Na,Oa = function() {
        return p.navigator ? p.navigator.userAgent : m
    };
    Na = Ma = La = Ka = !1;
    var Pa;
    if (Pa = Oa()) {
        var Qa = p.navigator;
        Ka = Pa.indexOf("Opera") == 0;
        La = !Ka && Pa.indexOf("MSIE") != -1;
        Ma = !Ka && Pa.indexOf("WebKit") != -1;
        Na = !Ka && !Ma && Qa.product == "Gecko"
    }
    var Ra = Ka,z = La,Sa = Na,A = Ma,Ta = p.navigator,Ua = (Ta && Ta.platform || "").indexOf("Mac") != -1,Va;
    a:{
        var Wa = "",Xa;
        if (Ra && p.opera)var Ya = p.opera.version,Wa = typeof Ya == "function" ? Ya() : Ya; else if (Sa ? Xa = /rv\:([^\);]+)(\)|;)/ : z ? Xa = /MSIE\s+([^\);]+)(\)|;)/ : A && (Xa = /WebKit\/(\S+)/),Xa)var Za = Xa.exec(Oa()),Wa = Za ? Za[1] : "";
        if (z) {
            var $a,ab = p.document;
            $a = ab ? ab.documentMode : h;
            if ($a > parseFloat(Wa)) {
                Va = String($a);
                break a
            }
        }
        Va = Wa
    }
    var bb = Va,cb = {},db = function(a) {
        return cb[a] || (cb[a] = za(bb, a) >= 0)
    };
    var eb = m,fb = m,gb = m;
    var hb = function(a, b) {
        for (var c in a)b.call(h, a[c], c, a)
    },ib = function(a) {
        var b = [],c = 0,d;
        for (d in a)b[c++] = a[d];
        return b
    },jb = function(a) {
        var b = [],c = 0,d;
        for (d in a)b[c++] = d;
        return b
    },kb = function(a, b, c) {
        b in a && f(Error('The object already contains the key "' + b + '"'));
        a[b] = c
    },lb = ["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"],mb = function(a) {
        for (var b,c,d = 1; d < arguments.length; d++) {
            c = arguments[d];
            for (b in c)a[b] = c[b];
            for (var e = 0; e < lb.length; e++)b =
                    lb[e],Object.prototype.hasOwnProperty.call(c, b) && (a[b] = c[b])
        }
    };
    var nb,ob = !z || db("9");
    !Sa && !z || z && db("9") || Sa && db("1.9.1");
    z && db("9");
    var pb = function(a) {
        var b;
        b = (b = a.className) && typeof b.split == "function" ? b.split(/\s+/) : [];
        var c = Ja(arguments, 1),d;
        d = b;
        for (var e = 0,g = 0; g < c.length; g++)Da(d, c[g]) >= 0 || (d.push(c[g]),e++);
        d = e == c.length;
        a.className = b.join(" ");
        return d
    };
    var rb = function(a) {
        return a ? new qb(a.nodeType == 9 ? a : a.ownerDocument || a.document) : nb || (nb = new qb)
    },sb = function(a, b) {
        var c = b && b != "*" ? b.toUpperCase() : "";
        if (a.querySelectorAll && a.querySelector && (!A || document.compatMode == "CSS1Compat" || db("528")) && c)return a.querySelectorAll(c + "");
        return a.getElementsByTagName(c || "*")
    },ub = function(a, b) {
        hb(b, function(b, d) {
            d == "style" ? a.style.cssText = b : d == "class" ? a.className = b : d == "for" ? a.htmlFor = b : d in tb ? a.setAttribute(tb[d], b) : a[d] = b
        })
    },tb = {cellpadding:"cellPadding",cellspacing:"cellSpacing",
        colspan:"colSpan",rowspan:"rowSpan",valign:"vAlign",height:"height",width:"width",usemap:"useMap",frameborder:"frameBorder",maxlength:"maxLength",type:"type"},wb = function(a, b, c) {
        function d(c) {
            c && b.appendChild(r(c) ? a.createTextNode(c) : c)
        }

        for (var e = 2; e < c.length; e++) {
            var g = c[e];
            ea(g) && !(ga(g) && g.nodeType > 0) ? Ea(vb(g) ? Ha(g) : g, d) : d(g)
        }
    },xb = function(a) {
        return a && a.parentNode ? a.parentNode.removeChild(a) : m
    },vb = function(a) {
        if (a && typeof a.length == "number")if (ga(a))return typeof a.item == "function" || typeof a.item ==
                "string"; else if (fa(a))return typeof a.item == "function";
        return!1
    },qb = function(a) {
        this.la = a || p.document || document
    };
    n = qb.prototype;
    n.Wf = function() {
        var a = this.la,b = arguments,c = b[0],d = b[1];
        if (!ob && d && (d.name || d.type)) {
            c = ["<",c];
            d.name && c.push(' name="', va(d.name), '"');
            if (d.type) {
                c.push(' type="', va(d.type), '"');
                var e = {};
                mb(e, d);
                d = e;
                delete d.type
            }
            c.push(">");
            c = c.join("")
        }
        c = a.createElement(c);
        if (d)r(d) ? c.className = d : q(d) ? pb.apply(m, [c].concat(d)) : ub(c, d);
        b.length > 2 && wb(a, c, b);
        return c
    };
    n.createElement = function(a) {
        return this.la.createElement(a)
    };
    n.createTextNode = function(a) {
        return this.la.createTextNode(a)
    };
    n.o = function() {
        return this.la.parentWindow || this.la.defaultView
    };
    n.appendChild = function(a, b) {
        a.appendChild(b)
    };
    n.removeNode = xb;
    var yb = function() {
    };
    yb.prototype.Pb = !1;
    yb.prototype.G = function() {
        if (!this.Pb)this.Pb = !0,this.h()
    };
    yb.prototype.h = function() {
    };
    var zb = new Function("a", "return a"),Ab = function(a, b) {
        try {
            return zb(a[b]),!0
        } catch(c) {
        }
        return!1
    };
    var Bb;
    !z || db("9");
    z && db("8");
    var B = function(a, b) {
        this.type = a;
        this.currentTarget = this.target = b
    };
    x(B, yb);
    B.prototype.h = function() {
        delete this.type;
        delete this.target;
        delete this.currentTarget
    };
    B.prototype.xb = !1;
    B.prototype.Qc = !0;
    var Cb = function(a, b) {
        a && this.Mc(a, b)
    };
    x(Cb, B);
    n = Cb.prototype;
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
    n.th = !1;
    n.Nc = m;
    n.Mc = function(a, b) {
        var c = this.type = a.type;
        B.call(this, c);
        this.target = a.target || a.srcElement;
        this.currentTarget = b;
        var d = a.relatedTarget;
        if (d)Sa && (Ab(d, "nodeName") || (d = m)); else if (c == "mouseover")d = a.fromElement; else if (c == "mouseout")d = a.toElement;
        this.relatedTarget = d;
        this.offsetX = a.offsetX !== h ? a.offsetX : a.layerX;
        this.offsetY = a.offsetY !== h ? a.offsetY : a.layerY;
        this.clientX = a.clientX !== h ? a.clientX : a.pageX;
        this.clientY = a.clientY !== h ? a.clientY : a.pageY;
        this.screenX = a.screenX || 0;
        this.screenY = a.screenY || 0;
        this.button =
                a.button;
        this.keyCode = a.keyCode || 0;
        this.charCode = a.charCode || (c == "keypress" ? a.keyCode : 0);
        this.ctrlKey = a.ctrlKey;
        this.altKey = a.altKey;
        this.shiftKey = a.shiftKey;
        this.metaKey = a.metaKey;
        this.th = Ua ? a.metaKey : a.ctrlKey;
        this.state = a.state;
        this.Nc = a;
        delete this.Qc;
        delete this.xb
    };
    n.h = function() {
        Cb.H.h.call(this);
        this.relatedTarget = this.currentTarget = this.target = this.Nc = m
    };
    var C = function(a, b) {
        this.hg = b;
        this.Xa = [];
        a > this.hg && f(Error("[goog.structs.SimplePool] Initial cannot be greater than max"));
        for (var c = 0; c < a; c++)this.Xa.push(this.dc())
    };
    x(C, yb);
    C.prototype.Ya = m;
    C.prototype.ig = m;
    C.prototype.getObject = function() {
        if (this.Xa.length)return this.Xa.pop();
        return this.dc()
    };
    var D = function(a, b) {
        a.Xa.length < a.hg ? a.Xa.push(b) : a.Gd(b)
    };
    C.prototype.dc = function() {
        return this.Ya ? this.Ya() : {}
    };
    C.prototype.Gd = function(a) {
        if (this.ig)this.ig(a); else if (ga(a))if (fa(a.G))a.G(); else for (var b in a)delete a[b]
    };
    C.prototype.h = function() {
        C.H.h.call(this);
        for (var a = this.Xa; a.length;)this.Gd(a.pop());
        delete this.Xa
    };
    var Db,Eb = (Db = "ScriptEngine"in p && p.ScriptEngine() == "JScript") ? p.ScriptEngineMajorVersion() + "." + p.ScriptEngineMinorVersion() + "." + p.ScriptEngineBuildVersion() : "0";
    var Fb = function() {
    },Gb = 0;
    n = Fb.prototype;
    n.key = 0;
    n.vb = !1;
    n.Xd = !1;
    n.Mc = function(a, b, c, d, e, g) {
        fa(a) ? this.ag = !0 : a && a.handleEvent && fa(a.handleEvent) ? this.ag = !1 : f(Error("Invalid listener argument"));
        this.fc = a;
        this.Tf = b;
        this.src = c;
        this.type = d;
        this.capture = !!e;
        this.Qd = g;
        this.Xd = !1;
        this.key = ++Gb;
        this.vb = !1
    };
    n.handleEvent = function(a) {
        if (this.ag)return this.fc.call(this.Qd || this.src, a);
        return this.fc.handleEvent.call(this.fc, a)
    };
    var Hb,Ib,Jb,Kb,Lb,Mb,Nb,Ob,Pb,Qb,Rb;
    (function() {
        function a() {
            return{i:0,ga:0}
        }

        function b() {
            return[]
        }

        function c() {
            var a = function(b) {
                return i.call(a.src, a.key, b)
            };
            return a
        }

        function d() {
            return new Fb
        }

        function e() {
            return new Cb
        }

        var g = Db && !(za(Eb, "5.7") >= 0),i;
        Mb = function(a) {
            i = a
        };
        if (g) {
            Hb = function() {
                return j.getObject()
            };
            Ib = function(a) {
                D(j, a)
            };
            Jb = function() {
                return k.getObject()
            };
            Kb = function(a) {
                D(k, a)
            };
            Lb = function() {
                return l.getObject()
            };
            Nb = function() {
                D(l, c())
            };
            Ob = function() {
                return o.getObject()
            };
            Pb = function(a) {
                D(o, a)
            };
            Qb = function() {
                return v.getObject()
            };
            Rb = function(a) {
                D(v, a)
            };
            var j = new C(0, 600);
            j.Ya = a;
            var k = new C(0, 600);
            k.Ya = b;
            var l = new C(0, 600);
            l.Ya = c;
            var o = new C(0, 600);
            o.Ya = d;
            var v = new C(0, 600);
            v.Ya = e
        } else Hb = a,Ib = ca,Jb = b,Kb = ca,Lb = c,Nb = ca,Ob = d,Pb = ca,Qb = e,Rb = ca
    })();
    var Sb = {},E = {},Tb = {},Ub = {},F = function(a, b, c, d, e) {
        if (b)if (q(b)) {
            for (var g = 0; g < b.length; g++)F(a, b[g], c, d, e);
            return m
        } else {
            var d = !!d,i = E;
            b in i || (i[b] = Hb());
            i = i[b];
            d in i || (i[d] = Hb(),i.i++);
            var i = i[d],j = s(a),k;
            i.ga++;
            if (i[j]) {
                k = i[j];
                for (g = 0; g < k.length; g++)if (i = k[g],i.fc == c && i.Qd == e) {
                    if (i.vb)break;
                    return k[g].key
                }
            } else k = i[j] = Jb(),i.i++;
            g = Lb();
            g.src = a;
            i = Ob();
            i.Mc(c, g, a, b, d, e);
            c = i.key;
            g.key = c;
            k.push(i);
            Sb[c] = i;
            Tb[j] || (Tb[j] = Jb());
            Tb[j].push(i);
            a.addEventListener ? (a == p || !a.Sf) && a.addEventListener(b, g, d) :
                    a.attachEvent(Vb(b), g);
            return c
        } else f(Error("Invalid event type"))
    },Wb = function(a, b, c, d, e) {
        if (q(b)) {
            for (var g = 0; g < b.length; g++)Wb(a, b[g], c, d, e);
            return m
        }
        a = F(a, b, c, d, e);
        Sb[a].Xd = !0;
        return a
    },Xb = function(a, b, c, d, e) {
        if (q(b))for (var g = 0; g < b.length; g++)Xb(a, b[g], c, d, e); else {
            d = !!d;
            a:{
                g = E;
                if (b in g && (g = g[b],d in g && (g = g[d],a = s(a),g[a]))) {
                    a = g[a];
                    break a
                }
                a = m
            }
            if (a)for (g = 0; g < a.length; g++)if (a[g].fc == c && a[g].capture == d && a[g].Qd == e) {
                Yb(a[g].key);
                break
            }
        }
    },Yb = function(a) {
        if (Sb[a]) {
            var b = Sb[a];
            if (!b.vb) {
                var c = b.src,
                        d = b.type,e = b.Tf,g = b.capture;
                c.removeEventListener ? (c == p || !c.Sf) && c.removeEventListener(d, e, g) : c.detachEvent && c.detachEvent(Vb(d), e);
                c = s(c);
                e = E[d][g][c];
                if (Tb[c]) {
                    var i = Tb[c];
                    Fa(i, b);
                    i.length == 0 && delete Tb[c]
                }
                b.vb = !0;
                e.Vf = !0;
                Zb(d, g, c, e);
                delete Sb[a]
            }
        }
    },Zb = function(a, b, c, d) {
        if (!d.Rc && d.Vf) {
            for (var e = 0,g = 0; e < d.length; e++)if (d[e].vb) {
                var i = d[e].Tf;
                i.src = m;
                Nb(i);
                Pb(d[e])
            } else e != g && (d[g] = d[e]),g++;
            d.length = g;
            d.Vf = !1;
            g == 0 && (Kb(d),delete E[a][b][c],E[a][b].i--,E[a][b].i == 0 && (Ib(E[a][b]),delete E[a][b],E[a].i--),
                    E[a].i == 0 && (Ib(E[a]),delete E[a]))
        }
    },$b = function(a) {
        var b,c = 0,d = b == m;
        b = !!b;
        if (a == m)hb(Tb, function(a) {
            for (var e = a.length - 1; e >= 0; e--) {
                var g = a[e];
                if (d || b == g.capture)Yb(g.key),c++
            }
        }); else if (a = s(a),Tb[a])for (var a = Tb[a],e = a.length - 1; e >= 0; e--) {
            var g = a[e];
            if (d || b == g.capture)Yb(g.key),c++
        }
    },Vb = function(a) {
        if (a in Ub)return Ub[a];
        return Ub[a] = "on" + a
    },bc = function(a, b, c, d, e) {
        var g = 1,b = s(b);
        if (a[b]) {
            a.ga--;
            a = a[b];
            a.Rc ? a.Rc++ : a.Rc = 1;
            try {
                for (var i = a.length,j = 0; j < i; j++) {
                    var k = a[j];
                    k && !k.vb && (g &= ac(k, e) !== !1)
                }
            } finally {
                a.Rc--,
                        Zb(c, d, b, a)
            }
        }
        return Boolean(g)
    },ac = function(a, b) {
        var c = a.handleEvent(b);
        a.Xd && Yb(a.key);
        return c
    };
    Mb(function(a, b) {
        if (!Sb[a])return!0;
        var c = Sb[a],d = c.type,e = E;
        if (!(d in e))return!0;
        var e = e[d],g,i;
        Bb === h && (Bb = z && !p.addEventListener);
        if (Bb) {
            g = b || ba("window.event");
            var j = !0 in e,k = !1 in e;
            if (j) {
                if (g.keyCode < 0 || g.returnValue != h)return!0;
                a:{
                    var l = !1;
                    if (g.keyCode == 0)try {
                        g.keyCode = -1;
                        break a
                    } catch(o) {
                        l = !0
                    }
                    if (l || g.returnValue == h)g.returnValue = !0
                }
            }
            l = Qb();
            l.Mc(g, this);
            g = !0;
            try {
                if (j) {
                    for (var v = Jb(),H = l.currentTarget; H; H = H.parentNode)v.push(H);
                    i = e[!0];
                    i.ga = i.i;
                    for (var K = v.length - 1; !l.xb && K >= 0 && i.ga; K--)l.currentTarget =
                            v[K],g &= bc(i, v[K], d, !0, l);
                    if (k) {
                        i = e[!1];
                        i.ga = i.i;
                        for (K = 0; !l.xb && K < v.length && i.ga; K++)l.currentTarget = v[K],g &= bc(i, v[K], d, !1, l)
                    }
                } else g = ac(c, l)
            } finally {
                if (v)v.length = 0,Kb(v);
                l.G();
                Rb(l)
            }
            return g
        }
        d = new Cb(b, this);
        try {
            g = ac(c, d)
        } finally {
            d.G()
        }
        return g
    });
    var cc = function(a) {
        var a = String(a),b;
        b = /^\s*$/.test(a) ? !1 : /^[\],:{}\s\u2028\u2029]*$/.test(a.replace(/\\["\\\/bfnrtu]/g, "@").replace(/"[^"\\\n\r\u2028\u2029\x00-\x08\x10-\x1f\x80-\x9f]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:[\s\u2028\u2029]*\[)+/g, ""));
        if (b)try {
            return eval("(" + a + ")")
        } catch(c) {
        }
        f(Error("Invalid JSON string: " + a))
    },dc = function(a) {
        return eval("(" + a + ")")
    },ec = function() {
    },gc = function(a) {
        var b = [];
        fc(new ec, a, b);
        return b.join("")
    },fc = function(a, b, c) {
        switch (typeof b) {
            case "string":
                hc(b, c);
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
                    for (var e = "",g = 0; g < d; g++)c.push(e),fc(a, b[g], c),e = ",";
                    c.push("]");
                    break
                }
                c.push("{");
                d = "";
                for (e in b)Object.prototype.hasOwnProperty.call(b, e) && (g = b[e],typeof g != "function" && (c.push(d),hc(e, c),c.push(":"),fc(a, g, c),d = ","));
                c.push("}");
                break;
            case "function":
                break;
            default:
                f(Error("Unknown type: " + typeof b))
        }
    },ic = {'"':'\\"',"\\":"\\\\","/":"\\/","\u0008":"\\b","\u000c":"\\f","\n":"\\n","\r":"\\r","\t":"\\t","\u000b":"\\u000b"},jc = /\uffff/.test("\uffff") ? /[\\\"\x00-\x1f\x7f-\uffff]/g : /[\\\"\x00-\x1f\x7f-\xff]/g,hc = function(a, b) {
        b.push('"', a.replace(jc, function(a) {
            if (a in ic)return ic[a];
            var b = a.charCodeAt(0),e = "\\u";
            b < 16 ? e += "000" : b < 256 ? e += "00" : b < 4096 && (e += "0");
            return ic[a] = e + b.toString(16)
        }), '"')
    };
    var kc = "StopIteration"in p ? p.StopIteration : Error("StopIteration"),lc = function() {
    };
    lc.prototype.next = function() {
        f(kc)
    };
    lc.prototype.$d = function() {
        return this
    };
    var mc = function(a) {
        if (a instanceof lc)return a;
        if (typeof a.$d == "function")return a.$d(!1);
        if (ea(a)) {
            var b = 0,c = new lc;
            c.next = function() {
                for (; ;)if (b >= a.length && f(kc),b in a)return a[b++]; else b++
            };
            return c
        }
        f(Error("Not implemented"))
    },nc = function(a, b) {
        if (ea(a))try {
            Ea(a, b, h)
        } catch(c) {
            c !== kc && f(c)
        } else {
            a = mc(a);
            try {
                for (; ;)b.call(h, a.next(), h, a)
            } catch(d) {
                d !== kc && f(d)
            }
        }
    };
    var oc = function(a) {
        if (typeof a.ua == "function")return a.ua();
        if (r(a))return a.split("");
        if (ea(a)) {
            for (var b = [],c = a.length,d = 0; d < c; d++)b.push(a[d]);
            return b
        }
        return ib(a)
    },pc = function(a, b, c) {
        if (typeof a.forEach == "function")a.forEach(b, c); else if (ea(a) || r(a))Ea(a, b, c); else {
            var d;
            if (typeof a.Ka == "function")d = a.Ka(); else if (typeof a.ua != "function")if (ea(a) || r(a)) {
                d = [];
                for (var e = a.length,g = 0; g < e; g++)d.push(g)
            } else d = jb(a); else d = h;
            for (var e = oc(a),g = e.length,i = 0; i < g; i++)b.call(c, e[i], d && d[i], a)
        }
    };
    var G = function(a) {
        this.ha = {};
        this.r = [];
        var b = arguments.length;
        if (b > 1) {
            b % 2 && f(Error("Uneven number of arguments"));
            for (var c = 0; c < b; c += 2)this.set(arguments[c], arguments[c + 1])
        } else if (a) {
            a instanceof G ? (b = a.Ka(),c = a.ua()) : (b = jb(a),c = ib(a));
            for (var d = 0; d < b.length; d++)this.set(b[d], c[d])
        }
    };
    n = G.prototype;
    n.i = 0;
    n.Ba = 0;
    n.Fb = function() {
        return this.i
    };
    n.ua = function() {
        qc(this);
        for (var a = [],b = 0; b < this.r.length; b++)a.push(this.ha[this.r[b]]);
        return a
    };
    n.Ka = function() {
        qc(this);
        return this.r.concat()
    };
    n.ra = function(a) {
        return rc(this.ha, a)
    };
    n.Hb = function() {
        return this.i == 0
    };
    n.clear = function() {
        this.ha = {};
        this.Ba = this.i = this.r.length = 0
    };
    n.remove = function(a) {
        if (rc(this.ha, a))return delete this.ha[a],this.i--,this.Ba++,this.r.length > 2 * this.i && qc(this),!0;
        return!1
    };
    var qc = function(a) {
        if (a.i != a.r.length) {
            for (var b = 0,c = 0; b < a.r.length;) {
                var d = a.r[b];
                rc(a.ha, d) && (a.r[c++] = d);
                b++
            }
            a.r.length = c
        }
        if (a.i != a.r.length) {
            for (var e = {},c = b = 0; b < a.r.length;)d = a.r[b],rc(e, d) || (a.r[c++] = d,e[d] = 1),b++;
            a.r.length = c
        }
    };
    G.prototype.get = function(a, b) {
        if (rc(this.ha, a))return this.ha[a];
        return b
    };
    G.prototype.set = function(a, b) {
        rc(this.ha, a) || (this.i++,this.r.push(a),this.Ba++);
        this.ha[a] = b
    };
    G.prototype.C = function() {
        return new G(this)
    };
    G.prototype.$d = function(a) {
        qc(this);
        var b = 0,c = this.r,d = this.ha,e = this.Ba,g = this,i = new lc;
        i.next = function() {
            for (; ;) {
                e != g.Ba && f(Error("The map has changed since the iterator was created"));
                b >= c.length && f(kc);
                var i = c[b++];
                return a ? i : d[i]
            }
        };
        return i
    };
    var rc = function(a, b) {
        return Object.prototype.hasOwnProperty.call(a, b)
    };
    var sc = function(a) {
        var b = p.onerror;
        p.onerror = function(c, d, e) {
            b && b(c, d, e);
            a({message:c,fileName:d,dg:e});
            return Boolean(h)
        }
    },tc = function(a) {
        var b = ba("window.location.href");
        if (r(a))return{message:a,name:"Unknown error",lineNumber:"Not available",fileName:b,stack:"Not available"};
        var c,d,e = !1;
        try {
            c = a.lineNumber || a.dg || "Not available"
        } catch(g) {
            c = "Not available",e = !0
        }
        try {
            d = a.fileName || a.filename || a.sourceURL || b
        } catch(i) {
            d = "Not available",e = !0
        }
        if (e || !a.lineNumber || !a.fileName || !a.stack)return{message:a.message,
            name:a.name,lineNumber:c,fileName:d,stack:a.stack || "Not available"};
        return a
    },vc = function(a) {
        return uc(a || arguments.callee.caller, [])
    },uc = function(a, b) {
        var c = [];
        if (Da(b, a) >= 0)c.push("[...circular reference...]"); else if (a && b.length < 50) {
            c.push(wc(a) + "(");
            for (var d = a.arguments,e = 0; e < d.length; e++) {
                e > 0 && c.push(", ");
                var g;
                g = d[e];
                switch (typeof g) {
                    case "object":
                        g = g ? "object" : "null";
                        break;
                    case "string":
                        break;
                    case "number":
                        g = String(g);
                        break;
                    case "boolean":
                        g = g ? "true" : "false";
                        break;
                    case "function":
                        g = (g = wc(g)) ?
                                g : "[fn]";
                        break;
                    default:
                        g = typeof g
                }
                g.length > 40 && (g = g.substr(0, 40) + "...");
                c.push(g)
            }
            b.push(a);
            c.push(")\n");
            try {
                c.push(uc(a.caller, b))
            } catch(i) {
                c.push("[exception trying to get caller]\n")
            }
        } else a ? c.push("[...long stack...]") : c.push("[end]");
        return c.join("")
    },wc = function(a) {
        a = String(a);
        if (!xc[a]) {
            var b = /function ([^\(]+)/.exec(a);
            xc[a] = b ? b[1] : "[Anonymous]"
        }
        return xc[a]
    },xc = {};
    var yc = function(a, b, c, d, e) {
        this.reset(a, b, c, d, e)
    };
    yc.prototype.cc = 0;
    yc.prototype.cg = m;
    yc.prototype.bg = m;
    var zc = 0;
    yc.prototype.reset = function(a, b, c, d, e) {
        this.cc = typeof e == "number" ? e : zc++;
        this.Ih = d || do_something();
        this.ic = a;
        this.mh = b;
        this.Hh = c;
        delete this.cg;
        delete this.bg
    };
    yc.prototype.qg = function(a) {
        this.ic = a
    };
    var I = function(a) {
        this.ng = a
    };
    I.prototype.Wc = m;
    I.prototype.ic = m;
    I.prototype.Zd = m;
    I.prototype.kg = m;
    var Ac = function(a, b) {
        this.name = a;
        this.value = b
    };
    Ac.prototype.toString = function() {
        return this.name
    };
    var Bc = new Ac("SEVERE", 1E3),Cc = new Ac("WARNING", 900),Dc = new Ac("INFO", 800),Ec = new Ac("CONFIG", 700),Fc = new Ac("FINE", 500),Gc = new Ac("FINEST", 300);
    I.prototype.getName = function() {
        return this.ng
    };
    I.prototype.getParent = function() {
        return this.Wc
    };
    I.prototype.qg = function(a) {
        this.ic = a
    };
    var Hc = function(a) {
        if (a.ic)return a.ic;
        if (a.Wc)return Hc(a.Wc);
        Ca("Root logger has no level set.");
        return m
    };
    n = I.prototype;
    n.log = function(a, b, c) {
        if (a.value >= Hc(this).value) {
            a = this.uh(a, b, c);
            this.uc("log:" + a.mh);
            for (b = this; b;) {
                var c = b,d = a;
                if (c.kg)for (var e = 0,g = h; g = c.kg[e]; e++)g(d);
                b = b.getParent()
            }
        }
    };
    n.uh = function(a, b, c) {
        var d = new yc(a, String(b), this.ng);
        if (c) {
            d.cg = c;
            var e;
            var g = arguments.callee.caller;
            try {
                var i = tc(c);
                e = "Message: " + va(i.message) + '\nUrl: <a href="view-source:' + i.fileName + '" target="_new">' + i.fileName + "</a>\nLine: " + i.lineNumber + "\n\nBrowser stack:\n" + va(i.stack + "-> ") + "[end]\n\nJS stack traversal:\n" + va(vc(g) + "-> ")
            } catch(j) {
                e = "Exception trying to expose exception! You win, we lose. " + j
            }
            d.bg = e
        }
        return d
    };
    n.k = function(a, b) {
        this.log(Bc, a, b)
    };
    n.v = function(a, b) {
        this.log(Cc, a, b)
    };
    n.info = function(a, b) {
        this.log(Dc, a, b)
    };
    var J = function(a, b) {
        a.log(Fc, b, h)
    },L = function(a, b) {
        a.log(Gc, b, h)
    };
    I.prototype.uc = function(a) {
        p.console && p.console.markTimeline && p.console.markTimeline(a)
    };
    var Ic = {},Jc = m,Kc = function() {
        Jc || (Jc = new I(""),Ic[""] = Jc,Jc.qg(Ec))
    },Lc = function() {
        Kc();
        return Jc
    },M = function(a) {
        Kc();
        var b;
        if (!(b = Ic[a])) {
            b = new I(a);
            var c = a.lastIndexOf("."),d = a.substr(c + 1),c = M(a.substr(0, c));
            if (!c.Zd)c.Zd = {};
            c.Zd[d] = b;
            b.Wc = c;
            Ic[a] = b
        }
        return b
    },Mc = function(a) {
        return function(b) {
            (a || Lc()).k("Error: " + b.message + " (" + b.fileName + " @ Line: " + b.dg + ")")
        }
    };
    var Nc = function() {
        this.Bc = {}
    };
    x(Nc, yb);
    Nc.prototype.Fc = M("goog.messaging.AbstractChannel");
    Nc.prototype.initbind = function(a) {
        a && a()
    };
    Nc.prototype.Y = function() {
        return!0
    };
    var Oc = function(a, b, c) {
        a.Bc[b] = {Of:c,Pf:!1}
    };
    Nc.prototype.h = function() {
        Nc.H.h.call(this);
        var a = this.Fc;
        a && typeof a.G == "function" && a.G();
        delete this.Fc;
        delete this.Bc;
        delete this.tf
    };
    var Pc = RegExp("^(?:([^:/?#.]+):)?(?://(?:([^/?#]*)@)?([\\w\\d\\-\\u0100-\\uffff.%]*)(?::([0-9]+))?)?([^?#]+)?(?:\\?([^#]*))?(?:#(.*))?$"),Qc = function(a) {
        var b = a.match(Pc),a = b[1],c = b[2],d = b[3],b = b[4],e = [];
        a && e.push(a, ":");
        d && (e.push("//"),c && e.push(c, "@"),e.push(d),b && e.push(":", b));
        return e.join("")
    };
    var N = function(a, b) {
        var c;
        a instanceof N ? (this.tb(b == m ? a.ka : b),Rc(this, a.K),Sc(this, a.Na),Tc(this, a.ia),Uc(this, a.ja),Vc(this, a.z),Wc(this, a.J.C()),Xc(this, a.Ma)) : a && (c = String(a).match(Pc)) ? (this.tb(!!b),Rc(this, c[1] || "", !0),Sc(this, c[2] || "", !0),Tc(this, c[3] || "", !0),Uc(this, c[4]),Vc(this, c[5] || "", !0),this.Cb(c[6] || "", !0),Xc(this, c[7] || "", !0)) : (this.tb(!!b),this.J = new Yc(m, this, this.ka))
    };
    n = N.prototype;
    n.K = "";
    n.Na = "";
    n.ia = "";
    n.ja = m;
    n.z = "";
    n.Ma = "";
    n.yh = !1;
    n.ka = !1;
    n.toString = function() {
        if (this.aa)return this.aa;
        var a = [];
        this.K && a.push(Zc(this.K, $c), ":");
        if (this.ia) {
            a.push("//");
            this.Na && a.push(Zc(this.Na, $c), "@");
            var b;
            b = this.ia;
            b = r(b) ? encodeURIComponent(b) : m;
            a.push(b);
            this.ja != m && a.push(":", String(this.ja))
        }
        this.z && (this.ia && this.z.charAt(0) != "/" && a.push("/"),a.push(Zc(this.z, this.z.charAt(0) == "/" ? ad : bd)));
        (b = String(this.J)) && a.push("?", b);
        this.Ma && a.push("#", Zc(this.Ma, cd));
        return this.aa = a.join("")
    };
    n.C = function() {
        return dd(this.K, this.Na, this.ia, this.ja, this.z, this.J.C(), this.Ma, this.ka)
    };
    var Rc = function(a, b, c) {
        ed(a);
        delete a.aa;
        a.K = c ? b ? decodeURIComponent(b) : "" : b;
        if (a.K)a.K = a.K.replace(/:$/, "")
    },Sc = function(a, b, c) {
        ed(a);
        delete a.aa;
        a.Na = c ? b ? decodeURIComponent(b) : "" : b
    },Tc = function(a, b, c) {
        ed(a);
        delete a.aa;
        a.ia = c ? b ? decodeURIComponent(b) : "" : b
    },Uc = function(a, b) {
        ed(a);
        delete a.aa;
        b ? (b = Number(b),(isNaN(b) || b < 0) && f(Error("Bad port number " + b)),a.ja = b) : a.ja = m
    },Vc = function(a, b, c) {
        ed(a);
        delete a.aa;
        a.z = c ? b ? decodeURIComponent(b) : "" : b
    },Wc = function(a, b, c) {
        ed(a);
        delete a.aa;
        b instanceof Yc ? (a.J =
                b,a.J.Sd = a,a.J.tb(a.ka)) : (c || (b = Zc(b, fd)),a.J = new Yc(b, a, a.ka));
        return a
    };
    N.prototype.Cb = function(a, b) {
        return Wc(this, a, b)
    };
    var gd = function(a) {
        a = a.J;
        if (!a.wb)a.wb = a.toString() ? decodeURIComponent(a.toString()) : "";
        return a.wb
    };
    N.prototype.xd = function() {
        return this.J.toString()
    };
    var add_param = function(a, b, c) {
        ed(a);
        delete a.aa;
        a.J.set(b, c)
    },jd = function(a, b, c) {
        ed(a);
        delete a.aa;
        q(c) || (c = [String(c)]);
        a = a.J;
        P(a);
        hd(a);
        b = id(a, b);
        if (a.ra(b)) {
            var d = a.q.get(b);
            q(d) ? a.i -= d.length : a.i--
        }
        c.length > 0 && (a.q.set(b, c),a.i += c.length)
    },Xc = function(a, b, c) {
        ed(a);
        delete a.aa;
        a.Ma = c ? b ? decodeURIComponent(b) : "" : b
    },add_zx_parameter = function(a) {
        ed(a);
        add_param(a, "zx", xalculate_zx());
        return a
    },ed = function(a) {
        a.yh && f(Error("Tried to modify a read-only Uri"))
    };
    N.prototype.tb = function(a) {
        this.ka = a;
        this.J && this.J.tb(a);
        return this
    };
    var ld = function(a) {
        return a instanceof N ? a.C() : new N(a, h)
    },dd = function(a, b, c, d, e, g, i, j) {
        j = new N(m, j);
        a && Rc(j, a);
        b && Sc(j, b);
        c && Tc(j, c);
        d && Uc(j, d);
        e && Vc(j, e);
        g && Wc(j, g);
        i && Xc(j, i);
        return j
    },md = /^[a-zA-Z0-9\-_.!~*'():\/;?]*$/,Zc = function(a, b) {
        var c = m;
        r(a) && (c = a,md.test(c) || (c = encodeURI(a)),c.search(b) >= 0 && (c = c.replace(b, nd)));
        return c
    },nd = function(a) {
        a = a.charCodeAt(0);
        return"%" + (a >> 4 & 15).toString(16) + (a & 15).toString(16)
    },$c = /[#\/\?@]/g,bd = /[\#\?:]/g,ad = /[\#\?]/g,fd = /[\#\?@]/g,cd = /#/g,Yc = function(a, b, c) {
        this.va = a || m;
        this.Sd = b || m;
        this.ka = !!c
    },P = function(a) {
        if (!a.q && (a.q = new G,a.va))for (var b = a.va.split("&"),c = 0; c < b.length; c++) {
            var d = b[c].indexOf("="),e = m,g = m;
            d >= 0 ? (e = b[c].substring(0, d),g = b[c].substring(d + 1)) : e = b[c];
            e = decodeURIComponent(e.replace(/\+/g, " "));
            e = id(a, e);
            a.add(e, g ? decodeURIComponent(g.replace(/\+/g, " ")) : "")
        }
    };
    n = Yc.prototype;
    n.q = m;
    n.i = m;
    n.Fb = function() {
        P(this);
        return this.i
    };
    n.add = function(a, b) {
        P(this);
        hd(this);
        a = id(this, a);
        if (this.ra(a)) {
            var c = this.q.get(a);
            q(c) ? c.push(b) : this.q.set(a, [c,b])
        } else this.q.set(a, b);
        this.i++;
        return this
    };
    n.remove = function(a) {
        P(this);
        a = id(this, a);
        if (this.q.ra(a)) {
            hd(this);
            var b = this.q.get(a);
            q(b) ? this.i -= b.length : this.i--;
            return this.q.remove(a)
        }
        return!1
    };
    n.clear = function() {
        hd(this);
        this.q && this.q.clear();
        this.i = 0
    };
    n.Hb = function() {
        P(this);
        return this.i == 0
    };
    n.ra = function(a) {
        P(this);
        a = id(this, a);
        return this.q.ra(a)
    };
    n.Ka = function() {
        P(this);
        for (var a = this.q.ua(),b = this.q.Ka(),c = [],d = 0; d < b.length; d++) {
            var e = a[d];
            if (q(e))for (var g = 0; g < e.length; g++)c.push(b[d]); else c.push(b[d])
        }
        return c
    };
    n.ua = function(a) {
        P(this);
        if (a)if (a = id(this, a),this.ra(a)) {
            var b = this.q.get(a);
            if (q(b))return b; else a = [],a.push(b)
        } else a = []; else for (var b = this.q.ua(),a = [],c = 0; c < b.length; c++) {
            var d = b[c];
            q(d) ? Ia(a, d) : a.push(d)
        }
        return a
    };
    n.set = function(a, b) {
        P(this);
        hd(this);
        a = id(this, a);
        if (this.ra(a)) {
            var c = this.q.get(a);
            q(c) ? this.i -= c.length : this.i--
        }
        this.q.set(a, b);
        this.i++;
        return this
    };
    n.get = function(a, b) {
        P(this);
        a = id(this, a);
        if (this.ra(a)) {
            var c = this.q.get(a);
            return q(c) ? c[0] : c
        } else return b
    };
    n.toString = function() {
        if (this.va)return this.va;
        if (!this.q)return"";
        for (var a = [],b = 0,c = this.q.Ka(),d = 0; d < c.length; d++) {
            var e = c[d],g = pa(e),e = this.q.get(e);
            if (q(e))for (var i = 0; i < e.length; i++)b > 0 && a.push("&"),a.push(g),e[i] !== "" && a.push("=", pa(e[i])),b++; else b > 0 && a.push("&"),a.push(g),e !== "" && a.push("=", pa(e)),b++
        }
        return this.va = a.join("")
    };
    var hd = function(a) {
        delete a.wb;
        delete a.va;
        a.Sd && delete a.Sd.aa
    };
    Yc.prototype.C = function() {
        var a = new Yc;
        if (this.wb)a.wb = this.wb;
        if (this.va)a.va = this.va;
        if (this.q)a.q = this.q.C();
        return a
    };
    var id = function(a, b) {
        var c = String(b);
        a.ka && (c = c.toLowerCase());
        return c
    };
    Yc.prototype.tb = function(a) {
        a && !this.ka && (P(this),hd(this),pc(this.q, function(a, c) {
            var d = c.toLowerCase();
            c != d && (this.remove(c),this.add(d, a))
        }, this));
        this.ka = a
    };
    var od = {1:"NativeMessagingTransport",2:"FrameElementMethodTransport",3:"IframeRelayTransport",4:"IframePollingTransport",5:"FlashTransport",6:"NixTransport"},pd = ["pu","lru","pru","lpu","ppu"],qd = {},sd = function(a) {
        for (var b = rd,c = b.length,d = ""; a-- > 0;)d += b.charAt(Math.floor(Math.random() * c));
        return d
    },rd = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",Q = M("goog.net.xpc");
    var td = function(a) {
        this.R = a || rb()
    };
    x(td, yb);
    td.prototype.$a = 0;
    td.prototype.fg = function() {
        return this.$a
    };
    td.prototype.o = function() {
        return this.R.o()
    };
    td.prototype.getName = function() {
        return od[this.$a] || ""
    };
    var ud = function(a, b) {
        this.R = b || rb();
        this.b = a;
        this.Yb = [];
        this.Tg = t(this.eh, this)
    };
    x(ud, td);
    n = ud.prototype;
    n.$a = 2;
    n.Id = !1;
    n.fa = 0;
    n.initbind = function() {
        vd(this.b) == 0 ? (this.sa = this.b.kb,this.sa.XPC_toOuter = t(this.uf, this)) : this.sf()
    };
    n.sf = function() {
        var a = !0;
        try {
            if (!this.sa)this.sa = this.o().frameElement;
            if (this.sa && this.sa.XPC_toOuter)this.zd = this.sa.XPC_toOuter,this.sa.XPC_toOuter.XPC_toInner = t(this.uf, this),a = !1,this.send("tp", "SETUP_ACK"),wd(this.b)
        } catch(b) {
            Q.k("exception caught while attempting setup: " + b)
        }
        if (a) {
            if (!this.Af)this.Af = t(this.sf, this);
            this.o().setTimeout(this.Af, 100)
        }
    };
    n.Od = function(a) {
        vd(this.b) == 0 && !this.b.Y() && a == "SETUP_ACK" ? (this.zd = this.sa.XPC_toOuter.XPC_toInner,wd(this.b)) : f(Error("Got unexpected transport message."))
    };
    n.uf = function(a, b) {
        if (!this.Id && this.Yb.length == 0)xd(this.b, a, b); else if (this.Yb.push({Wg:a,Fd:b}),this.Yb.length == 1)this.fa = this.o().setTimeout(this.Tg, 1)
    };
    n.eh = function() {
        for (; this.Yb.length;) {
            var a = this.Yb.shift();
            xd(this.b, a.Wg, a.Fd)
        }
    };
    n.send = function(a, b) {
        this.Id = !0;
        this.zd(a, b);
        this.Id = !1
    };
    n.h = function() {
        ud.H.h.call(this);
        this.sa = this.zd = m
    };
    var R = function(a, b) {
        this.R = b || rb();
        this.b = a;
        this.Tb = this.b.n.ppu;
        this.Vg = this.b.n.lpu;
        this.Gc = []
    },yd,zd;
    x(R, td);
    R.prototype.$a = 4;
    R.prototype.Hc = 0;
    R.prototype.ob = !1;
    R.prototype.W = !1;
    var Ad = function(a) {
        return"googlexpc_" + a.b.name + "_msg"
    },Bd = function(a) {
        return"googlexpc_" + a.b.name + "_ack"
    };
    R.prototype.initbind = function() {
        J(Q, "transport connect called");
        if (!this.W) {
            J(Q, "initializing...");
            var a = Ad(this);
            this.nb = Cd(this, a);
            this.ud = this.o().frames[a];
            a = Bd(this);
            this.mb = Cd(this, a);
            this.td = this.o().frames[a];
            this.W = !0
        }
        if (!Dd(this, Ad(this)) || !Dd(this, Bd(this))) {
            L(Q, "foreign frames not (yet) present");
            if (vd(this.b) == 1 && !this.Pg)L(Q, "innerPeerReconnect called"),this.b.name = sd(10),L(Q, "switching channels: " + this.b.name),Ed(this),this.W = !1,this.Pg = Cd(this, "googlexpc_reconnect_" + this.b.name); else if (vd(this.b) ==
                    0) {
                L(Q, "outerPeerReconnect called");
                for (var a = this.b.Z.frames,b = a.length,c = 0; c < b; c++) {
                    var d;
                    try {
                        if (a[c] && a[c].name)d = a[c].name
                    } catch(e) {
                    }
                    if (d) {
                        var g = d.split("_");
                        if (g.length == 3 && g[0] == "googlexpc" && g[1] == "reconnect") {
                            this.b.name = g[2];
                            Ed(this);
                            this.W = !1;
                            break
                        }
                    }
                }
            }
            this.o().setTimeout(t(this.initbind, this), 100)
        } else J(Q, "foreign frames present"),this.Te = new Fd(this, this.b.Z.frames[Ad(this)], t(this.Og, this)),this.Se = new Fd(this, this.b.Z.frames[Bd(this)], t(this.Ng, this)),this.cf()
    };
    var Cd = function(a, b) {
        L(Q, "constructing sender frame: " + b);
        var c = document.createElement("iframe"),d = c.style;
        d.position = "absolute";
        d.top = "-10px";
        d.left = "10px";
        d.width = "1px";
        d.height = "1px";
        c.id = c.name = b;
        c.src = a.Tb + "#INITIAL";
        a.o().document.body.appendChild(c);
        return c
    },Ed = function(a) {
        L(Q, "deconstructSenderFrames called");
        if (a.nb)a.nb.parentNode.removeChild(a.nb),a.nb = m,a.ud = m;
        if (a.mb)a.mb.parentNode.removeChild(a.mb),a.mb = m,a.td = m
    },Dd = function(a, b) {
        L(Q, "checking for receive frame: " + b);
        try {
            var c = a.b.Z.frames[b];
            if (!c || c.location.href.indexOf(a.Vg) != 0)return!1
        } catch(d) {
            return!1
        }
        return!0
    };
    R.prototype.cf = function() {
        var a = this.b.Z.frames;
        if (!a[Bd(this)] || !a[Ad(this)]) {
            if (!this.zf)this.zf = t(this.cf, this);
            this.o().setTimeout(this.zf, 100);
            J(Q, "local frames not (yet) present")
        } else this.rf = new Gd(this.Tb, this.ud),this.Dc = new Gd(this.Tb, this.td),J(Q, "local frames ready"),this.o().setTimeout(t(function() {
            this.rf.send("SETUP");
            this.ob = this.Gh = !0;
            J(Q, "SETUP sent")
        }, this), 100)
    };
    var Hd = function(a) {
        if (a.Hd && a.Df) {
            if (wd(a.b),a.ub) {
                J(Q, "delivering queued messages (" + a.ub.length + ")");
                for (var b = 0,c; b < a.ub.length; b++)c = a.ub[b],xd(a.b, c.ah, c.Fd);
                delete a.ub
            }
        } else L(Q, "checking if connected: ack sent:" + a.Hd + ", ack rcvd: " + a.Df)
    };
    R.prototype.Og = function(a) {
        L(Q, "msg received: " + a);
        if (a == "SETUP") {
            if (this.Dc)this.Dc.send("SETUP_ACK"),L(Q, "SETUP_ACK sent"),this.Hd = !0,Hd(this)
        } else if (this.b.Y() || this.Hd) {
            var b = a.indexOf("|"),c = a.substring(0, b),a = a.substring(b + 1),b = c.indexOf(",");
            if (b == -1) {
                var d;
                this.Dc.send("ACK:" + c);
                Id(this, a)
            } else {
                d = c.substring(0, b);
                this.Dc.send("ACK:" + d);
                c = c.substring(b + 1).split("/");
                b = parseInt(c[0], 10);
                c = parseInt(c[1], 10);
                if (b == 1)this.Kd = [];
                this.Kd.push(a);
                b == c && (Id(this, this.Kd.join("")),delete this.Kd)
            }
        } else Q.v("received msg, but channel is not connected")
    };
    R.prototype.Ng = function(a) {
        L(Q, "ack received: " + a);
        a == "SETUP_ACK" ? (this.ob = !1,this.Df = !0,Hd(this)) : this.b.Y() ? this.ob ? parseInt(a.split(":")[1], 10) == this.Hc ? (this.ob = !1,Jd(this)) : Q.v("got ack with wrong sequence") : Q.v("got unexpected ack") : Q.v("received ack, but channel not connected")
    };
    var Jd = function(a) {
        if (!a.ob && a.Gc.length) {
            var b = a.Gc.shift();
            ++a.Hc;
            a.rf.send(a.Hc + b);
            L(Q, "msg sent: " + a.Hc + b);
            a.ob = !0
        }
    },Id = function(a, b) {
        var c = b.indexOf(":"),d = b.substr(0, c),c = b.substring(c + 1);
        a.b.Y() ? xd(a.b, d, c) : ((a.ub || (a.ub = [])).push({ah:d,Fd:c}),L(Q, "queued delivery"))
    };
    R.prototype.Yc = 3800;
    R.prototype.send = function(a, b) {
        var c = a + ":" + b;
        if (!z || b.length <= this.Yc)this.Gc.push("|" + c); else for (var d = b.length,e = Math.ceil(d / this.Yc),g = 0,i = 1; g < d;)this.Gc.push("," + i + "/" + e + "|" + c.substr(g, this.Yc)),i++,g += this.Yc;
        Jd(this)
    };
    R.prototype.h = function() {
        R.H.h.call(this);
        var a = Kd;
        Fa(a, this.Te);
        Fa(a, this.Se);
        this.Te = this.Se = m;
        xb(this.nb);
        xb(this.mb);
        this.ud = this.td = this.nb = this.mb = m
    };
    var Kd = [],Ld = t(function() {
        var a = !1;
        try {
            for (var b = 0,c = Kd.length; b < c; b++) {
                var d;
                if (!(d = a)) {
                    var e = Kd[b],g = e.Mf.location.href;
                    if (g != e.Lf) {
                        e.Lf = g;
                        var i = g.split("#")[1];
                        i && (i = i.substr(1),e.dh(decodeURIComponent(i)));
                        d = !0
                    } else d = !1
                }
                a = d
            }
        } catch(j) {
            if (Q.info("receive_() failed: " + j),b = Kd[b].M.b,Q.info("Transport Error"),b.close(),!Kd.length)return
        }
        b = do_something();
        a && (yd = b);
        zd = window.setTimeout(Ld, b - yd < 1E3 ? 10 : 100)
    }, R),Md = function() {
        J(Q, "starting receive-timer");
        yd = do_something();
        zd && window.clearTimeout(zd);
        zd = window.setTimeout(Ld,
                10)
    },Gd = function(a, b) {
        this.Tb = a;
        this.Xf = b;
        this.Wd = 0
    };
    Gd.prototype.send = function(a) {
        this.Wd = ++this.Wd % 2;
        a = this.Tb + "#" + this.Wd + encodeURIComponent(a);
        try {
            A ? this.Xf.location.href = a : this.Xf.location.replace(a)
        } catch(b) {
            Q.k("sending failed", b)
        }
        Md()
    };
    var Fd = function(a, b, c) {
        this.M = a;
        this.Mf = b;
        this.dh = c;
        this.Lf = this.Mf.location.href.split("#")[0] + "#INITIAL";
        Kd.push(this);
        Md()
    };
    var Od = function(a, b) {
        this.R = b || rb();
        this.b = a;
        this.Sg = this.b.n.pru;
        this.Bf = this.b.n.ifrid;
        A && Nd()
    };
    x(Od, td);
    if (A)var Pd = [],Qd = 0,Nd = function() {
        Qd || (Qd = window.setTimeout(function() {
            Rd()
        }, 1E3))
    },Rd = function(a) {
        for (var b = do_something(),a = a || 3E3; Pd.length && b - Pd[0].timestamp >= a;) {
            var c = Pd.shift().bh;
            xb(c);
            L(Q, "iframe removed")
        }
        Qd = window.setTimeout(Sd, 1E3)
    },Sd = function() {
        Rd()
    };
    var Td = {};
    Od.prototype.$a = 3;
    Od.prototype.initbind = function() {
        this.o().xpcRelay || (this.o().xpcRelay = Ud);
        this.send("tp", "SETUP")
    };
    var Ud = function(a, b) {
        var c = b.indexOf(":"),d = b.substr(0, c),e = b.substr(c + 1);
        if (!z || (c = d.indexOf("|")) == -1)var g = d; else {
            var g = d.substr(0, c),d = d.substr(c + 1),c = d.indexOf("+"),i = d.substr(0, c),c = parseInt(d.substr(c + 1), 10),j = Td[i];
            j || (j = Td[i] = {mg:[],og:0,lg:0});
            if (d.indexOf("++") != -1)j.lg = c + 1;
            j.mg[c] = e;
            j.og++;
            if (j.og != j.lg)return;
            e = j.mg.join("");
            delete Td[i]
        }
        xd(qd[a], g, decodeURIComponent(e))
    };
    Od.prototype.Od = function(a) {
        a == "SETUP" ? (this.send("tp", "SETUP_ACK"),wd(this.b)) : a == "SETUP_ACK" && wd(this.b)
    };
    Od.prototype.send = function(a, b) {
        var c = encodeURIComponent(b),d = c.length;
        if (z && d > 1800)for (var e = xalculate_zx(),g = 0,i = 0; g < d; i++) {
            var j = c.substr(g, 1800);
            g += 1800;
            Vd(this, a, j, e + (g >= d ? "++" : "+") + i)
        } else Vd(this, a, c)
    };
    var Vd = function(a, b, c, d) {
        if (z) {
            var e = a.o().document.createElement("div");
            e.innerHTML = '<iframe onload="this.xpcOnload()"></iframe>';
            e = e.childNodes[0];
            e.xpcOnload = Wd
        } else e = a.o().document.createElement("iframe"),A ? Pd.push({timestamp:do_something(),bh:e}) : F(e, "load", Wd);
        var g = e.style;
        g.visibility = "hidden";
        g.width = e.style.height = "0px";
        g.position = "absolute";
        g = a.Sg;
        g += "#" + a.b.name;
        a.Bf && (g += "," + a.Bf);
        g += "|" + b;
        d && (g += "|" + d);
        g += ":" + c;
        e.src = g;
        a.o().document.body.appendChild(e);
        L(Q, "msg sent: " + g)
    },Wd = function() {
        L(Q,
                "iframe-load");
        xb(this);
        this.Zh = m
    };
    Od.prototype.h = function() {
        Od.H.h.call(this);
        A && Rd(0)
    };
    var Xd = function(a, b, c) {
        this.R = c || rb();
        this.b = a;
        this.Kf = b || "*"
    };
    x(Xd, td);
    Xd.prototype.W = !1;
    Xd.prototype.$a = 1;
    var Yd = {},Zd = function(a) {
        var b = a.Nc.data,c = b.indexOf("|"),d = b.indexOf(":");
        if (c == -1 || d == -1)return!1;
        var e = b.substring(0, c),c = b.substring(c + 1, d),b = b.substring(d + 1);
        J(Q, "messageReceived: channel=" + e + ", service=" + c + ", payload=" + b);
        if (d = qd[e])return xd(d, c, b, a.Nc.origin),!0;
        for (var g in qd)if (a = qd[g],vd(a) == 1 && !a.Y() && c == "tp" && b == "SETUP")return J(Q, "changing channel name to " + e),a.name = e,delete qd[g],qd[e] = a,xd(a, c, b),!0;
        Q.info('channel name mismatch; message ignored"');
        return!1
    };
    n = Xd.prototype;
    n.Od = function(a) {
        switch (a) {
            case "SETUP":
                this.send("tp", "SETUP_ACK");
                break;
            case "SETUP_ACK":
                wd(this.b)
        }
    };
    n.initbind = function() {
        var a = this.o(),b = s(a),c = Yd[b];
        typeof c == "number" || (c = 0);
        c == 0 && F(a.postMessage ? a : a.document, "message", Zd, !1, Xd);
        Yd[b] = c + 1;
        this.W = !0;
        this.If()
    };
    n.If = function() {
        !this.b.Y() && !this.Pb && (this.send("tp", "SETUP"),this.o().setTimeout(t(this.If, this), 100))
    };
    n.send = function(a, b) {
        var c = this.b.Z;
        if (c) {
            var d = c.postMessage ? c : c.document;
            this.send = function(a, b) {
                J(Q, "send(): payload=" + b + " to hostname=" + this.Kf);
                d.postMessage(this.b.name + "|" + a + ":" + b, this.Kf)
            };
            this.send(a, b)
        } else J(Q, "send(): window not ready")
    };
    n.h = function() {
        Xd.H.h.call(this);
        if (this.W) {
            var a = this.o(),b = s(a),c = Yd[b];
            Yd[b] = c - 1;
            c == 1 && Xb(a.postMessage ? a : a.document, "message", Zd, !1, Xd)
        }
    };
    var $d = function(a, b) {
        this.R = b || rb();
        this.b = a;
        this.nf = a.at || "";
        this.of = a.rat || "";
        var c = this.o();
        if (!c.nix_setup_complete)try {
            c.execScript("Class GCXPC____NIXVBS_wrapper\n Private m_Transport\nPrivate m_Auth\nPublic Sub SetTransport(transport)\nIf isEmpty(m_Transport) Then\nSet m_Transport = transport\nEnd If\nEnd Sub\nPublic Sub SetAuth(auth)\nIf isEmpty(m_Auth) Then\nm_Auth = auth\nEnd If\nEnd Sub\nPublic Function GetAuthToken()\n GetAuthToken = m_Auth\nEnd Function\nPublic Sub SendMessage(service, payload)\n Call m_Transport.GCXPC____NIXJS_handle_message(service, payload)\nEnd Sub\nPublic Sub CreateChannel(channel)\n Call m_Transport.GCXPC____NIXJS_create_channel(channel)\nEnd Sub\nPublic Sub GCXPC____NIXVBS_container()\n End Sub\nEnd Class\n Function GCXPC____NIXVBS_get_wrapper(transport, auth)\nDim wrap\nSet wrap = New GCXPC____NIXVBS_wrapper\nwrap.SetTransport transport\nwrap.SetAuth auth\nSet GCXPC____NIXVBS_get_wrapper = wrap\nEnd Function",
                    "vbscript"),c.nix_setup_complete = !0
        } catch(d) {
            Q.k("exception caught while attempting global setup: " + d)
        }
        this.GCXPC____NIXJS_handle_message = this.Qg;
        this.GCXPC____NIXJS_create_channel = this.bb
    };
    x($d, td);
    n = $d.prototype;
    n.$a = 6;
    n.sb = !1;
    n.Ja = m;
    n.initbind = function() {
        vd(this.b) == 0 ? this.yf() : this.vf()
    };
    n.yf = function() {
        if (!this.sb) {
            var a = this.b.kb;
            try {
                a.contentWindow.opener = this.o().GCXPC____NIXVBS_get_wrapper(this, this.nf),this.sb = !0
            } catch(b) {
                Q.k("exception caught while attempting setup: " + b)
            }
            this.sb || this.o().setTimeout(t(this.yf, this), 100)
        }
    };
    n.vf = function() {
        if (!this.sb) {
            try {
                var a = this.o().opener;
                if (a && "GCXPC____NIXVBS_container"in a) {
                    this.Ja = a;
                    if (this.Ja.GetAuthToken() != this.of) {
                        Q.k("Invalid auth token from other party");
                        return
                    }
                    this.Ja.CreateChannel(this.o().GCXPC____NIXVBS_get_wrapper(this, this.nf));
                    this.sb = !0;
                    wd(this.b)
                }
            } catch(b) {
                Q.k("exception caught while attempting setup: " + b);
                return
            }
            this.sb || this.o().setTimeout(t(this.vf, this), 100)
        }
    };
    n.bb = function(a) {
        (typeof a != "unknown" || !("GCXPC____NIXVBS_container"in a)) && Q.k("Invalid NIX channel given to createChannel_");
        this.Ja = a;
        this.Ja.GetAuthToken() != this.of ? Q.k("Invalid auth token from other party") : wd(this.b)
    };
    n.Qg = function(a, b) {
        this.o().setTimeout(t(function() {
            xd(this.b, a, b)
        }, this), 1)
    };
    n.send = function(a, b) {
        typeof this.Ja !== "unknown" && Q.k("NIX channel not connected");
        this.Ja.SendMessage(a, b)
    };
    n.h = function() {
        $d.H.h.call(this);
        this.Ja = m
    };
    var S = function(a, b) {
        this.Bc = {};
        for (var c = 0,d; d = pd[c]; c++)d in a && !/^https?:\/\//.test(a[d]) && f(Error("URI " + a[d] + " is invalid for field " + d));
        this.n = a;
        this.name = this.n.cn || sd(10);
        this.R = b || rb();
        a.lpu = a.lpu || Qc(this.R.o().location.href) + "/robots.txt";
        a.ppu = a.ppu || Qc(a.pu || "") + "/robots.txt";
        qd[this.name] = this;
        F(window, "unload", ae);
        Q.info("CrossPageChannel created: " + this.name)
    };
    x(S, Nc);
    var be = /^%*tp$/,ce = /^%+tp$/;
    n = S.prototype;
    n.M = m;
    n.f = 1;
    n.Y = function() {
        return this.f == 2
    };
    n.Z = m;
    n.kb = m;
    var de = function(a) {
        var b = {};
        b.cn = a.name;
        b.tp = a.n.tp;
        a.n.lru && (b.pru = a.n.lru);
        a.n.lpu && (b.ppu = a.n.lpu);
        a.n.ppu && (b.lpu = a.n.ppu);
        return b
    },ee = function(a) {
        var b = document.body,c = a.n.ifrid;
        c || (c = a.n.ifrid = "xpcpeer" + sd(4));
        var d = document.createElement("IFRAME");
        d.id = d.name = c;
        d.style.width = d.style.height = "100%";
        var e = a.n.pu;
        r(e) && (e = a.n.pu = new N(e));
        add_param(e, "xpc", gc(de(a)));
        Sa || A ? (a.Md = !0,window.setTimeout(t(function() {
            this.Md = !1;
            b.appendChild(d);
            d.src = e.toString();
            Q.info("peer iframe created (" + c + ")");
            this.Jf &&
            this.initbind(this.qf)
        }, a), 1)) : (d.src = e.toString(),b.appendChild(d),Q.info("peer iframe created (" + c + ")"))
    };
    S.prototype.Md = !1;
    S.prototype.Jf = !1;
    S.prototype.initbind = function(a) {
        this.qf = a || ca;
        if (this.Md)Q.info("connect() deferred"),this.Jf = !0; else {
            Q.info("connect()");
            if (this.n.ifrid)this.kb = r(this.n.ifrid) ? this.R.la.getElementById(this.n.ifrid) : this.n.ifrid;
            if (this.kb)(a = this.kb.contentWindow) || (a = window.frames[this.n.ifrid]),this.Z = a;
            if (!this.Z)window == top ? f(Error("CrossPageChannel: Can't connect, peer window-object not set.")) : this.Z = window.parent;
            if (!this.M) {
                if (!this.n.tp) {
                    var a = this.n,b;
                    if (fa(document.postMessage) || fa(window.postMessage) || z &&
                            window.postMessage)b = 1; else if (Sa)b = 2; else if (z && this.n.pru)b = 3; else {
                        var c;
                        if (c = z) {
                            c = !1;
                            try {
                                b = window.opener,window.opener = {},c = Ab(window, "opener"),window.opener = b
                            } catch(d) {
                            }
                        }
                        b = c ? 6 : 4
                    }
                    a.tp = b
                }
                switch (this.n.tp) {
                    case 1:
                        this.M = new Xd(this, this.n.ph, this.R);
                        break;
                    case 6:
                        this.M = new $d(this, this.R);
                        break;
                    case 2:
                        this.M = new ud(this, this.R);
                        break;
                    case 3:
                        this.M = new Od(this, this.R);
                        break;
                    case 4:
                        this.M = new R(this, this.R)
                }
                this.M ? Q.info("Transport created: " + this.M.getName()) : f(Error("CrossPageChannel: No suitable transport found!"))
            }
            this.M.initbind()
        }
    };
    S.prototype.close = function() {
        if (this.Y())this.f = 3,this.M.G(),this.M = m,Q.info('Channel "' + this.name + '" closed')
    };
    var wd = function(a) {
        if (!a.Y())a.f = 2,Q.info('Channel "' + a.name + '" connected'),a.qf()
    };
    S.prototype.send = function(a, b) {
        this.Y() ? this.Z.closed ? (Q.k("Peer has disappeared."),this.close()) : (ga(b) && (b = gc(b)),this.M.send(fe(a), b)) : Q.k("Can't send. Channel not connected.")
    };
    var xd = function(a, b, c, d) {
        var e = a.n.ph;
        if (/^[\s\xa0]*$/.test(d == m ? "" : String(d)) || /^[\s\xa0]*$/.test(e == m ? "" : String(e)) || d == a.n.ph)if (a.Pb)Q.v("CrossPageChannel::deliver_(): Disposed."); else if (!b || b == "tp")a.M.Od(c); else if (a.Y()) {
            if (b = b.replace(/%[0-9a-f]{2}/gi, decodeURIComponent),b = ce.test(b) ? b.substring(1) : b,d = a.Bc[b],d || (a.tf ? (d = la(a.tf, b),e = ga(c),d = {Of:d,Pf:e}) : (a.Fc.v('Unknown service name "' + b + '"'),d = m)),d) {
                var g;
                a:{
                    if ((e = d.Pf) && r(c))try {
                        g = cc(c);
                        break a
                    } catch(i) {
                        a.Fc.v("Expected JSON payload for " +
                                b + ', was "' + c + '"');
                        g = m;
                        break a
                    } else if (!e && !r(c)) {
                        g = gc(c);
                        break a
                    }
                    g = c
                }
                g != m && d.Of(g)
            }
        } else Q.info("CrossPageChannel::deliver_(): Not connected."); else Q.v('Message received from unapproved origin "' + d + '" - rejected.')
    },fe = function(a) {
        be.test(a) && (a = "%" + a);
        return a.replace(/[%:|]/g, encodeURIComponent)
    },vd = function(a) {
        return window.parent == a.Z ? 1 : 0
    };
    S.prototype.h = function() {
        S.H.h.call(this);
        this.close();
        this.kb = this.Z = m;
        delete qd[this.name]
    };
    var ae = function() {
        for (var a in qd) {
            var b = qd[a];
            b && b.G()
        }
    };
    var ge = function(a, b) {
        z ? a.cssText = b : a[A ? "innerText" : "innerHTML"] = b
    };
    var he = function(a, b, c, d, e, g) {
        var d = new N(d || window.location.href),i = new N;
        Tc(i, e || "talkgadget.google.com");
        Vc(i, "/talkgadget/d");
        add_param(i, "token", a);
        g && Uc(i, g);
        var a = c || "wcs-iframe",c = "#" + a + " { display: none; }",j = rb(h),k = m;
        if (z)k = j.la.createStyleSheet(),ge(k, c); else {
            var l = sb(j.la, "head")[0];
            l || (k = sb(j.la, "body")[0],l = j.Wf("head"),k.parentNode.insertBefore(l, k));
            k = j.Wf("style");
            ge(k, c);
            j.appendChild(l, k)
        }
        c = {};
        j = new N;
        Tc(j, e || "talkgadget.google.com");
        g && Uc(j, g);
        Vc(j, "/talkgadget/xpc_blank");
        d.K == "http" ||
                d.K == "https" ? (Rc(i, d.K),Rc(j, d.K),e = new N,Rc(e, d.K),Tc(e, d.ia),d.ja != 80 && Uc(e, d.ja),Vc(e, b)) : (Rc(i, "http"),Rc(j, "http"),e = new N("http://www.google.com/xpc_blank"));
        c.lpu = e.toString();
        c.ppu = j.toString();
        c.ifrid = a;
        c.pu = i.toString();
        S.call(this, c)
    };
    x(he, S);
    w("chat.WcsCrossPageChannel", he);
    var je = function(a, b, c, d, e) {
        this.readyState = 0;
        this.Rd = [];
        this.onopen = b.onopen;
        this.onmessage = b.onmessage;
        this.onerror = b.onerror;
        this.onclose = b.onclose;
        this.S = c || new he(a, "/_ah/channel/xpc_blank");
        this.Oc = c ? d : "wcs-iframe";
        this.$b = e || new ie(a);
        document.body || f("document.body is not defined -- do not create socket from script in <head>.");
        ee(this.S);
        Oc(this.S, "opened", t(this.jh, this));
        Oc(this.S, "onMessage", t(this.ih, this));
        Oc(this.S, "onError", t(this.Ec, this));
        Oc(this.S, "onClosed", t(this.Uf, this));
        this.S.initbind(t(function() {
            this.Pd()
        },
                this))
    };
    je.prototype.send = function() {
        return!1
    };
    je.prototype.close = function() {
        this.Uf()
    };
    je.prototype.vh = function() {
        for (var a = 0,b; b = this.Rd[a]; a++)switch (b.type) {
            case 0:
                this.onopen(b.Xc);
                break;
            case 1:
                this.onmessage(b.Xc);
                break;
            case 2:
                this.onerror(b.Xc);
                break;
            case 3:
                this.onclose(b.Xc)
        }
        this.Rd = []
    };
    var ke = function(a, b, c) {
        a.Rd.push({type:b,Xc:c});
        window.setTimeout(t(a.vh, a), 1)
    };
    n = je.prototype;
    n.ih = function(a) {
        var a = cc(a),b = a.m,a = a.s;
        a:{
            var c = le(this.$b, b);
            if (!ea(c) || !ea(a) || c.length != a.length)a = !1; else {
                for (var d = c.length,e = 0; e < d; e++)if (c[e] !== a[e]) {
                    a = !1;
                    break a
                }
                a = !0
            }
        }
        a && ke(this, 1, {data:b});
        this.$b.cc++
    };
    n.Ec = function(a) {
        a = cc(a);
        ke(this, 2, {description:a.d,code:a.c})
    };
    n.Pd = function() {
    };
    n.jh = function() {
        this.readyState = 1;
        ke(this, 0, {})
    };
    n.Uf = function() {
        this.S.close();
        this.readyState = 3;
        ke(this, 3, {});
        if (this.Oc) {
            var a = new qb,b = r(this.Oc) ? a.la.getElementById(this.Oc) : this.Oc;
            b && a.removeNode(b)
        }
    };
    var ie = function(a) {
        for (; a.length % 4 != 0;)a += ".";
        this.cc = 0;
        try {
            if (!eb) {
                eb = {};
                fb = {};
                gb = {};
                for (var b = 0; b < 65; b++)eb[b] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(b),fb[b] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.".charAt(b),gb[fb[b]] = b
            }
            for (var b = gb,c = [],d = 0; d < a.length;) {
                var e = b[a.charAt(d++)],g = d < a.length ? b[a.charAt(d)] : 0;
                ++d;
                var i = d < a.length ? b[a.charAt(d)] : 0;
                ++d;
                var j = d < a.length ? b[a.charAt(d)] : 0;
                ++d;
                (e == m || g == m || i == m || j == m) && f(Error());
                c.push(e <<
                        2 | g >> 4);
                i != 64 && (c.push(g << 4 & 240 | i >> 2),j != 64 && c.push(i << 6 & 192 | j))
            }
            this.gg = c
        } catch(k) {
            k.message ? f(Error("The provided token is invalid (" + k.name + ": " + k.message + ")")) : f(Error("The provided token is invalid."))
        }
        this.ba = new SHA1;
        this.qh = new G_HMAC(this.ba, this.gg, this.gg.length)
    },le = function(a, b) {
        for (var c = [],d = 0,e = 0; e < b.length; e++) {
            for (var g = b.charCodeAt(e); g > 255;)c[d++] = g & 255,g >>= 8;
            c[d++] = g
        }
        c.push(a.cc);
        d = a.qh;
        d.reset();
        d.update(c);
        return d.yb()
    };
    w("goog.appengine.Socket", je);
    w("goog.appengine.Socket.ReadyState", {CONNECTING:0,OPEN:1,Ph:2,CLOSED:3});
    w("goog.appengine.Socket.ReadyState.CONNECTING", 0);
    w("goog.appengine.Socket.ReadyState.OPEN", 1);
    w("goog.appengine.Socket.ReadyState.CLOSING", 2);
    w("goog.appengine.Socket.ReadyState.CLOSED", 3);
    w("goog.appengine.Socket.prototype.send", je.prototype.send);
    w("goog.appengine.Socket.prototype.close", je.prototype.close);
    var me = function() {
    };
    x(me, yb);
    n = me.prototype;
    n.Sf = !0;
    n.Nd = m;
    n.addEventListener = function(a, b, c, d) {
        F(this, a, b, c, d)
    };
    n.removeEventListener = function(a, b, c, d) {
        Xb(this, a, b, c, d)
    };
    n.dispatchEvent = function(a) {
        var b = a.type || a,c = E;
        if (b in c) {
            if (r(a))a = new B(a, this); else if (a instanceof B)a.target = a.target || this; else {
                var d = a,a = new B(b, this);
                mb(a, d)
            }
            var d = 1,e,c = c[b],b = !0 in c,g;
            if (b) {
                e = [];
                for (g = this; g; g = g.Nd)e.push(g);
                g = c[!0];
                g.ga = g.i;
                for (var i = e.length - 1; !a.xb && i >= 0 && g.ga; i--)a.currentTarget = e[i],d &= bc(g, e[i], a.type, !0, a) && a.Qc != !1
            }
            if (!1 in c)if (g = c[!1],g.ga = g.i,b)for (i = 0; !a.xb && i < e.length && g.ga; i++)a.currentTarget = e[i],d &= bc(g, e[i], a.type, !1, a) && a.Qc != !1; else for (e = this; !a.xb &&
                    e && g.ga; e = e.Nd)a.currentTarget = e,d &= bc(g, e, a.type, !1, a) && a.Qc != !1;
            a = Boolean(d)
        } else a = !0;
        return a
    };
    n.h = function() {
        me.H.h.call(this);
        $b(this);
        this.Nd = m
    };
    var oe = function(a, b) {
        this.gc = a || 1;
        this.ec = b || ne;
        this.Ud = t(this.sh, this);
        this.Vd = do_something()
    };
    x(oe, me);
    oe.prototype.enabled = !1;
    var ne = p.window;
    n = oe.prototype;
    n.fa = m;
    n.setInterval = function(a) {
        this.gc = a;
        this.fa && this.enabled ? (this.stop(),this.start()) : this.fa && this.stop()
    };
    n.sh = function() {
        if (this.enabled) {
            var a = do_something() - this.Vd;
            if (a > 0 && a < this.gc * 0.8)this.fa = this.ec.setTimeout(this.Ud, this.gc - a); else if (this.Td(),this.enabled)this.fa = this.ec.setTimeout(this.Ud, this.gc),this.Vd = do_something()
        }
    };
    n.Td = function() {
        this.dispatchEvent("tick")
    };
    n.start = function() {
        this.enabled = !0;
        if (!this.fa)this.fa = this.ec.setTimeout(this.Ud, this.gc),this.Vd = do_something()
    };
    n.stop = function() {
        this.enabled = !1;
        if (this.fa)this.ec.clearTimeout(this.fa),this.fa = m
    };
    n.h = function() {
        oe.H.h.call(this);
        this.stop();
        delete this.ec
    };
    var pe = function() {
        if (Sa)this.Wa = {},this.Jc = {},this.Pc = []
    };
    pe.prototype.g = M("goog.net.xhrMonitor");
    pe.prototype.Ic = Sa;
    var re = function(a) {
        var b = qe;
        if (b.Ic) {
            var c = r(a) ? a : ga(a) ? s(a) : "";
            L(b.g, "Pushing context: " + a + " (" + c + ")");
            b.Pc.push(c)
        }
    },te = function() {
        var a = qe;
        if (a.Ic) {
            var b = a.Pc.pop();
            L(a.g, "Popping context: " + b);
            se(a, b)
        }
    },ve = function(a) {
        var b = qe;
        if (b.Ic) {
            a = s(a);
            J(b.g, "Opening XHR : " + a);
            for (var c = 0; c < b.Pc.length; c++) {
                var d = b.Pc[c];
                ue(b.Wa, d, a);
                ue(b.Jc, a, d)
            }
        }
    },se = function(a, b) {
        var c = a.Jc[b],d = a.Wa[b];
        c && d && (L(a.g, "Updating dependent contexts"),Ea(c, function(a) {
            Ea(d, function(b) {
                ue(this.Wa, a, b);
                ue(this.Jc, b, a)
            }, this)
        },
                a))
    },ue = function(a, b, c) {
        a[b] || (a[b] = []);
        Da(a[b], c) >= 0 || a[b].push(c)
    },qe = new pe;
    var we = function() {
    };
    we.prototype.Cc = m;
    var ze = function() {
        return xe(ye)
    },ye,Ae = function() {
    };
    x(Ae, we);
    var xe = function(a) {
        return(a = Be(a)) ? new ActiveXObject(a) : new XMLHttpRequest
    },Ce = function(a) {
        var b = {};
        Be(a) && (b[0] = !0,b[1] = !0);
        return b
    };
    Ae.prototype.ae = m;
    var Be = function(a) {
        if (!a.ae && typeof XMLHttpRequest == "undefined" && typeof ActiveXObject != "undefined") {
            for (var b = ["MSXML2.XMLHTTP.6.0","MSXML2.XMLHTTP.3.0","MSXML2.XMLHTTP","Microsoft.XMLHTTP"],c = 0; c < b.length; c++) {
                var d = b[c];
                try {
                    return new ActiveXObject(d),a.ae = d
                } catch(e) {
                }
            }
            f(Error("Could not create ActiveXObject. ActiveX might be disabled, or MSXML might not be installed"))
        }
        return a.ae
    };
    ye = new Ae;
    var T = function(a) {
        this.headers = new G;
        this.pb = a || m
    };
    x(T, me);
    T.prototype.g = M("goog.net.XhrIo");
    var De = /^https?:?$/i,Ee = [],Fe = function(a) {
        a.G();
        Fa(Ee, a)
    };
    n = T.prototype;
    n.Fa = !1;
    n.j = m;
    n.wc = m;
    n.Ub = "";
    n.df = "";
    n.Sb = 0;
    n.l = "";
    n.Bd = !1;
    n.yc = !1;
    n.Ad = !1;
    n.Va = !1;
    n.Vb = 0;
    n.Ta = m;
    n.mf = "";
    n.Lg = !1;
    n.send = function(a, b, c, d) {
        this.j && f(Error("[goog.net.XhrIo] Object is active with another request"));
        b = b ? b.toUpperCase() : "GET";
        this.Ub = a;
        this.l = "";
        this.Sb = 0;
        this.df = b;
        this.Bd = !1;
        this.Fa = !0;
        this.j = this.pb ? xe(this.pb) : new ze;
        this.wc = this.pb ? this.pb.Cc || (this.pb.Cc = Ce(this.pb)) : ye.Cc || (ye.Cc = Ce(ye));
        ve(this.j);
        this.j.onreadystatechange = t(this.Ue, this);
        try {
            J(this.g, Ge(this, "Opening Xhr")),this.Ad = !0,this.j.open(b, a, !0),this.Ad = !1
        } catch(e) {
            J(this.g, Ge(this, "Error opening Xhr: " + e.message));
            He(this, e);
            return
        }
        var a =
                c || "",g = this.headers.C();
        d && pc(d, function(a, b) {
            g.set(b, a)
        });
        b == "POST" && !g.ra("Content-Type") && g.set("Content-Type", "application/x-www-form-urlencoded;charset=utf-8");
        pc(g, function(a, b) {
            this.j.setRequestHeader(b, a)
        }, this);
        if (this.mf)this.j.responseType = this.mf;
        if ("withCredentials"in this.j)this.j.withCredentials = this.Lg;
        try {
            if (this.Ta)ne.clearTimeout(this.Ta),this.Ta = m;
            if (this.Vb > 0)J(this.g, Ge(this, "Will abort after " + this.Vb + "ms if incomplete")),this.Ta = ne.setTimeout(t(this.Jb, this), this.Vb);
            J(this.g,
                    Ge(this, "Sending request"));
            this.yc = !0;
            this.j.send(a);
            this.yc = !1
        } catch(i) {
            J(this.g, Ge(this, "Send error: " + i.message)),He(this, i)
        }
    };
    n.dispatchEvent = function(a) {
        if (this.j) {
            re(this.j);
            try {
                return T.H.dispatchEvent.call(this, a)
            } finally {
                te()
            }
        } else return T.H.dispatchEvent.call(this, a)
    };
    n.Jb = function() {
        if (typeof aa != "undefined" && this.j)this.l = "Timed out after " + this.Vb + "ms, aborting",this.Sb = 8,J(this.g, Ge(this, this.l)),this.dispatchEvent("timeout"),this.abort(8)
    };
    var He = function(a, b) {
        a.Fa = !1;
        if (a.j)a.Va = !0,a.j.abort(),a.Va = !1;
        a.l = b;
        a.Sb = 5;
        Ie(a);
        Je(a)
    },Ie = function(a) {
        if (!a.Bd)a.Bd = !0,a.dispatchEvent("complete"),a.dispatchEvent("error")
    };
    T.prototype.abort = function(a) {
        if (this.j && this.Fa)J(this.g, Ge(this, "Aborting")),this.Fa = !1,this.Va = !0,this.j.abort(),this.Va = !1,this.Sb = a || 7,this.dispatchEvent("complete"),this.dispatchEvent("abort"),Je(this)
    };
    T.prototype.h = function() {
        if (this.j) {
            if (this.Fa)this.Fa = !1,this.Va = !0,this.j.abort(),this.Va = !1;
            Je(this, !0)
        }
        T.H.h.call(this)
    };
    T.prototype.Ue = function() {
        !this.Ad && !this.yc && !this.Va ? this.Yd() : Ke(this)
    };
    T.prototype.Yd = function() {
        Ke(this)
    };
    var Ke = function(a) {
        if (a.Fa && typeof aa != "undefined")if (a.wc[1] && Le(a) == 4 && a.xa() == 2)J(a.g, Ge(a, "Local request error detected and ignored")); else if (a.yc && Le(a) == 4)ne.setTimeout(t(a.Ue, a), 0); else if (a.dispatchEvent("readystatechange"),Le(a) == 4) {
            J(a.g, Ge(a, "Request complete"));
            a.Fa = !1;
            var b;
            a:switch (a.xa()) {
                case 0:
                    b = (b = r(a.Ub) ? a.Ub.match(Pc)[1] || m : a.Ub.K) ? De.test(b) : self.location ? De.test(self.location.protocol) : !0;
                    b = !b;
                    break a;
                case 200:
                case 204:
                case 304:
                case 1223:
                    b = !0;
                    break a;
                default:
                    b = !1
            }
            if (b)a.dispatchEvent("complete"),
                    a.dispatchEvent("success"); else {
                a.Sb = 6;
                var c;
                try {
                    c = Le(a) > 2 ? a.j.statusText : ""
                } catch(d) {
                    J(a.g, "Can not get status: " + d.message),c = ""
                }
                a.l = c + " [" + a.xa() + "]";
                Ie(a)
            }
            Je(a)
        }
    },Je = function(a, b) {
        if (a.j) {
            var c = a.j,d = a.wc[0] ? ca : m;
            a.j = m;
            a.wc = m;
            if (a.Ta)ne.clearTimeout(a.Ta),a.Ta = m;
            b || (re(c),a.dispatchEvent("ready"),te());
            var e = qe;
            if (e.Ic) {
                var g = s(c);
                J(e.g, "Closing XHR : " + g);
                delete e.Jc[g];
                for (var i in e.Wa)Fa(e.Wa[i], g),e.Wa[i].length == 0 && delete e.Wa[i]
            }
            try {
                c.onreadystatechange = d
            } catch(j) {
                a.g.k("Problem encountered resetting onreadystatechange: " +
                        j.message)
            }
        }
    };
    T.prototype.Ua = function() {
        return!!this.j
    };
    var Le = function(a) {
        return a.j ? a.j.readyState : 0
    };
    T.prototype.xa = function() {
        try {
            return Le(this) > 2 ? this.j.status : -1
        } catch(a) {
            return this.g.v("Can not get status: " + a.message),-1
        }
    };
    var Me = function(a) {
        try {
            return a.j ? a.j.responseText : ""
        } catch(b) {
            return J(a.g, "Can not get responseText: " + b.message),""
        }
    };
    T.prototype.Re = function() {
        return r(this.l) ? this.l : String(this.l)
    };
    var Ge = function(a, b) {
        return b + " [" + a.df + " " + a.Ub + " " + a.xa() + "]"
    };
    var Pe = function() {
        this.N = [];
        this.Da = new G;
        this.Hf = this.cd = this.dd = this.Eb = 0;
        this.Pa = new G;
        this.Ff = this.bd = 0;
        this.hh = 1;
        this.Ra = new C(0, 4E3);
        this.Ra.dc = function() {
            return new Ne
        };
        this.fd = new C(0, 50);
        this.fd.dc = function() {
            return new Oe
        };
        var a = this;
        this.ib = new C(0, 2E3);
        this.ib.dc = function() {
            return String(a.hh++)
        };
        this.ib.Gd = function() {
        };
        this.he = 3
    };
    Pe.prototype.g = M("goog.debug.Trace");
    Pe.prototype.nd = 1E3;
    var Oe = function() {
        this.oc = this.jd = this.count = 0
    };
    Oe.prototype.toString = function() {
        var a = [];
        a.push(this.type, " ", this.count, " (", Math.round(this.jd * 10) / 10, " ms)");
        this.oc && a.push(" [VarAlloc = ", this.oc, "]");
        return a.join("")
    };
    var Ne = function() {
    },Se = function(a, b, c, d) {
        var e = [];
        c == -1 ? e.push("    ") : e.push(Qe(a.qc - c));
        e.push(" ", Re(a.qc - b));
        a.Ob == 0 ? e.push(" Start        ") : a.Ob == 1 ? (e.push(" Done "),e.push(Qe(a.Dg - a.startTime), " ms ")) : e.push(" Comment      ");
        e.push(d, a);
        a.Qb > 0 && e.push("[VarAlloc ", a.Qb, "] ");
        return e.join("")
    };
    Ne.prototype.toString = function() {
        return this.type == m ? this.Rb : "[" + this.type + "] " + this.Rb
    };
    Pe.prototype.reset = function(a) {
        this.he = a;
        for (a = 0; a < this.N.length; a++) {
            var b = this.Ra.id;
            b && D(this.ib, b);
            D(this.Ra, this.N[a])
        }
        this.N.length = 0;
        this.Da.clear();
        this.Eb = do_something();
        this.Ff = this.bd = this.Hf = this.cd = this.dd = 0;
        b = this.Pa.Ka();
        for (a = 0; a < b.length; a++) {
            var c = this.Pa.get(b[a]);
            c.count = 0;
            c.jd = 0;
            c.oc = 0;
            D(this.fd, c)
        }
        this.Pa.clear()
    };
    var Te = function(a) {
        if ((a = a.Uh) && a.isTracing())return a.totalVarAlloc;
        return-1
    };
    Pe.prototype.toString = function() {
        for (var a = [],b = -1,c = [],d = 0; d < this.N.length; d++) {
            var e = this.N[d];
            e.Ob == 1 && c.pop();
            a.push(" ", Se(e, this.Eb, b, c.join("")));
            b = e.qc;
            a.push("\n");
            e.Ob == 0 && c.push("|  ")
        }
        if (this.Da.Fb() != 0) {
            var g = do_something();
            a.push(" Unstopped timers:\n");
            nc(this.Da, function(b) {
                a.push("  ", b, " (", g - b.startTime, " ms, started at ", Re(b.startTime), ")\n")
            })
        }
        b = this.Pa.Ka();
        for (d = 0; d < b.length; d++)c = this.Pa.get(b[d]),c.count > 1 && a.push(" TOTAL ", c, "\n");
        a.push("Total tracers created ", this.bd, "\n", "Total comments created ",
                this.Ff, "\n", "Overhead start: ", this.dd, " ms\n", "Overhead end: ", this.cd, " ms\n", "Overhead comment: ", this.Hf, " ms\n");
        return a.join("")
    };
    Pe.prototype.uc = function(a) {
        p.console && p.console.markTimeline && p.console.markTimeline(a)
    };
    var Ue = function(a) {
        p.msWriteProfilerMark && p.msWriteProfilerMark(a)
    },Qe = function(a) {
        var a = Math.round(a),b = "";
        a < 1E3 && (b = " ");
        a < 100 && (b = "  ");
        a < 10 && (b = "   ");
        return b + a
    },Re = function(a) {
        a = Math.round(a);
        return String(100 + a / 1E3 % 60).substring(1, 3) + "." + String(1E3 + a % 1E3).substring(1, 4)
    },Ve = new Pe;
    M("goog.debug.ErrorReporter");
    /*
     Portions of this code are from MochiKit, received by
     The Closure Authors under the MIT license. All other code is Copyright
     2005-2009 The Closure Authors. All Rights Reserved.
     */
    var We = function(a) {
        this.u = a
    };
    x(We, yb);
    var Xe = new C(0, 100),Ye = [],$e = function(a, b, c, d, e, g) {
        q(c) || (Ye[0] = c,c = Ye);
        for (var i = 0; i < c.length; i++)Ze(a, F(b, c[i], d || a, e || !1, g || a.u || a))
    },af = function(a, b, c, d, e, g) {
        if (q(c))for (var i = 0; i < c.length; i++)af(a, b, c[i], d, e, g); else Ze(a, Wb(b, c, d || a, e || !1, g || a.u || a))
    },Ze = function(a, b) {
        a.r ? a.r[b] = !0 : a.hc ? (a.r = Xe.getObject(),a.r[a.hc] = !0,a.hc = m,a.r[b] = !0) : a.hc = b
    },bf = function(a) {
        if (a.r) {
            for (var b in a.r)Yb(b),delete a.r[b];
            D(Xe, a.r);
            a.r = m
        } else a.hc && Yb(a.hc)
    };
    We.prototype.h = function() {
        We.H.h.call(this);
        bf(this)
    };
    We.prototype.handleEvent = function() {
        f(Error("EventHandler.handleEvent not implemented"))
    };
    var cf = function(a, b, c) {
        oe.call(this, b, c);
        this.rh = a
    };
    x(cf, oe);
    var df = M("fava.core.Timer");
    cf.prototype.Td = function() {
        J(df, "Tick for " + this.rh);
        cf.H.Td.call(this)
    };
    var ff = function(a, b, c, d) {
        fa(b) || b && typeof b.handleEvent == "function" || f(Error("Invalid listener argument"));
        a = t(ef, m, a, b, d);
        return ne.setTimeout(a, c || 0)
    },ef = function(a, b, c) {
        J(df, "Callback for " + a);
        fa(b) ? b.call(c) : b && typeof b.handleEvent == "function" && b.handleEvent.call(b)
    };
    var gf = function() {
        this.pg = do_something()
    };
    new gf;
    gf.prototype.set = function(a) {
        this.pg = a
    };
    gf.prototype.reset = function() {
        this.set(do_something())
    };
    gf.prototype.get = function() {
        return this.pg
    };
    var U = function(a, b, c, d, e) {
        this.b = a;
        this.e = b;
        this.ma = c;
        this.X = d;
        this.Gb = e || 1;
        this.Jb = 45E3;
        this.ge = new We(this);
        this.lc = new oe;
        this.lc.setInterval(250)
    };
    n = U.prototype;
    n.T = m;
    n.ca = !1;
    n.rb = m;
    n.Dd = m;
    n.ab = m;
    n.La = m;
    n.Aa = m;
    n.U = m;
    n.ya = m;
    n.I = m;
    n.Mb = 0;
    n.ea = m;
    n.fb = m;
    n.l = m;
    n.D = -1;
    n.re = !0;
    n.jb = !1;
    var hf = function(a, b) {
        switch (a) {
            case 0:
                return"Non-200 return code (" + b + ")";
            case 1:
                return"XMLHTTP failure (no data)";
            case 2:
                return"HttpConnection timeout";
            default:
                return"Unknown error"
        }
    },jf = {},kf = {};
    U.prototype.za = function(a) {
        this.T = a
    };
    U.prototype.setTimeout = function(a) {
        this.Jb = a
    };
    var mf = function(a, b, c) {
        a.La = 1;
        a.Aa = add_zx_parameter(b.C());
        a.ya = c;
        a.ee = !0;
        lf(a, m)
    },nf = function(a, b, c, d, e) {
        a.La = 1;
        a.Aa = add_zx_parameter(b.C());
        a.ya = m;
        a.ee = c;
        if (e)a.re = !1;
        lf(a, d)
    },lf = function(a, b) {
        a.U = a.Aa.C();
        jd(a.U, "t", a.Gb);
        a.Mb = 0;
        a.I = a.b.sd(a.b.vc() ? b : m);
        F(a.I, "readystatechange", a.pe, !1, a);
        var c;
        if (a.T) {
            c = a.T;
            var d = {},e;
            for (e in c)d[e] = c[e];
            c = d
        } else c = {};
        a.ya ? (a.fb = "POST",c["Content-Type"] = "application/x-www-form-urlencoded",a.I.send(a.U, a.fb, a.ya, c)) : (a.fb = "GET",a.re && !A && (c.Connection = "close"),a.I.send(a.U, a.fb, m, c));
        a.ab =
                do_something();
        if (d = a.ya) {
            c = "";
            d = d.split("&");
            for (e = 0; e < d.length; e++) {
                var g = d[e].split("=");
                if (g.length > 1) {
                    var i = g[0],g = g[1],j = i.split("_");
                    c += j.length >= 2 && j[1] == "type" ? i + "=" + g + "&" : i + "=redacted&"
                }
            }
        } else c = m;
        a.e.info("XMLHTTP REQ (" + a.X + ") [attempt " + a.Gb + "]: " + a.fb + "\n" + a.U + "\n" + c);
        of(a)
    };
    U.prototype.pe = function(a) {
        a = a.target;
        try {
            if (a == this.I)a:{
                var b = Le(this.I);
                if (z || A && !db("420+")) {
                    if (b < 4)break a
                } else if (b < 3 || b == 3 && !Ra && !Me(this.I))break a;
                pf(this);
                var c = this.I.xa();
                this.D = c;
                var d = Me(this.I);
                d || this.e.info("No response text for uri " + this.U + " status " + c);
                this.ca = c == 200;
                this.e.info("XMLHTTP RESP (" + this.X + ") [ attempt " + this.Gb + "]: " + this.fb + "\n" + this.U + "\n" + b + " " + c);
                if (this.ca) {
                    if (b == 4 && qf(this),this.ee ? (rf(this, b, d),Ra && b == 3 && ($e(this.ge, this.lc, "tick", this.tg),this.lc.start())) :
                            (sf(this.e, this.X, d, m),tf(this, d)),this.ca && !this.jb)b == 4 ? this.b.pc(this) : (this.ca = !1,of(this))
                } else c == 400 && d.indexOf("Unknown SID") > 0 ? (this.l = 3,V(13)) : (this.l = 0,V(14)),sf(this.e, this.X, d),qf(this),uf(this)
            } else this.e.v("Called back with an unexpected xmlhttp")
        } catch(e) {
            this.e.info("Failed call to OnXmlHttpReadyStateChanged_"),this.I && Me(this.I) ? vf(this.e, e, "ResponseText: " + Me(this.I)) : vf(this.e, e, "No response text")
        } finally {
        }
    };
    var rf = function(a, b, c) {
        for (var d = !0; !a.jb && a.Mb < c.length;) {
            var e = wf(a, c);
            if (e == kf) {
                if (b == 4)a.l = 4,V(15),d = !1;
                sf(a.e, a.X, m, "[Incomplete Response]");
                break
            } else if (e == jf) {
                a.l = 4;
                V(16);
                sf(a.e, a.X, c, "[Invalid Chunk]");
                d = !1;
                break
            } else sf(a.e, a.X, e, m),tf(a, e)
        }
        if (b == 4 && c.length == 0)a.l = 1,V(17),d = !1;
        a.ca = a.ca && d;
        d || (sf(a.e, a.X, c, "[Invalid Chunked Response]"),qf(a),uf(a))
    };
    U.prototype.tg = function() {
        var a = Le(this.I),b = Me(this.I);
        this.Mb < b.length && (pf(this),rf(this, a, b),this.ca && a != 4 && of(this))
    };
    var wf = function(a, b) {
        var c = a.Mb,d = b.indexOf("\n", c);
        if (d == -1)return kf;
        c = Number(b.substring(c, d));
        if (isNaN(c))return jf;
        d += 1;
        if (d + c > b.length)return kf;
        var e = b.substr(d, c);
        a.Mb = d + c;
        return e
    },xf = function(a, b) {
        a.ea = new ActiveXObject("htmlfile");
        var c = "",d = "<html><body>";
        if (b)c = window.location.hostname,d += '<script>document.domain="' + c + '"<\/script>';
        d += "</body></html>";
        a.ea.open();
        a.ea.write(d);
        a.ea.close();
        a.ea.parentWindow.m = t(a.Ug, a);
        a.ea.parentWindow.d = t(a.Cf, a, !0);
        a.ea.parentWindow.rpcClose = t(a.Cf,
                a, !1);
        d = a.ea.createElement("div");
        a.ea.parentWindow.document.body.appendChild(d);
        a.U = a.Aa.C();
        add_param(a.U, "DOMAIN", c);
        add_param(a.U, "t", a.Gb);
        d.innerHTML = '<iframe src="' + a.U + '"></iframe>';
        a.ab = do_something();
        a.e.info("TRIDENT REQ (" + a.X + ") [ attempt " + a.Gb + "]: GET\n" + a.U);
        of(a)
    };
    n = U.prototype;
    n.Ug = function(a) {
        yf(t(this.Ah, this, a), 0)
    };
    n.Ah = function(a) {
        if (!this.jb) {
            var b = this.e;
            b.info("TRIDENT TEXT (" + this.X + "): " + zf(b, a));
            pf(this);
            tf(this, a);
            of(this)
        }
    };
    n.Cf = function(a) {
        yf(t(this.zh, this, a), 0)
    };
    n.zh = function(a) {
        if (!this.jb)this.e.info("TRIDENT TEXT (" + this.X + "): " + a ? "success" : "failure"),pf(this),qf(this),this.ca = a,this.b.pc(this)
    };
    n.cancel = function() {
        this.jb = !0;
        pf(this);
        qf(this)
    };
    var of = function(a) {
        a.Dd = do_something() + a.Jb;
        Af(a, a.Jb)
    },Af = function(a, b) {
        a.rb != m && f(Error("WatchDog timer not null"));
        a.rb = yf(t(a.xh, a), b)
    },pf = function(a) {
        if (a.rb)p.clearTimeout(a.rb),a.rb = m
    };
    U.prototype.xh = function() {
        this.rb = m;
        var a = do_something();
        a - this.Dd >= 0 ? (this.ca && this.e.k("Received watchdog timeout even though request loaded successfully"),this.e.info("TIMEOUT: " + this.U),qf(this),this.l = 2,V(18),uf(this)) : (this.e.v("WatchDog timer called too early"),Af(this, this.Dd - a))
    };
    var uf = function(a) {
        !a.b.Rf() && !a.jb && a.b.pc(a)
    },qf = function(a) {
        a.lc.stop();
        bf(a.ge);
        if (a.I) {
            var b = a.I;
            a.I = m;
            Xb(b, "readystatechange", a.pe, !1, a);
            b.abort()
        }
        if (a.ea)a.ea = m
    };
    U.prototype.Re = function() {
        return this.l
    };
    U.prototype.O = function() {
        return this.D
    };
    U.prototype.xc = function() {
        return this.ma
    };
    var tf = function(a, b) {
        try {
            a.b.xf(a, b)
        } catch(c) {
            vf(a.e, c, "Error in httprequest callback")
        }
    };
    var Bf = function() {
        this.g = M("goog.net.BrowserChannel")
    },sf = function(a, b, c, d) {
        a.info("XMLHTTP TEXT (" + b + "): " + zf(a, c) + (d ? " " + d : ""))
    },Cf = function(a, b) {
        a.info(b)
    },vf = function(a, b, c) {
        a.k((c || "Exception") + b)
    };
    Bf.prototype.info = function(a) {
        this.g.info(a)
    };
    Bf.prototype.v = function(a) {
        this.g.v(a)
    };
    Bf.prototype.k = function(a) {
        this.g.k(a)
    };
    var zf = function(a, b) {
        if (!b || b == "y2f%")return b;
        try {
            for (var c = dc(b),d = 0; d < c.length; d++)if (q(c[d])) {
                var e = c[d];
                if (!(e.length < 2)) {
                    var g = e[1];
                    if (q(g) && !(g.length < 1)) {
                        var i = g[0];
                        if (i != "noop" && i != "stop")for (var j = 1; j < g.length; j++)g[j] = ""
                    }
                }
            }
            return gc(c)
        } catch(k) {
            return a.info("Exception parsing expected JS array - probably was not JS"),b
        }
    };
    var Ef = function(a, b, c, d, e) {
        Cf(new Bf, "TestLoadImageWithRetries: " + e);
        if (d == 0)c(!1); else {
            var g = e || 0;
            d--;
            Df(a, b, function(e) {
                e ? c(!0) : p.setTimeout(function() {
                    Ef(a, b, c, d, g)
                }, g)
            })
        }
    },Df = function(a, b, c) {
        var d = new Bf;
        d.info("TestLoadImage: loading " + a);
        var e = new Image;
        e.onload = function() {
            try {
                d.info("TestLoadImage: loaded"),Ff(e),c(!0)
            } catch(a) {
                vf(d, a)
            }
        };
        e.onerror = function() {
            try {
                d.info("TestLoadImage: error"),Ff(e),c(!1)
            } catch(a) {
                vf(d, a)
            }
        };
        e.onabort = function() {
            try {
                d.info("TestLoadImage: abort"),Ff(e),c(!1)
            } catch(a) {
                vf(d,
                        a)
            }
        };
        e.ontimeout = function() {
            try {
                d.info("TestLoadImage: timeout"),Ff(e),c(!1)
            } catch(a) {
                vf(d, a)
            }
        };
        p.setTimeout(function() {
            if (e.ontimeout)e.ontimeout()
        }, b);
        e.src = a
    },Ff = function(a) {
        a.onload = m;
        a.onerror = m;
        a.onabort = m;
        a.ontimeout = m
    };
    var Gf = function(a, b) {
        this.b = a;
        this.e = b
    };
    n = Gf.prototype;
    n.T = m;
    n.V = m;
    n.tc = !1;
    n.Eb = m;
    n.sc = m;
    n.ld = m;
    n.z = m;
    n.f = m;
    n.D = -1;
    n.na = m;
    n.kd = m;
    n.za = function(a) {
        this.T = a
    };
    n.initbind = function(a) {
        this.z = a;
        a = Hf(this.b, this.z);
        V(3);
        jd(a, "MODE", "init");
        this.V = new U(this, this.e, h, h, h);
        this.V.za(this.T);
        nf(this.V, a, !1, m, !0);
        this.f = 0;
        this.Eb = do_something()
    };
    n.Gg = function(a) {
        a ? (this.f = 2,If(this)) : (V(4),a = this.b,a.e.info("Test Connection Blocked"),a.D = a.Qa.O(),W(a, 9))
    };
    var If = function(a) {
        a.e.info("TestConnection: starting stage 2");
        a.V = new U(a, a.e, h, h, h);
        a.V.za(a.T);
        var b = Jf(a.b, a.na, a.z);
        V(5);
        if (z) {
            jd(b, "TYPE", "html");
            var c = a.V,a = Boolean(a.na);
            c.La = 3;
            c.Aa = add_zx_parameter(b.C());
            xf(c, a)
        } else jd(b, "TYPE", "xmlhttp"),nf(a.V, b, !1, a.na, !1)
    };
    n = Gf.prototype;
    n.sd = function(a) {
        return this.b.sd(a)
    };
    n.abort = function() {
        if (this.V)this.V.cancel(),this.V = m;
        this.D = -1
    };
    n.Rf = function() {
        return!1
    };
    n.xf = function(a, b) {
        this.D = a.O();
        if (this.f == 0)if (this.e.info("TestConnection: Got data for stage 1"),b) {
            try {
                var c = dc(b)
            } catch(d) {
                vf(this.e, d);
                Kf(this.b, this);
                return
            }
            this.na = this.b.jc(c[0]);
            this.kd = c[1]
        } else this.e.info("TestConnection: Null responseText"),Kf(this.b, this); else if (this.f == 2)if (this.tc)V(7),this.ld = do_something(); else if (b == "11111") {
            if (V(6),this.tc = !0,this.sc = do_something(),c = this.sc - this.Eb,!z || c < 500)this.D = 200,this.V.cancel(),this.e.info("Test connection succeeded; using streaming connection"),V(12),Lf(this.b,
                    this, !0)
        } else V(8),this.sc = this.ld = do_something(),this.tc = !1
    };
    n.pc = function() {
        this.D = this.V.O();
        if (this.V.ca)if (this.f == 0)if (this.e.info("TestConnection: request complete for initial check"),this.kd) {
            this.f = 1;
            var a = Mf(this.b, this.kd, "/mail/images/cleardot.gif");
            add_zx_parameter(a);
            Ef(a.toString(), 5E3, t(this.Gg, this), 3, 2E3)
        } else this.f = 2,If(this); else this.f == 2 && (this.e.info("TestConnection: request complete for stage 2"),a = !1,(a = z ? this.ld - this.sc < 200 ? !1 : !0 : this.tc) ? (this.e.info("Test connection succeeded; using streaming connection"),V(12),Lf(this.b, this, !0)) : (this.e.info("Test connection failed; not using streaming"),
                V(11),Lf(this.b, this, !1))); else this.e.info("TestConnection: request failed, in state " + this.f),this.f == 0 ? V(9) : this.f == 2 && V(10),Kf(this.b, this)
    };
    n.O = function() {
        return this.D
    };
    n.vc = function() {
        return this.b.vc()
    };
    n.Ua = function() {
        return this.b.Ua()
    };
    var X = function(a) {
        this.Db = a;
        this.f = 1;
        this.Q = [];
        this.pa = [];
        this.e = new Bf
    },Nf = function(a, b) {
        this.$f = a;
        this.map = b
    };
    n = X.prototype;
    n.T = m;
    n.ac = m;
    n.P = m;
    n.B = m;
    n.z = m;
    n.kc = m;
    n.be = m;
    n.na = m;
    n.oh = !0;
    n.Nb = 0;
    n.Rg = 0;
    n.Hg = !1;
    n.u = m;
    n.Ca = m;
    n.oa = m;
    n.Sa = m;
    n.Qa = m;
    n.$c = m;
    n.Xg = !0;
    n.zb = -1;
    n.je = -1;
    n.D = -1;
    n.hb = 0;
    n.gb = 0;
    n.cb = 8;
    var Of = new me,Pf = function(a, b) {
        B.call(this, "statevent", a);
        this.Yh = b
    };
    x(Pf, B);
    var Qf = function(a, b, c, d) {
        B.call(this, "timingevent", a);
        this.size = b;
        this.Nh = c;
        this.Mh = d
    };
    x(Qf, B);
    X.prototype.qb = function(a) {
        this.e = a
    };
    X.prototype.initbind = function(a, b, c, d, e) {
        this.e.info("connect()");
        V(0);
        this.z = b;
        this.ac = c || {};
        if (d && e !== h)this.ac.OSID = d,this.ac.OAID = e;
        this.e.info("connectTest_()");
        this.Qa = new Gf(this, this.e);
        this.Qa.za(this.T);
        this.Qa.initbind(a)
    };
    X.prototype.rc = function() {
        this.e.info("disconnect()");
        Rf(this);
        if (this.f == 3) {
            var a = this.Nb++,b = this.kc.C();
            add_param(b, "SID", this.ma);
            add_param(b, "RID", a);
            add_param(b, "TYPE", "terminate");
            Sf(this, b);
            a = new U(this, this.e, this.ma, a, h);
            a.La = 2;
            a.Aa = add_zx_parameter(b.C());
            (new Image).src = a.Aa;
            a.ab = do_something();
            of(a);
            Tf(this)
        }
    };
    X.prototype.xc = function() {
        return this.ma
    };
    var Rf = function(a) {
        if (a.Qa)a.Qa.abort(),a.Qa = m;
        if (a.B)a.B.cancel(),a.B = m;
        if (a.oa)p.clearTimeout(a.oa),a.oa = m;
        Uf(a);
        if (a.P)a.P.cancel(),a.P = m;
        if (a.Ca)p.clearTimeout(a.Ca),a.Ca = m
    };
    n = X.prototype;
    n.za = function(a) {
        this.T = a
    };
    n.Ea = function(a) {
        this.f == 0 && f(Error("Invalid operation: sending map when state is closed"));
        this.Q.length == 1E3 && this.e.k("Already have 1000 queued maps upon queueing " + gc(a));
        this.Q.push(new Nf(this.Rg++, a));
        (this.f == 2 || this.f == 3) && Vf(this)
    };
    n.Rf = function() {
        return this.f == 0
    };
    n.Ga = function() {
        return this.f
    };
    n.O = function() {
        return this.D
    };
    var Wf = function(a) {
        var b = 0;
        a.B && b++;
        a.P && b++;
        return b
    },Vf = function(a) {
        if (!a.P && !a.Ca)a.Ca = yf(t(a.Qe, a), 0),a.hb = 0
    };
    X.prototype.Qe = function(a) {
        this.Ca = m;
        this.e.info("startForwardChannel_");
        if (this.f == 1)if (a)this.e.k("Not supposed to retry the open"); else {
            this.e.info("open_()");
            this.Nb = Math.floor(Math.random() * 1E5);
            var a = this.Nb++,b = new U(this, this.e, "", a, h);
            b.za(this.T);
            var c = Xf(this),d = this.kc.C();
            add_param(d, "RID", a);
            this.Db && add_param(d, "CVER", this.Db);
            Sf(this, d);
            mf(b, d, c);
            this.P = b;
            this.f = 2
        } else this.f == 3 && Yf(this) && (a ? Zf(this, a) : this.Q.length == 0 ? this.e.info("startForwardChannel_ returned: nothing to send") : this.P ? this.e.k("startForwardChannel_ returned: connection already in progress") :
                (Zf(this),this.e.info("startForwardChannel_ finished, sent request")))
    };
    var Zf = function(a, b) {
        var c,d;
        b ? a.cb > 6 ? (a.Q = a.pa.concat(a.Q),a.pa.length = 0,c = a.Nb - 1,d = Xf(a)) : (c = b.X,d = b.ya) : (c = a.Nb++,d = Xf(a));
        var e = a.kc.C();
        add_param(e, "SID", a.ma);
        add_param(e, "RID", c);
        add_param(e, "AID", a.zb);
        Sf(a, e);
        c = new U(a, a.e, a.ma, c, a.hb + 1);
        c.za(a.T);
        c.setTimeout(Math.round(1E4) + Math.round(1E4 * Math.random()));
        a.P = c;
        mf(c, e, d)
    },Sf = function(a, b) {
        if (a.u) {
            var c = a.u.eg(a);
            c && pc(c, function(a, c) {
                add_param(b, c, a)
            })
        }
    },Xf = function(a) {
        var b = Math.min(a.Q.length, 1E3),c = ["count=" + b],d;
        a.cb > 6 && b > 0 ? (d = a.Q[0].$f,c.push("ofs=" + d)) : d = 0;
        for (var e =
                0; e < b; e++) {
            var g = a.Q[e].$f,i = a.Q[e].map;
            a.cb <= 6 ? g = e : g -= d;
            try {
                pc(i, function(a, b) {
                    c.push("req" + g + "_" + b + "=" + encodeURIComponent(a))
                })
            } catch(j) {
                c.push("req" + g + "_type=" + encodeURIComponent("_badmap"))
            }
        }
        a.pa = a.pa.concat(a.Q.splice(0, b));
        return c.join("&")
    },$f = function(a) {
        if (!a.B && !a.oa)a.Ve = 1,a.oa = yf(t(a.Gf, a), 0),a.gb = 0
    },bg = function(a) {
        if (a.B || a.oa)return a.e.k("Request already in progress"),!1;
        if (a.gb >= 3)return!1;
        a.e.info("Going to retry GET");
        a.Ve++;
        a.oa = yf(t(a.Gf, a), ag(a, a.gb));
        a.gb++;
        return!0
    };
    X.prototype.Gf = function() {
        this.oa = m;
        if (Yf(this)) {
            this.e.info("Creating new HttpRequest");
            this.B = new U(this, this.e, this.ma, "rpc", this.Ve);
            this.B.za(this.T);
            var a = this.be.C();
            add_param(a, "RID", "rpc");
            add_param(a, "SID", this.ma);
            add_param(a, "CI", this.$c ? "0" : "1");
            add_param(a, "AID", this.zb);
            Sf(this, a);
            if (z) {
                add_param(a, "TYPE", "html");
                var b = this.B,c = Boolean(this.na);
                b.La = 3;
                b.Aa = add_zx_parameter(a.C());
                xf(b, c)
            } else add_param(a, "TYPE", "xmlhttp"),nf(this.B, a, !0, this.na, !1);
            this.e.info("New Request created")
        }
    };
    var Yf = function(a) {
        if (a.u) {
            var b = a.u.Qf(a);
            if (b != 0)return a.e.info("Handler returned error code from okToMakeRequest"),W(a, b),!1
        }
        return!0
    },Lf = function(a, b, c) {
        a.e.info("Test Connection Finished");
        a.$c = a.Xg && c;
        a.D = b.O();
        a.e.info("connectChannel_()");
        a.Yg(1, 0);
        a.kc = Hf(a, a.z);
        Vf(a)
    },Kf = function(a, b) {
        a.e.info("Test Connection Failed");
        a.D = b.O();
        W(a, 2)
    };
    X.prototype.xf = function(a, b) {
        if (!(this.f == 0 || this.B != a && this.P != a))if (this.D = a.O(),this.P == a && this.f == 3)if (this.cb > 7) {
            var c;
            try {
                c = dc(b)
            } catch(d) {
                c = m
            }
            if (q(c) && c.length == 3) {
                var e = c;
                if (e[0] == 0)a:if (this.e.info("Server claims our backchannel is missing."),this.oa)this.e.info("But we are currently starting the request."); else {
                    if (this.B)if (this.B.ab + 3E3 < this.P.ab)Uf(this),this.B.cancel(),this.B = m; else break a; else this.e.v("We do not have a BackChannel established");
                    bg(this);
                    V(19)
                } else if (this.je = e[1],
                        c = this.je - this.zb,0 < c && (e = e[2],this.e.info(e + " bytes (in " + c + " arrays) are outstanding on the BackChannel"),e < 37500 && this.$c && this.gb == 0 && !this.Sa))this.Sa = yf(t(this.sg, this), 6E3)
            } else this.e.info("Bad POST response data returned"),W(this, 11)
        } else b != "y2f%" && (this.e.info("Bad data returned - missing/invald magic cookie"),W(this, 11)); else if (this.B == a && Uf(this),!/^[\s\xa0]*$/.test(b)) {
            c = dc(b);
            for (var e = this.u && this.u.mc ? [] : m,g = 0; g < c.length; g++) {
                var i = c[g];
                this.zb = i[0];
                i = i[1];
                if (this.f == 2)i[0] == "c" ?
                        (this.ma = i[1],this.na = this.jc(i[2]),i = i[3],this.cb = i != m ? i : 6,this.f = 3,this.u && this.u.ie(this),this.be = Jf(this, this.na, this.z),$f(this)) : i[0] == "stop" && W(this, 7); else if (this.f == 3) {
                    if (i[0] == "stop") {
                        if (e && e.length)this.u.mc(this, e),e.length = 0;
                        W(this, 7)
                    } else i[0] != "noop" && e && e.push(i);
                    this.gb = 0
                }
            }
            e && e.length && this.u.mc(this, e)
        }
    };
    X.prototype.jc = function(a) {
        if (this.oh) {
            if (this.u)return this.u.jc(a);
            return a
        }
        return m
    };
    X.prototype.sg = function() {
        if (this.Sa != m)this.Sa = m,this.B.cancel(),this.B = m,bg(this),V(20)
    };
    var Uf = function(a) {
        if (a.Sa != m)p.clearTimeout(a.Sa),a.Sa = m
    };
    X.prototype.pc = function(a) {
        this.e.info("Request complete");
        var b;
        if (this.B == a)Uf(this),this.B = m,b = 2; else if (this.P == a)this.P = m,b = 1; else return;
        this.D = a.O();
        if (this.f != 0)if (a.ca)b == 1 ? (b = do_something() - a.ab,Of.dispatchEvent(new Qf(Of, a.ya ? a.ya.length : 0, b, this.hb)),Vf(this),this.pa.length = 0) : $f(this); else {
            var c = a.Re();
            if (c == 3 || c == 0 && this.D > 0)this.e.info("Not retrying due to error type"); else {
                this.e.info("Maybe retrying, last error: " + hf(c, this.D));
                var d;
                if (d = b == 1)this.P || this.Ca ? (this.e.k("Request already in progress"),
                        d = !1) : this.f == 1 || this.hb >= (this.Hg ? 0 : 2) ? d = !1 : (this.e.info("Going to retry POST"),this.Ca = yf(t(this.Qe, this, a), ag(this, this.hb)),this.hb++,d = !0);
                if (d)return;
                if (b == 2 && bg(this))return;
                this.e.info("Exceeded max number of retries")
            }
            this.e.info("Error: HTTP request failed");
            switch (c) {
                case 1:
                    W(this, 5);
                    break;
                case 4:
                    W(this, 10);
                    break;
                case 3:
                    W(this, 6);
                    break;
                default:
                    W(this, 2)
            }
        }
    };
    var ag = function(a, b) {
        var c = 5E3 + Math.floor(Math.random() * 1E4);
        a.Ua() || (a.e.info("Inactive channel"),c *= 2);
        c *= b;
        return c
    };
    X.prototype.Yg = function() {
        Da(arguments, this.f) >= 0 || f(Error("Unexpected channel state: " + this.f))
    };
    var W = function(a, b) {
        a.e.info("Error code " + b);
        if (b == 2 || b == 9) {
            var c = m;
            a.u && (c = a.u.Nf(a));
            var d = t(a.fh, a);
            c || (c = new N("//www.google.com/images/cleardot.gif"),add_zx_parameter(c));
            Df(c.toString(), 1E4, d)
        } else V(2);
        a.Ec(b)
    };
    X.prototype.fh = function(a) {
        a ? (this.e.info("Successfully pinged google.com"),V(2)) : (this.e.info("Failed to ping google.com"),V(1),this.Ec(8))
    };
    X.prototype.Ec = function(a) {
        this.e.info("HttpChannel: error - " + a);
        this.f = 0;
        this.u && this.u.Ef(this, a);
        Tf(this);
        Rf(this)
    };
    var Tf = function(a) {
        a.f = 0;
        a.D = -1;
        if (a.u)if (a.pa.length == 0 && a.Q.length == 0)a.u.Cd(a); else {
            a.e.info("Number of undelivered maps, pending: " + a.pa.length + ", outgoing: " + a.Q.length);
            var b = Ha(a.pa),c = Ha(a.Q);
            a.pa.length = 0;
            a.Q.length = 0;
            a.u.Cd(a, b, c)
        }
    },Hf = function(a, b) {
        var c = Mf(a, m, b);
        a.e.info("GetForwardChannelUri: " + c);
        return c
    },Jf = function(a, b, c) {
        b = Mf(a, a.vc() ? b : m, c);
        a.e.info("GetBackChannelUri: " + b);
        return b
    },Mf = function(a, b, c) {
        var d = window.location,e = dd(d.protocol, m, b ? b + "." + d.hostname : d.hostname, d.port,
                c);
        a.ac && pc(a.ac, function(a, b) {
            add_param(e, b, a)
        });
        add_param(e, "VER", a.cb);
        Sf(a, e);
        return e
    };
    X.prototype.sd = function(a) {
        if (a)f(Error("Can't create secondary domain capable XhrIo object.")); else return new T
    };
    X.prototype.Ua = function() {
        return!!this.u && this.u.Ua(this)
    };
    var yf = function(a, b) {
        fa(a) || f(Error("Fn must not be null and must be a function"));
        return p.setTimeout(function() {
            a()
        }, b)
    },V = function(a) {
        Of.dispatchEvent(new Pf(Of, a))
    };
    X.prototype.vc = function() {
        return z
    };
    var cg = function() {
    };
    n = cg.prototype;
    n.mc = m;
    n.Qf = function() {
        return 0
    };
    n.ie = function() {
    };
    n.Ef = function() {
    };
    n.Cd = function() {
    };
    n.eg = function() {
        return{}
    };
    n.Nf = function() {
        return m
    };
    n.Ua = function() {
        return!0
    };
    n.jc = function(a) {
        return a
    };
    var dg = function() {
        this.Ia = []
    };
    dg.prototype.wa = 0;
    dg.prototype.Ha = 0;
    var eg = function(a) {
        if (a.wa != a.Ha) {
            var b = a.Ia[a.wa];
            delete a.Ia[a.wa];
            a.wa++;
            return b
        }
    };
    n = dg.prototype;
    n.Fb = function() {
        return this.Ha - this.wa
    };
    n.Hb = function() {
        return this.Ha - this.wa == 0
    };
    n.clear = function() {
        this.Ha = this.wa = this.Ia.length = 0
    };
    n.remove = function(a) {
        a = Da(this.Ia, a);
        if (a < 0)return!1;
        if (a == this.wa)eg(this); else {
            var b = this.Ia;
            Ba(b.length != m);
            y.splice.call(b, a, 1);
            this.Ha--
        }
        return!0
    };
    n.ua = function() {
        return this.Ia.slice(this.wa, this.Ha)
    };
    var Y = function(a, b, c, d, e, g) {
        this.w = a;
        this.talkserver_url = b;
        this.qe = d || m;
        this.Bb = new dg;
        this.Ib = new dg;
        this.ke = e || m;
        this.e = m;
        this.Db = c;
        this.f = -1;
        this.l = 0;
        this.b = this.bb(this.Db);
        this.Cg = !!g;
        this.nc = new cf("BrowserChannel heartbeat", 1E3);
        F(this.nc, "tick", this.le, !0, this);
        this.nc.start();
        this.Oa = 5E3 + Math.random() * 2E4
    };
    x(Y, cg);
    n = Y.prototype;
    n.g = M("fava.net.BrowserChannelWrapper");
    n.yd = m;
    n.Zc = 0;
    n.zc = !1;
    n.Lc = [];
    n.G = function() {
        Xb(this.nc, "tick", this.le, !0, this);
        this.f != -1 && this.b.rc();
        this.f = 1;
        this.Bb.clear();
        fg(this);
        gg(this);
        this.nc.G()
    };
    n.Ga = function() {
        if (this.Wb)return 4;
        return this.f
    };
    n.Jd = function() {
        return this.yd
    };
    n.mc = function(a, b) {
        if (a == this.b) {
            for (var c = 0; c < b.length; c++) {
                var d = this.Bb,e = b[c];
                d.Ia[d.Ha++] = e
            }
            this.ce()
        }
    };
    n.ce = function() {
        gg(this);
        for (var a = do_something(),b = []; !this.Bb.Hb();) {
            var c = eg(this.Bb),d = do_something(),e = c,c = e[0],g;
            g = Ve;
            var i = do_something(),j = Te(g),k = g.Da.Fb();
            if (g.N.length + k > g.nd) {
                g.g.v("Giant thread trace. Clearing to avoid memory leak.");
                if (g.N.length > g.nd / 2) {
                    for (var l = 0; l < g.N.length; l++) {
                        var o = g.N[l];
                        o.id && D(g.ib, o.id);
                        D(g.Ra, o)
                    }
                    g.N.length = 0
                }
                k > g.nd / 2 && g.Da.clear()
            }
            g.uc("Start : BrowserChannelServices.handleArray_");
            Ue("Start : BrowserChannelServices.handleArray_");
            o = g.Ra.getObject();
            o.Qb = j;
            o.Ob = 0;
            o.id = Number(g.ib.getObject());
            o.Rb = "BrowserChannelServices.handleArray_";
            o.type = h;
            g.N.push(o);
            g.Da.set(String(o.id), o);
            g.bd++;
            j = do_something();
            o.startTime = o.qc = j;
            g.dd += j - i;
            g = o.id;
            if (e.length <= 0)this.g.v("Got empty array"); else if (this.f == 3 && e[0] == "b")hg(this, 4); else if (this.f == 4)try {
                var v = this.w.Ab.get(e[0]);
                if (v && q(e[1])) {
                    var H = e[1];
                    v.dispatchEvent(new ig(H));
                    c += "-" + H[0]
                } else this.g.v("Unexpected response array: " + e)
            } catch(K) {
                this.g.k("Error handling array", K)
            }
            o = g;
            e = Ve;
            g = do_something();
            k = h;
            k = e.he;
            i = e.Da.get(String(o));
            if (i != m) {
                e.Da.remove(String(o));
                o = h;
                j = g - i.startTime;
                if (j < k)for (k = e.N.length - 1; k >= 0; k--) {
                    if (e.N[k] == i) {
                        e.N.splice(k, 1);
                        D(e.ib, i.id);
                        D(e.Ra, i);
                        break
                    }
                } else o = e.Ra.getObject(),o.Ob = 1,o.startTime = i.startTime,o.Rb = i.Rb,o.type = i.type,o.Dg = o.qc = g,e.N.push(o);
                k = i.type;
                l = m;
                if (k) {
                    l = e.Pa.get(k);
                    if (!l)l = e.fd.getObject(),l.type = k,e.Pa.set(k, l);
                    l.count++;
                    l.jd += j
                }
                if (o)j = "Stop : " + o.Rb,e.uc(j),Ue(j),o.Qb = Te(e),l && (l.oc += o.Qb - i.Qb);
                e.cd += do_something() - g
            }
            e = do_something();
            b.push([c + ":" + (e - d)]);
            if (e - a > 500) {
                this.g.v("Took too long handling arrays: " + wa(b.join(",")));
                break
            }
        }
        if (!this.Bb.Hb())this.g.info("Delaying array handling"),
                this.od = ff("fava.net.BrowserChannelWrapper", this.ce, 0, this)
    };
    n.Qf = function() {
        return 0
    };
    n.ie = function(a) {
        if (a == this.b)this.Oa = 5E3 + Math.random() * 2E4,hg(this, 3)
    };
    n.Ef = function(a, b) {
        if (a == this.b) {
            this.Wb = !1;
            if (b == 4)this.l = 1; else if (b == 2)this.l = 2; else if (b == 6)if (this.Cg) {
                if (this.f == 4 && !jg(this, !0))this.Wb = !0;
                this.l = 0;
                this.zc = !0
            } else this.l = 2; else if (b == 8)this.l = 3; else if (b == 7)this.l = 2; else if (b == 9)this.l = 4;
            jg(this, !0);
            hg(this, 5)
        }
    };
    n.Cd = function(a, b, c) {
        if (a == this.b && this.f != 5 && this.f != 6 && (this.Wb = !1,hg(this, 1),b || c))this.w.dispatchEvent(new kg(b || m, c || m))
    };
    n.eg = function(a) {
        if (a != this.b)return{};
        for (var b = {},a = 0; a < this.Lc.length; a++)mb(b, this.Lc[a].eb);
        return b
    };
    n.Nf = function(a) {
        if (a != this.b)return m;
        if (this.qe)return a = new N(this.qe),add_zx_parameter(a),a;
        return m
    };
    n.Ua = function() {
        return!0
    };
    var BrowserChannelServices.Channel = function(a) {
        fg(a);
        a.talkserver_url || f(Error("BrowserChannelServices.Channel: base path not set"));
        var test_url = a.talkserver_url + "test",bind_url = a.talkserver_url + "bind";
        if (a.f != -1) {
            (a.b.Ga() == 3 || Wf(a.b) != 0) && a.g.k("BrowserChannelServices.Channel: unexpected reconnect state: " + a.b.Ga());
            var d = a.b.xc(),e = a.b.zb;
            a.b = a.bb(a.Db);
            a.b.initbind(test_url, bind_url, {}, d, e)
        } else a.b.initbind(test_url, bind_url, {});
        hg(a, 2)
    };
    Y.prototype.lb = function() {
        switch (this.Ga()) {
            case -1:
            case 2:
            case 3:
            case 4:
                return!0;
            default:
                return this.Kc != m
        }
    };
    Y.prototype.Ea = function(a, b) {
        this.lb() || f(Error("BrowserChannelServices: Trying to send a map while we are disconnected: " + a.type));
        var c = b || 1;
        if (a != m) {
            var d = this.Ib;
            d.Ia[d.Ha++] = a;
            this.Ib.Fb() >= 5E3 && (this.g.v("Hit max queue size. Dropping BC message."),eg(this.Ib))
        }
        if (this.f == 4 && c == 1)for (; !this.Ib.Hb();)this.b.Ea(eg(this.Ib))
    };
    var hg = function(a, b) {
        var c = a.f;
        if (b == 5)c != 5 && mg(a),a.f = b; else if (c != b)switch (a.f = b,b) {
            case 4:
                a.l = 0,a.Wb = !1,a.Ea(m),a.w.dispatchEvent("d")
        } else return;
        a.Wb || a.w.dispatchEvent(new ng(c, b, a.l))
    };
    Y.prototype.bb = function(a) {
        a = this.ke ? this.ke(a) : new X(a);
        this.e && this.qb(this.e);
        a.u = this;
        return a
    };
    var fg = function(a) {
        if (a.Kc != m)ne.clearTimeout(a.Kc),a.Kc = m
    },gg = function(a) {
        if (a.od != m)ne.clearTimeout(a.od),a.od = m
    },mg = function(a) {
        if (a.l != 1 && a.l != 4) {
            !a.zc && a.Oa * 2 < 24E4 && (a.Oa *= 2);
            if (a.zc)a.Oa = 500;
            a.g.info("Retrying connection in " + a.Oa + "ms");
            a.yd = do_something() + a.Oa;
            fg(a);
            a.Kc = ff("fava.net.BrowserChannelServices", a.gh, a.Oa, a)
        }
    };
    Y.prototype.gh = function() {
        this.yd = m;
        if (this.f == 1 || this.f == 5 || this.f == 6)this.zc = !1,this.b && Wf(this.b) == 0 ? BrowserChannelServices.Channel(this) : mg(this)
    };
    Y.prototype.le = function() {
        if (!jg(this, !1))this.Zc = do_something()
    };
    var jg = function(a, b) {
        var c = do_something(),d = a.Zc > 0 && c - a.Zc > 3E4;
        if (b)a.Zc = c;
        return d
    };
    Y.prototype.hd = function(a) {
        var b = this.Lc;
        Da(b, a) >= 0 || b.push(a)
    };
    Y.prototype.Ld = function(a) {
        Fa(this.Lc, a)
    };
    Y.prototype.qb = function(a) {
        this.e = a;
        this.b && (a ? this.b.qb(a) : this.b.qb(new Bf))
    };
    var og = function(a, b, c, d, e) {
        this.Ab = new G;
        this.$ = new Y(this, a, b, c, d, e)
    };
    x(og, me);
    var pg = function(a, b) {
        this.La = b;
        this.w = a
    };
    x(pg, me);
    var ig = function(a) {
        B.call(this, "b");
        this.Zg = a
    };
    x(ig, B);
    pg.prototype.fg = function() {
        return this.La
    };
    pg.prototype.lb = function() {
        return this.w.lb()
    };
    pg.prototype.Ea = function(a, b) {
        this.w.Ea(this, a, b)
    };
    var ng = function(a, b, c) {
        B.call(this, "c");
        this.Kh = a;
        this.$g = b;
        this.error = c
    };
    x(ng, B);
    var kg = function(a, b) {
        B.call(this, "e");
        this.Lh = a;
        this.Oh = b
    };
    x(kg, B);
    n = og.prototype;
    n.g = M("fava.net.BrowserChannelServices");
    n.h = function() {
        og.H.h.call(this);
        this.$.G();
        for (var a = this.Ab.ua(),b = 0; b < a.length; b++)a[b].G();
        this.Ab.clear()
    };
    n.hd = function(a) {
        this.$.hd(a)
    };
    n.Ld = function(a) {
        this.$.Ld(a)
    };
    n.initbind = function() {
        this.Ga() == -1 && BrowserChannelServices.Channel(this.$)
    };
    n.rc = function() {
        this.$.b.rc()
    };
    n.xc = function() {
        return this.$.b.xc()
    };
    n.lb = function() {
        return this.$.lb()
    };
    n.Ea = function(a, b, c) {
        "_sc"in b && f(Error("sendMap called with reserved key: _sc"));
        b._sc = a.fg();
        this.$.Ea(b, c)
    };
    n.Ga = function() {
        return this.$.Ga()
    };
    n.Jd = function() {
        return this.$.Jd()
    };
    n.qb = function(a) {
        this.$.qb(a)
    };
    n.O = function() {
        return this.$.b.O()
    };
    T.send = function(a, b, c, d, e, g) {
        var i = new T;
        Ee.push(i);
        b && F(i, "complete", b);
        F(i, "ready", la(Fe, i));
        if (g)i.Vb = Math.max(0, g);
        i.send(a, c, d, e)
    };
    T.Sh = function() {
        for (; Ee.length;)Ee.pop().G()
    };
    T.Wh = function(a) {
        T.prototype.Yd = a.Jh(T.prototype.Yd)
    };
    T.Th = Fe;
    T.Qh = "Content-Type";
    T.Rh = "application/x-www-form-urlencoded;charset=utf-8";
    T.Xh = Ee;
    var Z = function() {
    };
    Z.prototype.da = function() {
    };
    Z.prototype.toString = function() {
        return this.a.toString()
    };
    var qg = function(a) {
        this.a = a || ["p"]
    };
    x(qg, Z);
    n = qg.prototype;
    n.da = function() {
        return"p"
    };
    n.L = function() {
        return this.a[1]
    };
    n.ta = function(a) {
        this.a[1] = a
    };
    n.gf = function() {
        return this.a[3]
    };
    n.kf = function(a) {
        this.a[3] = a
    };
    n.xa = function() {
        return this.a[4]
    };
    n.lf = function(a) {
        this.a[4] = a
    };
    n.ff = function() {
        return this.a[5]
    };
    n.jf = function(a) {
        this.a[5] = a
    };
    n.ef = function() {
        return this.a[6]
    };
    n.hf = function(a) {
        this.a[6] = a
    };
    var rg = function(a) {
        this.a = a || ["ru"];
        this.a[15] = this.a[15] || []
    };
    x(rg, Z);
    n = rg.prototype;
    n.da = function() {
        return"ru"
    };
    n.L = function() {
        return this.a[1]
    };
    n.ta = function(a) {
        this.a[1] = a
    };
    n.Lb = function() {
        return this.a[3]
    };
    n.He = function(a) {
        this.a[3] = a
    };
    n.se = function() {
        return this.a[4]
    };
    n.De = function(a) {
        this.a[4] = a
    };
    n.ve = function() {
        return this.a[5]
    };
    n.Ge = function(a) {
        this.a[5] = a
    };
    n.ue = function() {
        return this.a[6]
    };
    n.Fe = function(a) {
        this.a[6] = a
    };
    n.we = function() {
        return this.a[7]
    };
    n.Ie = function(a) {
        this.a[7] = a
    };
    n.xe = function() {
        return this.a[8]
    };
    n.Je = function(a) {
        this.a[8] = a
    };
    n.Ae = function() {
        return this.a[9]
    };
    n.Me = function(a) {
        this.a[9] = a
    };
    n.ze = function() {
        return this.a[10]
    };
    n.Le = function(a) {
        this.a[10] = a
    };
    n.Be = function() {
        return this.a[11]
    };
    n.Ne = function(a) {
        this.a[11] = a
    };
    n.Ce = function() {
        return this.a[12]
    };
    n.Oe = function(a) {
        this.a[12] = a
    };
    n.gd = function() {
        return this.a[13]
    };
    n.Pe = function(a) {
        this.a[13] = a
    };
    n.te = function() {
        return this.a[14]
    };
    n.Ee = function(a) {
        this.a[14] = a
    };
    n.ye = function() {
        return this.a[15]
    };
    n.Ke = function(a) {
        a = a || [];
        this.a[15] = a
    };
    var sg = function(a) {
        this.a = a || ["vc"]
    };
    x(sg, Z);
    n = sg.prototype;
    n.da = function() {
        return"vc"
    };
    n.L = function() {
        return this.a[1]
    };
    n.ta = function(a) {
        this.a[1] = a
    };
    n.getName = function() {
        return this.a[2]
    };
    n.rd = function(a) {
        this.a[2] = a
    };
    n.pd = function() {
        return this.a[3]
    };
    n.qd = function(a) {
        this.a[3] = a
    };
    var ug = function(a) {
        this.a = a || ["nqr"];
        this.a[5] = this.a[5] || [];
        this.Zb = [];
        for (a = 0; a < this.a[5].length; a++)this.Zb[a] = new tg(this.a[5][a])
    };
    x(ug, Z);
    n = ug.prototype;
    n.da = function() {
        return"nqr"
    };
    n.xd = function() {
        return this.a[1]
    };
    n.Cb = function(a) {
        this.a[1] = a
    };
    n.Ze = function() {
        return this.a[2]
    };
    n.setStart = function(a) {
        this.a[2] = a
    };
    n.We = function() {
        return this.a[3]
    };
    n.setEnd = function(a) {
        this.a[3] = a
    };
    n.Ye = function() {
        return this.a[4]
    };
    n.bf = function(a) {
        this.a[4] = a
    };
    n.Ac = function() {
        return this.Zb
    };
    var tg = function(a) {
        this.a = a || [];
        this.a[1] = this.a[1] || [];
        if (this.a[2])this.wf = new qg(this.a[2]);
        this.Ig = new rg(this.a[3]);
        this.Jg = new sg(this.a[4])
    };
    x(tg, Z);
    n = tg.prototype;
    n.L = function() {
        return this.a[0]
    };
    n.ta = function(a) {
        this.a[0] = a
    };
    n.Xe = function() {
        return this.a[1]
    };
    n.$e = function(a) {
        a = a || [];
        this.a[1] = a
    };
    n.wd = function() {
        return this.wf
    };
    n.af = function(a) {
        this.wf = a;
        this.a[2] = a ? a.a : a
    };
    var wg = function(a) {
        this.a = a || ["otr"];
        this.a[1] = this.a[1] || [];
        this.vd = [];
        for (a = 0; a < this.a[1].length; a++)this.vd[a] = new vg(this.a[1][a])
    };
    x(wg, Z);
    wg.prototype.da = function() {
        return"otr"
    };
    var vg = function(a) {
        this.a = a || []
    };
    x(vg, Z);
    vg.prototype.L = function() {
        return this.a[0]
    };
    vg.prototype.ta = function(a) {
        this.a[0] = a
    };
    var xg = function(a) {
        this.a = a || ["p"]
    };
    x(xg, Z);
    n = xg.prototype;
    n.da = function() {
        return"p"
    };
    n.L = function() {
        return this.a[1]
    };
    n.ta = function(a) {
        this.a[1] = a
    };
    n.gf = function() {
        return this.a[2]
    };
    n.kf = function(a) {
        this.a[2] = a
    };
    n.xa = function() {
        return this.a[3]
    };
    n.lf = function(a) {
        this.a[3] = a
    };
    n.ff = function() {
        return this.a[4]
    };
    n.jf = function(a) {
        this.a[4] = a
    };
    n.ef = function() {
        return this.a[5]
    };
    n.hf = function(a) {
        this.a[5] = a
    };
    var yg = function(a) {
        this.a = a || ["m"]
    };
    x(yg, Z);
    yg.prototype.da = function() {
        return"m"
    };
    yg.prototype.L = function() {
        return this.a[1]
    };
    yg.prototype.ta = function(a) {
        this.a[1] = a
    };
    var zg = function(a) {
        this.a = a || ["ra"];
        this.a[18] = this.a[18] || []
    };
    x(zg, Z);
    n = zg.prototype;
    n.da = function() {
        return"ra"
    };
    n.L = function() {
        return this.a[1]
    };
    n.ta = function(a) {
        this.a[1] = a
    };
    n.getName = function() {
        return this.a[2]
    };
    n.rd = function(a) {
        this.a[2] = a
    };
    n.Lb = function() {
        return this.a[3]
    };
    n.He = function(a) {
        this.a[3] = a
    };
    n.pd = function() {
        return this.a[4]
    };
    n.qd = function(a) {
        this.a[4] = a
    };
    n.se = function() {
        return this.a[5]
    };
    n.De = function(a) {
        this.a[5] = a
    };
    n.ve = function() {
        return this.a[6]
    };
    n.Ge = function(a) {
        this.a[6] = a
    };
    n.ue = function() {
        return this.a[7]
    };
    n.Fe = function(a) {
        this.a[7] = a
    };
    n.we = function() {
        return this.a[8]
    };
    n.Ie = function(a) {
        this.a[8] = a
    };
    n.xe = function() {
        return this.a[9]
    };
    n.Je = function(a) {
        this.a[9] = a
    };
    n.Ae = function() {
        return this.a[12]
    };
    n.Me = function(a) {
        this.a[12] = a
    };
    n.ze = function() {
        return this.a[13]
    };
    n.Le = function(a) {
        this.a[13] = a
    };
    n.Be = function() {
        return this.a[14]
    };
    n.Ne = function(a) {
        this.a[14] = a
    };
    n.Ce = function() {
        return this.a[15]
    };
    n.Oe = function(a) {
        this.a[15] = a
    };
    n.gd = function() {
        return this.a[16]
    };
    n.Pe = function(a) {
        this.a[16] = a
    };
    n.te = function() {
        return this.a[17]
    };
    n.Ee = function(a) {
        this.a[17] = a
    };
    n.ye = function() {
        return this.a[18]
    };
    n.Ke = function(a) {
        a = a || [];
        this.a[18] = a
    };
    var Bg = function(a) {
        this.a = a || ["qr"];
        this.a[5] = this.a[5] || [];
        this.Zb = [];
        for (a = 0; a < this.a[5].length; a++)this.Zb[a] = new Ag(this.a[5][a])
    };
    x(Bg, Z);
    n = Bg.prototype;
    n.da = function() {
        return"qr"
    };
    n.xd = function() {
        return this.a[1]
    };
    n.Cb = function(a) {
        this.a[1] = a
    };
    n.Ze = function() {
        return this.a[2]
    };
    n.setStart = function(a) {
        this.a[2] = a
    };
    n.We = function() {
        return this.a[3]
    };
    n.setEnd = function(a) {
        this.a[3] = a
    };
    n.Ye = function() {
        return this.a[4]
    };
    n.bf = function(a) {
        this.a[4] = a
    };
    n.Ac = function() {
        return this.Zb
    };
    var Ag = function(a) {
        this.a = a || ["c"];
        this.a[1] = this.a[1] || [];
        this.Kg = new zg(this.a[2])
    };
    x(Ag, Z);
    n = Ag.prototype;
    n.da = function() {
        return"c"
    };
    n.Xe = function() {
        return this.a[1]
    };
    n.$e = function(a) {
        a = a || [];
        this.a[1] = a
    };
    n.wd = function() {
        return this.a[4]
    };
    n.af = function(a) {
        this.a[4] = a
    };
    var Cg = function() {
        this.jg = new G;
        this.md = new G
    },Dg = function(a) {
        this.wh = a
    };
    Dg.prototype.getName = function() {
        return this.Fg || this.Mg || this.Eg || this.wh
    };
    Cg.prototype.translate = function(a) {
        switch (a[0]) {
            case "nqr":
                var a = new ug(a),b = new Bg;
                b.Cb(a.xd());
                b.setStart(a.Ze());
                b.setEnd(a.We());
                b.bf(a.Ye());
                if (a.Ac().length > 0) {
                    for (var c = 0; c < a.Ac().length; ++c) {
                        var d = a.Ac()[c],e = new Ag;
                        e.$e(d.Xe());
                        Eg(this, d.Ig);
                        Fg(this, d.Jg);
                        var g = Gg(this, d.L()),i = e,j = g;
                        i.Kg = j;
                        i.a[2] = j ? j.a : j;
                        e.a[3] = g.gd();
                        d.wd() && e.af(Hg(d.wd())[0]);
                        b.a[c + 5] = e.a
                    }
                    a = [b.a]
                } else a = [b.a.slice(0, 5)];
                return a;
            case "otr":
                a = new wg(a);
                b = [];
                for (c = 0; c < a.vd.length; ++c)d = a.vd[c],e = Gg(this, d.L()),e.Lb() &&
                        e.Lb().length > 0 && b.push(e.a),e.a[10] = d.a[1],e.a[11] = d.a[2];
                return b;
            case "p":
                return Hg(new qg(a));
            case "ru":
                return Eg(this, new rg(a));
            case "vc":
                return Fg(this, new sg(a));
            default:
                return[a]
        }
    };
    var Gg = function(a, b) {
        var c = a.jg.get(b);
        c || (c = new zg,c.ta(b),a.jg.set(b, c),a.md.set(b, new Dg(b)));
        return c
    },Hg = function(a) {
        var b = new xg,c = a.L(),d = c.indexOf("/");
        d > 0 && (c = c.substring(0, d));
        b.ta(c);
        switch (a.gf()) {
            case 1:
                c = "u";
                break;
            case 2:
            case 3:
                c = "i";
                break;
            case 4:
                c = "b";
                break;
            default:
                c = "a"
        }
        b.kf(c);
        b.lf(a.xa() || "");
        b.jf(a.ff());
        b.hf(a.ef());
        return[b.a]
    },Eg = function(a, b) {
        var c = Gg(a, b.L()),d = a.md.get(b.L());
        d.Fg = b.a[2];
        d.Eg = b.a[16];
        d.Fh = b.a[17];
        c.rd(d.getName());
        c.He(b.Lb() || b.L());
        c.qd(c.pd() || "/image?h=7b8ac4c3c5b468f9ceabd8eea8a9df61574ad997");
        c.De(b.se());
        c.Ge(b.ve());
        c.Fe(b.ue());
        c.Ie(b.we());
        d = "N";
        switch (b.xe()) {
            case 1:
                d = "B";
                break;
            case 2:
                d = "H";
                break;
            case 3:
                d = "N";
                break;
            case 4:
                d = "P"
        }
        c.Je(d);
        c.a[10] = c.a[10] || 0;
        c.a[11] = c.a[11] || 0;
        c.Me(b.Ae() || "");
        c.Le(b.ze() || "");
        c.Ne(b.Be());
        c.Oe(b.Ce());
        c.Pe(b.gd());
        c.Ee(b.te());
        c.Ke(b.ye());
        return[c.a]
    },Fg = function(a, b) {
        var c = Gg(a, b.L()),d = a.md.get(b.L());
        d.Mg = b.getName();
        c.rd(d.getName());
        c.qd("/image?h=" + b.pd());
        return c.Lb() ? [c.a] : []
    };
    var wight_gsession = function(a, b, clid, gsession_id, e, g, i, j, k, l, o, v, H, K) {
        this.u = h;
        this.ug = new N(a);
        this.vg = o || "channel";
        this.Ch = b;
        this.fe = clid;
        this.Ba = e;
        this.ne = g;
        this.me = H ? H : 0;
        this.Ag = j || "wcs";
        this.g = M("chat.WcsClient");
        sc(Mc(this.g));
        this.Dh = [];
        this.Eh = !1;
        this.eb = {};
        kb(this.eb, "clid", clid);
        kb(this.eb, "gsessionid", gsession_id);
        kb(this.eb, "prop", this.Ag);
        this.me != 0 && kb(this.eb, "authuser", this.me);
        K && mb(this.eb, K);
        af(this, window, "unload", this.G, !0);
        this.W = !1;
        this.wg = {};
        for (a = 0; a < 256; ++a)b = a.toString(16),b.length == 1 && (b = "0" + b),b = "%" + b,this.wg[unescape(b)] =
                a;
        this.oe = Ig(this);
        this.Kb = new oe(5E3);
        $e(this, this.Kb, "tick", this.yg, !1, this);
        this.Kb.start();
        if (this.qa = l && l > 0 ? new oe(l) : m)$e(this, this.qa, "tick", this.Bg, !1, this),this.qa.start();
        this.de = !1;
        this.rg = new Cg;
        if (l = k)l = k.Bh("d") !== m;
        if (l)this.w = k.get("d"); else {
            this.de = !0;
            l = this.ug;
            k = this.vg + "/";
            l instanceof N || (l = ld(l));
            k instanceof N || (k = ld(k));
            b = l;
            l = b.C();
            (a = !!k.K) ? Rc(l, k.K) : a = !!k.Na;
            a ? Sc(l, k.Na) : a = !!k.ia;
            a ? Tc(l, k.ia) : a = k.ja != m;
            clid = k.z;
            if (a)Uc(l, k.ja); else if (a = !!k.z)if (clid.charAt(0) != "/" && (b.ia && !b.z ?
                    clid = "/" + clid : (b = l.z.lastIndexOf("/"),b != -1 && (clid = l.z.substr(0, b + 1) + clid))),clid == ".." || clid == ".")clid = ""; else if (!(clid.indexOf("./") == -1 && clid.indexOf("/.") == -1)) {
                b = clid.lastIndexOf("/", 0) == 0;
                clid = clid.split("/");
                gsession_id = [];
                for (e = 0; e < clid.length;)g = clid[e++],g == "." ? b && e == clid.length && gsession_id.push("") : g == ".." ? ((gsession_id.length > 1 || gsession_id.length == 1 && gsession_id[0] != "") && gsession_id.pop(),b && e == clid.length && gsession_id.push("")) : (gsession_id.push(g),b = !0);
                clid = gsession_id.join("/")
            }
            a ? Vc(l, clid) : a = k.J.toString() !== "";
            a ? l.Cb(gd(k)) : a = !!k.Ma;
            a && Xc(l, k.Ma);
            this.w = new og(l.z, "1")
        }
        this.w.hd(this);
        k = this.w;
        l = k.Ab.get("c");
        l || (l = new pg(k,
                "c"),k.Ab.set("c", l));
        this.ed = l;
        $e(this, this.w, "c", this.xg, !0, this);
        $e(this, this.ed, "b", this.zg, !0, this);
        v && Jg(this, ["imq"])
    };
    x(wight_gsession, We);
    wight_gsession.prototype.h = function() {
        wight_gsession.H.h.call(this);
        this.w.Ld(this);
        this.de && this.w.G();
        if (this.Kb)this.Kb.G(),this.Kb = m;
        if (this.qa)this.qa.G(),this.qa = m;
        p.onerror = m
    };
    wight_gsession.prototype.Xb = function() {
    };
    wight_gsession.prototype.Ed = function(a, b) {
        b()
    };
    var Ig = function(a, b) {
        var c;
        if (b)c = b + "="; else {
            if (a.ne == "WCX" && (c = Ig(a, "WCM"),c != m))return c;
            c = a.ne + "="
        }
        for (var d = document.cookie.split(";"),e = 0; e < d.length; ++e) {
            var g = d[e],i = g.indexOf(c);
            if (i > -1)return g.substring(i + c.length)
        }
        return m
    };
    wight_gsession.prototype.yg = function() {
        var a = Ig(this);
        if (this.oe != a)this.oe = a
    };
    wight_gsession.prototype.Bg = function() {
        this.w.Ga() == 4 && Jg(this, ["noop"])
    };
    wight_gsession.prototype.pf = function(a) {
        (window.parent === window.self || !Kg(this, window.parent, a)) && Kg(this, window.self, a)
    };
    var Kg = function(a, b, c) {
        try {
            var d = "" + b.location;
            if (d) {
                var e = new N(d);
                add_param(e, "v", a.Ba);
                c ? add_param(e, "clid", a.fe) : e.J.remove("clid");
                a.g.info("Reloading:  " + e.toString());
                b.location = e.toString();
                return!0
            }
        } catch(g) {
        }
        return!1
    },Jg = function(a, b) {
        if (b == m || !q(b))a.g.k("sending invalid array: " + b); else {
            var c;
            a:switch (b[0]) {
                case "m":
                    c = new yg(b);
                    break a;
                default:
                    c = m
            }
            if (c)a:{
                var d;
                try {
                    var e = c.a.slice(1);
                    d = gc(e)
                } catch(g) {
                    a.g.k("error serializing message: " + c.a);
                    break a
                }
                Lg(a, {t:c.da(),p:d})
            } else {
                var i;
                try {
                    i = gc(b)
                } catch(j) {
                    a.g.k("error serializing array: " +
                            b);
                    return
                }
                Lg(a, {m:i})
            }
        }
    },Lg = function(a, b) {
        var c = a.fe;
        b.c = c;
        a.ed.lb() ? (a.ed.Ea(b),a.qa && (a.qa.stop(),a.qa.start())) : a.g.v("Cannot send message: " + c + ": " + b)
    };
    wight_gsession.prototype.bb = function() {
        this.g.info("Connecting browser channel.");
        this.w.initbind()
    };
    wight_gsession.prototype.xg = function(a) {
        switch (a.$g) {
            case 4:
                this.g.info("Browser channel opened");
                this.Xb(["connect-state","open"]);
                Jg(this, ["connect-add-client"]);
                break;
            case 1:
                this.g.v("Browser channel closed");
                this.Xb(["connect-state","close"]);
                this.W = !1;
                break;
            case 5:
                var b = this.w.Jd();
                if (b !== m)this.g.info("Browser channel error state: " + a.error + ". Retry @ " + b),this.Xb(["connect-state","error",b]),this.W = !1,this.w.O() == 401 && this.Ed(!1, t(this.pf, this, !1))
        }
    };
    wight_gsession.prototype.zg = function(a) {
        a = a.Zg;
        if (a.length != 2)this.g.k("Array from server is not length 2: " + a); else if (a[1][0] == "v")this.g.info("Received version: " + a[1]),this.Ba != a[1][1] && this.Ed(!0, t(this.pf, this, !0)); else {
            if (a[1][0] == "d")this.g.info("Received graceful disconnect"),this.w.rc(),this.W = !1;
            if (a[1][0] == "pu")this.W = !0;
            for (var b = this.rg.translate(a[1]),c = 0; c < b.length; ++c)try {
                this.Xb(["connect-data",a[0],b[c]])
            } catch(d) {
                var e = d,g = tc(e);
                e.stack != m && window.console != m && window.console.error != m && window.console.error(e.stack);
                String(g.fileName).split(/[\/\\]/).pop()
            }
        }
    };
    var WcsDataClient = function(a, b, c, d, e, g, i, j, k, l) {
        wight_gsession.call(this, a, b, c, d, e, g, 0, "data", h, h, "dch", !1, h, {token:i});
        this.bc = [];
        this.$b = l || new ie(i);
        this.S = m;
        k ? this.S = k : (a = new N(window.location.href),a = cc(a.J.get("xpc")),this.S = new S(a));
        this.S.initbind(t(this.Pd, this));
        this.Pb || this.bb()
    };
    x(WcsDataClient, wight_gsession);
    WcsDataClient.prototype.Pd = function() {
        for (var a = 0; a < this.bc.length; ++a)this.S.send(this.bc[a].message, this.bc[a].data);
        this.bc = []
    };
    WcsDataClient.prototype.Xb = function(a) {
        if (a && a[0]) {
            var b;
            if (a[0] == "connect-state")if (a[1] == "error") {
                if (this.w.O() != 401)b = {message:"onError",data:{}},b.data.c = this.w.O(),b.data.d = ""
            } else a[1] == "closed" && (b = {message:"onClosed",data:{}}); else if (a[0] == "connect-data") {
                if (!a[2] || !a[2][0])return;
                var a = a[2],c = a[0];
                if (c == "ae")a = a[1],b = {message:"onMessage",data:{}},b.data.m = a,b.data.s = le(this.$b, a),this.$b.cc++; else if (c == "me")b = {message:"opened",data:{}}; else if (c == "m" && a[4] == "e")a = a[2],b = {message:"onError",data:{}},
                        b.data.c = 1,b.data.d = a
            }
            b && (this.S.Y() ? this.S.send(b.message, b.data) : this.bc.push(b))
        }
    };
    WcsDataClient.prototype.Ed = function(a, b) {
        b()
    };
    w("chat.WcsDataClient", WcsDataClient);
    SHA1 = function() {
        this.A = Array(5);
        this.Sc = Array(64);
        this.nh = Array(80);
        this.Tc = Array(64);
        this.Tc[0] = 128;
        for (var a = 1; a < 64; ++a)this.Tc[a] = 0;
        this.reset()
    };
    SHA1.prototype.reset = function() {
        this.A[0] = 1732584193;
        this.A[1] = 4023233417;
        this.A[2] = 2562383102;
        this.A[3] = 271733878;
        this.A[4] = 3285377520;
        this.Uc = this.Za = 0
    };
    var Ng = function(a, b) {
        return(a << b | a >>> 32 - b) & 4294967295
    },Og = function(a, b) {
        for (var c = a.nh,d = 0; d < 64; d += 4)c[d / 4] = b[d] << 24 | b[d + 1] << 16 | b[d + 2] << 8 | b[d + 3];
        for (d = 16; d < 80; ++d)c[d] = Ng(c[d - 3] ^ c[d - 8] ^ c[d - 14] ^ c[d - 16], 1);
        for (var e = a.A[0],g = a.A[1],i = a.A[2],j = a.A[3],k = a.A[4],l,o,d = 0; d < 80; ++d)d < 40 ? d < 20 ? (l = j ^ g & (i ^ j),o = 1518500249) : (l = g ^ i ^ j,o = 1859775393) : d < 60 ? (l = g & i | j & (g | i),o = 2400959708) : (l = g ^ i ^ j,o = 3395469782),l = Ng(e, 5) + l + k + o + c[d] & 4294967295,k = j,j = i,i = Ng(g, 30),g = e,e = l;
        a.A[0] = a.A[0] + e & 4294967295;
        a.A[1] = a.A[1] + g & 4294967295;
        a.A[2] = a.A[2] + i & 4294967295;
        a.A[3] = a.A[3] + j & 4294967295;
        a.A[4] = a.A[4] + k & 4294967295
    };
    SHA1.prototype.update = function(a, b) {
        if (!b)b = a.length;
        var c = 0;
        if (this.Za == 0)for (; c + 64 < b;)Og(this, a.slice(c, c + 64)),c += 64,this.Uc += 64;
        for (; c < b;)if (this.Sc[this.Za++] = a[c++],++this.Uc,this.Za == 64) {
            this.Za = 0;
            for (Og(this, this.Sc); c + 64 < b;)Og(this, a.slice(c, c + 64)),c += 64,this.Uc += 64
        }
    };
    SHA1.prototype.yb = function() {
        var a = Array(20),b = this.Uc * 8;
        this.Za < 56 ? this.update(this.Tc, 56 - this.Za) : this.update(this.Tc, 64 - (this.Za - 56));
        for (var c = 63; c >= 56; --c)this.Sc[c] = b & 255,b >>>= 8;
        Og(this, this.Sc);
        for (c = b = 0; c < 5; ++c)for (var d = 24; d >= 0; d -= 8)a[b++] = this.A[c] >> d & 255;
        return a
    };
    G_HMAC = function(a, b, c) {
        (!a || typeof a != "object" || !a.reset || !a.update || !a.yb) && f(Error("Invalid hasher object. Hasher unspecified or does not implement expected interface."));
        b.constructor != Array && f(Error("Invalid key."));
        c && typeof c != "number" && f(Error("Invalid block size."));
        this.ba = a;
        this.Vc = c || 16;
        this.Yf = Array(this.Vc);
        this.Zf = Array(this.Vc);
        b.length > this.Vc && (this.ba.update(b),b = this.ba.yb());
        for (c = 0; c < this.Vc; c++)a = c < b.length ? b[c] : 0,this.Yf[c] = a ^ G_HMAC.lh,this.Zf[c] = a ^ G_HMAC.kh
    };
    G_HMAC.lh = 92;
    G_HMAC.kh = 54;
    G_HMAC.prototype.reset = function() {
        this.ba.reset();
        this.ba.update(this.Zf)
    };
    G_HMAC.prototype.update = function(a) {
        a.constructor != Array && f(Error("Invalid data. Data must be an array."));
        this.ba.update(a)
    };
    G_HMAC.prototype.yb = function() {
        var a = this.ba.yb();
        this.ba.reset();
        this.ba.update(this.Yf);
        this.ba.update(a);
        return this.ba.yb()
    };
})()
