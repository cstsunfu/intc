local configs = require("lspconfig.configs")
local util = require("lspconfig.util")
local capabilities = vim.lsp.protocol.make_client_capabilities()

configs.intc_lsp = {
	default_config = {
		cmd = { "intc-lsp" },

		root_dir = function(fname)
			local root = util.root_pattern(".intc.json*")(fname) -- or util.path.dirname(fname)
			if root == vim.g.HOME_PATH or root == nil then
				return nil
			end
			return root
		end,
		filetypes = { "jsonc", "yaml", "hjson", "json", "yml" },
		single_file_support = true,
	},
	docs = {
		package_json = "",
		description = [[
       intc language server
       ]],
	},
}

local common_config = {
	capabilities = capabilities,
	on_attach = function(_, _) end,
}

require("lspconfig")["intc_lsp"].setup(common_config)
