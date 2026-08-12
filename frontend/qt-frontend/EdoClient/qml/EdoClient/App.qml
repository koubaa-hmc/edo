import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../EdoClientContent" as Content

ApplicationWindow {
    id: root
    visible: true
    width: 1280
    height: 800
    title: "Energy Data Orchestrator"

    // Property to control the splash state
    property bool showSplash: true

    // Timer to switch views after 4 seconds (4000 milliseconds)
    Timer {
        interval: 400
        running: true
        repeat: false
        onTriggered: {
            root.showSplash = false
        }
    }

    // Loader or conditional visibility to transition between views
    Loader {
        id: mainLoader
        anchors.fill: parent
        sourceComponent: root.showSplash ? splashComponent : mainView
    }

    // Component 1: The 4-second Splash Screen (App.ui.qml content)
    Component {
        id: splashComponent
        Content.App {
            width: root.width
            height: root.height
        }
    }

    // Component 2: The Main Application View with the Drawer
    Component {
        id: mainView
        // If MainView.qml is in EdoClient, load it directly or via your local imports:
        MainView {
            id: mainViewInstance
            width: root.width
            height: root.height
        }
    }
}
