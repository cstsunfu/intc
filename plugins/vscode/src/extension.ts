/* -------------------------------------------------------------------------
 * Copyright the author(s) of intc.
 *
 * This source code is licensed under the Apache license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * There are some code copy from the pygls,
 * The code copied Copyright (c) Microsoft Corporation and Open Law Library.
 * ----------------------------------------------------------------------- */
"use strict";

import * as net from "net";
import * as path from "path";
import * as vscode from "vscode";
import * as semver from "semver";
import { workspace, commands, languages, window } from "vscode"

import { PythonExtension } from "@vscode/python-extension";
import { LanguageClient, LanguageClientOptions, ServerOptions, State, integer } from "vscode-languageclient/node";

const MIN_PYTHON = semver.parse("3.8.0")

let client: LanguageClient;
let clientStarting = false
let python: PythonExtension;
let logger: vscode.LogOutputChannel
// opend document set
let openDocuments = new Set<string>()

/**
 * This is the main entry point.
 * Called when vscode first activates the extension
 */
export async function activate(context: vscode.ExtensionContext) {
    logger = vscode.window.createOutputChannel('intclsp', { log: true })
    logger.info("Extension activated.")

    await getPythonExtension();
    if (!python) {
        return
    }

    // Restart language server command
    context.subscriptions.push(
        vscode.commands.registerCommand("intclsp.server.restart", async () => {
            logger.info('restarting server...')
            await startLangServer(null)
        })
    )

    // Execute command... command
    context.subscriptions.push(
        vscode.commands.registerCommand("intclsp.server.executeCommand", async () => {
            await executeServerCommand()
        })
    )

    // Restart the language server if the user switches Python envs...
    context.subscriptions.push(
        python.environments.onDidChangeActiveEnvironmentPath(async () => {
            logger.info('python env modified, restarting server...')
            // only restart if the server is already running
            if (client) {
                await startLangServer(null)
            }
        })
    )

    // ... or if they change a relevant config option
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(async (event) => {
            if (event.affectsConfiguration("intclsp.server") || event.affectsConfiguration("intclsp.client")) {
                if (client) {
                    logger.info('config modified, restarting server...')
                    await startLangServer(null)
                }
            }
        })
    )
    // remove the document from the openDocuments when the document is closed
    context.subscriptions.push(
        vscode.workspace.onDidCloseTextDocument(
            async (event) => {
                if (event.languageId === "json" || event.languageId === "jsonc") {
                    if (openDocuments.has(event.fileName)) {
                        openDocuments.delete(event.fileName)
                    }
                }
            }
        )
    )

    // restart the language server once the user opens the text document...
    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(
            async (event: vscode.TextDocument) => {
                await onOpenOrActiveDocument(event)
            }
        )
    )
}


/**
 * This function is called when the extension is activated.
 * It will be called the first time a command is executed.
 * @param event The event that triggered this function.
 * @returns
 */
async function onOpenOrActiveDocument(event: vscode.TextDocument) {
    if (event.languageId === "json" || event.languageId === "jsonc") {
        // if client is running and the file is in the openDocuments
        if (client && openDocuments.has(event.fileName)) {
            return
        }
        const rootPath = vscode.workspace.workspaceFolders[0].uri.fsPath
        let realRoot = path.dirname(event.fileName)
        // if the filePath is not in the workspace root
        if (!realRoot.startsWith(rootPath)) {
            return
        }
        if (path.dirname(rootPath) === rootPath) {
            return
        }
        while (realRoot !== path.dirname(rootPath)) {
            let intcConfig = path.join(realRoot, ".intc.json")
            let intcConfigc = path.join(realRoot, ".intc.jsonc")
            if (await workspace.fs.stat(vscode.Uri.file(intcConfig)).then(() => true, () => false)) {
                await startLangServer(event.fileName)
                return
            }
            if (await workspace.fs.stat(vscode.Uri.file(intcConfigc)).then(() => true, () => false)) {
                await startLangServer(event.fileName)
                return
            }
            realRoot = path.dirname(realRoot)
        }
    }
    return
}


export function deactivate(): Thenable<void> {
    return stopLangServer()
}
/**
 * Start (or restart) the language server.
 *
 * @param command The executable to run
 * @param args Arguments to pass to the executable
 * @param cwd The working directory in which to run the executable
 * @returns
 */
async function startLangServer(filePath: string | null) {

    // Don't interfere if we are already in the process of launching the server.
    if (clientStarting) {
        return
    }

    clientStarting = true
    if (client) {
        await stopLangServer()
    }
    const config = vscode.workspace.getConfiguration("intclsp.server")

    const cwd = getCwd()

    const resource = vscode.Uri.joinPath(vscode.Uri.file(cwd))
    const pythonCommand = await getPythonCommand(resource)
    if (!pythonCommand) {
        clientStarting = false
        return
    }

    logger.debug(`python: ${pythonCommand.join(" ")}`)
    const serverOptions: ServerOptions = {
        command: pythonCommand[0],
        args: [...pythonCommand.slice(1), "-m", "intc_lsp.cli"],
        //options: { cwd: "/home/sun/workspace/intc/intc/examples/exp1" },
    };

    client = new LanguageClient('intclsp', serverOptions, getClientOptions());
    const promises = [client.start()]

    if (config.get<boolean>("debug")) {
        promises.push(startDebugging())
    }

    const results = await Promise.allSettled(promises)
    clientStarting = false
    let success = true

    for (const result of results) {
        if (result.status === "rejected") {
            logger.error(`There was a error starting the server: ${result.reason}`)
            success = false
        }
    }
    if (success && filePath) {
        openDocuments.add(filePath)
    }
}

