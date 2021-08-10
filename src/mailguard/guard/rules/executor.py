def execute_from_chunks(chunks):
    if chunks.delete.action_fn is not None:
        for chunk in _chunk_mail_ids(chunks.delete.mails, 200):
            mails = _transform_mail_ids(chunk)
            chunks.delete.action_fn(mails)
    if chunks.copy.action_fn is not None:
        for chunk in _chunk_mail_ids(chunks.copy.mails, 200):
            mails = _transform_mail_ids(chunk)
            chunks.copy.action_fn(mails)
    for value in chunks.move.values():
        if value.action_fn is not None:
            for chunk in _chunk_mail_ids(value.mails, 200):
                mails = _transform_mail_ids(chunk)
                value.action_fn(mails)


def _chunk_mail_ids(data, size):
    for i in range(0, len(data), size):
        yield data[i: i + size]


def _transform_mail_ids(data):
    str_ids = [dat.decode() for dat in data]
    return ",".join(str_ids)
