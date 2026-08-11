/*
 * Screen01 - Main Content Area
 * 
 * This is a UI file (.ui.qml) designed for Qt Design Studio.
 * It provides the main content area with navigation and data display.
 */

import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts

Rectangle {
    id: mainScreen
    
    color: "#f5f5f5"
    
    // Signals for Python integration
    signal dataLoaded(var data)
    signal actionTriggered(string actionId, var params)
    signal statusMessage(string message)
    
    // Public functions
    function displayData(data) {
        contentArea.currentData = data
        contentArea.load()
    }
    
    function newWorkspace() {
        contentArea.clear()
        statusMessage("New workspace created")
    }
    
    // Top navigation bar
    Rectangle {
        id: navBar
        height: 50
        width: parent.width
        color: "white"
        
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 15
            anchors.rightMargin: 15
            
            // Navigation buttons
            Repeater {
                model: [
                    { label: "📊 Datasets", id: "nav_datasets" },
                    { label: "📈 Timeseries", id: "nav_timeseries" },
                    { label: "🔗 RDF Graph", id: "nav_rdf" },
                    { label: "⚙️ Settings", id: "nav_settings" }
                ]
                
                delegate: Button {
                    text: modelData.label
                    Layout.preferredHeight: 35
                    
                    FlatButtonBackground {
                        id: navBtnBg
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        color: "#333"
                    }
                    
                    component FlatButtonBackground: Rectangle {
                        color: parent.parent.pressed ? "#e0e0e0" : (parent.parent.hovered ? "#f0f0f0" : "transparent")
                        radius: 4
                    }
                    
                    onClicked: {
                        if (modelData.id === "nav_datasets") {
                            navStack.currentIndex = 0
                        } else if (modelData.id === "nav_timeseries") {
                            navStack.currentIndex = 1
                        } else if (modelData.id === "nav_rdf") {
                            navStack.currentIndex = 2
                        } else if (modelData.id === "nav_settings") {
                            navStack.currentIndex = 3
                        }
                    }
                }
            }
            
            Item { Layout.fillWidth: true }
            
            // Action buttons
            Button {
                id: importBtn
                text: "Import"
                visible: mainScreen.parent && mainScreen.parent.currentRole !== "guest_viewer"
                
                background: Rectangle {
                    color: importBtn.pressed ? "#004B87" : (importBtn.hovered ? "#005CA3" : "#00305E")
                    radius: 4
                }
                
                contentItem: Text {
                    text: importBtn.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    actionTriggered("data.import", {})
                }
            }
        }
    }
    
    // Stack for different views
    StackLayout {
        id: navStack
        currentIndex: 0
        anchors.top: navBar.bottom
        anchors.bottom: parent.bottom
        width: parent.width
        
        // Page 1: Datasets
        Rectangle {
            color: "#f5f5f5"
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15
                
                Label {
                    text: "Datasets"
                    font.pixelSize: 24
                    font.bold: true
                    color: "#333"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "white"
                    radius: 8
                    
                    border.color: "#dee2e6"
                    border.width: 1
                    
                    Label {
                        anchors.centerIn: parent
                        text: "Dataset Browser\n\nImport or select a dataset to begin"
                        horizontalAlignment: Text.AlignHCenter
                        color: "#6c757d"
                        font.pixelSize: 16
                    }
                }
            }
        }
        
        // Page 2: Timeseries
        Rectangle {
            color: "#f5f5f5"
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15
                
                Label {
                    text: "Timeseries Data"
                    font.pixelSize: 24
                    font.bold: true
                    color: "#333"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "white"
                    radius: 8
                    
                    border.color: "#dee2e6"
                    border.width: 1
                    
                    Label {
                        anchors.centerIn: parent
                        text: "Timeseries Grid\n\nLoad timeseries data to view"
                        horizontalAlignment: Text.AlignHCenter
                        color: "#6c757d"
                        font.pixelSize: 16
                    }
                }
            }
        }
        
        // Page 3: RDF
        Rectangle {
            color: "#f5f5f5"
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15
                
                Label {
                    text: "RDF Knowledge Graph"
                    font.pixelSize: 24
                    font.bold: true
                    color: "#333"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "white"
                    radius: 8
                    
                    border.color: "#dee2e6"
                    border.width: 1
                    
                    Label {
                        anchors.centerIn: parent
                        text: "RDF Inspector\n\nLoad RDF data to inspect"
                        horizontalAlignment: Text.AlignHCenter
                        color: "#6c757d"
                        font.pixelSize: 16
                    }
                }
            }
        }
        
        // Page 4: Settings
        Rectangle {
            color: "#f5f5f5"
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15
                
                Label {
                    text: "Settings"
                    font.pixelSize: 24
                    font.bold: true
                    color: "#333"
                }
                
                GroupBox {
                    title: "User Role"
                    Layout.fillWidth: true
                    
                    ColumnLayout {
                        anchors.fill: parent
                        
                        RadioButton {
                            id: roleGuest
                            text: "Guest Viewer"
                            checked: mainScreen.parent ? mainScreen.parent.currentRole === "guest_viewer" : false
                            onClicked: {
                                if (mainScreen.parent) mainScreen.parent.setRole("guest_viewer")
                            }
                        }
                        
                        RadioButton {
                            id: roleFellow
                            text: "Research Fellow"
                            checked: mainScreen.parent ? mainScreen.parent.currentRole === "research_fellow" : false
                            onClicked: {
                                if (mainScreen.parent) mainScreen.parent.setRole("research_fellow")
                            }
                        }
                        
                        RadioButton {
                            id: roleSteward
                            text: "Data Steward"
                            checked: mainScreen.parent ? mainScreen.parent.currentRole === "data_steward" : false
                            onClicked: {
                                if (mainScreen.parent) mainScreen.parent.setRole("data_steward")
                            }
                        }
                        
                        RadioButton {
                            id: roleAdmin
                            text: "Administrator"
                            checked: mainScreen.parent ? mainScreen.parent.currentRole === "admin" : false
                            onClicked: {
                                if (mainScreen.parent) mainScreen.parent.setRole("admin")
                            }
                        }
                    }
                }
            }
        }
    }
    
    // Content overlay for displaying loaded data
    ContentArea {
        id: contentArea
        anchors.fill: parent
        visible: currentData !== null
    }
}
