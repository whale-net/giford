from io import IOBase


DEFAULT_BUFFER_SIZE = 4096


def buffered_stream_copy(
    in_stream: IOBase, out_stream: IOBase, buffer_size: int = DEFAULT_BUFFER_SIZE
) -> None:
    """
    copies bytes from in stream to out stream using a buffer

    :param in_stream: input stream
    :param out_stream: output stream
    :param buffer_size: number of bytes to use as buffer, defaults to DEFAULT_BUFFER_SIZE
    """
    buff: bytes = in_stream.read(DEFAULT_BUFFER_SIZE)
    while len(buff) > 0:
        out_stream.write(buff)
        buff = in_stream.read(DEFAULT_BUFFER_SIZE)
