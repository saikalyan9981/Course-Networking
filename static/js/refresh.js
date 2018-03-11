/// @function updateDiv1
///  refreshes the div with id 'here' evry 15 seconds, modify as per your need
setInterval(function updateDiv()
{ 
    $( "#"+'here' ).load(window.location.href + " #" + 'here' );
}, 15*1000);
