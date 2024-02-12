const json_base = require("./grammar_base");

module.exports = grammar(json_base, {
  name: "json",
  extras: ($, original) => [...original, $.comment],

  rules: {
    _value: (_, original) => original,

    pair: (_, original) => original,

    object: ($) => seq("{", lineBreakOrComma($.pair), "}"),

    string: ($, original) => choice($.quoted_string, $.multiline_string),
    //  choice($.quoted_string, $.multiline_string, $.quoteless_string),

    array: ($) => seq("[", lineBreakOrComma($._value), "]"),

    quoted_string: ($) =>
      choice(
        seq('"', '"'),
        seq("'", "'"),
        seq('"', $._quoted_string_content, '"'),
        seq("'", $._quoted_string_content, "'")
      ),

    //  Use repeat1 here instead of repeat, as treesitter doesn't support matching with empty string
    _quoted_string_content: ($) =>
      repeat1(choice(token.immediate(/[^\\"\'\n]+/), $.escape_sequence)),

    //  quoteless string is conflicting with quoted string
    //  quoteless_string: ($) => repeat1(/[^\n]+/),

    multiline_string: ($) =>
      choice(seq("'''", "'''"), seq("'''", repeat1(/[^\\"\'\n]+/), "'''")),

    //  escape_sequence: ($) => token.immediate(seq("\\", /(\"|\'|\\|\/|b|f|n|r|t|u)/)),
    escape_sequence: ($, original) => original,

    comment: ($) =>
      token(
        choice(seq("//", /.*/), seq("/*", /[^*]*\*+([^/*][^*]*\*+)*/, "/"), seq("#", /.*/))
      ),
  },
});

function lineBreakOrComma1(rule) {
  return seq(rule, repeat(seq(/,|\n/, optional(rule))));
}

function lineBreakOrComma(rule) {
  return optional(lineBreakOrComma1(rule));
}
