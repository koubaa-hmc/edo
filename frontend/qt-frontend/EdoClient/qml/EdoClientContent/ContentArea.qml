/*
 * ContentArea - Dynamic data display component
 * 
 * Displays loaded data using appropriate view based on data type.
 */

import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts

Rectangle {
    id: contentArea
    
    color: "white"
    visible: false
    
    property var currentData: null
    
    signal closeRequested()
    
    function load() {
        if (!currentData) return
        
        // Determine data type and show appropriate view
        if (currentData.title && currentData.resources) {
            stackLayout.currentIndex = 0  // Dataset view
        } else if (currentData.timestamps && currentData.values) {
            stackLayout.currentIndex = 1  // Timeseries view
        } else if (currentData.uri || currentData["@type"]) {
            stackLayout.currentIndex = 2  // RDF view
        } else if (currentData.columns && currentData.rows) {
            stackLayout.currentIndex = 3  // Table view
        } else {
            stackLayout.currentIndex = 4  // Generic view
        }
        
        visible = true
    }
    
    function clear() {
        currentData = null
        visible = false
    }
    
    // Close button
    Rectangle {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 10
        width: 30
        height: 30
        radius: 15
        color: "#dc3545"
        
        Text {
            anchors.centerIn: parent
            text: "✕"
            color: "white"
            font.pixelSize: 18
        }
        
        MouseArea {
            anchors.fill: parent
            onClicked: closeRequested()
        }
    }
    
    StackLayout {
        id: stackLayout
        currentIndex: 0
        anchors.fill: parent
        anchors.margins: 20
        
        // View 1: Dataset Browser
        Rectangle {
            color: "transparent"
            
            ColumnLayout {
                anchors.fill: parent
                spacing: 15
                
                Label {
                    text: currentData ? currentData.title : "Dataset"
                    font.pixelSize: 28
                    font.bold: true
                    color: "#333"
                }
                
                Label {
                    text: currentData ? currentData.description : ""
                    wrapMode: Text.WordWrap
                    color: "#666"
                    font.pixelSize: 16
                }
                
                Label {
                    text: "Resources:"
                    font.pixelSize: 18
                    font.bold: true
                    color: "#333"
                }
                
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    model: currentData ? currentData.resources : []
                    
                    delegate: Rectangle {
                        width: parent.width
                        height: 50
                        color: index % 2 === 0 ? "#f8f9fa" : "white"
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 15
                            anchors.rightMargin: 15
                            
                            Label {
                                text: modelData.name || "Unknown"
                                font.bold: true
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            Label {
                                text: modelData.format || "?"
                                color: "#666"
                            }
                            
                            Label {
                                text: modelData.size || "?"
                                color: "#666"
                                leftPadding: 20
                            }
                        }
                    }
                }
            }
        }
        
        // View 2: Timeseries Grid
        Rectangle {
            color: "transparent"
            
            ColumnLayout {
                anchors.fill: parent
                spacing: 15
                
                Label {
                    text: "Timeseries Data"
                    font.pixelSize: 24
                    font.bold: true
                }
                
                Label {
                    text: currentData ? "Data Points: " + currentData.timestamps.length : ""
                    color: "#666"
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    
                    TableView {
                        id: timeseriesTable
                        width: parent.width
                        height: Math.min(400, currentData ? currentData.timestamps.length * 30 : 0)
                        
                        columnSpacing: 1
                        rowSpacing: 1
                        
                        model: ListModel {
                            dynamicRoles: true
                            Component.onCompleted: {
                                if (currentData && currentData.timestamps) {
                                    for (var i = 0; i < Math.min(currentData.timestamps.length, 100); i++) {
                                        append({"timestamp": currentData.timestamps[i], "value": currentData.values[i]})
                                    }
                                }
                            }
                        }
                        
                        delegate: Rectangle {
                            color: "white"
                            border.color: "#dee2e6"
                            
                            Text {
                                anchors.centerIn: parent
                                text: model[index] ? (model[index][role] || "") : ""
                            }
                        }
                    }
                }
            }
        }
        
        // View 3: RDF Inspector
        Rectangle {
            color: "transparent"
            
            ColumnLayout {
                anchors.fill: parent
                spacing: 15
                
                Label {
                    text: "RDF Resource"
                    font.pixelSize: 24
                    font.bold: true
                }
                
                Label {
                    text: currentData ? "URI: " + (currentData.uri || currentData["@id"] || "Unknown") : ""
                    font.family: "Courier New"
                    color: "#0066cc"
                    wrapMode: Text.WrapAnywhere
                }
                
                Label {
                    text: currentData ? "Type: " + (currentData["@type"] || "Unknown") : ""
                    font.bold: true
                    color: "#666"
                }
                
                Label {
                    text: "Properties:"
                    font.pixelSize: 18
                    font.bold: true
                }
                
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    model: currentData ? Object.keys(currentData).filter(k => !k.startsWith("@") && k !== "uri") : []
                    
                    delegate: Rectangle {
                        width: parent.width
                        height: 40
                        color: index % 2 === 0 ? "#f8f9fa" : "white"
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 15
                            anchors.rightMargin: 15
                            
                            Label {
                                text: modelData
                                font.bold: true
                                width: 200
                            }
                            
                            Label {
                                text: String(currentData[modelData])
                                color: "#666"
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }
        }
        
        // View 4: Table Viewer
        Rectangle {
            color: "transparent"
            
            ColumnLayout {
                anchors.fill: parent
                spacing: 15
                
                Label {
                    text: "Table Data"
                    font.pixelSize: 24
                    font.bold: true
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    
                    ListView {
                        model: currentData ? currentData.rows.length : 0
                        
                        header: Rectangle {
                            width: parent.width
                            height: 40
                            color: "#e9ecef"
                            
                            Row {
                                anchors.fill: parent
                                anchors.leftMargin: 10
                                
                                Repeater {
                                    model: currentData ? currentData.columns.length : 0
                                    Label {
                                        width: 150
                                        text: currentData ? currentData.columns[index] : ""
                                        font.bold: true
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }
                        
                        delegate: Rectangle {
                            width: parent.width
                            height: 35
                            color: index % 2 === 0 ? "#f8f9fa" : "white"
                            
                            Row {
                                anchors.fill: parent
                                anchors.leftMargin: 10
                                
                                Repeater {
                                    model: currentData ? currentData.columns.length : 0
                                    Label {
                                        width: 150
                                        text: currentData && currentData.rows[index] ? 
                                              String(currentData.rows[index][index]) : ""
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // View 5: Generic/Fallback
        Rectangle {
            color: "transparent"
            
            ColumnLayout {
                anchors.fill: parent
                spacing: 15
                
                Label {
                    text: "Data Preview"
                    font.pixelSize: 24
                    font.bold: true
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    
                    TextArea {
                        readOnly: true
                        text: currentData ? JSON.stringify(currentData, null, 2) : ""
                        font.family: "Courier New"
                        font.pixelSize: 12
                        wrapMode: TextArea.Wrap
                    }
                }
            }
        }
    }
}
