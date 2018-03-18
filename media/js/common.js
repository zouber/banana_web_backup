var isOpera = !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
    // Opera 8.0+ (UA detection to detect Blink/v8-powered Opera)
var isFirefox = typeof InstallTrigger !== 'undefined';   // Firefox 1.0+
var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
    // At least Safari 3+: "[object HTMLElementConstructor]"
var isChrome = !!window.chrome && !isOpera;              // Chrome 1+
var isIE = /*@cc_on!@*/false || !!document.documentMode; // At least IE6

var Cookie = {
    check: function(name) {
        return this.read(name) != null;
    },
    // if expires not set, then this cookie will be destroyed when browser is closed.
    // http://www.elated.com/articles/javascript-and-cookies/
    // and if no expires been set, this cookie will called "session"
    // but after testing, it seems not go the way, if we don't set expires, the cookie is always alive, even if we close the browser then re-open
    // but for now, this fact will not affect the outcome we want, so I decide to call it a day, maybe do some research and solve it another day.
    create: function(name, value, seconds) {
        if(seconds) {
            var date = new Date();
            date.setTime(date.getTime() + (seconds*1000));
            var expires = "; expires="+date.toGMTString();
        }
        else var expires = "";
        document.cookie = name+"="+value+expires+"; path=/";
    },
    read: function(name) {
        var nameEQ = name+"=";
        var ca = document.cookie.split(';');
        for(var i=0;i<ca.length;i++) {
            var c = ca[i];
            while(c.charAt(0)==" ") c=c.substring(1,c.length);
            if(c.indexOf(nameEQ)== 0)return c.substring(nameEQ.length,c.length);
        }
        return null;
    },
    erase: function(name) {
        this.create(name,"",-1);
    }
}