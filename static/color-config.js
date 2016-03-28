$(function() {
  $("#updateColors").click(function() {
    $(".python-keyword").css("color", $("#keyword-color").val());
    $(".python-name").css("color", $("#name-color").val());
  });
});
