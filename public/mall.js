$(document).ready(function () {
  var appendItem = function(container, template) {
    var timestamp = new Date().getTime();
    $(container).append(template.replace(/TIMESTAMP/g, timestamp));
  }

  $('#add_author').click(function (event) {
    appendItem("#authors",'<li><input type="text" name="authors[TIMESTAMP]" id="authors_TIMESTAMP"></li>');
    $("#authors li:last input").focus();
    return false;
  });

  $('#add_item').click(function (event) {
    appendItem("#items", '<li><b>att</b> <textarea name="items[TIMESTAMP]" id="items_TIMESTAMP" placeholder="Ytterligare någon vettig sak..."></textarea></li>');
    $("#items li:last textarea").focus();
    return false;
  });

  $('textarea').ata();
});
