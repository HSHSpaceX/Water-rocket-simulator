/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.6.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QFormLayout *formLayout;
    QLabel *label_speed;
    QDoubleSpinBox *doubleSpinBox_speed;
    QLabel *label_time;
    QDoubleSpinBox *doubleSpinBox_time;
    QPushButton *pushButton_simulate;
    QLabel *label_distance;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        formLayout = new QFormLayout(centralwidget);
        formLayout->setObjectName("formLayout");
        label_speed = new QLabel(centralwidget);
        label_speed->setObjectName("label_speed");

        formLayout->setWidget(0, QFormLayout::LabelRole, label_speed);

        doubleSpinBox_speed = new QDoubleSpinBox(centralwidget);
        doubleSpinBox_speed->setObjectName("doubleSpinBox_speed");

        formLayout->setWidget(0, QFormLayout::FieldRole, doubleSpinBox_speed);

        label_time = new QLabel(centralwidget);
        label_time->setObjectName("label_time");

        formLayout->setWidget(1, QFormLayout::LabelRole, label_time);

        doubleSpinBox_time = new QDoubleSpinBox(centralwidget);
        doubleSpinBox_time->setObjectName("doubleSpinBox_time");

        formLayout->setWidget(1, QFormLayout::FieldRole, doubleSpinBox_time);

        pushButton_simulate = new QPushButton(centralwidget);
        pushButton_simulate->setObjectName("pushButton_simulate");

        formLayout->setWidget(2, QFormLayout::FieldRole, pushButton_simulate);

        label_distance = new QLabel(centralwidget);
        label_distance->setObjectName("label_distance");

        formLayout->setWidget(4, QFormLayout::FieldRole, label_distance);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 800, 21));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName("statusbar");
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        label_speed->setText(QCoreApplication::translate("MainWindow", "speed", nullptr));
        label_time->setText(QCoreApplication::translate("MainWindow", "time", nullptr));
        pushButton_simulate->setText(QCoreApplication::translate("MainWindow", "PushButton", nullptr));
        label_distance->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
