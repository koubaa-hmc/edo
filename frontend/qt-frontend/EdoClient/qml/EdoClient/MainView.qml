import QtQuick
import QtQuick.Controls

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

    // Connect the button click safely using the instantiated UI form's alias
    Connections {
        target: uiView.toggleButton
        function onClicked() {
            uiView.sidebar.state = (uiView.sidebar.state === "open") ? "closed" : "open"
        }
    }

    // Sync button text and overlay opacity when sidebar state changes
    Connections {
        target: uiView.sidebar
        function onStateChanged() {
            let isOpen = (uiView.sidebar.state === "open")
            uiView.toggleButton.text = isOpen ? "Close Menu" : "Open Menu"
            uiView.overlay.opacity = isOpen ? 0.3 : 0.0
        }
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