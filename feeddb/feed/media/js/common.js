function toggle(id, img_id){
     var el= document.getElementById(id);
     var img = document.getElementById(img_id);
     if (el){
 
         if(el.style.display == "none") {
               el.style.display="inline";
               el.style.position="absolute";
           
               img.src= "/static/img/admin/icon-yes.gif"
             
         }else{
               el.style.display = "none";
                img.src= "/static/img/admin/icon_changelink.gif"
         }
     }
}
