function toggle(id, img_id){
     var el= document.getElementById(id);
     var img = document.getElementById(img_id);
     if (el){
 
         if(el.style.display == "none") {
               el.style.display="block";
               el.style.position="absolute";
               el.style.zindex = 1000;
               img.src= "/static/img/admin/icon-yes.gif";
             
         }else{
               el.style.display = "none";
                img.src= "/static/img/admin/icon_changelink.gif";
         }
     }
}

//this function is here as a placeholder for the same function in the i18n javascripts
function gettext(v1,v2,v3){
      return v1;
}
