#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QUrl>
#include <QDir>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    
    app.setApplicationName("Energy Data Orchestrator");
    app.setApplicationVersion("0.1.0");
    app.setOrganizationName("EDO Team");

    QQmlApplicationEngine engine;
    
    // Set QML import paths
    const QString qmlPath = QDir::currentPath() + "/qml";
    engine.addImportPath(qmlPath);
    
    // Load main QML file
    const QUrl url(QStringLiteral("qrc:/qml/EdoClientContent/App.qml"));
    
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreated,
        &app,
        [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection
    );
    
    engine.load(url);
    
    return app.exec();
}
