// Returns the version of Internet Explorer or a -1
// (indicating the use of another browser).
function hb_getInternetExplorerVersion() {
  var rv = -1; // Return value assumes failure.
  if (navigator.appName == 'Microsoft Internet Explorer') {
    var ua = navigator.userAgent;
    var re  = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
    if (re.exec(ua) != null) {
      rv = parseFloat( RegExp.$1 );
    }
  }
  return rv;
}

// Checks IE version and redirects
function hb_checkVersion(loc)
{
  var ver = hb_getInternetExplorerVersion();
  if ( ver > -1 ) {
    if ( ver <= 8.0 ) {
      function getCookie(c_name) {
        var i,x,y,ARRcookies=document.cookie.split(";");
        for (i=0;i<ARRcookies.length;i++) {
          x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
          y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
          x=x.replace(/^\s+|\s+$/g,"");
          if (x==c_name) {
            return unescape(y);
          }
        }
      }

      var checkIEsession=getCookie("oldIE");
      if (checkIEsession == null || checkIEsession != "true") {
        document.cookie = 'oldIE=true';
        window.location = loc;
      }
    }
  }
}

hb_checkVersion('/happybrowser')
