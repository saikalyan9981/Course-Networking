/// @function updateDiv2
///  submits a form first then updates the number of upvotes and downvotes
/// @param id
///  id of the div to be updated
function updateDiv2(id)
{ 
   document.getElementById('f2_'+id).submit();	
   setTimeout(function() {
    $( "#"+id ).load(window.location.href + " #" + id );
   }, 100);
}