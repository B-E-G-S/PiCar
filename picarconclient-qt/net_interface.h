#ifndef NETINTERFACE_H
#define NETINTERFACE_H

#include <QObject>

/* The PiCar uses a UDP multicast stream, so this class should use the QUdpSocket class for all transmission.
 *
 */

#include <QUdpSocket>

class NetInterface : public QObject
{
    Q_OBJECT

public:

    explicit NetInterface(QObject *parent = nullptr);



signals:

};

#endif // NETINTERFACE_H
