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
import "." as EdoClient

ApplicationWindow {
    id: mainWindow
    
    // Qt Design Studio event simulator (only active in QDS with QtQuick.Studio modules)
    // Commented out for runtime - uncomment when editing in Qt Design Studio
    /*
    EventListSimulator {
        id: eventSimulator
    }
    */
    
    width: EdoClient.Constants.width
    height: EdoClient.Constants.height
    visible: true
    title: qsTr("Energy Data Orchestrator")
    
    // Application-wide properties
    property string currentRole: "data_steward"
    property var currentData: null
    
    // Color scheme - HMC corporate colors (from Constants singleton)
    readonly property color primaryColor: EdoClient.Constants.primaryColor
    readonly property color secondaryColor: EdoClient.Constants.secondaryColor
    readonly property color backgroundColor: EdoClient.Constants.backgroundColor
    readonly property color accentColor: EdoClient.Constants.accentColor
    
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
                text: "Energy Data Orchestrator"
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
    Screen01Wrapper {
        id: mainScreen
        anchors.fill: parent
        
        onDataLoaded: function(data) {
            currentData = data
            statusLabel.text = "Data loaded: " + (data ? data.title || "Unknown" : "None")
        }
        
        onActionTriggered: function(actionId, params) {
            console.log("🔵 Action triggered:", actionId, JSON.stringify(params))
            console.log("pythonBridge available:", typeof pythonBridge !== 'undefined')
            statusLabel.text = "Executing: " + actionId
            // Forward to Python backend
            if (typeof pythonBridge !== 'undefined' && pythonBridge) {
                console.log("Calling pythonBridge.triggerAction...")
                pythonBridge.triggerAction(actionId, params)
            } else {
                console.warn("⚠️ pythonBridge not available!")
            }
        }
        
        onStatusMessage: function(message) {
            statusLabel.text = message
        }
        
        onRoleSelected: function(roleId) {
            setRole(roleId)
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
