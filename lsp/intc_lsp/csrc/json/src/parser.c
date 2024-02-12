#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 66
#define LARGE_STATE_COUNT 8
#define SYMBOL_COUNT 32
#define ALIAS_COUNT 0
#define TOKEN_COUNT 18
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 2
#define MAX_ALIAS_SEQUENCE_LENGTH 4
#define PRODUCTION_ID_COUNT 3

enum {
  anon_sym_LBRACE = 1,
  aux_sym_object_token1 = 2,
  anon_sym_RBRACE = 3,
  anon_sym_COLON = 4,
  anon_sym_LBRACK = 5,
  anon_sym_RBRACK = 6,
  sym_escape_sequence = 7,
  sym_number = 8,
  anon_sym_true = 9,
  anon_sym_false = 10,
  sym_null = 11,
  sym_comment = 12,
  anon_sym_DQUOTE = 13,
  anon_sym_SQUOTE = 14,
  aux_sym__quoted_string_content_token1 = 15,
  anon_sym_SQUOTE_SQUOTE_SQUOTE = 16,
  aux_sym_multiline_string_token1 = 17,
  sym_document = 18,
  sym__value = 19,
  sym_object = 20,
  sym_pair = 21,
  sym_array = 22,
  sym_string = 23,
  sym_bool = 24,
  sym_quoted_string = 25,
  aux_sym__quoted_string_content = 26,
  sym_multiline_string = 27,
  aux_sym_document_repeat1 = 28,
  aux_sym_object_repeat1 = 29,
  aux_sym_array_repeat1 = 30,
  aux_sym_multiline_string_repeat1 = 31,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [anon_sym_LBRACE] = "{",
  [aux_sym_object_token1] = "object_token1",
  [anon_sym_RBRACE] = "}",
  [anon_sym_COLON] = ":",
  [anon_sym_LBRACK] = "[",
  [anon_sym_RBRACK] = "]",
  [sym_escape_sequence] = "escape_sequence",
  [sym_number] = "number",
  [anon_sym_true] = "true",
  [anon_sym_false] = "false",
  [sym_null] = "null",
  [sym_comment] = "comment",
  [anon_sym_DQUOTE] = "\"",
  [anon_sym_SQUOTE] = "'",
  [aux_sym__quoted_string_content_token1] = "_quoted_string_content_token1",
  [anon_sym_SQUOTE_SQUOTE_SQUOTE] = "'''",
  [aux_sym_multiline_string_token1] = "multiline_string_token1",
  [sym_document] = "document",
  [sym__value] = "_value",
  [sym_object] = "object",
  [sym_pair] = "pair",
  [sym_array] = "array",
  [sym_string] = "string",
  [sym_bool] = "bool",
  [sym_quoted_string] = "quoted_string",
  [aux_sym__quoted_string_content] = "_quoted_string_content",
  [sym_multiline_string] = "multiline_string",
  [aux_sym_document_repeat1] = "document_repeat1",
  [aux_sym_object_repeat1] = "object_repeat1",
  [aux_sym_array_repeat1] = "array_repeat1",
  [aux_sym_multiline_string_repeat1] = "multiline_string_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [anon_sym_LBRACE] = anon_sym_LBRACE,
  [aux_sym_object_token1] = aux_sym_object_token1,
  [anon_sym_RBRACE] = anon_sym_RBRACE,
  [anon_sym_COLON] = anon_sym_COLON,
  [anon_sym_LBRACK] = anon_sym_LBRACK,
  [anon_sym_RBRACK] = anon_sym_RBRACK,
  [sym_escape_sequence] = sym_escape_sequence,
  [sym_number] = sym_number,
  [anon_sym_true] = anon_sym_true,
  [anon_sym_false] = anon_sym_false,
  [sym_null] = sym_null,
  [sym_comment] = sym_comment,
  [anon_sym_DQUOTE] = anon_sym_DQUOTE,
  [anon_sym_SQUOTE] = anon_sym_SQUOTE,
  [aux_sym__quoted_string_content_token1] = aux_sym__quoted_string_content_token1,
  [anon_sym_SQUOTE_SQUOTE_SQUOTE] = anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [aux_sym_multiline_string_token1] = aux_sym_multiline_string_token1,
  [sym_document] = sym_document,
  [sym__value] = sym__value,
  [sym_object] = sym_object,
  [sym_pair] = sym_pair,
  [sym_array] = sym_array,
  [sym_string] = sym_string,
  [sym_bool] = sym_bool,
  [sym_quoted_string] = sym_quoted_string,
  [aux_sym__quoted_string_content] = aux_sym__quoted_string_content,
  [sym_multiline_string] = sym_multiline_string,
  [aux_sym_document_repeat1] = aux_sym_document_repeat1,
  [aux_sym_object_repeat1] = aux_sym_object_repeat1,
  [aux_sym_array_repeat1] = aux_sym_array_repeat1,
  [aux_sym_multiline_string_repeat1] = aux_sym_multiline_string_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_LBRACE] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_object_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_RBRACE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COLON] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LBRACK] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RBRACK] = {
    .visible = true,
    .named = false,
  },
  [sym_escape_sequence] = {
    .visible = true,
    .named = true,
  },
  [sym_number] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_true] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_false] = {
    .visible = true,
    .named = false,
  },
  [sym_null] = {
    .visible = true,
    .named = true,
  },
  [sym_comment] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_DQUOTE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SQUOTE] = {
    .visible = true,
    .named = false,
  },
  [aux_sym__quoted_string_content_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_SQUOTE_SQUOTE_SQUOTE] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_multiline_string_token1] = {
    .visible = false,
    .named = false,
  },
  [sym_document] = {
    .visible = true,
    .named = true,
  },
  [sym__value] = {
    .visible = false,
    .named = true,
    .supertype = true,
  },
  [sym_object] = {
    .visible = true,
    .named = true,
  },
  [sym_pair] = {
    .visible = true,
    .named = true,
  },
  [sym_array] = {
    .visible = true,
    .named = true,
  },
  [sym_string] = {
    .visible = true,
    .named = true,
  },
  [sym_bool] = {
    .visible = true,
    .named = true,
  },
  [sym_quoted_string] = {
    .visible = true,
    .named = true,
  },
  [aux_sym__quoted_string_content] = {
    .visible = false,
    .named = false,
  },
  [sym_multiline_string] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_document_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_object_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_array_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_multiline_string_repeat1] = {
    .visible = false,
    .named = false,
  },
};

