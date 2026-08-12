import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: buttonRoot
    property alias iconSource: iconImage.source
    property alias labelText: buttonLabel.text
    property alias description: descLabel.text
    property alias mouseArea: mouseArea

    Layout.preferredHeight: 64

    Rectangle {
        id: buttonBackground
        anchors.fill: parent
        radius: 8
        color: mouseArea.containsMouse ? "#f3f4f6" : "transparent"

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
        }
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        spacing: 12

        Image {
            id: iconImage
            Layout.preferredWidth: 24
            Layout.preferredHeight: 24
            fillMode: Image.PreserveAspectFit
            visible: status === Image.Ready
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2

            Label {
                id: buttonLabel
                Layout.fillWidth: true
                font.pixelSize: 14
                font.bold: true
                color: "#1a1a1a"
            }

            Label {
                id: descLabel
                Layout.fillWidth: true
                font.pixelSize: 11
                color: "#6b7280"
            }
        }
    }
}
