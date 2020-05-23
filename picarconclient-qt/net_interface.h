#ifndef NETINTERFACE_H
#define NETINTERFACE_H

#include <QObject>
/* The PiCar uses a UDP multicast stream, so this class should use the QUdpSocket class for all transmission.
 *
 */
#include <QUdpSocket>
#include <QHostInfo>
#include <QNetworkInterface>

#include <QDebug>

class NetInterface : public QObject
{
    Q_OBJECT

	static const uint16_t MAGIC = 0x5049;
	static const uint16_t VERSION = 0x0001;

	enum COMMAND : uint8_t
	{
		STATE = 0x00,
		PING = 0x01
	};

	struct message
	{
		uint16_t magic = MAGIC;
		uint16_t version = VERSION;
		uint8_t sequence;
		//If command is PING, back and front are not sent, leaving the message size at 24 bytes instead of 32.
		COMMAND command;
		int8_t back;
		int8_t front;
	};

public:

	//TODO: REMOVE CONSTANTS BEFORE PRODUCTION!
	explicit NetInterface(QString init_host = "10.0.10.100", quint16 init_port = 39281);
	~NetInterface();

	void setConnection(QString new_host, quint16 new_port);

	QString getHost();
	quint16 getPort();

	bool pingServer();

	bool sendState(int new_speed = 0, int new_angle = 0);

signals:

private:

	uint8_t current_sequence = 0;

	QString local_host;
	QString host;
	quint16 port;
	QUdpSocket *socket = nullptr;

	bool sendMessage(message &m);

};

#endif // NETINTERFACE_H