enum {
  field_key = 1,
  field_value = 2,
};

static const char * const ts_field_names[] = {
  [0] = NULL,
  [field_key] = "key",
  [field_value] = "value",
};

static const TSFieldMapSlice ts_field_map_slices[PRODUCTION_ID_COUNT] = {
  [1] = {.index = 0, .length = 1},
  [2] = {.index = 1, .length = 2},
};

static const TSFieldMapEntry ts_field_map_entries[] = {
  [0] =
    {field_key, 0},
  [1] =
    {field_key, 0},
    {field_value, 2},
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 5,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 22,
  [24] = 24,
  [25] = 11,
  [26] = 26,
  [27] = 27,
  [28] = 27,
  [29] = 26,
  [30] = 30,
  [31] = 31,
  [32] = 31,
  [33] = 30,
  [34] = 13,
  [35] = 17,
  [36] = 18,
  [37] = 16,
  [38] = 14,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 21,
  [43] = 20,
  [44] = 8,
  [45] = 45,
  [46] = 46,
  [47] = 47,
  [48] = 15,
  [49] = 19,
  [50] = 50,
  [51] = 51,
  [52] = 10,
  [53] = 9,
  [54] = 54,
  [55] = 46,
  [56] = 56,
  [57] = 51,
  [58] = 54,
  [59] = 39,
  [60] = 45,
  [61] = 40,
  [62] = 62,
  [63] = 63,
  [64] = 64,
  [65] = 65,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(29);
      if (lookahead == '\n') ADVANCE(32);
      if (lookahead == '"') ADVANCE(53);
      if (lookahead == '#') ADVANCE(52);
      if (lookahead == '\'') ADVANCE(55);
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(9);
      if (lookahead == ',') ADVANCE(31);
      if (lookahead == '.') ADVANCE(24);
      if (lookahead == '/') ADVANCE(6);
      if (lookahead == '0') ADVANCE(38);
      if (lookahead == ':') ADVANCE(34);
      if (lookahead == '[') ADVANCE(35);
      if (lookahead == '\\') ADVANCE(23);
      if (lookahead == ']') ADVANCE(36);
      if (lookahead == 'f') ADVANCE(10);
      if (lookahead == 'n') ADVANCE(19);
      if (lookahead == 't') ADVANCE(16);
      if (lookahead == '{') ADVANCE(30);
      if (lookahead == '}') ADVANCE(33);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(27)
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(40);
      END_STATE();
    case 1:
      if (lookahead == '\n') SKIP(3)
      if (lookahead == '"') ADVANCE(53);
      if (lookahead == '#') ADVANCE(60);
      if (lookahead == '\'') ADVANCE(54);
      if (lookahead == '/') ADVANCE(57);
      if (lookahead == '\\') ADVANCE(23);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') ADVANCE(56);
      if (lookahead != 0) ADVANCE(61);
      END_STATE();
    case 2:
      if (lookahead == '\n') SKIP(2)
      if (lookahead == '#') ADVANCE(50);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '/') ADVANCE(64);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') ADVANCE(63);
      if (lookahead != 0 &&
          lookahead != '"' &&
          lookahead != '\\') ADVANCE(67);
      END_STATE();
    case 3:
      if (lookahead == '"') ADVANCE(53);
      if (lookahead == '#') ADVANCE(52);
      if (lookahead == '\'') ADVANCE(54);
      if (lookahead == '/') ADVANCE(6);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(3)
      END_STATE();
    case 4:
      if (lookahead == '\'') ADVANCE(5);
      END_STATE();
    case 5:
      if (lookahead == '\'') ADVANCE(62);
      END_STATE();
    case 6:
      if (lookahead == '*') ADVANCE(8);
      if (lookahead == '/') ADVANCE(52);
      END_STATE();
    case 7:
      if (lookahead == '*') ADVANCE(7);
      if (lookahead == '/') ADVANCE(49);
      if (lookahead != 0) ADVANCE(8);
      END_STATE();
    case 8:
      if (lookahead == '*') ADVANCE(7);
      if (lookahead != 0) ADVANCE(8);
      END_STATE();
    case 9:
      if (lookahead == '0') ADVANCE(39);
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(40);
      END_STATE();
    case 10:
      if (lookahead == 'a') ADVANCE(13);
      END_STATE();
    case 11:
      if (lookahead == 'e') ADVANCE(46);
      END_STATE();
    case 12:
      if (lookahead == 'e') ADVANCE(47);
      END_STATE();
    case 13:
      if (lookahead == 'l') ADVANCE(17);
      END_STATE();
    case 14:
      if (lookahead == 'l') ADVANCE(48);
      END_STATE();
    case 15:
      if (lookahead == 'l') ADVANCE(14);
      END_STATE();
    case 16:
      if (lookahead == 'r') ADVANCE(18);
      END_STATE();
    case 17:
      if (lookahead == 's') ADVANCE(12);
      END_STATE();
    case 18:
      if (lookahead == 'u') ADVANCE(11);
      END_STATE();
    case 19:
      if (lookahead == 'u') ADVANCE(15);
      END_STATE();
    case 20:
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(25);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(44);
      END_STATE();
    case 21:
      if (lookahead == '0' ||
          lookahead == '1') ADVANCE(42);
      END_STATE();
    case 22:
      if (('0' <= lookahead && lookahead <= '7')) ADVANCE(43);
      END_STATE();
    case 23:
      if (lookahead == '"' ||
          lookahead == '/' ||
          lookahead == '\\' ||
          lookahead == 'b' ||
          lookahead == 'f' ||
          lookahead == 'n' ||
          lookahead == 'r' ||
          lookahead == 't' ||
          lookahead == 'u') ADVANCE(37);
      END_STATE();
    case 24:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(41);
      END_STATE();
    case 25:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(44);
      END_STATE();
    case 26:
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'F') ||
          ('a' <= lookahead && lookahead <= 'f')) ADVANCE(45);
      END_STATE();
    case 27:
      if (eof) ADVANCE(29);
      if (lookahead == '\n') ADVANCE(32);
      if (lookahead == '"') ADVANCE(53);
      if (lookahead == '#') ADVANCE(52);
      if (lookahead == '\'') ADVANCE(55);
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(9);
      if (lookahead == ',') ADVANCE(31);
      if (lookahead == '.') ADVANCE(24);
      if (lookahead == '/') ADVANCE(6);
      if (lookahead == '0') ADVANCE(38);
      if (lookahead == ':') ADVANCE(34);
      if (lookahead == '[') ADVANCE(35);
      if (lookahead == ']') ADVANCE(36);
      if (lookahead == 'f') ADVANCE(10);
      if (lookahead == 'n') ADVANCE(19);
      if (lookahead == 't') ADVANCE(16);
      if (lookahead == '{') ADVANCE(30);
      if (lookahead == '}') ADVANCE(33);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(27)
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(40);
      END_STATE();
    case 28:
      if (eof) ADVANCE(29);
      if (lookahead == '"') ADVANCE(53);
      if (lookahead == '#') ADVANCE(52);
      if (lookahead == '\'') ADVANCE(55);
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(9);
      if (lookahead == '.') ADVANCE(24);
      if (lookahead == '/') ADVANCE(6);
      if (lookahead == '0') ADVANCE(38);
      if (lookahead == '[') ADVANCE(35);
      if (lookahead == ']') ADVANCE(36);
      if (lookahead == 'f') ADVANCE(10);
      if (lookahead == 'n') ADVANCE(19);
      if (lookahead == 't') ADVANCE(16);
      if (lookahead == '{') ADVANCE(30);
      if (lookahead == '}') ADVANCE(33);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(28)
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(40);
      END_STATE();
    case 29:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 30:
      ACCEPT_TOKEN(anon_sym_LBRACE);
      END_STATE();
    case 31:
      ACCEPT_TOKEN(aux_sym_object_token1);
      END_STATE();
    case 32:
      ACCEPT_TOKEN(aux_sym_object_token1);
      if (lookahead == '\n') ADVANCE(32);
      if (lookahead == ',') ADVANCE(31);
      END_STATE();
    case 33:
      ACCEPT_TOKEN(anon_sym_RBRACE);
      END_STATE();
    case 34:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(anon_sym_RBRACK);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(sym_escape_sequence);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(41);
      if (lookahead == 'B' ||
          lookahead == 'b') ADVANCE(21);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(20);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(22);
      if (lookahead == 'X' ||
          lookahead == 'x') ADVANCE(26);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(41);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(20);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(41);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(20);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(40);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(20);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(41);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '0' ||
          lookahead == '1') ADVANCE(42);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '7')) ADVANCE(43);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(44);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'F') ||
          ('a' <= lookahead && lookahead <= 'f')) ADVANCE(45);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(anon_sym_true);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(anon_sym_false);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(sym_null);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(sym_comment);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '"' ||
          lookahead == '\'' ||
          lookahead == '\\') ADVANCE(52);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(50);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '"' &&
          lookahead != '\'' &&
          lookahead != '\\') ADVANCE(67);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(52);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(anon_sym_DQUOTE);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(anon_sym_SQUOTE);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(anon_sym_SQUOTE);
      if (lookahead == '\'') ADVANCE(5);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(aux_sym__quoted_string_content_token1);
      if (lookahead == '#') ADVANCE(60);
      if (lookahead == '/') ADVANCE(57);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') ADVANCE(56);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '"' &&
          lookahead != '\'' &&
          lookahead != '\\') ADVANCE(61);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(aux_sym__quoted_string_content_token1);
      if (lookahead == '*') ADVANCE(59);
      if (lookahead == '/') ADVANCE(60);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '"' &&
          lookahead != '\'' &&
          lookahead != '\\') ADVANCE(61);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(aux_sym__quoted_string_content_token1);
      if (lookahead == '*') ADVANCE(58);
      if (lookahead == '/') ADVANCE(61);
      if (lookahead == '\n' ||
          lookahead == '"' ||
          lookahead == '\'' ||
          lookahead == '\\') ADVANCE(8);
      if (lookahead != 0) ADVANCE(59);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(aux_sym__quoted_string_content_token1);
      if (lookahead == '*') ADVANCE(58);
      if (lookahead == '\n' ||
          lookahead == '"' ||
          lookahead == '\'' ||
          lookahead == '\\') ADVANCE(8);
      if (lookahead != 0) ADVANCE(59);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(aux_sym__quoted_string_content_token1);
      if (lookahead == '"' ||
          lookahead == '\'' ||
          lookahead == '\\') ADVANCE(52);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(60);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(aux_sym__quoted_string_content_token1);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '"' &&
          lookahead != '\'' &&
          lookahead != '\\') ADVANCE(61);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(anon_sym_SQUOTE_SQUOTE_SQUOTE);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(aux_sym_multiline_string_token1);
      if (lookahead == '#') ADVANCE(50);
      if (lookahead == '/') ADVANCE(64);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') ADVANCE(63);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '"' &&
          lookahead != '\'' &&
          lookahead != '\\') ADVANCE(67);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(aux_sym_multiline_string_token1);
      if (lookahead == '*') ADVANCE(66);
      if (lookahead == '/') ADVANCE(50);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '"' &&
          lookahead != '\'' &&
          lookahead != '\\') ADVANCE(67);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(aux_sym_multiline_string_token1);
      if (lookahead == '*') ADVANCE(65);
      if (lookahead == '/') ADVANCE(51);
      if (lookahead == '\n' ||
          lookahead == '"' ||
          lookahead == '\'' ||
          lookahead == '\\') ADVANCE(8);
      if (lookahead != 0) ADVANCE(66);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(aux_sym_multiline_string_token1);
      if (lookahead == '*') ADVANCE(65);
      if (lookahead == '\n' ||
          lookahead == '"' ||
          lookahead == '\'' ||
          lookahead == '\\') ADVANCE(8);
      if (lookahead != 0) ADVANCE(66);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(aux_sym_multiline_string_token1);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '"' &&
          lookahead != '\'' &&
          lookahead != '\\') ADVANCE(67);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 28},
  [2] = {.lex_state = 28},
  [3] = {.lex_state = 28},
  [4] = {.lex_state = 0},
  [5] = {.lex_state = 28},
  [6] = {.lex_state = 28},
  [7] = {.lex_state = 28},
  [8] = {.lex_state = 28},
  [9] = {.lex_state = 28},
  [10] = {.lex_state = 28},
  [11] = {.lex_state = 28},
  [12] = {.lex_state = 0},
  [13] = {.lex_state = 28},
  [14] = {.lex_state = 28},
  [15] = {.lex_state = 28},
  [16] = {.lex_state = 28},
  [17] = {.lex_state = 28},
  [18] = {.lex_state = 28},
  [19] = {.lex_state = 28},
  [20] = {.lex_state = 28},
  [21] = {.lex_state = 28},
  [22] = {.lex_state = 28},
  [23] = {.lex_state = 28},
  [24] = {.lex_state = 1},
  [25] = {.lex_state = 0},
  [26] = {.lex_state = 1},
  [27] = {.lex_state = 1},
  [28] = {.lex_state = 1},
  [29] = {.lex_state = 1},
  [30] = {.lex_state = 1},
  [31] = {.lex_state = 1},
  [32] = {.lex_state = 1},
  [33] = {.lex_state = 1},
  [34] = {.lex_state = 0},
  [35] = {.lex_state = 0},
  [36] = {.lex_state = 0},
  [37] = {.lex_state = 0},
  [38] = {.lex_state = 0},
  [39] = {.lex_state = 0},
  [40] = {.lex_state = 0},
  [41] = {.lex_state = 0},
  [42] = {.lex_state = 0},
  [43] = {.lex_state = 0},
  [44] = {.lex_state = 0},
  [45] = {.lex_state = 0},
  [46] = {.lex_state = 2},
  [47] = {.lex_state = 0},
  [48] = {.lex_state = 0},
  [49] = {.lex_state = 0},
  [50] = {.lex_state = 0},
  [51] = {.lex_state = 0},
  [52] = {.lex_state = 0},
  [53] = {.lex_state = 0},
  [54] = {.lex_state = 2},
  [55] = {.lex_state = 2},
  [56] = {.lex_state = 2},
  [57] = {.lex_state = 0},
  [58] = {.lex_state = 2},
  [59] = {.lex_state = 0},
  [60] = {.lex_state = 0},
  [61] = {.lex_state = 0},
  [62] = {.lex_state = 0},
  [63] = {.lex_state = 0},
  [64] = {.lex_state = 0},
  [65] = {.lex_state = 28},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_LBRACE] = ACTIONS(1),
    [aux_sym_object_token1] = ACTIONS(1),
    [anon_sym_RBRACE] = ACTIONS(1),
    [anon_sym_COLON] = ACTIONS(1),
    [anon_sym_LBRACK] = ACTIONS(1),
    [anon_sym_RBRACK] = ACTIONS(1),
    [sym_escape_sequence] = ACTIONS(1),
    [sym_number] = ACTIONS(1),
    [anon_sym_true] = ACTIONS(1),
    [anon_sym_false] = ACTIONS(1),
    [sym_null] = ACTIONS(1),
    [sym_comment] = ACTIONS(3),
    [anon_sym_DQUOTE] = ACTIONS(1),
    [anon_sym_SQUOTE] = ACTIONS(1),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(1),
  },
  [1] = {
    [sym_document] = STATE(65),
    [sym__value] = STATE(2),
    [sym_object] = STATE(21),
    [sym_array] = STATE(21),
    [sym_string] = STATE(21),
    [sym_bool] = STATE(21),
    [sym_quoted_string] = STATE(11),
    [sym_multiline_string] = STATE(11),
    [aux_sym_document_repeat1] = STATE(2),
    [ts_builtin_sym_end] = ACTIONS(5),
    [anon_sym_LBRACE] = ACTIONS(7),
    [anon_sym_LBRACK] = ACTIONS(9),
    [sym_number] = ACTIONS(11),
    [anon_sym_true] = ACTIONS(13),
    [anon_sym_false] = ACTIONS(13),
    [sym_null] = ACTIONS(11),
    [sym_comment] = ACTIONS(15),
    [anon_sym_DQUOTE] = ACTIONS(17),
    [anon_sym_SQUOTE] = ACTIONS(19),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(21),
  },
  [2] = {
    [sym__value] = STATE(3),
    [sym_object] = STATE(21),
    [sym_array] = STATE(21),
    [sym_string] = STATE(21),
    [sym_bool] = STATE(21),
    [sym_quoted_string] = STATE(11),
    [sym_multiline_string] = STATE(11),
    [aux_sym_document_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(23),
    [anon_sym_LBRACE] = ACTIONS(7),
    [anon_sym_LBRACK] = ACTIONS(9),
    [sym_number] = ACTIONS(11),
    [anon_sym_true] = ACTIONS(13),
    [anon_sym_false] = ACTIONS(13),
    [sym_null] = ACTIONS(11),
    [sym_comment] = ACTIONS(15),
    [anon_sym_DQUOTE] = ACTIONS(17),
    [anon_sym_SQUOTE] = ACTIONS(19),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(21),
  },
  [3] = {
    [sym__value] = STATE(3),
    [sym_object] = STATE(21),
    [sym_array] = STATE(21),
    [sym_string] = STATE(21),
    [sym_bool] = STATE(21),
    [sym_quoted_string] = STATE(11),
    [sym_multiline_string] = STATE(11),
    [aux_sym_document_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(25),
    [anon_sym_LBRACE] = ACTIONS(27),
    [anon_sym_LBRACK] = ACTIONS(30),
    [sym_number] = ACTIONS(33),
    [anon_sym_true] = ACTIONS(36),
    [anon_sym_false] = ACTIONS(36),
    [sym_null] = ACTIONS(33),
    [sym_comment] = ACTIONS(15),
    [anon_sym_DQUOTE] = ACTIONS(39),
    [anon_sym_SQUOTE] = ACTIONS(42),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(45),
  },
  [4] = {
    [sym__value] = STATE(62),
    [sym_object] = STATE(42),
    [sym_array] = STATE(42),
    [sym_string] = STATE(42),
    [sym_bool] = STATE(42),
    [sym_quoted_string] = STATE(25),
    [sym_multiline_string] = STATE(25),
    [anon_sym_LBRACE] = ACTIONS(48),
    [aux_sym_object_token1] = ACTIONS(50),
    [anon_sym_LBRACK] = ACTIONS(52),
    [anon_sym_RBRACK] = ACTIONS(54),
    [sym_number] = ACTIONS(56),
    [anon_sym_true] = ACTIONS(58),
    [anon_sym_false] = ACTIONS(58),
    [sym_null] = ACTIONS(56),
    [sym_comment] = ACTIONS(3),
    [anon_sym_DQUOTE] = ACTIONS(60),
    [anon_sym_SQUOTE] = ACTIONS(62),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(64),
  },
  [5] = {
    [sym__value] = STATE(45),
    [sym_object] = STATE(42),
    [sym_array] = STATE(42),
    [sym_string] = STATE(42),
    [sym_bool] = STATE(42),
    [sym_quoted_string] = STATE(25),
    [sym_multiline_string] = STATE(25),
    [anon_sym_LBRACE] = ACTIONS(66),
    [anon_sym_LBRACK] = ACTIONS(68),
    [anon_sym_RBRACK] = ACTIONS(70),
    [sym_number] = ACTIONS(72),
    [anon_sym_true] = ACTIONS(74),
    [anon_sym_false] = ACTIONS(74),
    [sym_null] = ACTIONS(72),
    [sym_comment] = ACTIONS(15),
    [anon_sym_DQUOTE] = ACTIONS(76),
    [anon_sym_SQUOTE] = ACTIONS(62),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(78),
  },
  [6] = {
    [sym__value] = STATE(60),
    [sym_object] = STATE(42),
    [sym_array] = STATE(42),
    [sym_string] = STATE(42),
    [sym_bool] = STATE(42),
    [sym_quoted_string] = STATE(25),
    [sym_multiline_string] = STATE(25),
    [anon_sym_LBRACE] = ACTIONS(66),
    [anon_sym_LBRACK] = ACTIONS(68),
    [anon_sym_RBRACK] = ACTIONS(80),
    [sym_number] = ACTIONS(72),
    [anon_sym_true] = ACTIONS(74),
    [anon_sym_false] = ACTIONS(74),
    [sym_null] = ACTIONS(72),
    [sym_comment] = ACTIONS(15),
    [anon_sym_DQUOTE] = ACTIONS(76),
    [anon_sym_SQUOTE] = ACTIONS(62),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(78),
  },
  [7] = {
    [sym__value] = STATE(63),
    [sym_object] = STATE(42),
    [sym_array] = STATE(42),
    [sym_string] = STATE(42),
    [sym_bool] = STATE(42),
    [sym_quoted_string] = STATE(25),
    [sym_multiline_string] = STATE(25),
    [anon_sym_LBRACE] = ACTIONS(66),
    [anon_sym_LBRACK] = ACTIONS(68),
    [sym_number] = ACTIONS(72),
    [anon_sym_true] = ACTIONS(74),
    [anon_sym_false] = ACTIONS(74),
    [sym_null] = ACTIONS(72),
    [sym_comment] = ACTIONS(15),
    [anon_sym_DQUOTE] = ACTIONS(76),
    [anon_sym_SQUOTE] = ACTIONS(62),
    [anon_sym_SQUOTE_SQUOTE_SQUOTE] = ACTIONS(78),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(84), 1,
      anon_sym_SQUOTE,
    ACTIONS(82), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [18] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(88), 1,
      anon_sym_SQUOTE,
    ACTIONS(86), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [36] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(92), 1,
      anon_sym_SQUOTE,
    ACTIONS(90), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [54] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(96), 1,
      anon_sym_SQUOTE,
    ACTIONS(94), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [72] = 10,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(60), 1,
      anon_sym_DQUOTE,
    ACTIONS(62), 1,
      anon_sym_SQUOTE,
    ACTIONS(64), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    ACTIONS(98), 1,
      aux_sym_object_token1,
    ACTIONS(100), 1,
      anon_sym_RBRACE,
    ACTIONS(102), 1,
      sym_number,
    STATE(50), 1,
      sym_string,
    STATE(64), 1,
      sym_pair,
    STATE(25), 2,
      sym_quoted_string,
      sym_multiline_string,
  [104] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(106), 1,
      anon_sym_SQUOTE,
    ACTIONS(104), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [122] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(110), 1,
      anon_sym_SQUOTE,
    ACTIONS(108), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [140] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(114), 1,
      anon_sym_SQUOTE,
    ACTIONS(112), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [158] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(118), 1,
      anon_sym_SQUOTE,
    ACTIONS(116), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [176] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(122), 1,
      anon_sym_SQUOTE,
    ACTIONS(120), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [194] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(126), 1,
      anon_sym_SQUOTE,
    ACTIONS(124), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [212] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(130), 1,
      anon_sym_SQUOTE,
    ACTIONS(128), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [230] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(134), 1,
      anon_sym_SQUOTE,
    ACTIONS(132), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [248] = 3,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(138), 1,
      anon_sym_SQUOTE,
    ACTIONS(136), 9,
      ts_builtin_sym_end,
      anon_sym_LBRACE,
      anon_sym_LBRACK,
      sym_number,
      anon_sym_true,
      anon_sym_false,
      sym_null,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
  [266] = 9,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(62), 1,
      anon_sym_SQUOTE,
    ACTIONS(76), 1,
      anon_sym_DQUOTE,
    ACTIONS(78), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    ACTIONS(140), 1,
      anon_sym_RBRACE,
    ACTIONS(142), 1,
      sym_number,
    STATE(39), 1,
      sym_pair,
    STATE(50), 1,
      sym_string,
    STATE(25), 2,
      sym_quoted_string,
      sym_multiline_string,
  [295] = 9,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(62), 1,
      anon_sym_SQUOTE,
    ACTIONS(76), 1,
      anon_sym_DQUOTE,
    ACTIONS(78), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    ACTIONS(142), 1,
      sym_number,
    ACTIONS(144), 1,
      anon_sym_RBRACE,
    STATE(50), 1,
      sym_string,
    STATE(59), 1,
      sym_pair,
    STATE(25), 2,
      sym_quoted_string,
      sym_multiline_string,
  [324] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(146), 1,
      sym_escape_sequence,
    ACTIONS(151), 1,
      aux_sym__quoted_string_content_token1,
    STATE(24), 1,
      aux_sym__quoted_string_content,
    ACTIONS(149), 2,
      anon_sym_DQUOTE,
      anon_sym_SQUOTE,
  [341] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(94), 1,
      aux_sym_object_token1,
    ACTIONS(96), 3,
      anon_sym_RBRACE,
      anon_sym_COLON,
      anon_sym_RBRACK,
  [353] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(154), 1,
      sym_escape_sequence,
    ACTIONS(156), 1,
      anon_sym_DQUOTE,
    ACTIONS(158), 1,
      aux_sym__quoted_string_content_token1,
    STATE(24), 1,
      aux_sym__quoted_string_content,
  [369] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(154), 1,
      sym_escape_sequence,
    ACTIONS(156), 1,
      anon_sym_SQUOTE,
    ACTIONS(158), 1,
      aux_sym__quoted_string_content_token1,
    STATE(24), 1,
      aux_sym__quoted_string_content,
  [385] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(154), 1,
      sym_escape_sequence,
    ACTIONS(158), 1,
      aux_sym__quoted_string_content_token1,
    ACTIONS(160), 1,
      anon_sym_SQUOTE,
    STATE(24), 1,
      aux_sym__quoted_string_content,
  [401] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(154), 1,
      sym_escape_sequence,
    ACTIONS(158), 1,
      aux_sym__quoted_string_content_token1,
    ACTIONS(160), 1,
      anon_sym_DQUOTE,
    STATE(24), 1,
      aux_sym__quoted_string_content,
  [417] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(162), 1,
      sym_escape_sequence,
    ACTIONS(164), 1,
      anon_sym_SQUOTE,
    ACTIONS(166), 1,
      aux_sym__quoted_string_content_token1,
    STATE(28), 1,
      aux_sym__quoted_string_content,
  [433] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(168), 1,
      sym_escape_sequence,
    ACTIONS(170), 1,
      anon_sym_DQUOTE,
    ACTIONS(172), 1,
      aux_sym__quoted_string_content_token1,
    STATE(26), 1,
      aux_sym__quoted_string_content,
  [449] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(164), 1,
      anon_sym_DQUOTE,
    ACTIONS(174), 1,
      sym_escape_sequence,
    ACTIONS(176), 1,
      aux_sym__quoted_string_content_token1,
    STATE(29), 1,
      aux_sym__quoted_string_content,
  [465] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(170), 1,
      anon_sym_SQUOTE,
    ACTIONS(178), 1,
      sym_escape_sequence,
    ACTIONS(180), 1,
      aux_sym__quoted_string_content_token1,
    STATE(27), 1,
      aux_sym__quoted_string_content,
  [481] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(104), 1,
      aux_sym_object_token1,
    ACTIONS(106), 3,
      anon_sym_RBRACE,
      anon_sym_COLON,
      anon_sym_RBRACK,
  [493] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(120), 1,
      aux_sym_object_token1,
    ACTIONS(122), 3,
      anon_sym_RBRACE,
      anon_sym_COLON,
      anon_sym_RBRACK,
  [505] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(124), 1,
      aux_sym_object_token1,
    ACTIONS(126), 3,
      anon_sym_RBRACE,
      anon_sym_COLON,
      anon_sym_RBRACK,
  [517] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(116), 1,
      aux_sym_object_token1,
    ACTIONS(118), 3,
      anon_sym_RBRACE,
      anon_sym_COLON,
      anon_sym_RBRACK,
  [529] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(108), 1,
      aux_sym_object_token1,
    ACTIONS(110), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [540] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(182), 1,
      aux_sym_object_token1,
    ACTIONS(184), 1,
      anon_sym_RBRACE,
    STATE(57), 1,
      aux_sym_object_repeat1,
  [553] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(186), 1,
      aux_sym_object_token1,
    ACTIONS(188), 1,
      anon_sym_RBRACK,
    STATE(41), 1,
      aux_sym_array_repeat1,
  [566] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(190), 1,
      aux_sym_object_token1,
    ACTIONS(193), 1,
      anon_sym_RBRACK,
    STATE(41), 1,
      aux_sym_array_repeat1,
  [579] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(136), 1,
      aux_sym_object_token1,
    ACTIONS(138), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [590] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(132), 1,
      aux_sym_object_token1,
    ACTIONS(134), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [601] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(82), 1,
      aux_sym_object_token1,
    ACTIONS(84), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [612] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(186), 1,
      aux_sym_object_token1,
    ACTIONS(195), 1,
      anon_sym_RBRACK,
    STATE(61), 1,
      aux_sym_array_repeat1,
  [625] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(197), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    ACTIONS(199), 1,
      aux_sym_multiline_string_token1,
    STATE(56), 1,
      aux_sym_multiline_string_repeat1,
  [638] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(201), 1,
      aux_sym_object_token1,
    ACTIONS(204), 1,
      anon_sym_RBRACE,
    STATE(47), 1,
      aux_sym_object_repeat1,
  [651] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(112), 1,
      aux_sym_object_token1,
    ACTIONS(114), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [662] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(128), 1,
      aux_sym_object_token1,
    ACTIONS(130), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [673] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(206), 1,
      aux_sym_object_token1,
    ACTIONS(208), 1,
      anon_sym_RBRACE,
    ACTIONS(210), 1,
      anon_sym_COLON,
  [686] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(182), 1,
      aux_sym_object_token1,
    ACTIONS(212), 1,
      anon_sym_RBRACE,
    STATE(47), 1,
      aux_sym_object_repeat1,
  [699] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(90), 1,
      aux_sym_object_token1,
    ACTIONS(92), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [710] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(86), 1,
      aux_sym_object_token1,
    ACTIONS(88), 2,
      anon_sym_RBRACE,
      anon_sym_RBRACK,
  [721] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(214), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    ACTIONS(216), 1,
      aux_sym_multiline_string_token1,
    STATE(46), 1,
      aux_sym_multiline_string_repeat1,
  [734] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(199), 1,
      aux_sym_multiline_string_token1,
    ACTIONS(218), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    STATE(56), 1,
      aux_sym_multiline_string_repeat1,
  [747] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(220), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    ACTIONS(222), 1,
      aux_sym_multiline_string_token1,
    STATE(56), 1,
      aux_sym_multiline_string_repeat1,
  [760] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(182), 1,
      aux_sym_object_token1,
    ACTIONS(225), 1,
      anon_sym_RBRACE,
    STATE(47), 1,
      aux_sym_object_repeat1,
  [773] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(227), 1,
      anon_sym_SQUOTE_SQUOTE_SQUOTE,
    ACTIONS(229), 1,
      aux_sym_multiline_string_token1,
    STATE(55), 1,
      aux_sym_multiline_string_repeat1,
  [786] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(182), 1,
      aux_sym_object_token1,
    ACTIONS(231), 1,
      anon_sym_RBRACE,
    STATE(51), 1,
      aux_sym_object_repeat1,
  [799] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(186), 1,
      aux_sym_object_token1,
    ACTIONS(233), 1,
      anon_sym_RBRACK,
    STATE(40), 1,
      aux_sym_array_repeat1,
  [812] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(186), 1,
      aux_sym_object_token1,
    ACTIONS(235), 1,
      anon_sym_RBRACK,
    STATE(41), 1,
      aux_sym_array_repeat1,
  [825] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(193), 1,
      anon_sym_RBRACK,
    ACTIONS(237), 1,
      aux_sym_object_token1,
  [835] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(239), 1,
      aux_sym_object_token1,
    ACTIONS(241), 1,
      anon_sym_RBRACE,
  [845] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(204), 1,
      anon_sym_RBRACE,
    ACTIONS(243), 1,
      aux_sym_object_token1,
  [855] = 2,
    ACTIONS(15), 1,
      sym_comment,
    ACTIONS(245), 1,
      ts_builtin_sym_end,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(8)] = 0,
  [SMALL_STATE(9)] = 18,
  [SMALL_STATE(10)] = 36,
  [SMALL_STATE(11)] = 54,
  [SMALL_STATE(12)] = 72,
  [SMALL_STATE(13)] = 104,
  [SMALL_STATE(14)] = 122,
  [SMALL_STATE(15)] = 140,
  [SMALL_STATE(16)] = 158,
  [SMALL_STATE(17)] = 176,
  [SMALL_STATE(18)] = 194,
  [SMALL_STATE(19)] = 212,
  [SMALL_STATE(20)] = 230,
  [SMALL_STATE(21)] = 248,
  [SMALL_STATE(22)] = 266,
  [SMALL_STATE(23)] = 295,
  [SMALL_STATE(24)] = 324,
  [SMALL_STATE(25)] = 341,
  [SMALL_STATE(26)] = 353,
  [SMALL_STATE(27)] = 369,
  [SMALL_STATE(28)] = 385,
  [SMALL_STATE(29)] = 401,
  [SMALL_STATE(30)] = 417,
  [SMALL_STATE(31)] = 433,
  [SMALL_STATE(32)] = 449,
  [SMALL_STATE(33)] = 465,
  [SMALL_STATE(34)] = 481,
  [SMALL_STATE(35)] = 493,
  [SMALL_STATE(36)] = 505,
  [SMALL_STATE(37)] = 517,
  [SMALL_STATE(38)] = 529,
  [SMALL_STATE(39)] = 540,
  [SMALL_STATE(40)] = 553,
  [SMALL_STATE(41)] = 566,
  [SMALL_STATE(42)] = 579,
  [SMALL_STATE(43)] = 590,
  [SMALL_STATE(44)] = 601,
  [SMALL_STATE(45)] = 612,
  [SMALL_STATE(46)] = 625,
  [SMALL_STATE(47)] = 638,
  [SMALL_STATE(48)] = 651,
  [SMALL_STATE(49)] = 662,
  [SMALL_STATE(50)] = 673,
  [SMALL_STATE(51)] = 686,
  [SMALL_STATE(52)] = 699,
  [SMALL_STATE(53)] = 710,
  [SMALL_STATE(54)] = 721,
  [SMALL_STATE(55)] = 734,
  [SMALL_STATE(56)] = 747,
  [SMALL_STATE(57)] = 760,
  [SMALL_STATE(58)] = 773,
  [SMALL_STATE(59)] = 786,
  [SMALL_STATE(60)] = 799,
  [SMALL_STATE(61)] = 812,
  [SMALL_STATE(62)] = 825,
  [SMALL_STATE(63)] = 835,
  [SMALL_STATE(64)] = 845,
  [SMALL_STATE(65)] = 855,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = false}}, SHIFT_EXTRA(),
  [5] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_document, 0),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(5),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(20),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT_EXTRA(),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [19] = {.entry = {.count = 1, .reusable = false}}, SHIFT(33),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(54),
  [23] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_document, 1),
  [25] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2),
  [27] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(22),
  [30] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(5),
  [33] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(21),
  [36] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(20),
  [39] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(31),
  [42] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(33),
  [45] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_document_repeat1, 2), SHIFT_REPEAT(54),
  [48] = {.entry = {.count = 1, .reusable = false}}, SHIFT(23),
  [50] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_array_repeat1, 1),
  [52] = {.entry = {.count = 1, .reusable = false}}, SHIFT(6),
  [54] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_array_repeat1, 1),
  [56] = {.entry = {.count = 1, .reusable = false}}, SHIFT(42),
  [58] = {.entry = {.count = 1, .reusable = false}}, SHIFT(43),
  [60] = {.entry = {.count = 1, .reusable = false}}, SHIFT(32),
  [62] = {.entry = {.count = 1, .reusable = false}}, SHIFT(30),
  [64] = {.entry = {.count = 1, .reusable = false}}, SHIFT(58),
  [66] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [68] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [70] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [72] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [74] = {.entry = {.count = 1, .reusable = true}}, SHIFT(43),
  [76] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [78] = {.entry = {.count = 1, .reusable = true}}, SHIFT(58),
  [80] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [82] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_object, 2),
  [84] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_object, 2),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_array, 4),
  [88] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_array, 4),
  [90] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_object, 4),
  [92] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_object, 4),
  [94] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_string, 1),
  [96] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_string, 1),
  [98] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_object_repeat1, 1),
  [100] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_object_repeat1, 1),
  [102] = {.entry = {.count = 1, .reusable = false}}, SHIFT(50),
  [104] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_multiline_string, 3),
  [106] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_multiline_string, 3),
  [108] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_array, 2),
  [110] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_array, 2),
  [112] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_object, 3),
  [114] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_object, 3),
  [116] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_quoted_string, 2),
  [118] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_quoted_string, 2),
  [120] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_quoted_string, 3),
  [122] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_quoted_string, 3),
  [124] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_multiline_string, 2),
  [126] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_multiline_string, 2),
  [128] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_array, 3),
  [130] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_array, 3),
  [132] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_bool, 1),
  [134] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_bool, 1),
  [136] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__value, 1),
  [138] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym__value, 1),
  [140] = {.entry = {.count = 1, .reusable = true}}, SHIFT(8),
  [142] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [144] = {.entry = {.count = 1, .reusable = true}}, SHIFT(44),
  [146] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym__quoted_string_content, 2), SHIFT_REPEAT(24),
  [149] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym__quoted_string_content, 2),
  [151] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym__quoted_string_content, 2), SHIFT_REPEAT(24),
  [154] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [156] = {.entry = {.count = 1, .reusable = false}}, SHIFT(17),
  [158] = {.entry = {.count = 1, .reusable = false}}, SHIFT(24),
  [160] = {.entry = {.count = 1, .reusable = false}}, SHIFT(35),
  [162] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [164] = {.entry = {.count = 1, .reusable = false}}, SHIFT(37),
  [166] = {.entry = {.count = 1, .reusable = false}}, SHIFT(28),
  [168] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [170] = {.entry = {.count = 1, .reusable = false}}, SHIFT(16),
  [172] = {.entry = {.count = 1, .reusable = false}}, SHIFT(26),
  [174] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [176] = {.entry = {.count = 1, .reusable = false}}, SHIFT(29),
  [178] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [180] = {.entry = {.count = 1, .reusable = false}}, SHIFT(27),
  [182] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [184] = {.entry = {.count = 1, .reusable = false}}, SHIFT(15),
  [186] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [188] = {.entry = {.count = 1, .reusable = false}}, SHIFT(53),
  [190] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_array_repeat1, 2), SHIFT_REPEAT(4),
  [193] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_array_repeat1, 2),
  [195] = {.entry = {.count = 1, .reusable = false}}, SHIFT(19),
  [197] = {.entry = {.count = 1, .reusable = false}}, SHIFT(13),
  [199] = {.entry = {.count = 1, .reusable = false}}, SHIFT(56),
  [201] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_object_repeat1, 2), SHIFT_REPEAT(12),
  [204] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_object_repeat1, 2),
  [206] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_pair, 1, .production_id = 1),
  [208] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_pair, 1, .production_id = 1),
  [210] = {.entry = {.count = 1, .reusable = false}}, SHIFT(7),
  [212] = {.entry = {.count = 1, .reusable = false}}, SHIFT(52),
  [214] = {.entry = {.count = 1, .reusable = false}}, SHIFT(18),
  [216] = {.entry = {.count = 1, .reusable = false}}, SHIFT(46),
  [218] = {.entry = {.count = 1, .reusable = false}}, SHIFT(34),
  [220] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_multiline_string_repeat1, 2),
  [222] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_multiline_string_repeat1, 2), SHIFT_REPEAT(56),
  [225] = {.entry = {.count = 1, .reusable = false}}, SHIFT(10),
  [227] = {.entry = {.count = 1, .reusable = false}}, SHIFT(36),
  [229] = {.entry = {.count = 1, .reusable = false}}, SHIFT(55),
  [231] = {.entry = {.count = 1, .reusable = false}}, SHIFT(48),
  [233] = {.entry = {.count = 1, .reusable = false}}, SHIFT(49),
  [235] = {.entry = {.count = 1, .reusable = false}}, SHIFT(9),
  [237] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_array_repeat1, 2),
  [239] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_pair, 3, .production_id = 2),
  [241] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_pair, 3, .production_id = 2),
  [243] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_object_repeat1, 2),
  [245] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef _WIN32
#define extern __declspec(dllexport)
#endif

extern const TSLanguage *tree_sitter_json(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .field_names = ts_field_names,
    .field_map_slices = ts_field_map_slices,
    .field_map_entries = ts_field_map_entries,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
