var cur_edit_id=-1;

function toggle(id, img_id){
     var el= document.getElementById(id);
     var img = document.getElementById(img_id);
     if (el){
 
         if(el.style.display == "none") {
               el.style.display="block";
               el.style.position="absolute";
               el.style.zindex = 1000;
               el.opacity= 0 ;
               img.src= "/static/img/admin/icon-yes.gif";
             
         }else{
               el.style.display = "none";
                img.src= "/static/img/admin/icon_changelink.gif";
         }
     }
}
function show(id, e){
      hide(cur_edit_id);
      cur_edit_id=id;
      var ev=e;
      if(! ev) ev=window.event;
     
     var x = ev.pageX-250;
     var y = ev.pageY-140;
   
    var el= document.getElementById(id);
     if (el){
          el.style.display="block";
          el.style.position="absolute";
          el.style.zindex = 1000;
          el.style.left = x+"px";
          el.style.top  = y+"px";
     }
}


function hide(id){
     var el= document.getElementById(id);
     if (el){
         el.style.display = "none";
     }
}

function onmove(){
    hide(cur_edit_id);	
}
//this function is here as a placeholder for the same function in the i18n javascripts
function gettext(v1,v2,v3){
      return v1;
}
