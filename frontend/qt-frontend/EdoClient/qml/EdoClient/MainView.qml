import QtQuick
import QtQuick.Controls

import "../EdoClientContent" as Content

Content.MainView {
    id: root

    // Connect the button click imperatively here, completely outside the .ui.qml file
    Connections {
        target: root.toggleButton
        function onClicked() {
            root.sidebar.state = (root.sidebar.state === "open") ? "closed" : "open"
        }
    }
}
