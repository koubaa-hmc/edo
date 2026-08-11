

/*
 * Screen01 - Main Content Area
 *
 * UI component for EdoClient main screen with navigation and data display.
 */
import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts
import "../EdoClient" as EdoClient

Rectangle {
    id: mainScreen

    color: EdoClient.Constants.lightGray

    // Signals for Python integration
    signal dataLoaded(var data)
    signal actionTriggered(string actionId, var params)
    signal statusMessage(string message)
    signal roleSelected(string roleId)
    




    // Properties for external control
    property var externalData: null
    property bool triggerNewWorkspace: false

    // Navigation state
    property int currentNavIndex: 0

    // Top navigation bar
    Rectangle {
        id: navBar
        height: EdoClient.Constants.headerHeight - 10
        width: parent.width
        color: EdoClient.Constants.backgroundColor

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 15
            anchors.rightMargin: 15

            // Navigation buttons
            Button {
                id: navDatasets
                text: "Datasets"
                flat: false
                Layout.preferredWidth: 120
                rightPadding: 4
                bottomPadding: 4
                padding: 4
                leftPadding: 4
                topPadding: 4
                Layout.margins: 4
                Layout.leftMargin: 4
                Layout.topMargin: 4
                icon.cache: true
                icon.height: 16
                icon.width: 16
                display: AbstractButton.TextBesideIcon
                Layout.preferredHeight: 35
                icon.source: "images/layers.svg"
                
                onClicked: {
                    currentNavIndex = 0
                    mainScreen.actionTriggered("nav.datasets", {})
                }
            }

            Button {
                id: navTimeseries
                text: "Timeseries"
                flat: false
                Layout.preferredWidth: 120
                rightPadding: 4
                bottomPadding: 4
                padding: 4
                leftPadding: 4
                topPadding: 4
                Layout.margins: 4
                Layout.leftMargin: 4
                Layout.topMargin: 4
                icon.cache: true
                icon.height: 16
                icon.width: 16
                display: AbstractButton.TextBesideIcon
                Layout.preferredHeight: 35
                icon.source: "images/folder-clock.svg"
                
                onClicked: {
                    currentNavIndex = 1
                    mainScreen.actionTriggered("nav.timeseries", {})
                }
            }

            Button {
                id: navRdf
                text: "RDF Graph"
                flat: false
                Layout.preferredWidth: 120
                rightPadding: 4
                bottomPadding: 4
                padding: 4
                leftPadding: 4
                topPadding: 4
                Layout.margins: 4
                Layout.leftMargin: 4
                Layout.topMargin: 4
                icon.cache: true
                icon.height: 16
                icon.width: 16
                display: AbstractButton.TextBesideIcon
                Layout.preferredHeight: 35
                icon.source: "images/share-2.svg"
                
                onClicked: {
                    currentNavIndex = 2
                    mainScreen.actionTriggered("nav.rdf", {})
                }
            }

            Button {
                id: navSettings
                text: "Settings"
                flat: false
                Layout.preferredWidth: 120
                rightPadding: 4
                bottomPadding: 4
                padding: 4
                leftPadding: 4
                topPadding: 4
                Layout.margins: 4
                Layout.leftMargin: 4
                Layout.topMargin: 4
                icon.cache: true
                icon.height: 16
                icon.width: 16
                display: AbstractButton.TextBesideIcon
                Layout.preferredHeight: 35
                icon.source: "images/settings.svg"
                
                onClicked: {
                    currentNavIndex = 3
                    mainScreen.actionTriggered("nav.settings", {})
                }
            }

            Item {
                Layout.fillWidth: true
            }

            // Action buttons
            Button {
                id: importBtn
                text: "Import"
                flat: false
                Layout.preferredWidth: 120
                rightPadding: 4
                bottomPadding: 4
                padding: 4
                leftPadding: 4
                topPadding: 4
                Layout.margins: 4
                Layout.leftMargin: 4
                Layout.topMargin: 4
                icon.cache: true
                icon.height: 16
                icon.width: 16
                display: AbstractButton.TextBesideIcon
                Layout.preferredHeight: 35
                icon.source: "images/download.svg"
                visible: true
                
                onClicked: mainScreen.actionTriggered("data.import", {})
            }
        }
    }

    // Stack for different views
    StackLayout {
        id: navStack
        currentIndex: currentNavIndex
        anchors.top: navBar.bottom
        anchors.bottom: parent.bottom
        width: parent.width

        // Page 1: Datasets
        Rectangle {
            color: EdoClient.Constants.lightGray

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: EdoClient.Constants.defaultMargin
                spacing: EdoClient.Constants.smallMargin + 5

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
            color: EdoClient.Constants.lightGray

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: EdoClient.Constants.defaultMargin
                spacing: EdoClient.Constants.smallMargin + 5

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
            color: EdoClient.Constants.lightGray

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: EdoClient.Constants.defaultMargin
                spacing: EdoClient.Constants.smallMargin + 5

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
            color: EdoClient.Constants.lightGray

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: EdoClient.Constants.defaultMargin
                spacing: EdoClient.Constants.smallMargin + 5

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

                        // Role radio buttons
                        RadioButton {
                            id: roleGuest
                            text: "Guest Viewer"
                            checked: true
                            property string roleValue: "guest_viewer"
                            
                            onToggled: {
                                if (checked) mainScreen.roleSelected(roleGuest.roleValue)
                            }
                        }

                        RadioButton {
                            id: roleFellow
                            text: "Research Fellow"
                            property string roleValue: "research_fellow"
                            
                            onToggled: {
                                if (checked) mainScreen.roleSelected(roleFellow.roleValue)
                            }
                        }

                        RadioButton {
                            id: roleSteward
                            text: "Data Steward"
                            property string roleValue: "data_steward"
                            
                            onToggled: {
                                if (checked) mainScreen.roleSelected(roleSteward.roleValue)
                            }
                        }

                        RadioButton {
                            id: roleAdmin
                            text: "Administrator"
                            property string roleValue: "admin"
                            
                            onToggled: {
                                if (checked) mainScreen.roleSelected(roleAdmin.roleValue)
                            }
                        }
                    }
                }
            }
        }
    }

    // Note: ContentArea to be added in wrapper component
    // Placeholder for dynamic content
    Rectangle {
        id: contentPlaceholder
        anchors.fill: parent
        color: "transparent"
        visible: false
    }
}
