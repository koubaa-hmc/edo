

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

    property alias toggleButton: toggleButton
    property alias sidebar: sidebar
    property alias overlay: overlay // Expose overlay to be managed outside

    Rectangle {
        anchors.fill: parent
        color: "#f5f5f5"
    }

    Button {
        id: toggleButton
        text: "Open Menu" // Default static text; MainView.qml will update it dynamically
        anchors.centerIn: parent
    }

    Rectangle {
        id: overlay
        anchors.fill: parent
        color: "#000000"
        opacity: 0.0 // Default hidden; controlled via states or MainView.qml
        visible: opacity > 0

        Behavior on opacity {
            NumberAnimation {
                duration: 250
            }
        }

        MouseArea {
            id: overlayMouse
            anchors.fill: parent
            onClicked: sidebar.state
                       = "closed" // Direct state assignment is permitted for simple triggers here
        }
    }

    SidebarMenu {
        id: sidebar
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        z: 10
    }
}
