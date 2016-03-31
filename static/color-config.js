$(function() {
  var updateColor = function(name) {
    if ($("#" + name + "-is-set").is(":checked")) {
      $(".python-" + name).css("color", $("#" + name + "-color").val());
    }
  };

  var updateAllColors = function() {
    updateColor("keyword");
    updateColor("def");
    updateColor("class");
    updateColor("import");
    updateColor("return");
    updateColor("decorator");
    updateColor("name");
    updateColor("constant");
    updateColor("None");
    updateColor("for");
    updateColor("while");
    updateColor("if");
    updateColor("else");
    updateColor("false");
    updateColor("true");
    updateColor("and");
    updateColor("or");
    updateColor("number");
    updateColor("pass");
    updateColor("string");
  };

  $("#updateColors").click(updateAllColors);
  updateAllColors();
});
