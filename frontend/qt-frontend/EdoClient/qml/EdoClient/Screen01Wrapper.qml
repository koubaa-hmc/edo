/*
 * Screen01Wrapper - Logic layer for Screen01.ui.qml
 * 
 * This wrapper contains ALL business logic, signals, and properties.
 * Uses Connections to hook into UI events via the mainScreen item's child scope.
 * Use this in App.qml.
 */

import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts
import "../EdoClientContent"

Item {
    id: wrapper
    anchors.fill: parent
    
    // ========== SIGNALS ==========
    signal dataLoaded(var data)
    signal actionTriggered(string actionId, var params)
    signal statusMessage(string message)
    signal roleSelected(string roleId)
    
    // ========== PROPERTIES ==========
    property var externalData: null
    property bool triggerNewWorkspace: false
    property int currentNavIndex: 0
    property string currentRole: "guest_viewer"
    property var currentData: null
    property bool contentVisible: false
    
    // ========== UI COMPONENT ==========
    Screen01 {
        id: mainScreen
        anchors.fill: parent
        
        Component.onCompleted: {
            console.log("Screen01Wrapper: Connecting button handlers...")
            
            // Connect navigation buttons
            mainScreen.navDatasets.clicked.connect(wrapper.onNavDatasetsClicked)
            mainScreen.navTimeseries.clicked.connect(wrapper.onNavTimeseriesClicked)
            mainScreen.navRdf.clicked.connect(wrapper.onNavRdfClicked)
            mainScreen.navSettings.clicked.connect(wrapper.onNavSettingsClicked)
            mainScreen.importBtn.clicked.connect(wrapper.onImportClicked)
            
            // Connect radio buttons
            mainScreen.roleGuest.toggled.connect(wrapper.onRoleToggled)
            mainScreen.roleFellow.toggled.connect(wrapper.onRoleToggled)
            mainScreen.roleSteward.toggled.connect(wrapper.onRoleToggled)
            mainScreen.roleAdmin.toggled.connect(wrapper.onRoleToggled)
            
            console.log("Screen01Wrapper: All connections established")
        }
        
        // ========== PUBLIC API FUNCTIONS ==========
        function displayData(data) {
            console.log("Displaying data:", data)
            wrapper.currentData = data
            wrapper.contentVisible = true
            wrapper.dataLoaded(data)
        }
        
        function clearData() {
            console.log("Clearing data")
            wrapper.currentData = null
            wrapper.contentVisible = false
        }
        
        function newWorkspace() {
            console.log("Creating new workspace")
            clearData()
            wrapper.statusMessage("New workspace created")
        }
    }
    
    // ========== NAVIGATION HANDLERS ==========
    function onNavDatasetsClicked() {
        console.log("Navigation: Datasets clicked")
        currentNavIndex = 0
        actionTriggered("nav.datasets", {})
    }
    
    function onNavTimeseriesClicked() {
        console.log("Navigation: Timeseries clicked")
        currentNavIndex = 1
        actionTriggered("nav.timeseries", {})
    }
    
    function onNavRdfClicked() {
        console.log("Navigation: RDF Graph clicked")
        currentNavIndex = 2
        actionTriggered("nav.rdf", {})
    }
    
    function onNavSettingsClicked() {
        console.log("Navigation: Settings clicked")
        currentNavIndex = 3
        actionTriggered("nav.settings", {})
    }
    
    function onImportClicked() {
        console.log("Action: Import clicked")
        actionTriggered("data.import", {})
    }
    
    // ========== ROLE HANDLER ==========
    function onRoleToggled() {
        if (mainScreen.roleGuest.checked) {
            console.log("Role selected: guest_viewer")
            currentRole = "guest_viewer"
            roleSelected("guest_viewer")
        } else if (mainScreen.roleFellow.checked) {
            console.log("Role selected: research_fellow")
            currentRole = "research_fellow"
            roleSelected("research_fellow")
        } else if (mainScreen.roleSteward.checked) {
            console.log("Role selected: data_steward")
            currentRole = "data_steward"
            roleSelected("data_steward")
        } else if (mainScreen.roleAdmin.checked) {
            console.log("Role selected: admin")
            currentRole = "admin"
            roleSelected("admin")
        }
    }
    
    // ========== PROPERTY WATCHERS ==========
    onExternalDataChanged: {
        if (externalData !== null) {
            console.log("External data changed, displaying...")
            mainScreen.displayData(externalData)
        }
    }
    
    onTriggerNewWorkspaceChanged: {
        if (triggerNewWorkspace) {
            console.log("Trigger new workspace detected")
            mainScreen.newWorkspace()
            triggerNewWorkspace = false
        }
    }
    
    onCurrentNavIndexChanged: {
        console.log("Nav index changed to:", currentNavIndex)
        mainScreen.navStack.currentIndex = currentNavIndex
    }
}
