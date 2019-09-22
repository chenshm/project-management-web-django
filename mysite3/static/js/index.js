//document.getElementById("d-sibling1").addEventListener("click", function(){myFunction("nav-dropdown1")});
//document.getElementById("d-sibling2").addEventListener("click", function(){myFunction("nav-dropdown2")});
//document.getElementById("menu").addEventListener("click",function(){myfunction2()});
window.onload = function(){
var el=document.getElementById("demo");
if(el){
  el.addEventListener("click", function(){myFunction("nav-dropdown1")});
}

var el2=document.getElementById("d-sibling2");
if(el2){
  el2.addEventListener("click", function(){myFunction("nav-dropdown2")});
}

var el3=document.getElementById("menu");
if(el3){
  el3.addEventListener("click",function(){myfunction2()});
}


}
function myFunction(w) {
  //console.log(this);
    var x = document.getElementById(w);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function myfunction2(){
  var x =document.getElementById("bar");
   var y =document.getElementById("content"); 
  if (x.style.display === "none") {
    x.style.display = "block";
    y.style.marginLeft ="25%";
  } else {
    x.style.display = "none";
    y.style.marginLeft ="0%";
  }
}