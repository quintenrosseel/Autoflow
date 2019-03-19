/*
 PRECONDITIONS OF THIS IMPLEMENTATION
 - a is sorted array from small to big
 - comparison function uses an ordering relation in its comparisons
 */

function binSearch(f, a) {
  var l = 0;
  var r = (a.length - 1);

  while(!(l >= r)) {
    //console.log("Left Bound l: " + str(l));
    //console.log("Right Bound r: " + str(r));

    //console.log("Searching in: ")
    //console.log(a.slice(l,r+1));

    //console.log("Searching in [" + str(l) + ", " +str(r) + "]");
    var pivot = Math.floor((l + r)/2);
    //console.log("... with pivot " + str(pivot));
    if(f(pivot)) {
      //console.log("Searching Left. ");
      r = pivot;
    } else {
      //console.log("Searching Right. ");
      l = pivot + 1;
    }
  }
  //console.log("Searching in [" + str(l) + ", " +str(r) + "]");
  return l;
}
