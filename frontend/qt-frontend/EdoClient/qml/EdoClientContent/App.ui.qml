import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: mainSplatch
    width: 1280
    height: 800

    // Background
    Rectangle {
        anchors.fill: parent
        color: "#f5f5f5"
    }

    // Main content area
    ColumnLayout {
        anchors.centerIn: parent
        spacing: 24

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: "Energy Data Orchestrator"
            font.pixelSize: 28
            font.bold: true
            color: "#1a1a1a"
        }

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: "Qt Design Studio - Editable UI"
            font.pixelSize: 16
            color: "#666666"
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 400
            Layout.preferredHeight: 2
            color: "#cccccc"
        }

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: "This file (App.ui.qml) can be edited in Qt Design Studio"
            font.pixelSize: 12
            color: "#999999"
        }
    }
}
