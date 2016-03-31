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
    updateColor("return");

    updateColor("name");

    updateColor("module");
    updateColor("import");
    updateColor("from");
    updateColor("as");

    updateColor("loop");
    updateColor("for");
    updateColor("in");
    updateColor("while");

    updateColor("conditional");
    updateColor("if");
    updateColor("elif");
    updateColor("else");

    updateColor("bool-op")
    updateColor("and");
    updateColor("or");

    updateColor("constant")
    updateColor("true");
    updateColor("false");
    updateColor("none");

    updateColor("literal");
    updateColor("constant");
    updateColor("number");
    updateColor("pass");
    updateColor("string");
  };

  $("#updateColors").click(updateAllColors);

  $(".section").click(function() {
    $(this).nextUntil("tr.section").slideToggle(0);
  });

  $(".section").nextUntil("tr.section").slideToggle(0);
  updateAllColors();
});
