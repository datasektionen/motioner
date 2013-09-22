$(document).ready(function() {
  $('#add_author').click(function(event) {
    $("#authors").append('<li><input type="text" name="authors[]"></li>');
    $("#authors li:last input").focus();
    return false;
  });

  $('#add_item').click(function(event) {
    $("#items").append('<li><b>att</b> <textarea name="items[]" placeholder="Ytterligare någon vettig sak..."></textarea></li>');
    $("#items li:last textarea").focus();
    return false;
  });

  $('textarea').ata();
});
