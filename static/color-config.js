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

var loadColors = function(colors) {
  $("[type=checkbox]").prop("checked", false);

  var cookies = document.cookie.split(/; */);
  if (cookies.length === 1 && cookies[0] === '') {
    // default
  } else {
    $.each(cookies, function() {
      var splitCookie = this.split('=');
      var id  = splitCookie[0];
      var val = splitCookie[1];
      var element = $(document.getElementById(id));

      if (val === "checked") {
        console.log(this);
        element.prop("checked", true);
      } else {
        element.val(val);
      }
    });
  }

  updateAllColors();
}

var saveColors = function() {
  var checked = []
  var colors = {}

  colors['default-color'] = $("#default-color").val()
  colors['background-color'] = $("#background-color").val()
  $("[type=checkbox]").each(function(_, checkbox) {
    var color_picker = $(checkbox).parent().parent().children().
        children("[type=color]");
    colors[color_picker.attr("id")] = color_picker.val();

    if ($(checkbox).is(":checked")) {
      checked.push($(checkbox).attr("id"));
    } else console.log($(checkbox).attr("id") + " is not checked")
  });

  $.ajax({
    type: "POST",
    contentType: "application/json",
    url: $save_url,
    data: JSON.stringify({colors: colors, checked: checked})
  });
}

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

$(function() {
  $("#saveColors").click(saveColors);
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
  loadColors();
  $("div.python-line:empty").remove();
});
