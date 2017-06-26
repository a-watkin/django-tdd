// alert('test');
// $('.has-error').hide();


// This line says: find any input elements whose name attribute is "text", and
// add an event listener which reacts on keypress events. The event listener
// is the inline function, which hides all elements that have the class .has-
// error.
// $('input[name="text"]').on('keypress', function () { 
//   $('.has-error').hide();
// });

// console.log('list.js loaded');


// so the above but being called by inline script
var initialize = function () {
  // console.log('initialize called');
  $('input[name="text"]').on('keypress', function () {
    // console.log('in keypress handler');
    $('.has-error').hide();
  });
};
// console.log('list.js loaded');