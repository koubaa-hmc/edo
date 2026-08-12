

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: sidebarRoot
    width: 250
    height: 800

    // Expose a state property so the parent can open/close it
    state: "closed"

    // Background panel of the drawer
    Rectangle {
        id: backgroundRect
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: parent.width
        color: "#ffffff"
        border.color: "#e0e0e0"
        border.width: 1

        // Menu items layout
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            Label {
                text: "Menu"
                font.pixelSize: 20
                font.bold: true
                color: "#1a1a1a"
            }

            Button {
                Layout.fillWidth: true
                text: "Menu Item 1"
            }

            Button {
                Layout.fillWidth: true
                text: "Menu Item 2"
            }

            Item {
                Layout.fillHeight: true // Spacer push items to top
            }
        }
    }

    // Define states for open and closed positions
    states: [
        State {
            name: "closed"
            // Hide off-screen to the left
            PropertyChanges {
                target: sidebarRoot
                x: -sidebarRoot.width
            }
        },
        State {
            name: "open"
            // Slide into view
            PropertyChanges {
                target: sidebarRoot
                x: 0
            }
        }
    ]

    // Smooth sliding animation
    transitions: [
        Transition {
            from: "closed"
            to: "open"
            NumberAnimation {
                property: "x"
                duration: 250
                easing.type: Easing.OutCubic
            }
        },
        Transition {
            from: "open"
            to: "closed"
            NumberAnimation {
                property: "x"
                duration: 250
                easing.type: Easing.InCubic
            }
        }
    ]
}
