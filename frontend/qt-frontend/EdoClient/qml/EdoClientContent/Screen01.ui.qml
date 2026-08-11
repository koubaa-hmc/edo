/*
 * Screen01 - Main Content Area
 *
 * UI component for EdoClient main screen with navigation and data display.
 * Pure UI file - NO logic, NO signals, NO handlers. Editable in Qt Design Studio.
 */
import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts
import "../EdoClient" as EdoClient

Rectangle {
    id: mainScreen

    color: EdoClient.Constants.lightGray
    
    // ========== EXPOSED REFERENCES (Qt Design Studio compatible) ==========
    // These aliases allow the wrapper to access internal items
    property alias navStack: navStack
    property alias navDatasets: navDatasets
    property alias navTimeseries: navTimeseries
    property alias navRdf: navRdf
    property alias navSettings: navSettings
    property alias importBtn: importBtn
    property alias roleGuest: roleGuest
    property alias roleFellow: roleFellow
    property alias roleSteward: roleSteward
    property alias roleAdmin: roleAdmin

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
            }
        }
    }

    // Stack for different views
    StackLayout {
        id: navStack
        anchors.top: navBar.bottom
        anchors.bottom: parent.bottom
        width: parent.width

        // Page 1: Datasets
        Rectangle {
            id: pageDatasets
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
            id: pageTimeseries
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
            id: pageRdf
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
            id: pageSettings
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
                        }

                        RadioButton {
                            id: roleFellow
                            text: "Research Fellow"
                        }

                        RadioButton {
                            id: roleSteward
                            text: "Data Steward"
                        }

                        RadioButton {
                            id: roleAdmin
                            text: "Administrator"
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
