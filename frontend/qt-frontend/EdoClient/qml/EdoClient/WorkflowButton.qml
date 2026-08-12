// Wrapper for WorkflowButton.ui.qml - adds click signal emission
// Edit WorkflowButton.ui.qml in Qt Design Studio; this file handles logic
import QtQuick
import QtQuick.Layouts
import "../EdoClientContent" as Content

Item {
    id: wrapper
    width: 280
    Layout.preferredHeight: 64

    signal clicked

    // Expose properties from the UI form
    property alias iconSource: uiForm.iconSource
    property alias labelText: uiForm.labelText
    property alias description: uiForm.description

    Content.WorkflowButtonUi {
        id: uiForm
        anchors.fill: parent
        hovered: wrapperMouseArea.containsMouse
    }

    MouseArea {
        id: wrapperMouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        z: 1
        onClicked: wrapper.clicked()
    }
}
