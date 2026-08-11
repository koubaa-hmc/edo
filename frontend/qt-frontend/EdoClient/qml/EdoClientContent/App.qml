/*
 * EDO Client - Main Application Window
 * 
 * This file is designed to be edited in Qt Design Studio.
 * The window integrates with Python backend via PyQt6.
 */

import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    id: mainWindow
    
    width: 1920
    height: 1080
    visible: true
    title: qsTr("Energy Data Orchestrator")
    
    // Application-wide properties
    property string currentRole: "data_steward"
    property var currentData: null
    
    // Color scheme - HMC corporate colors
    readonly property color primaryColor: "#00305E"
    readonly property color secondaryColor: "#004B87"
    readonly property color backgroundColor: "#FFFFFF"
    readonly property color accentColor: "#0066CC"
    
    header: ToolBar {
        height: 60
        background: Rectangle {
            color: mainWindow.primaryColor
        }
        
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            
            Label {
                text: "🧠 Energy Data Orchestrator"
                color: "white"
                font.pixelSize: 24
                font.bold: true
            }
            
            Item { Layout.fillWidth: true }
            
            // Role indicator
            Label {
                text: "Role: " + mainWindow.currentRole
                color: "white"
                font.pixelSize: 14
                opacity: 0.8
            }
        }
    }
    
    footer: ToolBar {
        height: 30
        background: Rectangle {
            color: "#f8f9fa"
            border.color: "#dee2e6"
            border.width: 1
        }
        
        Label {
            id: statusLabel
            text: "Ready"
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            color: "#495057"
        }
    }
    
    // Main content area
    Screen01 {
        id: mainScreen
        anchors.fill: parent
        
        onDataLoaded: {
            currentData = data
            statusLabel.text = "Data loaded: " + (data ? data.title || "Unknown" : "None")
        }
        
        onActionTriggered: {
            console.log("Action triggered:", actionId, params)
            statusLabel.text = "Executing: " + actionId
        }
        
        onStatusMessage: {
            statusLabel.text = message
        }
    }
    
    // Keyboard shortcuts
    Shortcut {
        sequence: "Ctrl+Q"
        onActivated: Qt.quit()
    }
    
    Shortcut {
        sequence: "Ctrl+N"
        onActivated: {
            console.log("New workspace")
            mainScreen.newWorkspace()
        }
    }
    
    // Expose functions for Python integration
    function loadDataset(data) {
        currentData = data
        mainScreen.displayData(data)
        statusLabel.text = "Dataset loaded: " + (data.title || "Unknown")
    }
    
    function setRole(roleId) {
        currentRole = roleId
        statusLabel.text = "Role changed to: " + roleId
    }
    
    function showStatus(message) {
        statusLabel.text = message
    }
}
