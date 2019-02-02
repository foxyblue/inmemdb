from io import StringIO
from exceptions import CommandError, Disconnect, Error


class AbstractHandler:

    def handle_request(self, socket_file):
        """Parse a request from the client into it's component parts."""
        raise NotImplementedError

    def write_response(self, socket_file, data):
        """Serialize the response data and send it to the client."""
        raise NotImplementedError


class ProtocolHandler(AbstractHandler):

    def __init__(self):
        self.handlers = {
            b'+': self.handle_simple_string,
            b'-': self.handle_error,
            b':': self.handle_integer,
            # (byte string)
            b'$': self.handle_string,
            b'*': self.handle_array,
            b'%': self.handle_dict,
        }

    def handle_request(self, socket_file):
        first_byte = socket_file.read(1)
        if not first_byte:
            raise Disconnect()

        try:
            # Delegate to the appropriate handler based on
            # the first byte.
            return self.handlers[first_byte](socket_file)
        except KeyError:
            raise CommandError('bad request')

    def handle_simple_string(self, socket_file):
        return socket_file.readline().decode('utf-8').rstrip('\r\n')

    def handle_error(self, socket_file):
        return Error(socket_file.readline().decode('utf-8').rstrip('\r\n'))

    def handle_integer(self, socket_file):
        return int(socket_file.readline().decode('utf-8').rstrip('\r\n'))

    def handle_string(self, socket_file):
        # First read the length ($<length>\r\n).
        length = int(socket_file.readline().decode('utf-8').rstrip('\r\n'))
        if length == -1:
            # Null Case
            return None
        length += 2
        return socket_file.read(length).decode('utf-8').rstrip('\r\n')

    def handle_array(self, socket_file):
        num_elements = int(socket_file.readline().decode('utf-8').rstrip('\r\n'))
        return [self.handle_request(socket_file) for _ in range(num_elements)]

    def handle_dict(self, socket_file):
        num_items = int(socket_file.readline().decode('utf-8').rstrip('\r\n'))
        elements = [self.handle_request(socket_file)
                    for _ in range(num_items * 2)]
        return dict(zip(elements[::2], elements[1::2]))

    # Serialization
    def write_response(self, socket_file, data):
        buf = StringIO()
        self._write(buf, data)
        buf.seek(0)
        # print(buf.getvalue())
        socket_file.write(buf.getvalue().encode('utf-8'))
        socket_file.flush()

    def _write(self, buf, data):
        if isinstance(data, str):
            data = data.encode('utf-8')

        if isinstance(data, bytes):
            buf.write('$%s\r\n%s\r\n' % (len(data), data.decode('utf-8')))
        elif isinstance(data, int):
            buf.write(':%s\r\n' % data)
        elif isinstance(data, Error):
            buf.write('-%s\r\n' % data.message)
        elif isinstance(data, (list, tuple)):
            buf.write('*%s\r\n' % len(data))
            for item in data:
                self._write(buf, item)
        elif isinstance(data, dict):
            buf.write('%%%s\r\n' % len(data))
            for key in data:
                self._write(buf, key)
                self._write(buf, data[key])
        elif data is None:
            buf.write('$-1\r\n')
        else:
            raise CommandError("unrecognized type: '%s'" % type(data))
