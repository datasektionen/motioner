$(document).ready(function () {
  var appendItem = function(container, template) {
    var timestamp = new Date().getTime();
    $(container).append(template.replace(/TIMESTAMP/g, timestamp));
  }

  $('#add_author').click(function () {
    appendItem("#authors",'<li><input type="text" name="authors[TIMESTAMP]" id="authors_TIMESTAMP"></li>');
  });

  $('#add_item').click(function () {
    appendItem("#items", '<li><b>att</b> <textarea name="items[TIMESTAMP]" id="authors_TIMESTAMP" placeholder="Ytterligare någon vettig sak..."></textarea></li>');
  });

  $('textarea').ata();
});
