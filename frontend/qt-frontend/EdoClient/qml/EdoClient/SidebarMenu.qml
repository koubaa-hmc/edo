import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../EdoClientContent" as Content

Item {
    id: sidebarRoot
    width: 280
    height: 800

    // Expose a state property so the parent can open/close it
    state: "closed"

    // User info properties (set by parent)
    property string userName: "Guest User"
    property string userRole: "guest_viewer"

    // Signal for exit request
    signal exitRequested()

    // Navigation signals for workflow buttons
    signal workflowRequested(string step)

    Content.SidebarMenuUi {
        id: ui
        anchors.fill: parent
        userName: sidebarRoot.userName
        userRole: sidebarRoot.userRole
        
        onExitRequested: sidebarRoot.exitRequested()
    }

    // Wire up workflow button clicks
    Connections {
        target: ui.planButton
        function onClicked() { sidebarRoot.workflowRequested("plan") }
    }

    Connections {
        target: ui.collectButton
        function onClicked() { sidebarRoot.workflowRequested("collect") }
    }

    Connections {
        target: ui.processButton
        function onClicked() { sidebarRoot.workflowRequested("process") }
    }

    Connections {
        target: ui.analyzeButton
        function onClicked() { sidebarRoot.workflowRequested("analyze") }
    }

    Connections {
        target: ui.preserveButton
        function onClicked() { sidebarRoot.workflowRequested("preserve") }
    }

    Connections {
        target: ui.shareButton
        function onClicked() { sidebarRoot.workflowRequested("share") }
    }

    Connections {
        target: ui.reuseButton
        function onClicked() { sidebarRoot.workflowRequested("reuse") }
    }

    // Helper function to get role badge color
    function getRoleColor(role) {
        switch(role) {
            case "admin": return "#7c3aed"      // Purple
            case "data_steward": return "#059669" // Green
            case "research_fellow": return "#2563eb" // Blue
            case "guest_viewer": return "#6b7280" // Gray
            default: return "#6b7280"
        }
    }

    // Helper function to format role name for display
    function formatRoleName(role) {
        switch(role) {
            case "admin": return "ADMIN"
            case "data_steward": return "DATA STEWARD"
            case "research_fellow": return "RESEARCH FELLOW"
            case "guest_viewer": return "GUEST VIEWER"
            default: return role.toUpperCase().replace("_", " ")
        }
    }

    // Define states for open and closed positions
    states: [
        State {
            name: "closed"
            PropertyChanges {
                target: sidebarRoot
                x: -sidebarRoot.width
            }
        },
        State {
            name: "open"
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
