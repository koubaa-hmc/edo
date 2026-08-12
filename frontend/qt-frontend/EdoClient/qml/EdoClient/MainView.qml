import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../EdoClientContent" as Content

Item {
    id: root
    width: 1280
    height: 800

    // Instantiate the UI form from the content folder inside this wrapper
    Content.MainView {
        id: uiView
        anchors.fill: parent
    }

    // Wrapper container for the toggle button with animated positioning
    Item {
        id: toggleButtonWrapper
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: uiView.sidebar.state === "open" ? 296 : 16
        anchors.topMargin: 16
        z: 20
        width: 44
        height: 44

        Behavior on anchors.leftMargin {
            NumberAnimation {
                duration: 400
                easing.type: Easing.OutCubic
            }
        }

        // Actual button inside the wrapper
        Button {
            id: innerToggleButton
            anchors.fill: parent

            background: Rectangle {
                anchors.fill: parent
                radius: 8
                color: innerToggleButton.pressed ? "#e5e7eb" : (innerToggleButton.hovered ? "#f3f4f6" : "transparent")
            }

            contentItem: Image {
                source: "../EdoClientContent/images/icons/chevron-right.svg"
                fillMode: Image.PreserveAspectFit
                visible: status === Image.Ready
                rotation: uiView.sidebar.state === "open" ? 180 : 0

                Behavior on rotation {
                    NumberAnimation {
                        duration: 400
                        easing.type: Easing.OutCubic
                    }
                }
            }

            onClicked: {
                uiView.sidebar.state = (uiView.sidebar.state === "open") ? "closed" : "open"
            }
        }
    }

    // Hide the original button from the UI form
    Component.onCompleted: {
        uiView.toggleButton.visible = false
    }

    // Connect workflow buttons to log and emit workflowRequested signal
    Connections {
        target: uiView.sidebar.planButton
        function onClicked() {
            console.log("Navigate to: Plan")
            uiView.workflowRequested("Plan")
        }
    }

    Connections {
        target: uiView.sidebar.collectButton
        function onClicked() {
            console.log("Navigate to: Collect")
            uiView.workflowRequested("Collect")
        }
    }

    Connections {
        target: uiView.sidebar.processButton
        function onClicked() {
            console.log("Navigate to: Process")
            uiView.workflowRequested("Process")
        }
    }

    Connections {
        target: uiView.sidebar.analyzeButton
        function onClicked() {
            console.log("Navigate to: Analyze")
            uiView.workflowRequested("Analyze")
        }
    }

    Connections {
        target: uiView.sidebar.preserveButton
        function onClicked() {
            console.log("Navigate to: Preserve")
            uiView.workflowRequested("Preserve")
        }
    }

    Connections {
        target: uiView.sidebar.shareButton
        function onClicked() {
            console.log("Navigate to: Share")
            uiView.workflowRequested("Share")
        }
    }

    Connections {
        target: uiView.sidebar.reuseButton
        function onClicked() {
            console.log("Navigate to: Reuse")
            uiView.workflowRequested("Reuse")
        }
    }
}