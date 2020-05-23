# PiCar Control Server API

## Message Structure

| Field    | Type     | Description                                           |
| -------- | -------- | ----------------------------------------------------- |
| Magic    | `uint16` | Identifies PiCar message (always `0x5049`)            |
| Version  | `uint16` | PiCar version (always `0x0001`)                       |
| Sequence | `uint8`  | Sequence number for packet ordering/response matching |
| Command  | `uint8`  | Message type, determines length and contents of Data  |
| Data     | varies   | See below                                             |

## Message Types

### State

**ID:** `0x00`

This message can be sent either by the client or the server. When sent by the
client, the server is instructed to match this state. When sent as a response
by the server, this indicates the current/updated state.

| Field | Type | Description |
| - | - | - |
| Back | `int8` | Value between -100 and 100, indicates speed |
| Front | `int8` | Value between -90 and 90, indicates left/right rotation |

### Ping

**ID:** `0x01`

Sent from the client to the server to request a state message without changing
anything.

