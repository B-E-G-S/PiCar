#include "net_interface.h"

NetInterface::NetInterface(QString init_host, quint16 init_port) :
	QObject()
{
	socket = new QUdpSocket(this);

	local_host = "192.168.1.228";
	qDebug() << "local_host: " << local_host;

	setConnection(init_host, init_port);
}

NetInterface::~NetInterface()
{
	delete(socket);
}

void NetInterface::setConnection(QString new_host, quint16 new_port)
{
	host = new_host;
	port = new_port;

	socket->bind(QHostAddress(local_host), port);
}

QString NetInterface::getHost()
{
	return(host);
}

quint16 NetInterface::getPort()
{
	return(port);
}

bool NetInterface::pingServer()
{
	message to_send;
	to_send.command = PING;

	return(sendMessage(to_send));
}

bool NetInterface::sendState(int new_speed, int new_angle)
{
	message to_send;
	to_send.command = STATE;

	if(new_speed < -100 || new_speed > 100)
	{
		qDebug() << QString("Error: new_speed is out of bounds: %1").arg(new_speed);
		return(false);
	}
	to_send.back = static_cast<int8_t>(new_speed);

	if(new_angle < -90 || new_angle > 90)
	{
		qDebug() << QString("Error: new_angle is out of bounds: %1").arg(new_angle);
		return(false);
	}
	to_send.front = static_cast<int8_t>(new_angle);

	return(sendMessage(to_send));
}

bool NetInterface::sendMessage(message &m)
{
//	qDebug() << "sendMessage() NYI!";

	m.sequence = current_sequence;
	current_sequence++;

	//TODO: SEND MESSAGE!

	if(socket->isOpen())
	{
		char *raw;

		switch(m.command)
		{
		case PING:
		{
			/* We will transmit 6 bytes of data, formatted as follows:
			 * 0x5		0x4		0x3		0x2		0x1		0x0
			 * comm		seq		ver_hi	ver_lo	mag_hi	mag_lo
			 *
			 */
			raw = new char[6];
			//Magic number.
			raw[0] = m.magic & 0xff;
			raw[1] = m.magic & (0xff << 8);
			//Version.
			raw[2] = m.version & 0xff;
			raw[3] = m.version & (0xff << 8);
			//Sequence number.
			raw[4] = m.sequence;
			//Command.
			raw[5] = m.command;

//			socket->write(raw, 6);
			socket->writeDatagram(raw, 6, QHostAddress(host), port);

			break;
		}
		case STATE:
		{
			/* We will transmit 8 bytes of data, formatted as follows:
			 * 0x7		0x6		0x5		0x4		0x3		0x2		0x1		0x0
			 * front	back	comm	seq		ver_hi	ver_lo	mag_hi	mag_lo
			 *
			 */
			raw = new char[8];
			//Magic number.
			raw[0] = m.magic & 0xff;
			raw[1] = m.magic & (0xff << 8);
			//Version.
			raw[2] = m.version & 0xff;
			raw[3] = m.version & (0xff << 8);
			//Sequence number.
			raw[4] = m.sequence;
			//Command.
			raw[5] = m.command;
			//Back.
			raw[6] = m.back;
			//Front.
			raw[7] = m.front;

//			socket->write(raw, 8);
			socket->writeDatagram(raw, 8, QHostAddress(host), port);

			break;
		}
		default:
		{
			qDebug() << "Error: incorrect command: " << m.command;
			delete(raw);
			return(false);
		}
		}
	}

	return(true);
}
