import QtQuick
import EdoClient

Window {
    width: mainScreen.width
    height: mainScreen.height

    visible: true
    title: "EdoClient"

    Screen01 {
        id: mainScreen

        anchors.centerIn: parent
    }

}