async function stopLangServer(): Promise<void> {
    if (!client) {
        return
    }

    if (client.state === State.Running) {
        await client.stop()
    }

    client.dispose()
    client = undefined
    openDocuments.clear()
}

function startDebugging(): Promise<void> {
    if (!vscode.workspace.workspaceFolders) {
        logger.error("Unable to start debugging, there is no workspace.")
        return Promise.reject("Unable to start debugging, there is no workspace.")
    }
    // TODO: Is there a more reliable way to ensure the debug adapter is ready?
    setTimeout(async () => {
        await vscode.debug.startDebugging(vscode.workspace.workspaceFolders[0], "intclsp: Debug Server")
    }, 2000)
}

function getClientOptions(): LanguageClientOptions {
    const options = {
        documentSelector: [{
            "scheme": "file",
            "language": "jsonc"
        }, {
            "scheme": "file",
            "language": "json"
        }],
        outputChannel: logger,
        connectionOptions: {
            maxRestartCount: 0 // don't restart on server failure.
        },
    };
    logger.info(`client options: ${JSON.stringify(options, undefined, 2)}`)
    return options
}

function startLangServerTCP(addr: number): LanguageClient {
    const serverOptions: ServerOptions = () => {
        return new Promise((resolve /*, reject */) => {
            const clientSocket = new net.Socket();
            clientSocket.connect(addr, "127.0.0.1", () => {
                resolve({
                    reader: clientSocket,
                    writer: clientSocket,
                });
            });
        });
    };


    return new LanguageClient(
        `tcp lang server (port ${addr})`,
        serverOptions,
        getClientOptions()
    );
}

/**
 * Execute a command provided by the language server.
 */
async function executeServerCommand() {
    if (!client || client.state !== State.Running) {
        await vscode.window.showErrorMessage("There is no language server running.")
        return
    }

    const knownCommands = client.initializeResult.capabilities.executeCommandProvider?.commands
    if (!knownCommands || knownCommands.length === 0) {
        const info = client.initializeResult.serverInfo
        const name = info?.name || "Server"
        const version = info?.version || ""

        await vscode.window.showInformationMessage(`${name} ${version} does not implement any commands.`)
        return
    }

    const commandName = await vscode.window.showQuickPick(knownCommands, { canPickMany: false })
    if (!commandName) {
        return
    }
    logger.info(`executing command: '${commandName}'`)

    const result = await vscode.commands.executeCommand(commandName /* if your command accepts arguments you can pass them here */)
    logger.info(`${commandName} result: ${JSON.stringify(result, undefined, 2)}`)
}

/**
 * If the user has explicitly provided a src directory use that.
 * Otherwise, fallback to the examples/servers directory.
 *
 * @returns The working directory from which to launch the server
 */
function getCwd(): string {
    const config = vscode.workspace.getConfiguration("intclsp.server")
    const cwd = config.get<string>('cwd')
    if (cwd) {
        return cwd
    }

    return "."
}

/**
 * Return the python command to use when starting the server.
 *
 * If debugging is enabled, this will also included the arguments to required
 * to wrap the server in a debug adapter.
 *
 * @returns The full python command needed in order to start the server.
 */
async function getPythonCommand(resource?: vscode.Uri): Promise<string[] | undefined> {
    const config = vscode.workspace.getConfiguration("intclsp.server", resource)
    const pythonPath = await getPythonInterpreter(resource)
    if (!pythonPath) {
        return
    }
    const command = [pythonPath]

    return command
}

/**
 * Return the python interpreter to use when starting the server.
 *
 * This uses the official python extension to grab the user's currently
 * configured environment.
 *
 * @returns The python interpreter to use to launch the server
 */
async function getPythonInterpreter(resource?: vscode.Uri): Promise<string | undefined> {
    const config = vscode.workspace.getConfiguration("intclsp.server", resource)
    const pythonPath = config.get<string>('pythonPath')
    if (pythonPath) {
        logger.info(`Using user configured python environment: '${pythonPath}'`)
        return pythonPath
    }

    if (!python) {
        return
    }

    if (resource) {
        logger.info(`Looking for environment in which to execute: '${resource.toString()}'`)
    }
    // Use whichever python interpreter the user has configured.
    const activeEnvPath = python.environments.getActiveEnvironmentPath(resource)
    logger.info(`Found environment: ${activeEnvPath.id}: ${activeEnvPath.path}`)

    const activeEnv = await python.environments.resolveEnvironment(activeEnvPath)
    if (!activeEnv) {
        logger.error(`Unable to resolve envrionment: ${activeEnvPath}`)
        return
    }

    const v = activeEnv.version
    const pythonVersion = semver.parse(`${v.major}.${v.minor}.${v.micro}`)

    // Check to see if the environment satisfies the min Python version.
    if (semver.lt(pythonVersion, MIN_PYTHON)) {
        const message = [
            `Your currently configured environment provides Python v${pythonVersion} `,
            `but intclsp requires v${MIN_PYTHON}.\n\nPlease choose another environment.`
        ].join('')

        const response = await vscode.window.showErrorMessage(message, "Change Environment")
        if (!response) {
            return
        } else {
            await vscode.commands.executeCommand('python.setInterpreter')
            return
        }
    }

    const pythonUri = activeEnv.executable.uri
    if (!pythonUri) {
        logger.error(`URI of Python executable is undefined!`)
        return
    }

    return pythonUri.fsPath
}

async function getPythonExtension() {
    try {
        python = await PythonExtension.api();
    } catch (err) {
        logger.error(`Unable to load python extension: ${err}`)
    }
}
