pragma Singleton
import QtQuick

QtObject {
    /* Application dimensions */
    readonly property int width: 1920
    readonly property int height: 1080
    
    /* Font configuration */
    readonly property string relativeFontDirectory: "fonts"
    
    readonly property font font: Qt.font({
        family: Qt.application.font.family,
        pixelSize: Qt.application.font.pixelSize
    })
    
    readonly property font largeFont: Qt.font({
        family: Qt.application.font.family,
        pixelSize: Qt.application.font.pixelSize * 1.6
    })
    
    /* Color scheme - HMC corporate colors */
    readonly property color backgroundColor: "#FFFFFF"
    readonly property color primaryColor: "#00305E"
    readonly property color secondaryColor: "#004B87"
    readonly property color accentColor: "#0066CC"
    readonly property color lightGray: "#f5f5f5"
    readonly property color borderGray: "#dee2e6"
    
    /* UI spacing */
    readonly property int defaultMargin: 20
    readonly property int smallMargin: 10
    readonly property int buttonHeight: 40
    readonly property int headerHeight: 60
    readonly property int footerHeight: 30
}
