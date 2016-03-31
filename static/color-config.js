$(function() {
  var updateColor = function(name) {
    var checkbox = $("#" + name + "-is-set");
    var elements = $(".python-" + name);

    if (checkbox.is(":checked")) {
      if (checkbox.parent().hasClass("ignore")) {
        elements.css("color", $("#default-color").val());
      } else {
        elements.css("color", $("#" + name + "-color").val());
      }
    }
  };

  var updateAllColors = function() {
    $(".python-source").css("color", $("#default-color").val())
    $(".python-source").css("background-color", $("#background-color").val())

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

  $("tr.section").children().children("[type=checkbox]").click(function() {
    $(this).parent().parent().nextUntil("tr.section")
      .children().toggleClass("ignore");
  });

  $("td.section-label").click(function() {
    $(this).parent().nextUntil("tr.section").toggle();
    $(this).find('.expand-marker').text(function(_, value) {
      return value == '+' ? '-' : '+';
    });
  });

  $("tr.section").nextUntil("tr.section").toggle();
  updateAllColors();
});
