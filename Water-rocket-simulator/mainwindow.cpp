#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QString>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}




void MainWindow::on_pushButton_simulate_clicked()
{
    double speed = ui->doubleSpinBox_speed->value();
    double time = ui->doubleSpinBox_time->value();
    double distance = speed*time;

    QString distanceString = QString::number(distance);
    ui->label_distance->setText(distanceString);
}

