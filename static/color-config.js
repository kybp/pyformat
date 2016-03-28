$(function() {
  $("#updateColors").click(function() {
    $(".python-keyword").css("color", $("#keyword-color").val());
    $(".python-def").css("color", $("#def-color").val());
    $(".python-import").css("color", $("#import-color").val());
    $(".python-return").css("color", $("#return-color").val());
    $(".python-name").css("color", $("#name-color").val());
  });
});
