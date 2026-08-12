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
}