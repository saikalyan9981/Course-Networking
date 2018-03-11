/// @function updateDiv1
///  submits a form first then updates the number of upvotes and downvotes
/// @param id
///  id of the div to be updated
function updateDiv1(id)
{ 
   document.getElementById('f1_'+id).submit();	
   setTimeout(function() {
    $( "#"+id ).load(window.location.href + " #" + id );
   }, 100);
}