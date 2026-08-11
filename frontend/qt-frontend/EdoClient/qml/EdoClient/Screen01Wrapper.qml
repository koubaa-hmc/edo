/*
 * Screen01Wrapper - Logic layer for Screen01.ui.qml
 * 
 * This wrapper adds JavaScript functions that cannot be in .ui.qml files.
 * Place this file in the EdoClient folder alongside other logic components.
 * Use this component instead of Screen01.ui.qml directly in App.qml.
 */

import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts
import "../EdoClientContent"

Item {
    id: wrapper
    anchors.fill: parent
    
    // Expose signals from mainScreen for App.qml to connect to
    signal dataLoaded(var data)
    signal actionTriggered(string actionId, var params)
    signal statusMessage(string message)
    signal roleSelected(string roleId)
    
    // Current role tracking
    property string currentRole: "guest_viewer"
    
    // Content management
    property var currentData: null
    property bool contentVisible: false
    
    Screen01 {
        id: mainScreen
        anchors.fill: parent
        
        // Public API functions (these cannot be in .ui.qml)
        function displayData(data) {
            currentData = data
            contentVisible = true
            dataLoaded(data)
        }
        
        function clearData() {
            currentData = null
            contentVisible = false
        }
        
        function newWorkspace() {
            clearData()
            statusMessage("New workspace created")
        }
        
        // Handle external data changes
        onExternalDataChanged: {
            if (externalData !== null) {
                displayData(externalData)
            }
        }
        
        // Handle new workspace trigger
        onTriggerNewWorkspaceChanged: {
            if (triggerNewWorkspace) {
                newWorkspace()
                triggerNewWorkspace = false
            }
        }
        
        // Sync button checked states with currentNavIndex
        onCurrentNavIndexChanged: function(index) {
            if (mainScreen.navDatasets) mainScreen.navDatasets.checked = (index === 0)
            if (mainScreen.navTimeseries) mainScreen.navTimeseries.checked = (index === 1)
            if (mainScreen.navRdf) mainScreen.navRdf.checked = (index === 2)
            if (mainScreen.navSettings) mainScreen.navSettings.checked = (index === 3)
        }
        
        // Forward signals to wrapper
        onDataLoaded: function(data) {
            wrapper.dataLoaded(data)
        }
        onActionTriggered: function(actionId, params) {
            wrapper.actionTriggered(actionId, params)
        }
        onStatusMessage: function(message) {
            wrapper.statusMessage(message)
        }
        onRoleSelected: function(roleId) {
            wrapper.roleSelected(roleId)
        }
    }
}
