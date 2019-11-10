function nthIndex(str, sub_str, n){
    var L= str.length, i= -1;
    while(n-- && i++<L){
        i= str.indexOf(sub_str, i);
        if (i < 0) break;
    }
    return i;
}

function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}