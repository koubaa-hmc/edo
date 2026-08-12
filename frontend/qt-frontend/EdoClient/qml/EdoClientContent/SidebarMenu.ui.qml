/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../EdoClient" as EdoClient

Item {
    id: sidebarRoot
    width: 280
    height: 800

    // User info properties (set by parent)
    property string userName: "Guest User"
    property string userRole: "guest_viewer"

    // Expose workflow buttons (wrapper type with clicked signal)
    property var planButton: planButton
    property var collectButton: collectButton
    property var processButton: processButton
    property var analyzeButton: analyzeButton
    property var preserveButton: preserveButton
    property var shareButton: shareButton
    property var reuseButton: reuseButton

    // Signal for exit request
    signal exitRequested()

    // Signal for workflow navigation (emitted by parent via button connections)
    signal workflowRequested(string step)

    // Background panel of the drawer
    Rectangle {
        id: backgroundRect
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: parent.width
        color: "#ffffff"
        border.color: "#e0e0e0"
        border.width: 1

        // Main layout
        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // === USER INFO HEADER ===
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color: "#f8f9fa"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 12

                    // User avatar placeholder
                    Rectangle {
                        Layout.preferredWidth: 48
                        Layout.preferredHeight: 48
                        radius: 24
                        color: "#4a90d9"

                        Label {
                            anchors.centerIn: parent
                            text: userName.charAt(0).toUpperCase()
                            font.pixelSize: 20
                            font.bold: true
                            color: "#ffffff"
                        }
                    }

                    // User details
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 4

                        Label {
                            Layout.fillWidth: true
                            text: userName
                            font.pixelSize: 14
                            font.bold: true
                            color: "#1a1a1a"
                            elide: Label.ElideRight
                        }

                        Rectangle {
                            Layout.preferredHeight: 20
                            Layout.preferredWidth: parent.width
                            radius: 4
                            color: "#6b7280"

                            Label {
                                anchors.centerIn: parent
                                text: "GUEST VIEWER"
                                font.pixelSize: 10
                                font.bold: true
                                color: "#ffffff"
                            }
                        }
                    }
                }
            }

            // === WORKFLOW SECTION ===
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: "#e0e0e0"
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                ColumnLayout {
                    width: sidebarRoot.width - 32
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 16
                    spacing: 4

                    // Section title
                    Label {
                        Layout.fillWidth: true
                        Layout.margins: 4
                        text: "FAIR Data Lifecycle"
                        font.pixelSize: 11
                        font.bold: true
                        color: "#666666"
                    }

                    // PLAN
                    EdoClient.WorkflowButton {
                        id: planButton
                        Layout.fillWidth: true
                        iconSource: "../EdoClientContent/images/icons/file-pen.svg"
                        labelText: "Plan"
                        description: "Data management planning"
                    }

                    // COLLECT
                    EdoClient.WorkflowButton {
                        id: collectButton
                        Layout.fillWidth: true
                        iconSource: "../EdoClientContent/images/icons/upload.svg"
                        labelText: "Collect"
                        description: "Generate or acquire data"
                    }

                    // PROCESS
                    EdoClient.WorkflowButton {
                        id: processButton
                        Layout.fillWidth: true
                        iconSource: "../EdoClientContent/images/icons/code-2.svg"
                        labelText: "Process"
                        description: "Clean and transform data"
                    }

                    // ANALYZE
                    EdoClient.WorkflowButton {
                        id: analyzeButton
                        Layout.fillWidth: true
                        iconSource: "../EdoClientContent/images/icons/search-code.svg"
                        labelText: "Analyze"
                        description: "Extract insights from data"
                    }

                    // PRESERVE
                    EdoClient.WorkflowButton {
                        id: preserveButton
                        Layout.fillWidth: true
                        iconSource: "../EdoClientContent/images/icons/shield-check.svg"
                        labelText: "Preserve"
                        description: "Long-term storage & integrity"
                    }

                    // SHARE
                    EdoClient.WorkflowButton {
                        id: shareButton
                        Layout.fillWidth: true
                        iconSource: "../EdoClientContent/images/icons/share-2.svg"
                        labelText: "Share"
                        description: "Make data discoverable"
                    }

                    // REUSE
                    EdoClient.WorkflowButton {
                        id: reuseButton
                        Layout.fillWidth: true
                        iconSource: "../EdoClientContent/images/icons/link-2.svg"
                        labelText: "Reuse"
                        description: "Apply data to new research"
                    }
                }
            }

            // === BOTTOM SPACER ===
            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: 16
            }

            // === DIVIDER ===
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: "#e0e0e0"
            }

            // === EXIT BUTTON ===
            Button {
                id: exitButton
                Layout.fillWidth: true
                Layout.margins: 16
                Layout.preferredHeight: 44

                background: Rectangle {
                    anchors.fill: parent
                    radius: 8
                    color: "#fef2f2"
                    border.color: "#ef4444"
                    border.width: 1
                }

                contentItem: RowLayout {
                    anchors.centerIn: parent
                    spacing: 12

                    Image {
                        Layout.preferredWidth: 20
                        Layout.preferredHeight: 20
                        source: "../EdoClientContent/images/icons/log-in.svg"
                        fillMode: Image.PreserveAspectFit
                        visible: status === Image.Ready
                    }

                    Label {
                        text: "Exit Application"
                        font.pixelSize: 14
                        font.bold: true
                        color: "#dc2626"
                    }
                }
            }
        }
    }
}
