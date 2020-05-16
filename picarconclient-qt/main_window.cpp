#include "main_window.h"
#include "./ui_main_window.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

	test_interface = new NetInterface("10.0.10.20");

	//Connect angle controls to change with one another.
	connect(ui->center_button, &QPushButton::pressed, [=]()
	{
		ui->angle_slider->setValue(0);
	});

	connect(ui->angle_slider, &QSlider::valueChanged, [=](int value)
	{
	   if(value != ui->angle_box->value())
	   {
		   ui->angle_box->setValue(value);
	   }
	});

	connect(ui->angle_box, QOverload<int>::of(&QSpinBox::valueChanged), [=](int value)
	{
		if(value != ui->angle_slider->value())
		{
			ui->angle_slider->setValue(value);
		}
	});

	//Connect speed controls to change with one another.
	connect(ui->stop_button, &QPushButton::pressed, [=]()
	{
		ui->speed_slider->setValue(0);
	});

	connect(ui->speed_slider, &QSlider::valueChanged, [=](int value)
	{
	   if(value != ui->speed_box->value())
	   {
		   ui->speed_box->setValue(value);
	   }
	});

	connect(ui->speed_box, QOverload<int>::of(&QSpinBox::valueChanged), [=](int value)
	{
		if(value != ui->speed_slider->value())
		{
			ui->speed_slider->setValue(value);
		}
	});

	test_interface->pingServer();

	connect(ui->test_packet_button, &QPushButton::pressed, [=]()
	{
		test_interface->sendState(ui->speed_box->value(), ui->angle_box->value());
	});

}

MainWindow::~MainWindow()
{
	delete(test_interface);
	delete(ui);
}

