const express    = require("express");
const http       = require("http");
const { Server } = require("socket.io");
const axios      = require("axios");
const tabManager = require("./tabManager");

const app    = express();
const server = http.createServer(app);
const io     = new Server(server, { cors: { origin: "*" } });

const DJANGO_URL = "http://localhost:8000/api";

io.on("connection", (socket) => {
    console.log("Client connected:", socket.id);

    socket.on("new_tab", () => {
        const tabId = tabManager.createTab();
        socket.emit("tab_created", { tabId, tabs: tabManager.getAllTabs() });
    });

    socket.on("close_tab", ({ tabId }) => {
        tabManager.closeTab(tabId);
        socket.emit("tab_closed", { tabId, tabs: tabManager.getAllTabs() });
    });

    socket.on("run_command", async ({ command, tabId }) => {
        if (!tabManager.getTab(tabId)) {
            tabManager.createTab(tabId);
        }

        socket.emit("command_start", { tabId, command });

        try {
            const response = await axios.post(`${DJANGO_URL}/run/`, {
                command,
                tab_id: tabId
            });

            const result = response.data;
            tabManager.addToHistory(tabId, command, result);

            socket.emit("command_result", {
                tabId,
                command,
                output:    result.output,
                error:     result.error,
                cwd:       result.cwd,
                exit_code: result.exit_code
            });

        } catch (err) {
            socket.emit("command_result", {
                tabId,
                command,
                output: "",
                error:  "Node server error: " + err.message,
                cwd:    "~"
            });
        }
    });

    socket.on("get_tabs", () => {
        socket.emit("tabs_list", { tabs: tabManager.getAllTabs() });
    });

    socket.on("disconnect", () => {
        console.log("Client disconnected:", socket.id);
    });
});

server.listen(3000, () => {
    console.log("Node.js server running on port 3000");
});