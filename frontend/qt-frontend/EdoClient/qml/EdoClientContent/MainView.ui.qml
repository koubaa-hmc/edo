

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
    id: mainView
    width: 1280
    height: 800

    // Background
    Rectangle {
        anchors.fill: parent
        color: "#f5f5f5"
    }

    // Button to toggle the custom drawer open/closed
    Button {
        text: sidebar.state === "open" ? "Close Menu" : "Open Menu"
        anchors.centerIn: parent
    }

    // Semi-transparent backdrop overlay when drawer is open (optional)
    Rectangle {
        id: overlay
        anchors.fill: parent
        color: "#000000"
        opacity: sidebar.state === "open" ? 0.3 : 0.0
        visible: opacity > 0

        Behavior on opacity {
            NumberAnimation {
                duration: 250
            }
        }

        MouseArea {
            anchors.fill: parent
            onClicked: sidebar.state = "closed"
        }
    }

    // The Custom Sidebar Component placed on top layer
    SidebarMenu {
        id: sidebar
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        z: 10 // Ensure it sits above the background/content
    }
}
