'use strict';

var updateColor = function(name) {
  var checkbox = $("#" + name + "-is-set");
  var elements = $(".python-" + name);

  if (checkbox.is(":checked")) {
    if (checkbox.parent().parent().hasClass("ignore")) {
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
    $(".option").addClass("ignore");
    $("#default-color").val("#ffffff");
    $("#loop-section-is-set").prop("checked", true);
    $("#for-color").val("#ad1993");
    $("#loop-color").parent().parent().nextUntil("tr.section")
      .removeClass("ignore");
    $("#for-is-set").prop("checked", true);
  } else {
    $.each(cookies, function() {
      var splitCookie = this.split('=');
      var id  = splitCookie[0];
      var val = splitCookie[1];
      var element = $(document.getElementById(id));

      if (val === "checked") {
        element.prop("checked", true);
      } else if (val === "ignore") {
        element.addClass("ignore");
      } else {
        element.val(val);
      }
    });
  }

  updateAllColors();
}

var saveColors = function() {
  var checked = []
  var ignored = []
  var colors  = {}

  $(".ignore.option").each(function() {
    var id = $(this).attr("id");
    ignored.push(id);
  });

  colors['default-color'] = $("#default-color").val()
  colors['background-color'] = $("#background-color").val()
  $("[type=checkbox]").each(function(_, checkbox) {
    var color_picker = $(checkbox).parent().parent().children().
        children("[type=color]");
    colors[color_picker.attr("id")] = color_picker.val();

    if ($(checkbox).is(":checked")) {
      checked.push($(checkbox).attr("id"));
    }
  });

  $.ajax({
    type: "POST",
    contentType: "application/json",
    url: $save_url,
    data: JSON.stringify({colors: colors, checked: checked, ignored: ignored})
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
  updateColor("comment")

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
    $(this).parent().parent().nextUntil("tr.section").toggleClass("ignore");
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
